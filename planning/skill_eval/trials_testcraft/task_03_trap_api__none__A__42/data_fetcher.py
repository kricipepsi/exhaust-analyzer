from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


class FetchError(RuntimeError):
    """Raised when a URL cannot be fetched or its response is not valid JSON."""

    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"FetchError for {url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Return parsed JSON from *url*, using a file-based disk cache.

    On a cache hit the cached value is returned. On a miss the URL is fetched
    and stored before returning. Raises :exc:`FetchError` when the URL cannot be
    reached or its body is not valid JSON.
    """
    cache_path = Path(cache_dir) / _cache_key(url)
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    try:
        with urlopen(url, timeout=10) as response:
            raw = response.read()
    except (URLError, OSError) as exc:
        raise FetchError(url, str(exc)) from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(url, f"invalid JSON: {exc}") from exc

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data), encoding="utf-8")
    return data


def _cache_key(url: str) -> str:
    """Return a filesystem-safe cache filename for *url*."""
    safe = "".join(character if character.isalnum() else "_" for character in url)
    return f"{safe}.json"
