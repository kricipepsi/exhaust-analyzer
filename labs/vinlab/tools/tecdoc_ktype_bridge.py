"""
tools/tecdoc_ktype_bridge.py
Maps failing VDS patterns to TecDoc KType IDs via three-layer heuristic.
Reads: vehicle-data/tecdoc_schema_map.md (for table/column names)
       vinlab/data/vds_engine_map.csv (to skip already-covered VDS)
       OPSI Nio_vozila_*.csv (to extract brand/ccm/year for unmatched VDS)
Writes: vehicle-data/ktype_bridge_map.csv

H1 PETROL-ONLY: diesel filter applied at SQL layer AND output-writing layer.
"""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path
from typing import Any

import mysql.connector

# -- paths -----------------------------------------------------------
VEHICLE_DATA_ROOT_ENV = os.environ.get("VEHICLE_DATA_ROOT")
if not VEHICLE_DATA_ROOT_ENV:
    raise RuntimeError("VEHICLE_DATA_ROOT environment variable is not set")
OPSI_DIR = Path(VEHICLE_DATA_ROOT_ENV) / "OPSI_podatki_reg._vozilih_30.06.2023"
OPSI_FILES = [
    OPSI_DIR / "Nio_vozila_1.csv",
    OPSI_DIR / "Nio_vozila_2.csv",
    OPSI_DIR / "Nio_vozila_3.csv",
]
VDS_MAP_PATH = Path(__file__).resolve().parent.parent / "data" / "vds_engine_map.csv"
OUTPUT_PATH = Path(VEHICLE_DATA_ROOT_ENV) / "ktype_bridge_map.csv"

# -- MySQL config ----------------------------------------------------
MYSQL_CFG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "tecdoc",
    "charset": "utf8mb4",
    "connection_timeout": 30,
}

# -- Constants -------------------------------------------------------
# source: T-TD-2 task spec — 8 target WMI groups
TARGET_WMIS: frozenset[str] = frozenset({
    "JMZ", "KNE", "KLA", "KNA", "3MZ", "3MD", "3MV", "MDH",
})

# source: T-TD-2 task spec — brand mapping
WMI_TO_BRAND: dict[str, str] = {
    "JMZ": "Mazda",
    "KNE": "Kia",
    "KLA": "Daewoo",
    "KNA": "Kia",
    "3MZ": "Mazda",
    "3MD": "Mazda",
    "3MV": "Mazda",
    "MDH": "Nissan",
}

# source: tecdoc_schema_map.md — TecDoc matchcode per brand
BRAND_TO_MATCHCODE: dict[str, str] = {
    "Mazda": "MAZDA",
    "Kia": "KIA",
    "Daewoo": "DAEWOO",
    "Nissan": "NISSA",
    "Hyundai": "HYUNDAI",
}

# source: T-FX-6 task spec + H1 hard constraint — diesel engine codes
DIESEL_CODES: frozenset[str] = frozenset({
    "sh", "rf", "d4cb", "d4bh", "d4ea", "d4fc", "d4fd", "d4fv",
    "j2", "jtd", "cdi", "tdi", "dci", "hdi", "cdti", "dth",
    "d4bb", "d4bf", "crdi",
})

# source: tecdoc_schema_map.md — petrol fuel type values (Russian)
PETROL_FUEL_VALUES: frozenset[str] = frozenset({
    "бензин",
    "Бензин/спирт",
    "Бензин/газ",
    "Супер-бензин (95) неэтилированный",
    "Super (98) этилированный",
    "нормальный бензин (91) неэтилированный",
})

# source: T-TD-2 task spec — displacement windows
LAYER_2_WINDOW = 75   # cc
LAYER_3_WINDOW = 150  # cc

OUTPUT_COLUMNS = [
    "brand", "vds_full", "ktype_id", "tecdoc_engine_id",
    "tecdoc_engine_code", "eng_ccm", "cylinder_count",
    "match_layer", "confidence",
]


# ===================================================================
# OPSI extraction
# ===================================================================

def load_covered_vds() -> set[tuple[str, str]]:
    """Load (brand, vds_full) already in vds_engine_map.csv."""
    covered: set[tuple[str, str]] = set()
    if not VDS_MAP_PATH.exists():
        return covered
    with VDS_MAP_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            covered.add((row["brand"].strip(), row["vds_full"].strip()))
    return covered


def extract_uncovered() -> list[dict[str, Any]]:
    """Extract petrol M1 VDS patterns from OPSI for target WMIs,
    skipping already-covered ones. Returns list of unique patterns."""
    covered = load_covered_vds()
    # (brand, vds_full) -> {engine_code, disp}
    patterns: dict[tuple[str, str], dict[str, Any]] = {}

    for fpath in OPSI_FILES:
        if not fpath.exists():
            print(f"WARNING: OPSI file not found: {fpath}", file=sys.stderr)
            continue
        with fpath.open(encoding="utf-8", errors="replace", newline="") as fh:
            reader = csv.reader(fh, delimiter=";", quotechar='"')
            next(reader, None)
            for row in reader:
                if len(row) < 57:
                    continue
                vin = row[26].strip()
                if len(vin) != 17:
                    continue
                wmi = vin[:3]
                if wmi not in TARGET_WMIS:
                    continue
                # H2: M1 only
                kat = row[32].strip() if len(row) > 32 else ""
                kat_opis = row[33].strip() if len(row) > 33 else ""
                if kat != "M1" and "osebni" not in kat_opis.lower():
                    continue
                # H1: petrol only
                fuel_code = row[49].strip() if len(row) > 49 else ""
                if fuel_code != "P":
                    continue

                brand = WMI_TO_BRAND[wmi]
                vds_full = vin[3:8]
                key = (brand, vds_full)
                if key in covered:
                    continue

                engine_code = row[51].strip() if len(row) > 51 else ""
                if engine_code and engine_code.lower() in DIESEL_CODES:
                    continue

                disp_str = row[46].strip() if len(row) > 46 else ""
                try:
                    disp = int(disp_str) if disp_str else 0
                except ValueError:
                    disp = 0

                if key not in patterns:
                    patterns[key] = {
                        "brand": brand,
                        "vds_full": vds_full,
                        "engine_code_hint": engine_code.upper() if engine_code else "",
                        "displacement_cc": disp,
                        "opsi_count": 0,
                    }
                entry = patterns[key]
                entry["opsi_count"] += 1
                # Keep strongest hint
                if engine_code and not entry["engine_code_hint"]:
                    entry["engine_code_hint"] = engine_code.upper()
                if disp > 0 and entry["displacement_cc"] == 0:
                    entry["displacement_cc"] = disp

    return sorted(patterns.values(), key=lambda x: (x["brand"], x["vds_full"]))


# ===================================================================
# TecDoc query layer
# ===================================================================

def _connect():
    return mysql.connector.connect(**MYSQL_CFG)


def _petrol_clause(table_alias: str = "ea_fuel") -> str:
    """SQL clause to filter petrol-only engines."""
    values = ", ".join(f"'{v}'" for v in PETROL_FUEL_VALUES)
    return f"{table_alias}.displayvalue IN ({values})"


def _year_clause(table_alias: str = "pc") -> str:
    """H2: year scope 1990-2020 filter on constructioninterval.
    Format: 'MM.YYYY - MM.YYYY' or 'MM.YYYY - ' (open-ended)."""
    return (
        f"CAST(SUBSTRING_INDEX({table_alias}.constructioninterval, '.', -1) "
        f"AS UNSIGNED) <= 2020 "
        f"AND ("
        f"  {table_alias}.constructioninterval LIKE '%- %' "
        f"  AND SUBSTRING_INDEX(SUBSTRING_INDEX("
        f"    {table_alias}.constructioninterval, ' - ', -1), '.', -1"
        f"  ) = '' "
        f"  OR CAST(SUBSTRING_INDEX(SUBSTRING_INDEX("
        f"    {table_alias}.constructioninterval, ' - ', -1), '.', -1"
        f"  ) AS UNSIGNED) >= 1990"
        f")"
    )


def _displacement_clause(ccm: int, window: int) -> str:
    """Displacement range filter."""
    lo = max(0, ccm - window)
    hi = ccm + window
    return (
        f"CAST(REPLACE(ea_cap.displayvalue, ' ccm', '') AS UNSIGNED) "
        f"BETWEEN {lo} AND {hi}"
    )


def _build_layer_query(
    brand: str,
    displacement_cc: int,
    window: int,
    engine_code_hint: str = "",
) -> str:
    """Build the combined SQL query for Layer 1/2/3.
    Layer 1: adds engine code normalization filter.
    Layers 2/3: brand + displacement + year + petrol."""
    matchcode = BRAND_TO_MATCHCODE.get(brand, brand.upper())

    base = f"""
SELECT DISTINCT
    pc.id AS ktype_id,
    e.id AS tecdoc_engine_id,
    e.description AS tecdoc_engine_code,
    CAST(REPLACE(ea_cap.displayvalue, ' ccm', '') AS UNSIGNED) AS eng_ccm
FROM passanger_cars pc
JOIN models md ON pc.modelid = md.id
JOIN manufacturers m ON md.manufacturerid = m.id
    AND m.ispassengercar = 'True'
JOIN passanger_car_engines pce ON pc.id = pce.id
JOIN engines e ON pce.engineid = e.id
JOIN engine_attributes ea_cap ON e.id = ea_cap.engineid
    AND ea_cap.attributetype = 'Capacity'
JOIN engine_attributes ea_fuel ON e.id = ea_fuel.engineid
    AND ea_fuel.attributetype = 'FuelType'
WHERE m.matchcode = '{matchcode}'
  AND {_petrol_clause()}
  AND {_year_clause()}
  AND {_displacement_clause(displacement_cc, window)}
"""

    if engine_code_hint:
        base += (
            f"  AND UPPER(REPLACE(e.description, ' ', '')) = "
            f"UPPER(REPLACE('{engine_code_hint}', ' ', ''))\n"
        )

    base += "LIMIT 10;"
    return base


def _to_int(value: object) -> int:
    """Cast mysql-connector row value (int/Decimal/str) to int."""
    return int(str(value))


def _get_cylinder_count(engine_id: int, cursor) -> int:
    """Query cylinder count from engine_attributes."""
    cursor.execute(
        "SELECT displayvalue FROM engine_attributes "
        "WHERE engineid = %s AND attributetype = 'NumberOfCylinders'",
        (engine_id,),
    )
    row = cursor.fetchone()
    if row:
        try:
            return int(row[0])
        except (ValueError, TypeError):
            pass
    return 0


def query_tecadoc(
    brand: str,
    vds_full: str,
    displacement_cc: int,
    engine_code_hint: str = "",
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    """Run the three-layer matching strategy for a single VDS pattern.
    Returns list of match rows (empty if no matches)."""
    results: list[dict[str, Any]] = []

    if dry_run:
        print(f"\nDRY-RUN: {brand}/{vds_full} "
              f"disp={displacement_cc} hint='{engine_code_hint}'")

    conn = None
    try:
        conn = _connect()
        cursor = conn.cursor()

        # Layer 1: direct engine code match (only if hint available)
        if engine_code_hint:
            sql = _build_layer_query(
                brand, displacement_cc, LAYER_2_WINDOW, engine_code_hint
            )
            if dry_run:
                print(f"  Layer 1 SQL: {sql[:200]}...")
            else:
                cursor.execute(sql)
                for ktype_id, eng_id, eng_code, eng_ccm in cursor.fetchall():
                    cyl = _get_cylinder_count(_to_int(eng_id), cursor)
                    results.append({
                        "brand": brand, "vds_full": vds_full,
                        "ktype_id": str(ktype_id),
                        "tecdoc_engine_id": str(eng_id),
                        "tecdoc_engine_code": eng_code or "",
                        "eng_ccm": str(eng_ccm),
                        "cylinder_count": str(cyl),
                        "match_layer": "1",
                        "confidence": "high",
                    })

        # Layer 2: brand + displacement ±75cc + year + petrol
        if not results:
            sql = _build_layer_query(brand, displacement_cc, LAYER_2_WINDOW)
            if dry_run:
                print(f"  Layer 2 SQL: {sql[:200]}...")
            else:
                cursor.execute(sql)
                for ktype_id, eng_id, eng_code, eng_ccm in cursor.fetchall():
                    cyl = _get_cylinder_count(_to_int(eng_id), cursor)
                    results.append({
                        "brand": brand, "vds_full": vds_full,
                        "ktype_id": str(ktype_id),
                        "tecdoc_engine_id": str(eng_id),
                        "tecdoc_engine_code": eng_code or "",
                        "eng_ccm": str(eng_ccm),
                        "cylinder_count": str(cyl),
                        "match_layer": "2",
                        "confidence": "medium",
                    })

        # Layer 3: widened displacement ±150cc
        if not results:
            sql = _build_layer_query(brand, displacement_cc, LAYER_3_WINDOW)
            if dry_run:
                print(f"  Layer 3 SQL: {sql[:200]}...")
            else:
                cursor.execute(sql)
                for ktype_id, eng_id, eng_code, eng_ccm in cursor.fetchall():
                    cyl = _get_cylinder_count(_to_int(eng_id), cursor)
                    results.append({
                        "brand": brand, "vds_full": vds_full,
                        "ktype_id": str(ktype_id),
                        "tecdoc_engine_id": str(eng_id),
                        "tecdoc_engine_code": eng_code or "",
                        "eng_ccm": str(eng_ccm),
                        "cylinder_count": str(cyl),
                        "match_layer": "3",
                        "confidence": "low",
                    })

        cursor.close()
    except Exception as exc:
        print(f"ERROR querying TecDoc for {brand}/{vds_full}: {exc}",
              file=sys.stderr)
    finally:
        if conn:
            conn.close()

    return results


# ===================================================================
# Diesel guard
# ===================================================================

def assert_no_diesel(rows: list[dict[str, Any]]) -> None:
    """H1 guard: raise if any output row contains a diesel engine code."""
    diesel_in_output = [
        r for r in rows
        if r.get("tecdoc_engine_code", "").lower() in DIESEL_CODES
    ]
    if diesel_in_output:
        raise AssertionError(
            f"H1 VIOLATION: diesel engine codes in output: {diesel_in_output}"
        )


# ===================================================================
# Main
# ===================================================================

def main() -> None:
    dry_run = "--dry-run" in sys.argv

    # 1. Extract uncovered VDS patterns from OPSI
    print("=== Extracting uncovered VDS patterns from OPSI ===", file=sys.stderr)
    patterns = extract_uncovered()
    print(f"VDS patterns to process: {len(patterns)}", file=sys.stderr)
    if patterns:
        for p in patterns[:10]:
            print(
                f"  {p['brand']:8s} {p['vds_full']:5s} "
                f"disp={p['displacement_cc']:5d} "
                f"hint='{p['engine_code_hint']}' "
                f"(n={p['opsi_count']})",
                file=sys.stderr,
            )

    # 2. Run three-layer matching
    all_rows: list[dict[str, Any]] = []
    stats = {"layer1": 0, "layer2": 0, "layer3": 0, "unmatched": 0, "diesel_skipped": 0}

    for i, pat in enumerate(patterns):
        rows = query_tecadoc(
            brand=pat["brand"],
            vds_full=pat["vds_full"],
            displacement_cc=pat["displacement_cc"],
            engine_code_hint=pat["engine_code_hint"],
            dry_run=dry_run,
        )
        if rows:
            all_rows.extend(rows)
            layers = {r["match_layer"] for r in rows}
            for layer in layers:
                stats[f"layer{layer}"] += 1
        elif not dry_run:
            stats["unmatched"] += 1

    # 3. Diesel guard
    if all_rows:
        assert_no_diesel(all_rows)

    # 4. Write output (skip if dry-run)
    if not dry_run:
        with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=OUTPUT_COLUMNS,
                                    lineterminator="\n")
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
        print(f"\nWrote {len(all_rows)} rows to {OUTPUT_PATH}", file=sys.stderr)
    else:
        print(f"\nDRY-RUN complete — would write {len(all_rows)} rows "
              f"to {OUTPUT_PATH}", file=sys.stderr)

    # 5. Summary
    print(file=sys.stderr)
    print(f"VDS patterns attempted:  {len(patterns)}", file=sys.stderr)
    print(f"Layer-1 matches:         {stats['layer1']}", file=sys.stderr)
    print(f"Layer-2 matches:         {stats['layer2']}", file=sys.stderr)
    print(f"Layer-3 matches:         {stats['layer3']} (low confidence)", file=sys.stderr)
    print(f"Unmatched:               {stats['unmatched']}", file=sys.stderr)
    print(f"Diesel rows skipped:     {stats['diesel_skipped']}", file=sys.stderr)
    print(f"Output rows written:     {len(all_rows)}", file=sys.stderr)


if __name__ == "__main__":
    main()
