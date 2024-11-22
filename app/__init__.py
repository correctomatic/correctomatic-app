import os
import sys
import logging
import uuid
from flask import Flask,g, request
from flask_caching import Cache

from .extensions import db, get_connection_string
from .errors import register_errors
from .config import configurations


def set_log_level(app):
    DEFAULT_LOG_LEVEL = 'WARNING'

    if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    else:
        app.logger.setLevel(os.getenv('LOG_LEVEL', DEFAULT_LOG_LEVEL))

    return app

def add_request_id_to_log(app):
    # Generate a request ID for each incoming request
    @app.before_request
    def generate_request_id():
        g.request_id = str(uuid.uuid4())
        app.logger.info(f"Request ID: {g.request_id} - {request.method} {request.path}")

    # Custom log format including the request ID
    @app.after_request
    def add_request_id_to_log(response):
        app.logger.info(f"Request ID: {g.request_id} finished")
        return response

def mask_sensitive_data(connection_string):
    """
    Masks sensitive data (like passwords) in the connection string for safe logging.
    """
    import re
    # Match connection strings and replace the password part
    pattern = r"(://.*:)(.*)(@)"
    return re.sub(pattern, r"\1******\3", connection_string)

def test_db_connection(app):
    try:
        connection_string = app.config['SQLALCHEMY_DATABASE_URI']
        safe_connection_string = mask_sensitive_data(connection_string)

        app.logger.info(f"Testing database connection to: {safe_connection_string}")

        with app.app_context():
            # Attempt to connect to the database
            connection = db.get_engine().connect()
            connection.close()
            app.logger.info("Database connection test successful.")
    except Exception as e:
        app.logger.critical('Database connection test failed', exc_info=True)
        sys.exit(1)

def create_app(environment='development'):
    app = Flask(__name__)

    app.logger.info(f"Running in {environment} environment")
    app.config.from_object(configurations[environment])

    set_log_level(app)
    add_request_id_to_log(app)

    # ----------------------------------------
    # Debugging log level
    # ----------------------------------------
    current_log_level = app.logger.getEffectiveLevel()
    log_level_name = logging.getLevelName(current_log_level)
    app.logger.info(f"Current log level: {log_level_name}")

    # Set up caching configuration
    app.config['CACHE_TYPE'] = 'simple'  # or 'filesystem', 'redis', 'memcached', etc.
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Optional: set default cache timeout (in seconds)

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

    test_db_connection(app)

    with app.app_context():
        app.cache = cache

        from .routes import lti
        from .routes import home, submissions
        from .routes import correctomatic

        # Register Blueprints
        app.register_blueprint(home.bp)
        app.register_blueprint(submissions.bp, url_prefix='/submissions')
        app.register_blueprint(correctomatic.bp, url_prefix='/correctomatic')
        app.register_blueprint(lti.bp, url_prefix='/lti')

        register_errors(app)

        return app
