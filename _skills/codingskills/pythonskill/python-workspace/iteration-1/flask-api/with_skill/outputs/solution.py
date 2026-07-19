"""Flask API endpoint for managing contacts with SQLite persistence.

This module implements a production-quality REST API endpoint for storing
contact information with proper input validation, error handling, and logging.
"""

from __future__ import annotations

import logging
import re
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request

# Configure logging at module level
logger = logging.getLogger(__name__)

# Constants
DATABASE_PATH = Path(__file__).parent / "contacts.db"
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
MESSAGE_MIN_LENGTH = 1
MESSAGE_MAX_LENGTH = 500
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_ERROR = 500


def init_app(app: Flask) -> None:
    """Initialize the Flask application with database setup and routes.

    Args:
        app: Flask application instance to configure
    """
    setup_database()
    register_routes(app)


def setup_database() -> None:
    """Create contacts table if it does not exist.

    Uses parameterised SQL to prevent injection and proper context management
    for database connections.
    """
    try:
        with sqlite3.connect(str(DATABASE_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        logger.info("Database initialized successfully at %s", DATABASE_PATH)
    except sqlite3.Error as exc:
        logger.error("Failed to initialize database: %s", exc, exc_info=True)
        raise


def validate_email(email: str) -> tuple[bool, str | None]:
    """Validate email format.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message). error_message is None if valid.
    """
    if not isinstance(email, str):
        return False, "Email must be a string"

    if not email.strip():
        return False, "Email cannot be empty"

    if len(email) > 254:
        return False, "Email is too long (max 254 characters)"

    if not EMAIL_REGEX.match(email):
        return False, "Invalid email format"

    return True, None


def validate_message(message: str) -> tuple[bool, str | None]:
    """Validate message content and length.

    Args:
        message: Message text to validate

    Returns:
        Tuple of (is_valid, error_message). error_message is None if valid.
    """
    if not isinstance(message, str):
        return False, "Message must be a string"

    if len(message) < MESSAGE_MIN_LENGTH:
        return False, "Message cannot be empty"

    if len(message) > MESSAGE_MAX_LENGTH:
        return (
            False,
            f"Message exceeds maximum length ({MESSAGE_MAX_LENGTH} characters)"
        )

    return True, None


def save_contact(email: str, message: str) -> dict[str, Any]:
    """Save contact to database with parameterised query.

    Args:
        email: Contact email address
        message: Contact message

    Returns:
        Dictionary with success status and contact ID or error message

    Raises:
        sqlite3.Error: If database operation fails
    """
    try:
        with sqlite3.connect(str(DATABASE_PATH)) as conn:
            cursor = conn.cursor()
            # Use parameterised query to prevent SQL injection
            cursor.execute(
                "INSERT INTO contacts (email, message) VALUES (?, ?)",
                (email, message)
            )
            conn.commit()
            contact_id = cursor.lastrowid

            logger.info(
                "Contact saved successfully",
                extra={"contact_id": contact_id, "email_domain": email.split("@")[1]}
            )

            return {
                "success": True,
                "contact_id": contact_id,
                "message": "Contact saved successfully"
            }
    except sqlite3.Error as exc:
        logger.error("Database error while saving contact: %s", exc, exc_info=True)
        raise


def register_routes(app: Flask) -> None:
    """Register API routes with the Flask application.

    Args:
        app: Flask application instance
    """
    @app.route("/api/contacts", methods=["POST"])
    def create_contact() -> tuple[dict[str, Any], int]:
        """Handle POST request to create a new contact.

        Expects JSON body with:
        - email (required, string): Valid email address
        - message (required, string): Message 1-500 characters

        Returns:
            Tuple of (response_dict, http_status_code)
        """
        # Validate request has JSON body
        if not request.is_json:
            logger.warning("Request missing JSON content type")
            return {
                "error": "Request must be JSON",
                "code": "INVALID_CONTENT_TYPE"
            }, HTTP_BAD_REQUEST

        try:
            data = request.get_json()
        except Exception as exc:
            logger.warning("Failed to parse JSON body: %s", exc)
            return {
                "error": "Invalid JSON in request body",
                "code": "MALFORMED_JSON"
            }, HTTP_BAD_REQUEST

        # Validate email field exists and is valid
        email = data.get("email") if isinstance(data, dict) else None
        if email is None:
            logger.warning("Request missing required field: email")
            return {
                "error": "Missing required field: email",
                "code": "MISSING_EMAIL"
            }, HTTP_BAD_REQUEST

        is_valid_email, email_error = validate_email(email)
        if not is_valid_email:
            logger.warning("Invalid email provided: %s", email_error)
            return {
                "error": email_error,
                "code": "INVALID_EMAIL"
            }, HTTP_BAD_REQUEST

        # Validate message field exists and is valid
        message = data.get("message") if isinstance(data, dict) else None
        if message is None:
            logger.warning("Request missing required field: message")
            return {
                "error": "Missing required field: message",
                "code": "MISSING_MESSAGE"
            }, HTTP_BAD_REQUEST

        is_valid_message, message_error = validate_message(message)
        if not is_valid_message:
            logger.warning("Invalid message provided: %s", message_error)
            return {
                "error": message_error,
                "code": "INVALID_MESSAGE"
            }, HTTP_BAD_REQUEST

        # Attempt to save contact
        try:
            result = save_contact(email, message)
            return {
                "success": True,
                "contact_id": result["contact_id"],
                "message": "Contact saved successfully"
            }, HTTP_CREATED
        except sqlite3.Error:
            logger.error(
                "Failed to save contact to database",
                exc_info=True
            )
            return {
                "error": "Failed to save contact. Please try again later.",
                "code": "DATABASE_ERROR"
            }, HTTP_INTERNAL_ERROR


def create_app() -> Flask:
    """Create and configure Flask application instance.

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Configure logging for the app
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s"
    )

    init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
