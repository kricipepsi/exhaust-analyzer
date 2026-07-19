"""Download and cache vPIC SQLite database from corgi.

Downloads vpic.lite.db.gz, verifies SHA256, decompresses to a local cache.
Skips download if cached file matches published checksum.

Typical usage:
    python tools/import_vpic.py                   # download + cache (default)
    python tools/import_vpic.py --force            # re-download even if cached
    python tools/import_vpic.py --cache /tmp/vpic  # custom cache directory
"""

from __future__ import annotations

import gzip
import hashlib
import shutil
import sys
from pathlib import Path

import requests

DEFAULT_CACHE_DIR = Path.home() / ".vinlab-cache"
VPIC_URL = "https://corgi.cardog.io/vpic.lite.db.gz"
VPIC_SHA256_URL = "https://corgi.cardog.io/vpic.lite.sha256"
VPIC_DB_NAME = "vpic.lite.db"
VPIC_GZ_NAME = "vpic.lite.db.gz"


class VPICDownloadError(Exception):
    """Raised when vPIC download or verification fails."""


def _fetch_sha256() -> str:
    """Fetch the published SHA256 from corgi."""
    resp = requests.get(VPIC_SHA256_URL, timeout=30)
    resp.raise_for_status()
    for line in resp.text.strip().splitlines():
        if ".gz" in line:
            return line.strip().split()[0].lower()
    raise VPICDownloadError("Could not find .gz checksum in SHA256 file")


def _compute_sha256(path: Path) -> str:
    """Compute SHA256 hex digest of a file."""
    sha = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest().lower()


def ensure_vpic_db(cache_dir: Path | None = None, force: bool = False) -> Path:
    """Return path to vpic.lite.db, downloading if necessary.

    Args:
        cache_dir: Directory for cached files. Defaults to ~/.vinlab-cache/.
        force: If True, re-download even when cached file matches checksum.

    Returns:
        Path to the decompressed vpic.lite.db file.

    Raises:
        VPICDownloadError: If download or SHA256 verification fails.
    """
    if cache_dir is None:
        cache_dir = DEFAULT_CACHE_DIR
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    db_path = cache_dir / VPIC_DB_NAME
    gz_path = cache_dir / VPIC_GZ_NAME

    published_sha = _fetch_sha256()

    if not force and gz_path.exists():
        local_sha = _compute_sha256(gz_path)
        if local_sha == published_sha:
            if not db_path.exists():
                _decompress(gz_path, db_path)
            return db_path
        gz_path.unlink()

    _download_gz(gz_path)

    local_sha = _compute_sha256(gz_path)
    if local_sha != published_sha:
        gz_path.unlink()
        raise VPICDownloadError(
            f"SHA256 mismatch: expected {published_sha}, got {local_sha}"
        )

    _decompress(gz_path, db_path)
    return db_path


def _download_gz(dest: Path) -> None:
    """Download vpic.lite.db.gz to dest."""
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    try:
        resp = requests.get(VPIC_URL, timeout=300, stream=True)
        resp.raise_for_status()
        with tmp.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        tmp.rename(dest)
    except requests.RequestException as exc:
        if tmp.exists():
            tmp.unlink()
        raise VPICDownloadError(f"Download failed: {exc}") from exc


def _decompress(gz_path: Path, db_path: Path) -> None:
    """Decompress gz_path to db_path."""
    tmp = db_path.with_suffix(db_path.suffix + ".tmp")
    tmp.unlink(missing_ok=True)
    try:
        with gzip.open(gz_path, "rb") as gz_f, tmp.open("wb") as out_f:
            shutil.copyfileobj(gz_f, out_f, length=1_048_576)
        db_path.unlink(missing_ok=True)
        tmp.rename(db_path)
    except OSError as exc:
        tmp.unlink(missing_ok=True)
        raise VPICDownloadError(f"Decompression failed: {exc}") from exc


if __name__ == "__main__":
    force = "--force" in sys.argv
    cache_arg = None
    for i, arg in enumerate(sys.argv[1:], start=1):
        if arg == "--cache" and i < len(sys.argv) - 1:
            cache_arg = Path(sys.argv[i + 1])

    try:
        db = ensure_vpic_db(cache_dir=cache_arg, force=force)
        print(f"vPIC database ready: {db}")
    except VPICDownloadError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
