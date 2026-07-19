from __future__ import annotations

from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    """Raised when a URL cannot be fetched or returns a non-200 response."""

    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"FetchError for {url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Return parsed JSON from *url*, using a disk cache.

    Raises FetchError (with the URL in the message) when the URL cannot be
    reached or returns a non-200 status.
    """
    cache = DiskCache(cache_dir)
    cached = cache.get(url)
    if cached is not None:
        return cached
    response = get(url)
    if response.status_code != 200:
        raise FetchError(url, f"HTTP {response.status_code}")
    data = response.json()
    cache.set(url, data)
    return data
