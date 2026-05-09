#!/usr/bin/env python3
"""Build engine/v2/vref.db with the V2 engine_ref schema.

Primary data source: tools/vref_manual_overrides.yaml (top engine codes
with tech-mask flags). Optional OPSI CSV enrichment if the vehicle-data
directory is present.

V2 schema per v2-era-masking skill §5:
  engine_code TEXT PRIMARY KEY, brand, displacement_cc, euro_norm,
  my_start, my_end, era_bucket, has_vvt, has_gdi, has_turbo,
  is_v_engine, has_egr, has_secondary_air, o2_type,
  target_rpm_u2, target_lambda_v112
"""

from __future__ import annotations

import csv
import re
import sqlite3
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
OVERRIDES_YAML = ROOT / "tools" / "vref_manual_overrides.yaml"
OUT_DB = ROOT / "engine" / "v2" / "vref.db"
CSV_DIR = ROOT / "vehicle-data" / "OPSI_podatki_reg._vozilih_30.06.2023"
CSV_ENCODING = "iso-8859-1"
CSV_FILES = [CSV_DIR / f"Nio_vozila_{i}.csv" for i in (1, 2, 3)]

# ---------------------------------------------------------------------------
# Era bucket derivation
# ---------------------------------------------------------------------------
ERA_BUCKETS = [
    (1990, 1995, "ERA_PRE_OBDII"),
    (1996, 2005, "ERA_OBDII_EARLY"),
    (2006, 2015, "ERA_CAN"),
    (2016, 2020, "ERA_MODERN"),
]


def _derive_era(my_start: int, my_end: int) -> str:
    """Map (my_start, my_end) to the earliest matching era bucket."""
    for era_start, era_end, label in ERA_BUCKETS:
        if my_start <= era_end and my_end >= era_start:
            return label
    return "ERA_MODERN"


# ---------------------------------------------------------------------------
# V2 engine_ref schema (source: v2-era-masking skill §5)
# ---------------------------------------------------------------------------
CREATE_ENGINE_REF = """\
CREATE TABLE IF NOT EXISTS engine_ref (
    engine_code        TEXT PRIMARY KEY,
    brand              TEXT    NOT NULL,
    displacement_cc    INTEGER,
    euro_norm          TEXT,
    my_start           INTEGER,
    my_end             INTEGER,
    era_bucket         TEXT    NOT NULL,
    has_vvt            INTEGER NOT NULL DEFAULT 0,
    has_gdi            INTEGER NOT NULL DEFAULT 0,
    has_turbo          INTEGER NOT NULL DEFAULT 0,
    is_v_engine        INTEGER NOT NULL DEFAULT 0,
    has_egr            INTEGER NOT NULL DEFAULT 0,
    has_secondary_air  INTEGER NOT NULL DEFAULT 0,
    o2_type            TEXT    NOT NULL DEFAULT 'NB',
    target_rpm_u2      INTEGER NOT NULL DEFAULT 2500,
    target_lambda_v112 REAL    NOT NULL DEFAULT 1.000
)
"""

INSERT_ROW = """\
INSERT OR REPLACE INTO engine_ref
    (engine_code, brand, displacement_cc, euro_norm, my_start, my_end,
     era_bucket, has_vvt, has_gdi, has_turbo, is_v_engine, has_egr,
     has_secondary_air, o2_type, target_rpm_u2, target_lambda_v112)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# ---------------------------------------------------------------------------
# Petrol-only guard
# ---------------------------------------------------------------------------
PETROL_ONLY_FUEL_TYPES = frozenset({"petrol"})


def _bool_to_int(value: bool) -> int:
    return 1 if value else 0


# ---------------------------------------------------------------------------
# YAML loading (stdlib-only, no PyYAML dependency)
# ---------------------------------------------------------------------------
def _load_overrides(path: Path) -> list[dict]:
    """Parse vref_manual_overrides.yaml without a YAML library.

    Uses a minimal line-based parser that handles the simple flat-record
    format used by the overrides file. Falls back to PyYAML if installed.
    """
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        yaml = None  # type: ignore[assignment]

    if yaml is not None:
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        return doc.get("engines", [])

    # Minimal stdlib parser for this specific YAML structure
    return _parse_overrides_stdlib(path)


def _parse_overrides_stdlib(path: Path) -> list[dict]:
    """Minimal line-based parser for the manual overrides YAML format."""
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[dict] = []
    current: dict | None = None
    list_context: str | None = None

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Detect list-of-dicts start
        if stripped == "engines:":
            list_context = "engines"
            continue

        if list_context == "engines" and stripped.startswith("- "):
            key_val = stripped[2:]
            if ":" in key_val:
                k, v = key_val.split(":", 1)
                k = k.strip()
                v = v.strip()
                if k == "engine_code":
                    if current is not None:
                        entries.append(current)
                    current = {}
                if current is not None:
                    current[k] = _yaml_scalar(v)
            continue

        # Indented key: value (4 spaces)
        if (current is not None and line.startswith("    ")
                and not stripped.startswith("- ") and ":" in stripped):
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip()
            if k not in ("engine_code",) and v:
                current[k] = _yaml_scalar(v)

    if current is not None:
        entries.append(current)

    return entries


def _yaml_scalar(value: str) -> str | int | float | bool:
    """Coerce a YAML scalar string to the appropriate Python type."""
    v = value.strip().strip('"').strip("'")
    if v in ("true", "True", "TRUE"):
        return True
    if v in ("false", "False", "FALSE"):
        return False
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


# ---------------------------------------------------------------------------
# Optional OPSI CSV enrichment
# ---------------------------------------------------------------------------
PETROL_CODES = frozenset({"P", "P/LPG", "P/CNG", "P/ET", "CNG", "LPG", "M"})
_EURO_RE = re.compile(r"EURO\s*(\d+[a-zA-Z]?|VI)", re.IGNORECASE)


def _norm_euro(raw: str) -> str:
    s = raw.strip()
    if not s or s == "-":
        return "unknown"
    m = _EURO_RE.search(s)
    if not m:
        if re.search(r"2003/76B", s):
            return "euro4"
        if re.search(r"91/441", s):
            return "euro1"
        if re.search(r"94/12", s):
            return "euro2"
        if re.search(r"96/69", s):
            return "euro2"
        if re.search(r"98/69", s) or re.search(r"1999/102", s):
            return "euro3"
        return "unknown"
    tok = m.group(1).upper()
    if tok == "VI":
        return "euro6"
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


def _try_enrich_from_opsi(rows: list[dict]) -> None:
    """If OPSI CSVs exist, compute median lambda/RPM per (brand, displ_cc, euro_norm)
    and update any matching rows' target_rpm_u2/target_lambda_v112."""
    if not CSV_DIR.exists():
        print("OPSI CSVs not found — skipping enrichment pass.")
        return

    try:
        import numpy as np
    except ImportError:
        print("numpy not installed — skipping OPSI enrichment.")
        return

    from collections import defaultdict

    groups: dict[tuple, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for csv_path in CSV_FILES:
        if not csv_path.exists():
            continue
        print(f"Reading {csv_path.name} for enrichment ...")
        with open(csv_path, encoding=CSV_ENCODING) as fh:
            for row in csv.DictReader(fh, delimiter=";"):
                fuel_code = (row.get("P13-Vrsta goriva (oznaka)", "") or "").strip()
                if fuel_code not in PETROL_CODES:
                    continue
                brand = (row.get("D1-Znamka", "") or "").strip().upper()
                if not brand:
                    continue
                cc_raw = row.get("P11-Delovna prostornina", "")
                try:
                    displ_cc = int(float(str(cc_raw).replace(",", ".")))
                except (TypeError, ValueError):
                    continue
                displ_bucket = round(displ_cc / 100) * 100
                euro = _norm_euro(row.get("V9-Podatek o okoljevarstveni kategoriji vozila", ""))

                key = (brand, displ_bucket, euro)

                for col, csv_field in [
                    ("lambda_vals", "V112-Vrednost Lambda"),
                    ("rpm_hi_vals", "V11-Vrtilna frekvenca prostega teka, visoka"),
                ]:
                    raw = row.get(csv_field, "")
                    v = _safe_float(raw)
                    if v is not None and 0 < v < 100000:
                        groups[key][col].append(v)

    enriched = 0
    for row_dict in rows:
        brand = str(row_dict.get("brand", "")).upper()
        displ = int(row_dict.get("displacement_cc", 0))
        displ_bucket = round(displ / 100) * 100
        euro = str(row_dict.get("euro_norm", "unknown"))
        key = (brand, displ_bucket, euro)
        if key in groups:
            lambdas = groups[key].get("lambda_vals", [])
            rpms = groups[key].get("rpm_hi_vals", [])
            if lambdas and "target_lambda_v112" not in row_dict:
                row_dict["target_lambda_v112"] = round(float(np.median(lambdas)), 3)
                enriched += 1
            if rpms and "target_rpm_u2" not in row_dict:
                row_dict["target_rpm_u2"] = int(round(np.median(rpms)))
                enriched += 1

    if enriched:
        print(f"OPSI enrichment: {enriched} fields updated.")


def _safe_float(raw: str) -> float | None:
    if not raw:
        return None
    s = str(raw).strip()
    if not s or s == "-":
        return None
    try:
        return float(s.replace(",", "."))
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def main() -> None:
    # 1. Load manual overrides
    print(f"Loading manual overrides from {OVERRIDES_YAML} ...")
    if not OVERRIDES_YAML.exists():
        print(f"ERROR: {OVERRIDES_YAML} not found.")
        raise SystemExit(1)

    entries = _load_overrides(OVERRIDES_YAML)

    # 2. Filter petrol-only
    petrol_entries = []
    skipped = 0
    for e in entries:
        fuel = str(e.get("fuel_type", "petrol")).lower()
        if fuel in PETROL_ONLY_FUEL_TYPES:
            petrol_entries.append(e)
        else:
            skipped += 1
            print(f"  Skipping non-petrol: {e.get('engine_code', '?')} (fuel_type={fuel})")

    print(f"Loaded {len(petrol_entries)} petrol engine codes"
          f"{f' ({skipped} skipped)' if skipped else ''}.")

    # 3. Optional OPSI enrichment
    _try_enrich_from_opsi(petrol_entries)

    # 4. Derive era_bucket for any entry missing it
    for e in petrol_entries:
        my_start = int(e.get("my_start", 2000))
        my_end = int(e.get("my_end", 2010))
        if "era_bucket" not in e:
            e["era_bucket"] = _derive_era(my_start, my_end)

    # 5. Create output directory and database
    out_dir = OUT_DB.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(OUT_DB))
    conn.execute("DROP TABLE IF EXISTS engine_ref")
    conn.execute(CREATE_ENGINE_REF)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_engine_ref_brand "
        "ON engine_ref(brand, displacement_cc, euro_norm)"
    )

    # 6. Insert rows
    inserted = 0
    for e in petrol_entries:
        ec = str(e.get("engine_code", ""))
        if not ec:
            continue

        brand = str(e.get("brand", "")).upper()
        displ_cc = int(e.get("displacement_cc", 0))
        euro = str(e.get("euro_norm", "unknown"))
        my_start = int(e.get("my_start", 2000))
        my_end = int(e.get("my_end", 2010))
        era_bucket = str(e.get("era_bucket", _derive_era(my_start, my_end)))

        row = (
            ec,
            brand,
            displ_cc if displ_cc > 0 else None,
            euro if euro != "unknown" else None,
            my_start,
            my_end,
            era_bucket,
            _bool_to_int(bool(e.get("has_vvt", False))),
            _bool_to_int(bool(e.get("has_gdi", False))),
            _bool_to_int(bool(e.get("has_turbo", False))),
            _bool_to_int(bool(e.get("is_v_engine", False))),
            _bool_to_int(bool(e.get("has_egr", False))),
            _bool_to_int(bool(e.get("has_secondary_air", False))),
            str(e.get("o2_type", "NB")),
            int(e.get("target_rpm_u2", 2500)),
            float(e.get("target_lambda_v112", 1.000)),
        )
        conn.execute(INSERT_ROW, row)
        inserted += 1

    conn.commit()

    # 7. Report
    count = conn.execute("SELECT COUNT(*) FROM engine_ref").fetchone()[0]
    print(f"Wrote {count} rows to {OUT_DB}")

    # Quick sanity
    sample = conn.execute(
        "SELECT engine_code, brand, era_bucket, has_vvt, has_gdi, has_turbo "
        "FROM engine_ref ORDER BY engine_code LIMIT 5"
    ).fetchall()
    print("Sample rows:")
    for s in sample:
        print(f"  {s[0]:30s} {s[1]:15s} {s[2]:20s} vvt={s[3]} gdi={s[4]} turbo={s[5]}")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
