"""SQL isolation layer for vref.db — all SQL strings live here (H8).

The decoder calls lookup_engine_ref() to fetch the tech-mask + CoC overlay
for a resolved engine_code. No other module writes SQL.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

__all__ = ["lookup_engine_ref", "open_vref_readonly"]


import re
from functools import lru_cache



def _normalise_code(raw: str) -> str:
    """Normalize engine code for joining: uppercase, alphanumeric only."""
    return re.sub(r"[^A-Z0-9]", "", raw.upper())


@lru_cache(maxsize=1)
def _build_normalised_index(db_path: Path) -> dict[str, str]:
    """Build an in-memory index mapping normalized engine_code -> actual engine_code.

    This is cached per db_path so the index is built once per process.
    """
    uri = f"file:{db_path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        cur = conn.execute("SELECT engine_code FROM engine_ref")
        index = {}
        for row in cur:
            actual = row[0]
            norm = _normalise_code(actual)
            # Only store first mapping (deterministic iteration order)
            if norm not in index:
                index[norm] = actual
        return index
    finally:
        conn.close()


def lookup_engine_ref(db_path: Path, engine_code: str) -> dict[str, Any] | None:
    """Query vref.db engine_ref for tech-mask and CoC measurements.

    Args:
        db_path: Path to the vref.db SQLite database.
        engine_code: Resolved engine code from vds_engine_map.csv.

    Returns:
        Row as a dict keyed by column name, or None if not found.

    Tries exact match first, then normalized match (uppercase, alphanumeric only)
    to handle spelling variations like "K4M G8" vs "K4MG8" vs "K4M_G8".
    """
    if not engine_code:
        return None

    uri = f"file:{db_path}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        conn.row_factory = sqlite3.Row
        # Try exact match first
        cur = conn.execute(
            "SELECT * FROM engine_ref WHERE engine_code = ?", (engine_code,)
        )
        row = cur.fetchone()
        if row is not None:
            return dict(row)

    # Fallback: normalized match
    norm_code = _normalise_code(engine_code)
    norm_index = _build_normalised_index(db_path)
    actual_code = norm_index.get(norm_code)
    if actual_code is not None:
        with sqlite3.connect(uri, uri=True) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute(
                "SELECT * FROM engine_ref WHERE engine_code = ?", (actual_code,)
            )
            row = cur.fetchone()
            if row is not None:
                return dict(row)

    return None


def open_vref_readonly(db_path: Path) -> sqlite3.Connection:
    """Open vref.db in read-only mode via URI.

    The decoder calls this once in __init__ and reuses the connection.
    """
    uri = f"file:{db_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)
