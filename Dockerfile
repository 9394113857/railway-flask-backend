# Use official python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run migrations when container starts
CMD flask db upgrade && gunicorn -b 0.0.0.0:$PORT run:app
