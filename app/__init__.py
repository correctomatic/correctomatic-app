import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/correctomatic'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

    db.init_app(app)

    with app.app_context():
        from .routes import home, submissions

        # Register Blueprints
        app.register_blueprint(home.bp)
        app.register_blueprint(submissions.bp)

        return app
