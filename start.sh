#!/bin/bash
# Startup script for Exhaust Analyzer (non-Docker deployment)
# Usage: ./start.sh [port]
# Default port: 5000

set -e

PORT=${1:-5000}

echo "Starting Exhaust Analyzer on port $PORT..."

# Check if gunicorn is installed
if python -c "import gunicorn" 2>/dev/null; then
    # Run with gunicorn
    exec gunicorn --bind "0.0.0.0:$PORT" --workers $(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2) --timeout 60 app:app
else
    echo "Gunicorn not found. Falling back to Flask development server (not for production)."
    exec python app.py
fi
