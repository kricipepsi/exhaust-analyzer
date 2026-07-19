"""
tools/backfill_cylinder_count.py

Reads docs/cylinder_count_resolved.md, filters to HIGH and MEDIUM confidence
rows, and back-fills cylinder_count and engine_configuration into
vinlab/data/vds_engine_map.csv for rows whose engine_code appears in the
resolved list.  Runs idempotently — re-running on an already-updated CSV
produces an identical SHA-256.

H1 PETROL-ONLY: diesel guard checks that no diesel row gains a cylinder_count.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESOLVED_MD = ROOT / "docs" / "cylinder_count_resolved.md"
CSV_PATH = ROOT / "vinlab" / "data" / "vds_engine_map.csv"

# Known diesel fuel-system markers — rows with these must not gain cylinder_count.
DIESEL_MARKERS: frozenset[str] = frozenset({
    "DIRECT_INJECTION_DIESEL",
    "DIRECT_INJECTION_DIESEL_TURBO",
    "DIESEL",
    "TURBO_DIESEL",
    "COMMON_RAIL_DIESEL",
    "COMMON_RAIL_DIESEL_TURBO",
    "COMMON_RAIL_TURBO_DIESEL",
})


def sha256_hex(path: Path) -> str:
    """Return the SHA-256 hex digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_resolved_md(path: Path) -> list[dict[str, str]]:
    """Parse the markdown file, returning a list of dicts with keys
    engine_code, cylinder_count, engine_configuration, confidence.
    Only HIGH and MEDIUM confidence rows are returned."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    records: list[dict[str, str]] = []
    in_brand = False

    for line in lines:
        stripped = line.strip()

        # Detect brand header: "## BRAND_NAME (N codes)"
        if stripped.startswith("## ") and "codes)" in stripped:
            in_brand = True
            continue

        if not in_brand:
            continue

        # Skip blank lines, table headers, dividers, non-table content
        if not stripped:
            continue
        if stripped.startswith("|---"):
            continue
        if stripped.startswith("| Engine Code"):
            continue
        if not stripped.startswith("|"):
            # End of table for this brand
            in_brand = False
            continue

        # Parse table row: | Engine Code | Disp | Cyl | Config | Induction | Conf | Sample VIN | Note |
        parts = [p.strip() for p in stripped.split("|")]
        if len(parts) < 8:
            continue

        engine_code = parts[1]
        cylinder_count = parts[3]   # Cyl
        config = parts[4]           # Config
        confidence = parts[6]       # Conf

        if not engine_code:
            continue
        if confidence not in ("HIGH", "MEDIUM"):
            continue

        records.append({
            "engine_code": engine_code,
            "cylinder_count": cylinder_count,
            "engine_configuration": config,
            "confidence": confidence,
        })

    return records


def build_lookup(records: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """Build a case-insensitive lookup keyed by stripped engine_code.
    If duplicate engine_codes exist (different casing), the first wins."""
    lookup: dict[str, dict[str, str]] = {}
    for rec in records:
        key = rec["engine_code"].strip().upper()
        if key not in lookup:
            lookup[key] = rec
    return lookup


def is_diesel(fuel_system: str) -> bool:
    """Return True if the fuel_system_type string indicates diesel."""
    return fuel_system.strip().upper().replace(" ", "_") in DIESEL_MARKERS


def run(dry_run: bool = False) -> tuple[int, int, int, int]:
    """Main logic. Returns (filled_cyl, filled_cfg, total_rows, new_coverage_rows)."""

    # 1. Parse resolved MD
    records = parse_resolved_md(RESOLVED_MD)
    lookup = build_lookup(records)
    print(f"Parsed {len(records)} HIGH+MEDIUM rows from {RESOLVED_MD.name}")

    # 2. Read CSV
    old_hash = sha256_hex(CSV_PATH)
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    # Ensure engine_configuration column exists after cylinder_count
    if "engine_configuration" not in fieldnames:
        cyl_idx = fieldnames.index("cylinder_count")
        fieldnames.insert(cyl_idx + 1, "engine_configuration")
        for row in rows:
            row["engine_configuration"] = ""

    total_rows = len(rows)
    filled_cyl = 0
    filled_cfg = 0
    diesel_blocked = 0

    for row in rows:
        engine_code = row.get("engine_code", "").strip().upper()
        if not engine_code:
            continue

        resolved = lookup.get(engine_code)
        if resolved is None:
            continue

        fuel_system = row.get("fuel_system_type", "")

        # Diesel guard
        if is_diesel(fuel_system):
            diesel_blocked += 1
            continue

        # Fill cylinder_count only if empty or "0"
        existing_cyl = row.get("cylinder_count", "").strip()
        if not existing_cyl or existing_cyl == "0":
            row["cylinder_count"] = resolved["cylinder_count"]
            filled_cyl += 1

        # Fill engine_configuration only if empty
        existing_cfg = row.get("engine_configuration", "").strip()
        if not existing_cfg:
            row["engine_configuration"] = resolved["engine_configuration"]
            filled_cfg += 1

    # Sanitize pre-existing cylinder_count="1" — impossible for petrol
    # passenger vehicles 1990-2020 (smallest is 2-cyl microcar / 3-cyl).
    sanitized = 0
    for row in rows:
        if row.get("cylinder_count", "").strip() == "1":
            row["cylinder_count"] = ""
            sanitized += 1
    if sanitized:
        print(f"Sanitized {sanitized} pre-existing cylinder_count=1 rows")

    if dry_run:
        coverage = _calc_coverage(rows)
        print(f"Would fill {filled_cyl} cylinder_count, {filled_cfg} engine_configuration")
        print(f"Would reach coverage {coverage}/5806 ({coverage / 5806 * 100:.1f}%)")
        if diesel_blocked:
            print(f"Diesel guard would block {diesel_blocked} rows")
        return filled_cyl, filled_cfg, total_rows, coverage

    # Write CSV
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    new_hash = sha256_hex(CSV_PATH)
    coverage = _calc_coverage(rows)

    if filled_cyl == 0 and filled_cfg == 0:
        print(f"Filled 0 cylinder_count / 0 engine_configuration; coverage {coverage}/{total_rows} ({coverage / total_rows * 100:.1f}%)")
    else:
        print(f"Filled {filled_cyl} cylinder_count / {filled_cfg} engine_configuration; coverage {coverage}/{total_rows} ({coverage / total_rows * 100:.1f}%)")

    if diesel_blocked:
        print(f"Diesel guard blocked {diesel_blocked} rows")

    if old_hash != new_hash:
        print(f"SHA-256: {new_hash}")
    else:
        print("SHA-256 unchanged (idempotent)")

    return filled_cyl, filled_cfg, total_rows, coverage


def _calc_coverage(rows: list[dict[str, str]]) -> int:
    """Count rows where cylinder_count is non-empty and not '0'."""
    count = 0
    for row in rows:
        v = row.get("cylinder_count", "").strip()
        if v and v != "0":
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill cylinder_count from resolved MD")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be filled without modifying the CSV")
    args = parser.parse_args()

    filled_cyl, filled_cfg, total, coverage = run(dry_run=args.dry_run)

    # Exit non-zero if live run and targets not met (dry-run is always 0)
    if not args.dry_run:
        if filled_cyl == 0 and filled_cfg == 0:
            # Idempotent re-run — acceptable
            pass
        elif filled_cyl < 1400:
            print(f"FAIL: filled_cyl={filled_cyl} below threshold of 1400", file=sys.stderr)
            sys.exit(1)
        elif coverage / total < 0.78:
            print(f"FAIL: coverage {coverage}/{total} ({coverage / total * 100:.1f}%) below 78%", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
