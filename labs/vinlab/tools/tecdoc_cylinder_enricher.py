"""
tools/tecdoc_cylinder_enricher.py

Queries TecDoc MySQL for cylinder_count by engine code and updates
vinlab/data/vds_engine_map.csv in-place.

INPUT:  vinlab/data/vds_engine_map.csv  (read all rows)
OUTPUT: vinlab/data/vds_engine_map.csv  (cylinder_count column updated
                                         for rows where it was 0 or empty)

MySQL: host=127.0.0.1, port=3306, user=root, password='', database=tecdoc
       Connect via mysql.connector (already in requirements.txt).

H1 PETROL-ONLY: every SQL query includes the fuel type filter.
H4 READ-ONLY MySQL: SELECT only.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

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
VDS_MAP_CSV = ROOT / "vinlab" / "data" / "vds_engine_map.csv"
KTYPE_BRIDGE_CSV = ROOT.parent.parent.parent / "vehicle-data" / "ktype_bridge_map.csv"

DIESEL_CODES = {
    "sh", "rf", "d4cb", "d4bh", "d4ea", "d4fc", "d4fd",
    "d4fv", "d4bb", "d4bf", "cdi", "tdi",
    "dci", "hdi", "cdti", "crdi",
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


def query_cylinder_by_engine_code(engine_codes: list[str]) -> dict[str, int | None]:
    """Direct engine code lookup: engine_code -> cylinder_count.

    For each engine code, finds the most frequent NumberOfCylinders value
    from TecDoc, filtered to petrol engines only (H1).
    Returns None for codes with no match.
    """
    if not engine_codes:
        return {}

    conn = get_connection()
    cur = conn.cursor()

    results: dict[str, int | None] = dict.fromkeys(engine_codes)

    for code in engine_codes:
        sql = """
            SELECT ea_cyl.displayvalue, COUNT(*) as cnt
            FROM engines e
            JOIN engine_attributes ea_cyl
                ON ea_cyl.engineid = e.id
                AND ea_cyl.attributetype = 'NumberOfCylinders'
            JOIN engine_attributes ea_fuel
                ON ea_fuel.engineid = e.id
                AND ea_fuel.attributetype = 'FuelType'
            WHERE UPPER(TRIM(e.description)) = UPPER(TRIM(%s))
              AND CAST(ea_cyl.displayvalue AS UNSIGNED) BETWEEN 2 AND 16
              AND (ea_fuel.displayvalue = 'бензин'
                   OR ea_fuel.displayvalue LIKE '%Бензин%'
                   OR ea_fuel.displayvalue LIKE '%бензин%')
              AND ea_fuel.displayvalue NOT LIKE '%Дизель%'
            GROUP BY ea_cyl.displayvalue
            ORDER BY cnt DESC
            LIMIT 1
        """
        cur.execute(sql, (code,))
        row = cur.fetchone()
        if row:
            try:
                cyl = int(float(str(row[0])))  # type: ignore[arg-type]
                if 2 <= cyl <= 16:
                    results[code] = cyl
            except (ValueError, TypeError):
                pass

    cur.close()
    conn.close()
    return results


def query_cylinder_by_displacement(
    rows: list[dict],
) -> dict[str, int | None]:
    """Fallback: match by engine displacement when engine code lookup fails.

    For each row with a displacement value but no matching engine code,
    queries the most common cylinder count for petrol engines in that cc range.
    Range is +/- 15% of the displacement value (e.g. 1.4L covers 1190-1610cc).
    """
    conn = get_connection()
    cur = conn.cursor()

    results: dict[str, int | None] = {}

    for r in rows:
        code = r.get("engine_code", "").strip().upper()
        if not code or code in results:
            continue

        disp_str = r.get("engine_displacement", "").strip()
        if not disp_str:
            continue

        try:
            disp_l = float(disp_str)
        except (ValueError, TypeError):
            continue

        if disp_l <= 0:
            continue

        disp_cc = disp_l * 1000.0
        cc_low = int(disp_cc * 0.85)
        cc_high = int(disp_cc * 1.15)

        cur.execute(
            """
            SELECT ea_cyl.displayvalue, COUNT(*) as cnt
            FROM engines e
            JOIN engine_attributes ea_ccm
                ON ea_ccm.engineid = e.id
                AND ea_ccm.attributetype = 'Capacity'
            JOIN engine_attributes ea_cyl
                ON ea_cyl.engineid = e.id
                AND ea_cyl.attributetype = 'NumberOfCylinders'
            JOIN engine_attributes ea_fuel
                ON ea_fuel.engineid = e.id
                AND ea_fuel.attributetype = 'FuelType'
            WHERE CAST(ea_ccm.displayvalue AS UNSIGNED) BETWEEN %s AND %s
              AND CAST(ea_cyl.displayvalue AS UNSIGNED) BETWEEN 2 AND 16
              AND (ea_fuel.displayvalue = 'бензин'
                   OR ea_fuel.displayvalue LIKE '%Бензин%'
                   OR ea_fuel.displayvalue LIKE '%бензин%')
              AND ea_fuel.displayvalue NOT LIKE '%Дизель%'
            GROUP BY ea_cyl.displayvalue
            ORDER BY cnt DESC
            LIMIT 1
            """,
            (cc_low, cc_high),
        )
        row = cur.fetchone()
        if row:
            try:
                cyl = int(float(str(row[0])))  # type: ignore[arg-type]
                if 2 <= cyl <= 16:
                    results[code] = cyl
            except (ValueError, TypeError):
                pass

    cur.close()
    conn.close()
    return results


def query_cylinder_by_ktype(ktype_ids: list[str]) -> dict[str, int | None]:
    """Fallback: KType ID -> most-frequent petrol cylinder count.

    Queries via passanger_car_engines -> engines -> engine_attributes.
    Returns ktype_id -> cylinder_count mapping.
    """
    if not ktype_ids:
        return {}

    conn = get_connection()
    cur = conn.cursor()

    placeholders = ",".join(["%s"] * len(ktype_ids))

    sql = f"""
        SELECT
            pce.id AS ktype_id,
            ea.displayvalue,
            COUNT(*) AS cnt
        FROM passanger_car_engines pce
        JOIN engines e ON e.id = pce.engineid
        JOIN engine_attributes ea
            ON ea.engineid = e.id
            AND ea.attributetype = 'NumberOfCylinders'
        JOIN engine_attributes ea_fuel
            ON ea_fuel.engineid = e.id
            AND ea_fuel.attributetype = 'FuelType'
        WHERE pce.id IN ({placeholders})
          AND CAST(ea.displayvalue AS UNSIGNED) BETWEEN 2 AND 16
          AND (ea_fuel.displayvalue = 'бензин'
               OR ea_fuel.displayvalue LIKE '%Бензин%'
               OR ea_fuel.displayvalue LIKE '%бензин%')
          AND ea_fuel.displayvalue NOT LIKE '%Дизель%'
        GROUP BY pce.id, ea.displayvalue
        ORDER BY pce.id, cnt DESC
    """

    cur.execute(sql, tuple(ktype_ids))

    raw: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for row in cur.fetchall():
        ktype_id, displayvalue, cnt_raw = row[0], row[1], row[2]  # type: ignore[index]
        cnt = int(cnt_raw)  # type: ignore[arg-type]
        try:
            cyl = int(float(str(displayvalue)))
            if 2 <= cyl <= 16:
                raw[str(ktype_id)].append((cyl, cnt))
        except (ValueError, TypeError):
            pass

    cur.close()
    conn.close()

    results: dict[str, int | None] = {}
    for ktype_id, entries in raw.items():
        entries.sort(key=lambda x: x[1], reverse=True)
        results[ktype_id] = entries[0][0]

    return results


def load_ktype_bridge() -> dict[str, list[str]]:
    """Load ktype_bridge_map.csv: engine_code -> list of ktype_ids."""
    mapping: dict[str, list[str]] = defaultdict(list)
    if not KTYPE_BRIDGE_CSV.exists():
        return mapping

    with KTYPE_BRIDGE_CSV.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            code = row.get("engine_code", "").strip().upper()
            ktype = row.get("ktype_id", "").strip()
            if code and ktype:
                mapping[code].append(ktype)

    return mapping


def is_diesel_code(engine_code: str) -> bool:
    """Check if engine_code matches known diesel patterns (H1 guard)."""
    code_lower = engine_code.strip().lower()
    if code_lower in DIESEL_CODES:
        return True
    for dc in DIESEL_CODES:
        if dc in code_lower:
            return True
    return False


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="T-CSV-2: Fill cylinder_count in vds_engine_map.csv from TecDoc"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be written, modify nothing",
    )
    args = parser.parse_args()

    if not VDS_MAP_CSV.exists():
        print(f"ERROR: {VDS_MAP_CSV} not found")
        sys.exit(1)

    # 1. Read original CSV
    with VDS_MAP_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            print("ERROR: CSV has no header")
            sys.exit(1)
        all_rows = list(reader)

    original_header = list(fieldnames)
    print(f"Rows loaded:                     {len(all_rows)}")

    # 2. Identify rows needing enrichment
    needs_fill: list[int] = []  # indices into all_rows
    skip_already = 0
    skip_no_code = 0
    skip_diesel = 0
    codes_to_query: set[str] = set()

    for i, row in enumerate(all_rows):
        cyl_raw = row.get("cylinder_count", "").strip()
        if cyl_raw and cyl_raw != "0":
            skip_already += 1
            continue

        engine_code = row.get("engine_code", "").strip()
        if not engine_code:
            skip_no_code += 1
            continue

        if is_diesel_code(engine_code):
            skip_diesel += 1
            continue

        needs_fill.append(i)
        codes_to_query.add(engine_code.upper())

    print(f"Already have cylinder_count:     {skip_already}")
    print(f"No engine_code (skip):           {skip_no_code}")
    print(f"Diesel code (skip):              {skip_diesel}")
    print(f"Unique engine codes to query:    {len(codes_to_query)}")
    print(f"Rows needing enrichment:         {len(needs_fill)}")

    if not needs_fill:
        print("Nothing to do.")
        return

    # 3. Direct engine code lookup
    code_list = sorted(codes_to_query)
    direct_results = query_cylinder_by_engine_code(code_list)

    resolved_direct = sum(1 for v in direct_results.values() if v is not None)
    print(f"Resolved via TecDoc (direct):    {resolved_direct}")

    # 4. Displacement fallback for unresolved codes
    unresolved_after_direct = [c for c in code_list if direct_results.get(c) is None]
    disp_results: dict[str, int | None] = {}

    if unresolved_after_direct:
        # Collect rows with unresolved codes that have displacement values
        rows_to_resolve = [
            all_rows[i] for i in needs_fill
            if all_rows[i].get("engine_code", "").strip().upper() in unresolved_after_direct
        ]
        disp_results = query_cylinder_by_displacement(rows_to_resolve)
        resolved_disp = sum(1 for v in disp_results.values() if v is not None)
        print(f"Resolved via displacement:       {resolved_disp}")
    else:
        print("Resolved via displacement:       0")

    # 5. KType fallback for codes still unresolved
    unresolved_after_disp = [
        c for c in unresolved_after_direct
        if disp_results.get(c) is None
    ]
    ktype_results: dict[str, int | None] = {}

    if unresolved_after_disp:
        bridge = load_ktype_bridge()
        print(f"KType bridge entries loaded:     {len(bridge)}")

        ktype_ids_to_query: set[str] = set()
        code_to_ktypes: dict[str, list[str]] = {}
        for code in unresolved_after_disp:
            ktypes = bridge.get(code, [])
            if ktypes:
                code_to_ktypes[code] = ktypes
                ktype_ids_to_query.update(ktypes)

        if ktype_ids_to_query:
            print(f"KType IDs to query (fallback):   {len(ktype_ids_to_query)}")
            ktype_cyl = query_cylinder_by_ktype(list(ktype_ids_to_query))

            for code, ktypes in code_to_ktypes.items():
                cyl_values = [ktype_cyl.get(k, None) for k in ktypes]
                cyl_values = [v for v in cyl_values if v is not None]
                if cyl_values:
                    ktype_results[code] = max(set(cyl_values), key=cyl_values.count)

        resolved_ktype = sum(1 for v in ktype_results.values() if v is not None)
        print(f"Resolved via KType fallback:     {resolved_ktype}")
    else:
        print("Resolved via KType fallback:     0")

    # 6. Apply updates
    resolved_all = {**direct_results, **disp_results, **ktype_results}
    updated = 0
    unresolved = 0

    for idx in needs_fill:
        code = all_rows[idx].get("engine_code", "").strip().upper()
        cyl = resolved_all.get(code)
        if cyl is not None:
            all_rows[idx]["cylinder_count"] = str(cyl)
            updated += 1
        else:
            unresolved += 1

    print(f"Rows updated:                    {updated}")
    print(f"Unresolved (left empty):         {unresolved}")

    # 6. Write CSV (preserve exact header order)
    if args.dry_run:
        print("\n[DRY RUN] Would update the following rows:")
        count = 0
        for idx in needs_fill:
            if all_rows[idx].get("cylinder_count", "").strip() not in ("", "0"):
                r = all_rows[idx]
                brand = r.get("brand", "")[:15]
                code = r.get("engine_code", "")[:15]
                cyl = r.get("cylinder_count", "")
                try:
                    print(f"  {brand:15} code={code:15} cyl={cyl}")
                except UnicodeEncodeError:
                    print(f"  {'(brand)':15} code={code:15} cyl={cyl}")
                count += 1
                if count >= 50:
                    print(f"  ... and {updated - 50} more")
                    break
        print(f"[DRY RUN] Would update {updated} rows.")
        return

    if updated == 0:
        print("No rows to write.")
        return

    with VDS_MAP_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=original_header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"vds_engine_map.csv written:      {len(all_rows)} rows")

    # 7. Validation assertions
    with VDS_MAP_CSV.open("r", encoding="utf-8", newline="") as f:
        verify_rows = list(csv.DictReader(f))

    # Assert header identical
    assert list(verify_rows[0].keys()) == original_header, (
        "Header changed — column added/removed"
    )

    # Assert all updated rows have cylinder_count in valid range
    updated_indices = set(needs_fill)
    bad_range = []
    for i, r in enumerate(verify_rows):
        if i not in updated_indices:
            continue
        cyl_raw = r.get("cylinder_count", "").strip()
        if not cyl_raw or cyl_raw == "0":
            continue
        try:
            cyl = int(cyl_raw)
            if not (2 <= cyl <= 16):
                bad_range.append((r.get("brand", ""), r.get("engine_code", ""), cyl))
        except ValueError:
            bad_range.append((r.get("brand", ""), r.get("engine_code", ""), cyl_raw))

    assert not bad_range, f"Out-of-range cylinder_count: {bad_range[:5]}"

    filled_count = sum(
        1 for r in verify_rows
        if r.get("cylinder_count", "").strip() not in ("", "0")
    )
    print(f"Range check PASS                 ({filled_count} rows with cylinder_count)")

    # Assert no diesel codes escaped
    diesel_rows = [
        r for r in verify_rows
        if r.get("cylinder_count", "").strip() not in ("", "0")
        and is_diesel_code(r.get("engine_code", "").strip())
    ]
    assert not diesel_rows, f"Diesel codes with cylinder_count: {diesel_rows[:3]}"

    print("Diesel guard PASS")
    print("OK")


if __name__ == "__main__":
    main()
