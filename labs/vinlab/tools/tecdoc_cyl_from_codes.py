"""
tools/tecdoc_cyl_from_codes.py

Derives cylinder_count from manufacturer engine-code naming conventions
for the four top unresolved brands (Renault, Mercedes, BMW, Peugeot).

This is a STRUCTURAL approach — the engine code itself encodes the cylinder
layout via family prefix, digit position, or numeric range.  No MySQL.

Source of rules:
  vehicle-data/enginevincyl.md

H1 PETROL-ONLY: diesel guard applied at the engine-code level (same
   DIESEL_CODES set as all other tools/tecdoc_*.py scripts).
H3 Do not modify: vinlab/decoder.py, vinlab/models.py, vinlab/overlay/*.py.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
VDS_MAP_CSV = ROOT / "vinlab" / "data" / "vds_engine_map.csv"

DIESEL_CODES: frozenset[str] = frozenset({
    "sh", "rf", "d4cb", "d4bh", "d4ea", "d4fc", "d4fd",
    "d4fv", "d4bb", "d4bf", "cdi", "tdi",
    "dci", "hdi", "cdti", "crdi",
})

# Target brands (uppercase — matched case-insensitively against CSV brand column)
TARGET_BRANDS = {"RENAULT", "MERCEDES BENZ", "MERCEDES-BENZ", "BMW", "PEUGEOT"}

# ---------------------------------------------------------------------------
# manufacturer rules
# ---------------------------------------------------------------------------

# -- Renault: first letter determines cylinder count --------------------------
# Source: enginevincyl.md §1

RENAULT_3 = frozenset("HB")          # H4B, H5F, B4D — 3-cyl TCe
RENAULT_4 = frozenset("KFRMDG")      # K4M, F4R, R9M, M9R, D4F, G9T
RENAULT_6 = frozenset("V")           # V4Y, V9X — V6


def renault_cyl(code: str) -> int | None:
    code = code.strip().upper()
    if not code:
        return None
    first = code[0]
    if first in RENAULT_3:
        return 3
    if first in RENAULT_4:
        return 4
    if first in RENAULT_6:
        return 6
    return None


# -- Mercedes: 3-digit family number after M / OM prefix ----------------------
# Source: enginevincyl.md §2

MERC_FAMILIES: dict[str, int] = {
    # 4 cylinders
    "111": 4, "260": 4, "270": 4, "271": 4, "274": 4,
    "611": 4, "640": 4, "646": 4, "651": 4, "654": 4,
    # 6 cylinders
    "112": 6, "272": 6, "276": 6, "256": 6, "642": 6, "656": 6,
    # 8 cylinders
    "113": 8, "273": 8, "278": 8, "176": 8, "177": 8, "157": 8,
}

_MERC_RE = re.compile(r"(?:M|OM)?(\d{3})")


def mercedes_cyl(code: str) -> int | None:
    clean = code.strip().upper().replace(" ", "").replace(".", "").replace(",", "")
    m = _MERC_RE.search(clean)
    if m:
        return MERC_FAMILIES.get(m.group(1))
    return None


# -- BMW: 2nd character (first digit after letter prefix) = cylinder count ----
# Source: enginevincyl.md §3
# BMW engine codes: N47D20, B58B30, S65B40 — letter + digit pair.
# N47 = 4-cyl, B58 = 6-cyl (5 = modular inline-6 exception), B38 = 3-cyl.

_BMW_RE = re.compile(r"^([NBSM])(\d)")


def bmw_cyl(code: str) -> int | None:
    clean = code.strip().upper().replace(" ", "").replace(".", "")
    m = _BMW_RE.match(clean)
    if not m:
        return None
    digit = int(m.group(2))
    if digit == 5:
        return 6  # exception: B58 / N55 / S55 = inline-6, not 5-cyl
    if digit in (3, 4, 6, 8):
        return digit
    return None


# -- Peugeot / PSA: engine family prefix -------------------------------------
# Source: enginevincyl.md §4

PEUGEOT_FAMILIES: dict[str, int] = {
    "EB": 3,  # EB2DT PureTech 3-cyl
    "DV": 4,  # DV6 HDi
    "EP": 4,  # EP6 Prince
    "EW": 4,  # EW10
    "DW": 4,  # DW10 HDi
    "TU": 4,  # TU5
    "ET": 4,  # ET3
    "ES": 6,  # ES9 V6
}


def peugeot_cyl(code: str) -> int | None:
    clean = code.strip().upper().replace(" ", "")
    prefix = clean[:2]
    return PEUGEOT_FAMILIES.get(prefix)


# ---------------------------------------------------------------------------
# brand dispatch
# ---------------------------------------------------------------------------

# Map of brand name -> rule function.  Only these brands are decoded.
BRAND_RULES = {
    "RENAULT": renault_cyl,
    "MERCEDES BENZ": mercedes_cyl,
    "MERCEDES-BENZ": mercedes_cyl,
    "BMW": bmw_cyl,
    "PEUGEOT": peugeot_cyl,
}


def is_diesel_code(engine_code: str) -> bool:
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

def main() -> None:
    parser = argparse.ArgumentParser(
        description="T-CSV-3b: Derive cylinder_count from engine-code naming conventions"
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

    # 2. Identify rows needing enrichment — target brands only, empty cyl
    needs_fill: list[int] = []
    skip_already = 0
    skip_no_code = 0
    skip_diesel = 0
    skip_wrong_brand = 0

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

        brand = row.get("brand", "").strip().upper()
        if brand not in TARGET_BRANDS:
            skip_wrong_brand += 1
            continue

        needs_fill.append(i)

    print(f"Already have cylinder_count:     {skip_already}")
    print(f"No engine_code (skip):           {skip_no_code}")
    print(f"Diesel code (skip):              {skip_diesel}")
    print(f"Not a target brand (skip):       {skip_wrong_brand}")
    print(f"Rows needing enrichment:         {len(needs_fill)}")

    if not needs_fill:
        print("Nothing to do.")
        return

    # 3. Apply manufacturer rules
    filled = 0
    filled_by: dict[str, int] = {}
    not_found: list[tuple[str, str]] = []  # (brand, code)

    for idx in needs_fill:
        brand = all_rows[idx].get("brand", "").strip().upper()
        code = all_rows[idx].get("engine_code", "").strip().upper()
        rule = BRAND_RULES.get(brand)
        if rule is None:
            not_found.append((brand, code))
            continue
        cyl = rule(code)
        if cyl is not None:
            all_rows[idx]["cylinder_count"] = str(cyl)
            filled += 1
            filled_by[brand] = filled_by.get(brand, 0) + 1
        else:
            not_found.append((brand, code))

    print(f"Rows filled via naming rules:    {filled}")
    for brand, cnt in sorted(filled_by.items(), key=lambda x: -x[1]):
        print(f"  {brand:30} {cnt}")

    # 4. Dry-run or write
    if args.dry_run:
        print(f"\n[DRY RUN] Would update {filled} rows.")
        if not_found:
            print(f"[DRY RUN] {len(not_found)} codes remain unresolved in target brands.")
        shown = 0
        for idx in needs_fill:
            if all_rows[idx].get("cylinder_count", "").strip() not in ("", "0"):
                r = all_rows[idx]
                brand = r.get("brand", "")[:25]
                code = r.get("engine_code", "")[:25]
                cyl = r.get("cylinder_count", "")
                try:
                    print(f"  {brand:25} code={code:25} cyl={cyl}")
                except UnicodeEncodeError:
                    print(f"  {'(brand)':25} code={code:25} cyl={cyl}")
                shown += 1
                if shown >= 30:
                    if filled > 30:
                        print(f"  ... and {filled - 30} more")
                    break
        print()
        print("---")
        print(f"Rows filled this run:                  {filled}")
        print(f"Rows still unresolved in target brands: {len(not_found)}")
        return

    if filled == 0:
        print("No rows to write.")
        return

    # 5. Write CSV (preserve exact header order)
    with VDS_MAP_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=original_header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"vds_engine_map.csv written:      {original_row_count} rows")

    # 6. Post-write validation
    with VDS_MAP_CSV.open("r", encoding="utf-8", newline="") as f:
        verify_rows = list(csv.DictReader(f))

    assert list(verify_rows[0].keys()) == original_header, (
        "Header changed — column added/removed"
    )
    assert len(verify_rows) == original_row_count, (
        f"Row count changed: {original_row_count} -> {len(verify_rows)}"
    )

    # Range check: only rows updated this run
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

    filled_total = sum(
        1 for r in verify_rows
        if r.get("cylinder_count", "").strip() not in ("", "0")
    )
    print(f"Range check PASS                 ({filled_total} rows with cylinder_count)")

    # Diesel guard: only rows updated this run
    diesel_rows = [
        r for i, r in enumerate(verify_rows)
        if i in updated_indices
        and r.get("cylinder_count", "").strip() not in ("", "0")
        and is_diesel_code(r.get("engine_code", "").strip())
    ]
    assert not diesel_rows, f"Diesel codes with cylinder_count: {diesel_rows[:3]}"
    print("Diesel guard PASS")
    print("OK")

    # 7. Exit summary
    still_empty = sum(
        1 for r in verify_rows
        if r.get("cylinder_count", "").strip() in ("", "0")
        and r.get("engine_code", "").strip()
    )
    print()
    print("---")
    print(f"Rows filled this run:                  {filled}")
    print(f"Total rows with cylinder_count:        {filled_total}")
    print(f"Rows still empty (w/ engine_code):     {still_empty}")


if __name__ == "__main__":
    main()
