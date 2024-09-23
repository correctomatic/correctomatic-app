import os
import logging
import uuid
from flask import Flask,g, request
from flask_caching import Cache

from .extensions import db, get_connection_string
from .errors import register_errors

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

    # ----------------------------------------
    # Debugging log level
    # ----------------------------------------
    current_log_level = app.logger.getEffectiveLevel()
    log_level_name = logging.getLevelName(current_log_level)
    app.logger.info(f"Current log level: {log_level_name}")

    # Set up caching configuration
    app.config['CACHE_TYPE'] = 'simple'  # or 'filesystem', 'redis', 'memcached', etc.
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Optional: set default cache timeout (in seconds)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', os.path.join(app.root_path, "..", "uploads"))
    app.config['CALLBACK_HOST'] = os.getenv('CALLBACK_HOST', 'http://localhost:5000')
    app.config['CORRECTOMATIC_API_SERVER'] = os.getenv('CORRECTOMATIC_API_SERVER')
    app.config['DEFAULT_ASSIGNMENT'] = os.getenv('DEFAULT_ASSIGNMENT', 'correction-test-1')

    # SQLAlchemy pool configuration
    app.config['SQLALCHEMY_POOL_SIZE'] = 10         # Number of connections to keep in the pool
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5      # Timeout in seconds to get a connection from the pool
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600    # Time in seconds to recycle a connection
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20      # Number of connections to allow beyond the pool size

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
