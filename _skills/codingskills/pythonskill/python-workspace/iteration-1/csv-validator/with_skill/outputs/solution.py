"""CSV validator module for reading and validating CSV files efficiently."""

import csv
import logging
from pathlib import Path
from typing import Generator

logger = logging.getLogger(__name__)


def validate_name(value: str) -> tuple[bool, str | None]:
    """
    Validate a name field.

    Args:
        value: The name value to validate.

    Returns:
        A tuple of (is_valid, error_message). error_message is None if valid.
    """
    if not isinstance(value, str):
        return False, f"name must be a string, got {type(value).__name__}"

    if not value.strip():
        return False, "name cannot be empty"

    return True, None


def validate_age(value: str) -> tuple[bool, str | None]:
    """
    Validate an age field.

    Args:
        value: The age value to validate (as string from CSV).

    Returns:
        A tuple of (is_valid, error_message). error_message is None if valid.
    """
    try:
        age = int(value)
    except (ValueError, TypeError):
        return False, f"age must be an integer, got {value!r}"

    if age < 0 or age > 120:
        return False, f"age must be between 0 and 120, got {age}"

    return True, None


def read_and_validate_csv(
    file_path: Path | str,
) -> list[dict[str, str]]:
    """
    Read a CSV file, validate each row, and return valid records.

    Validates that each row has:
    - 'name': non-empty string
    - 'age': positive integer between 0 and 120

    Invalid rows are logged with a warning showing the row number and
    specific validation error, then skipped. This function handles large
    files efficiently by streaming rows rather than loading the entire
    file into memory.

    Args:
        file_path: Path to the CSV file (str or pathlib.Path).

    Returns:
        A list of valid records as dictionaries, where each dict has
        'name' and 'age' keys. Returns an empty list if no valid records
        are found or the file is empty.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file has no 'name' or 'age' column headers.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    valid_records = []

    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or has no headers")

            # Validate that required columns exist
            required_columns = {"name", "age"}
            if not required_columns.issubset(set(reader.fieldnames)):
                missing = required_columns - set(reader.fieldnames)
                raise ValueError(
                    f"CSV file missing required columns: {', '.join(sorted(missing))}"
                )

            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                # Validate name
                name_valid, name_error = validate_name(row.get("name", "").strip())
                if not name_valid:
                    logger.warning(
                        f"Row {row_num}: Invalid name - {name_error}"
                    )
                    continue

                # Validate age
                age_valid, age_error = validate_age(row.get("age", ""))
                if not age_valid:
                    logger.warning(
                        f"Row {row_num}: Invalid age - {age_error}"
                    )
                    continue

                # Both fields are valid; add the record
                valid_records.append({
                    "name": row["name"].strip(),
                    "age": row["age"],
                })

    except (FileNotFoundError, ValueError):
        raise
    except Exception as exc:
        logger.exception("Unexpected error reading CSV file: %s", file_path)
        raise

    return valid_records


def read_and_validate_csv_streaming(
    file_path: Path | str,
) -> Generator[dict[str, str], None, None]:
    """
    Read a CSV file and yield valid records as a generator.

    This streaming version is ideal for processing very large files where
    you don't need all records in memory at once. Invalid rows are logged
    with warnings and skipped.

    Args:
        file_path: Path to the CSV file (str or pathlib.Path).

    Yields:
        Valid records as dictionaries with 'name' and 'age' keys.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file has no 'name' or 'age' column headers.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or has no headers")

            # Validate that required columns exist
            required_columns = {"name", "age"}
            if not required_columns.issubset(set(reader.fieldnames)):
                missing = required_columns - set(reader.fieldnames)
                raise ValueError(
                    f"CSV file missing required columns: {', '.join(sorted(missing))}"
                )

            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                # Validate name
                name_valid, name_error = validate_name(row.get("name", "").strip())
                if not name_valid:
                    logger.warning(
                        f"Row {row_num}: Invalid name - {name_error}"
                    )
                    continue

                # Validate age
                age_valid, age_error = validate_age(row.get("age", ""))
                if not age_valid:
                    logger.warning(
                        f"Row {row_num}: Invalid age - {age_error}"
                    )
                    continue

                # Both fields are valid; yield the record
                yield {
                    "name": row["name"].strip(),
                    "age": row["age"],
                }

    except (FileNotFoundError, ValueError):
        raise
    except Exception as exc:
        logger.exception("Unexpected error reading CSV file: %s", file_path)
        raise
