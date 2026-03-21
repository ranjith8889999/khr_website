# Dockerfile for Easypanel - FastAPI + nginx + supervisord
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including nginx and supervisor
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/images /app/instance /var/log/supervisor

# Copy nginx config
RUN cp /app/nginx.conf /etc/nginx/sites-available/default

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose port 80 (nginx front-end; EasyPanel proxies to port 80)
EXPOSE 80

# Health check via nginx
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:80/api/status || exit 1

# Start both nginx and gunicorn via supervisord
CMD ["supervisord", "-c", "/app/supervisord.conf"]
