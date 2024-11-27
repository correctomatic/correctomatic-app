import os
from dotenv import load_dotenv

load_dotenv(override=True)

def connection_string(db_name, user, password, host, port = 5432,):
    return f'postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}'

class BaseConfig:
    # Shared configuratio, move to environments as needed
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10         # Number of connections to keep in the pool
    SQLALCHEMY_POOL_TIMEOUT = 5      # Timeout in seconds to get a connection from the pool
    SQLALCHEMY_POOL_RECYCLE = 3600    # Time in seconds to recycle a connection
    SQLALCHEMY_MAX_OVERFLOW = 20      # Number of connections to allow beyond the pool size

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.dirname(__file__), "..", "uploads"))
    CALLBACK_HOST = os.getenv("CALLBACK_HOST", "http://localhost:5000")
    CORRECTOMATIC_API_SERVER = os.getenv("CORRECTOMATIC_API_SERVER")
    CORRECTOMATIC_API_KEY = os.getenv("CORRECTOMATIC_API_KEY")

    @classmethod
    def initialize(cls):
        cls.SQLALCHEMY_DATABASE_URI = connection_string(cls.DB_NAME, cls.DB_USER, cls.DB_PASSWORD, cls.DB_HOST, cls.DB_PORT)
        return cls

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allows cookies to be set in a dev environment

    @classmethod
    def initialize(cls):
        # Must match the ones defined in docker-init-db.sh
        cls.DB_NAME = os.getenv("DB_NAME", "correctomatic_app")
        cls.DB_USER = os.getenv("DB_USER")
        cls.DB_PASSWORD = os.getenv("DB_PASSWORD")
        cls.DB_HOST = os.getenv("DB_HOST")
        cls.DB_PORT = os.getenv("DB_PORT", "5432")

        return super().initialize()

class TestingConfig(BaseConfig):
    TESTING = True
    SESSION_COOKIE_SECURE = False

    @classmethod
    def initialize(cls):
        # Must match the ones defined in docker-init-db.sh
        cls.DB_NAME = "inscripciones_test"
        cls.DB_USER = "test_user"
        cls.DB_PASSWORD = "test_password"
        cls.DB_HOST = "localhost"
        cls.DB_PORT = "5432"

        return super().initialize()

class ProductionConfig(BaseConfig):

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Enforces secure cookies in production

    @classmethod
    def initialize(cls):
        cls.DB_NAME = os.getenv("DB_NAME", "correctomatic_app")
        cls.DB_USER = os.getenv("DB_USER")
        cls.DB_PASSWORD = os.getenv("DB_PASSWORD")
        cls.DB_HOST = os.getenv("DB_HOST")
        cls.DB_PORT = os.getenv("DB_PORT", "5432")

        return super().initialize()

configurations = {
    'development': DevelopmentConfig.initialize(),
    'testing': TestingConfig.initialize(),
    'production': ProductionConfig.initialize()
}
