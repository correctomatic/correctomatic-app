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

# All params passed to the correctomatic are lowercase
# Moodle sends the params in the case used AND lowercase if written using uppercase characters
def get_correction_params(launch_data):
    launch_params = launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {})

    # Create a new dictionary with lowercase keys
    lowercase_params = {}
    for key, value in launch_params.items():
        lowercase_key = key.lower()
        # Only add the key if it's not already present (prioritize existing lowercase keys)
        if lowercase_key not in lowercase_params:
            lowercase_params[lowercase_key] = value

    # Remove 'assignment_id' if present
    lowercase_params.pop('assignment_id', None)

    return lowercase_params

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
                g.correction_params = get_correction_params(launch_data)
                current_app.logger.debug(f"Current user: {g.current_user}. Assignment ID: {g.assignment_id}")
            except Exception as e:
                current_app.logger.error(f"Failed to load launch data: {e}")
                g.current_user = None
                g.assignment_id = None
            return f(*args, **kwargs)

        return decorated_function
    return decorator
