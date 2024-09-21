import jwt
from flask import current_app, url_for, redirect, session, current_app, request
from pylti1p3.contrib.flask import FlaskMessageLaunch, FlaskRequest

from . import bp
from app.lib.lti_lib import lti_tool_conf

def get_deployment_id_from_request(request):
    # Get the token from the request
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]  # Extract the token
    else:
        token = request.form.get('id_token')  # Try to get from form if not in headers

    if not token:
        return None  # Token not found

    # Decode the JWT token without verifying the signature for now
    decoded_token = jwt.decode(token, options={"verify_signature": False})

    # Extract the deployment_id
    deployment_id = decoded_token.get("https://purl.imsglobal.org/spec/lti/claim/deployment_id")
    return deployment_id

@bp.route("/launch", methods=["GET", "POST"])
def launch():
    current_app.logger.debug(f'Deployment ID in request: {get_deployment_id_from_request(request)}')
    flask_request = FlaskRequest()

    message_launch = FlaskMessageLaunch(
        request=flask_request,
        tool_config=lti_tool_conf()
    )

    # Still testing this part
    data = message_launch.get_launch_data()
    session['launch_data'] = data

    deployment_id = data.get("https://purl.imsglobal.org/spec/lti/claim/deployment_id")
    current_app.logger.debug(f'Deployment ID in launch data: {deployment_id}')

    current_app.logger.debug(f'Data from launch: {data}')

    launch_id = message_launch.get_launch_id()
    session['launch_id'] = launch_id

    user = data.get("sub")
    session['user'] = user

    return redirect(url_for("submissions.index"))
