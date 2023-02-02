""" WEBUI basic routes """
from app import db
from app.broker_manager import BrokerManager
from app.webui.basic.forms import AddUserForm, ACLPatternRuleForm, ACLUserRuleForm, MosquittoConfigForm, SettingsForm
from collections import namedtuple
from flask import request, flash
from flask_login import login_required
import logging
import time

from flask import Blueprint, render_template, redirect, url_for
basic = Blueprint('basic', __name__, static_folder='static', template_folder='templates')


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except Exception:
        return redirect(fallback)
    return redirect(dest_url)


@basic.route('/')
@login_required
def index():
    return render_template('index.html', config_changed=BrokerManager.config_changed)


@basic.route('/explorer/')
@login_required
def explorer():
    return render_template('explorer_copy.html', config_changed=BrokerManager.config_changed)


@basic.route('/config/settings/', methods=['GET', 'POST'])
def settings():
    # Get the current settings 
    # and convert it to an object that can be accessed using dot notation
    # This is needed for prefilling the form
    settings = db.load_general_settings()
    settings_obj = None
    if settings is not None:
        #remove fields that start with _ because namedtuples don't allow it
        settings.pop('_id', None) 
        settings_obj = namedtuple("settings_obj", settings.keys())(*settings.values())
        
    form=SettingsForm(obj=settings_obj)
    # When submitting the form...
    if form.validate_on_submit():
        form_data_dict = form.data
        # Remove the CSRF token and save btn from the form data, no need to save it in the DB
        form_data_dict.pop('csrf_token', None)
        form_data_dict.pop('save', None)
        # If the form is valid, save the settings
        db.save_general_settings(form_data_dict)
        return redirect_dest(url_for('basic.settings'))
        


    return render_template('settings.html', form=form)


@basic.route('/config/users/', methods=['GET', 'POST'])
@login_required
def users():
    add_form = AddUserForm()
    #delete_form = DeleteUserForm()
    userlist = BrokerManager.list_users()

    # if POST form, ADD user
    if add_form.validate_on_submit() and add_form.add.data:
        username = add_form.username.data
        password = add_form.password.data
        BrokerManager.add_user(username, password)
        return redirect_dest(url_for('basic.users'))

    # when pushing the DELETE button, delete user
    if request.method == 'POST' and 'delete' in request.form:
        username = request.form['delete']
        BrokerManager.delete_user(username)
        return redirect_dest(url_for('basic.users'))        

    return render_template(
        'users.html',
        config_changed=BrokerManager.config_changed,
        form=add_form, 
        userlist=userlist)



@basic.route('/config/users/edit/<usr>/', methods=['GET', 'POST'])
@login_required
def edit_user(usr):
    user_rule_form = ACLUserRuleForm()
    rules = BrokerManager.acl_to_dict(acl_file='/mosquitto/config/acl.acl')
    user_rules = rules["user_acl"].get(usr, {}) #dictionary of user rules
    
    # if POST form, ADD topic rule
    if user_rule_form.validate_on_submit() and user_rule_form.add_topic.data:
        topic = user_rule_form.topic.data
        read = user_rule_form.read.data
        write = user_rule_form.write.data
        success = BrokerManager.add_acl_user_rule(usr, topic, read, write)
        if not success:
            flash(f'Failed to add topic "{topic}". Maybe you tried adding a topic without read or write?', 'warning')
        return redirect_dest(url_for('basic.edit_user', usr=usr))
    
    # when pushing the DELETE button, delete topic rule
    if request.method == 'POST' and 'delete_user_topic' in request.form:
        pattern = request.form['delete_user_topic']
        success = BrokerManager.delete_acl_user_rule(usr, pattern)
        if not success:
            flash(f'Failed to remove ACL pattern rule: {pattern}', 'warning')
        return redirect_dest(url_for('basic.edit_user', usr=usr))

    return render_template(
        'user_edit.html',
        config_changed=BrokerManager.config_changed, 
        usr=usr, 
        user_rule_form=user_rule_form, 
        user_rules=user_rules)
    


# configures the broker
@basic.route('/config/broker/', methods=['GET', 'POST'])
@login_required
def broker():
    #TODO save config to database and if config cant be loaded from file, load from database
    # Get the current config (dictionary) 
    # and convert it to an object that can be accessed using dot notation
    # This is needed for prefilling the form
    config_dict = BrokerManager.config_to_dict()
    if config_dict is not False:
        config_obj = namedtuple("config_obj", config_dict.keys())(*config_dict.values())
    else:
        config_obj = None
        flash('Failed to load configuration', 'danger')
    
    # Prefill the form when loading the page
    form = MosquittoConfigForm(obj = config_obj)
    # When submitting the form...
    if form.validate_on_submit():
        # clean up the form data
        new_config_dict = {k:v for k,v in form.data.items() if v != '' and v is not None }
        # remove unneeded fields
        del new_config_dict['csrf_token']
        del new_config_dict['save']
        # rename listener fields
        # TODO improve this for multiple listeners
        new_config_dict['listener']= form.data['listener'][0]['port']
        new_config_dict['protocol']= form.data['listener'][0]['protocol']
        if BrokerManager.dict_to_config(new_config_dict):
            flash('Configuration saved', 'success')
        else:
            flash('Failed to save configuration', 'danger')
        return redirect_dest(url_for('basic.broker'))

    # when pushing the START/STOP button -> START/STOP BROKER
    if request.method == 'POST' and 'command' in request.form:
        command = request.form['command']
        if command == 'stop_broker':
            BrokerManager.stop_broker()
            # TODO added a 1s delay so broker can fully stop before loading page
            # this is a workaround and probably not the best solution
            time.sleep(1)
        elif command == 'start_broker':
            BrokerManager.start_broker()
        return redirect_dest(url_for('basic.broker'))

    return render_template(
        'broker.html',
        config_changed=BrokerManager.config_changed,
        broker_is_running = BrokerManager.is_running(),
        ports = BrokerManager.get_ports(),
        mosquitto_version = BrokerManager.get_version(),
        form=form)



@basic.route('/config/acl/', methods=['GET', 'POST'])
@login_required
def acl():
    rules = BrokerManager.acl_to_dict(acl_file='/mosquitto/config/acl.acl')
    pattern_rules = rules["pattern_acl"]
    user_rules = rules["user_acl"]

    pattern_form = ACLPatternRuleForm()
    # if POST form, ADD pattern rule
    if pattern_form.validate_on_submit() and pattern_form.add_rule.data:
        pattern = pattern_form.pattern.data
        read = pattern_form.read.data
        write = pattern_form.write.data
        success = BrokerManager.add_acl_pattern_rule(pattern, read, write)
        if not success:
            flash(f'Failed to add ACL pattern rule: {pattern}', 'warning')
        return redirect_dest(url_for('basic.acl'))

    # when pushing the DELETE button, delete pattern rule
    if request.method == 'POST' and 'delete_pattern' in request.form:
        pattern = request.form['delete_pattern']
        success = BrokerManager.delete_acl_pattern_rule(pattern)
        if not success:
            flash(f'Failed to remove ACL pattern rule: {pattern}', 'warning')
        return redirect_dest(url_for('basic.acl'))

    return render_template(
        'acl.html', 
        config_changed=BrokerManager.config_changed, 
        pattern_form=pattern_form, 
        pattern_rules=pattern_rules, 
        user_rules=user_rules)


    