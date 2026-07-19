"""User database and reporting utilities."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_users(
    db: dict[str, Any],
    filters: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Retrieve users from the database, optionally filtered by name.

    Args:
        db: Dictionary with 'users' key containing a list of user dictionaries.
        filters: List of strings to match against user names (case-sensitive substring match).
                If None or empty, all users are returned.

    Returns:
        List of user dictionaries matching the filter criteria.

    Raises:
        ValueError: If database structure is invalid.
        KeyError: If a user is missing required 'name' field.
    """
    if "users" not in db:
        raise ValueError("Database must contain 'users' key")
    if not isinstance(db["users"], list):
        raise ValueError("db['users'] must be a list")

    if filters is None:
        filters = []

    results = []
    for user in db["users"]:
        # Validate user structure
        if "name" not in user:
            logger.warning("Skipping user with missing 'name' field: %s", user)
            continue

        # If no filters, include all; otherwise include if any filter matches
        if not filters or any(f in user["name"] for f in filters):
            results.append(user)

    return results


def make_report(users: list[dict[str, Any]]) -> str:
    """
    Generate a formatted report from user data.

    Args:
        users: List of user dictionaries with 'name' and 'age' keys.

    Returns:
        Formatted report string with one user per line.
    """
    lines = [f"Name: {u['name']}, Age: {u['age']}" for u in users]
    return "\n".join(lines)
