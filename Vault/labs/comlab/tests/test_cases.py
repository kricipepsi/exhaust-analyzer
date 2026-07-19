"""Parametrized characterization net over comlab_cases.csv (T-COMTST-2).

Expected-output columns are intentionally empty, so this is a regression net,
not a correctness gate. It asserts no crash, schema-valid output, and
fail-closed handling for invalid inputs while recording observed verdicts.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, get_args

from pydantic import ValidationError

from comlab.schemas.response import (
    ConfidenceLit,
    DegradationLit,
    FaultFamilyLit,
    OrchestratorFinalUIOutput,
)
from tests.fixtures.descriptor import build_comlab_descriptor

_CSV_PATH = Path(__file__).resolve().parent / "fixtures" / "comlab_cases.csv"
_PINNED_ROW_COUNT = 24  # task: T-COMTST-1 fixture pin
_VALIDATION_ERROR_HINTS = frozenset({"invalid_input"})
_DESCRIPTOR = build_comlab_descriptor()


def _load_csv_rows() -> list[dict[str, str]]:
    """Load all pinned COMLab characterization rows."""
    with _CSV_PATH.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == _PINNED_ROW_COUNT, (
        f"Expected {_PINNED_ROW_COUNT} rows, found {len(rows)}"
    )
    return rows


def _make_row_id(row: dict[str, str]) -> str:
    """Build a readable test ID from the case and intended family coverage."""
    case_id = row.get("case_id", "?").strip() or "unknown"
    family = row.get("family_hint", "?").strip() or "unknown"
    return f"{case_id}_{family}"


def pytest_generate_tests(metafunc: Any) -> None:
    """Generate one test per comlab_cases.csv row."""
    if "row" not in metafunc.fixturenames:
        return

    rows = _load_csv_rows()
    metafunc.parametrize(
        "row",
        rows,
        ids=[_make_row_id(row) for row in rows],
    )


def test_csv_cases_comlab(row: dict[str, str]) -> None:
    """Characterize every assembled-verdict row without scoring accuracy."""
    family_hint = row.get("family_hint", "").strip()

    try:
        args = _DESCRIPTOR.build_args(row)
        result = _DESCRIPTOR.entry_point(*args)
    except ValidationError:
        assert family_hint in _VALIDATION_ERROR_HINTS, (
            f"Row {row['case_id']}: valid characterization row failed validation"
        )
        return

    assert isinstance(result, OrchestratorFinalUIOutput), (
        f"Row {row['case_id']}: expected OrchestratorFinalUIOutput, "
        f"got {type(result).__name__}"
    )

    degradation_mode = result.execution_meta.degradation_mode
    confidence = result.execution_meta.processing_confidence_rating
    verdict = result.diagnostic_verdict

    assert degradation_mode in get_args(DegradationLit)
    assert confidence in get_args(ConfidenceLit)
    assert verdict.fault_family in get_args(FaultFamilyLit)
    assert isinstance(verdict.fault_code, str)
    assert isinstance(verdict.confidence_score, float)

    if verdict.fault_family == "invalid_input":
        assert degradation_mode == "FATAL_INCOMPLETE", (
            f"Row {row['case_id']}: invalid-input verdict did not fail closed"
        )

    print(
        f"\n{row['case_id']}: "
        f"top_fault={verdict.fault_code} "
        f"fault_family={verdict.fault_family} "
        f"degradation_mode={degradation_mode} "
        f"confidence={confidence}"
    )
