import os
from jwcrypto import jwk
from flask import jsonify

from . import bp
from app.lib.lti_lib import lti_config_dir

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
