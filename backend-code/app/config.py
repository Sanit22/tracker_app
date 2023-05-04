import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir", basedir)
print(os.path.join(basedir, 'csv_files'))

class LocalDevelopmentConfig():
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'nadfas$%3@=_dsnisvnsv!'
    SQL_DB_DIR = os.path.join(basedir, '../db_directory')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQL_DB_DIR, "trackuDb.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'fsgfsg121%#4@345dfgsdg345#53345#@11!$$56dghh#3'
    PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/api/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    MAIL_DEFAULT_SENDER = "sanit.arora19@gmail.com"
    MAIL_USERNAME = "sanit.arora19@gmail.com"
    # MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    TIMEZONE = 'Asia/Kolkata'
    CSV_FILEPATH = os.path.join(basedir, 'csv_files')
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    

class StageConfig():
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'nadfas$%3@=_dsnisvnsv!'
    SQL_DB_DIR = os.path.join(basedir, '../db_directory')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQL_DB_DIR, "trackuDb.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'fsgfsg121%#4@345dfgsdg345#53345#@11!$$56dghh#3'
    PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/api/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    MAIL_DEFAULT_SENDER = "sanit.arora19@gmail.com"
    MAIL_USERNAME = "sanit.arora19@gmail.com"
    # MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    TIMEZONE = 'Asia/Kolkata'
    REDIS_URL = 'redis://localhost:6379'
    CSV_FILEPATH = os.path.join(basedir, 'csv_files')
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379