import os
from flask_sqlalchemy import SQLAlchemy

# https://alembic.sqlalchemy.org/en/latest/

db = SQLAlchemy()

def get_connection_string():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')

    return f'postgresql://{user}:{password}@{host}:{port}/correctomatic'

