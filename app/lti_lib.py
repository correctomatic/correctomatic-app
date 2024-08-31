import os
from flask import current_app
from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
)
from pylti1p3.tool_config import ToolConfJsonFile

def lti_config_dir():
    default_config_dir = os.path.join(current_app.root_path, "..", "configs")
    return os.getenv('LTI_CONFIG_DIR', default_config_dir)

def lti_config_file():
    return os.path.join(lti_config_dir(), "correctomatic.json")

def lti_tool_conf():
    return ToolConfJsonFile(lti_config_file())

def lti_launch_data_storage():
    cache = current_app.cache
    return FlaskCacheDataStorage(cache)

# tool_conf = ToolConfJsonFile(get_lti_config_path())
# flask_request = FlaskRequest()
# launch_data_storage = get_launch_data_storage()
# message_launch = ExtendedFlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
# launch_data_storage=launch_data_storage)
