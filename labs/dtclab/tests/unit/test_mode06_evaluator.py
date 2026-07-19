"""Tests for dtclab.core.mode06_evaluator — margin tri-state classifier.

Covers: margin boundaries (0, 15, 16, -5, 100), MID key validation (valid,
invalid format, valid regex but unknown MID), component lookup (known MID,
unknown MID).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dtclab.core.mode06_evaluator import classify_margin, evaluate_monitor
from dtclab.schemas.dna_view import EuroEmissionCategory
from dtclab.schemas.vocabulary import Mode06MonitorState


# -- helpers --------------------------------------------------------------------


def _make_dict(tmp_path: Path) -> Path:
    """Write a minimal MID dictionary into *tmp_path* and return the path."""
    dictionary = {
        "_source_wiki": "DTC_VOCABULARY.md §13.2",
        "21": {"name": "Catalyst OSC Bank 1", "source_wiki": "DTC_VOCABULARY.md §13.2"},
        "A1": {"name": "Misfire Cylinder 1", "source_wiki": "DTC_VOCABULARY.md §13.2"},
        "A2": {"name": "Misfire Cylinder 2", "source_wiki": "DTC_VOCABULARY.md §13.2"},
    }
    dict_path = tmp_path / "mode_06_hex_dictionary.json"
    dict_path.write_text(json.dumps(dictionary), encoding="utf-8")
    return dict_path


# -- margin classification -----------------------------------------------------


_MARGIN_CASES = [
    (0.0, Mode06MonitorState.CRITICAL_FAIL),
    (-5.0, Mode06MonitorState.CRITICAL_FAIL),
    (-0.1, Mode06MonitorState.CRITICAL_FAIL),
    (1.0, Mode06MonitorState.PENDING_FAIL_MARGINAL),
    (15.0, Mode06MonitorState.PENDING_FAIL_MARGINAL),
    (7.5, Mode06MonitorState.PENDING_FAIL_MARGINAL),
    (16.0, Mode06MonitorState.PASSED),
    (100.0, Mode06MonitorState.PASSED),
    (50.0, Mode06MonitorState.PASSED),
]


@pytest.mark.parametrize(("margin_pct", "expected"), _MARGIN_CASES)
def test_classify_margin_boundaries(
    margin_pct: float, expected: Mode06MonitorState
) -> None:
    assert classify_margin(margin_pct) == expected


# -- MID key validation ---------------------------------------------------------


_VALID_KEYS = [
    "MID_21_TID_81",
    "MID_A2_TID_0B",
    "MID_01_TID_01",
    "MID_E1_TID_80",
    "MID_3D_TID_84",
]


@pytest.mark.parametrize("mid_key", _VALID_KEYS)
def test_valid_mid_keys(mid_key: str, tmp_path: Path) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor(mid_key, 50.0, dict_path)
    assert result.monitor_id == mid_key
    assert result.state == Mode06MonitorState.PASSED


_INVALID_KEYS = [
    ("MID_A2_TID_0", "TID too short — 1 hex digit"),
    ("MID_A2_TID_0BC", "TID too long — 3 hex digits"),
    ("MID_A22_TID_0B", "MID too long — 3 hex digits"),
    ("MID_G2_TID_0B", "non-hex MID character"),
    ("MID_A2_TID_0G", "non-hex TID character"),
    ("", "empty string"),
    ("   ", "whitespace"),
    ("just_random", "no MID prefix"),
    ("mid_a2_tid_0b", "lowercase — must be uppercase"),
    ("A2_TID_0B", "missing MID_ prefix"),
    ("MID_A2_0B", "missing TID_ segment"),
]


@pytest.mark.parametrize(("mid_key", "_desc"), _INVALID_KEYS)
def test_invalid_mid_keys_raise(mid_key: str, _desc: str, tmp_path: Path) -> None:
    dict_path = _make_dict(tmp_path)
    with pytest.raises(ValueError, match="Invalid MID key"):
        evaluate_monitor(mid_key, 50.0, dict_path)


# -- component lookup -----------------------------------------------------------


def test_component_lookup_known_mid(tmp_path: Path) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor("MID_21_TID_81", 8.0, dict_path)
    assert result.target_component == "Catalyst OSC Bank 1"
    assert result.monitor_id == "MID_21_TID_81"
    assert result.state == Mode06MonitorState.PENDING_FAIL_MARGINAL
    assert result.margin_pct == 8.0


def test_component_lookup_unknown_mid(tmp_path: Path) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor("MID_99_TID_01", 30.0, dict_path)
    assert result.target_component == "UNKNOWN"
    assert result.state == Mode06MonitorState.PASSED


# -- structural checks (mirrors the task Verification block) --------------------


def test_margin_structural_assertions(tmp_path: Path) -> None:
    """Direct port of the verification block structural checks."""
    dict_path = _make_dict(tmp_path)

    r0 = evaluate_monitor("MID_21_TID_81", 0.0, dict_path)
    r15 = evaluate_monitor("MID_21_TID_81", 15.0, dict_path)
    r16 = evaluate_monitor("MID_21_TID_81", 16.0, dict_path)
    rn5 = evaluate_monitor("MID_21_TID_81", -5.0, dict_path)

    assert r0.state == Mode06MonitorState.CRITICAL_FAIL, f"Got {r0.state}"
    assert r15.state == Mode06MonitorState.PENDING_FAIL_MARGINAL, f"Got {r15.state}"
    assert r16.state == Mode06MonitorState.PASSED, f"Got {r16.state}"
    assert rn5.state == Mode06MonitorState.CRITICAL_FAIL, f"Got {rn5.state}"


# -- Mode06MonitorResult field integrity ----------------------------------------


def test_result_fields_are_fully_populated(tmp_path: Path) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor("MID_A2_TID_0B", -3.5, dict_path)
    assert result.monitor_id == "MID_A2_TID_0B"
    assert result.state == Mode06MonitorState.CRITICAL_FAIL
    assert result.margin_pct == -3.5
    assert result.target_component == "Misfire Cylinder 2"


# -- monitor-aborted no-start proposal -----------------------------------------


def test_monitor_incomplete_can_era_misfire_monitor_returns_aborted(
    tmp_path: Path,
) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor(
        "MID_A1_TID_53",
        50.0,
        dict_path,
        monitor_incomplete=True,
        euro_emission_category=EuroEmissionCategory.EURO_4,
    )

    assert result.state == Mode06MonitorState.MONITOR_ABORTED
    assert result.margin_pct == 50.0
    assert result.target_component == "Misfire Cylinder 1"


@pytest.mark.parametrize(
    "category",
    [
        EuroEmissionCategory.EURO_1,
        EuroEmissionCategory.EURO_2,
        EuroEmissionCategory.EURO_3,
        EuroEmissionCategory.UNKNOWN,
        None,
    ],
)
def test_monitor_incomplete_pre_can_or_unknown_uses_margin_path(
    category: EuroEmissionCategory | None,
    tmp_path: Path,
) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor(
        "MID_A1_TID_53",
        50.0,
        dict_path,
        monitor_incomplete=True,
        euro_emission_category=category,
    )

    assert result.state == Mode06MonitorState.PASSED


def test_monitor_incomplete_non_no_start_mid_uses_margin_path(
    tmp_path: Path,
) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor(
        "MID_A2_TID_0B",
        -1.0,
        dict_path,
        monitor_incomplete=True,
        euro_emission_category=EuroEmissionCategory.EURO_4,
    )

    assert result.state == Mode06MonitorState.CRITICAL_FAIL


def test_monitor_not_incomplete_can_era_uses_margin_path(
    tmp_path: Path,
) -> None:
    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor(
        "MID_A1_TID_53",
        15.0,
        dict_path,
        monitor_incomplete=False,
        euro_emission_category=EuroEmissionCategory.EURO_4,
    )

    assert result.state == Mode06MonitorState.PENDING_FAIL_MARGINAL


def test_mid_key_validation_using_schema(tmp_path: Path) -> None:
    """Mode06MonitorResult Pydantic model enforces the MID key regex."""
    from dtclab.schemas.mode06_result import Mode06MonitorResult

    dict_path = _make_dict(tmp_path)
    result = evaluate_monitor("MID_3D_TID_84", 20.0, dict_path)

    # round-trip through model validation
    validated = Mode06MonitorResult.model_validate(result.model_dump())
    assert validated.monitor_id == "MID_3D_TID_84"


def test_mid_key_rejects_invalid_in_schema() -> None:
    from dtclab.schemas.mode06_result import Mode06MonitorResult

    with pytest.raises(ValueError):
        Mode06MonitorResult(
            monitor_id="bad_key",
            state=Mode06MonitorState.PASSED,
            margin_pct=50.0,
            target_component="Test",
        )


def test_mode06_monitor_result_json_serialisation() -> None:
    from dtclab.schemas.mode06_result import Mode06MonitorResult

    result = Mode06MonitorResult(
        monitor_id="MID_21_TID_81",
        state=Mode06MonitorState.PENDING_FAIL_MARGINAL,
        margin_pct=10.0,
        target_component="Catalyst OSC Bank 1",
    )
    data = result.model_dump()
    assert data["monitor_id"] == "MID_21_TID_81"
    assert data["state"] == "PENDING_FAIL_MARGINAL"
    assert data["margin_pct"] == 10.0
    assert data["target_component"] == "Catalyst OSC Bank 1"


# -- metadata keys are skipped in lookup ----------------------------------------


def test_metadata_keys_not_mistaken_for_mids(tmp_path: Path) -> None:
    dict_path = _make_dict(tmp_path)
    # "_source_wiki" is a metadata key, not a valid MID — lookup returns UNKNOWN
    result = evaluate_monitor("MID_99_TID_01", 30.0, dict_path)
    assert result.target_component == "UNKNOWN"


# -- dictionary load memoization (T-FU-3) ---------------------------------------


def test_dictionary_loaded_at_most_once(tmp_path: Path) -> None:
    """N ≥ 5 monitors against the same dictionary path open the file ≤ 1 time."""
    import builtins

    dict_path = _make_dict(tmp_path)
    opens: dict[str, int] = {}
    _real_open = builtins.open

    def _counting_open(file: object, *args: object, **kwargs: object) -> object:
        opens[str(file)] = opens.get(str(file), 0) + 1
        return _real_open(file, *args, **kwargs)  # pyright: ignore[reportCallIssue, reportArgumentType]

    builtins.open = _counting_open
    try:
        mids = [
            "MID_A1_TID_0B", "MID_A2_TID_0B", "MID_A3_TID_0B",
            "MID_21_TID_81", "MID_3D_TID_84",
        ]
        for mid in mids:
            evaluate_monitor(mid, 50.0, dict_path)
    finally:
        builtins.open = _real_open

    dict_file = str(dict_path)
    n = opens.get(dict_file, 0)
    assert n <= 1, f"dictionary opened {n} times; expected ≤ 1"
