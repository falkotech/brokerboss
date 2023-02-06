import os

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']

class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']

class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']