import os
from jwcrypto import jwk
from flask import Blueprint, url_for, redirect, session, jsonify
from ..lti_lib import (
    lti_tool_conf,
    lti_launch_data_storage,
    lti_config_dir
)

from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
    FlaskSessionService,
    FlaskCookieService
)
from pylti1p3.tool_config import ToolConfJsonFile

bp = Blueprint("lti", __name__)

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

@bp.route("/launch", methods=["GET", "POST"])
def launch():
    flask_request = FlaskRequest()

    message_launch = FlaskMessageLaunch(
        request=flask_request,
        tool_config=lti_tool_conf()
    )

    # Still testing this part
    data = message_launch.get_launch_data()
    session['launch_data'] = data
    print(f'Data from launch: {data}')

    launch_id = message_launch.get_launch_id()
    session['launch_id'] = launch_id

    user = data.get("sub")
    session['user'] = user

    return redirect(url_for("submissions.index"))

@bp.route("/jwks", methods=["GET"])
def jwks():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    public_key_path = os.path.join(lti_config_dir(), "public.key")

    with open(public_key_path, "rb") as public_key_file:
        public_key = public_key_file.read()

    key = jwk.JWK.from_pem(public_key)
    jwk_data = key.export(as_dict=True)
    jwks = {"keys": [jwk_data]}
    return jsonify(jwks)
