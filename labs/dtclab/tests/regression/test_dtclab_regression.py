"""Regression tests wired to the DTCLab case corpus.

Each case is a standalone JSON fixture under ``fixtures/``.  The test
parametrizes over all ``case_*.json`` files, constructs the appropriate
``DataFusionSanitizer`` (with or without a typed ``DtcLabDnaView``), runs
the full pipeline, and asserts routing tags, historical fault context,
and derived freeze-frame flags against expected values.

Source: DTC_VOCABULARY.md §11, §17.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from dtclab import DataFusionSanitizer
from dtclab.schemas.dna_view import DtcLabDnaView
from dtclab.schemas.vocabulary import DTCRoutingTag, HistoricalFaultContext

_FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ------------------------------------------------------------------
# Fixture discovery
# ------------------------------------------------------------------


def _discover_fixture_paths() -> list[Path]:
    """Return all case_*.json fixture files sorted by name."""
    return sorted(_FIXTURES_DIR.glob("case_*.json"))


def _load_fixture(path: Path) -> dict[str, Any]:
    """Load a single JSON fixture file."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ------------------------------------------------------------------
# Parametrized regression suite
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_path",
    _discover_fixture_paths(),
    ids=lambda p: p.stem,
)
def test_regression_case(fixture_path: Path):
    """Run a single regression case through the full DTCLab pipeline."""
    data = _load_fixture(fixture_path)

    # --- Build DNA view ---------------------------------------------------
    dna_view: DtcLabDnaView | None = None
    dna_json = data.get("dna_view_json")
    if dna_json is not None:
        dna_view = DtcLabDnaView.model_validate(dna_json)

    # --- Build sanitizer kwargs -------------------------------------------
    kwargs = data.get("sanitize_kwargs", {})

    # --- Run pipeline -----------------------------------------------------
    sanitizer = DataFusionSanitizer(dna_view)
    payload = sanitizer.sanitize(
        raw_dtcs=data["raw_dtcs"],
        raw_freeze_frame=data["raw_freeze_frame"],
        raw_mode06=data.get("raw_mode06", {}),
        codes_cleared=kwargs.get("codes_cleared", False),
        active_mil=kwargs.get("active_mil", False),
        mil_flashing=kwargs.get("mil_flashing", False),
    )

    # --- Assert routing tags — exact set equality -------------------------
    expected_tags = [DTCRoutingTag(t) for t in data["expected_routing_tags"]]
    assert set(payload.routing_tags) == set(expected_tags), (
        f"[{fixture_path.stem}] Routing tag mismatch: "
        f"expected {sorted(t.value for t in expected_tags)}, "
        f"got {sorted(t.value for t in payload.routing_tags)}"
    )

    # --- Assert historical fault context ----------------------------------
    expected_hfc = HistoricalFaultContext(data["expected_hfc"])
    assert payload.historical_fault_context == expected_hfc, (
        f"[{fixture_path.stem}] Expected HFC {expected_hfc.value}, "
        f"got {payload.historical_fault_context.value}"
    )

    # --- Assert derived flags ---------------------------------------------
    expected_flags: dict[str, bool] = data.get("expected_flags", {})
    ff = payload.freeze_frame
    for flag_name, expected_value in expected_flags.items():
        actual = getattr(ff, flag_name)
        assert actual == expected_value, (
            f"[{fixture_path.stem}] Flag {flag_name}: "
            f"expected {expected_value}, got {actual}"
        )

    # --- Assert payload structural validity -------------------------------
    assert isinstance(payload.confirmed_dtcs, list)
    assert isinstance(payload.pending_dtcs, list)
    assert isinstance(payload.permanent_dtcs, list)
    assert isinstance(payload.routing_tags, list)
    assert isinstance(payload.mode_06_monitors, dict)
    assert isinstance(payload.freeze_frame.coolant_temp_c, float)
    assert isinstance(payload.freeze_frame.short_term_ft1, float)
    assert isinstance(payload.freeze_frame.long_term_ft1, float)


# ------------------------------------------------------------------
# Suite sanity checks
# ------------------------------------------------------------------


def test_all_fixture_files_loadable():
    """Every JSON fixture file is valid JSON and has required keys."""
    required = {"raw_dtcs", "raw_freeze_frame", "expected_routing_tags", "expected_hfc"}
    paths = _discover_fixture_paths()
    assert len(paths) >= 5, f"Expected >= 5 fixtures, found {len(paths)}"

    for path in paths:
        data = _load_fixture(path)
        missing = required - set(data.keys())
        assert not missing, f"[{path.stem}] Missing required keys: {missing}"


def test_dna_injection_coverage():
    """At least one fixture uses a HIGH-confidence DNA view and at least
    one uses dna_view_json=null (the pre-DNA fallback)."""
    dna_fixtures = 0
    null_fixtures = 0
    for path in _discover_fixture_paths():
        data = _load_fixture(path)
        if data.get("dna_view_json") is not None:
            dna_fixtures += 1
        else:
            null_fixtures += 1
    assert dna_fixtures >= 1, "Need >= 1 fixture with dna_view_json set"
    assert null_fixtures >= 1, "Need >= 1 fixture with dna_view_json=null"


def test_case04_mode06_critical_fail():
    """Case 04 (non-start) specifically asserts MID_21_TID_81 is CRITICAL_FAIL."""
    path = _FIXTURES_DIR / "case_04_nonstart_mode06.json"
    assert path.exists(), "case_04 fixture missing"

    data = _load_fixture(path)
    sanitizer = DataFusionSanitizer(None)
    payload = sanitizer.sanitize(
        raw_dtcs=data["raw_dtcs"],
        raw_freeze_frame=data["raw_freeze_frame"],
        raw_mode06=data.get("raw_mode06", {}),
    )

    monitor = payload.mode_06_monitors.get("MID_21_TID_81")
    assert monitor is not None, "MID_21_TID_81 not in mode_06_monitors"
    assert monitor.state.value == "CRITICAL_FAIL", (
        f"Expected CRITICAL_FAIL, got {monitor.state.value}"
    )


def test_case05_trim_values_present():
    """Case 05 (self-healing delta) asserts STFT +22 and LTFT +11 are
    present in the freeze_frame output so COMLab can compute delta_Healing."""
    path = _FIXTURES_DIR / "case_05_selfheal_delta_inputs.json"
    assert path.exists(), "case_05 fixture missing"

    data = _load_fixture(path)
    sanitizer = DataFusionSanitizer(None)
    kwargs = data.get("sanitize_kwargs", {})
    payload = sanitizer.sanitize(
        raw_dtcs=data["raw_dtcs"],
        raw_freeze_frame=data["raw_freeze_frame"],
        raw_mode06=data.get("raw_mode06", {}),
        codes_cleared=kwargs.get("codes_cleared", False),
        active_mil=kwargs.get("active_mil", False),
    )

    assert payload.freeze_frame.short_term_ft1 == 22.0, (
        f"STFT1 expected 22.0, got {payload.freeze_frame.short_term_ft1}"
    )
    assert payload.freeze_frame.long_term_ft1 == 11.0, (
        f"LTFT1 expected 11.0, got {payload.freeze_frame.long_term_ft1}"
    )
    assert payload.freeze_frame.ff_codes_cleared_invalidated is True
