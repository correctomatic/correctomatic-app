from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .routes import home

        # Register Blueprints
        app.register_blueprint(home.bp)
        # app.register_blueprint(auth.bp)

        return app
