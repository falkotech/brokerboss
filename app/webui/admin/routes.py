"""Routes for the admin blueprint."""
from app import db, flask_bcrypt
from app.webui.admin.forms import Register_form, Login_form, Password_reset_request_form, Password_reset_form, ChangePasswordForm
from app.webui.admin.models import User
from flask import Blueprint, render_template, redirect, url_for, current_app, flash, request
from flask_login import login_user, login_required, logout_user, current_user, user_logged_in
import logging
from itsdangerous import URLSafeSerializer


admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except Exception:
        return redirect(fallback)
    return redirect(dest_url)

# LOGIN
@admin.route('/login/', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect_dest(url_for('basic.index'))
    form = Login_form()
    if form.validate_on_submit():
        # find matching email
        admin = User.get_user_by_email(form.email.data)
        # if a matching user exists and the password matches
        if admin and flask_bcrypt.check_password_hash(admin.user_data["password"], form.password.data):
            # Log the user in and send him to homepage.
            login_user(admin, remember=form.remember.data)
            flash('Welcome back!', "success")
            return redirect_dest(url_for('basic.index'))
        else:
            flash('Login failed, please check email and password.', "danger")

    return render_template('admin/login.html',form=form)



# LOG OUT
@login_required
@admin.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


# REGISTER
@admin.route('/register/', methods = ['GET', 'POST'])
def register():
    # If an admin exists, redirect to different page
    if db.admin_collection.find_one():
        flash('An admin account already exists. Multiple admins are not yet supported', "danger")
        return redirect_dest(url_for('admin.login'))

    form = Register_form()
    # if Register Form is sent & valid
    if form.validate_on_submit():
        if User.register_user(form.email.data, form.password.data):
            flash('Your account has been created, you can now log in!', "success")
            # Send user to login page
            return redirect_dest(url_for('admin.login'))
        else:
            flash('Could not register user, please check email and password.', "danger")

    return render_template('admin/register.html', form=form)


# PROFILE
@admin.route('/profile/', methods = ['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm()
    user = current_user
    if form.validate_on_submit():
        # change the password to the new one.
        if current_user.set_new_password(form.old_password.data, form.new_password.data):
            flash('Password is now changed.', "success")
            return redirect_dest(url_for('admin.profile'))
        else:
            flash('Could not change password, please check passwords.', "danger")

    return render_template('profile.html', user=user, form=form)

# PASSWORD RESET REQUEST
@admin.route('/reset_password_request/', methods = ['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect_dest(url_for('main.home'))
    form = Password_reset_request_form()
    # find matching email
    if form.validate_on_submit():
        admin = User.get_user_by_email(form.email.data)
        # if a matching user exists, send password reset mail
        if admin:
            admin.send_password_reset_email(admin)
        flash('Check your email for the instructions to reset your password','success')
        return redirect_dest(url_for('admin.login'))
    return render_template('reset_password_request.html', form=form)