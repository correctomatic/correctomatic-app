import os
from jwcrypto import jwk
from flask import Blueprint, jsonify, current_app

from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
)
from pylti1p3.tool_config import ToolConfJsonFile

bp = Blueprint("lti", __name__)

def get_lti_config_path():
    return os.path.join(current_app.root_path, "configs", "reactquiz.json")

def get_launch_data_storage():
    cache = current_app.cache
    return FlaskCacheDataStorage(cache)

@bp.route("/login/", methods=["GET", "POST"])
def login():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    launch_data_storage = get_launch_data_storage()
    flask_request = FlaskRequest()

    target_link_uri = flask_request.get_param("target_link_uri")
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(
        flask_request, tool_conf, launch_data_storage=launch_data_storage
    )

    return oidc_login.enable_check_cookies().redirect(target_link_uri)

@bp.route("/jwks", methods=["GET"])
def jwks():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    public_key_path = os.path.join(__location__, "configs", "public.key")

    with open(public_key_path, "rb") as public_key_file:
        public_key = public_key_file.read()

    key = jwk.JWK.from_pem(public_key)
    jwk_data = key.export(as_dict=True)
    jwks = {"keys": [jwk_data]}
    return jsonify(jwks)
