"""Extract engine codes from OPSI DMV CSV files for 7 WMI groups.

Reads three Nio_vozila_*.csv files, extracts engine codes from the P15
column for target WMI prefixes (JMZ, KNE, KLA, KNA, 3MZ, 3MD, 3MV, MDH),
filters out diesel codes, groups by (brand, vds_full, engine_code) with
most-frequent displacement, and writes vds_engine_map.csv rows.

Usage:
    cd C:/Users/muto/claude/4DApp/4DLab/DNALab/VINLab
    python tools/extract_opsi_engine_codes.py new_opsi_rows.csv

Run once per build cycle; kept as audit trail.
"""

from __future__ import annotations

import csv
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

# source: OPSI dataset — Slovenian DMV registration data 30.06.2023
VEHICLE_DATA_ROOT_ENV = os.environ.get("VEHICLE_DATA_ROOT")
if not VEHICLE_DATA_ROOT_ENV:
    raise RuntimeError("VEHICLE_DATA_ROOT environment variable is not set")
OPSI_DIR = Path(VEHICLE_DATA_ROOT_ENV) / "OPSI_podatki_reg._vozilih_30.06.2023"
OPSI_FILES: list[Path] = [
    OPSI_DIR / "Nio_vozila_1.csv",
    OPSI_DIR / "Nio_vozila_2.csv",
    OPSI_DIR / "Nio_vozila_3.csv",
]

# source: T-FX-6 task spec — 7 WMI groups to extract (petrol only)
TARGET_WMI_PREFIXES: frozenset[str] = frozenset({
    "JMZ", "KNE", "KLA", "KNA", "3MZ", "3MD", "3MV", "MDH",
})

# source: T-FX-6 task spec §Context — confirmed diesel engine codes
# that appear in the OPSI data for these WMI groups. Must be excluded.
DIESEL_CODES: frozenset[str] = frozenset({
    "sh", "rf", "d4cb", "d4bh", "d4ea", "d4fc", "d4fd", "d4fv",
    "j2", "jtd", "cdi", "tdi", "dci", "hdi", "cdti", "dth",
    "d4bb", "d4bf", "crdi",
})

# source: T-FX-6 task spec — brand mapping for WMI prefixes
WMI_TO_BRAND: dict[str, str] = {
    "JMZ": "Mazda",
    "KNE": "Kia",       # uses KIA engine namespace per platform sharing
    "KLA": "Daewoo",
    "KNA": "Kia",
    "3MZ": "Mazda",
    "3MD": "Mazda",
    "3MV": "Mazda",
    "MDH": "Nissan",
}

# source: vref.db row 0 — this is an authoritative override at decode time.
# The numbers below are safe defaults that won't be reached if vref.db has data.
# source: T-FX-6 task spec — safe cylinder count defaults by displacement band
def derive_cylinder_count(displacement_cc: int) -> int:
    """Derive cylinder count from displacement (safe default only)."""
    if displacement_cc <= 1000:
        return 3
    if displacement_cc <= 2200:
        return 4
    return 6


def is_diesel(engine_code: str) -> bool:
    """Check if an engine code is a known diesel code."""
    return engine_code.lower() in DIESEL_CODES


def extract() -> list[dict[str, str]]:
    """Extract engine codes from all 3 OPSI CSV files.

    Returns a list of rows ready to append to vds_engine_map.csv,
    in the format:
        brand,vds_full,pos_8_only,engine_code,engine_displacement,cylinder_count,fuel_system_type
    """
    # Group key: (brand, vds_full, engine_code)
    # Store: {group_key: Counter[displacement_cc]}
    groups: dict[tuple[str, str, str], Counter[int]] = defaultdict(Counter)

    total_rows: int = 0
    diesel_excluded: int = 0
    empty_engine: int = 0
    corrupt_excluded: int = 0

    for fpath in OPSI_FILES:
        if not fpath.exists():
            print(f"WARNING: file not found, skipping: {fpath}", file=sys.stderr)
            continue

        with fpath.open(encoding="utf-8", errors="replace", newline="") as fh:
            reader = csv.reader(fh, delimiter=";", quotechar='"')
            next(reader, None)  # skip header
            for row in reader:
                if len(row) < 57:
                    continue
                vin = row[26].strip()  # col 27 E-VIN, 0-indexed = 26
                if len(vin) != 17:
                    continue
                wmi = vin[:3]
                if wmi not in TARGET_WMI_PREFIXES:
                    continue

                total_rows += 1
                engine_code = row[51].strip()  # col 52 P15, 0-indexed = 51
                if not engine_code:
                    empty_engine += 1
                    continue
                if "�" in engine_code:
                    corrupt_excluded += 1
                    continue
                if is_diesel(engine_code):
                    diesel_excluded += 1
                    continue

                vds_full = vin[3:8]
                brand = WMI_TO_BRAND[wmi]
                displacement_str = row[46].strip()  # col 47 P11, 0-indexed = 46
                disp_cc = 0
                if displacement_str:
                    try:
                        disp_cc = int(displacement_str)
                    except ValueError:
                        pass

                key = (brand, vds_full, engine_code.upper())
                groups[key][disp_cc] += 1

    # Produce output rows — pick most-frequent displacement per group
    rows: list[dict[str, str]] = []
    for (brand, vds_full, engine_code), disp_counter in sorted(groups.items()):
        # Most frequent non-zero displacement; fall back to most frequent
        if disp_counter:
            best_disp = max(disp_counter, key=lambda d: disp_counter[d])
        else:
            best_disp = 0

        cylinder_count = derive_cylinder_count(best_disp) if best_disp > 0 else 4
        displacement_liters = best_disp / 1000.0 if best_disp > 0 else 0.0

        rows.append({
            "brand": brand,
            "vds_full": vds_full,
            "pos_8_only": "",
            "engine_code": engine_code,
            "engine_displacement": f"{displacement_liters:.3g}",
            "cylinder_count": str(cylinder_count),
            "fuel_system_type": "PORT_INJECTION",
        })

    # Print summary to stderr
    print(f"Total rows processed (target WMIs, len=17): {total_rows}", file=sys.stderr)
    print(f"Diesel excluded: {diesel_excluded}", file=sys.stderr)
    print(f"Empty engine code: {empty_engine}", file=sys.stderr)
    print(f"Corrupt encoding excluded: {corrupt_excluded}", file=sys.stderr)
    print(f"Net new rows: {len(rows)}", file=sys.stderr)

    return rows


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    """Write rows to output_path in vds_engine_map.csv column order."""
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(
            "brand,vds_full,pos_8_only,engine_code,engine_displacement,"
            "cylinder_count,fuel_system_type\n"
        )
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "brand", "vds_full", "pos_8_only", "engine_code",
                "engine_displacement", "cylinder_count", "fuel_system_type",
            ],
            lineterminator="\n",
        )
        for row in rows:
            writer.writerow(row)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python tools/extract_opsi_engine_codes.py <output.csv>", file=sys.stderr)
        sys.exit(1)
    output_path = Path(sys.argv[1])
    rows = extract()
    write_csv(rows, output_path)
    print(f"Wrote {len(rows)} rows to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
