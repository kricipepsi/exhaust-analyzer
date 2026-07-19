# Task: Refactor Module

**Difficulty:** Medium · **Type:** Real-adjacent (refactor) · **Primary axes:** rubric (structure/naming/readability), cyclomatic complexity reduction

## Prompt

Refactor the provided `legacy_processor.py` to meet modern Python standards.
The module processes a list of sensor readings and generates a summary report.

**Goals (in priority order):**

1. **Make it readable.** The current code uses cryptic names and has no structure.
   Rename variables/functions to describe what they represent.
2. **Extract functions.** Break the monolithic logic into small, single-purpose functions.
3. **Add type hints.** Every function signature should be fully annotated.
4. **Fix error handling.** Replace bare excepts with specific exception handling.
5. **Add docstrings.** Every public function needs one.
6. **Preserve behavior.** The refactored module must pass the same tests as the original.

The module is used like this:
```python
from legacy_processor import process_readings
report = process_readings(readings, threshold=50.0)
```

## Input Format

`readings` is a list of dicts: `[{"sensor_id": str, "value": float, "unit": str}, ...]`

## Output Format

`report` is a dict:
```python
{
    "total_readings": int,
    "valid_readings": int,
    "invalid_readings": int,
    "by_unit": {unit: {"count": int, "avg": float, "max": float, "min": float}},
    "alerts": [{"sensor_id": str, "value": float, "threshold": float}],
}
```

An "alert" is any reading where value > threshold. An "invalid" reading is one
where value is None, negative, or has an unknown unit.

## Requirements

- Python 3.10+ syntax (use `X | Y`, not `Union[X, Y]`)
- All functions fully type-hinted
- No bare `except:`
- No mutable defaults
- Tests must still pass

## Output

Write the refactored `legacy_processor.py` in the working directory.
Also write `test_legacy_processor.py` if tests were missing (the original may or may not have tests).
