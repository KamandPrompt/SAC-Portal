from functools import wraps
from flask import session
# Route guard to prevent logged in user access to login and register page
def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if 'logged_in' in session:
            return 'Unauthorised! You are already logged in.'
        else:
            return f(*args, **kwargs)
    return wrap

# Check if user is logged-in or not
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return 'Unauthorized! Please login.'
    return wrap
