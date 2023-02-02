"""Test webui routes"""
from bs4 import BeautifulSoup
from app.webui.admin.models import User



def test_register_page(client, app):
    response = client.get('/register/')
    assert response.status_code == 200
    assert b'Register' in response.data
    assert b"csrf_token" in response.data
    # Get csrf token from page
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find(id='csrf_token')['value']
    # Register user with csrf token
    response = client.post('/register/', data={"email": "testuser@test.com", "password": "testpassword123ABC", "confirm_password": "testpassword123ABC", "csrf_token": csrf_token})
    with app.app_context():
        assert User.get_user_by_email("testuser@test.com") is not None


def test_login_page(client):
    response = client.get('/login/')
    assert response.status_code == 200
    assert b'Log in' in response.data
    assert b"csrf_token" in response.data
    # Get csrf token from page
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find(id='csrf_token')['value']
    # Login user with csrf token
    response2 = client.post('/login/', data={"email": "testuser@test.com", "password": "testpassword123ABC", "csrf_token": csrf_token})
    assert response.status_code == 200
    assert b'Login failed, please check email and password.' not in response2.data

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'BrokerBoss' in response.data

def test_users_page(client):
    response = client.get('/config/users/')
    assert response.status_code == 200
    assert b'Add User' in response.data

def test_config_settings_page(client):
    response = client.get('/config/settings/')
    assert response.status_code == 200
    assert b'Settings' in response.data
    #TODO: Add more tests
    # TEST change config

def test_config_broker_page(client):
    response = client.get('/config/broker/')
    assert response.status_code == 200
    assert b'Broker Configuration' in response.data

    #TODO: Add more tests
    # TEST Start/Stop Broker
    # TEST change config
    # TEST change config with invalid data

# This test is failing because it needs to run inside a container running flask
# TODO make the testing part of the docker-compose file as a stage before the final image is built
# def test_config_users_page(client):
#     response = client.get('/config/users/')
#     assert response.status_code == 200
#     assert b'No users. Add a user to get started.' in response.data
#     assert b"csrf_token" in response.data
#     # Get csrf token from page
#     soup = BeautifulSoup(response.data, 'html.parser')
#     csrf_token = soup.find(id='csrf_token')['value']
#     # TEST Add user
#     response2 = client.post('/config/users/', data={"username": "test_username", "password": "TEST_password", "confirm_password": "TEST_password", "csrf_token": csrf_token})
#     assert response2.status_code == 200
#     assert b'<td colspan="3">test_username</td>' in response2.data
#     # TEST Delete user
#     response3 = client.post('/config/users/', data={"delete": "test_username", "csrf_token": csrf_token})
#     assert response3.status_code == 200
#     assert b'<td colspan="3">test_username</td>' not in response3.data

def test_config_acl_page(client):
    response = client.get('/config/acl/')
    assert response.status_code == 200
    assert b'Access control list' in response.data

# This is the last test because it logs out the user
def test_logout_page(client):
    response = client.get('/logout/')
    assert response.status_code == 302
    assert b'login' in response.data

