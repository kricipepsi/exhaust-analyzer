import json
from pathlib import Path

import pytest

from obdlab.core.exceptions import PIDValidationError, SemanticConsistencyError
from obdlab.core.sensor_signal_translator import SensorSignalTranslator
from obdlab.schemas.dna_view import ObdLabDnaView
from obdlab.schemas.vocabulary import O2FailureMode, VEValidity

_LOGSET_PATH = Path(__file__).resolve().parent / "logset.json"


def _load_sourced_cases():
    """Load sourced cases from logset.json."""
    with open(_LOGSET_PATH, encoding="utf-8") as fh:
        cases = json.load(fh)
    return cases


def parse_comparison(actual: float, expected_expr: str | float) -> bool:
    """Helper to parse threshold-string comparison rules (e.g. '>+15', '<50')."""
    if isinstance(expected_expr, (int, float)):
        return abs(actual - expected_expr) < 1e-4

    expr = expected_expr.strip()
    if expr.startswith(">+"):
        return actual > float(expr[2:])
    elif expr.startswith(">"):
        return actual > float(expr[1:])
    elif expr.startswith("<+"):
        return actual < float(expr[2:])
    elif expr.startswith("<"):
        return actual < float(expr[1:])
    elif expr.startswith("=="):
        return abs(actual - float(expr[2:])) < 1e-4
    else:
        return abs(actual - float(expr)) < 1e-4


@pytest.mark.parametrize(
    "case",
    _load_sourced_cases(),
    ids=lambda c: c["case_id"]
)
def test_pid_logset_case(case):
    """Run SensorSignalTranslator.translate on each case and assert expected results."""
    translator = SensorSignalTranslator()

    dna_json = case["dna_view"]
    raw_pids = case["raw_pids"]
    dna_view = ObdLabDnaView.model_validate(dna_json)

    if "expected_rejection" in case:
        rejection = case["expected_rejection"]
        err_type_str = rejection["error_type"]

        # Map error type string to actual Exception class
        if err_type_str == "PIDValidationError":
            err_class = PIDValidationError
        elif err_type_str == "SemanticConsistencyError":
            err_class = SemanticConsistencyError
        else:
            raise ValueError(f"Unknown expected error type: {err_type_str}")

        with pytest.raises(err_class):
            translator.translate(raw_pids, dna_view)

    else:
        # Expected success path
        payload = translator.translate(raw_pids, dna_view)
        sig = case["expected_obd_signature"]

        # 1. Assert on exact match enum/string fields
        assert payload.rpm_state_bucket.value == sig["rpm_state_bucket"], (
            f"rpm_state_bucket mismatch: expected {sig['rpm_state_bucket']}, got {payload.rpm_state_bucket.value}"
        )
        assert payload.ve_validity.value == sig["ve_validity"], (
            f"ve_validity mismatch: expected {sig['ve_validity']}, got {payload.ve_validity.value}"
        )
        assert payload.trim_analytics_gate.value == sig["trim_analytics_gate"], (
            f"trim_analytics_gate mismatch: expected {sig['trim_analytics_gate']}, got {payload.trim_analytics_gate.value}"
        )

        # 2. Assert on normalized_obd_lambda within ±0.02 tolerance
        assert payload.normalized_obd_lambda == pytest.approx(sig["normalized_obd_lambda"], abs=0.02), (
            f"normalized_obd_lambda mismatch: expected ~{sig['normalized_obd_lambda']}, got {payload.normalized_obd_lambda}"
        )

        # 3. Assert on total_trim_correction_delta using threshold/exact parser
        assert parse_comparison(payload.total_trim_correction_delta, sig["total_trim_correction_delta"]), (
            f"total_trim_correction_delta mismatch: expected expression {sig['total_trim_correction_delta']}, got {payload.total_trim_correction_delta}"
        )

        # 4. If o2_channel_fault expected, verify O2 normalizer clamped or flagged failure
        if sig.get("o2_channel_fault"):
            # O2 failure mode should be flagged or lambda should be at boundaries (0.7 / 1.3)
            is_clamped = payload.normalized_obd_lambda in (0.7, 1.3)
            is_flagged = payload.o2_failure_mode != O2FailureMode.NO_FAULT
            assert is_clamped or is_flagged, (
                f"o2_channel_fault expected True but payload was not clamped or flagged: lambda={payload.normalized_obd_lambda}, failure={payload.o2_failure_mode}"
            )


def test_coverage_matrix_and_aggregate_rate():
    """Verify the 8-cell coverage matrix and that all-default shape is < 5% of non-rejections."""
    cases = _load_sourced_cases()
    non_rejections = [c for c in cases if "expected_rejection" not in c]
    rejections = [c for c in cases if "expected_rejection" in c]

    # 1. VE Routing branches (MAF_ONLY, MAP_ONLY_SPEED_DENSITY, DUAL_MAF_MAP_CROSSCHECK)
    strategies = {c["dna_view"]["air_metering_strategy"] for c in non_rejections}
    assert "MAF_ONLY" in strategies
    assert "MAP_ONLY_SPEED_DENSITY" in strategies
    assert "DUAL_MAF_MAP_CROSSCHECK" in strategies

    # 2. Upstream O2 sensor types (NARROWBAND_0_TO_1V, WIDEBAND_LINEAR, WIDEBAND_NB_SIM)
    o2_types = {c["dna_view"]["upstream_o2_type"] for c in non_rejections}
    assert "NARROWBAND_0_TO_1V" in o2_types
    assert "WIDEBAND_LINEAR" in o2_types
    assert "WIDEBAND_NB_SIM" in o2_types

    # 3. Lambda outcomes (lean, stoich, rich, clamp/fault)
    lambdas = {c["expected_obd_signature"]["normalized_obd_lambda"] for c in non_rejections}
    assert any(lam > 1.01 for lam in lambdas)   # lean
    assert any(abs(lam - 1.0) < 1e-4 for lam in lambdas)  # stoich
    assert any(lam < 0.99 for lam in lambdas)   # rich
    assert any(c["expected_obd_signature"].get("o2_channel_fault") for c in non_rejections)  # clamp/fault

    # 4. Fuel-trim outcomes (healthy/near-zero, large positive, large negative)
    trims = [c["expected_obd_signature"]["total_trim_correction_delta"] for c in non_rejections]
    assert any(isinstance(t, (int, float)) and abs(t) < 5.0 for t in trims)  # near-zero
    assert any(isinstance(t, (int, float)) and t > 15.0 for t in trims)    # large positive
    assert any(isinstance(t, (int, float)) and t < -15.0 for t in trims)   # large negative

    # 5. VE validity faults (collapse, contamination, skew)
    ve_validities = {c["expected_obd_signature"]["ve_validity"] for c in non_rejections}
    assert "FAULT_VE_IDLE_COLLAPSE" in ve_validities
    assert "FAULT_MAF_CONTAMINATION" in ve_validities
    assert "FAULT_VE_SENSOR_SKEW" in ve_validities

    # 6. RPM/thermal states (stabilized, regulatory high, stress, cold start)
    buckets = {c["expected_obd_signature"]["rpm_state_bucket"] for c in non_rejections}
    assert "STABILIZED_IDLE" in buckets
    assert "REGULATORY_HIGH_IDLE" in buckets
    assert "STRESS_IDLE" in buckets
    assert "COLD_OPEN_LOOP_INVALID" in buckets

    # 7. Trim analytics gates (VALID, ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE)
    gates = {c["expected_obd_signature"]["trim_analytics_gate"] for c in non_rejections}
    assert "VALID" in gates
    assert "ENGINE_COLD" in gates
    assert "OPEN_LOOP" in gates
    assert "O2_FAULT_ACTIVE" in gates
    assert "CKP_CMP_FAULT_ACTIVE" in gates
    assert "CODES_RECENTLY_CLEARED" in gates
    assert "WOT_ACTIVE" in gates
    assert "DFCO_ACTIVE" in gates

    # 8. Boundary / rejection cases
    rejection_reasons = {c["expected_rejection"]["reason"] for c in rejections}
    assert any("outside bounds" in r for r in rejection_reasons)
    assert any("must be null" in r for r in rejection_reasons)
    assert any("exceeds DNA" in r for r in rejection_reasons)
    assert any("Physics_Gate_1" in r for r in rejection_reasons)
    assert any("Physics_Gate_2" in r for r in rejection_reasons)

    # 9. Fault families
    families = {c["fault_family"] for c in non_rejections}
    assert "lean_condition" in families
    assert "rich_condition" in families
    assert "mechanical_wear" in families
    assert "sensor_fault" in families
    assert "no_fault" in families

    # 10. Aggregate anti-regression: strictly fewer than 5% default shape
    translator = SensorSignalTranslator()
    default_count = 0
    for case in non_rejections:
        payload = translator.translate(case["raw_pids"], ObdLabDnaView.model_validate(case["dna_view"]))
        if (
            payload.o2_failure_mode == O2FailureMode.NO_FAULT
            and payload.ve_pct == 0.0
            and payload.ve_validity == VEValidity.UNKNOWN
            and payload.total_trim_correction_delta == 0.0
        ):
            default_count += 1

    default_pct = (default_count / len(non_rejections)) * 100.0
    print(f"\nDefault shape count: {default_count} / {len(non_rejections)} ({default_pct:.2f}%)")
    assert default_pct < 5.0, f"Default shape rate too high: {default_pct:.2f}%"
