#!/bin/bash

# Exit on error
set -e

echo "Starting KHR Website Application..."

# Wait for database to be ready if using PostgreSQL
if [[ $DATABASE_URL == postgresql* ]]; then
    echo "Waiting for PostgreSQL to be ready..."
    for i in {1..30}; do
        if python -c "from sqlalchemy import create_engine; import os; create_engine(os.getenv('DATABASE_URL')).connect()" 2>/dev/null; then
            echo "PostgreSQL is ready!"
            break
        fi
        echo "Waiting for PostgreSQL... ($i/30)"
        sleep 2
    done
fi

# Initialize database tables (FastAPI app uses SQLAlchemy directly)
echo "Initializing database..."
python -c "
from backend.database import Base, engine
from backend import models  # noqa: F401 - import so models are registered
Base.metadata.create_all(bind=engine)
print('Database tables created successfully!')
"

# Seed initial data if needed
if [ "${SEED_DATA:-false}" = "true" ]; then
    echo "Seeding initial data..."
    python backend/seed_data.py || echo "Seed data script not found or failed"
fi

echo "Starting Gunicorn server (FastAPI via uvicorn worker)..."
exec gunicorn --bind 0.0.0.0:5000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    backend.app:app
