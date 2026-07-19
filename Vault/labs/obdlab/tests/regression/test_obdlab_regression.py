"""Regression test suite for OBDLab — parametrized over JSON fixture files.

Each fixture exercises the full SensorSignalTranslator pipeline end-to-end
with real-ish input values derived from OBDLab_KG_Wiki.md §13–§17 fault profiles.

Covers: HIGH-confidence DNA, dna_view=None, PARTIAL-confidence DNA.
"""

import json
import math
from enum import Enum
from pathlib import Path

import pytest

from obdlab.core.sensor_signal_translator import SensorSignalTranslator
from obdlab.schemas.dna_view import ObdLabDnaView
from obdlab.schemas.payload import OBDLivePayload

_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def _load_fixture_files():
    """Yield (case_id, fixture_dict) for every JSON file in fixtures/."""
    for fpath in sorted(_FIXTURES_DIR.glob("*.json")):
        with open(fpath, encoding="utf-8") as fh:
            yield fpath.stem, json.load(fh)


def _resolve_expected(fixture, key):
    """Resolve an expected value, supporting the '_approx' suffix for float tolerance."""
    expected = fixture["expected_payload_subset"]
    exact = expected.get(key)
    if exact is not None:
        return exact, False
    approx_key = f"{key}_approx"
    approx_val = expected.get(approx_key)
    if approx_val is not None:
        return approx_val, True
    return None, False


def _assert_field(payload, field, expected, is_approx):
    """Assert a single payload field against expected value."""
    actual = getattr(payload, field)

    if expected is None:
        assert actual is None, f"{field}: expected None, got {actual}"
        return

    # Enum fields: compare .value (string) against expected string
    if isinstance(actual, Enum):
        actual = actual.value

    if is_approx:
        assert actual == pytest.approx(expected, abs=1e-4), (
            f"{field}: expected ~{expected}, got {actual}"
        )
    elif isinstance(expected, float):
        if math.isnan(expected):
            assert math.isnan(actual), f"{field}: expected NaN, got {actual}"
        else:
            assert actual == pytest.approx(expected, abs=1e-6), (
                f"{field}: expected {expected}, got {actual}"
            )
    else:
        assert actual == expected, (
            f"{field}: expected {expected!r}, got {actual!r}"
        )


@pytest.fixture(scope="class")
def translator():
    return SensorSignalTranslator()


class TestOBDLabRegression:
    """Parametrized regression suite — one test per fixture JSON file."""

    @pytest.mark.parametrize(
        "case_id,fixture",
        [pytest.param(stem, data, id=stem) for stem, data in _load_fixture_files()],
    )
    def test_regression_case(self, translator, case_id, fixture):
        """Run a single regression case: translate inputs → assert expected subset."""
        raw_inputs = fixture["raw_user_inputs"]
        dna_json = fixture["dna_view_json"]

        dna_view = ObdLabDnaView.model_validate(dna_json) if dna_json is not None else None

        payload = translator.translate(raw_inputs, dna_view)

        assert isinstance(payload, OBDLivePayload), (
            f"Expected OBDLivePayload, got {type(payload).__name__}"
        )

        # Assert every field in expected_payload_subset
        expected = fixture["expected_payload_subset"]
        for field_name in expected:
            if field_name.endswith("_approx"):
                continue
            expected_val, is_approx = _resolve_expected(fixture, field_name)
            _assert_field(payload, field_name, expected_val, is_approx)

        # Round-trip JSON
        json_str = payload.model_dump_json()
        reloaded = OBDLivePayload.model_validate_json(json_str)
        assert reloaded == payload, "model_dump_json → model_validate_json round-trip failed"

    def test_fixture_count(self):
        """At least 5 regression fixtures are present."""
        files = list(_FIXTURES_DIR.glob("*.json"))
        assert len(files) >= 5, f"Expected >= 5 fixture files, found {len(files)}"


def test_dna_confidence_coverage():
    """Verify regression fixtures cover HIGH, None, and PARTIAL DNA confidence."""
    confidences = set()
    for _, fixture in _load_fixture_files():
        dna_json = fixture["dna_view_json"]
        if dna_json is None:
            confidences.add("NONE")
        else:
            confidences.add(dna_json.get("confidence", "missing"))
    assert "HIGH" in confidences, "Missing fixture with HIGH-confidence DNA"
    assert "NONE" in confidences, "Missing fixture with dna_view_json=null"
    assert "PARTIAL" in confidences, "Missing fixture with PARTIAL-confidence DNA"
