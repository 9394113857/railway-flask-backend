# Use official python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Railway provides PORT environment variable
ENV PORT=5000

# Expose port for Railway
EXPOSE 5000

# ---------------------------------------------------------
# Run database migrations automatically BEFORE starting app
# ---------------------------------------------------------
CMD flask db upgrade && gunicorn -b 0.0.0.0:5000 run:app
