"""
tools/tecdoc_hardware_enricher.py
Enriches vref.db with engine hardware attributes from TecDoc.

INPUT:  vehicle-data/ktype_bridge_map.csv
        vinlab/data/vref.db
OUTPUT: vinlab/data/vref.db  (INSERT new engine rows only)

Attributes queried from TecDoc engine_attributes:
- ChargeType      → has_turbo   (Russian values mapped per schema_map.md)
- FuelMixture     → has_gdi     ('Непосредственный впрыск' = GDI)
- ValveManagement → has_vvt, valvetrain_type

Gaps (documented in schema_map.md):
- No LINK_PT_VEH → cannot detect MAF vs MAP (induction_type stays NULL)
- No ENGINE_CRITERIA → VVT detection from ValveManagement text only
- ValveManagement values describe mechanical actuation (rocker/bucket/hydraulic),
  not variable timing, so has_vvt will be 0 for most engines.

Rules:
- Only INSERT rows for engine_codes NOT currently in vref.db (H4 read-only MySQL).
- Never overwrite existing vref.db rows.
- All CoC measurement fields default to NULL (decoder handles NULL gracefully).
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

import mysql.connector

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
BRIDGE_CSV = ROOT.parent.parent.parent / "vehicle-data" / "ktype_bridge_map.csv"
VREF_DB = ROOT / "vinlab" / "data" / "vref.db"

# ---------------------------------------------------------------------------
# MySQL connection
# ---------------------------------------------------------------------------

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "tecdoc"


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connection_timeout=10,
    )


# ---------------------------------------------------------------------------
# attribute mappings (Russian → DNALab)
# ---------------------------------------------------------------------------

# ChargeType values that indicate forced induction (→ has_turbo=True).
# Everything else is treated as naturally aspirated.
TURBO_VALUES: set[str] = {
    "компрессор",
    "турбо",
    "нагнетаемый",
    "G - нагнетатель",
    "Турбонагнетатель",
    "турбо/охладитель нагнетаем.воздуха",
    "Турбокомпрессор / компрессор",
    "Сист. надува ДВС с 2 парал.включ. турбонагн./охлад. нагн.воз",
}

# FuelMixture values indicating direct injection (→ has_gdi=True).
GDI_VALUES: set[str] = {
    "Непосредственный впрыск",
    "Впрыскивание во впускной коллектор / прямое впрыскивание",
}

# ValveManagement → valvetrain_type enum (from schema_map.md VALVE_MAP).
VALVETRAIN_MAP: dict[str, str] = {
    "Коромысло": "ROCKER",
    "тяговое коромысло": "ROCKER",
    "тарельчатый толкатель": "BUCKET_TAPPET",
    "для двигателей с гидравлическими толкателями": "HYDRAULIC_TAPPET",
}

# VVT detection keywords — searched case-insensitively in ValveManagement text.
# Includes OEM brand names and Russian terms for variable timing.
VVT_KEYWORDS: list[str] = [
    "VVT", "V-TEC", "VTEC", "VANOS", "VALVETRONIC", "VALVEMATIC",
    "CVVT", "DVVT", "VVTI", "VTC", "MIVEC", "AVCS", "S-VT",
    "VTI", "VVL", "VVTL", "VVEL", "MULTIAIR", "TI-VCT", "VCT",
    "регулировка фаз", "изменяемый", "переменный",
    "изменение фаз", "регулируемый",
]


def is_turbo(charge_type: str) -> bool:
    return charge_type in TURBO_VALUES


def is_gdi(fuel_mixture: str) -> bool:
    return fuel_mixture in GDI_VALUES


def detect_vvt(valve_mgmt: str) -> bool:
    upper = valve_mgmt.upper()
    return any(kw.upper() in upper for kw in VVT_KEYWORDS)


def map_valvetrain(valve_mgmt: str) -> str | None:
    return VALVETRAIN_MAP.get(valve_mgmt)


# ---------------------------------------------------------------------------
# vref.db helpers
# ---------------------------------------------------------------------------


def get_existing_engine_codes() -> set[str]:
    """Return set of engine_codes already in vref.db engine_ref table."""
    conn = sqlite3.connect(str(VREF_DB))
    cur = conn.cursor()
    cur.execute("SELECT engine_code FROM engine_ref")
    codes = {row[0] for row in cur.fetchall()}
    conn.close()
    return codes


def insert_engine_row(
    db_path: Path,
    engine_code: str,
    brand: str,
    hardware: dict,
    dry_run: bool,
) -> bool:
    """Insert a new engine row into vref.db. Returns True on success."""
    if dry_run:
        return True

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO engine_ref (
            engine_code, brand,
            has_vvt, has_gdi, has_turbo,
            is_v_engine, has_egr,
            o2_type, induction_type, fuel_delivery_type, valvetrain_type,
            displacement_cc, euro_norm, era_bucket,
            my_start, my_end,
            target_lambda_v112, target_rpm_u2, idle_rpm_low,
            co_low_idle, co_high_idle, co_type_approval,
            hc_type_approval, nox_type_approval, hc_nox_type_approval,
            co2_type_approval, noise_stationary_dba, noise_rpm, noise_driving_dba
        ) VALUES (
            ?, ?,
            ?, ?, ?,
            0, 0,
            'NB', ?, ?, ?,
            NULL, NULL, 'OBD_STD',
            NULL, NULL,
            NULL, NULL, NULL,
            NULL, NULL, NULL,
            NULL, NULL, NULL,
            NULL, NULL, NULL, NULL
        )
        """,
        (
            engine_code,
            brand,
            1 if hardware.get("has_vvt") else 0,
            1 if hardware.get("has_gdi") else 0,
            1 if hardware.get("has_turbo") else 0,
            hardware.get("induction_type"),
            hardware.get("fuel_delivery_type"),
            hardware.get("valvetrain_type"),
        ),
    )
    conn.commit()
    conn.close()
    return True


# ---------------------------------------------------------------------------
# TecDoc query
# ---------------------------------------------------------------------------


def query_hardware_attributes(
    cur, tecdoc_engine_id: int
) -> dict:
    """Query TecDoc engine_attributes for hardware flags.

    Returns a dict with keys matching vref.db columns:
      has_vvt, has_gdi, has_turbo, induction_type,
      fuel_delivery_type, valvetrain_type
    """
    cur.execute(
        """
        SELECT attributetype, displayvalue
        FROM engine_attributes
        WHERE engineid = %s
          AND attributetype IN ('ChargeType', 'FuelMixture', 'ValveManagement')
        """,
        (tecdoc_engine_id,),
    )

    has_turbo = False
    has_gdi = False
    has_vvt = False
    valvetrain_type = None

    for atype, aval in cur.fetchall():
        if atype == "ChargeType":
            has_turbo = is_turbo(aval)
        elif atype == "FuelMixture":
            has_gdi = is_gdi(aval)
        elif atype == "ValveManagement":
            has_vvt = detect_vvt(aval)
            valvetrain_type = map_valvetrain(aval)

    return {
        "has_vvt": has_vvt,
        "has_gdi": has_gdi,
        "has_turbo": has_turbo,
        "induction_type": None,       # cannot determine MAF vs MAP without LINK_PT_VEH
        "fuel_delivery_type": "GDI" if has_gdi else None,
        "valvetrain_type": valvetrain_type,
    }


def verify_inserted(cur, engine_code: str) -> bool:
    """Verify a row exists in vref.db for the given engine_code."""
    cur.execute(
        "SELECT engine_code, has_turbo, has_gdi, has_vvt FROM engine_ref WHERE engine_code = ?",
        (engine_code,),
    )
    return cur.fetchone() is not None


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="T-TD-4: Enrich vref.db with TecDoc hardware attributes"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print proposed changes, do not write vref.db",
    )
    args = parser.parse_args()

    # 1. Load ktype_bridge_map.csv
    if not BRIDGE_CSV.exists():
        print(f"ERROR: {BRIDGE_CSV} not found")
        sys.exit(1)

    bridge_rows: list[dict] = []
    with open(BRIDGE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        bridge_rows = list(reader)

    if not bridge_rows:
        print("ktype_bridge_map.csv is empty — no engine codes to enrich.")
        print("Engine codes checked:   0")
        print("Already in vref.db:     0 (skipped)")
        print("MAF confirmed:          0")
        print("MAP confirmed:          0")
        print("DUAL confirmed:         0")
        print("VVT confirmed:          0")
        print("vref.db rows upserted:  0")
        return

    # 2. Collect unique engine codes from bridge (petrol-only already enforced by T-TD-2)
    existing_codes = get_existing_engine_codes()

    # Deduplicate by engine_code
    seen: dict[str, dict] = {}
    for row in bridge_rows:
        code = row.get("tecdoc_engine_code", "").strip()
        if not code:
            continue
        if code not in seen:
            seen[code] = {
                "engine_code": code,
                "tecdoc_engine_id": int(row["tecdoc_engine_id"]),
                "brand": row.get("brand", "").strip(),
            }

    unique_entries = list(seen.values())
    print(f"ktype_bridge_map rows:          {len(bridge_rows)}")
    print(f"Unique engine codes to check:   {len(unique_entries)}")
    print(f"Already in vref.db:             {len([e for e in unique_entries if e['engine_code'] in existing_codes])} (will skip)")

    # 3. Query TecDoc for hardware attributes
    stats = {
        "checked": 0,
        "already_in_vref": 0,
        "maf": 0,
        "map": 0,
        "dual": 0,
        "vvt": 0,
        "upserted": 0,
    }

    proposed: list[dict] = []

    db = get_connection()
    cur = db.cursor()

    for entry in unique_entries:
        code = entry["engine_code"]
        stats["checked"] += 1

        if code in existing_codes:
            stats["already_in_vref"] += 1
            continue

        hardware = query_hardware_attributes(cur, entry["tecdoc_engine_id"])

        # Tally confirmed values
        if hardware["has_vvt"]:
            stats["vvt"] += 1

        # induction_type is always None (no LINK_PT_VEH) so MAF/MAP/DUAL stay 0
        induction = hardware.get("induction_type")
        if induction == "MAF":
            stats["maf"] += 1
        elif induction == "MAP":
            stats["map"] += 1
        elif induction == "DUAL_MAF_MAP":
            stats["dual"] += 1

        proposed.append({**entry, "hardware": hardware})

    cur.close()
    db.close()

    # 4. Write or dry-run
    if args.dry_run:
        print("\nDRY RUN — no writes to vref.db")
        if proposed:
            print(f"Proposed upserts ({len(proposed)}):")
            for p in proposed:
                h = p["hardware"]
                print(
                    f"  {p['engine_code']:20s} turbo={h['has_turbo']} "
                    f"gdi={h['has_gdi']} vvt={h['has_vvt']} "
                    f"valvetrain={h['valvetrain_type']} brand={p['brand']}"
                )
        else:
            print("  (none — all engine codes already in vref.db)")
    else:
        for p in proposed:
            ok = insert_engine_row(VREF_DB, p["engine_code"], p["brand"], p["hardware"], dry_run=False)
            if ok:
                stats["upserted"] += 1

        # Verify each upserted row
        if stats["upserted"] > 0:
            conn = sqlite3.connect(str(VREF_DB))
            conn.row_factory = sqlite3.Row
            vcur = conn.cursor()
            verified = 0
            for p in proposed:
                if verify_inserted(vcur, p["engine_code"]):
                    verified += 1
            conn.close()
            print(f"Post-write verification:        {verified}/{stats['upserted']} rows confirmed")
            assert verified == stats["upserted"], (
                f"Verification mismatch: {verified} confirmed vs {stats['upserted']} upserted"
            )

    # 5. Print stats
    print(f"\nEngine codes checked:   {stats['checked']}")
    print(f"Already in vref.db:     {stats['already_in_vref']} (skipped)")
    print(f"MAF confirmed:          {stats['maf']}")
    print(f"MAP confirmed:          {stats['map']}")
    print(f"DUAL confirmed:         {stats['dual']}")
    print(f"VVT confirmed:          {stats['vvt']}")
    print(f"vref.db rows upserted:  {stats['upserted']}")


if __name__ == "__main__":
    main()
