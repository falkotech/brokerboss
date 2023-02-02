from flask import Blueprint, redirect, request, url_for
import subprocess
from app.broker_manager import BrokerManager
from app.api import api_allowed


broker = Blueprint('broker', __name__)


@broker.route('/api/broker/restart/', methods=['POST'])
@api_allowed
def restart_broker():
    """Restart the Mosquitto MQTT broker"""
    BrokerManager.stop_broker()
    
    return redirect(url_for('broker.start_broker'), code=307)


@broker.route('/api/broker/stop/', methods=['POST'])
@api_allowed
def stop_broker():
    """Stop the Mosquitto MQTT broker"""
    BrokerManager.stop_broker()
    
    # check if mosquitto is running
    if BrokerManager.is_running():
        return 'Mosquitto broker not stopped', 500
    else:
        return 'Mosquitto broker stopped', 200


@broker.route('/api/broker/start/', methods=['POST'])
@api_allowed
def start_broker():
    """Start the Mosquitto MQTT broker"""
    BrokerManager.start_broker()
    
    # check if mosquitto is running
    if BrokerManager.is_running():
        return 'Mosquitto broker started', 200
    else:
        return 'Mosquitto broker not started', 500


@broker.route('/api/broker/status/', methods=['GET'])
@api_allowed
def status_broker():
    """Check if the Mosquitto MQTT broker is running"""
    if BrokerManager.is_running():
        return 'Mosquitto broker running', 200
    else:
        return 'Mosquitto broker not running', 200
