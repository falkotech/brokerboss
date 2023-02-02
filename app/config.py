import os

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    MONGODB_URI = os.environ['MONGODB_URI']

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    MONGODB_URI = os.environ['MONGODB_URI']

class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    MONGODB_URI = os.environ['MONGODB_URI']