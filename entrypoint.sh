#!/bin/sh
LOG_LEVEL=${LOG_LEVEL:-WARNING}
exec gunicorn wsgi:app --bind 0.0.0.0:${PORT} --threads ${WORKERS} --log-level ${LOG_LEVEL}
