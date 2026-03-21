# Dockerfile for Easypanel - FastAPI runs directly on port 80
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/images /app/instance

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:${PORT}/api/status || exit 1

# Run FastAPI via gunicorn with uvicorn workers - reads PORT env var (default 8000)
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 4 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --access-logfile - --error-logfile - backend.app:app
