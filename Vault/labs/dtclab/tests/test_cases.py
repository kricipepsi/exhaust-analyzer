"""Parametrized characterization net over dtclab_cases.csv (T-TST-9).

All 194 rows from T-TST-7's projection.  Expected-output columns are empty
(gt_method=characterization), so this is a regression net, not a correctness
gate: it asserts no crash + schema-valid payload, and records the observed
routing_tags / historical_context / freeze_frame_status.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from dtclab.schemas.payload import DTCLabPayload
from tests.conftest import (
    is_fail_closed,
    make_freeze_frame_raw,
    map_fuel_status,
    parse_dtc_cell,
    run_sanitize,
)

# Path to the CSV fixture, relative to this test file.
_CSV_PATH = Path(__file__).resolve().parent / "fixtures" / "dtclab_cases.csv"

# Columns with core freeze-frame data that justify running the pipeline.
_CORE_FF_COLS = ("ff_ect", "ff_rpm", "ff_load")


def _load_csv_rows() -> list[dict[str, str]]:
    """Load all rows from dtclab_cases.csv."""
    rows: list[dict[str, str]] = []
    with _CSV_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(r)
    assert len(rows) == 194, f"Expected 194 rows, found {len(rows)}"
    return rows


def _has_ff_core(row: dict[str, str]) -> bool:
    """True if the row has ect, rpm, and load values."""
    return all(row.get(col, "").strip() for col in _CORE_FF_COLS)


def _build_ff_from_row(row: dict[str, str]) -> dict[str, Any] | None:
    """Build a freeze-frame dict from CSV row columns.

    Returns None when core FF fields are absent.  Fills missing mandatory
    PIDs with benign defaults so the pipeline can run on partial-FF rows.
    """
    if not _has_ff_core(row):
        return None

    ff: dict[str, Any] = {
        "coolant_temp_c": float(row["ff_ect"]),
        "engine_rpm": int(float(row["ff_rpm"])),
        "calculated_load_pct": float(row["ff_load"]),
        "manifold_pressure_kpa": float(row["ff_map"]) if row.get("ff_map", "").strip() else 100.0,
        "short_term_ft1": float(row["ff_stft_b1"]) if row.get("ff_stft_b1", "").strip() else 0.0,
        "long_term_ft1": float(row["ff_ltft_b1"]) if row.get("ff_ltft_b1", "").strip() else 0.0,
        "vehicle_speed_kmh": 0,
        "ignition_advance_deg": 5.0,
        "intake_air_temp_c": 20.0,
        "maf_gps": 3.0,
        "throttle_pos_pct": 15.0,
    }

    fs_raw = row.get("fuel_status", "").strip()
    if fs_raw:
        fs_enum = map_fuel_status(fs_raw)
        if fs_enum is not None:
            ff["fuel_system_status"] = fs_enum.value
        else:
            ff["fuel_system_status"] = "CL"
    else:
        ff["fuel_system_status"] = "CL"

    return ff


def _make_row_id(row: dict[str, str]) -> str:
    """Human-readable test ID from a CSV row."""
    case_id = row.get("case_id", "?")
    dtcs = row.get("dtcs", "").strip()
    has_ff = "ff" if _has_ff_core(row) else "noff"
    dtc_info = dtcs[:20].replace(",", "_").replace("|", "_") if dtcs else "nodtc"
    return f"{case_id}_{has_ff}_{dtc_info}"


# =============================================================================
# Parametrized characterization net
# =============================================================================


def pytest_generate_tests(metafunc: Any) -> None:
    """Generate one test per dtclab_cases.csv row."""
    if "row" not in metafunc.fixturenames:
        return

    rows = _load_csv_rows()
    metafunc.parametrize(
        "row",
        rows,
        ids=[_make_row_id(r) for r in rows],
    )


def test_csv_cases_dtclab(row: dict[str, str]) -> None:
    """Characterization net — no crash + schema-valid payload per CSV row.

    Expected columns are empty (gt_method=characterization T-TST-7).
    Records observed routing_tags / historical_context / freeze_frame_status.
    """
    dtc_codes = parse_dtc_cell(row.get("dtcs", ""))
    ff = _build_ff_from_row(row)

    # Case 1: no DTCs and no freeze-frame core → nothing to exercise.
    if not dtc_codes and ff is None:
        return

    # Case 2: DTCs present, no freeze-frame core → use default FF.
    if dtc_codes and ff is None:
        ff = make_freeze_frame_raw()

    # Case 3: no DTCs but freeze-frame core present → empty DTC list.
    if not dtc_codes and ff is not None:
        dtc_codes = []

    assert ff is not None  # guaranteed by cases above

    # Run pipeline
    result, error = run_sanitize(dtc_codes, freeze_frame=ff)

    # Every outcome must be fail-closed
    assert is_fail_closed(result, error), (
        f"Row {row['case_id']}: NOT fail-closed — "
        f"error={type(error).__name__ if error else 'None'}: {error}"
    )

    if error is not None:
        # Expected error for incomplete/malformed inputs — not a crash.
        return

    # Schema-valid payload — record observed values
    assert isinstance(result, DTCLabPayload), (
        f"Row {row['case_id']}: expected DTCLabPayload, got {type(result).__name__}"
    )

    # Smoke-check: payload fields are sensible
    assert isinstance(result.active_mil, bool)
    assert isinstance(result.mil_flashing, bool)
    assert isinstance(result.confirmed_dtcs, list)
    assert isinstance(result.pending_dtcs, list)
    assert isinstance(result.permanent_dtcs, list)
    assert isinstance(result.routing_tags, list)
    assert isinstance(result.mode_06_monitors, dict)

    # Record for audit
    observed_tags = [t.value for t in result.routing_tags]
    observed_ctx = result.historical_fault_context.value
    print(
        f"\n{row['case_id']}: "
        f"tags={observed_tags} ctx={observed_ctx}"
    )
