# Use official python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system deps (optional but SAFE for psycopg2)
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment
ENV FLASK_APP=run.py

# Run migrations automatically when the container starts
CMD ["bash", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:${PORT} run:app"]
