import os
from flask import Flask
from flask_caching import Cache

from .routes import lti_endpoints
from .extensions import db, get_connection_string

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

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
