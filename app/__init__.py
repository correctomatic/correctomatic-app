import os
import logging
from flask import Flask
from flask_caching import Cache

from .routes import lti_endpoints
from .extensions import db, get_connection_string

def set_log_level(app):
    DEFAULT_LOG_LEVEL = 'WARNING'

    if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    else:
        app.logger.setLevel(os.getenv('LOG_LEVEL', DEFAULT_LOG_LEVEL))

    return app

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
    set_log_level(app)

    # ----------------------------------------
    # Debugging log level
    # ----------------------------------------
    current_log_level = app.logger.getEffectiveLevel()
    log_level_name = logging.getLevelName(current_log_level)
    app.logger.error(f"El nivel de registro actual es: {log_level_name}")

    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    # ----------------------------------------

    # Set up caching configuration
    app.config['CACHE_TYPE'] = 'simple'  # or 'filesystem', 'redis', 'memcached', etc.
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Optional: set default cache timeout (in seconds)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', os.path.join(app.root_path, "..", "uploads"))
    app.config['CALLBACK_HOST'] = os.getenv('CALLBACK_HOST', 'http://localhost:5000')
    app.config['CORRECTOMATIC_API_SERVER'] = os.getenv('CORRECTOMATIC_API_SERVER')
    app.config['DEFAULT_CONTAINER'] = os.getenv('DEFAULT_CONTAINER', 'correction-test-1')

    # Validations before running the app
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        raise ValueError(f'Upload folder {app.config["UPLOAD_FOLDER"]} does not exist')
    if not app.config['CALLBACK_HOST']:
        raise ValueError("Environment variable 'CALLBACK_HOST' is required")
    if not app.config['CORRECTOMATIC_API_SERVER']:
        raise ValueError("Environment variable 'CORRECTOMATIC_API_SERVER' is required")

    # Must be done after setting up the configuration
    cache = Cache(app)

    db.init_app(app)

    with app.app_context():
        app.cache = cache

        from .routes import home, submissions, responses

        # Register Blueprints
        app.register_blueprint(home.bp)
        app.register_blueprint(submissions.bp)
        app.register_blueprint(responses.bp)
        app.register_blueprint(lti_endpoints.bp)

        return app
