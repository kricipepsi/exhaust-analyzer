from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


class FetchError(RuntimeError):
    """Raised when fetching or parsing a URL fails."""
    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"Cannot fetch {url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Return JSON from *url*, backed by a file-based cache."""
    cache = _Cache(Path(cache_dir))
    cached = cache.read(url)
    if cached is not None:
        return cached
    data = _download_json(url)
    cache.write(url, data)
    return data


# ---- internal ----

def _download_json(url: str) -> dict:
    try:
        with urlopen(url, timeout=10) as response:
            raw = response.read()
    except (URLError, OSError) as exc:
        raise FetchError(url, str(exc)) from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(url, str(exc)) from exc


class _Cache:
    def __init__(self, root: Path) -> None:
        self._root = root

    def _path(self, key: str) -> Path:
        safe = "".join(ch if ch.isalnum() else "_" for ch in key)
        return self._root / f"{safe}.json"

    def read(self, key: str) -> dict | None:
        path = self._path(key)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def write(self, key: str, data: dict) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")
