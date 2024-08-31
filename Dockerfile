ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ENV FLASK_ENV=production
# Ensure Python output is sent straight to terminal (e.g., for Docker logs)
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKERS=4

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir --no-compile -r requirements.txt

COPY wsgi.py /app/
COPY app /app/app

# Precompile Python files
RUN python -m compileall .

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
