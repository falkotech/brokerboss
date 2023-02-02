from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, FloatField, SelectField, RadioField, Form, FormField, FieldList
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp, InputRequired
from app import db

# Email regular expression validator string. From http://emailregex.com/
regex_email_val = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

class Register_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=80), Regexp(regex_email_val, message='Please enter a valid email address.')]) 
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=40, message='Password must be between 8 and 40 characters.')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message="Passwords don't match.")])
    register = SubmitField("Register")

    def validate_email(self, email):
        usr = db.admin_collection.find_one({"email":email.data})
        if usr:
            raise ValidationError("We already have an account with that email")

class Login_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    login = SubmitField("Log in")

class Password_reset_request_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=80), Regexp(regex_email_val, message='Please enter a valid email address.')])
    send = SubmitField("Request password reset")

class Password_reset_form(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=40, message='Password must be between 8 and 40 characters.')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    reset = SubmitField("Reset password")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8, max=40, message='Password must be between 8 and 40 characters.')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('new_password')])
    save = SubmitField("Change password")