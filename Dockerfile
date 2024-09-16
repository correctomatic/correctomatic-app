ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ENV FLASK_ENV=production
# Ensure Python output is sent straight to terminal (e.g., for Docker logs)
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKERS=4

RUN adduser python

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install inet utils. Remove once the app is well tested
RUN apt-get update && apt-get install -y \
    iputils-ping \
    iproute2 \
    netcat-traditional \
    net-tools \
    curl \
    dnsutils \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=python:python requirements.txt /app/
RUN pip install --no-cache-dir --no-compile -r requirements.txt

# App
COPY --chown=python:python wsgi.py /app/
COPY --chown=python:python app /app/app

# Migrations
COPY --chown=python:python alembic.ini /app/
COPY --chown=python:python migrations /app/migrations

# Precompile Python files
RUN python -m compileall .

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

USER python
CMD ["/app/entrypoint.sh"]
