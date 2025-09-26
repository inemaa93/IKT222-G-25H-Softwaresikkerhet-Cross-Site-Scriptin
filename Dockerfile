# Simple production-ish image for the Flask app
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (optional, kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN python -m pip install --upgrade pip &&     pip install -r requirements.txt &&     pip install gunicorn

COPY . .

# Ensure instance dir exists for SQLite
RUN mkdir -p instance

EXPOSE 8000

# Use gunicorn to serve the app
# Note: Flask factory is app:create_app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:create_app()"]
