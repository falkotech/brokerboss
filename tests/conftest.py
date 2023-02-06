import pytest
from app import create_app
import logging
import os

@pytest.fixture(scope='session')
def app():
    # Set the environment variables for testing
    os.environ['FLASK_SECRET_KEY'] = "SECRET_KEY_FOR_TESTING"
    # Create the app with the testing config
    app = create_app(config_object='app.config.TestingConfig')
    yield app
    #clear database after testing
    with app.app_context():
        app.db.client.drop_database('testing')


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()