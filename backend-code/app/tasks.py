from flask import current_app as app
from app.workers import celery
from celery.schedules import crontab
from app.database import db
from app.models import *
from datetime import datetime as dt
import datetime
from json import dumps
from httplib2 import Http
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from flask import render_template
from weasyprint import HTML
from email import encoders

# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=13, minute=58),
#         print_current_time_job.s(),
#  )

@celery.task()
def print_current_time_job():
    print("START")
    now = dt.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string) 
    print("COMPLETE")



@celery.task()
def test_celery():
    print("INSIDE TASK ****")
    return "HELLO FROM TASK"


@celery.task()
def evening_log_reminder():
    trackers = Tracker.query.all()
    logged = False
    t = datetime.timezone(datetime.timedelta(hours=5, minutes = 30))
    curr_time = dt.now(tz=t)
    curr_time = curr_time.strftime("%d-%m-%Y")
    for tracker in trackers:
        last_logged = tracker.last_logged.split(' ')
        last_logged = last_logged[0]
        if(last_logged == curr_time):
            logged = True
            break
    
    
    if(not logged):
        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAALDg1w4U/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=gV9dwwrY0KJfH2aIqgPLb5M6EeW5WbNvcLeDhmX37ZA%3D'
        message = {
            'text': 'Reminder: You haven\'t logged into any tracker today.'
        }
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
        uri=webhook_url,
        method='POST',
        headers=message_headers,
        body=dumps(message),
        )
        print(response)
    else:
        print("YOU ARE GOOD TO GO!")


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "sanit.arora@email.com"
SENDER_PASSWORD = "123"


@celery.task()
def monthly_report_mail():
    users = User.query.all()
    for user in users:
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
        msg = MIMEMultipart()
        if(user.report_format == 'html'):
             msg.attach(MIMEText(message, "html"))
        else:
            html = HTML(string=message)
            file_name = ""+ user.username +"monthlyreport.pdf"
            html.write_pdf(target=file_name)
            with open(file_name, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename={file_name}",
            )
            msg_body = "Hello "+user.username+", Please find the attached pdf report. Thanks"
            msg.attach(MIMEText(msg_body, "plain"))
            msg.attach(part)
        
        msg["From"] = SENDER_ADDRESS
        msg["To"] = user.email
        msg["Subject"] = "Hello "+user.username+" : Progress report"

       

        s = smtplib.SMTP(host=SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()

celery.conf.beat_schedule = {
    'evening-log-reminder': {
        'task': 'app.tasks.evening_log_reminder',
        'schedule': crontab(hour=17, minute=30),
    },
    'monthly_report_mail':{
        'task': 'app.tasks.monthly_report_mail',
        'schedule': crontab(),
    }
}

