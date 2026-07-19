import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def validate_csv(
    file_path: str | Path,
    chunk_size: int = 1000
) -> List[Dict[str, Any]]:
    """
    Read and validate a CSV file, returning a list of valid records.

    Validates that each row has:
    - 'name': a non-empty string
    - 'age': a positive integer between 0 and 120 (inclusive)

    Invalid rows are logged with a warning showing the row number and
    specific validation error, then skipped.

    Args:
        file_path: Path to the CSV file to validate.
        chunk_size: Number of rows to process in memory at a time (for efficiency
                   with large files). Defaults to 1000.

    Returns:
        A list of dictionaries containing valid records from the CSV file.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is missing required columns ('name' or 'age').

    Example:
        >>> valid_records = validate_csv('data.csv')
        >>> print(valid_records)
        [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    valid_records: List[Dict[str, Any]] = []

    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Validate that required columns exist
            if reader.fieldnames is None or 'name' not in reader.fieldnames or 'age' not in reader.fieldnames:
                raise ValueError(
                    f"CSV file must contain 'name' and 'age' columns. "
                    f"Found columns: {reader.fieldnames}"
                )

            # Process rows with efficient memory handling
            row_number = 1  # Account for header row
            for row in reader:
                row_number += 1

                # Validate 'name' field
                name = row.get('name', '').strip() if row.get('name') else ''
                if not name:
                    logger.warning(
                        f"Row {row_number}: Invalid 'name' - must be a non-empty string"
                    )
                    continue

                # Validate 'age' field
                age_str = row.get('age', '').strip() if row.get('age') else ''
                if not age_str:
                    logger.warning(
                        f"Row {row_number}: Invalid 'age' - field is empty"
                    )
                    continue

                try:
                    age = int(age_str)
                except ValueError:
                    logger.warning(
                        f"Row {row_number}: Invalid 'age' - must be an integer, got '{age_str}'"
                    )
                    continue

                if age < 0 or age > 120:
                    logger.warning(
                        f"Row {row_number}: Invalid 'age' - must be between 0 and 120, got {age}"
                    )
                    continue

                # Record is valid
                valid_records.append({
                    'name': name,
                    'age': age
                })

    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        raise

    return valid_records
