from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskRequest,
    FlaskSessionService,
    FlaskCookieService
)
from flask import flash, abort, current_app

from . import bp
from app.lib.lti_lib import lti_tool_conf

@bp.route("/login", methods=["GET", "POST"])
def login():
    tool_conf =lti_tool_conf()
    # launch_data_storage = lti_launch_data_storage()
    flask_request = FlaskRequest()

    target_link_uri = flask_request.get_param("target_link_uri")
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(
        request=flask_request,
        tool_config=tool_conf,
        session_service=FlaskSessionService(flask_request),
        cookie_service=FlaskCookieService(flask_request)
    )

    try:
        login = oidc_login.enable_check_cookies().redirect(target_link_uri)
    except Exception as e:
        current_app.logger.error(f'Error getting launch: {e}')
        flash(f'Something bad happened in login', "danger")
        # flash(f'The site is not autorized: [{site}]/[{id}]', "danger")
        abort(403)

    return login

