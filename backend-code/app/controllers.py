from main import app as app
from app.database import db
from app.models import *
from flask import render_template, redirect, flash, url_for, request, session, send_file
from .forms import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy  import exc, insert
from flask_bcrypt import Bcrypt
import datetime
from datetime import datetime as dt, timezone
import calendar
from calendar import month_abbr
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from matplotlib.figure import Figure
from app import tasks
from weasyprint import HTML
from flask import send_file
from flask_sse import sse
from flask import Response, make_response
import time
import csv
from app import cache

print("Inside controllers")
bcrypt = Bcrypt(app)
print("after bcrypt controllers")

# @app.route('/testtemplate', methods=["GET","POST"])
# def test_template():
#     return render_template('test_sse.html')

# @app.route('/testsse', methods=["GET","POST"])
# def publish_hello():
#     sse.publish({"message": "Hello!"}, type='greeting')
#     return "Message sent!"

@app.route('/test_download')
def test_download():
    file = open(''+app.config["CSV_FILEPATH"]+'/Neil_trackers.csv', 'rb') 
    response = make_response(file.read())
    response.headers.set('Content-Type', 'text/csv')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='test.csv')
    return response


@app.route('/test_stream')
def stream():
    try:
        with open('names.csv', 'w', newline='') as csvfile:
            fieldnames = ['first_name', 'last_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
            writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
        # def get_data():
        #     while True:
        #         time.sleep(1)
        #         yield f'data: {"trackers"} \n\n'
        # return Response(get_data(), mimetype='text/event-stream')
        return Response(f'data:{"csv created"} \n\n', mimetype='text/event-stream')
    except:
        print("Unable to create csv file")
        return Response(f'data:{"unable to create csv"} \n\n', mimetype='text/event-stream')
    
        
@app.route('/testcelery')
def testcelery():
    job = tasks.test_celery.delay()
    return str(job), 200    

@app.route('/')
def index():
    login_form = Login_form()
    sign_up_form = Sign_up_form()
    return render_template('index.html', login_form = login_form, sign_up_form = sign_up_form)

@app.route('/testreport')
def testreport():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    trackers = user.trackers
    tracker_count = len(trackers)
    logs_count = dict()
    value_summary = dict()
    for tracker in trackers:
        num_logs = len(tracker.logs)
        logs_count[tracker.name] = num_logs
        if(tracker.tracker_type == 'Numerical' or tracker.tracker_type == 'Time Duration'):
            sum_val = 0
            avg = 0
            for log in tracker.logs:
                sum_val += (int)(log.value)
            if(num_logs != 0):
                avg = sum_val // num_logs
            value_summary[tracker.name] = "Average = " + (str)(avg) + " " + tracker.settings[0].name
        else:
            proportion = dict()
            for setting in tracker.settings:
                proportion[setting.name] = 0
            if(num_logs != 0):
                for log in tracker.logs:
                    proportion[log.value] += 1
                for keys in proportion:
                    proportion[keys] = (str)(int((proportion[keys] / num_logs) * 100)) + "%"
            value_summary[tracker.name] = proportion
        
    message = render_template('monthly_progress.html', user = user, trackers = trackers, tracker_count = tracker_count, logs_count=logs_count, value_summary=value_summary)
    html = HTML(string=message)
    file_name = "testreport.pdf"
    html.write_pdf(target=file_name)
    return {'status': 'okay'}

@app.route('/sign-up', methods=["POST", "GET"])
def signup():
    form = Sign_up_form()
    print("INSIDE SIGN UPP")
    # if(form.validate_on_submit()):
    #     name = form.name.data
    #     email = form.email.data
    #     password = form.password.data
    #     try:
    #         new_user = User(name, email, password)
    #         db.session.add(new_user)
    #         db.session.commit()
    #     except IntegrityError:
    #         db.session.rollback()
    #         flash('User already exists')
    #         return redirect(url_for('index'))
    #     session['user_id'] = new_user.id
    #     return redirect(url_for('dashboard'))
    # else:
    #     flash('Invalid credentials! Please try again.')
    #     print(form.errors)
    #     return redirect(url_for('index'))
    return render_template('sign_up.html')

@app.route('/login', methods=["POST"])
def login():
    error = None
    login_form = Login_form()
    if login_form.validate_on_submit():

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email = email).first()
        if(user):
            pw_hash = user.password
            if(bcrypt.check_password_hash(pw_hash, password)):
                print("INSIDE VALID PASSWORD**")
                session['user_id'] = user.id
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email/password!', 'error')
                return render_template('index.html', login_form = login_form)
        else:
            print("INSIDE INVALID USERNAME/PASS")
            error = 'Invalid email/password!'
            return render_template('index.html', error=error, login_form = login_form)
    else:
        flash('Something went wrong!', 'error')
        return render_template('index.html', login_form = login_form)



@app.route('/dashboard')
def dashboard():
    print(session)
    if(session.get('user_id')):
        x = [5,8,19,40,3,9]
        y = [12,5,8,45,2,53]
        fig = Figure()
        ax = fig.subplots()
        ax.plot(x,y)
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        # trackers = cache.dashboard_data(session['user_id'])
        start = time.perf_counter()
        trackers = Tracker.query.filter_by(user_id=session['user_id']).all()
        stop = time.perf_counter()
        print("Time taken",stop - start)  
        username = User.query.filter_by(id=session['user_id']).first().username
        print("UTC NOW", dt.utcnow())
        print("timezone", dt.now(timezone.utc)) 
        curr_time = dt.utcnow()
        print(type(curr_time))
        print(type(curr_time.strftime("%b-%-d %-I:%-M %p")))
        month_num = dt.now().month
        print(month_abbr[month_num])
        # for tracker in trackers:
        #     last_logged = tracker.last_logged.split(' ')
        #     last_logged = last_logged[0]
        #     print(last_logged)

        return render_template('dashboard.html', trackers = trackers, data=data, username=username)    
    else:
        flash('Please login/signup')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session['user_id'] = None
    return redirect(url_for('index'))   

@app.route('/create_tracker')
def create_tracker():
    form = Create_tracker_form()
    return render_template('tracker_form.html', form = form)

@app.route('/add_tracker', methods = ['GET', 'POST'])
def add_tracker():
    form = Create_tracker_form()
    if form.validate_on_submit():

        print("FORM VALIDATED****")
        name = form.name.data
        tracker_type = form.tracker_type.data
        
        description = form.description.data
        if(tracker_type == 'Boolean'):
            tracker_settings = 'Yes,No'
        else:
            tracker_settings = form.tracker_settings.data
        tracker_settings = tracker_settings.split(',')
        user_id = session['user_id']
        try:
            new_tracker = Tracker(name, description, tracker_type, user_id)
            db.session.add(new_tracker)
            db.session.commit()
            #if any setting already exists -- no need to add it
            settings_query = Settings.query.all()
            setting_list = []
            for setting in settings_query:
                setting_list.append(setting.name)
            for setting in tracker_settings:
                if(setting in setting_list):
                    new_setting = Settings.query.filter_by(name=setting).first()
                else:
                    new_setting = Settings(setting)
                    db.session.add(new_setting)
                    db.session.commit()
                #add to the table options
                new_tracker.settings.append(new_setting)
                db.session.commit()
            

        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(type(e))
            raise(e)
            flash('ERROR --  Make sure the tracker has a unique name')
            return redirect(url_for('create_tracker'))
        return redirect(url_for('dashboard'))
    else:
        print("FORM INVALIDATED****")
        flash('Invalid form data')
        return redirect(url_for('create_tracker'))
    
@app.route('/create_log/<tracker_id>', methods = ['GET', 'POST'])
def create_log(tracker_id):
    form = Create_log_form()
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    timestamp = dt.utcnow()
    timestamp = timestamp.strftime("%Y-%m-%dT%H:%M")
    print(type(timestamp))
    for setting in tracker.settings:
        print(setting.name)
    return render_template('create_log_form.html', form = form, tracker = tracker, timestamp=timestamp)

@app.route('/add_log/<tracker_id>', methods=['GET', 'POST'])
def add_log(tracker_id):

    form = Create_log_form()
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    if( form.validate_on_submit()):
        #validate choices for multiple choice and boolean
        settings = tracker.settings
        setting_list = []
        for setting in settings:
            setting_list.append(setting.name)
        print(setting_list)
        print(form.data)
        value = form.value.data
        timestamp = form.timestamp.data
        print(timestamp)
        timestamp = dt.strptime(timestamp, "%Y-%m-%dT%H:%M")
        print(type(timestamp))
        print(value)
        if(tracker.tracker_type == 'Multiple Choice' or tracker.tracker_type == 'Boolean'):
            if(value not in setting_list):
                flash('Invalid form data. Please refill.')
                return redirect(url_for('create_log', tracker_id=tracker_id))
        try:
            new_log = Logs(form.note.data, value, tracker_id, timestamp)
            tracker.last_logged = timestamp.strftime("%d-%m-%Y at %H:%M")
            db.session.add(new_log)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(type(e))
            db.session.rollback()
            flash('ERROR OCCURRED WHILE ADDING LOG')
            raise e
            # return redirect(url_for('create_log', tracker_id=tracker_id))
        
        #update to viewlogs url and add a message 'log added successfully'
        return redirect(url_for('view_logs', tracker_id=tracker_id))

@app.route('/delete_tracker/<tracker_id>')
def delete_tracker(tracker_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    if(tracker):
        db.session.delete(tracker)
        db.session.commit()
        flash('Tracker deleted successfully')
        #TO DO --if any other tracker is not sharing these settings -- delete them
        return redirect(url_for('dashboard'))
    else:
        flash('Deletion error. Please try again')
        return redirect(url_for('dashboard'))

@app.route('/view_logs/<tracker_id>')
def view_logs(tracker_id):
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    if(tracker):
        tracker_name = tracker.name
        logs = tracker.logs
        # add scatter plot
        values = []
        dates = []
        timestamps = []
        for log in logs:
            values.append(log.value)
            date = log.user_timestamp.strftime("%Y-%m-%d")
            date = date.split('-')
            month = month_abbr[int(date[1])]
            timestamp = log.user_timestamp.strftime("%Y-%m-%d at %H:%M")
            print(timestamp)
            timestamps.append(timestamp)
            day = date[2]
            date = day + '-' + month
            dates.append(date)
        fig = Figure()
        ax = fig.subplots()
        ax.plot(values,dates)
        ax.set_xlabel('Values')
        ax.set_ylabel('Dates')
        # Save it to a temporary buffer.
        buf = BytesIO() 
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return render_template('view_logs.html', logs = logs, tracker_id=tracker_id, data=data, tracker_name=tracker_name, timestamps=timestamps)
    else:
        flash('Error in viewing logs')
        return redirect(url_for('dashboard'))

@app.route('/delete_log/<tracker_id>/<log_id>')
def delete_log(tracker_id, log_id):
    log = Logs.query.filter_by(id=log_id).first()
    try:
        db.session.delete(log)
        db.session.commit()
        flash('Log deleted successfully')
    except:
        flash('Error in deleting log')
    return redirect(url_for('view_logs', tracker_id=tracker_id))

@app.route('/edit_tracker/<tracker_id>', methods=['GET', 'POST'])
def edit_tracker(tracker_id):
    form = Create_tracker_form()
    tracker = Tracker.query.filter_by(id=tracker_id).first()
    time_settings = ['hours', 'minutes']
    

    if(request.method == 'POST' and form.validate_on_submit()):
        print(form.data)
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        tracker.name = form.name.data
        tracker.description = form.description.data
        db.session.commit()
        if(tracker.tracker_type != form.tracker_type.data):
            tracker.tracker_type = form.tracker_type.data
            #remove all logs
            logs = tracker.logs
            for log in logs:
                db.session.delete(log)
                db.session.commit()

        #remove(unlink) all existing settings
        
        curr_settings = tracker.settings
        print(curr_settings)
        for setting in curr_settings:
            print("Set -- ", setting.name)
            tracker.settings.remove(setting)
        print(tracker.settings)
        #if its a new setting add it to settings else don't
        settings_list = []
        if(form.tracker_type.data == 'Boolean'):
            settings_list = ['Yes', 'No']
        elif(form.tracker_type.data == 'Numerical'):
            setting_data = form.tracker_settings.data
            settings_list.append(setting_data)
        elif(form.tracker_type.data == 'Multiple Choice' or form.tracker_type.data == 'Time Duration'):
            setting_data = form.tracker_settings.data
            print(setting_data)
            settings_list = setting_data.split(',')
        print(settings_list)
        for setting in settings_list:
            #query the setting -- if found add to tracker else create a new setting 
            new_setting = Settings.query.filter_by(name=setting).first()
            if(not new_setting):
                new_setting = Settings(setting)
                db.session.add(new_setting)
                db.session.commit()
            tracker.settings.append(new_setting)
            db.session.commit()

        return redirect(url_for('dashboard'))
    # else:
    #     flash('Invalid form data -- Could not be edited')
    #     return redirect(url_for('edit_tracker', tracker_id = tracker.id))



    #give me a pre filled tracker form and the ability to make changes
    #what will happen to the logs if u change the tracker type
    # if tracker type changes -- give the user a warning that all his logs will be deleted -- if yes delete all
    print("FORM NOT VALIDATED ** ")
    form.name.data = tracker.name
    form.tracker_type.data = tracker.tracker_type
    form.description.data = tracker.description
    setting_str = ""
    for setting in tracker.settings:
        setting_str += setting.name + ','
    setting_str = setting_str[:-1]
    form.tracker_settings.data = setting_str
    
    return render_template('edit_tracker.html', form = form, tracker_id=tracker_id)


@app.route('/edit_log/<tracker_id>/<log_id>', methods=['GET', 'POST'])
def edit_log(tracker_id, log_id):
    form = Create_log_form()
    log = Logs.query.filter_by(id=log_id).first()
    tracker = Tracker.query.filter_by(id=tracker_id).first()

    if(request.method == 'POST' and form.validate_on_submit()):
        print("INSIDE FORM")
        try:
            log.note = form.note.data
            log.value = form.value.data
            #this is a temporary solution to creating and editing timestamps
            print(form.timestamp.data)
            new_timestamp = dt.strptime(form.timestamp.data, "%Y-%m-%dT%H:%M")
            log.user_timestamp = new_timestamp
            t = datetime.timezone(datetime.timedelta(hours=5, minutes = 30))
            time = dt.now(tz=t)
            tracker.last_logged = time.strftime("%d-%m-%Y at %H:%M")
            t = datetime.timezone(datetime.timedelta(hours=5, minutes = 30))
            log.db_timestamp = dt.now(tz=t)
            print("INSIDE EDIT LOG")
            db.session.commit()
            return redirect(url_for('view_logs', tracker_id=tracker_id))   
        except exc.SQLAlchemyError as e:
            print("INSIDE ERROR")
            print(type(e))
            flash('error in editing log')
            return redirect(url_for('edit_log', tracker_id=tracker_id, log_id=log_id))
        
    print("OUTSIDE FORM")
    form.note.data = log.note
    form.value.data = log.value
    timestamp = log.user_timestamp.strftime("%Y-%m-%dT%H:%M")
    
    
    return render_template('edit_log.html', form=form, log_id=log_id, tracker_id=tracker_id, timestamp=timestamp)