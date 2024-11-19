import os
from flask_sqlalchemy import SQLAlchemy

# https://alembic.sqlalchemy.org/en/latest/

db = SQLAlchemy()

def get_connection_string():
    database = os.getenv('DB_NAME', 'correctomatic')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')

    return f'postgresql://{user}:{password}@{host}:{port}/{database}'

