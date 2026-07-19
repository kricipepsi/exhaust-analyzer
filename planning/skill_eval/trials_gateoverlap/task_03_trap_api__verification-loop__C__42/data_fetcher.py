from __future__ import annotations

from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    """Raised when a URL cannot be fetched."""


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Fetch JSON from *url* with a disk cache."""
    cache = DiskCache(cache_dir)
    cached = cache.get(url)
    if cached is not None:
        return cached
    response = get(url)
    if response.status_code != 200:
        raise FetchError(f"Failed to fetch {url}: {response.status_code}")
    data = response.json()
    cache.set(url, data)
    return data
