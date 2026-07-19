"""Build wmi.csv from vPIC WMI data + petrol CSV era hints.

Emits vinlab/data/wmi.csv with schema: wmi,brand,country,era_hint

Usage:
    python tools/build_wmi_map.py
    python tools/build_wmi_map.py --petrol-csv <path>
"""

from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "vinlab" / "data"
VEHICLE_DATA_ROOT_ENV = os.environ.get("VEHICLE_DATA_ROOT")
if not VEHICLE_DATA_ROOT_ENV:
    raise RuntimeError("VEHICLE_DATA_ROOT environment variable is not set")
DEFAULT_PETROL_CSV = (
    Path(VEHICLE_DATA_ROOT_ENV)
    / "petrol_vin"
    / "vehicles_petrol_specimens.csv"
)

# source: SAE J853 + VINlookup.md — scope is 1990-2020
ERA_SPLIT_YEAR = 2000


def _load_vpic_wmis(vpic_db: Path) -> dict[str, dict[str, str]]:
    """Return {wmi: {brand, country}} from vPIC for passenger-car WMIs."""
    import sqlite3

    conn = sqlite3.connect(str(vpic_db))
    rows = conn.execute("""
        SELECT w.Wmi, COALESCE(m.Name, '') AS brand, COALESCE(c.Name, '') AS country
        FROM Wmi w
        LEFT JOIN Wmi_Make wm ON w.Id = wm.WmiId
        LEFT JOIN Make m ON wm.MakeId = m.Id
        LEFT JOIN Country c ON w.CountryId = c.Id
        WHERE m.Name IS NOT NULL
    """).fetchall()
    conn.close()

    result: dict[str, dict[str, str]] = {}
    for wmi, brand, country in rows:
        wmi_key = wmi.strip().upper()
        result[wmi_key] = {"brand": brand.strip(), "country": country.strip()}
    return result


def _extract_era_hints(petrol_csv: Path) -> dict[str, str]:
    """Scan petrol CSV and return {wmi: era_hint} based on B_first_reg_date.

    era_hint = "legacy" if every row for that WMI has reg_year <= ERA_SPLIT_YEAR,
    otherwise "modern".
    """
    wmi_years: dict[str, list[int]] = defaultdict(list)

    with petrol_csv.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            vin = (row.get("E_VIN") or "").strip().upper()
            reg_date = (row.get("B_first_reg_date") or "").strip()
            if len(vin) < 3 or not reg_date:
                continue
            wmi = vin[:3]
            try:
                year = int(reg_date.split(".")[-1])
            except (ValueError, IndexError):
                continue
            wmi_years[wmi].append(year)

    hints: dict[str, str] = {}
    for wmi, years in wmi_years.items():
        hints[wmi] = "legacy" if max(years) <= ERA_SPLIT_YEAR else "modern"
    return hints


def build(wmi_csv_out: Path, vpic_db: Path, petrol_csv: Path) -> int:
    """Build wmi.csv. Returns row count written."""
    import sqlite3

    if not vpic_db.exists():
        from tools.import_vpic import ensure_vpic_db

        vpic_db = ensure_vpic_db()

    vpic_wmis = _load_vpic_wmis(vpic_db)
    era_hints = _extract_era_hints(petrol_csv)

    rows: list[tuple[str, str, str, str]] = []
    seen: set[str] = set()

    # Merge: vPIC is primary for brand/country, CSV adds era_hint
    for wmi, info in sorted(vpic_wmis.items()):
        era = era_hints.get(wmi, "modern")
        rows.append((wmi, info["brand"], info["country"], era))
        seen.add(wmi)

    # Add CSV-only WMIs not in vPIC (e.g., Slovenian-market low-volume makes)
    conn2 = sqlite3.connect(str(vpic_db))
    for wmi, era in sorted(era_hints.items()):
        if wmi not in seen:
            row = conn2.execute(
                "SELECT COALESCE(m.Name,''), COALESCE(c.Name,'') "
                "FROM Wmi w "
                "LEFT JOIN Wmi_Make wm ON w.Id = wm.WmiId "
                "LEFT JOIN Make m ON wm.MakeId = m.Id "
                "LEFT JOIN Country c ON w.CountryId = c.Id "
                "WHERE w.Wmi = ? AND m.Name IS NOT NULL "
                "LIMIT 1",
                (wmi,),
            ).fetchone()
            if row:
                rows.append((wmi, row[0].strip(), row[1].strip(), era))
            else:
                rows.append((wmi, "", "", era))
            seen.add(wmi)
    conn2.close()

    wmi_csv_out.parent.mkdir(parents=True, exist_ok=True)
    with wmi_csv_out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["wmi", "brand", "country", "era_hint"])
        for r in sorted(rows, key=lambda x: x[0]):
            writer.writerow(r)

    return len(rows)


if __name__ == "__main__":
    petrol_arg = DEFAULT_PETROL_CSV
    for i, arg in enumerate(sys.argv[1:], start=1):
        if arg == "--petrol-csv" and i < len(sys.argv) - 1:
            petrol_arg = Path(sys.argv[i + 1])

    try:
        from tools.import_vpic import ensure_vpic_db

        db = ensure_vpic_db()
    except ImportError:
        sys.path.insert(0, str(PROJECT_ROOT))
        from tools.import_vpic import ensure_vpic_db

        db = ensure_vpic_db()

    count = build(DATA_DIR / "wmi.csv", db, petrol_arg)
    print(f"wmi.csv: {count} rows written to {DATA_DIR / 'wmi.csv'}")
