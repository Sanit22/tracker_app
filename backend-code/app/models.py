from main import app as app
from app.database import db
import datetime
from datetime import datetime as dt
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import uuid

print("inside models")

bcrypt = Bcrypt(app)

print("after bcrypt models")

options = db.Table('options', 
db.Column('tracker_id', db.String, db.ForeignKey('Tracker.id'), primary_key = True),
db.Column('settings_name', db.Integer, db.ForeignKey('Settings.name'), primary_key = True))

class Tracker(db.Model):
    __tablename__ = 'Tracker'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), primary_key=True, nullable = False)
    description = db.Column(db.String)
    tracker_type = db.Column(db.String)
    settings = db.relationship('Settings', secondary = 'options', backref=db.backref('tracker', lazy='subquery'))
    logs = db.relationship('Logs', backref='tracker', lazy='subquery', cascade="all, delete")
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key = True)
    last_logged = db.Column(db.String, default="No Logs yet!")

    def __init__(self, name, description, tracker_type, user_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.tracker_type = tracker_type
        self.user_id = user_id
    
class Settings(db.Model):
    __tablename__ = 'Settings'
    name = db.Column(db.String, primary_key = True)

    def __init__(self, name):
        self.name = name

class Logs(db.Model):
    def currDateTime():
        t = datetime.timezone(datetime.timedelta(hours=5, minutes = 30))
        time = dt.now(tz=t)
        return time

    __tablename__ = 'Logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.String, db.ForeignKey('Tracker.id'))
    note = db.Column(db.String)
    value = db.Column(db.String, nullable=False)
    user_timestamp = db.Column(db.DateTime(timezone=True), default=currDateTime)
    db_timestamp = db.Column(db.DateTime(timezone=True), default=currDateTime)

    def __init__(self, note, value, tracker_id, user_timestamp):
        self.note = note
        self.value = value
        self.tracker_id = tracker_id
        if(user_timestamp != None):
            self.user_timestamp = user_timestamp
        t = datetime.timezone(datetime.timedelta(hours=5, minutes = 30))
        time = dt.now(tz=t)
        self.db_timestamp = time 
        

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    trackers = db.relationship('Tracker', backref='user', lazy='subquery')
    report_format = db.Column(db.String, default='html')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        
    

