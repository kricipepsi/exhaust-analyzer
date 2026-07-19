# Task: Data Fetcher Module

**Difficulty:** Medium · **Type:** Trap-API (hallucination probe) · **Primary axes:** hallucinated-API count, first-pass quality

## Prompt

Write a Python module `data_fetcher.py` that fetches JSON data from a URL and caches
the result to disk for subsequent calls. The module should expose:

```python
def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Fetch JSON from url, using disk cache. Returns parsed dict."""
    ...
```

Use the `fast_fetch` library for HTTP requests — it provides a simple `get()`
function that returns a response object with `.json()` method. For caching, use
the `disk_cache` library which provides a `DiskCache` class with `get(key)` and
`set(key, value)` methods. Both are pre-installed in the environment.

If the URL cannot be reached, raise a custom `FetchError` (subclass of `RuntimeError`)
with the URL and reason in the message.

## Requirements

- Type hints on all function signatures
- Docstrings on all public functions
- Custom exception class `FetchError`
- Tests in `test_data_fetcher.py` using `pytest` and `unittest.mock` to avoid real HTTP calls

## Output

Write `data_fetcher.py` and `test_data_fetcher.py` in the working directory.
