from flask_restful import Resource, Api
from flask_restful import reqparse
from app.database import db
from main import app as app
from  app.models import User, Tracker, Logs, Settings
from flask import request,session,jsonify
from flask_bcrypt import Bcrypt
import collections 
import datetime
from datetime import datetime as dt, timezone
from flask_jwt_extended import ( 
    create_access_token, set_access_cookies, create_refresh_token,
    set_refresh_cookies, unset_jwt_cookies, get_jwt_identity, 
    jwt_required, JWTManager )
from sqlalchemy  import exc, insert
from flask_mail import Message
from flask_mail import Mail
from flask_sse import sse
from flask import Response, send_from_directory, make_response
import json
import csv
import time
from app import cache


print("inside api")

bcrypt = Bcrypt(app)

print("after bcrypt inside api")

class LoginUser(Resource):
    def get(self):
        return {"msg": "OK TESTED COOL"}
    def post(self):
        email = request.form['email']
        password = request.form['password']
       

        user = User.query.filter_by(email = email).first()
        if(user):
            pw_hash = user.password
            if(bcrypt.check_password_hash(pw_hash, password)):
                session['user_id'] = user.id
                trackers = Tracker.query.filter_by(user_id=session['user_id']).all()
                tracker_list = []
                for tracker in trackers:
                    tracker_list.append(tracker.name)
                user_email = user.email
                access_token = create_access_token(identity=user_email) 
                resp = make_response(json.dumps({'login': True}), 200)
                set_access_cookies(resp, access_token)
                return resp
            else:
               return make_response(jsonify({"msg": "Invalid email/password"}), 401)
        else:
            return make_response(jsonify({"msg": "User doesn't exist"}), 401)


class DashboardData(Resource):
    @jwt_required()
    def get(self):
        if(session['user_id']):
            print(session['user_id'])
            user_id = session['user_id']
            user_email = get_jwt_identity()
            user = User.query.filter_by(id=user_id).first()
            if(user.email == user_email):
                start = time.perf_counter()
                trackers = user.trackers
                stop = time.perf_counter()
                print("time taken", stop - start)
                allTrackers = []
                for tracker in trackers:
                    tracker_id = tracker.id
                    allLogs = list(tracker.logs)
                    tracker_info = dict()
                    tracker_info['tracker_name'] = tracker.name
                    tracker_info['tracker_id'] = tracker.id
                    tracker_info['last_logged'] = tracker.last_logged
                    allTrackers.append(tracker_info)
                print("INSIDE SERVER")
                return make_response(jsonify({
                    "dashboard_data" : allTrackers, 
                    "user_name": user.username
                    }), 200)
            else:
                return make_response(jsonify({"msg" : "Invalid id"}), 400)
        else:
            return {"msg" : "Please login first"}, 400

class CreateLogForm(Resource):
    @jwt_required()
    def get(self):
        tracker_id = request.args.get('tracker_id') 
        try:
            tracker = Tracker.query.filter_by(id=tracker_id).first()
            tracker_type = tracker.tracker_type
            tracker_name = tracker.name
            settings = tracker.settings
            tracker_settings = []
            for setting in  settings:
                tracker_settings.append(setting.name)
            return make_response(jsonify({
                'tracker_type': tracker_type,
                'tracker_settings': tracker_settings,
                'tracker_name': tracker_name
            }), 200)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify({"msg" : "Invalid Tracker id"}), 400)

class AddLog(Resource):
    @jwt_required()
    def post(self):
        tracker_id = request.args.get('tracker_id')
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        settings = tracker.settings
        setting_list = []
        for setting in settings:
            setting_list.append(setting.name)
        value = request.form['value']
        timestamp = request.form['timestamp']
        timestamp = dt.strptime(timestamp, "%Y-%m-%dT%H:%M")
        note = request.form['note']
        if(tracker.tracker_type == 'Multiple Choice' or tracker.tracker_type == 'Boolean'):
            if(value not in setting_list):
                return make_response(jsonify({
                    'msg': 'Invalid form data. Please refill.'
                }), 400)
        try:
            new_log = Logs(note, value, tracker_id, timestamp)
            tracker.last_logged = timestamp.strftime("%d-%m-%Y at %H:%M")
            db.session.add(new_log)
            db.session.commit()
            return make_response(jsonify({
                'msg': 'Successfully added log. Keep logging!',
            }), 200)
    
        except exc.SQLAlchemyError as e:
            print(type(e))
            db.session.rollback()
            return make_response(jsonify({
                    'msg': 'Error occurred while adding in database.',
            }), 400)

class ViewLogs(Resource):
    @jwt_required()
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        user_name = user.username
        logs = []
        tracker_id = request.args.get('tracker_id')
        try:
            tracker = Tracker.query.filter_by(id=tracker_id).first()
            allLogs = tracker.logs
            tracker_name = tracker.name
            for log in allLogs:
                new_dict = dict()
                new_dict['log_id'] = log.id
                new_dict['note'] = log.note
                new_dict['value'] = log.value
                new_dict['timestamp'] = log.user_timestamp
                logs.append(new_dict)
            return make_response(jsonify({'logs': logs, 'tracker_name':tracker_name, 'user_name':user_name, 'tracker_type': tracker.tracker_type}), 200)
        except exc.SQLAlchemyError as e:
            print(type(e))
            db.session.rollback()
            return make_response(jsonify({'msg': 'Something went wrong'}), 400)

class EditLogForm(Resource):
    @jwt_required()
    def get(self):
        tracker_id = request.args.get('tracker_id')
        log_id = request.args.get('log_id')
        try:
            tracker = Tracker.query.filter_by(id=tracker_id).first()
            tracker_settings = []
            settings = tracker.settings
            for setting in settings:
                tracker_settings.append(setting.name)
            log = Logs.query.filter_by(id=log_id).first()
            note = log.note
            value = log.value
            timestamp = log.user_timestamp.strftime("%Y-%m-%dT%H:%M")
            log_data = {
                'log_id': log.id,
                'note': note,
                'value':value,
                'timestamp':timestamp,
            }

            return make_response(jsonify({'log_data':log_data, 'tracker_settings':tracker_settings, 'tracker_type':tracker.tracker_type, 'tracker_name':tracker.name}), 200)    
        except exc.SQLAlchemyError as e:
            print(type(e))  
            return make_response(jsonify({'msg': 'Unable to edit log!!'}), 400)
            

class EditLog(Resource):
    @jwt_required()
    def post(self):
        log_id = request.args.get('log_id')
        tracker_id = request.args.get('tracker_id')
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        log = Logs.query.filter_by(id=log_id).first()
        try:
            log.note = request.form['note']
            log.value = request.form['value']
            new_timestamp = dt.strptime(request.form['timestamp'], "%Y-%m-%dT%H:%M")
            log.user_timestamp = new_timestamp
            t = datetime.timezone(datetime.timedelta(hours=5, minutes = 30))
            time = dt.now(tz=t)
            tracker.last_logged = time.strftime("%d-%m-%Y at %H:%M")
            t = datetime.timezone(datetime.timedelta(hours=5, minutes = 30))
            log.db_timestamp = dt.now(tz=t)
            db.session.commit()
            return make_response(jsonify({'msg': 'Log edited successfully!!'}), 200)
        except exc.SQLAlchemyError as e:
            print(type(e))  
            return make_response(jsonify({'msg': 'Unable to edit log!!'}), 400)
        
class DeleteLog(Resource):
    @jwt_required()
    def get(self):
        log_id = request.args.get('log_id')
        log = Logs.query.filter_by(id=log_id).first()
        try:
            db.session.delete(log)
            db.session.commit()
            return make_response(jsonify({'msg': 'Log deleted successfully!!'}), 200)
        except exc.SQLAlchemyError as e:
            print(type(e))
            return make_response(jsonify({'msg': 'Unable to delete log'}), 400)
        
class CreateTracker(Resource):
    @jwt_required()
    def post(self):
        print(request.form)
        tracker_name = request.form['tracker_name']
        description = request.form['description']
        tracker_type = request.form['tracker_type']
        tracker_settings = ''
        if tracker_type == 'Boolean':
            tracker_settings = 'Yes,No'

        else:
            tracker_settings = request.form['settings']
    
        tracker_settings = tracker_settings.split(',')
        user_id = session['user_id']
        try:
            new_tracker = Tracker(tracker_name, description, tracker_type, user_id)
            db.session.add(new_tracker)
            db.session.commit()
            #if any setting already exists -- no need to add it
            settings_query = Settings.query.all()
            setting_list = []
            for setting in settings_query:
                setting_list.append(setting.name)
            print(setting_list)
            for setting in tracker_settings:
                print(setting_list)
                print(setting)
                if(setting in setting_list):
                    new_setting = Settings.query.filter_by(name=setting).first()
                else:
                    try:
                        new_setting = Settings(setting)
                        setting_list.append(setting)
                        print(setting_list)
                        db.session.add(new_setting)
                        db.session.commit()
                    except exc.SQLAlchemyError as e:
                        db.session.rollback()
                        print(type(e))
                        print("ERROR IN ADDING SETTINGS")
                #add to the table options
                new_tracker.settings.append(new_setting)
                db.session.commit()
            print(new_tracker.settings)
            return make_response(jsonify({'msg': 'Tracker added successfully!!'}), 200)  

        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(type(e))
            return make_response(jsonify({'msg': 'ERROR WHILE ADDING TO DB!!'}), 400)

class EditTrackerForm(Resource):
    @jwt_required()
    def get(self):
        tracker_id = request.args.get('tracker_id')
        tracker = Tracker.query.filter_by(id=tracker_id).first()
        try:
            tracker_name = tracker.name
            tracker_type = tracker.tracker_type
            description = tracker.description
            settings = tracker.settings
            tracker_settings = []
            for setting in settings:
                tracker_settings.append(setting.name)
            tracker_details = {
                'tracker_name': tracker_name,
                'tracker_type': tracker_type,
                'description': description,
                'tracker_settings': tracker_settings
            }
            return make_response(jsonify({'tracker_details': tracker_details}), 200)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(type(e))
            return make_response(jsonify({'msg': 'ERROR WHILE FETCHING TRACKER DETAILS!!'}), 400)

class EditTracker(Resource):
    @jwt_required()
    def post(self):
        tracker_id = request.args.get('tracker_id')
        try:
            tracker = Tracker.query.filter_by(id=tracker_id).first()
            print(request.form)
            tracker.name = request.form['tracker_name']
            tracker.description = request.form['description']
            new_tracker_type = request.form['tracker_type']
            print(new_tracker_type)
            db.session.commit()
            old_tracker_type = tracker.tracker_type
            tracker.tracker_type = new_tracker_type
            print(old_tracker_type)
            #if tracker type changes #remove all existing logs
            if(new_tracker_type != old_tracker_type):
                #remove all logs
                print("INSIDE OLD NEW")
                logs = tracker.logs
                for log in logs:
                    db.session.delete(log)
                    db.session.commit()

            tracker_settings = ''
            if new_tracker_type == 'Boolean':
                tracker_settings = 'Yes,No'
            else:
                tracker_settings = request.form['settings']
        
            tracker_settings = tracker_settings.split(',')
            old_settings = []
            curr_settings = tracker.settings
            for setting in curr_settings:
                old_settings.append(setting.name)

            #if new settings are different from old settings -- unlink previous then add new
            if collections.Counter(old_settings) != collections.Counter(tracker_settings):
                print("SETTINGS CHANGED  ** * ** * ")
                
                print(tracker.settings)
            
                for setting in old_settings:
                    del_setting = Settings.query.filter_by(name=setting).first()
                    tracker.settings.remove(del_setting) 
                
                print("AFTER DELETING", tracker.settings)


                settings_query = Settings.query.all()
                setting_list = []
                for setting in settings_query:
                    setting_list.append(setting.name)
                for setting in tracker_settings:
                    new_setting = setting
                    if(setting in setting_list):
                        new_setting = Settings.query.filter_by(name=setting).first()
                    else:
                        try:
                            new_setting = Settings(setting)
                            setting_list.append(setting)
                            db.session.add(new_setting)
                            db.session.commit()
                        except exc.SQLAlchemyError as e:
                            db.session.rollback()
                            print(type(e))
                            print("ERROR IN ADDING SETTINGS")
                    #add to the table options
                    tracker.settings.append(new_setting)
                    print(new_setting.name)
                    db.session.commit()
                new_set = tracker.settings
                for s in new_set:
                    print("NEW SETTING", s.name)


            return make_response(jsonify({'msg': 'Tracker edited successfully'}), 200)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(type(e))
            return make_response(jsonify({'msg': 'ERROR WHILE FETCHING TRACKER DETAILS!!'}), 400)
    
class DeleteTracker(Resource):
    @jwt_required()
    def get(self):
        tracker_id = request.args.get('tracker_id')
        try:
            tracker = Tracker.query.filter_by(id=tracker_id).first()
            db.session.delete(tracker)
            db.session.commit()
            return make_response(jsonify({'msg': 'Sucessfully deleted tracker'}), 200)
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(type(e))
            return make_response(jsonify({'msg': 'ERROR WHILE REMOVING TRACKER!!'}), 400)

class LogoutUser(Resource):
    @jwt_required()
    def get(self):
        session['user_id'] = None
        resp = make_response(jsonify({'logout': True}), 200)
        unset_jwt_cookies(resp)
        return resp

class SignUpUser(Resource):
    def post(self):
        #validate form data pending
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            new_user = User(name, email, password)
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'msg': 'User added successfully!'}), 200)
        except exc.SQLAlchemyError as e:
            print(type(e))
            db.session.rollback()
            return make_response(jsonify({
                'msg': 'Error occurred while adding in database.'
            }), 400)

class ChangeReportFormat(Resource):
    @jwt_required()
    def get(self):
        new_format = request.args.get("format")
        if(session['user_id']):
            user_email = get_jwt_identity()
            user = User.query.filter_by(email=user_email).first()
            user.report_format = new_format
            db.session.commit()
            return make_response(jsonify({
                'msg': 'Successfully changed format!'
            }), 200)
        else:
            return make_response(jsonify({
                'msg': 'User not found!'
            }), 400)
            
class ExportTrackers(Resource):
    @jwt_required()
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        header = ['Tracker name', 'Tracker Type', 'Description', 'Settings']
        trackers = user.trackers
        tracker_list = []
        for tracker in trackers:
            curr_tracker = [tracker.name, tracker.tracker_type, tracker.description]
            settings = ""
            for setting in tracker.settings:
                settings += setting.name + ","
            settings = settings[:-1]
            curr_tracker.append(settings)
            tracker_list.append(curr_tracker)
        
        try:
            with open(""+app.config["CSV_FILEPATH"]+"/"+user.username+"_trackers.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(tracker_list)
                return Response(f'data:{"csv created"} \n\n', mimetype='text/event-stream', status=200)
        except BaseException as err:
            print(err, type(err))
            return Response(f'data:{"Unable to create csv"} \n\n', mimetype='text/event-stream', status=400)
        
class DownloadTrackers(Resource):
    @jwt_required()
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        filename = ""+user.username+"_trackers.csv" 
        file = open(''+app.config["CSV_FILEPATH"]+'/'+filename+'', 'rb') 
        response = make_response(file.read())
        response.headers.set('Content-Type', 'text/csv')
        response.status_code = 200
        response.headers.set(
            'Content-Disposition', 'attachment', filename=filename)
        return response
    
class ExportLogs(Resource):
    @jwt_required()
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        trackers = user.trackers
        header = ['Tracker name', 'Note', 'Options', 'Value', 'Timestamp']
        log_list = []
        
        for tracker in trackers:
            logs = tracker.logs
            settings = tracker.settings
            sett_name = ""
            for setting in settings:
                sett_name += setting.name + ','
            sett_name = sett_name[:-1]            
            for log in logs:
                li = [tracker.name, log.note, sett_name, log.value, log.user_timestamp]
                log_list.append(li)
        
        try:
            with open(""+app.config["CSV_FILEPATH"]+"/"+user.username+"_logs.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(log_list)
                return Response(f'data:{"csv created"} \n\n', mimetype='text/event-stream', status=200)
        except BaseException as err:
            print(err, type(err))
            return Response(f'data:{"Unable to create csv"} \n\n', mimetype='text/event-stream', status=400)
        

class DownloadLogs(Resource):
    @jwt_required()
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        filename = ""+user.username+"_logs.csv" 
        file = open(''+app.config["CSV_FILEPATH"]+'/'+filename+'', 'rb') 
        response = make_response(file.read())
        response.status_code = 200
        response.headers.set('Content-Type', 'text/csv')
        response.headers.set(
            'Content-Disposition', 'attachment', filename=filename)
        return response
    
class getChartData(Resource):
    @jwt_required()
    def get(self):
        tracker_id = request.args.get('tracker_id')
        try:
            tracker = Tracker.query.filter_by(id=tracker_id).first()
            
            labels_mb = []
            labels_nt = []
            data_dict = dict()
            
            # if mc or bool
            # data['yes'] = 40, data['no] = 60 and so....
            # if num or time
            # [4,5,6,7,3,1]
            
            for setting in tracker.settings:
                labels_mb.append(setting.name)
                if(tracker.tracker_type == 'Multiple Choice' or tracker.tracker_type == 'Boolean'):
                    data_dict[setting.name] = 0
            
            for log in tracker.logs:
                if(tracker.tracker_type == 'Multiple Choice' or tracker.tracker_type == 'Boolean'):
                    data_dict[log.value] += 1
                else:
                    timestring = log.user_timestamp.strftime('%d %b,%Y')
                    labels_nt.append(timestring)
                    data_dict[timestring] = log.value
            
            return make_response(jsonify({
                'labels_mb': labels_mb,
                'labels_nt': labels_nt,
                'data_dict': data_dict
            }), 200)
        except exc.SQLAlchemyError as e:
            print(type(e))
            return make_response(jsonify({'msg': 'Error while fetching tracker details'}), 400)
            
            