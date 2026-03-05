# PythonAnywhere WSGI configuration for Exhaust Analyzer
# Place this file in: /var/www/yourusername_pythonanywhere_com_wsgi.py

import sys
import os

# Add project directory to Python path
project_home = '/var/www/yourusername_pythonanywhere_com'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'
# IMPORTANT: Change this to a random secret in production!
os.environ['SECRET_KEY'] = 'change-me-to-random-32-char-string'

# Import Flask app as the application object
from app import app as application  # noqa
