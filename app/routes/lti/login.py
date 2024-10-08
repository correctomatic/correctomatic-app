from werkzeug.exceptions import Forbidden, BadRequest
from flask import flash, abort, current_app

from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskRequest,
    FlaskSessionService,
    FlaskCookieService
)

from . import bp
from app.lib.lti_lib import lti_tool_conf

def check_target_link_uri(flask_request):
    target_link_uri = flask_request.get_param("target_link_uri")
    if not target_link_uri:
        raise BadRequest('Missing "target_link_uri" param')

def check_iss_params(flask_request, tool_conf):
    iss = flask_request.get_param("iss")
    client_id = flask_request.get_param("client_id")

    if not iss:
        raise BadRequest('Missing "iss" param in request')

    if not client_id:
        raise BadRequest('Missing "client_id" param in request')

    try:
        tool_conf.find_registration_by_params(iss, client_id)
    except Exception as e:
        message = f'Registration for [{iss}/{client_id}] not found in tool configuration'
        current_app.logger.error(f'{message}, exception: {e}')
        raise Forbidden(message)

@bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        tool_conf =lti_tool_conf()
        flask_request = FlaskRequest()

        check_target_link_uri(flask_request)
        check_iss_params(flask_request, tool_conf)

        oidc_login = FlaskOIDCLogin(
            request=flask_request,
            tool_config=tool_conf,
            session_service=FlaskSessionService(flask_request),
            cookie_service=FlaskCookieService(flask_request)
        )

        login = oidc_login.enable_check_cookies().redirect(flask_request.get_param("target_link_uri"))

    except BadRequest as e:
        flash(f'Bad Request: {e.description}', 'error')
        return abort(400)

    except Forbidden as e:
        flash(f'{e.description}', 'error')
        return abort(403)

    except Exception as e:
        current_app.logger.error(f'Error getting launch: {e}')
        flash(f'Something bad happened in login', 'error')
        abort(500)

    return login

