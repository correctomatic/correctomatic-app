from functools import wraps
from flask import (
    request,
    current_app,
    session,
    g
)

def get_launch_data():
    return session.get('launch_data')

def get_current_user(launch_data):
    return launch_data.get("sub")

def get_assignment_id(launch_data):
    return launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}).get('assignment_id', None)

# TO-DO: Allow getting "launch data" from a different source
# That way, we can use this app outside of the LTI context
def require_launch_data(methods=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if methods and request.method not in methods: return

            try:
                launch_data = get_launch_data()
                g.current_user = get_current_user(launch_data)
                g.assignment_id = get_assignment_id(launch_data)
            except Exception as e:
                current_app.logger.error(f"Failed to load launch data: {e}")
                g.current_user = None
                g.assignment_id = None
            return f(*args, **kwargs)

        return decorated_function
    return decorator
