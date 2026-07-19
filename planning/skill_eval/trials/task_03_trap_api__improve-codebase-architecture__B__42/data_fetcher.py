from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

__all__ = ["fetch_json", "FetchError"]


class FetchError(RuntimeError):
    """Fetch or parse failure for a URL."""
    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"{url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Return JSON from *url*, using a file-based disk cache."""
    store = _JsonStore(Path(cache_dir))
    if (data := store.load(url)) is not None:
        return data
    data = _http_get_json(url)
    store.save(url, data)
    return data


# ---- internal: all hidden behind the public function ----

class _JsonStore:
    """File-based JSON key-value store."""
    def __init__(self, root: Path) -> None:
        self._root = root

    def load(self, key: str) -> dict | None:
        path = self._make_path(key)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def save(self, key: str, data: dict) -> None:
        path = self._make_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def _make_path(self, key: str) -> Path:
        safe = "".join(ch if ch.isalnum() else "_" for ch in key)
        return self._root / f"{safe}.json"


def _http_get_json(url: str) -> dict:
    try:
        with urlopen(url, timeout=10) as resp:
            raw = resp.read()
    except (URLError, OSError) as exc:
        raise FetchError(url, str(exc)) from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(url, str(exc)) from exc
