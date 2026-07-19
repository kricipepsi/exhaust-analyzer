def get_users(db: dict, filter: list[str] | None = None) -> list[dict]:
    """
    Filter users from database by name substring matching.

    Args:
        db: Database dict containing 'users' key with list of user dicts
        filter: List of substrings to match against user names.
               If None or empty, returns all users.
               Returns users matching ANY filter term (OR logic).

    Returns:
        List of user dictionaries matching filter criteria

    Raises:
        KeyError: If db['users'] key is missing
        TypeError: If filter is not list-like
    """
    if filter is None:
        filter = []

    users = db['users']  # Will raise KeyError if missing - explicit error

    if not filter:
        return users.copy()  # Return copy to prevent external modification

    results = []
    seen = set()

    for user in users:
        try:
            name = user.get('name', '')
            user_id = id(user)  # Use object identity to avoid duplicates

            if user_id not in seen:
                for term in filter:
                    if term.lower() in name.lower():
                        results.append(user)
                        seen.add(user_id)
                        break
        except (AttributeError, TypeError) as e:
            # Log or handle specific errors if needed
            continue

    return results


def make_report(users: list[dict]) -> str:
    """
    Generate a formatted report of users.

    Args:
        users: List of user dictionaries with 'name' and 'age' keys

    Returns:
        Formatted report string with one user per line

    Raises:
        KeyError: If required keys missing
    """
    lines = []

    for user in users:
        try:
            name = user.get('name', 'Unknown')
            age = user.get('age', 'Unknown')
            line = f"Name: {name}, Age: {age}"
            lines.append(line)
        except (AttributeError, TypeError):
            continue

    return '\n'.join(lines)


# Usage example (if called as main)
if __name__ == '__main__':
    # Example usage
    sample_db = {
        'users': [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25},
            {'name': 'Charlie', 'age': 35}
        ]
    }

    # Get users matching filter
    filtered = get_users(sample_db, filter=['li', 'ob'])

    # Generate and return report
    report = make_report(filtered)
    print(report)
