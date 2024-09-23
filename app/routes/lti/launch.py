import jwt
from werkzeug.exceptions import Forbidden, BadRequest
from flask import current_app, url_for, redirect, session, current_app, request, flash, abort
from pylti1p3.contrib.flask import FlaskMessageLaunch, FlaskRequest

from . import bp
from app.lib.lti_lib import lti_tool_conf

def get_site_data_from_request(request):
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

    site = decoded_token.get("iss")
    deployment_id = decoded_token.get("https://purl.imsglobal.org/spec/lti/claim/deployment_id")

    return [ site, deployment_id ]

@bp.route("/launch", methods=["GET", "POST"])
def launch():
    try:
        [ site, id ] = get_site_data_from_request(request)
        current_app.logger.debug(f'Request data - Site: {site}, ID: {id}')
        flask_request = FlaskRequest()

        message_launch = FlaskMessageLaunch(
            request=flask_request,
            tool_config=lti_tool_conf()
        )

        try:
            data = message_launch.get_launch_data()
            session['launch_data'] = data
        except Exception as e:
            current_app.logger.error(f'Error getting launch: {e}')
            raise Forbidden(f'The site is not autorized: [{site}]/[{id}]')

        deployment_id = data.get("https://purl.imsglobal.org/spec/lti/claim/deployment_id")
        current_app.logger.debug(f'Deployment ID in launch data: {deployment_id}')

        current_app.logger.debug(f'Data from launch: {data}')

        launch_id = message_launch.get_launch_id()
        session['launch_id'] = launch_id

        user = data.get("sub")
        session['user'] = user

        return redirect(url_for("submissions.index"))

    except Forbidden as e:
        flash(f'{e.description}', 'error')
        return abort(403)

    except Exception as e:
        current_app.logger.error(f'Error getting launch: {e}')
        flash(f'Something bad happened in login', 'error')
        abort(500)
