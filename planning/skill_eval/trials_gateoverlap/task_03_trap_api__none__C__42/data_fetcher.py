from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    pass


def fetch_json(url, cache_dir="./cache"):
    cache = DiskCache(cache_dir)
    hit = cache.get(url)
    if hit is not None:
        return hit
    resp = get(url)
    if resp.status_code != 200:
        raise FetchError("bad status for " + url)
    data = resp.json()
    cache.set(url, data)
    return data
