# Dockerfile for 5-Gas Exhaust Analyzer
# Build: docker build -t exhaust-analyzer:latest .
# Run:   docker run -p 5000:5000 --env-file .env exhaust-analyzer:latest

# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if any needed, e.g., gcc for some packages). For this app, none beyond Python.
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
COPY app.py .
COPY engine/ engine/
COPY knowledge/ knowledge/
COPY static/ static/
COPY templates/ templates/

# Install Python dependencies (from project's requirements) and gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Set environment variables (can be overridden at runtime)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
# IMPORTANT: set a strong SECRET_KEY via .env or docker -e

# Expose the port the app runs on
EXPOSE 5000

# Run the app with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
