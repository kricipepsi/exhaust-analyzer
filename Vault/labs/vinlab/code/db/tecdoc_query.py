"""SQL isolation layer for vref.db — all SQL strings live here (H8).

The decoder calls lookup_engine_ref() to fetch the tech-mask + CoC overlay
for a resolved engine_code. No other module writes SQL.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

__all__ = ["lookup_engine_ref", "open_vref_readonly"]


def lookup_engine_ref(db_path: Path, engine_code: str) -> dict[str, Any] | None:
    """Query vref.db engine_ref for tech-mask and CoC measurements.

    Args:
        db_path: Path to the vref.db SQLite database.
        engine_code: Resolved engine code from vds_engine_map.csv.

    Returns:
        Row as a dict keyed by column name, or None if not found.
    """
    uri = f"file:{db_path}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            "SELECT * FROM engine_ref WHERE engine_code = ?", (engine_code,)
        )
        row = cur.fetchone()
    if row is None:
        return None
    return dict(row)


def open_vref_readonly(db_path: Path) -> sqlite3.Connection:
    """Open vref.db in read-only mode via URI.

    The decoder calls this once in __init__ and reuses the connection.
    """
    uri = f"file:{db_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)
