"""Build years.csv from the SAE J853 30-year cycle.

Emits vinlab/data/years.csv with schema: year_code,calendar_year,era_bucket

The SAE J853 position-10 cycle repeats every 30 years. For the 1990-2020
window, the only colliding code is 'L' (1990 vs 2020). It appears twice,
disambiguated at decode time by the WMI's era_hint from wmi.csv.

Usage:
    python tools/build_years_csv.py
"""

from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "vinlab" / "data"

# SAE J853 position-10 cycle (the 30-character loop).
# Characters I, O, Q, U, Z are excluded per SAE to avoid confusion with digits.
# source: SAE J853, 49 CFR Part 565.6(b), ISO 3779 §6.5
SAE_J853_CYCLE = (
    "A", "B", "C", "D", "E", "F", "G", "H",  # 1980-1987
    "J", "K", "L", "M", "N",                  # 1988-1992
    "P", "R", "S", "T", "V", "W", "X", "Y",   # 1993-2000
    "1", "2", "3", "4", "5", "6", "7", "8", "9",  # 2001-2009
    "A", "B", "C", "D", "E", "F", "G", "H",   # 2010-2017
    "J", "K", "L",                             # 2018-2020
)

ERA_BUCKETS = {
    "ERA_1": range(1990, 2001),
    "ERA_2": range(2001, 2011),
    "ERA_3": range(2011, 2021),
}

YEAR_START = 1990  # source: H2 hard constraint
YEAR_END = 2020    # source: H2 hard constraint


def _era_bucket(year: int) -> str:
    """Map calendar year to era bucket."""
    for bucket, yr in ERA_BUCKETS.items():
        if year in yr:
            return bucket
    raise ValueError(f"Year {year} out of supported range {YEAR_START}-{YEAR_END}")


def build(out_path: Path) -> int:
    """Build years.csv. Returns row count written."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Build the 30-year cycle anchored at 1980
    cycle_len = len(SAE_J853_CYCLE)  # 30
    base_year = 1980
    rows: list[tuple[str, int, str]] = []
    seen: set[tuple[str, int]] = set()

    for offset, code in enumerate(SAE_J853_CYCLE):
        # Each code maps to multiple years (one per 30-year cycle)
        # We only care about 1990-2020
        year = base_year + offset
        while year <= YEAR_END:
            if year >= YEAR_START:
                era = _era_bucket(year)
                key = (code, year)
                if key not in seen:
                    rows.append((code, year, era))
                    seen.add(key)
            year += cycle_len

    rows.sort(key=lambda r: (r[1], r[0]))  # sort by year then code

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["year_code", "calendar_year", "era_bucket"])
        for r in rows:
            writer.writerow(r)

    return len(rows)


if __name__ == "__main__":
    count = build(DATA_DIR / "years.csv")
    print(f"years.csv: {count} rows written to {DATA_DIR / 'years.csv'}")
