# API initialization file
from app import db
from flask import redirect, url_for
from functools import wraps

def _api_access_enabled():
    """Check if the api is enabled under user settings."""
    settings_dict = db.load_general_settings()
    return settings_dict.get('enable_api', False)


def api_allowed(func):
    """Decorator to check if the api is enabled."""
    #TODO add check to see if user is allowed to use the API
    @wraps(func)
    def inner_function(*args, **kwargs):
        if not _api_access_enabled():
            return "API ACCESS NOT ALLOWED", 405
        return func(*args, **kwargs)

    return inner_function