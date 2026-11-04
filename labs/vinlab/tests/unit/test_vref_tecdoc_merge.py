"""Tests for tools/merge_tecdoc_extract.py (T-VINA-13b; G1, G2 and the coalesce rule: T-VINA-14).

Each test merges into a temporary vref.db in its pre-T-VINA-13b state: the
shipped engine_ref rows minus those the merge added, in the schema shipped
before the merge. The rule tests use a small fixture extract and engine map
under tmp_path; the decode test uses the real extract and engine map.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest

from vinlab.decoder import RobustVINDecoder

TOOL = Path(__file__).resolve().parents[2] / "tools" / "merge_tecdoc_extract.py"

EXTRACT_HEADER = [
    "brand", "engine_code", "match_tier", "status", "tecdoc_engine_ids", "tecdoc_description",
    "displacement_cc", "cylinder_count", "fuel_delivery_type", "induction_type", "has_turbo", "has_gdi",
    "is_v_engine", "valvetrain_type", "euro_norm", "my_start", "my_end", "n_cars",
]
MAP_HEADER = [
    "brand", "vds_full", "pos_8_only", "engine_code", "engine_displacement", "cylinder_count",
    "engine_configuration", "fuel_system_type", "majority_share",
]
COC_COLUMNS = (
    "rated_rpm", "target_lambda_v112", "target_rpm_u2", "idle_rpm_low", "co_low_idle", "co_high_idle",
    "co_type_approval", "hc_type_approval", "nox_type_approval", "hc_nox_type_approval", "co2_type_approval",
    "noise_stationary_dba", "noise_rpm", "noise_driving_dba",
)
# A real VIN that gains a row: Opel X10XE, model year 1999; the map says 1.4 L, TecDoc says 973 cc.
REAL_VIN = "W0L0SBF08X4314007"
# engine_ref as shipped before T-VINA-13b (base 11dfa95): has_maf/has_map NOT NULL DEFAULT 0, rated_rpm last.
PRE_MERGE_DDL = """\
CREATE TABLE engine_ref (
    engine_code TEXT PRIMARY KEY, brand TEXT NOT NULL, displacement_cc INTEGER, euro_norm TEXT,
    my_start INTEGER, my_end INTEGER, era_bucket TEXT NOT NULL,
    has_vvt INTEGER NOT NULL DEFAULT 0, has_gdi INTEGER NOT NULL DEFAULT 0, has_turbo INTEGER NOT NULL DEFAULT 0,
    is_v_engine INTEGER NOT NULL DEFAULT 0, has_egr INTEGER NOT NULL DEFAULT 0,
    has_maf INTEGER NOT NULL DEFAULT 0, has_map INTEGER NOT NULL DEFAULT 0,
    o2_type TEXT NOT NULL DEFAULT 'NB', induction_type TEXT, fuel_delivery_type TEXT, valvetrain_type TEXT,
    target_lambda_v112 REAL, target_rpm_u2 INTEGER, idle_rpm_low INTEGER, co_low_idle REAL, co_high_idle REAL,
    co_type_approval REAL, hc_type_approval REAL, nox_type_approval REAL, hc_nox_type_approval REAL,
    co2_type_approval REAL, noise_stationary_dba REAL, noise_rpm INTEGER, noise_driving_dba REAL,
    rated_rpm integer
);
CREATE INDEX idx_engine_ref_brand ON engine_ref(brand, displacement_cc, euro_norm);
"""
# The merge writes o2_type '' on every row it adds; the 72 shipped rows carry NB or WB.
COPY_PRE_MERGE_ROWS = (
    "INSERT INTO engine_ref (engine_code, brand, displacement_cc, euro_norm, my_start, my_end, era_bucket, "
    "has_vvt, has_gdi, has_turbo, is_v_engine, has_egr, has_maf, has_map, o2_type, induction_type, "
    "fuel_delivery_type, valvetrain_type, target_lambda_v112, target_rpm_u2, idle_rpm_low, co_low_idle, "
    "co_high_idle, co_type_approval, hc_type_approval, nox_type_approval, hc_nox_type_approval, "
    "co2_type_approval, noise_stationary_dba, noise_rpm, noise_driving_dba, rated_rpm) "
    "SELECT engine_code, brand, displacement_cc, euro_norm, my_start, my_end, era_bucket, "
    "has_vvt, has_gdi, has_turbo, is_v_engine, has_egr, has_maf, has_map, o2_type, induction_type, "
    "fuel_delivery_type, valvetrain_type, target_lambda_v112, target_rpm_u2, idle_rpm_low, co_low_idle, "
    "co_high_idle, co_type_approval, hc_type_approval, nox_type_approval, hc_nox_type_approval, "
    "co2_type_approval, noise_stationary_dba, noise_rpm, noise_driving_dba, rated_rpm "
    "FROM shipped.engine_ref WHERE o2_type != ''"
)
PRE_MERGE_ROWS = 72
# The 72 original rows as explicit columns, read in this order (correction 02).
ORIGINAL_ROWS_SQL = (
    "SELECT engine_code, brand, displacement_cc, euro_norm, my_start, my_end, era_bucket, has_vvt, has_gdi, "
    "has_turbo, is_v_engine, has_egr, has_maf, has_map, o2_type, induction_type, fuel_delivery_type, "
    "valvetrain_type, rated_rpm, target_lambda_v112, target_rpm_u2, idle_rpm_low, co_low_idle, co_high_idle, "
    "co_type_approval, hc_type_approval, nox_type_approval, hc_nox_type_approval, co2_type_approval, "
    "noise_stationary_dba, noise_rpm, noise_driving_dba FROM engine_ref WHERE o2_type != '' ORDER BY engine_code"
)
# sha256 of the canonical dump (ORIGINAL_ROWS_SQL, each value as [python type name, value], compact JSON) of
# `git show 11dfa95:labs/vinlab/vinlab/data/vref.db` (blob c75ea107, the pre-merge file).
ORIGINAL_ROWS_SHA256 = "89403096d8074357d62e94187c58c71664c73ab4bc47c5ca4d00dbf654625275"


@pytest.fixture(scope="module")
def tool():
    spec = importlib.util.spec_from_file_location("merge_tecdoc_extract", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolves the module through sys.modules
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def db(data_dir, tmp_path) -> Path:
    """A vref.db in its pre-T-VINA-13b state, rebuilt from the shipped file."""
    path = tmp_path / "vref.db"
    conn = sqlite3.connect(f"file:{path}?mode=rwc", uri=True)  # uri=True so the ATTACH below opens read-only
    try:
        conn.executescript(PRE_MERGE_DDL)
        conn.execute("ATTACH DATABASE ? AS shipped", (f"file:{data_dir / 'vref.db'}?mode=ro",))
        conn.execute(COPY_PRE_MERGE_ROWS)
        conn.commit()
        conn.execute("DETACH DATABASE shipped")
        count = conn.execute("SELECT COUNT(*) FROM engine_ref").fetchone()[0]
    finally:
        conn.close()
    assert count == PRE_MERGE_ROWS
    return path


def _extract_row(**overrides: str) -> dict[str, str]:
    row = {
        "brand": "TESTBRAND", "engine_code": "ZZ9NEW", "match_tier": "T0", "status": "OK",
        "tecdoc_engine_ids": "1", "tecdoc_description": "ZZ9NEW", "displacement_cc": "1598",
        "cylinder_count": "4", "fuel_delivery_type": "PORT_INJECTION", "induction_type": "NATURALLY_ASPIRATED",
        "has_turbo": "0", "has_gdi": "0", "is_v_engine": "0", "valvetrain_type": "DOHC", "euro_norm": "euro4",
        "my_start": "1999", "my_end": "2004", "n_cars": "1",
    }
    row.update(overrides)
    return row


def _map_row(**overrides: str) -> dict[str, str]:
    row = {
        "brand": "TESTBRAND", "vds_full": "ABCDE", "pos_8_only": "", "engine_code": "ZZ9NEW",
        "engine_displacement": "1.6", "cylinder_count": "4", "engine_configuration": "I4",
        "fuel_system_type": "PORT_INJECTION", "majority_share": "1.000",
    }
    row.update(overrides)
    return row


def _write_csv(path: Path, header: list[str], rows) -> Path:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _merge(tool, tmp_path: Path, db: Path, extract_rows, map_rows=()):
    extract = _write_csv(tmp_path / "extract.csv", EXTRACT_HEADER, extract_rows)
    map_path = _write_csv(tmp_path / "map.csv", MAP_HEADER, map_rows)
    return tool.merge(db, extract, map_path)


def _query(db: Path, sql: str, params=()) -> list[dict]:
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params)]
    finally:
        conn.close()


def _row(db: Path, code: str) -> dict | None:
    rows = _query(db, "SELECT * FROM engine_ref WHERE engine_code = ?", (code,))
    return rows[0] if rows else None


def _dump(db: Path) -> dict[str, dict[str, tuple[str, object]]]:
    return {
        r["engine_code"]: {k: (type(v).__name__, v) for k, v in r.items()}
        for r in _query(db, "SELECT * FROM engine_ref")
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_inserts_new_code(tool, tmp_path, db):
    report = _merge(tool, tmp_path, db, [_extract_row()])
    assert report.inserted == ("ZZ9NEW",)
    row = _row(db, "ZZ9NEW")
    assert row is not None
    assert row["brand"] == "TESTBRAND"
    assert row["displacement_cc"] == 1598
    assert row["euro_norm"] == "euro4"
    assert row["induction_type"] == "NATURALLY_ASPIRATED"
    assert row["fuel_delivery_type"] == "PORT_INJECTION"
    assert row["valvetrain_type"] == "DOHC"
    assert (row["my_start"], row["my_end"]) == (1999, 2005)
    assert row["is_v_engine"] == 0


def test_skips_code_already_in_vref(tool, tmp_path, db):
    before = _row(db, "5FR")
    report = _merge(tool, tmp_path, db, [_extract_row(engine_code="5 FR", displacement_cc="9999")])
    assert report.inserted == ()
    assert "5FR" in report.skipped["in_vref"]
    assert _row(db, "5 FR") is None
    assert _row(db, "5FR") == before


def test_skips_collision_code(tool, tmp_path, db):
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ8COL", displacement_cc="1598"),
        _extract_row(brand="BRANDB", engine_code="ZZ8COL", displacement_cc="1796"),
    ]
    report = _merge(tool, tmp_path, db, rows)
    assert report.inserted == ()
    assert report.skipped["collision"] == ("ZZ8COL",)
    assert _row(db, "ZZ8COL") is None


def test_skips_code_without_my_start(tool, tmp_path, db):
    report = _merge(tool, tmp_path, db, [_extract_row(engine_code="ZZ7NOS", my_start="")])
    assert report.inserted == ()
    assert report.skipped["no_my_start"] == ("ZZ7NOS",)
    assert _row(db, "ZZ7NOS") is None


def test_new_row_leaves_maf_and_map_null(tool, tmp_path, db):
    _merge(tool, tmp_path, db, [_extract_row(induction_type="TURBOCHARGED", has_turbo="1")])
    row = _row(db, "ZZ9NEW")
    assert row is not None
    assert row["has_maf"] is None
    assert row["has_map"] is None


def test_new_row_o2_type_is_empty(tool, tmp_path, db):
    _merge(tool, tmp_path, db, [_extract_row()])
    row = _row(db, "ZZ9NEW")
    assert row is not None
    assert row["o2_type"] == ""


def test_blank_fields_become_null_or_zero(tool, tmp_path, db):
    blank = _extract_row(
        displacement_cc="", euro_norm="", induction_type="", fuel_delivery_type="", valvetrain_type="",
        has_turbo="", has_gdi="", is_v_engine="",
    )
    _merge(tool, tmp_path, db, [blank])
    row = _row(db, "ZZ9NEW")
    assert row is not None
    for col in ("displacement_cc", "euro_norm", "induction_type", "fuel_delivery_type", "valvetrain_type",
                *COC_COLUMNS):
        assert row[col] is None, col
    for col in ("has_turbo", "has_gdi", "is_v_engine", "has_vvt", "has_egr"):
        assert row[col] == 0, col


def test_window_adds_one_model_year_and_closes_open_end(tool, tmp_path, db):
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ6WIN", my_start="1996", my_end="2000"),
        _extract_row(brand="BRANDB", engine_code="ZZ6WIN", my_start="1999", my_end=""),
    ]
    _merge(tool, tmp_path, db, rows)
    row = _row(db, "ZZ6WIN")
    assert row is not None
    assert (row["my_start"], row["my_end"]) == (1996, 2020)
    assert row["brand"] == "BRANDA"


def test_era_bucket_comes_from_builder(tool, tmp_path, db):
    _merge(tool, tmp_path, db, [_extract_row(my_start="1997", my_end="2001")])
    row = _row(db, "ZZ9NEW")
    assert row is not None
    assert (row["my_start"], row["my_end"]) == (1997, 2002)
    assert row["era_bucket"] == "ERA_OBDII_EARLY"
    assert row["era_bucket"] == tool.derive_era(1997, 2002)


def test_ambiguous_code_is_inserted(tool, tmp_path, db):
    report = _merge(tool, tmp_path, db, [_extract_row(status="AMBIGUOUS", displacement_cc="")])
    assert report.inserted == ("ZZ9NEW",)
    row = _row(db, "ZZ9NEW")
    assert row is not None
    assert row["displacement_cc"] is None


def test_map_boxer_code_is_inserted(tool, tmp_path, db):
    # T-VINA-14 R1: the decoder gives a row on a map BOXER two banks, so is_v_engine 0 loses nothing.
    report = _merge(tool, tmp_path, db, [_extract_row()], [_map_row(engine_configuration="BOXER_4")])
    assert report.inserted == ("ZZ9NEW",)
    assert report.skipped["map_banks"] == ()
    row = _row(db, "ZZ9NEW")
    assert row is not None
    assert row["is_v_engine"] == 0


def test_blank_is_v_engine_with_v_map_is_skipped(tool, tmp_path, db):
    report = _merge(
        tool, tmp_path, db, [_extract_row(is_v_engine="", cylinder_count="6")],
        [_map_row(engine_configuration="V6", cylinder_count="6")],
    )
    assert report.inserted == ()
    assert report.skipped["map_banks"] == ("ZZ9NEW",)


def test_stated_na_heuristic_code_is_inserted(tool, tmp_path, db):
    # The Skoda brand rule reads 1.198 L as a 1.2 TSI (I3 TURBOCHARGED); TecDoc states NATURALLY_ASPIRATED, and
    # T-VINA-14 R2 keeps a stated induction in the decoder, so G2 has no induction test.
    extract = _extract_row(brand="SKODA", engine_code="ZZ5SKQ", displacement_cc="1198", cylinder_count="3")
    map_row = _map_row(brand="SKODA", engine_code="ZZ5SKQ", engine_displacement="", cylinder_count="",
                       engine_configuration="")
    report = _merge(tool, tmp_path, db, [extract], [map_row])
    assert report.inserted == ("ZZ5SKQ",)
    assert report.skipped["cylinder_heuristic"] == ()
    row = _row(db, "ZZ5SKQ")
    assert row is not None
    assert row["induction_type"] == "NATURALLY_ASPIRATED"


def test_blank_against_value_collision_is_coalesced(tool, tmp_path, db):
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ2BLK", euro_norm="", valvetrain_type=""),
        _extract_row(brand="BRANDB", engine_code="ZZ2BLK", euro_norm="euro4", valvetrain_type="SOHC",
                     induction_type=""),
    ]
    report = _merge(tool, tmp_path, db, rows)
    assert report.inserted == ("ZZ2BLK",)
    assert report.skipped["collision"] == ()
    row = _row(db, "ZZ2BLK")
    assert row is not None
    assert row["brand"] == "BRANDA"
    assert row["euro_norm"] == "euro4"
    assert row["valvetrain_type"] == "SOHC"
    assert row["induction_type"] == "NATURALLY_ASPIRATED"


def test_one_cc_collision_takes_first_stating_brand_cc(tool, tmp_path, db):
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ2ONE", displacement_cc=""),
        _extract_row(brand="BRANDB", engine_code="ZZ2ONE", displacement_cc="1598"),
        _extract_row(brand="BRANDC", engine_code="ZZ2ONE", displacement_cc="1597"),
    ]
    report = _merge(tool, tmp_path, db, rows)
    assert report.inserted == ("ZZ2ONE",)
    row = _row(db, "ZZ2ONE")
    assert row is not None
    assert row["brand"] == "BRANDA"
    assert row["displacement_cc"] == 1598


def test_two_cc_spread_stays_collision(tool, tmp_path, db):
    # PIN
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ2TWO", displacement_cc="1597"),
        _extract_row(brand="BRANDB", engine_code="ZZ2TWO", displacement_cc="1599"),
    ]
    report = _merge(tool, tmp_path, db, rows)
    assert report.inserted == ()
    assert report.skipped["collision"] == ("ZZ2TWO",)


def test_three_cc_values_stay_collision(tool, tmp_path, db):
    # PIN (correction 01, C2): adjacent 1 cc steps are not one value.
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ2THR", displacement_cc="1597"),
        _extract_row(brand="BRANDB", engine_code="ZZ2THR", displacement_cc="1598"),
        _extract_row(brand="BRANDC", engine_code="ZZ2THR", displacement_cc="1599"),
    ]
    report = _merge(tool, tmp_path, db, rows)
    assert report.inserted == ()
    assert report.skipped["collision"] == ("ZZ2THR",)


def test_g1_runs_on_the_coalesced_row(tool, tmp_path, db):
    # Review correction 02 (a): the coalesced is_v_engine is BRANDB's stated 0, so the blank-is_v_engine G1 skip
    # does not fire; on BRANDA's row alone it would.
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ2GOO", is_v_engine=""),
        _extract_row(brand="BRANDB", engine_code="ZZ2GOO", is_v_engine="0"),
    ]
    map_row = _map_row(engine_code="ZZ2GOO", engine_configuration="V6", cylinder_count="6")
    report = _merge(tool, tmp_path, db, rows, [map_row])
    assert report.inserted == ("ZZ2GOO",)
    assert report.skipped["map_banks"] == ()


def test_g2_runs_on_the_coalesced_row(tool, tmp_path, db):
    # Review correction 02 (b): the coalesced displacement is BRANDB's 1198 cc; the Skoda brand rule reads it as an
    # I3, TecDoc states 4 cylinders, so G2 (i) fires; on BRANDA's blank displacement alone it would not.
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ2GTW", displacement_cc="", cylinder_count="4", is_v_engine="0"),
        _extract_row(brand="BRANDB", engine_code="ZZ2GTW", displacement_cc="1198", cylinder_count="4",
                     is_v_engine="0"),
    ]
    map_row = _map_row(brand="SKODA", engine_code="ZZ2GTW", engine_displacement="", cylinder_count="",
                       engine_configuration="")
    report = _merge(tool, tmp_path, db, rows, [map_row])
    assert report.inserted == ()
    assert report.skipped["cylinder_heuristic"] == ("ZZ2GTW",)


def test_non_displacement_conflict_stays_collision(tool, tmp_path, db):
    # PIN (correction 01, C2)
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ2IND", induction_type="NATURALLY_ASPIRATED"),
        _extract_row(brand="BRANDB", engine_code="ZZ2IND", induction_type="TURBOCHARGED"),
    ]
    report = _merge(tool, tmp_path, db, rows)
    assert report.inserted == ()
    assert report.skipped["collision"] == ("ZZ2IND",)


def test_cylinder_heuristic_two_bank_hint_alone_is_skipped(tool, tmp_path, db):
    # G2 (iii) in isolation (correction 02): the map says I4 with no cylinder count and no displacement, so the
    # no-row hint is unresolved; at TecDoc's 3.0 L the displacement fallback says 6 cylinders, V6, NA. TecDoc
    # states 6 cylinders, NA and not V, so only the second bank is the heuristic's own value.
    extract = _extract_row(engine_code="ZZ3VEE", displacement_cc="3000", cylinder_count="6", is_v_engine="0")
    map_row = _map_row(engine_code="ZZ3VEE", engine_displacement="", cylinder_count="", engine_configuration="I4")
    report = _merge(tool, tmp_path, db, [extract], [map_row])
    assert report.inserted == ()
    assert report.skipped["cylinder_heuristic"] == ("ZZ3VEE",)
    assert report.skipped["map_banks"] == ()


def test_shipped_original_rows_match_the_pinned_base_digest(data_dir):
    conn = sqlite3.connect(f"file:{data_dir / 'vref.db'}?mode=ro", uri=True)
    try:
        rows = [[[type(v).__name__, v] for v in r] for r in conn.execute(ORIGINAL_ROWS_SQL)]
    finally:
        conn.close()
    assert len(rows) == PRE_MERGE_ROWS
    digest = hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()
    assert digest == ORIGINAL_ROWS_SHA256


def test_span_gap_code_is_skipped(tool, tmp_path, db):
    rows = [
        _extract_row(brand="BRANDA", engine_code="ZZ4GAP", my_start="1980", my_end="1985"),
        _extract_row(brand="BRANDB", engine_code="ZZ4GAP", my_start="1990", my_end="1995"),
        _extract_row(brand="BRANDA", engine_code="ZZ4ONE", my_start="1980", my_end="1985"),
        _extract_row(brand="BRANDB", engine_code="ZZ4ONE", my_start="1987", my_end="1990"),
    ]
    report = _merge(tool, tmp_path, db, rows)
    assert report.skipped["span_gap"] == ("ZZ4GAP",)
    assert report.inserted == ("ZZ4ONE",)


def test_second_run_inserts_nothing_and_keeps_bytes(tool, tmp_path, db):
    first = _merge(tool, tmp_path, db, [_extract_row()])
    assert first.inserted == ("ZZ9NEW",)
    assert first.schema_rebuilt
    digest = _sha256(db)
    second = _merge(tool, tmp_path, db, [_extract_row()])
    assert second.inserted == ()
    assert not second.schema_rebuilt
    assert _sha256(db) == digest


def test_existing_rows_keep_every_value(tool, tmp_path, db):
    before = _dump(db)
    assert len(before) == 72
    _merge(tool, tmp_path, db, [_extract_row()])
    after = _dump(db)
    assert {code: after[code] for code in before} == before
    assert {after[code]["has_maf"] for code in before} <= {("int", 0), ("int", 1)}
    assert {after[code]["has_map"] for code in before} <= {("int", 0), ("int", 1)}


def test_schema_matches_builder(tool, tmp_path, db):
    _merge(tool, tmp_path, db, [_extract_row()])
    ref = sqlite3.connect(":memory:")
    try:
        ref.executescript(tool.CREATE_ENGINE_REF)
        expected = ref.execute("PRAGMA table_info(engine_ref)").fetchall()
    finally:
        ref.close()
    conn = sqlite3.connect(db)
    try:
        actual = conn.execute("PRAGMA table_info(engine_ref)").fetchall()
        indexes = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = 'engine_ref'"
            " AND name = 'idx_engine_ref_brand'"
        ).fetchall()
    finally:
        conn.close()
    assert actual == expected
    sensors = {r[1]: (r[3], r[4]) for r in actual if r[1] in ("has_maf", "has_map")}
    assert sensors == {"has_maf": (0, None), "has_map": (0, None)}
    assert indexes == [("idx_engine_ref_brand",)]


def test_real_vin_gains_row_with_tecdoc_displacement(tool, data_dir, tmp_path, db):
    pre_merge = tmp_path / "pre_merge.db"
    shutil.copyfile(db, pre_merge)
    tool.merge(db, tool.DEFAULT_EXTRACT, tool.DEFAULT_MAP)
    before = RobustVINDecoder(data_dir)
    before.db_path = pre_merge
    after = RobustVINDecoder(data_dir)
    after.db_path = db
    without_row = before.decode_vin_payload(REAL_VIN)
    with_row = after.decode_vin_payload(REAL_VIN)
    assert without_row.engine_displacement_liters == 1.4
    assert with_row.engine_displacement_liters == 0.973
    assert with_row.air_metering_architecture == without_row.air_metering_architecture
    assert with_row.emissions.upstream_o2_type == without_row.emissions.upstream_o2_type
