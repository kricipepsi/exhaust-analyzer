---
name: python-testing
description: Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements.
origin: ECC
---

# Python Testing Patterns

Comprehensive testing strategies for Python applications using pytest, TDD methodology, and best practices.

## When to Activate

- Writing new Python code (follow TDD: red, green, refactor)
- Designing test suites for Python projects
- Reviewing Python test coverage
- Setting up testing infrastructure

## Core Testing Philosophy

### Test-Driven Development (TDD)

Always follow the TDD cycle:

1. **RED**: Write a failing test for the desired behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code while keeping tests green

```python
# Step 1: Write failing test (RED)
def test_add_numbers():
    result = add(2, 3)
    assert result == 5

# Step 2: Write minimal implementation (GREEN)
def add(a, b):
    return a + b

# Step 3: Refactor if needed (REFACTOR)
```

### Coverage Requirements

- **Target**: 80%+ code coverage
- **Critical paths**: 100% coverage required
- Use `pytest --cov` to measure coverage

```bash
pytest --cov=mypackage --cov-report=term-missing --cov-report=html
```

## pytest Fundamentals

### Basic Test Structure

```python
import pytest

def test_addition():
    """Test basic addition."""
    assert 2 + 2 == 4
```

### Assertions

```python
assert result == expected
assert result is None
assert item in collection
with pytest.raises(ValueError):
    raise ValueError("error message")
with pytest.raises(ValueError, match="invalid input"):
    raise ValueError("invalid input provided")
```

## Fixtures

```python
@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

@pytest.fixture
def database():
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()
```

### Fixture Scopes

```python
@pytest.fixture(scope="module")   # once per module
@pytest.fixture(scope="session")  # once per session
```

## Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

## Mocking and Patching

```python
from unittest.mock import patch, Mock

@patch("mypackage.external_api_call")
def test_with_mock(api_call_mock):
    api_call_mock.return_value = {"status": "success"}
    result = my_function()
    api_call_mock.assert_called_once()
    assert result["status"] == "success"
```

## Test Organization

```
tests/
├── conftest.py
├── unit/
│   ├── test_models.py
│   └── test_utils.py
└── integration/
    └── test_api.py
```

## pytest Configuration (pytest.ini)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = --strict-markers --cov=mypackage --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

## Running Tests

```bash
pytest                              # Run all tests
pytest tests/test_utils.py          # Run specific file
pytest -v                           # Verbose output
pytest --cov=mypackage              # With coverage
pytest -m "not slow"                # Skip slow tests
pytest -x                           # Stop on first failure
pytest --lf                         # Run last failed
```

## Best Practices

**DO:**
- Follow TDD: write tests before code
- Test one thing per test
- Use descriptive names: `test_user_login_with_invalid_credentials_fails`
- Mock external dependencies
- Test edge cases: empty inputs, None values, boundary conditions

**DON'T:**
- Test implementation details — test behaviour
- Share state between tests
- Catch exceptions in tests — use `pytest.raises`
- Write tests that are too brittle

**Remember**: Tests are code too. Keep them clean, readable, and maintainable.
