#!/usr/bin/env python3
"""Build vinlab/data/vref.db from TecDoc MySQL + petrol CSV + manual YAML overrides.

One-shot build script. Produces a SQLite database with the engine_ref table
keyed by engine_code. The shipped vinlab/ package has no MySQL dependency.

Data sources (in precedence order):
  1. TecDoc MySQL      — tech-mask flags, engine measurements (when available)
  2. YAML overrides    — canonical engine codes, fallback flags
  3. petrol CSV        — CoC empirical medians per engine_code

Build is idempotent: re-running on same inputs produces byte-identical vref.db.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from statistics import median as _median
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
OVERRIDES_YAML = ROOT / "tools" / "vref_manual_overrides.yaml"
OUT_DB = ROOT / "vinlab" / "data" / "vref.db"
# DBS lives outside the repo (large reference dataset). Must be set in the environment.
DBS_ROOT_ENV = os.environ.get("DBS_ROOT")
if not DBS_ROOT_ENV:
    raise RuntimeError("DBS_ROOT environment variable is not set")
DBS_ROOT = Path(DBS_ROOT_ENV)
PETROL_CSV = DBS_ROOT / "docs" / "vehicles_petrol_specimens.csv"
CSV_ENCODING = "iso-8859-1"

# ---------------------------------------------------------------------------
# TecDoc connection (env vars with defaults)
# ---------------------------------------------------------------------------
TECDOC_HOST = os.environ.get("TECDOC_HOST", "127.0.0.1")
TECDOC_PORT = int(os.environ.get("TECDOC_PORT", "3306"))
TECDOC_USER = os.environ.get("TECDOC_USER", "root")
TECDOC_PASS = os.environ.get("TECDOC_PASS", "")
TECDOC_DB = os.environ.get("TECDOC_DB", "tecdoc")

# ---------------------------------------------------------------------------
# Era bucket derivation (source: v2-era-masking skill §5)
# ---------------------------------------------------------------------------
ERA_BUCKETS = [
    (1990, 1995, "ERA_PRE_OBDII"),
    (1996, 2005, "ERA_OBDII_EARLY"),
    (2006, 2015, "ERA_CAN"),
    (2016, 2020, "ERA_MODERN"),
]


def _derive_era(my_start: int, my_end: int) -> str:
    for era_start, era_end, label in ERA_BUCKETS:
        if my_start <= era_end and my_end >= era_start:
            return label
    return "ERA_MODERN"


# ---------------------------------------------------------------------------
# Petrol-only guard
# ---------------------------------------------------------------------------
PETROL_FUEL_TYPES = frozenset({"petrol"})
# TecDoc Russian fuel values that indicate petrol
TECDOC_PETROL_RUSSIAN = frozenset({
    "бензин", "Бензиновый двигатель", "Бензин/этанол",
    "Бензин/автогаз (LPG)", "Бензин/природный газ (CNG)",
    "Бензин / электричество", "Бензин/этанол/электричество",
    "Бензин / электричество / автогаз (LPG)",
    "Бензин / этанол / природный газ",
    "Бензиновый двигатель (двухтактный)",
})
# CSV fuel codes for petrol (source: v2 line 183)
CSV_PETROL_CODES = frozenset({"P", "P/LPG", "P/CNG", "P/ET", "CNG", "LPG", "M"})


# ---------------------------------------------------------------------------
# VINLab engine_ref schema (task T-VL-3 Deliverable 2f)
# ---------------------------------------------------------------------------
CREATE_ENGINE_REF = """\
CREATE TABLE IF NOT EXISTS engine_ref (
    engine_code        TEXT PRIMARY KEY,
    brand              TEXT NOT NULL,
    displacement_cc    INTEGER,
    euro_norm          TEXT,
    my_start           INTEGER,
    my_end             INTEGER,
    era_bucket         TEXT NOT NULL,
    -- Tech-mask flags (TecDoc primary, YAML fallback)
    has_vvt            INTEGER NOT NULL DEFAULT 0,
    has_gdi            INTEGER NOT NULL DEFAULT 0,
    has_turbo          INTEGER NOT NULL DEFAULT 0,
    is_v_engine        INTEGER NOT NULL DEFAULT 0,
    has_egr            INTEGER NOT NULL DEFAULT 0,
    has_maf            INTEGER NOT NULL DEFAULT 0,
    has_map            INTEGER NOT NULL DEFAULT 0,
    o2_type            TEXT NOT NULL DEFAULT 'NB',
    induction_type     TEXT,
    fuel_delivery_type TEXT,
    valvetrain_type    TEXT,
    -- CoC medians from petrol CSV (NULL if no CSV rows matched)
    rated_rpm                INTEGER,
    target_lambda_v112       REAL,
    target_rpm_u2            INTEGER,
    idle_rpm_low             INTEGER,
    co_low_idle              REAL,
    co_high_idle             REAL,
    co_type_approval         REAL,
    hc_type_approval         REAL,
    nox_type_approval        REAL,
    hc_nox_type_approval     REAL,
    co2_type_approval        REAL,
    noise_stationary_dba     REAL,
    noise_rpm                INTEGER,
    noise_driving_dba        REAL
);
CREATE INDEX IF NOT EXISTS idx_engine_ref_brand
    ON engine_ref(brand, displacement_cc, euro_norm);
"""

INSERT_ROW = """\
INSERT OR REPLACE INTO engine_ref
    (engine_code, brand, displacement_cc, euro_norm, my_start, my_end,
     era_bucket, has_vvt, has_gdi, has_turbo, is_v_engine, has_egr,
     has_maf, has_map, o2_type, induction_type,
     fuel_delivery_type, valvetrain_type,
     rated_rpm, target_lambda_v112, target_rpm_u2, idle_rpm_low,
     co_low_idle, co_high_idle, co_type_approval, hc_type_approval,
     nox_type_approval, hc_nox_type_approval, co2_type_approval,
     noise_stationary_dba, noise_rpm, noise_driving_dba)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------
def _bool_to_int(value: bool) -> int:
    return 1 if value else 0


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


def _safe_int(raw: str) -> int | None:
    if not raw:
        return None
    s = str(raw).strip()
    if not s or s == "-":
        return None
    try:
        return int(float(s.replace(",", ".")))
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# YAML loading (stdlib-only, no PyYAML dependency — adapted from v2)
# ---------------------------------------------------------------------------
def _load_overrides(path: Path) -> list[dict]:
    """Parse vref_manual_overrides.yaml without a YAML library."""
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        yaml = None  # type: ignore[assignment]

    if yaml is not None:
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        return doc.get("engines", [])

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

        if (
            current is not None
            and line.startswith("    ")
            and not stripped.startswith("- ")
            and ":" in stripped
        ):
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip()
            if k not in ("engine_code",) and v:
                current[k] = _yaml_scalar(v)

    if current is not None:
        entries.append(current)

    return entries


def _yaml_scalar(value: str) -> str | int | float | bool:
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
# TecDoc extraction
# ---------------------------------------------------------------------------
# Russian-to-English translation map (source: BUILD_DATA_SOURCES.md §C.3)
_ENGINE_CONSTRUCTION_MAP = {
    "ряд": "I",
    "V": "V",
    "VR": "V",
    "W": "W",
    "оппозитный двигатель": "BOXER",
}
_CHARGE_TYPE_MAP = {
    "всасывающее устройство": "NATURALLY_ASPIRATED",
    "турбо/нагнетатель": "TURBOCHARGED",
    "турбонагнетатель": "TURBOCHARGED",
    "компрессор": "SUPERCHARGED",
    "битурбо": "TURBOCHARGED",
}
_FUEL_MIXTURE_MAP = {
    "Впрыскивание во впускной коллектор": "PORT_INJECTION",
    "Непосредственный впрыск": "GDI",
    "Карбюратор": "CARBURETOR",
    "Впрыск с форсункой": "PORT_INJECTION",
}
_EMISSION_NORM_RE = re.compile(r"Euro\s*(\d+[a-zA-Z]?|VI)", re.IGNORECASE)


def _norm_euro_tecdoc(raw: str) -> str:
    """Normalize TecDoc EmissionNorm to 'euroN' format."""
    s = raw.strip()
    if not s or s == "-":
        return "unknown"
    m = _EMISSION_NORM_RE.search(s)
    if not m:
        return "unknown"
    tok = m.group(1).upper()
    if tok == "VI":
        return "euro6"
    num = re.match(r"(\d+)", tok)
    if num:
        digit = int(num.group(1))
        return f"euro{min(digit, 6)}"
    return "unknown"


def _try_connect_tecdoc() -> Any | None:
    """Return a mysql.connector connection or None if unavailable."""
    try:
        import mysql.connector
    except ImportError:
        print("mysql.connector not installed — skipping TecDoc extraction.")
        return None

    try:
        conn = mysql.connector.connect(
            host=TECDOC_HOST,
            port=TECDOC_PORT,
            user=TECDOC_USER,
            password=TECDOC_PASS,
            database=TECDOC_DB,
            connection_timeout=10,
        )
        print(f"Connected to TecDoc MySQL at {TECDOC_HOST}:{TECDOC_PORT}")
        return conn
    except Exception as exc:
        print(f"TecDoc MySQL unavailable ({exc}) — building from YAML + CSV only.")
        return None


def _tecdoc_fetch_engine_attributes(
    conn: Any, engine_id: int
) -> dict[str, str]:
    """Fetch EAV attributes for a single engine."""
    cur = conn.cursor()
    cur.execute(
        "SELECT displaytitle, displayvalue FROM engine_attributes WHERE engineid = %s",
        (engine_id,),
    )
    attrs = {}
    for title, value in cur.fetchall():
        if title and value:
            attrs[title.strip()] = value.strip()
    cur.close()
    return attrs


def _tecdoc_fetch_car_attributes(
    conn: Any, car_id: int
) -> dict[str, str]:
    """Fetch EAV attributes for a single passenger car."""
    cur = conn.cursor()
    cur.execute(
        "SELECT displaytitle, displayvalue FROM passanger_car_attributes WHERE passangercarid = %s",
        (car_id,),
    )
    attrs = {}
    for title, value in cur.fetchall():
        if title and value:
            attrs[title.strip()] = value.strip()
    cur.close()
    return attrs


def _tecdoc_check_part_group(conn: Any, car_id: int, assembly_group: str) -> bool:
    """Check if a car has any parts in the given assembly group."""
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM passanger_car_prd"
        " WHERE id = %s AND assemblygroupdescription = %s",
        (car_id, assembly_group),
    )
    count = cur.fetchone()[0]
    cur.close()
    return count > 0


def _tecdoc_has_product(conn: Any, car_id: int, prd_description: str) -> bool:
    """Check if a car has parts matching the given prd.description text."""
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM passanger_car_prd"
        " WHERE id = %s AND description = %s",
        (car_id, prd_description),
    )
    count = cur.fetchone()[0]
    cur.close()
    return count > 0


def _extract_tecdoc(conn: Any, max_engines: int = 0) -> dict[str, dict]:
    """Pull all petrol passenger engines from TecDoc into a dict keyed by engine_code.

    Uses batch queries (3 total) instead of per-engine queries for performance.
    """
    result: dict[str, dict] = {}
    cur = conn.cursor()

    # Phase 1 — find petrol car IDs
    print("Finding petrol passenger cars in TecDoc ...")
    petrol_vals = "','".join(TECDOC_PETROL_RUSSIAN)
    cur.execute(
        f"""SELECT DISTINCT pca.passangercarid
           FROM passanger_car_attributes pca
           WHERE pca.displaytitle IN ('Fuel type', 'Engine type')
             AND pca.displayvalue IN ('{petrol_vals}')"""
    )
    petrol_car_ids = {row[0] for row in cur.fetchall()}
    print(f"  Found {len(petrol_car_ids)} petrol passenger cars.")

    if not petrol_car_ids:
        cur.close()
        print("  WARNING: No petrol cars found in TecDoc — check FuelType/EngineType values.")
        return result

    # Phase 2 — car → engine linkages (with model_id for part lookups)
    print("Fetching car -> engine linkages ...")
    id_list = ",".join(str(cid) for cid in petrol_car_ids)
    cur.execute(
        f"""SELECT pce.id, pce.engineid, m.description, pc.modelid
           FROM passanger_car_engines pce
           JOIN engines e ON pce.engineid = e.id
           JOIN manufacturers m ON e.manufacturerid = m.id
           JOIN passanger_cars pc ON pce.id = pc.id
           WHERE pce.id IN ({id_list})"""
    )
    car_engine_brand = {}
    for car_id, engine_id, brand, model_id in cur.fetchall():
        if car_id not in car_engine_brand:
            car_engine_brand[car_id] = (engine_id, brand.strip().upper() if brand else "UNKNOWN", model_id)

    print(f"  Mapped {len(car_engine_brand)} cars to engines.")

    # Group by engine_id (deduplicate)
    engine_cars: dict[int, list[int]] = defaultdict(list)
    for car_id, (engine_id, _, _model_id) in car_engine_brand.items():
        engine_cars[engine_id].append(car_id)

    all_engine_ids = list(engine_cars.keys())
    print(f"  {len(all_engine_ids)} unique engines across all petrol cars.")

    # Build rep-car lookup: engine_id -> (rep_car_id, rep_model_id, brand)
    engine_rep: dict[int, tuple[int, int, str]] = {}
    all_rep_car_ids = []
    all_model_ids = set()
    for engine_id, car_ids in engine_cars.items():
        rep_car_id = car_ids[0]
        _, brand, model_id = car_engine_brand[rep_car_id]
        engine_rep[engine_id] = (rep_car_id, model_id, brand)
        all_rep_car_ids.append(rep_car_id)
        all_model_ids.add(model_id)

    # Phase 3 — BATCH: fetch all engine_attributes
    print("Batch-fetching engine attributes ...")
    eng_ids_str = ",".join(str(eid) for eid in all_engine_ids)
    cur.execute(
        f"SELECT engineid, displaytitle, displayvalue FROM engine_attributes"
        f" WHERE engineid IN ({eng_ids_str})"
    )
    eng_attrs_all: dict[int, dict[str, str]] = defaultdict(dict)
    for eid, title, value in cur.fetchall():
        if title and value:
            eng_attrs_all[eid][title.strip()] = value.strip()
    print(f"  Fetched attributes for {len(eng_attrs_all)} engines.")

    # Phase 4 — BATCH: fetch all car_attributes for representative cars
    print("Batch-fetching car attributes ...")
    car_ids_str = ",".join(str(cid) for cid in all_rep_car_ids)
    cur.execute(
        f"SELECT passangercarid, displaytitle, displayvalue FROM passanger_car_attributes"
        f" WHERE passangercarid IN ({car_ids_str})"
    )
    car_attrs_all: dict[int, dict[str, str]] = defaultdict(dict)
    for cid, title, value in cur.fetchall():
        if title and value:
            car_attrs_all[cid][title.strip()] = value.strip()
    print(f"  Fetched attributes for {len(car_attrs_all)} cars.")

    # Phase 5 — BATCH: fetch all PRD entries for relevant model IDs
    print("Batch-fetching part data (PRD) ...")
    model_ids_str = ",".join(str(mid) for mid in all_model_ids)
    cur.execute(
        f"SELECT id, assemblygroupdescription, description FROM passanger_car_prd"
        f" WHERE id IN ({model_ids_str})"
    )
    prd_by_model: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for mid, ag, desc in cur.fetchall():
        prd_by_model[mid].append((ag or "", desc or ""))
    prd_models = len(prd_by_model)
    print(f"  Fetched PRD entries for {prd_models} models (of {len(all_model_ids)} relevant).")

    cur.close()

    # Phase 6 — process engines in-memory (no DB calls)
    processed = 0
    for engine_id in all_engine_ids:
        rep_car_id, rep_model_id, brand = engine_rep[engine_id]
        eng_attrs = eng_attrs_all.get(engine_id, {})
        car_attrs = car_attrs_all.get(rep_car_id, {})

        # Fuel type gate (double-check petrol)
        fuel_type_val = car_attrs.get("Fuel type", "")
        engine_type_val = car_attrs.get("Engine type", "")
        if (
            "дизель" in fuel_type_val.lower()
            or "дизель" in engine_type_val.lower()
        ):
            continue

        # --- Extract key fields ---

        # Displacement
        displ_raw = car_attrs.get("Capacity (technic)", "")
        if not displ_raw:
            displ_raw = eng_attrs.get("Capacity", "")
        displacement_cc = 0
        if displ_raw:
            m = re.search(r"(\d+)", displ_raw.replace(" ", ""))
            if m:
                displacement_cc = int(m.group(1))

        # Engine construction
        eng_constr = eng_attrs.get("EngineConstruction", "")
        is_v_engine = False
        if "V" in eng_constr or "VR" in eng_constr or "W" in eng_constr:
            is_v_engine = True

        # Induction type
        charge_type = eng_attrs.get("ChargeType", "")
        induction_type = ""
        for ru, en in _CHARGE_TYPE_MAP.items():
            if ru in charge_type:
                induction_type = en
                break

        # Fuel delivery
        fuel_mixture = car_attrs.get("Fuel mixture", "")
        if not fuel_mixture:
            fuel_mixture = eng_attrs.get("FuelMixture", "")
        fuel_delivery_type = ""
        for ru, en in _FUEL_MIXTURE_MAP.items():
            if ru in fuel_mixture:
                fuel_delivery_type = en
                break

        # Euro norm
        euro_raw = eng_attrs.get("EmissionNorm", "")
        euro_norm = _norm_euro_tecdoc(euro_raw) if euro_raw else "unknown"

        # Valvetrain
        valve_mgmt = eng_attrs.get("ValveManagement", "")
        cyl_constr = eng_attrs.get("CylinderConstruction", "")
        has_vvt = False
        if "DOHC" in cyl_constr or "гидравлический" in valve_mgmt:
            has_vvt = True
        valvetrain_type = valve_mgmt if valve_mgmt else ""

        # Model year range
        my_start, my_end = 2000, 2010
        if euro_norm == "euro1":
            my_start, my_end = 1992, 1996
        elif euro_norm == "euro2":
            my_start, my_end = 1996, 2000
        elif euro_norm == "euro3":
            my_start, my_end = 2000, 2005
        elif euro_norm == "euro4":
            my_start, my_end = 2005, 2010
        elif euro_norm == "euro5":
            my_start, my_end = 2009, 2015
        elif euro_norm == "euro6":
            my_start, my_end = 2014, 2020

        # Part-level lookups (via model_id)
        prd_entries = prd_by_model.get(rep_model_id, [])
        prd_ag_set = {ag for ag, _ in prd_entries}
        prd_desc_set = {desc for _, desc in prd_entries}

        has_egr = "Рециркуляция ОГ" in prd_ag_set
        has_maf = "Приготовление смеси" in prd_ag_set
        has_map = "Датчик, давление наддува" in prd_desc_set

        # O2 type
        o2_type = "NB"
        if has_egr and euro_norm in ("euro4", "euro5", "euro6"):
            o2_type = "WB"

        # Synthetic engine_code
        displ_str = str(displacement_cc) if displacement_cc > 0 else "UNK"
        ind_str = "NA"
        if induction_type == "TURBOCHARGED":
            ind_str = "T"
        elif induction_type == "SUPERCHARGED":
            ind_str = "S"
        fuel_str = ""
        if fuel_delivery_type == "GDI":
            fuel_str = "_GDI"
        engine_code = f"{brand}_{displ_str}cc_{ind_str}{fuel_str}_TecDoc_{engine_id}"

        result[engine_code] = {
            "engine_code": engine_code,
            "brand": brand,
            "displacement_cc": displacement_cc,
            "euro_norm": euro_norm,
            "my_start": my_start,
            "my_end": my_end,
            "era_bucket": _derive_era(my_start, my_end),
            "has_vvt": has_vvt,
            "has_gdi": fuel_delivery_type == "GDI",
            "has_turbo": induction_type == "TURBOCHARGED",
            "is_v_engine": is_v_engine,
            "has_egr": has_egr,
            "has_maf": has_maf,
            "has_map": has_map,
            "o2_type": o2_type,
            "induction_type": induction_type,
            "fuel_delivery_type": fuel_delivery_type,
            "valvetrain_type": valvetrain_type,
            "_source": "tecdoc",
        }

        processed += 1
        if processed % 100 == 0:
            print(f"  Processed {processed} engines ...")
        if max_engines > 0 and processed >= max_engines:
            print(f"  Reached --max-engines limit ({max_engines}); stopping extraction early.")
            break

    maf_confirmed = sum(1 for e in result.values() if e.get("has_maf"))
    map_confirmed = sum(1 for e in result.values() if e.get("has_map"))
    print(f"  Extracted {len(result)} engine entries from TecDoc.")
    print(f"  has_maf confirmed: {maf_confirmed}  has_map confirmed: {map_confirmed}")
    return result


# ---------------------------------------------------------------------------
# YAML loading and merge
# ---------------------------------------------------------------------------
def _load_yaml_entries(path: Path) -> dict[str, dict]:
    """Load YAML overrides into a dict keyed by engine_code."""
    entries = _load_overrides(path)
    result: dict[str, dict] = {}
    for e in entries:
        ec = str(e.get("engine_code", ""))
        if not ec:
            continue
        fuel = str(e.get("fuel_type", "petrol")).lower()
        if fuel not in PETROL_FUEL_TYPES:
            print(f"  Skipping non-petrol YAML entry: {ec} (fuel_type={fuel})")
            continue

        result[ec] = {
            "engine_code": ec,
            "brand": str(e.get("brand", "")).upper(),
            "displacement_cc": int(e.get("displacement_cc", 0)),
            "euro_norm": str(e.get("euro_norm", "unknown")),
            "my_start": int(e.get("my_start", 2000)),
            "my_end": int(e.get("my_end", 2010)),
            "era_bucket": str(e.get("era_bucket", "")),
            "has_vvt": bool(e.get("has_vvt", False)),
            "has_gdi": bool(e.get("has_gdi", False)),
            "has_turbo": bool(e.get("has_turbo", False)),
            "is_v_engine": bool(e.get("is_v_engine", False)),
            "has_egr": bool(e.get("has_egr", False)),
            "has_maf": bool(e.get("has_maf", False)),
            "has_map": bool(e.get("has_map", False)),
            "o2_type": str(e.get("o2_type", "NB")),
            "induction_type": (
                "TURBOCHARGED" if e.get("has_turbo")
                else "SUPERCHARGED" if False  # YAML doesn't distinguish
                else "NATURALLY_ASPIRATED"
            ),
            "fuel_delivery_type": (
                "GDI" if e.get("has_gdi") else "PORT_INJECTION"
            ),
            "valvetrain_type": "",
            "rated_rpm": _safe_int(e.get("rated_rpm", "")),
            "target_rpm_u2": int(e.get("target_rpm_u2", 2500)),
            "target_lambda_v112": float(e.get("target_lambda_v112", 1.000)),
            "idle_rpm_low": _safe_int(e.get("idle_rpm_low", "")),
            "co_low_idle": _safe_float(e.get("co_low_idle", "")),
            "co_high_idle": _safe_float(e.get("co_high_idle", "")),
            "co_type_approval": _safe_float(e.get("co_type_approval", "")),
            "hc_type_approval": _safe_float(e.get("hc_type_approval", "")),
            "nox_type_approval": _safe_float(e.get("nox_type_approval", "")),
            "hc_nox_type_approval": _safe_float(
                e.get("hc_nox_type_approval", "")
            ),
            "co2_type_approval": _safe_float(e.get("co2_type_approval", "")),
            "noise_stationary_dba": _safe_float(
                e.get("noise_stationary_dba", "")
            ),
            "noise_rpm": _safe_int(e.get("noise_rpm", "")),
            "noise_driving_dba": _safe_float(
                e.get("noise_driving_dba", "")
            ),
            "_source": "yaml",
        }
    return result


def _merge_tecdoc_into_yaml(
    yaml_entries: dict[str, dict],
    tecdoc_entries: dict[str, dict],
) -> dict[str, dict]:
    """Merge TecDoc entries into YAML entries by brand+displacement+euro matching.

    For matched entries: TecDoc tech-mask flags win. YAML keeps its engine_code.
    Unmatched TecDoc entries are added with their synthetic engine_code.
    Unmatched YAML entries stay as-is.
    """
    conflicts = 0

    # Build a lookup for TecDoc entries keyed by (brand, displ_bucket, euro)
    tecdoc_lookup: dict[tuple, list[dict]] = defaultdict(list)
    for ec, entry in tecdoc_entries.items():
        brand = str(entry["brand"]).upper()
        displ = int(entry.get("displacement_cc", 0))
        displ_bucket = round(displ / 100) * 100
        euro = str(entry.get("euro_norm", "unknown"))
        tecdoc_lookup[(brand, displ_bucket, euro)].append(entry)

    # Try to match each YAML entry to a TecDoc entry
    matched_tecdoc = set()
    for yaml_ec, y_entry in yaml_entries.items():
        brand = str(y_entry["brand"]).upper()
        displ = int(y_entry.get("displacement_cc", 0))
        displ_bucket = round(displ / 100) * 100
        euro = str(y_entry.get("euro_norm", "unknown"))
        key = (brand, displ_bucket, euro)

        if key in tecdoc_lookup and tecdoc_lookup[key]:
            t_entry = tecdoc_lookup[key][0]
            # TecDoc wins on tech-mask flags; YAML keeps engine_code
            for flag in (
                "has_vvt", "has_gdi", "has_turbo", "is_v_engine",
                "has_egr", "has_maf", "has_map", "o2_type",
                "induction_type", "fuel_delivery_type", "valvetrain_type",
            ):
                if t_entry.get(flag):
                    y_entry[flag] = t_entry[flag]
            # Update measurements from TecDoc if YAML has 0/default
            if y_entry.get("displacement_cc", 0) == 0 and t_entry.get("displacement_cc", 0) > 0:
                y_entry["displacement_cc"] = t_entry["displacement_cc"]
            if t_entry.get("euro_norm", "unknown") != "unknown" and y_entry.get("euro_norm", "unknown") == "unknown":
                y_entry["euro_norm"] = t_entry["euro_norm"]
            y_entry["_source"] = "yaml+tecdoc"
            conflicts += 1
            matched_tecdoc.add(ec_for_entry(t_entry))

    # Add unmatched TecDoc entries
    added = 0
    for ec, t_entry in tecdoc_entries.items():
        if ec not in matched_tecdoc:
            yaml_entries[ec] = t_entry
            added += 1

    if added:
        print(f"  Added {added} unmatched TecDoc entries to engine_ref.")
    print(f"  TecDoc->YAML merges: {conflicts} (TecDoc tech-mask flags won).")
    return yaml_entries


def ec_for_entry(entry: dict) -> str:
    return str(entry.get("engine_code", ""))


# ---------------------------------------------------------------------------
# CSV CoC enrichment (source: v2 _try_enrich_from_opsi, adapted for VINLab)
# ---------------------------------------------------------------------------
_EURO_RE = re.compile(r"EURO\s*(\d+[a-zA-Z]?|VI)", re.IGNORECASE)


def _norm_euro_csv(raw: str) -> str:
    """Normalize CSV V9_euro_class_full or euro_label to 'euroN' format."""
    s = str(raw).strip()
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


def _enrich_from_csv(entries: dict[str, dict]) -> None:
    """Stream petrol CSV, compute CoC medians per (brand, displ_bucket, euro)
    bucket, and update matching engine_ref entries."""
    if not PETROL_CSV.exists():
        print(f"Petrol CSV not found at {PETROL_CSV} — skipping CoC enrichment.")
        return

    print(f"Streaming {PETROL_CSV.name} for CoC enrichment ...")

    # Collect values per bucket, plus exact engine-code rated RPM.
    groups: dict[tuple, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    rated_rpm_by_engine: dict[str, list[float]] = defaultdict(list)

    with open(PETROL_CSV, encoding=CSV_ENCODING) as fh:
        reader = csv.DictReader(fh, delimiter=";")
        row_count = 0
        for row in reader:
            # Petrol-only gate
            fuel_code = (row.get("P13_fuel_code", "") or "").strip()
            if fuel_code != "P":
                continue

            brand = (row.get("D1_make", "") or "").strip().upper()
            if not brand:
                continue

            # Displacement
            cc_raw = row.get("P11_displacement_cc", "")
            try:
                displ_cc = int(float(str(cc_raw).replace(",", ".")))
            except (TypeError, ValueError):
                continue
            displ_bucket = round(displ_cc / 100) * 100

            # Euro norm: prefer euro_label, fall back to V9
            euro_raw = row.get("euro_label", "")
            if not euro_raw or euro_raw.strip() in ("", "-"):
                euro_raw = row.get("V9_euro_class_full", "")
            euro = _norm_euro_csv(euro_raw)

            key = (brand, displ_bucket, euro)

            engine_code = (row.get("P15_engine_code", "") or "").strip()
            rated_rpm = _safe_float(row.get("P14_rated_rpm", ""))
            if engine_code and rated_rpm is not None and 0 < rated_rpm < 100000:
                rated_rpm_by_engine[engine_code].append(rated_rpm)

            # Collect all CoC measurements
            csv_fields = {
                "target_lambda_v112": "V112_lambda",
                "target_rpm_u2": "V11_idle_rpm_high",
                "idle_rpm_low": "V10_idle_rpm_low",
                "co_low_idle": "V101_CO_low_idle",
                "co_high_idle": "V111_CO_high_idle",
                "co_type_approval": "V1_CO",
                "hc_type_approval": "V2_HC",
                "nox_type_approval": "V3_NOx",
                "hc_nox_type_approval": "V4_HC_NOx",
                "co2_type_approval": "V7_CO2",
                "noise_stationary_dba": "U1_noise_stationary_dBA",
                "noise_rpm": "U2_noise_rpm",
                "noise_driving_dba": "U3_noise_driving_dBA",
            }

            for field_name, csv_col in csv_fields.items():
                raw = row.get(csv_col, "")
                v = _safe_float(raw)
                if v is not None and 0 < v < 100000:
                    groups[key][field_name].append(v)

            row_count += 1
            if row_count % 50000 == 0:
                print(f"  Streamed {row_count} rows ...")

    print(f"  Streamed {row_count} petrol rows, {len(groups)} unique buckets.")

    # Enrich entries
    enriched = 0
    enriched_fields: dict[str, int] = defaultdict(int)
    for ec, entry in entries.items():
        rated_vals = rated_rpm_by_engine.get(str(ec), [])
        if rated_vals:
            entry["rated_rpm"] = int(round(_median(rated_vals)))
            enriched_fields["rated_rpm"] += 1
            enriched += 1

        brand = str(entry.get("brand", "")).upper()
        displ = int(entry.get("displacement_cc", 0))
        displ_bucket = round(displ / 100) * 100
        euro = str(entry.get("euro_norm", "unknown"))
        key = (brand, displ_bucket, euro)

        if key not in groups:
            continue

        bucket = groups[key]
        for field_name in (
            "target_lambda_v112", "target_rpm_u2", "idle_rpm_low",
            "co_low_idle", "co_high_idle", "co_type_approval",
            "hc_type_approval", "nox_type_approval", "hc_nox_type_approval",
            "co2_type_approval", "noise_stationary_dba", "noise_rpm",
            "noise_driving_dba",
        ):
            vals = bucket.get(field_name, [])
            if vals:
                # CSV medians override YAML defaults when real data exists
                if field_name in ("target_rpm_u2", "idle_rpm_low", "noise_rpm"):
                    entry[field_name] = int(round(_median(vals)))
                else:
                    entry[field_name] = round(float(_median(vals)), 3)
                enriched_fields[field_name] += 1
                enriched += 1

    if enriched:
        print(f"  CoC enrichment: {enriched} field values set across {len(entries)} entries.")
        for fname, count in sorted(enriched_fields.items()):
            print(f"    {fname}: {count} entries enriched")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Run TecDoc extraction only; do not write vref.db")
    parser.add_argument("--max-engines", type=int, default=0,
                        help="Limit TecDoc engines processed (0 = unlimited, for testing)")
    args = parser.parse_args()

    # 1. Load YAML overrides (always available — shipped with the repo)
    print(f"Loading manual overrides from {OVERRIDES_YAML} ...")
    if not OVERRIDES_YAML.exists():
        print(f"ERROR: {OVERRIDES_YAML} not found.")
        raise SystemExit(1)

    yaml_entries = _load_yaml_entries(OVERRIDES_YAML)
    print(f"Loaded {len(yaml_entries)} petrol engine codes from YAML.")

    # 2. Try TecDoc extraction
    conn = _try_connect_tecdoc()
    tecdoc_entries: dict[str, dict] = {}
    if conn is not None:
        try:
            tecdoc_entries = _extract_tecdoc(conn, max_engines=args.max_engines)
        except Exception as exc:
            print(f"TecDoc extraction failed ({exc}) — continuing with YAML only.")
        finally:
            conn.close()

    # 3. Merge TecDoc into YAML
    if tecdoc_entries:
        all_entries = _merge_tecdoc_into_yaml(yaml_entries, tecdoc_entries)
    else:
        all_entries = yaml_entries

    # 4. Derive era_bucket for entries missing it
    for entry in all_entries.values():
        if not entry.get("era_bucket"):
            my_start = int(entry.get("my_start", 2000))
            my_end = int(entry.get("my_end", 2010))
            entry["era_bucket"] = _derive_era(my_start, my_end)

    # 5. CSV CoC enrichment
    _enrich_from_csv(all_entries)

    # 6. Sort entries by engine_code for idempotent output
    sorted_entries = sorted(all_entries.values(), key=lambda e: str(e.get("engine_code", "")))

    if args.dry_run:
        print(f"\nDry-run: {len(sorted_entries)} entries prepared. DB write skipped.")
        return

    # 7. Create output directory; delete old DB for a fresh start
    out_dir = OUT_DB.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    if OUT_DB.exists():
        OUT_DB.unlink()

    conn_db = sqlite3.connect(str(OUT_DB))
    conn_db.execute("PRAGMA journal_mode=OFF")
    conn_db.execute("PRAGMA page_size=4096")
    conn_db.executescript(CREATE_ENGINE_REF)

    # Schema migration guard — adds columns to existing DBs without them
    for col, defn in [("has_maf", "INTEGER NOT NULL DEFAULT 0"),
                      ("has_map", "INTEGER NOT NULL DEFAULT 0")]:
        try:
            conn_db.execute(f"ALTER TABLE engine_ref ADD COLUMN {col} {defn}")
        except sqlite3.OperationalError:
            pass  # column already exists

    # 8. Insert rows
    inserted = 0
    for e in sorted_entries:
        ec = str(e.get("engine_code", ""))
        if not ec:
            continue

        brand = str(e.get("brand", "")).upper()
        displ_cc_val = int(e.get("displacement_cc", 0))
        displ_cc: int | None = displ_cc_val if displ_cc_val > 0 else None
        euro = str(e.get("euro_norm", "unknown"))
        euro_norm: str | None = euro if euro != "unknown" else None
        my_start = int(e.get("my_start", 2000))
        my_end = int(e.get("my_end", 2010))
        era_bucket = str(e.get("era_bucket", _derive_era(my_start, my_end)))

        row = (
            ec,
            brand,
            displ_cc,
            euro_norm,
            my_start,
            my_end,
            era_bucket,
            _bool_to_int(bool(e.get("has_vvt", False))),
            _bool_to_int(bool(e.get("has_gdi", False))),
            _bool_to_int(bool(e.get("has_turbo", False))),
            _bool_to_int(bool(e.get("is_v_engine", False))),
            _bool_to_int(bool(e.get("has_egr", False))),
            _bool_to_int(bool(e.get("has_maf", False))),
            _bool_to_int(bool(e.get("has_map", False))),
            str(e.get("o2_type", "NB")),
            str(e.get("induction_type", "")) or None,
            str(e.get("fuel_delivery_type", "")) or None,
            str(e.get("valvetrain_type", "")) or None,
            e.get("rated_rpm"),
            e.get("target_lambda_v112"),
            e.get("target_rpm_u2"),
            e.get("idle_rpm_low"),
            e.get("co_low_idle"),
            e.get("co_high_idle"),
            e.get("co_type_approval"),
            e.get("hc_type_approval"),
            e.get("nox_type_approval"),
            e.get("hc_nox_type_approval"),
            e.get("co2_type_approval"),
            e.get("noise_stationary_dba"),
            e.get("noise_rpm"),
            e.get("noise_driving_dba"),
        )
        conn_db.execute(INSERT_ROW, row)
        inserted += 1

    conn_db.commit()

    # 9. Report
    count = conn_db.execute("SELECT COUNT(*) FROM engine_ref").fetchone()[0]
    coc_count = conn_db.execute(
        "SELECT COUNT(*) FROM engine_ref WHERE target_lambda_v112 IS NOT NULL"
    ).fetchone()[0]
    print(f"\nWrote {count} rows to {OUT_DB}")
    print(f"  Rows with CoC enrichment: {coc_count}")
    print(f"  Sources: YAML={sum(1 for e in sorted_entries if 'yaml' in str(e.get('_source','')))}, "
          f"TecDoc={sum(1 for e in sorted_entries if 'tecdoc' in str(e.get('_source','')))}")

    # Quick sanity
    sample = conn_db.execute(
        "SELECT engine_code, brand, era_bucket, has_vvt, has_gdi, has_turbo, "
        "target_lambda_v112, target_rpm_u2 "
        "FROM engine_ref ORDER BY engine_code LIMIT 5"
    ).fetchall()
    print("\nSample rows:")
    for s in sample:
        print(
            f"  {s[0]:35s} {s[1]:15s} {s[2]:20s} "
            f"vvt={s[3]} gdi={s[4]} turbo={s[5]} "
            f"lambda={s[6]} rpm={s[7]}"
        )

    conn_db.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
