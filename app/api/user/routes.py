"""API Routes related to MQTT Users and ACLs"""
from app.broker_manager import BrokerManager
from flask import Blueprint, request
import subprocess
from app.api import api_allowed


user = Blueprint('user', __name__)

@user.route('/api/user/test/', methods=['POST'])
@api_allowed
def test_user():
    """Add a user to the Mosquitto MQTT broker"""
    # Get the user data from the request
    data = request.get_json()
    username = data['username']
    password = data['password']
    return f'Username: {username}, Password: {password}', 200



# ADD USER
@user.route('/api/user/add/', methods=['POST'])
@api_allowed
def add_user():
    """Add a user to the Mosquitto MQTT broker"""
    # Get the user data from the request
    data = request.get_json()
    username = data['username']
    password = data['password']
    success = BrokerManager.add_user(username, password)
    # inform the client of the result
    if success:
        # Return a response to the client
        return f'Succes! Added user: {username}', 200
    else:
        return f'Error adding user: {username}', 500



# DELETE USER
@user.route('/api/user/delete/', methods=['DELETE', 'POST'])
@api_allowed
def delete_user():
    """Delete a user from the Mosquitto MQTT broker"""
    # Get the user data from the request
    data = request.get_json()
    username = data['username']
    
    success = BrokerManager.delete_user(username)
    # inform the client of the result
    if success:
        # Return a response to the client
        return f'Succes! Deleted user: {username}', 200
    else:
        return f'Error deleting user: {username}', 500