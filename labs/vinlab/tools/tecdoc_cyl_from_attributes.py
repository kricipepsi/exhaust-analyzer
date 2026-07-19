"""
tools/tecdoc_cyl_from_attributes.py

Queries TecDoc MySQL engine_attributes for 'NumberOfCylinders' per engine
code and updates vinlab/data/vds_engine_map.csv in-place.

Source of truth for the attribute structure:
  vehicle-data/1Q2019/install_database/db.sql
  (items_atributes table — direct equivalent of engine_attributes in MySQL)

MySQL: host=127.0.0.1 port=3306 user=root password='' database=tecdoc
       See mysql_bridge.py for the connection pattern.

H1 PETROL-ONLY: fuel filter applied at SQL layer.
H4 READ-ONLY: SELECT only.
"""

from __future__ import annotations

import argparse
import csv
import sys
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

DIESEL_CODES: frozenset[str] = frozenset({
    "sh", "rf", "d4cb", "d4bh", "d4ea", "d4fc", "d4fd",
    "d4fv", "d4bb", "d4bf", "cdi", "tdi",
    "dci", "hdi", "cdti", "crdi",
})


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


def is_diesel_code(engine_code: str) -> bool:
    code_lower = engine_code.strip().lower()
    if code_lower in DIESEL_CODES:
        return True
    for dc in DIESEL_CODES:
        if dc in code_lower:
            return True
    return False


def normalize_code(code: str) -> str:
    """Strip formatting characters for cross-reference matching.

    TecDoc stores engine codes with spaces, dots, dashes, and slashes
    (e.g. '021 C.1000', 'M 111.940') while vds_engine_map.csv stores them
    without (e.g. '021C1000', '111.940').  Normalising both sides to a
    compact form catches these format variants.
    """
    return (
        code.strip().upper()
        .replace(" ", "")
        .replace(".", "")
        .replace("-", "")
        .replace("/", "")
    )


def build_cylinder_lookup() -> tuple[dict[str, int], dict[str, int]]:
    """Single bulk query: all petrol engine codes -> cylinder_count.

    Returns two dicts:
      exact  — original TecDoc description -> cylinder_count
      norm   — normalized description -> cylinder_count (for flexible matching)

    Dedup rule: highest cnt wins; tied counts -> lower cylinder number.
    If two different TecDoc codes normalize to the same key, the one with
    the higher count wins.
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT
            e.description AS engine_code,
            ea_cyl.displayvalue AS cylinder_count,
            COUNT(*) AS cnt
        FROM engines e
        JOIN engine_attributes ea_cyl
            ON ea_cyl.engineid = e.id
            AND ea_cyl.attributetype = 'NumberOfCylinders'
            AND ea_cyl.displayvalue IN ('2','3','4','5','6','8','10','12','16')
        JOIN engine_attributes ea_fuel
            ON ea_fuel.engineid = e.id
            AND ea_fuel.attributetype = 'FuelType'
            AND (ea_fuel.displayvalue = 'бензин'
                 OR ea_fuel.displayvalue LIKE '%Бензин%'
                 OR ea_fuel.displayvalue LIKE '%бензин%')
            AND ea_fuel.displayvalue NOT LIKE '%Дизель%'
        WHERE e.description != ''
          AND e.description IS NOT NULL
        GROUP BY e.description, ea_cyl.displayvalue
        ORDER BY e.description, cnt DESC
    """

    cur.execute(sql)
    raw_exact: dict[str, list[tuple[int, int]]] = {}
    for row in cur.fetchall():
        code = str(row[0]).strip().upper()  # type: ignore[arg-type]
        cyl = int(float(str(row[1])))  # type: ignore[arg-type]
        cnt = int(str(row[2]))  # type: ignore[arg-type]
        if code not in raw_exact:
            raw_exact[code] = []
        raw_exact[code].append((cyl, cnt))

    cur.close()
    conn.close()

    exact: dict[str, int] = {}
    norm: dict[str, int] = {}
    for code, entries in raw_exact.items():
        entries.sort(key=lambda x: (-x[1], x[0]))
        best = entries[0][0]
        exact[code] = best
        ncode = normalize_code(code)
        if ncode not in norm or best != norm.get(ncode):
            norm[ncode] = best

    return exact, norm


def build_suffix_lookup(
    norm_lookup: dict[str, int],
    candidates: set[str],
) -> dict[str, int]:
    """Match CSV codes that appear as a suffix of a TecDoc normalized code.

    Handles cases like '112.947' (CSV) vs 'M 112.947' (TecDoc), where the
    CSV drops a manufacturer prefix.  Only considers candidate codes of
    length >= 5 (after normalization) to avoid spurious short-code matches.
    """
    if not candidates:
        return {}

    suffix: dict[str, list[tuple[str, int]]] = {}
    for n_code in candidates:
        n = normalize_code(n_code)
        if len(n) >= 5:
            suffix[n] = []

    for td_norm, cyl in norm_lookup.items():
        for cand_norm in list(suffix.keys()):
            if td_norm.endswith(cand_norm):
                suffix[cand_norm].append((td_norm, cyl))

    result: dict[str, int] = {}
    for cand_norm, matches in suffix.items():
        if not matches:
            continue
        # Take the match whose normalized TecDoc code is shortest
        # (most specific — e.g. 'M 112.947' is better than 'OM 112.947')
        matches.sort(key=lambda x: (len(x[0]), -x[1]))
        result[cand_norm] = matches[0][1]

    return result


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="T-CSV-3: Fill cylinder_count in vds_engine_map.csv from TecDoc engine_attributes"
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
    original_row_count = len(all_rows)
    print(f"Rows loaded:                     {original_row_count}")

    # 2. Identify rows needing enrichment
    needs_fill: list[int] = []
    skip_already = 0
    skip_no_code = 0
    skip_diesel = 0

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

    print(f"Already have cylinder_count:     {skip_already}")
    print(f"No engine_code (skip):           {skip_no_code}")
    print(f"Diesel code (skip):              {skip_diesel}")
    print(f"Rows needing enrichment:         {len(needs_fill)}")

    if not needs_fill:
        print("Nothing to do.")
        return

    # 3. Query MySQL — single bulk pass
    print("Querying TecDoc engine_attributes (single pass)...")
    code_to_cyl_exact, code_to_cyl_norm = build_cylinder_lookup()
    total_pairs = len(code_to_cyl_exact)
    print(f"TecDoc engine_code->cyl pairs loaded:  {total_pairs}")

    # 4. Apply results — try exact → normalized → suffix
    filled = 0
    filled_norm = 0
    filled_suffix = 0
    not_found: list[str] = []
    suffix_candidates: set[str] = set()

    for idx in needs_fill:
        code = all_rows[idx].get("engine_code", "").strip().upper()
        cyl = code_to_cyl_exact.get(code)
        if cyl is not None:
            all_rows[idx]["cylinder_count"] = str(cyl)
            filled += 1
            continue
        cyl = code_to_cyl_norm.get(normalize_code(code))
        if cyl is not None:
            all_rows[idx]["cylinder_count"] = str(cyl)
            filled += 1
            filled_norm += 1
            continue
        # Defer to suffix pass
        suffix_candidates.add(code)

    # 4b. Suffix lookup for remaining codes
    suffix_lookup: dict[str, int] = {}
    if suffix_candidates:
        suffix_lookup = build_suffix_lookup(code_to_cyl_norm, suffix_candidates)
        for idx in needs_fill:
            code = all_rows[idx].get("engine_code", "").strip().upper()
            if all_rows[idx].get("cylinder_count", "").strip() not in ("", "0"):
                continue  # already filled
            cyl = suffix_lookup.get(normalize_code(code))
            if cyl is not None:
                all_rows[idx]["cylinder_count"] = str(cyl)
                filled += 1
                filled_suffix += 1
                continue
            not_found.append(code)
    else:
        not_found = list(suffix_candidates)

    print(f"Resolved via exact match:        {filled - filled_norm - filled_suffix}")
    print(f"Resolved via normalized match:   {filled_norm}")
    print(f"Resolved via suffix match:       {filled_suffix}")

    # 5. Dry-run or write
    if args.dry_run:
        print(f"\n[DRY RUN] Would update {filled} rows.")
        if not_found:
            print(f"[DRY RUN] {len(not_found)} codes remain unresolved.")
            from collections import Counter
            top = Counter(not_found).most_common(10)
            print("Top 10 unresolved engine codes:")
            for code, count in top:
                print(f"  {code}  (x{count})")
        # Show preview
        shown = 0
        for idx in needs_fill:
            if all_rows[idx].get("cylinder_count", "").strip() not in ("", "0"):
                r = all_rows[idx]
                brand = r.get("brand", "")[:20]
                code = r.get("engine_code", "")[:20]
                cyl = r.get("cylinder_count", "")
                try:
                    print(f"  {brand:20} code={code:20} cyl={cyl}")
                except UnicodeEncodeError:
                    print(f"  {'(brand)':20} code={code:20} cyl={cyl}")
                shown += 1
                if shown >= 30:
                    if filled > 30:
                        print(f"  ... and {filled - 30} more")
                    break
        # Print final summary
        print()
        print("---")
        print(f"TecDoc engine_code->cyl pairs loaded:  {total_pairs}")
        print(f"vds_engine_map rows already filled:    {skip_already}  (skipped)")
        print(f"Rows filled this run:                  {filled}")
        print(f"Rows still missing (engine_code unknown to TecDoc):  {len(not_found)}")
        if not_found:
            from collections import Counter
            top = Counter(not_found).most_common(10)
            print("Top 10 unresolved engine codes:")
            for code, count in top:
                print(f"  {code}  (x{count})")
        return

    if filled == 0:
        print("No rows to write.")
        return

    # 6. Write CSV (preserve exact header order)
    with VDS_MAP_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=original_header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"vds_engine_map.csv written:      {original_row_count} rows")

    # 7. Post-write validation
    with VDS_MAP_CSV.open("r", encoding="utf-8", newline="") as f:
        verify_rows = list(csv.DictReader(f))

    # Assert header identical
    assert list(verify_rows[0].keys()) == original_header, (
        "Header changed — column added/removed"
    )

    # Assert row count unchanged
    assert len(verify_rows) == original_row_count, (
        f"Row count changed: {original_row_count} -> {len(verify_rows)}"
    )

    # Assert all rows updated this run have valid cylinder_count in range 2-16
    updated_indices = {idx for idx in needs_fill
                       if all_rows[idx].get("cylinder_count", "").strip() not in ("", "0")}
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

    # Assert no diesel codes escaped with cylinder_count filled (this run only)
    diesel_rows = [
        r for i, r in enumerate(verify_rows)
        if i in updated_indices
        and r.get("cylinder_count", "").strip() not in ("", "0")
        and is_diesel_code(r.get("engine_code", "").strip())
    ]
    assert not diesel_rows, f"Diesel codes with cylinder_count: {diesel_rows[:3]}"

    print("Diesel guard PASS")
    print("OK")

    # 8. Exit summary
    empty_count = sum(
        1 for r in verify_rows
        if r.get("cylinder_count", "").strip() in ("", "0")
        and r.get("engine_code", "").strip()
    )
    print()
    print("---")
    print(f"TecDoc engine_code->cyl pairs loaded:  {total_pairs}")
    print(f"vds_engine_map rows already filled:    {skip_already}  (skipped)")
    print(f"Rows filled this run:                  {filled}")
    print(f"Rows still missing (engine_code unknown to TecDoc):  {empty_count}")
    if not_found:
        from collections import Counter
        top = Counter(not_found).most_common(10)
        print("Top 10 unresolved engine codes:")
        for code, count in top:
            print(f"  {code}  (x{count})")


if __name__ == "__main__":
    main()
