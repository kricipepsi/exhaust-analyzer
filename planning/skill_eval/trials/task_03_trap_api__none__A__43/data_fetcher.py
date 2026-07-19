from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    pass


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    cache = DiskCache(cache_dir)
    cached = cache.get(url)
    if cached is not None:
        return cached

    response = get(url)
    if response.status_code != 200:
        raise FetchError(f"Failed to fetch {url}: HTTP {response.status_code}")

    try:
        data = response.json()
    except Exception as e:
        raise FetchError(f"Failed to parse JSON from {url}: {e}")

    cache.set(url, data)
    return data
