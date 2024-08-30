ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# Ensure Python output is sent straight to terminal (e.g., for Docker logs)
ENV PYTHONUNBUFFERED=1

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

# 7. Expose the port (optional, depending on the application)
# EXPOSE 8000  # Uncomment if you're running a web server

# 8. Run the application (use a more specific command for your app)
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
