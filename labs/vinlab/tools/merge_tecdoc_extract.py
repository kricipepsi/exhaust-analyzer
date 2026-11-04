#!/usr/bin/env python3
"""Merge the TecDoc 1Q2019 engine extract into vinlab/data/vref.db (T-VINA-13b, T-VINA-14).

Inserts one engine_ref row per extract engine code whose normalised code
(vinlab.db.tecdoc_query._normalise_code) vref.db does not hold yet. Existing
rows keep every value. The first run also rebuilds engine_ref with the
builder's DDL (tools/build_vref_db.py CREATE_ENGINE_REF), in which has_maf and
has_map accept NULL. A second run inserts nothing and writes nothing.

The rows of one code (one per brand) are coalesced first (T-VINA-14 R3): each
engine field takes the one non-blank value the brands state, or blank. Two
displacement_cc values 1 cc apart also coalesce, to the value of the
alphabetically first brand that states one. The row's brand is the
alphabetically first brand.

A code is skipped when (plans approved in
tasks/corrections/T-VINA-13b_plan_correction_20261104.md and
tasks/corrections/T-VINA-14_plan_correction_20261104.md):
  in_vref             its normalised code is already in engine_ref
  collision           an engine field holds two non-blank values that do not coalesce
  status              a row has a status other than OK, FAMILY or AMBIGUOUS
  no_my_start         a row has no my_start
  span_gap            its brand production spans leave more than one missing year (C3)
  map_banks           G1: a blank extract is_v_engine with a map V or W configuration
  cylinder_heuristic  G2: the decoder's cylinder fallback would set a cylinder count
                      or a second bank that TecDoc contradicts

Stdlib plus this lab's own package. Usage:
  python tools/merge_tecdoc_extract.py [--db PATH] [--extract PATH] [--map PATH]
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import os
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from vinlab.db.tecdoc_query import _normalise_code
from vinlab.overlay.cylinder_heuristic import infer_cylinder

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_DB = TOOLS_DIR.parent / "vinlab" / "data" / "vref.db"
DEFAULT_EXTRACT = TOOLS_DIR / "data" / "tecdoc_1q2019_engine_extract.csv"
DEFAULT_MAP = TOOLS_DIR.parent / "vinlab" / "data" / "vds_engine_map.csv"


def _load_builder() -> ModuleType:
    """Load tools/build_vref_db.py for CREATE_ENGINE_REF and _derive_era.

    The builder raises at import when DBS_ROOT is unset (build_vref_db.py:33-36).
    This tool reads no DBS file, so a placeholder is set for the import only.
    """
    old = os.environ.get("DBS_ROOT")
    if not old:
        os.environ["DBS_ROOT"] = "unused-by-merge_tecdoc_extract"
    try:
        spec = importlib.util.spec_from_file_location("build_vref_db", TOOLS_DIR / "build_vref_db.py")
        if spec is None or spec.loader is None:
            raise ImportError("cannot load tools/build_vref_db.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if old is None:
            del os.environ["DBS_ROOT"]
        elif not old:
            os.environ["DBS_ROOT"] = old
    return module


_BUILDER = _load_builder()
CREATE_ENGINE_REF: str = _BUILDER.CREATE_ENGINE_REF
derive_era = _BUILDER._derive_era

# source: tools/extract_tecdoc_1q2019.py FIELDS (the engine fields); rows of one code that differ here collide (R2)
COLLISION_FIELDS = (
    "displacement_cc", "cylinder_count", "fuel_delivery_type", "induction_type", "has_turbo", "has_gdi",
    "is_v_engine", "valvetrain_type", "euro_norm",
)
EXTRACT_COLUMNS = ("brand", "engine_code", "status", *COLLISION_FIELDS, "my_start", "my_end")
MAP_COLUMNS = ("brand", "engine_code", "engine_displacement", "cylinder_count", "engine_configuration")
# plan, correction 01: AMBIGUOUS rows are candidates; their disagreeing fields are blank
ALLOWED_STATUSES = frozenset({"OK", "FAMILY", "AMBIGUOUS"})
# source: the extract is TecDoc 1Q2019; an open my_end means the engine type was current in that data
OPEN_END_YEAR = 2019
# plan, correction 01: VIN position 10 is a model year; a car built in calendar year Y can carry model year Y + 1
MODEL_YEAR_LAG = 1
# correction 01, C3: brand production spans further apart than this many missing years are not one window
MAX_SPAN_GAP_YEARS = 1
SKIP_REASONS = (
    "in_vref", "collision", "status", "no_my_start", "span_gap", "map_banks", "cylinder_heuristic",
)

COPY_ROWS = (
    "INSERT INTO engine_ref (engine_code, brand, displacement_cc, euro_norm, my_start, my_end, era_bucket, "
    "has_vvt, has_gdi, has_turbo, is_v_engine, has_egr, has_maf, has_map, o2_type, induction_type, "
    "fuel_delivery_type, valvetrain_type, rated_rpm, target_lambda_v112, target_rpm_u2, idle_rpm_low, "
    "co_low_idle, co_high_idle, co_type_approval, hc_type_approval, nox_type_approval, hc_nox_type_approval, "
    "co2_type_approval, noise_stationary_dba, noise_rpm, noise_driving_dba) "
    "SELECT engine_code, brand, displacement_cc, euro_norm, my_start, my_end, era_bucket, "
    "has_vvt, has_gdi, has_turbo, is_v_engine, has_egr, has_maf, has_map, o2_type, induction_type, "
    "fuel_delivery_type, valvetrain_type, rated_rpm, target_lambda_v112, target_rpm_u2, idle_rpm_low, "
    "co_low_idle, co_high_idle, co_type_approval, hc_type_approval, nox_type_approval, hc_nox_type_approval, "
    "co2_type_approval, noise_stationary_dba, noise_rpm, noise_driving_dba "
    "FROM engine_ref_old"
)
INSERT_ROW = (
    "INSERT INTO engine_ref (engine_code, brand, displacement_cc, euro_norm, my_start, my_end, era_bucket, "
    "has_vvt, has_gdi, has_turbo, is_v_engine, has_egr, has_maf, has_map, o2_type, induction_type, "
    "fuel_delivery_type, valvetrain_type) "
    "VALUES (:engine_code, :brand, :displacement_cc, :euro_norm, :my_start, :my_end, :era_bucket, "
    ":has_vvt, :has_gdi, :has_turbo, :is_v_engine, :has_egr, :has_maf, :has_map, :o2_type, :induction_type, "
    ":fuel_delivery_type, :valvetrain_type)"
)


@dataclass(frozen=True)
class MergeReport:
    inserted: tuple[str, ...]
    skipped: dict[str, tuple[str, ...]]
    schema_rebuilt: bool
    rows_after: int


def _read_csv(path: Path, required: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in required if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path}: missing columns {missing}")
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _int_or_none(raw: str) -> int | None:
    return int(raw) if raw else None


def _flag(raw: str) -> int:
    """Extract 0/1 flag; blank is written 0 (R3)."""
    if raw not in ("", "0", "1"):
        raise ValueError(f"flag value {raw!r} is not blank, 0 or 1")
    return 1 if raw == "1" else 0


def _two_bank(config: str) -> bool:
    # source: decoder.py:278-280 and :479-482 (V/W/BOXER configurations emit number_of_banks=2)
    config = config.upper()
    return config[:1] in ("V", "W") or config.startswith("BOXER")


def _map_cylinders_unknown(raw: str) -> bool:
    # source: decoder.py:270-274 and :465 (a blank, 0 or non-integer map count leaves cylinder_count 0)
    try:
        return int(raw) == 0
    except ValueError:
        return True


def _map_liters(raw: str) -> float:
    # source: decoder.py:265-269 (a blank or non-numeric map displacement leaves 0.0)
    try:
        return float(raw)
    except ValueError:
        return 0.0


def _span_gap(group: list[dict[str, str]]) -> bool:
    """C3: True when the brand production spans leave more than MAX_SPAN_GAP_YEARS missing years."""
    spans = sorted((int(r["my_start"]), int(r["my_end"]) if r["my_end"] else OPEN_END_YEAR) for r in group)
    reach = spans[0][1]
    for start, end in spans[1:]:
        if start - reach - 1 > MAX_SPAN_GAP_YEARS:
            return True
        reach = max(reach, end)
    return False


def _one_cc_spread(values: set[str]) -> bool:
    """True for exactly two displacement_cc values 1 cc apart (T-VINA-14 R3)."""
    if len(values) != 2:
        return False
    low, high = sorted(int(v) for v in values)
    return high - low == 1


def _coalesce(group: list[dict[str, str]]) -> dict[str, str] | None:
    """Coalesce the brand rows of one code (sorted by brand), or None when they collide.

    Each COLLISION_FIELDS field takes the first non-blank value in brand order,
    or blank. A field with two distinct non-blank values is a collision, except
    displacement_cc with two values 1 cc apart.
    """
    row = dict(group[0])
    for field in COLLISION_FIELDS:
        values = [r[field] for r in group if r[field]]
        distinct = set(values)
        if len(distinct) > 1 and not (field == "displacement_cc" and _one_cc_spread(distinct)):
            return None
        row[field] = values[0] if values else ""
    return row


def _g1_map_banks(row: dict[str, str], map_rows: list[dict[str, str]]) -> bool:
    """G1: a blank extract is_v_engine, written 0, would replace a map V or W configuration's second bank.

    The decoder gives a row two banks for is_v_engine 1 or a map BOXER
    configuration (decoder.py _apply_vref_techmask, T-VINA-14 R1), so a map
    BOXER loses nothing. A stated 0 against a map V or W is TecDoc's value.
    """
    return not row["is_v_engine"] and any(m["engine_configuration"].upper()[:1] in ("V", "W") for m in map_rows)


def _g2_cylinder_heuristic(row: dict[str, str], map_rows: list[dict[str, str]]) -> bool:
    """G2: with the row, the decoder's cylinder fallback would emit a value TecDoc contradicts.

    _cylinder_fallback (decoder.py) runs infer_cylinder on the row's
    displacement when the map row has no cylinder count. It may set a count
    and add a second bank. Skip the code when that differs from the no-row
    decode and TecDoc states otherwise. The fallback keeps an induction the
    row states (T-VINA-14 R2), so G2 has no induction test.
    """
    if not row["displacement_cc"]:
        return False
    tecdoc_liters = int(row["displacement_cc"]) / 1000.0
    for m in map_rows:
        if not _map_cylinders_unknown(m["cylinder_count"]):
            continue
        before = infer_cylinder(m["engine_code"], _map_liters(m["engine_displacement"]), m["brand"])
        after = infer_cylinder(m["engine_code"], tecdoc_liters, m["brand"])
        if after.count <= 0:
            continue
        if row["cylinder_count"] and after.count != int(row["cylinder_count"]) and after.count != before.count:
            return True
        if row["is_v_engine"] != "1" and _two_bank(after.config) and not (
            before.count > 0 and _two_bank(before.config)
        ):
            return True
    return False


def _skip_reason(
    code: str,
    group: list[dict[str, str]],
    row: dict[str, str] | None,
    existing: set[str],
    map_rows: list[dict[str, str]],
) -> str | None:
    if code in existing:
        return "in_vref"
    if row is None:
        return "collision"
    if any(r["status"] not in ALLOWED_STATUSES for r in group):
        return "status"
    if any(not r["my_start"] for r in group):
        return "no_my_start"
    if _span_gap(group):
        return "span_gap"
    if _g1_map_banks(row, map_rows):
        return "map_banks"
    if _g2_cylinder_heuristic(row, map_rows):
        return "cylinder_heuristic"
    return None


def _new_row(first: dict[str, str], group: list[dict[str, str]]) -> dict[str, Any]:
    """Build the engine_ref row from the coalesced row (engine fields) and the group (window)."""
    my_start = min(int(r["my_start"]) for r in group)
    my_end = max(int(r["my_end"]) if r["my_end"] else OPEN_END_YEAR for r in group) + MODEL_YEAR_LAG
    return {
        "engine_code": first["engine_code"],
        "brand": first["brand"].upper(),
        "displacement_cc": _int_or_none(first["displacement_cc"]),
        "euro_norm": first["euro_norm"] or None,
        "my_start": my_start,
        "my_end": my_end,
        "era_bucket": derive_era(my_start, my_end),
        "has_vvt": 0,
        "has_gdi": _flag(first["has_gdi"]),
        "has_turbo": _flag(first["has_turbo"]),
        "is_v_engine": _flag(first["is_v_engine"]),
        "has_egr": 0,
        "has_maf": None,
        "has_map": None,
        "o2_type": "",
        "induction_type": first["induction_type"] or None,
        "fuel_delivery_type": first["fuel_delivery_type"] or None,
        "valvetrain_type": first["valvetrain_type"] or None,
    }


def select_rows(
    extract_rows: list[dict[str, str]],
    existing: set[str],
    map_rows: dict[str, list[dict[str, str]]],
) -> tuple[list[dict[str, Any]], dict[str, tuple[str, ...]]]:
    """Return the engine_ref rows to insert and the skipped normalised codes per reason."""
    by_code: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in extract_rows:
        code = _normalise_code(r["engine_code"])
        if not code:
            raise ValueError(f"extract row without an engine code: {r}")
        by_code[code].append(r)
    rows: list[dict[str, Any]] = []
    skipped: dict[str, list[str]] = {reason: [] for reason in SKIP_REASONS}
    for code in sorted(by_code):
        group = sorted(by_code[code], key=lambda r: r["brand"])
        row = _coalesce(group)
        reason = _skip_reason(code, group, row, existing, map_rows.get(code, []))
        if reason is not None:
            skipped[reason].append(code)
        elif row is None:
            raise RuntimeError(f"{code}: rows collide but no skip reason was given")
        else:
            rows.append(_new_row(row, group))
    return rows, {reason: tuple(codes) for reason, codes in skipped.items()}


def _statements(script: str) -> list[str]:
    out: list[str] = []
    buf = ""
    for line in script.splitlines(keepends=True):
        buf += line
        if sqlite3.complete_statement(buf):
            out.append(buf.strip())
            buf = ""
    if buf.strip():
        raise ValueError("CREATE_ENGINE_REF ends in an incomplete statement")
    return out


def _columns(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    return [(r[1], r[3]) for r in conn.execute("PRAGMA table_info(engine_ref)")]


def _rebuild_engine_ref(conn: sqlite3.Connection) -> None:
    """Recreate engine_ref with the builder DDL and copy every row by column name (inside the caller's transaction)."""
    conn.execute("DROP INDEX IF EXISTS idx_engine_ref_brand")
    conn.execute("ALTER TABLE engine_ref RENAME TO engine_ref_old")
    for statement in _statements(CREATE_ENGINE_REF):
        conn.execute(statement)
    conn.execute(COPY_ROWS)
    conn.execute("DROP TABLE engine_ref_old")


def merge(db_path: Path = DEFAULT_DB, extract_path: Path = DEFAULT_EXTRACT, map_path: Path = DEFAULT_MAP) -> MergeReport:
    """Insert the selected extract rows into db_path; rebuild engine_ref first when has_maf/has_map are NOT NULL."""
    if not db_path.is_file():
        raise FileNotFoundError(db_path)
    extract_rows = _read_csv(extract_path, EXTRACT_COLUMNS)
    map_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for m in _read_csv(map_path, MAP_COLUMNS):
        if m["engine_code"]:
            map_rows[_normalise_code(m["engine_code"])].append(m)

    reference = sqlite3.connect(":memory:")
    try:
        reference.executescript(CREATE_ENGINE_REF)
        builder_names = {name for name, _ in _columns(reference)}
    finally:
        reference.close()

    conn = sqlite3.connect(db_path, isolation_level=None)
    try:
        columns = _columns(conn)
        if {name for name, _ in columns} != builder_names:
            raise RuntimeError("engine_ref columns differ from CREATE_ENGINE_REF; refusing to merge")
        rebuild = any(notnull for name, notnull in columns if name in ("has_maf", "has_map"))
        existing = {_normalise_code(code) for (code,) in conn.execute("SELECT engine_code FROM engine_ref")}
        rows, skipped = select_rows(extract_rows, existing, map_rows)
        if rebuild or rows:
            conn.execute("BEGIN IMMEDIATE")
            try:
                if rebuild:
                    _rebuild_engine_ref(conn)
                conn.executemany(INSERT_ROW, rows)
                conn.execute("COMMIT")
            except BaseException:
                conn.execute("ROLLBACK")
                raise
        rows_after = conn.execute("SELECT COUNT(*) FROM engine_ref").fetchone()[0]
    finally:
        conn.close()
    return MergeReport(
        inserted=tuple(r["engine_code"] for r in rows),
        skipped=skipped,
        schema_rebuilt=rebuild,
        rows_after=rows_after,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge the TecDoc 1Q2019 engine extract into vref.db (T-VINA-13b).")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--extract", type=Path, default=DEFAULT_EXTRACT)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    args = parser.parse_args(argv)
    report = merge(args.db, args.extract, args.map)
    for reason in SKIP_REASONS:
        print(f"skipped {reason}: {len(report.skipped[reason])}")
    print("collision codes: " + " ".join(report.skipped["collision"]))
    print(
        f"inserted {len(report.inserted)} rows; engine_ref now {report.rows_after} rows; "
        f"schema rebuilt: {'yes' if report.schema_rebuilt else 'no'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
