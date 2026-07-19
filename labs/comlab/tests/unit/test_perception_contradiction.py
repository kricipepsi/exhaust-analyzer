"""Unit tests for perception-contradiction detector.

Covers the 5 cases in T-FX-6 Success criteria plus edge cases.
"""

from __future__ import annotations

import pytest

from comlab.core.perception_contradiction import (
    detect,
    detect_compensated_rich,
    select_perception_lambda,
    CompensatedRichResult,
    PerceptionContradictionResult,
    QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM,
    QUALIFIER_RAIL_OUT_OF_BAND,
)
from comlab.schemas.vocabulary import ChemicalSignature, DownstreamTrimRole


# -- Case 1: within tolerance → no bias, delta reported --------------------


def test_no_bias_when_within_tolerance():
    """lambda_chem ≈ normalized_obd_lambda → no bias finding, delta reported."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=1.01, era_lambda_tolerance=0.05)
    assert isinstance(result, PerceptionContradictionResult)
    assert result.lambda_perception_delta == pytest.approx(0.01)
    assert result.bias_verdict is None
    assert result.guard_suppressed is False


def test_no_bias_exact_match():
    """Exact match → zero delta, no bias."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=1.00, era_lambda_tolerance=0.02)
    assert result.lambda_perception_delta == pytest.approx(0.0)
    assert result.bias_verdict is None
    assert result.guard_suppressed is False


def test_no_bias_at_tolerance_boundary():
    """Delta exactly at tolerance → no bias (must exceed, not equal)."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=1.05, era_lambda_tolerance=0.05)
    assert result.bias_verdict is None


# -- Case 2: OBD lambda lean by > tolerance → O2_SENSOR_BIASED_HIGH --------


def test_biased_high_when_obd_lean():
    """normalized_obd_lambda lean by > tolerance → O2_SENSOR_BIASED_HIGH."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=1.12, era_lambda_tolerance=0.02)
    assert result.lambda_perception_delta == pytest.approx(0.12)
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_HIGH
    assert result.guard_suppressed is False


def test_biased_high_modern_tight_tolerance():
    """MODERN era (tolerance=0.02) — small divergence triggers bias."""
    result = detect(lambda_chem=0.99, normalized_obd_lambda=1.02, era_lambda_tolerance=0.02)
    assert result.lambda_perception_delta == pytest.approx(0.03)
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_HIGH


# -- Case 3: OBD lambda rich by > tolerance → O2_SENSOR_BIASED_LOW ----------


def test_biased_low_when_obd_rich():
    """normalized_obd_lambda rich by > tolerance → O2_SENSOR_BIASED_LOW."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=0.88, era_lambda_tolerance=0.02)
    assert result.lambda_perception_delta == pytest.approx(-0.12)
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_LOW
    assert result.guard_suppressed is False


def test_biased_low_legacy_wide_tolerance():
    """LEGACY era (tolerance=0.10) — only large divergence triggers."""
    # Just below tolerance → no bias
    result = detect(lambda_chem=1.00, normalized_obd_lambda=0.91, era_lambda_tolerance=0.10)
    assert result.bias_verdict is None
    # Well below tolerance → bias
    result = detect(lambda_chem=1.00, normalized_obd_lambda=0.85, era_lambda_tolerance=0.10)
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_LOW


# -- Case 4: Lambda Truth guard — suppress when gas chemistry deeply abnormal


def test_guard_suppresses_when_lambda_chem_low():
    """lambda_chem < 0.90 → bias suppressed (real rich mixture dominates)."""
    result = detect(lambda_chem=0.82, normalized_obd_lambda=1.12, era_lambda_tolerance=0.02)
    assert result.guard_suppressed is True
    assert result.bias_verdict is None
    # delta still reported for UI transparency
    assert result.lambda_perception_delta == pytest.approx(0.30)


def test_guard_suppresses_when_lambda_chem_high():
    """lambda_chem > 1.10 → bias suppressed (real lean mixture dominates)."""
    result = detect(lambda_chem=1.18, normalized_obd_lambda=0.88, era_lambda_tolerance=0.02)
    assert result.guard_suppressed is True
    assert result.bias_verdict is None
    assert result.lambda_perception_delta == pytest.approx(-0.30)


def test_guard_boundary_low():
    """lambda_chem exactly at 0.90 → guard NOT triggered (boundary is exclusive)."""
    result = detect(lambda_chem=0.90, normalized_obd_lambda=1.05, era_lambda_tolerance=0.02)
    assert result.guard_suppressed is False
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_HIGH


def test_guard_boundary_high():
    """lambda_chem exactly at 1.10 → guard NOT triggered (boundary is exclusive)."""
    result = detect(lambda_chem=1.10, normalized_obd_lambda=0.95, era_lambda_tolerance=0.02)
    assert result.guard_suppressed is False
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_LOW


# -- Case 5: OBD channel absent → detector inert, no crash -----------------


def test_inert_when_obd_absent():
    """normalized_obd_lambda is None → detector inert, no finding, no crash."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=None, era_lambda_tolerance=0.02)
    assert result.lambda_perception_delta == pytest.approx(0.0)
    assert result.bias_verdict is None
    assert result.guard_suppressed is False


# -- T-COMV2-VPWR-GATE-1: control-module rail pre-check -------------------


def test_vpwr_inert_when_off():
    """Flag-off low rail and flag-on healthy rail preserve the baseline result."""
    baseline = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
    )
    flag_off = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
        control_module_voltage_v=11.0,
        enable_vpwr_gate=False,
    )
    healthy_rail = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
        control_module_voltage_v=14.0,
        enable_vpwr_gate=True,
    )

    assert flag_off == baseline
    assert healthy_rail == baseline
    assert QUALIFIER_RAIL_OUT_OF_BAND not in baseline.qualifiers


def test_vpwr_low_rail_qualifies():
    """A low control-module rail qualifies and suppresses sensor-bias routing."""
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
        control_module_voltage_v=11.0,
        enable_vpwr_gate=True,
    )

    assert result.lambda_perception_delta == pytest.approx(0.12)
    assert result.bias_verdict is None
    assert result.guard_suppressed is False
    assert QUALIFIER_RAIL_OUT_OF_BAND in result.qualifiers


def test_vpwr_high_rail_qualifies():
    """A high control-module rail follows the same qualifier-only suppression path."""
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=0.88,
        era_lambda_tolerance=0.02,
        control_module_voltage_v=15.6,
        enable_vpwr_gate=True,
    )

    assert result.lambda_perception_delta == pytest.approx(-0.12)
    assert result.bias_verdict is None
    assert result.guard_suppressed is False
    assert QUALIFIER_RAIL_OUT_OF_BAND in result.qualifiers


# -- T-FX-7: select_perception_lambda + no-OBD path -----------------------


def test_select_obd_wins_when_present():
    """OBD lambda is returned when both sources are present (OBD wins)."""
    result = select_perception_lambda(normalized_obd_lambda=1.05, lambda_measured=1.12)
    assert result == 1.05



def test_select_falls_back_to_measured_when_obd_absent():
    """GASLab measured lambda is returned when OBD channel absent."""
    result = select_perception_lambda(normalized_obd_lambda=None, lambda_measured=1.12)
    assert result == 1.12


def test_select_returns_none_when_neither_present():
    """None returned when both sources absent -- detector will be inert."""
    result = select_perception_lambda(normalized_obd_lambda=None, lambda_measured=None)
    assert result is None


def test_no_obd_measured_diverges_fires_bias():
    """No OBD channel + lambda_measured diverges beyond tolerance -> bias fires.

    lambda_chem=1.00 (stoich, guard not triggered), lambda_measured=1.12
    (deviation=0.12 > MODERN tolerance 0.02) -> O2_SENSOR_BIASED_HIGH.
    T-FX-7 Success criteria case 1.
    """
    perception = select_perception_lambda(normalized_obd_lambda=None, lambda_measured=1.12)
    result = detect(lambda_chem=1.00, normalized_obd_lambda=perception, era_lambda_tolerance=0.02)
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_HIGH
    assert result.guard_suppressed is False


def test_no_obd_measured_absent_detector_inert():
    """No OBD channel + lambda_measured absent -> detector inert, no crash.

    T-FX-7 Success criteria case 2.
    """
    perception = select_perception_lambda(normalized_obd_lambda=None, lambda_measured=None)
    result = detect(lambda_chem=1.00, normalized_obd_lambda=perception, era_lambda_tolerance=0.02)
    assert result.lambda_perception_delta == pytest.approx(0.0)
    assert result.bias_verdict is None
    assert result.guard_suppressed is False


def test_obd_present_measured_lambda_has_no_effect():
    """OBD channel present -> lambda_measured does not affect delta (OBD wins).

    lambda_chem=1.00, normalized_obd_lambda=1.01 (within tolerance),
    lambda_measured=1.12 (would trigger bias if selected) -> no bias because
    OBD lambda is selected and is within tolerance.
    T-FX-7 Success criteria case 3.
    """
    perception = select_perception_lambda(normalized_obd_lambda=1.01, lambda_measured=1.12)
    result = detect(lambda_chem=1.00, normalized_obd_lambda=perception, era_lambda_tolerance=0.05)
    assert result.bias_verdict is None
    assert result.lambda_perception_delta == pytest.approx(0.01)


# -- Result type is frozen -------------------------------------------------


def test_result_is_frozen():
    """PerceptionContradictionResult is immutable."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=1.00, era_lambda_tolerance=0.02)
    with pytest.raises(Exception):
        result.lambda_perception_delta = 99.0  # type: ignore[misc]


# ===========================================================================
# Downstream-trim-aware perception detector — T-FX-9
# ===========================================================================


# -- Role: NONE (default) — within tolerance, no masking --------------------


def test_downstream_trim_none_within_tolerance():
    """NONE role + within tolerance -> no bias, qualifiers empty."""
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.NONE,
    )
    assert result.bias_verdict is None
    assert result.qualifiers == ()


def test_downstream_trim_none_default_within_tolerance():
    """Default (omitted) role -> qualifiers empty (same as NONE)."""
    result = detect(lambda_chem=1.00, normalized_obd_lambda=1.01, era_lambda_tolerance=0.05)
    assert result.bias_verdict is None
    assert result.qualifiers == ()


# -- Role: CATALYST_MONITOR_ONLY — within tolerance, no masking --------------


def test_downstream_trim_catalyst_monitor_within_tolerance():
    """CATALYST_MONITOR_ONLY + within tolerance -> no bias, qualifiers empty."""
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.CATALYST_MONITOR_ONLY,
    )
    assert result.bias_verdict is None
    assert result.qualifiers == ()


# -- Role: SECONDARY_FUEL_TRIM — within tolerance, MASKED --------------------


def test_downstream_trim_secondary_within_tolerance_masked():
    """SECONDARY_FUEL_TRIM + within tolerance -> no bias BUT masked qualifier.

    Success criterion 4: the in-tolerance agreement is distinguishable from
    CATALYST_MONITOR_ONLY / NONE — the verdict carries a masked-by-downstream-trim
    caveat.
    """
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
    )
    assert result.bias_verdict is None
    assert result.guard_suppressed is False
    assert QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM in result.qualifiers


def test_downstream_trim_secondary_exact_match_masked():
    """SECONDARY_FUEL_TRIM + exact match -> masked (delta=0 within tolerance)."""
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.00,
        era_lambda_tolerance=0.02,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
    )
    assert result.bias_verdict is None
    assert QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM in result.qualifiers


# -- Role: SECONDARY_FUEL_TRIM — beyond tolerance, NOT masked ----------------


def test_downstream_trim_secondary_biased_high_not_masked():
    """SECONDARY_FUEL_TRIM + beyond tolerance (biased high) -> bias fires, qualifiers empty.

    Success criterion 4: a delta beyond tolerance is unaffected by the role —
    a contradiction stays a contradiction.
    """
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
    )
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_HIGH
    assert result.qualifiers == ()


def test_downstream_trim_secondary_biased_low_not_masked():
    """SECONDARY_FUEL_TRIM + beyond tolerance (biased low) -> bias fires, qualifiers empty."""
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=0.88,
        era_lambda_tolerance=0.02,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
    )
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_LOW
    assert result.qualifiers == ()


# -- Role: SECONDARY_FUEL_TRIM — guard suppressed, NOT masked ----------------


def test_downstream_trim_secondary_guard_suppressed_not_masked():
    """SECONDARY_FUEL_TRIM + guard suppressed -> no bias, qualifiers empty.

    The guard fires because gas chemistry is deeply abnormal — the downstream
    trim loop is irrelevant when the mixture itself is way off.
    """
    result = detect(
        lambda_chem=0.82,
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
    )
    assert result.guard_suppressed is True
    assert result.bias_verdict is None
    assert result.qualifiers == ()


# -- Role: SECONDARY_FUEL_TRIM — OBD absent, NOT masked ----------------------


def test_downstream_trim_secondary_obd_absent_not_masked():
    """SECONDARY_FUEL_TRIM + OBD absent -> detector inert, qualifiers empty."""
    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=None,
        era_lambda_tolerance=0.02,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
    )
    assert result.bias_verdict is None
    assert result.lambda_perception_delta == pytest.approx(0.0)
    assert result.qualifiers == ()


# -- Consistency: all three roles produce same bias verdict for same delta ----


def test_downstream_trim_all_roles_same_bias_verdict():
    """All three roles produce O2_SENSOR_BIASED_HIGH for the same beyond-tolerance delta.

    The role only qualifies the in-tolerance case; it does not change the verdict.
    """
    for role in DownstreamTrimRole:
        result = detect(
            lambda_chem=1.00,
            normalized_obd_lambda=1.12,
            era_lambda_tolerance=0.02,
            downstream_trim_role=role,
        )
        assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_HIGH
        assert result.qualifiers == ()


# ===========================================================================
# Compensated-rich detector — T-P6-6c
# ===========================================================================


# -- Core AND gate: fires when all 3 conditions met --------------------------


def test_compensated_rich_fires_all_gates_pass():
    """λ=1.01, trim=-27, P0172, OBD=0.92, MODERN tol=0.05 → fires with confidence boost."""
    result = detect_compensated_rich(
        lambda_chem=1.01,
        total_trim_correction_delta=-27.0,
        obd_lambda=0.92,
        era_lambda_tolerance=0.05,  # MODERN
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    # δ = 0.92 − 1.01 = −0.09, −δ = 0.09 > 0.05 → boosted
    assert result.confidence == pytest.approx(0.90)


def test_compensated_rich_fires_obd_small_delta():
    """CASE-025 pattern: λ=1.00, trim=-30, P0172, small OBD delta → fires at base confidence."""
    result = detect_compensated_rich(
        lambda_chem=1.00,
        total_trim_correction_delta=-30.0,
        obd_lambda=0.97,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    assert result.confidence == pytest.approx(0.75)  # small Δ, no confidence boost


def test_compensated_rich_fires_obd_none():
    """OBD lambda absent → fires at base confidence (trim + DTC carry the signal)."""
    result = detect_compensated_rich(
        lambda_chem=1.00,
        total_trim_correction_delta=-20.0,
        obd_lambda=None,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    assert result.confidence == pytest.approx(0.75)


# -- Gate 1: lambda_chem window --------------------------------------------------


def test_compensated_rich_suppressed_lambda_below_window():
    """λ_chem < 0.95 (genuinely rich) → suppressed."""
    result = detect_compensated_rich(
        lambda_chem=0.92,
        total_trim_correction_delta=-20.0,
        obd_lambda=0.90,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is False


def test_compensated_rich_suppressed_lambda_above_window():
    """λ_chem > 1.05 (genuinely lean — case_013) → suppressed."""
    result = detect_compensated_rich(
        lambda_chem=1.08,
        total_trim_correction_delta=-38.0,
        obd_lambda=0.92,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is False


def test_compensated_rich_boundary_low_included():
    """λ_chem = 0.95 (boundary) → fires."""
    result = detect_compensated_rich(
        lambda_chem=0.95,
        total_trim_correction_delta=-20.0,
        obd_lambda=0.92,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True


def test_compensated_rich_boundary_high_included():
    """λ_chem = 1.05 (boundary) → fires."""
    result = detect_compensated_rich(
        lambda_chem=1.05,
        total_trim_correction_delta=-20.0,
        obd_lambda=0.95,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True


# -- Gate 2: trim threshold --------------------------------------------------


def test_compensated_rich_suppressed_trim_at_threshold():
    """trim = −15.0 (at threshold, not below) → suppressed."""
    result = detect_compensated_rich(
        lambda_chem=1.01,
        total_trim_correction_delta=-15.0,
        obd_lambda=0.95,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is False


def test_compensated_rich_suppressed_trim_normal():
    """trim = −5.0 (normal) → suppressed."""
    result = detect_compensated_rich(
        lambda_chem=1.00,
        total_trim_correction_delta=-5.0,
        obd_lambda=1.00,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is False


# -- Gate 3: rich DTC --------------------------------------------------------


def test_compensated_rich_suppressed_no_rich_dtc():
    """No P0172/P0175 → suppressed even with railed trim."""
    result = detect_compensated_rich(
        lambda_chem=1.01,
        total_trim_correction_delta=-25.0,
        obd_lambda=0.95,
        era_lambda_tolerance=0.10,
        rich_dtc_present=False,
    )
    assert result.is_compensated_rich is False


# -- Confidence modifier -----------------------------------------------------


def test_compensated_rich_confidence_boosted_obd_richer():
    """OBD reads richer than truth beyond tolerance → confidence 0.90."""
    result = detect_compensated_rich(
        lambda_chem=1.02,
        total_trim_correction_delta=-28.0,
        obd_lambda=0.94,
        era_lambda_tolerance=0.05,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    # δ = 0.94 − 1.02 = −0.08, −δ = 0.08 > 0.05 → boosted
    assert result.confidence == pytest.approx(0.90)


def test_compensated_rich_confidence_not_boosted_obd_leaner():
    """OBD reads leaner than truth → no boost (wrong direction)."""
    result = detect_compensated_rich(
        lambda_chem=0.97,
        total_trim_correction_delta=-20.0,
        obd_lambda=1.05,
        era_lambda_tolerance=0.05,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    # δ = 1.05 − 0.97 = +0.08 → OBD leaner, not richer → no boost
    assert result.confidence == pytest.approx(0.75)


# -- Known false positive: case_038 -----------------------------------------


def test_compensated_rich_case_038_false_positive():
    """case_038 (λ=1.00, trim=-27, P0172, OBD=0.92) → fires (known limitation).

    T-P6-6a: case_038 is a dual-sensor fault (MAF+O2 cancel), not a real
    compensated-rich.  The detector cannot discriminate this from EXT-203
    without sensor-health data that COMLab doesn't receive.
    """
    result = detect_compensated_rich(
        lambda_chem=1.00,
        total_trim_correction_delta=-27.0,
        obd_lambda=0.92,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    # Δ = 0.92 − 1.00 = −0.08, −Δ = 0.08 > ... no, LEGACY tolerance is 0.10
    # 0.08 < 0.10 → no confidence boost, stays at base
    assert result.confidence == pytest.approx(0.75)


# -- Result type is mutable (unlike PerceptionContradictionResult) -----------


def test_compensated_rich_result_is_mutable():
    """CompensatedRichResult is intentionally mutable — router may adjust confidence."""
    result = CompensatedRichResult()
    result.is_compensated_rich = True
    result.confidence = 0.85
    assert result.is_compensated_rich is True


# -- T-P6-6a pattern-confirmation cases --------------------------------------


def test_ext_203_canonical():
    """EXT-203: λ=1.01, trim=-27, P0172, Δ=−0.06, LEGACY tol=0.10 → fires at base."""
    result = detect_compensated_rich(
        lambda_chem=1.01,
        total_trim_correction_delta=-27.0,
        obd_lambda=0.95,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    # Δ = −0.06, |Δ| = 0.06 < 0.10 → no confidence boost
    assert result.confidence == pytest.approx(0.75)


def test_ext_206_evap_purge():
    """EXT-206: λ=1.02, trim=-28, P0172, Δ=−0.08 → fires at base (Δ < tol 0.10)."""
    result = detect_compensated_rich(
        lambda_chem=1.02,
        total_trim_correction_delta=-28.0,
        obd_lambda=0.94,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    assert result.confidence == pytest.approx(0.75)


def test_case_025_evap_purge_valve():
    """CASE-025: λ=1.00, trim=-30, P0172, Δ=−0.03 → fires at base."""
    result = detect_compensated_rich(
        lambda_chem=1.00,
        total_trim_correction_delta=-30.0,
        obd_lambda=0.97,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is True
    assert result.confidence == pytest.approx(0.75)


def test_case_013_ecu_inversion_suppressed():
    """case_013: λ=1.08 > 1.05 → suppressed (genuinely lean, ECU logic inversion)."""
    result = detect_compensated_rich(
        lambda_chem=1.08,
        total_trim_correction_delta=-38.0,
        obd_lambda=0.92,
        era_lambda_tolerance=0.10,
        rich_dtc_present=True,
    )
    assert result.is_compensated_rich is False


# ===========================================================================
# De-cat + secondary trim incoherence — T-FX-11
# ===========================================================================


def test_decat_secondary_trim_within_tolerance_incoherent():
    """De-cat + SECONDARY_FUEL_TRIM → DECAT_SECONDARY_TRIM_INCOHERENT qualifier.

    T-FX-11 Success criterion 4: the incoherence qualifier fires regardless of
    the lambda delta — it is a configuration-level check, not a signal-level one.
    Even when perception/truth agree, the configuration is physically impossible.
    """
    from comlab.core.perception_contradiction import (
        QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT,
        QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM,
    )

    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
        has_catalyst=False,
    )
    assert result.bias_verdict is None
    assert QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT in result.qualifiers
    assert QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM in result.qualifiers


def test_decat_secondary_trim_biased_still_incoherent():
    """De-cat + SECONDARY_FUEL_TRIM → incoherent even when bias fires.

    The configuration incoherence qualifier is independent of the bias verdict.
    """
    from comlab.core.perception_contradiction import (
        QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT,
    )

    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
        has_catalyst=False,
    )
    assert result.bias_verdict is ChemicalSignature.O2_SENSOR_BIASED_HIGH
    assert QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT in result.qualifiers


def test_decat_none_role_no_incoherence():
    """De-cat + NONE role → no incoherence (secondary loop not present)."""
    from comlab.core.perception_contradiction import (
        QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT,
    )

    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.NONE,
        has_catalyst=False,
    )
    assert result.bias_verdict is None
    assert QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT not in result.qualifiers


def test_decat_catalyst_monitor_no_incoherence():
    """De-cat + CATALYST_MONITOR_ONLY → no incoherence.

    CATALYST_MONITOR_ONLY is a monitoring role, not a trim loop — the
    incoherence only applies to SECONDARY_FUEL_TRIM which depends on
    catalyst oxygen buffering.
    """
    from comlab.core.perception_contradiction import (
        QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT,
    )

    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.CATALYST_MONITOR_ONLY,
        has_catalyst=False,
    )
    assert result.bias_verdict is None
    assert QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT not in result.qualifiers


def test_has_catalyst_secondary_trim_no_incoherence():
    """Catalyst present + SECONDARY_FUEL_TRIM → MASKED but NOT incoherent.

    The incoherence qualifier only fires when the catalyst is absent.
    """
    from comlab.core.perception_contradiction import (
        QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT,
        QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM,
    )

    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
        has_catalyst=True,
    )
    assert result.bias_verdict is None
    assert QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM in result.qualifiers
    assert QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT not in result.qualifiers


def test_decat_secondary_trim_guard_suppressed_still_incoherent():
    """De-cat + SECONDARY_FUEL_TRIM → incoherent even with guard suppressed.

    The configuration incoherence survives the Lambda Truth guard because it
    is a hardware-configuration finding, not a signal-level finding.
    """
    from comlab.core.perception_contradiction import (
        QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT,
    )

    result = detect(
        lambda_chem=0.82,  # Guard triggers (λ < 0.90)
        normalized_obd_lambda=1.12,
        era_lambda_tolerance=0.02,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
        has_catalyst=False,
    )
    assert result.guard_suppressed is True
    assert result.bias_verdict is None
    assert QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT in result.qualifiers


def test_decat_default_has_catalyst_true():
    """Default has_catalyst=True preserves existing behaviour."""
    from comlab.core.perception_contradiction import (
        QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT,
    )

    result = detect(
        lambda_chem=1.00,
        normalized_obd_lambda=1.01,
        era_lambda_tolerance=0.05,
        downstream_trim_role=DownstreamTrimRole.SECONDARY_FUEL_TRIM,
    )
    assert QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT not in result.qualifiers
