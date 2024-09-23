import os
from flask import current_app
from pylti1p3.contrib.flask import FlaskCacheDataStorage
from pylti1p3.tool_config import ToolConfJsonFile, ToolConfDict
from cachetools import cached, TTLCache

from app.models import Platform

# Create a cache for the configuration
cache = TTLCache(maxsize=1, ttl=10)

@cached(cache)

def get_configuration_from_db():
    platforms = Platform.query.all()
    configuration = {}

    for platform in platforms:
        platform_data = {
            "default": platform.default,
            "client_id": platform.client_id,
            "auth_login_url": platform.auth_login_url,
            "auth_token_url": platform.auth_token_url,
            "auth_audience": platform.auth_audience,
            "key_set_url": platform.key_set_url,
            "key_set": None,
            "private_key_file": platform.private_key_file,
            "public_key_file": platform.public_key_file,
            "deployment_ids": [d.deployment_id for d in platform.deployments]
        }

        configuration.setdefault(platform.url, []).append(platform_data)

    return ToolConfDict(configuration)

def lti_config_dir():
    default_config_dir = os.path.join(current_app.root_path, "..", "configs")
    return os.getenv('LTI_CONFIG_DIR', default_config_dir)

def lti_config_file():
    return os.path.join(lti_config_dir(), "correctomatic.json")

def lti_tool_conf():
    # return ToolConfJsonFile(lti_config_file())
    return get_configuration_from_db()

def lti_launch_data_storage():
    cache = current_app.cache
    return FlaskCacheDataStorage(cache)
