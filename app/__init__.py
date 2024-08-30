import os
from flask import Flask
from flask_caching import Cache

from .routes import lti_endpoints
from .extensions import db, get_connection_string

def create_app():
    app = Flask(__name__)
    cache = Cache(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['CALLBACK_HOST'] = os.getenv('CALLBACK_HOST', 'http://localhost:5000')
    app.config['CORRECTOMATIC_API_SERVER'] = os.getenv('CORRECTOMATIC_API_SERVER')
    app.config['DEFAULT_CONTAINER'] = os.getenv('DEFAULT_CONTAINER', 'correction-test-1')
    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    
    # Validations before running the app
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        raise ValueError(f"Upload folder {app.config['UPLOAD_FOLDER']} does not exist")
    if not app.config['CALLBACK_HOST']:
        raise ValueError("Environment variable 'CALLBACK_HOST' is required")
    if not app.config['CORRECTOMATIC_API_SERVER']:
        raise ValueError("Environment variable 'CORRECTOMATIC_API_SERVER' is required")

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
