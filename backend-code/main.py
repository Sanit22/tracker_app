import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Resource, Api
from app.config import LocalDevelopmentConfig, StageConfig
from app.database import db
from flask_cors import CORS
from flask_mail import Mail
from app import workers
from flask_sse import sse
from flask_redis import Redis
from flask_caching import Cache



from flask_jwt_extended import ( 
    create_access_token, set_access_cookies, create_refresh_token,
    set_refresh_cookies, unset_jwt_cookies, get_jwt_identity, 
    jwt_required, JWTManager )


app = None
api = None
celery = None
redis = Redis()
cache = None

def create_app():
    app = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    elif(os.getenv('ENV', "development") == 'stage'):
      print("Starting staging environment")
      app.logger.info("Starting staging environment.")
      app.config.from_object(StageConfig)
    else:
      app.logger.info("Starting Local Development.")
      print("Starting Local Development")
      app.config.from_object(LocalDevelopmentConfig)

    print("staging config done")
    with app.app_context():
      db.init_app(app)
    print("db config done")
    app.logger.info("App setup complete")
    # Setup Flask-Security
    # user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    # security = Security(app, user_datastore)
    # user_datastore.create_user(username="thejeshgn",email='i@thejeshgn.com', password=utils.hash_password('password'), active=1)
    # db.session.commit()   
    with app.app_context():
      mail = Mail(app) 
      api = Api(app)
    print("mail,api config done")
    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone =  app.config["TIMEZONE"]
    )

    with app.app_context():
      celery.Task = workers.ContextTask
      CORS(app, supports_credentials=True)
      jwt = JWTManager(app)   
    
    cache = Cache(app)
    app.app_context().push()   
    print("celery, cors, jwt config done")
    return app, api, jwt, mail, celery, cache

app, api, jwt, mail, celery, cache = create_app()
redis.init_app(app)

#flask sse setup

app.register_blueprint(sse, url_prefix='/stream')
print("blueprint config done")

@app.route('/testtemplate', methods=["GET","POST"])
def test_template():
    return render_template('test_sse.html')

@app.route('/testsse', methods=["GET","POST"])
def publish_hello():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"



from app.controllers import * 


from app.api import ( LoginUser, SignUpUser, DashboardData, CreateLogForm, AddLog, ViewLogs, EditLogForm, 
EditLog, DeleteLog, CreateTracker, EditTrackerForm, EditTracker, DeleteTracker, LogoutUser, 
ChangeReportFormat, ExportTrackers, DownloadTrackers, ExportLogs, DownloadLogs, getChartData )

class HelloWorld(Resource):
    def get(self):
        return {'msg': 'Hello world'}

api.add_resource(HelloWorld, '/testapi')
api.add_resource(SignUpUser, '/api/signup')
api.add_resource(LoginUser, '/api/login')
api.add_resource(CreateLogForm, '/api/create_log_form')
api.add_resource(AddLog, '/api/add_log')
api.add_resource(ViewLogs, '/api/view_logs')

api.add_resource(EditLogForm, '/api/edit_log_form')
api.add_resource(EditLog, '/api/edit_log')
api.add_resource(DeleteLog, '/api/delete_log')
api.add_resource(CreateTracker, '/api/create_tracker')
api.add_resource(EditTrackerForm, '/api/edit_tracker_form')
api.add_resource(EditTracker, '/api/edit_tracker')

api.add_resource(DeleteTracker, '/api/delete_tracker')
api.add_resource(LogoutUser, '/api/logout')

api.add_resource(ChangeReportFormat, '/api/change_format')

api.add_resource(DashboardData, '/api/dashboard')

api.add_resource(ExportTrackers, '/api/export_trackers')
api.add_resource(DownloadTrackers, '/api/download_trackers')
api.add_resource(ExportLogs, '/api/export_logs')
api.add_resource(DownloadLogs, '/api/download_logs')
api.add_resource(getChartData, '/api/getchartdata')

if __name__ == "__main__":
  app.run()