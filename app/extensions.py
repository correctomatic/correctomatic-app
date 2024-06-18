import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_connection_string():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST', 'localhost')

    return f'postgresql://{user}:{password}@{host}/correctomatic'

