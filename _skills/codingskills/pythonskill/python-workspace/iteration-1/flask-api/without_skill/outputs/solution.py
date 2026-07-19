"""
Production-quality Flask API for managing contacts with SQLite persistence.
Includes comprehensive input validation, error handling, parameterized queries, and logging.
"""

import logging
import sqlite3
import re
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flask_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Database configuration
DB_PATH = Path(__file__).parent / 'contacts.db'
DB_SCHEMA = '''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
'''

# Validation constants
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
MESSAGE_MIN_LENGTH = 1
MESSAGE_MAX_LENGTH = 500


def get_db_connection():
    """
    Create and return a database connection with row factory.

    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database schema if not already present."""
    try:
        conn = get_db_connection()
        conn.execute(DB_SCHEMA)
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise


def validate_email(email):
    """
    Validate email format using regex pattern.

    Args:
        email (str): Email address to validate

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not isinstance(email, str):
        return False, "Email must be a string"

    email = email.strip()

    if not email:
        return False, "Email is required"

    if len(email) > 254:
        return False, "Email is too long (max 254 characters)"

    if not re.match(EMAIL_PATTERN, email):
        return False, "Invalid email format"

    return True, None


def validate_message(message):
    """
    Validate message content and length.

    Args:
        message (str): Message content to validate

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not isinstance(message, str):
        return False, "Message must be a string"

    message = message.strip()

    if not message:
        return False, "Message is required"

    if len(message) < MESSAGE_MIN_LENGTH:
        return False, f"Message must be at least {MESSAGE_MIN_LENGTH} character"

    if len(message) > MESSAGE_MAX_LENGTH:
        return False, f"Message must not exceed {MESSAGE_MAX_LENGTH} characters"

    return True, None


def handle_api_errors(f):
    """
    Decorator to handle unexpected API errors with proper logging and response.

    Args:
        f: Flask view function

    Returns:
        Wrapped function with error handling
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            logger.warning(f"Integrity constraint violation: {e}")
            return jsonify({
                'success': False,
                'error': 'A contact with this email already exists'
            }), 409
        except sqlite3.Error as e:
            logger.error(f"Database error in {f.__name__}: {e}")
            return jsonify({
                'success': False,
                'error': 'Database error occurred'
            }), 500
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'An unexpected error occurred'
            }), 500

    return decorated_function


@app.route('/api/contacts', methods=['POST'])
@handle_api_errors
def create_contact():
    """
    Create a new contact with email and message.

    Request JSON body:
        {
            "email": "user@example.com",
            "message": "Contact message here"
        }

    Returns:
        JSON response with status and contact details or error message
        HTTP Status codes:
            - 201: Contact created successfully
            - 400: Invalid input (missing fields or validation failed)
            - 409: Email already exists
            - 415: Invalid content type
            - 500: Server error
    """
    # Validate content type
    if not request.is_json:
        logger.warning(f"Invalid content type: {request.content_type}")
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 415

    # Extract and log request data
    data = request.get_json(silent=True)
    if data is None:
        logger.warning("Failed to parse JSON body")
        return jsonify({
            'success': False,
            'error': 'Invalid JSON format'
        }), 400

    # Validate required fields
    email = data.get('email')
    message = data.get('message')

    if email is None:
        logger.info("Missing email field in request")
        return jsonify({
            'success': False,
            'error': 'Email field is required'
        }), 400

    if message is None:
        logger.info("Missing message field in request")
        return jsonify({
            'success': False,
            'error': 'Message field is required'
        }), 400

    # Validate email format
    is_valid_email, email_error = validate_email(email)
    if not is_valid_email:
        logger.info(f"Invalid email format: {email_error}")
        return jsonify({
            'success': False,
            'error': email_error
        }), 400

    # Validate message content
    is_valid_message, message_error = validate_message(message)
    if not is_valid_message:
        logger.info(f"Invalid message: {message_error}")
        return jsonify({
            'success': False,
            'error': message_error
        }), 400

    # Insert into database with parameterized query
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Use parameterized query to prevent SQL injection
        cursor.execute(
            '''INSERT INTO contacts (email, message, created_at, updated_at)
               VALUES (?, ?, ?, ?)''',
            (email.strip(), message.strip(), datetime.utcnow().isoformat(), datetime.utcnow().isoformat())
        )

        conn.commit()
        contact_id = cursor.lastrowid
        conn.close()

        logger.info(f"Contact created successfully - ID: {contact_id}, Email: {email}")

        return jsonify({
            'success': True,
            'message': 'Contact created successfully',
            'contact': {
                'id': contact_id,
                'email': email.strip(),
                'message': message.strip()
            }
        }), 201

    finally:
        if conn:
            conn.close()


@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
@handle_api_errors
def get_contact(contact_id):
    """
    Retrieve a contact by ID.

    Args:
        contact_id (int): Contact ID

    Returns:
        JSON response with contact details or error message
        HTTP Status codes:
            - 200: Contact found
            - 404: Contact not found
            - 500: Server error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Use parameterized query
        cursor.execute('SELECT id, email, message, created_at FROM contacts WHERE id = ?', (contact_id,))
        contact = cursor.fetchone()
        conn.close()

        if not contact:
            logger.info(f"Contact not found - ID: {contact_id}")
            return jsonify({
                'success': False,
                'error': 'Contact not found'
            }), 404

        logger.info(f"Contact retrieved - ID: {contact_id}")

        return jsonify({
            'success': True,
            'contact': dict(contact)
        }), 200

    finally:
        if conn:
            conn.close()


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.

    Returns:
        JSON response with health status
    """
    return jsonify({
        'success': True,
        'status': 'healthy'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.info(f"Endpoint not found: {request.path}")
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    logger.info(f"Method not allowed: {request.method} {request.path}")
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


if __name__ == '__main__':
    # Initialize database before starting the app
    init_db()

    # Run Flask development server
    app.run(debug=False, host='127.0.0.1', port=5000)
