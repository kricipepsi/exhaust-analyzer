"""
tools/tecdoc_engine_enricher.py
Enriches vds_engine_map.csv with TecDoc engine codes for unmatched VDS patterns.

INPUT:  vehicle-data/ktype_bridge_map.csv
        vinlab/data/vds_engine_map.csv  (to skip already-covered keys)
OUTPUT: vinlab/data/vds_engine_map.csv  (new rows appended)

H1 PETROL-ONLY: assert that every output row has fuel_system_type=PORT_INJECTION.
Any row with a diesel engine code is a bug — raise AssertionError, do not write it.
"""

import argparse
import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, cast

import mysql.connector

# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "tecdoc"

ROOT = Path(__file__).resolve().parent.parent
BRIDGE_CSV = ROOT.parent.parent.parent / "vehicle-data" / "ktype_bridge_map.csv"
VDS_MAP_CSV = ROOT / "vinlab" / "data" / "vds_engine_map.csv"

DIESEL_CODES = {
    "sh", "rf", "d4cb", "d4bh", "d4ea", "d4fc", "d4fd",
    "d4fv", "d4bb", "d4bf", "j2", "jtd", "cdi", "tdi",
    "dci", "hdi", "cdti", "crdi", "dth",
}

# WMI → brand key for vds_engine_map.csv output
BRAND_MAP = {
    "JMZ": "Mazda",
    "KNE": "Kia",
    "KLA": "Daewoo",
    "KNA": "Kia",
    "3MZ": "Mazda",
    "3MD": "Mazda",
    "3MV": "Mazda",
    "MDH": "Nissan",
    "KMH": "Hyundai",
    "TMB": "Skoda",
    "TMA": "Hyundai",
    "TM9": "Hyundai",
    "VSS": "Seat",
    "W0L": "Opel",
    "XW8": "Skoda",
    "ZFA": "Mazda",
    "ZFF": "Mazda",
    "Z6F": "Mazda",
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connection_timeout=10,
    )


def load_bridge_map(confidence_filter: str) -> list[dict]:
    """Load ktype_bridge_map.csv, optionally filtered by confidence."""
    rows = []
    if not BRIDGE_CSV.exists():
        print(f"ERROR: {BRIDGE_CSV} not found")
        sys.exit(1)

    with open(BRIDGE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if confidence_filter == "all" or row.get("confidence", "").lower() == confidence_filter:
                rows.append(row)

    return rows


def load_existing_vds_keys() -> set[str]:
    """Return set of vds_full keys already in vds_engine_map.csv."""
    keys: set[str] = set()
    if not VDS_MAP_CSV.exists():
        return keys

    with open(VDS_MAP_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vds = row.get("vds_full", "").strip()
            if vds:
                keys.add(vds.upper())
    return keys


def query_engines(ktype_ids: list[str]) -> dict[str, list[dict]]:
    """Query TecDoc for engine data per KType.

    Returns dict: ktype_id -> list of engine dicts.
    """
    if not ktype_ids:
        return {}

    conn = get_connection()
    cur = conn.cursor()

    placeholders = ",".join(["%s"] * len(ktype_ids))

    sql = f"""
        SELECT
            pce.id          AS ktype_id,
            e.id            AS engine_id,
            e.description   AS engine_code,
            MAX(CASE WHEN ea.attributetype = 'Capacity'
                THEN ea.displayvalue END)          AS capacity_cc,
            MAX(CASE WHEN ea.attributetype = 'NumberOfCylinders'
                THEN ea.displayvalue END)          AS cylinders,
            MAX(CASE WHEN ea.attributetype = 'FuelType'
                THEN ea.displayvalue END)          AS fuel_type
        FROM passanger_car_engines pce
        JOIN engines e ON e.id = pce.engineid
        JOIN engine_attributes ea ON ea.engineid = e.id
        WHERE pce.id IN ({placeholders})
          AND ea.attributetype IN (
              'EngineType', 'Capacity', 'NumberOfCylinders', 'FuelType'
          )
        GROUP BY pce.id, e.id, e.description
        HAVING
            MAX(CASE WHEN ea.attributetype = 'FuelType'
                THEN ea.displayvalue END) IS NOT NULL
            AND (
                MAX(CASE WHEN ea.attributetype = 'FuelType'
                    THEN ea.displayvalue END) = 'бензин'
                OR MAX(CASE WHEN ea.attributetype = 'FuelType'
                    THEN ea.displayvalue END) LIKE '%Бензин%'
                OR MAX(CASE WHEN ea.attributetype = 'FuelType'
                    THEN ea.displayvalue END) LIKE '%бензин%'
            )
            AND MAX(CASE WHEN ea.attributetype = 'FuelType'
                THEN ea.displayvalue END) NOT LIKE '%Дизель%'
        ORDER BY pce.id, e.id
    """

    cur.execute(sql, tuple(ktype_ids))

    results: dict[str, list[dict]] = defaultdict(list)
    for row in cur.fetchall():
        r = cast(tuple[Any, ...], row)
        ktype_id = str(r[0])
        ccm_raw = r[3]
        cyl_raw = r[4]
        try:
            ccm = int(float(str(ccm_raw))) if ccm_raw else None
        except (ValueError, TypeError):
            ccm = None
        try:
            cyl = int(float(str(cyl_raw))) if cyl_raw else None
        except (ValueError, TypeError):
            cyl = None

        # CCM sanity range 600-6000 (M1 petrol engines only)
        if ccm is not None and (ccm < 600 or ccm > 6000):
            ccm = None

        engine = {
            "engine_id": r[1],
            "engine_code": str(r[2]) if r[2] else "",
            "capacity_cc": ccm,
            "cylinders": cyl,
            "fuel_type": str(r[5]) if r[5] else "",
        }
        results[ktype_id].append(engine)

    cur.close()
    conn.close()
    return results


def deduplicate(
    bridge_rows: list[dict],
    ktype_engines: dict[str, list[dict]],
) -> dict[str, dict]:
    """Deduplicate: vds_full -> single engine (most frequent engine_code wins).

    When multiple KTypes share the same vds_full, we merge engine codes across
    them and pick the most frequent.  If only one KType maps to a vds_full,
    pick the engine with the smallest engine_id (most canonical in TecDoc).
    """
    vds_to_engines: dict[str, list[dict]] = defaultdict(list)

    for b_row in bridge_rows:
        vds_full = b_row["vds_full"].strip().upper()
        ktype_id = b_row["ktype_id"].strip()
        engines = ktype_engines.get(ktype_id, [])
        vds_to_engines[vds_full].extend(engines)

    result: dict[str, dict] = {}
    for vds_full, engines in vds_to_engines.items():
        if not engines:
            continue

        freq: dict[str, int] = defaultdict(int)
        best = engines[0]
        for eng in engines:
            code = eng["engine_code"].strip().upper()
            if code:
                freq[code] += 1
        if freq:
            top_code = max(freq, key=lambda k: freq[k])
            for eng in engines:
                if eng["engine_code"].strip().upper() == top_code:
                    best = eng
                    break
        else:
            best = min(engines, key=lambda e: e["engine_id"] if e["engine_id"] is not None else 999999)

        result[vds_full] = best

    return result


def append_to_csv(
    new_rows: list[dict],
    dry_run: bool,
    source_label: str,
) -> int:
    """Append new rows to vds_engine_map.csv. Returns count written."""
    if dry_run:
        print("\n[DRY RUN] Would append the following rows:")
        for row in new_rows:
            print(
                f"  {row['brand']},{row['vds_full']},,"
                f"{row['engine_code']},"
                f"{row['engine_displacement']},"
                f"{row['cylinder_count']},{row['fuel_system_type']}"
            )
        return len(new_rows)

    if not new_rows:
        return 0

    existing = set()
    if VDS_MAP_CSV.exists():
        with open(VDS_MAP_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add(row.get("vds_full", "").strip().upper())

    truly_new = [r for r in new_rows if r["vds_full"].upper() not in existing]

    if not truly_new:
        return 0

    with open(VDS_MAP_CSV, "a", newline="", encoding="utf-8") as f:
        f.write(f"# source: {source_label}\n")
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "brand", "vds_full", "pos_8_only",
                "engine_code", "engine_displacement", "cylinder_count",
                "fuel_system_type",
            ],
            extrasaction="ignore",
        )
        for row in truly_new:
            writer.writerow(row)

    return len(truly_new)


def format_displacement(cc: int | None) -> str:
    """Format displacement in litres, e.g. 1998 -> '2.0'."""
    if cc is None:
        return ""
    litres = cc / 1000.0
    if litres < 1.0:
        return f"{litres:.3f}".rstrip("0").rstrip(".")
    if litres < 10.0:
        return f"{litres:.1f}".rstrip("0").rstrip(".")
    return str(int(litres))


def build_output_row(vds_full: str, engine: dict) -> dict:
    """Build a CSV row dict for vds_engine_map.csv."""
    wmi = vds_full[:3].upper()
    brand = BRAND_MAP.get(wmi, "")

    code = engine.get("engine_code", "").strip()
    if code:
        try:
            code.encode("ascii")
        except UnicodeEncodeError:
            code = ""

    return {
        "brand": brand,
        "vds_full": vds_full.upper(),
        "pos_8_only": "",
        "engine_code": code,
        "engine_displacement": format_displacement(engine.get("capacity_cc")),
        "cylinder_count": str(engine.get("cylinders") or ""),
        "fuel_system_type": "PORT_INJECTION",
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="T-TD-3: TecDoc engine code enrichment")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print proposed rows, do not write to CSV",
    )
    parser.add_argument(
        "--confidence", choices=["all", "high", "medium", "low"],
        default="all",
        help="Filter ktype_bridge_map.csv by confidence level (default: all)",
    )
    args = parser.parse_args()

    today = date.today().isoformat()
    source_label = f"TecDoc {today}"

    # 1. Load input data
    bridge_rows = load_bridge_map(args.confidence)
    existing_keys = load_existing_vds_keys()

    print(f"KType bridge rows loaded:        {len(bridge_rows)}")
    print(f"Existing VDS keys in map:        {len(existing_keys)}")

    # 2. Collect KType IDs (deduplicate)
    ktype_ids = list({r["ktype_id"].strip() for r in bridge_rows if r.get("ktype_id", "").strip()})
    print(f"Unique KType IDs to query:       {len(ktype_ids)}")

    # 3. Query TecDoc
    ktype_engines = query_engines(ktype_ids)

    total_engines_found = sum(len(v) for v in ktype_engines.values())
    print(f"Engine codes found (petrol):     {total_engines_found}")

    # 4. Deduplicate by vds_full
    deduped = deduplicate(bridge_rows, ktype_engines)

    # 5. Build output rows, skip already-covered
    diesel_skipped = 0
    already_in_map = 0
    output_rows: list[dict] = []

    for vds_full, engine in deduped.items():
        if vds_full.upper() in existing_keys:
            already_in_map += 1
            continue

        code = engine.get("engine_code", "").strip().upper()
        if code.lower() in DIESEL_CODES:
            diesel_skipped += 1
            continue

        row = build_output_row(vds_full, engine)
        assert row["fuel_system_type"] == "PORT_INJECTION", (
            f"BUG: non-PORT_INJECTION row {row}"
        )

        # engine code assertion: must be ASCII (no Cyrillic) if present
        if row["engine_code"]:
            try:
                row["engine_code"].encode("ascii")
            except UnicodeEncodeError:
                raise AssertionError(
                    f"Non-ASCII engine code for VDS {vds_full}: {row['engine_code']!r}"
                )

        output_rows.append(row)

    print(f"Already in map (skip):           {already_in_map}")
    print(f"Diesel skipped:                  {diesel_skipped}")

    # 6. Write
    written = append_to_csv(output_rows, args.dry_run, source_label)
    print(f"New rows appended:               {written}")

    # 7. Final assertions
    if not args.dry_run and written > 0:
        with open(VDS_MAP_CSV, newline="", encoding="utf-8") as f:
            all_rows = list(csv.DictReader(f))
        bad = [
            r for r in all_rows
            if r.get("engine_code", "").strip().lower() in DIESEL_CODES
        ]
        assert not bad, f"DIESEL FOUND IN OUTPUT: {bad}"

    print("OK")


if __name__ == "__main__":
    main()
