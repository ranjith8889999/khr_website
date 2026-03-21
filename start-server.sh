#!/bin/bash

# Start Flask backend with gunicorn in the background
echo "Starting Flask backend..."
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile - --error-logfile - backend.app:app &

# Wait a bit for backend to start
sleep 3

# Start Nginx to serve static files and proxy API requests
echo "Starting Nginx..."
nginx -g 'daemon off;'
