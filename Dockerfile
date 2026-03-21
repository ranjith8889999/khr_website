# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including nginx
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the entire application
COPY . .

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Create necessary directories
RUN mkdir -p /app/images /app/instance /var/log/nginx

# Set permissions
RUN chmod +x start-server.sh 2>/dev/null || echo "start-server.sh will be made executable"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=backend/app.py

# Expose port (nginx will listen on 80, but we expose 5000 for Flask)
EXPOSE 5000 80

# Run the startup script
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile - --error-logfile - backend.app:app & nginx -g 'daemon off;'"]
