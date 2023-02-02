from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, FloatField, SelectField, RadioField, Form, FormField, FieldList
from wtforms.validators import EqualTo, Length, ValidationError, Regexp, InputRequired, Optional, NumberRange

class AddUserForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired(), Regexp(r'^[a-z0-9_-]+$', message="Only lowercase alphanumeric characters, hyphens, and underscores allowed")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    add = SubmitField("Add User")


class mqtt_listener(Form):
    port = IntegerField('Port', validators=[InputRequired()])
    protocol = SelectField('Protocol', choices=[('mqtt', 'MQTT'), ('websockets', 'WebSockets')])


class MosquittoConfigForm(FlaskForm):
    # Custom validation for max_packet_size
    def check_packet_size(self, field):
        if field.data != 0 and field.data < 20:
            raise ValidationError('Max Packet Size should be 0 or greater than 20')
    # GENERAL
    per_listener_settings = BooleanField('Per Listener Settings')
    allow_zero_length_clientid = BooleanField('Allow Zero Length Client ID')
    auto_id_prefix = StringField('Auto ID Prefix', validators=[InputRequired(), Regexp(r'^\S+$', message="No spaces allowed")])
    check_retain_source = BooleanField('Check Retain Source')
    max_inflight_bytes = IntegerField('Max Inflight Bytes', validators=[InputRequired()])
    max_inflight_messages = IntegerField('Max Inflight Messages', validators=[InputRequired()])
    max_keepalive = IntegerField('Max Keepalive', validators=[InputRequired()])
    max_packet_size = IntegerField('Max Packet Size', validators=[check_packet_size], default=0)
    max_queued_bytes = IntegerField('Max Queued Bytes', validators=[InputRequired()])
    max_qos = IntegerField('Max QoS', validators=[InputRequired()])
    max_queued_messages = IntegerField('Max Queued Messages', validators=[InputRequired()])
    memory_limit = IntegerField('Memory Limit', validators=[InputRequired()])
    message_size_limit = IntegerField('Message Size Limit', validators=[InputRequired(), NumberRange(max=268435455, min=0)], default=0)
    persistant_client_expiration = StringField('Persistant Client Expiration', validators=[Regexp(r'^\S+$', message="No spaces allowed")])
    #pid_file = StringField('PID File')
    queue_qos0_messages = BooleanField('Queue QoS0 Messages')
    retain_available = BooleanField('Retain Available')
    set_tcp_nodelay = BooleanField('Set TCP No Delay')
    sys_interval = IntegerField('Sys Interval', validators=[InputRequired()])
    upgrade_outgoing_qos = BooleanField('Upgrade Outgoing QoS')
    # LISTENERS
    listener = FieldList(FormField(mqtt_listener), min_entries=1)
    # LOGGING
    enable_logging = BooleanField('Enable Logging')
    # SECURITY
    clientid_prefixes = StringField('Client ID Prefixes', validators=[Regexp(r'^[a-z0-9_-]+$', message="Only lowercase alphanumeric characters, hyphens, and underscores allowed")])
    allow_anonymous = BooleanField('Allow Anonymous')
    # SAVE
    save = SubmitField("Save configuration")


class ACLPatternRuleForm(FlaskForm):
    pattern = StringField('Pattern',validators=[InputRequired(), Regexp(r'^(%[uc])?[a-z0-9_+-/#]+(%[uc][a-z0-9_+-/#]+)*$', message="Allowed characters: lowercase alphanumeric characters, slashes, hash symbols, plus signs, dashes, underscores and 'client' or 'username' wildcards (a-z, 0-9, -_#+/%u %c).")])
    read = BooleanField('Read')
    write = BooleanField('Write')
    add_rule = SubmitField("Add Rule")


class ACLUserRuleForm(FlaskForm):
    topic = StringField('Topic', validators=[InputRequired(), Regexp(r'^[a-z0-9_\-\+#\/]+$', message="Only lowercase alphanumeric characters, slashes, hash symbols, plus signs, dashes, and underscores allowed (a-z, 0-9, -_#+/")])
    read = BooleanField('Read')
    write = BooleanField('Write')
    add_topic = SubmitField("Add Topic")


class SettingsForm(FlaskForm):
    # General
    #dark_mode = BooleanField('Dark Mode')
    # Security
    enable_api = BooleanField('Enable API')
    save = SubmitField("Save settings")

