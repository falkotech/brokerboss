from flask import Blueprint, render_template, redirect, url_for, send_file
from flask_login import login_required

download = Blueprint('download', __name__, static_folder='static', template_folder='templates')

# LOGS
@download.route('/download/logs')
@login_required
def download_logs ():
    path = "/mosquitto/log/mosquitto.log"
    return send_file(path, as_attachment=True)

# CONFIG FILE
@download.route('/download/config')
@login_required
def download_configuration_file ():
    path = "/mosquitto/config/mosquitto.conf"
    return send_file(path, as_attachment=True)

# ACL FILE
@download.route('/download/acl')
@login_required
def download_acl_file ():
    path = "/mosquitto/config/acl.acl"
    return send_file(path, as_attachment=True)

# PASSWORD FILE
@download.route('/download/password-file')
@login_required
def download_password_file ():
    path = "/mosquitto/config/pw.txt"
    return send_file(path, as_attachment=True)