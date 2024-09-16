#!/bin/sh
LOG_LEVEL=${LOG_LEVEL:-WARNING}

# Run alembic migrations
alembic upgrade head

# Start the server
exec gunicorn wsgi:app --bind 0.0.0.0:${PORT} --threads ${WORKERS} --log-level ${LOG_LEVEL}
