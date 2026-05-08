#!/usr/bin/env python3
"""Build vref.db from OPSI Slovenian registration CSV files.

Reads Nio_vozila_1/2/3.csv, filters petrol, buckets displacement, and
aggregates per-engine emission/RPM reference values via median.

Extends the original schema with 6 new columns requested by v2 HLD:
  ref_u2_rpm, ref_low_idle_rpm, ref_low_idle_co,
  ref_high_idle_rpm, ref_high_idle_co, ref_high_idle_lambda
"""

from __future__ import annotations

import csv
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent.parent
CSV_DIR = ROOT / "vehicle-data" / "OPSI_podatki_reg._vozilih_30.06.2023"
OUT_DB = ROOT / "vehicle-data" / "vref.db"
CSV_ENCODING = "iso-8859-1"

CSV_FILES = [CSV_DIR / f"Nio_vozila_{i}.csv" for i in (1, 2, 3)]

# ---------------------------------------------------------------------------
# Fuel-code → internal fuel_type
# ---------------------------------------------------------------------------
PETROL_CODES = {"P", "P/LPG", "P/CNG", "P/ET", "CNG", "LPG", "M", "LNG", "H", "O"}
DIESEL_CODES = {"D", "D/BD", "D/LPG", "D/CNG", "LNG/D"}


def _norm_fuel(raw: str) -> str | None:
    code = raw.strip()
    if code in PETROL_CODES:
        return "petrol"
    if code in DIESEL_CODES:
        return "diesel"
    return None


# ---------------------------------------------------------------------------
# Euro-norm string → internal code (euro4, euro5, euro6, pre_euro3, etc.)
# ---------------------------------------------------------------------------
_EURO_RE = re.compile(r"EURO\s*(\d+[a-zA-Z]?|VI)", re.IGNORECASE)


def _norm_euro(raw: str) -> str:
    s = raw.strip()
    if not s or s == "-":
        return "unknown"
    m = _EURO_RE.search(s)
    if not m:
        # Try common patterns without "EURO" label
        if re.search(r"2003/76B", s):
            return "euro4"
        if re.search(r"2002/80[AB]?", s):
            return "euro4"
        if re.search(r"2001/100A?", s):
            return "euro3"
        if re.search(r"2006/96B?", s):
            return "euro4"
        if re.search(r"83RII", s):
            return "euro4"
        if re.search(r"98/69", s) or re.search(r"1999/102", s):
            return "euro3"
        if re.search(r"96/69", s) or re.search(r"94/12", s):
            return "euro2"
        if re.search(r"91/441", s):
            return "euro1"
        if re.search(r"97/24", s):
            return "euro2"
        return "unknown"

    tok = m.group(1).upper()
    if tok == "VI":
        return "euro6"
    # Strip trailing letters: "5a" → "5", "6b" → "6", "6d" → "6"
    num = re.match(r"(\d+)", tok)
    if num:
        digit = int(num.group(1))
        if digit <= 0:
            return "euro0"
        if digit <= 1:
            return "euro1"
        if digit <= 2:
            return "euro2"
        if digit <= 3:
            return "euro3"
        if digit <= 4:
            return "euro4"
        if digit <= 5:
            return "euro5"
        return "euro6"
    return "unknown"


def _emission_class(euro_norm: str) -> str:
    """Map fine-grained euro_norm to coarse emission_class."""
    if euro_norm in ("euro4", "euro5", "euro6"):
        return "euro4"
    return "pre_euro4"


# ---------------------------------------------------------------------------
# Displacement bucket
# ---------------------------------------------------------------------------
def _bucket(cc) -> int | None:
    try:
        return round(int(cc) / 100) * 100
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def _safe_float(raw) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s == "-":
        return None
    try:
        s = s.replace(",", ".")
        return float(s)
    except (TypeError, ValueError):
        return None


def _safe_int(raw) -> int | None:
    v = _safe_float(raw)
    if v is None:
        return None
    return int(round(v))


def main() -> None:
    # Read & parse all CSVs into per-key lists of numeric values
    groups: dict[tuple, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )

    total_rows = 0
    petrol_rows = 0

    for csv_path in CSV_FILES:
        print(f"Reading {csv_path.name} ...")
        with open(csv_path, "r", encoding=CSV_ENCODING) as fh:
            reader = csv.DictReader(fh, delimiter=";")
            for row in reader:
                total_rows += 1

                fuel = _norm_fuel(row.get("P13-Vrsta goriva (oznaka)", ""))
                if fuel is None:
                    continue
                if fuel not in ("petrol", "diesel"):
                    continue
                petrol_rows += 1

                brand = (row.get("D1-Znamka", "") or "").strip().upper()
                if not brand:
                    continue

                displ_cc = _bucket(row.get("P11-Delovna prostornina", ""))
                if displ_cc is None:
                    continue

                euro = _norm_euro(
                    row.get("V9-Podatek o okoljevarstveni kategoriji vozila", "")
                )

                key = (brand, fuel, displ_cc, euro)

                # Existing columns
                _append_float(groups, key, "ref_co",
                              row.get("V1-CO"))
                _append_float(groups, key, "ref_hc",
                              row.get("V2-HC"))
                _append_float(groups, key, "ref_nox",
                              row.get("V3-Nox"))
                _append_float(groups, key, "ref_hc_nox",
                              row.get("V4-HC + Nox"))
                _append_float(groups, key, "ref_pm",
                              row.get("V5-Delci pri dizel motorjih"))
                _append_float(groups, key, "ref_smoke_k",
                              row.get("V6-Korigiran absorpcijski koeficient pri dizel motorjih"))
                _append_float(groups, key, "ref_co2",
                              row.get("V7-CO2"))
                _append_float(groups, key, "ref_co2_wltp",
                              row.get("CO2_WLTP"))
                _append_float(groups, key, "ref_fuel_cons",
                              row.get("V8-Kombinirana poraba goriva"))
                _append_float(groups, key, "ref_lambda",
                              row.get("V112-Vrednost Lambda"))
                _append_float(groups, key, "ref_idle_rpm_lo",
                              row.get("V10-Vrtilna frekvenca prostega teka, nizka"))
                _append_float(groups, key, "ref_idle_rpm_hi",
                              row.get("V11-Vrtilna frekvenca prostega teka, visoka"))
                _append_float(groups, key, "ref_co_idle_lo",
                              row.get("V101-Vsebina CO"))
                _append_float(groups, key, "ref_co_idle_hi",
                              row.get("V111-Vsebina CO"))

                # New columns (Part 2)
                _append_float(groups, key, "ref_u2_rpm",
                              row.get("U2-Pri vrtilni frekvenci motorja"))
                _append_float(groups, key, "ref_low_idle_rpm",
                              row.get("V10-Vrtilna frekvenca prostega teka, nizka"))
                _append_float(groups, key, "ref_low_idle_co",
                              row.get("V101-Vsebina CO"))
                _append_float(groups, key, "ref_high_idle_rpm",
                              row.get("V11-Vrtilna frekvenca prostega teka, visoka"))
                _append_float(groups, key, "ref_high_idle_co",
                              row.get("V111-Vsebina CO"))
                _append_float(groups, key, "ref_high_idle_lambda",
                              row.get("V112-Vrednost Lambda"))

    print(f"Total rows: {total_rows:,}")
    print(f"Petrol rows: {petrol_rows:,}")
    print(f"Aggregate keys (brand+fuel+displ+euro): {len(groups):,}")

    # Write to SQLite
    out_dir = OUT_DB.parent
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(OUT_DB))
    conn.execute("DROP TABLE IF EXISTS vehicle_refs")
    conn.execute("""
        CREATE TABLE vehicle_refs (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            brand               TEXT    NOT NULL,
            fuel_type           TEXT    NOT NULL,
            displ_bucket        INTEGER NOT NULL,
            euro_norm           TEXT    NOT NULL,
            emission_class      TEXT    NOT NULL,
            sample_count        INTEGER NOT NULL,
            ref_co              REAL,
            ref_hc              REAL,
            ref_nox             REAL,
            ref_hc_nox          REAL,
            ref_pm              REAL,
            ref_smoke_k         REAL,
            ref_co2             REAL,
            ref_co2_wltp        REAL,
            ref_fuel_cons       REAL,
            ref_lambda          REAL,
            ref_idle_rpm_lo     INTEGER,
            ref_idle_rpm_hi     INTEGER,
            ref_co_idle_lo      REAL,
            ref_co_idle_hi      REAL,
            ref_u2_rpm          INTEGER,
            ref_low_idle_rpm    INTEGER,
            ref_low_idle_co     REAL,
            ref_high_idle_rpm   INTEGER,
            ref_high_idle_co    REAL,
            ref_high_idle_lambda REAL
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_vehicle_refs_lookup "
        "ON vehicle_refs(brand, fuel_type, displ_bucket, euro_norm)"
    )

    sorted_keys = sorted(groups.keys())
    for key in sorted_keys:
        brand, fuel, displ, euro = key
        vals = groups[key]
        sample_count = len(vals["ref_co"])
        emission_class = _emission_class(euro)

        row_data = (
            brand, fuel, displ, euro, emission_class, sample_count,
            _median_float(vals.get("ref_co")),
            _median_float(vals.get("ref_hc")),
            _median_float(vals.get("ref_nox")),
            _median_float(vals.get("ref_hc_nox")),
            _median_float(vals.get("ref_pm")),
            _median_float(vals.get("ref_smoke_k")),
            _median_float(vals.get("ref_co2")),
            _median_float(vals.get("ref_co2_wltp")),
            _median_float(vals.get("ref_fuel_cons")),
            _median_float(vals.get("ref_lambda")),
            _median_int(vals.get("ref_idle_rpm_lo")),
            _median_int(vals.get("ref_idle_rpm_hi")),
            _median_float(vals.get("ref_co_idle_lo")),
            _median_float(vals.get("ref_co_idle_hi")),
            _median_int(vals.get("ref_u2_rpm")),
            _median_int(vals.get("ref_low_idle_rpm")),
            _median_float(vals.get("ref_low_idle_co")),
            _median_int(vals.get("ref_high_idle_rpm")),
            _median_float(vals.get("ref_high_idle_co")),
            _median_float(vals.get("ref_high_idle_lambda")),
        )

        conn.execute(
            """INSERT INTO vehicle_refs
               (brand, fuel_type, displ_bucket, euro_norm, emission_class,
                sample_count,
                ref_co, ref_hc, ref_nox, ref_hc_nox, ref_pm, ref_smoke_k,
                ref_co2, ref_co2_wltp, ref_fuel_cons, ref_lambda,
                ref_idle_rpm_lo, ref_idle_rpm_hi, ref_co_idle_lo, ref_co_idle_hi,
                ref_u2_rpm, ref_low_idle_rpm, ref_low_idle_co,
                ref_high_idle_rpm, ref_high_idle_co, ref_high_idle_lambda)
               VALUES (?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?,
                       ?, ?, ?, ?,
                       ?, ?, ?,
                       ?, ?, ?)""",
            row_data,
        )

    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM vehicle_refs").fetchone()[0]
    print(f"Wrote {count} rows to {OUT_DB}")

    # Sanity checks
    row = conn.execute(
        "SELECT brand, ref_u2_rpm, ref_high_idle_rpm, ref_high_idle_lambda "
        "FROM vehicle_refs WHERE brand='VOLKSWAGEN' AND displ_bucket=1400 "
        "AND euro_norm='euro5'"
    ).fetchone()
    if row:
        print(f"\nSanity check VW 1400cc euro5:")
        print(f"  ref_u2_rpm={row[1]}, ref_high_idle_rpm={row[2]}, "
              f"ref_high_idle_lambda={row[3]}")
        if row[1] is None or row[1] < 2500 or row[1] > 4500:
            print("  WARNING: ref_u2_rpm out of expected range (2500-4500)")
        else:
            print("  OK: ref_u2_rpm in expected range")
    else:
        print("WARNING: VW 1400cc euro5 not found in output")

    conn.close()
    print("Done.")


def _append_float(groups, key, col, raw):
    v = _safe_float(raw)
    if v is not None:
        groups[key][col].append(v)


def _median_float(lst) -> float | None:
    if not lst:
        return None
    return float(np.median(lst))


def _median_int(lst) -> int | None:
    if not lst:
        return None
    return int(round(np.median(lst)))


if __name__ == "__main__":
    main()
