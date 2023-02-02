from flask import Flask, session, current_app, flash, url_for, redirect, request
from flask_login import UserMixin
from itsdangerous import URLSafeSerializer
import logging
from app import db, flask_bcrypt, login_manager


@login_manager.user_loader
def load_user(session_token):
    users = db.admin_collection
    user_data = users.find_one({'session_token': session_token})
    if user_data is not None:
        return User(user_data)
    else:
        return None

class User(UserMixin):
    
    def __init__(self, user_data) -> None:
        self.user_data = user_data
    
    def get_id(self):
        return self.user_data['session_token']

    def set_new_password(self,old_password, new_password) -> bool:
        # if the password matches
        if flask_bcrypt.check_password_hash(self.user_data["password"], old_password):
            # change the password to the new one.
            try:
                email = self.user_data['email']
                session_token = User.generate_session_token(email, new_password)
                hashed_pass = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
                admin_collection = db.admin_collection
                query = {'email': email}
                replace = {"$set": {'password': hashed_pass, 'session_token': session_token }}
                # find and replace
                admin_collection.find_one_and_update(query, replace)
                return True
            except Exception as e:
                logging.error(f"Error updating password: {e}, Type: {type(e)}")
                return False
        # if the password does not match
        return False
    
    @classmethod
    def generate_session_token(cls, email, password):
        serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
        session_token = serializer.dumps([email, password])
        return session_token

    @classmethod
    def register_user(cls, email, password) -> bool:
        try:
            # check if the user already exists
            admin_collection = db.admin_collection
            user_data = admin_collection.find_one({"email": email})
            if user_data is not None:
                return False
            # if the user does not exist, add him to DB
            session_token = cls.generate_session_token(email, password)
            hashed_pass = flask_bcrypt.generate_password_hash(password).decode('utf-8')
            admin_collection.insert_one({'email': email, 'password': hashed_pass, 'session_token': session_token})
            return True
        except Exception as e:
            logging.error(f"Error registering user: {e}, Type: {type(e)}")
            return False

    @classmethod
    def login_user(cls, email, password) -> bool:
        admin_collection = db.admin_collection
        user_data = admin_collection.find_one({"email": email})
        if user_data is not None:
            if flask_bcrypt.check_password_hash(user_data["password"], password):
                return True
        return False

    @classmethod
    def get_user_by_email(cls, email):
        admin_collection = db.admin_collection
        user_data = admin_collection.find_one({"email": email})
        if user_data is not None:
            return User(user_data)
