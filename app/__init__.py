"""The application factory for the Flask app."""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import logging
from .database_manager import DatabaseManager
import os


db = DatabaseManager()

flask_bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_object):

    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # set up the database connection
    connection_string = os.environ.get('MONGODB_URI')
    db.connect_to_database(connection_string, testing=app.testing)
    # connect to db manager via the app. This is used in tests
    app.db = db
    
    # load general settings
    app.settings = db.load_general_settings()
    
    # Initialize Flask extensions
    flask_bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "Please log in to access this page." # Default msg = "Please log in to access this page." 
    login_manager.login_message_category = "danger"
    
    # Register API blueprints here
    from app.api.user.routes import user
    app.register_blueprint(user)
    from app.api.broker.routes import broker
    app.register_blueprint(broker)
    # Register WEBUI blueprints here
    from app.webui.basic.routes import basic
    app.register_blueprint(basic)
    from app.webui.admin.routes import admin
    app.register_blueprint(admin)
    from app.webui.download.routes import download
    app.register_blueprint(download)

    # Register routes here
    # app.add_url_rule('/', 'index', index)
    # app.add_url_rule('/some-route', 'some_route', some_view_function)

    return app

