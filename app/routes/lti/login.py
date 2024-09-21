from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskRequest,
    FlaskSessionService,
    FlaskCookieService
)

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

    # oidc_login = FlaskOIDCLogin(
    #     flask_request, tool_conf, launch_data_storage=launch_data_storage
    # )
    oidc_login = FlaskOIDCLogin(
        request=flask_request,
        tool_config=tool_conf,
        # launch_data_storage=lti_launch_data_storage()
        session_service=FlaskSessionService(flask_request),
        cookie_service=FlaskCookieService(flask_request)
    )

    return oidc_login.enable_check_cookies().redirect(target_link_uri)

