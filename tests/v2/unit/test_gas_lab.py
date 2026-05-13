"""Unit tests for gas_lab.py (M2) — Brettschneider, per-state symptom detection,
dual-state delta, NOx probe gate, baseline deviation, cam timing re-threshold.

source: v2-gas-chemistry §1–§6.
"""

from __future__ import annotations

import pytest

from engine.v2.dna_core import DNAOutput
from engine.v2.gas_lab import (
    GasLabOutput,
    _brettschneider,
    _compute_dual_state_delta,
    _detect_gas_symptoms,
    analyse_gas,
)
from engine.v2.input_model import (
    DiagnosticInput,
    GasRecord,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)

# ── helpers ─────────────────────────────────────────────────────────────────


def _gas(
    co_pct: float = 0.0,
    hc_ppm: float = 0.0,
    co2_pct: float = 0.0,
    o2_pct: float = 0.0,
    nox_ppm: float | None = None,
) -> GasRecord:
    return GasRecord(
        co_pct=co_pct,
        hc_ppm=hc_ppm,
        co2_pct=co2_pct,
        o2_pct=o2_pct,
        nox_ppm=nox_ppm,
    )


def _ctx(engine_code: str = "EA111_1.2_TSI", my: int = 2012) -> VehicleContext:
    return VehicleContext(
        brand="VOLKSWAGEN",
        model="Golf",
        engine_code=engine_code,
        displacement_cc=1197,
        my=my,
    )


def _validated(
    gas_idle: GasRecord | None = None,
    gas_high: GasRecord | None = None,
    nox_suppressed: bool = False,
    obd: OBDRecord | None = None,
) -> ValidatedInput:
    return ValidatedInput(
        raw=DiagnosticInput(
            vehicle_context=_ctx(),
            dtcs=[],
            analyser_type="4-gas" if nox_suppressed else "5-gas",
            gas_idle=gas_idle,
            gas_high=gas_high,
            obd=obd,
        ),
        valid_channels={"gas_idle", "gas_high"},
        nox_suppressed=nox_suppressed,
    )


def _dna(
    target_lambda: float = 1.000,
    target_rpm: int = 2500,
    era_bucket: str = "ERA_CAN",
    engine_state: str = "warm_closed_loop",
) -> DNAOutput:
    return DNAOutput(
        engine_state=engine_state,
        era_bucket=era_bucket,
        tech_mask={},
        o2_type="WB",
        target_rpm_u2=target_rpm,
        target_lambda_v112=target_lambda,
        vref_missing=False,
        confidence_ceiling=1.00,
    )


# ── _detect_gas_symptoms: lambda ────────────────────────────────────────────
# source: v2-gas-chemistry §2 — lambda thresholds at 0.97 and 1.03


def test_lambda_rich_below_097():
    """λ < 0.97 → SYM_LAMBDA_LOW."""
    gas = _gas(co_pct=3.0, hc_ppm=100.0, co2_pct=12.0, o2_pct=0.3)
    lamb = _brettschneider(gas)
    assert lamb < 0.97, f"precondition failed: λ={lamb}"
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_LAMBDA_LOW" in symptoms
    assert "SYM_LAMBDA_HIGH" not in symptoms
    assert "SYM_LAMBDA_NORMAL" not in symptoms


def test_lambda_lean_above_103():
    """λ > 1.03 → SYM_LAMBDA_HIGH."""
    gas = _gas(co_pct=0.02, hc_ppm=30.0, co2_pct=14.0, o2_pct=3.0)
    lamb = _brettschneider(gas)
    assert lamb > 1.03, f"precondition failed: λ={lamb}"
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_LAMBDA_HIGH" in symptoms
    assert "SYM_LAMBDA_LOW" not in symptoms


def test_lambda_normal_range():
    """0.97 ≤ λ ≤ 1.03 → SYM_LAMBDA_NORMAL."""
    gas = _gas(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=0.8)
    lamb = _brettschneider(gas)
    assert 0.97 <= lamb <= 1.03, f"precondition failed: λ={lamb}"
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_LAMBDA_NORMAL" in symptoms


# ── _detect_gas_symptoms: HC ────────────────────────────────────────────────
# source: v2-gas-chemistry §2 — HC > 600 ppm → SYM_HC_MISFIRE


def test_hc_high_above_600():
    """HC > 600 ppm → SYM_HC_HIGH."""
    gas = _gas(co_pct=0.5, hc_ppm=601.0, co2_pct=14.0, o2_pct=1.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_HC_HIGH" in symptoms
    assert "SYM_HC_LOW" not in symptoms


def test_hc_low_below_600():
    """HC ≤ 600 ppm → SYM_HC_LOW."""
    gas = _gas(co_pct=0.5, hc_ppm=600.0, co2_pct=14.0, o2_pct=1.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_HC_HIGH" not in symptoms
    assert "SYM_HC_LOW" in symptoms


def test_hc_at_threshold_boundary():
    """HC at exactly 600 ppm is LOW (≤ threshold)."""
    gas = _gas(co_pct=0.5, hc_ppm=600.0, co2_pct=14.0, o2_pct=1.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_HC_HIGH" not in symptoms
    assert "SYM_HC_LOW" in symptoms


# ── _detect_gas_symptoms: HC — GDI threshold ─────────────────────────────────
# source: master_gas_guide.md §6.2 GDI footnote — GDI HC threshold = 900 ppm
# source: VIN_ENGINE_CONNECTION_REVIEW.md Fix C


@pytest.mark.parametrize(
    "has_gdi, hc_ppm, expect_high",
    [
        (True, 750.0, False),   # GDI: 750 < 900 → no SYM_HC_HIGH
        (True, 950.0, True),    # GDI: 950 > 900 → SYM_HC_HIGH
        (False, 650.0, True),   # MPFI: 650 > 600 → SYM_HC_HIGH
        (False, 550.0, False),  # MPFI: 550 ≤ 600 → no SYM_HC_HIGH
    ],
)
def test_hc_gdi_threshold(has_gdi, hc_ppm, expect_high):
    """GDI engines use 900 ppm HC threshold; MPFI uses 600 ppm."""
    gas = _gas(co_pct=0.5, hc_ppm=hc_ppm, co2_pct=14.0, o2_pct=1.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False, has_gdi=has_gdi)
    if expect_high:
        assert "SYM_HC_HIGH" in symptoms
        assert "SYM_HC_LOW" not in symptoms
    else:
        assert "SYM_HC_HIGH" not in symptoms
        assert "SYM_HC_LOW" in symptoms


# ── _detect_gas_symptoms: CO ────────────────────────────────────────────────
# source: v2-gas-chemistry §2 — CO > 3.0% → SYM_CO_HIGH


def test_co_high_above_3pct():
    """CO > 3.0% → SYM_CO_HIGH."""
    gas = _gas(co_pct=3.1, hc_ppm=100.0, co2_pct=12.0, o2_pct=0.5)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_CO_HIGH" in symptoms


def test_co_normal_below_3pct():
    """CO ≤ 3.0% → no SYM_CO_HIGH."""
    gas = _gas(co_pct=3.0, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_CO_HIGH" not in symptoms


# ── _detect_gas_symptoms: CO2 ───────────────────────────────────────────────
# source: v2-gas-chemistry §2 — CO2 < 12.5% → SYM_CO2_LOW


def test_co2_low_below_12p5():
    """CO2 < 12.5% → SYM_CO2_LOW."""
    gas = _gas(co_pct=0.5, hc_ppm=100.0, co2_pct=12.4, o2_pct=1.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_CO2_LOW" in symptoms
    assert "SYM_CO2_GOOD" not in symptoms


def test_co2_good_above_12p5():
    """CO2 ≥ 12.5% → SYM_CO2_GOOD."""
    gas = _gas(co_pct=0.5, hc_ppm=100.0, co2_pct=12.5, o2_pct=1.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_CO2_GOOD" in symptoms
    assert "SYM_CO2_LOW" not in symptoms


# ── _detect_gas_symptoms: O2 ────────────────────────────────────────────────
# source: v2-gas-chemistry §2 — O2 > 2.0% → SYM_O2_HIGH


def test_o2_high_above_2pct():
    """O2 > 2.0% → SYM_O2_HIGH."""
    gas = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.0, o2_pct=2.1)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_O2_HIGH" in symptoms


def test_o2_normal_below_2pct():
    """O2 ≤ 2.0% → no SYM_O2_HIGH."""
    gas = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.0, o2_pct=2.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_O2_HIGH" not in symptoms


# ── _detect_gas_symptoms: NOx ───────────────────────────────────────────────
# source: v2-gas-chemistry §2 — NOx > 1500 ppm, gated by nox_suppressed


def test_nox_high_above_1500():
    """NOx > 1500 ppm → SYM_NOX_HIGH."""
    gas = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.0, o2_pct=1.0, nox_ppm=1501.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_NOX_HIGH" in symptoms


def test_nox_normal_below_1500():
    """NOx ≤ 1500 ppm → no SYM_NOX_HIGH."""
    gas = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.0, o2_pct=1.0, nox_ppm=1500.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_NOX_HIGH" not in symptoms


def test_nox_suppressed_skips_nox_check():
    """On 4-gas analyser, never emit SYM_NOX_HIGH regardless of NOx value."""
    gas = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.0, o2_pct=1.0, nox_ppm=2000.0)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=True)
    assert "SYM_NOX_HIGH" not in symptoms


def test_nox_none_skips_check():
    """NOx=None on 4-gas analyser — skip, no crash."""
    gas = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.0, o2_pct=1.0, nox_ppm=None)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=False)
    assert "SYM_NOX_HIGH" not in symptoms


# ── _compute_dual_state_delta ───────────────────────────────────────────────
# source: v2-gas-chemistry §3 dual-state delta tags


def test_dual_state_missing_idle():
    """None returned when idle gas is missing."""
    gas_high = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.5, o2_pct=0.5)
    tag = _compute_dual_state_delta(None, gas_high)
    assert tag is None


def test_dual_state_missing_high():
    """None returned when high-idle gas is missing."""
    gas_idle = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.5, o2_pct=0.5)
    tag = _compute_dual_state_delta(gas_idle, None)
    assert tag is None


def test_dual_state_both_missing():
    """None returned when both gas samples are missing."""
    tag = _compute_dual_state_delta(None, None)
    assert tag is None


def test_dual_state_improving():
    """CO2_high − CO2_idle ≥ 2 AND O2_high − O2_idle ≤ −0.5 → IMPROVING."""
    gas_idle = _gas(co_pct=0.5, hc_ppm=100.0, co2_pct=12.0, o2_pct=2.0)
    gas_high = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.5, o2_pct=0.5)
    tag = _compute_dual_state_delta(gas_idle, gas_high)
    assert tag == "SYM_DUAL_IMPROVING"


def test_dual_state_stable():
    """|CO2_high − CO2_idle| < 1 → STABLE."""
    gas_idle = _gas(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0)
    gas_high = _gas(co_pct=0.4, hc_ppm=80.0, co2_pct=14.3, o2_pct=0.8)
    tag = _compute_dual_state_delta(gas_idle, gas_high)
    assert tag == "SYM_DUAL_STABLE"


def test_dual_state_declining_co2():
    """CO2_high − CO2_idle ≤ −1 → DECLINING."""
    gas_idle = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.5, o2_pct=0.5)
    gas_high = _gas(co_pct=0.5, hc_ppm=100.0, co2_pct=12.0, o2_pct=2.0)
    tag = _compute_dual_state_delta(gas_idle, gas_high)
    assert tag == "SYM_DUAL_DECLINING"


def test_dual_state_declining_o2():
    """O2_high − O2_idle ≥ 1 → DECLINING (with |CO2 delta| ≥ 1 so STABLE
    does not take priority over DECLINING)."""
    gas_idle = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=13.0, o2_pct=0.5)
    gas_high = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=11.5, o2_pct=2.0)
    tag = _compute_dual_state_delta(gas_idle, gas_high)
    assert tag == "SYM_DUAL_DECLINING"


# ── analyse_gas: idle-only ──────────────────────────────────────────────────


def test_analyse_gas_idle_only():
    """Idle-only analysis: symptoms_idle populated, symptoms_high empty,
    dual_state_tag None, baseline_deviation_high None."""
    gas_idle = _gas(co_pct=0.18, hc_ppm=80.0, co2_pct=14.6, o2_pct=1.8)
    vi = _validated(gas_idle=gas_idle, gas_high=None)
    result = analyse_gas(vi, _dna())
    assert len(result.symptoms_idle) > 0
    assert result.symptoms_high == []
    assert result.analyser_lambda_idle is not None
    assert result.analyser_lambda_high is None
    assert result.dual_state_tag is None
    assert result.baseline_deviation_high is None


# ── analyse_gas: high-idle + baseline deviation ─────────────────────────────


def test_analyse_gas_high_idle_baseline_deviation():
    """High-idle analysis emits baseline deviation when |λ_high − target| > 0.02."""
    # Use target_lambda=1.000 and gas that gives lean lambda
    gas_high = _gas(co_pct=0.02, hc_ppm=30.0, co2_pct=14.0, o2_pct=3.0)
    vi = _validated(gas_idle=None, gas_high=gas_high)
    result = analyse_gas(vi, _dna(target_lambda=1.000))
    assert result.analyser_lambda_high is not None
    assert result.baseline_deviation_high is not None
    lamb = result.analyser_lambda_high
    deviation = abs(lamb - 1.000)
    assert deviation > 0.02, f"precondition: expected deviation > 0.02, got {deviation}"
    assert "SYM_BASELINE_DEVIATION" in result.symptoms_high


def test_analyse_gas_baseline_within_tolerance():
    """No SYM_BASELINE_DEVIATION when |λ_high − target| ≤ 0.02."""
    # Use a near-stoich mix with target_lambda matching closely
    gas_high = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.5, o2_pct=0.8)
    vi = _validated(gas_idle=None, gas_high=gas_high)
    lamb = _brettschneider(gas_high)
    # Set target lambda very close to actual
    result = analyse_gas(vi, _dna(target_lambda=lamb))
    assert result.baseline_deviation_high == 0.0
    assert "SYM_BASELINE_DEVIATION" not in result.symptoms_high


# ── analyse_gas: NOx suppression ────────────────────────────────────────────


def test_analyse_gas_nox_suppressed_4gas():
    """4-gas analyser: nox_suppressed=True, SYM_NOX_HIGH never emitted."""
    gas_idle = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.0, o2_pct=1.0, nox_ppm=2000.0)
    vi = _validated(gas_idle=gas_idle, gas_high=None, nox_suppressed=True)
    result = analyse_gas(vi, _dna())
    all_symptoms = result.symptoms_idle + result.symptoms_high
    assert "SYM_NOX_HIGH" not in all_symptoms


# ── cam timing re-threshold pin tests ───────────────────────────────────────
# source: timing_compression_forensic_2026-05-03.md
# V2 correct: hc_min=200ppm, co_min=0.3% (was 5000ppm/2.5% in V1)
# source: v2-gas-chemistry §5 re-thresholded patterns


def test_cam_timing_v2_threshold_gas_symptoms():
    """With V2-corrected thresholds (hc=200ppm, co=0.3%):
    HC=200 < 600 → SYM_HC_LOW (not elevated)
    CO=0.3 < 3.0 → no SYM_CO_HIGH
    These gas values combine to indicate mild late-timing signature
    that M3 will interpret as SYM_LATE_TIMING.
    """
    gas_idle = _gas(co_pct=0.3, hc_ppm=200.0, co2_pct=14.0, o2_pct=1.2)
    vi = _validated(gas_idle=gas_idle, gas_high=None)
    result = analyse_gas(vi, _dna())
    symptoms = result.symptoms_idle
    # HC=200 < 600 → LOW
    assert "SYM_HC_LOW" in symptoms
    assert "SYM_HC_HIGH" not in symptoms
    # CO=0.3 < 3.0 → not HIGH
    assert "SYM_CO_HIGH" not in symptoms
    # Brettschneider produces a valid lambda
    assert result.analyser_lambda_idle is not None


def test_cam_timing_v1_old_threshold_regression_guard():
    """Old V1 threshold (hc=5000ppm, co=2.5%) should produce same gas-level
    symptoms as any other high-HC/high-CO input. V1's special threshold is
    removed — gas_lab treats 5000ppm HC the same as any HC > 600.
    """
    gas_idle = _gas(co_pct=2.5, hc_ppm=5000.0, co2_pct=10.0, o2_pct=0.8)
    vi = _validated(gas_idle=gas_idle, gas_high=None)
    result = analyse_gas(vi, _dna())
    symptoms = result.symptoms_idle
    # HC=5000 > 600 → HIGH (same as any other >600ppm value)
    assert "SYM_HC_HIGH" in symptoms
    assert "SYM_HC_LOW" not in symptoms
    # CO=2.5 < 3.0 → not HIGH
    assert "SYM_CO_HIGH" not in symptoms
    # Rich lambda
    assert result.analyser_lambda_idle is not None
    assert result.analyser_lambda_idle < 0.97


# ── analyse_gas: dual-state delta integration ───────────────────────────────


def test_analyse_gas_dual_state_integration():
    """Full dual-state analysis produces correct tag and per-state symptoms."""
    gas_idle = _gas(co_pct=0.5, hc_ppm=100.0, co2_pct=12.0, o2_pct=2.0)
    gas_high = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=14.5, o2_pct=0.5)
    vi = _validated(gas_idle=gas_idle, gas_high=gas_high)
    result = analyse_gas(vi, _dna())
    assert result.dual_state_tag == "SYM_DUAL_IMPROVING"
    assert len(result.symptoms_idle) > 0
    assert len(result.symptoms_high) > 0
    assert result.analyser_lambda_idle is not None
    assert result.analyser_lambda_high is not None


# ── analyse_gas: completely missing gas ─────────────────────────────────────


def test_analyse_gas_no_gas_samples():
    """Both gas samples None: empty symptoms, all optional fields None."""
    vi = _validated(gas_idle=None, gas_high=None)
    result = analyse_gas(vi, _dna())
    assert result.symptoms_idle == []
    assert result.symptoms_high == []
    assert result.analyser_lambda_idle is None
    assert result.analyser_lambda_high is None
    assert result.dual_state_tag is None
    assert result.baseline_deviation_high is None


# ── GasLabOutput dataclass contract ─────────────────────────────────────────


def test_gas_lab_output_defaults():
    """GasLabOutput fields match the contract in v2-gas-chemistry §6."""
    out = GasLabOutput()
    assert out.symptoms_idle == []
    assert out.symptoms_high == []
    assert out.dual_state_tag is None
    assert out.analyser_lambda_idle is None
    assert out.analyser_lambda_high is None
    assert out.baseline_deviation_high is None


# ── parametrized symptom matrix ─────────────────────────────────────────────
# source: v2-gas-chemistry §2 per-state symptom detection table


@pytest.mark.parametrize(
    "co_pct, hc_ppm, co2_pct, o2_pct, nox_ppm, nox_supp, expected_absent",
    [
        # HC boundary: 600 → LOW, 601 → HIGH
        (0.5, 601.0, 14.0, 1.0, None, False, "SYM_HC_LOW"),
        (0.5, 600.0, 14.0, 1.0, None, False, "SYM_HC_HIGH"),
        # CO boundary: 3.0 → no CO_HIGH, 3.1 → CO_HIGH
        (3.1, 100.0, 12.0, 0.5, None, False, None),
        (3.0, 100.0, 14.0, 1.0, None, False, "SYM_CO_HIGH"),
        # CO2 boundary: 12.5 → GOOD, 12.4 → LOW
        (0.5, 100.0, 12.4, 1.0, None, False, "SYM_CO2_GOOD"),
        (0.5, 100.0, 12.5, 1.0, None, False, "SYM_CO2_LOW"),
        # O2 boundary: 2.0 → no O2_HIGH, 2.1 → O2_HIGH
        (0.1, 50.0, 14.0, 2.1, None, False, None),
        (0.1, 50.0, 14.0, 2.0, None, False, "SYM_O2_HIGH"),
        # NOx boundary: 1500 → no NOX_HIGH, 1501 → NOX_HIGH
        (0.1, 50.0, 14.0, 1.0, 1501.0, False, None),
        (0.1, 50.0, 14.0, 1.0, 1500.0, False, "SYM_NOX_HIGH"),
        # NOx suppressed: 2000 ppm but 4-gas → no NOX_HIGH
        (0.1, 50.0, 14.0, 1.0, 2000.0, True, None),
        # NOx=None: skip check
        (0.1, 50.0, 14.0, 1.0, None, False, "SYM_NOX_HIGH"),
    ],
)
def test_symptom_boundaries(co_pct, hc_ppm, co2_pct, o2_pct, nox_ppm, nox_supp, expected_absent):
    """Parametrized boundary checks for symptom thresholds."""
    gas = _gas(co_pct=co_pct, hc_ppm=hc_ppm, co2_pct=co2_pct, o2_pct=o2_pct, nox_ppm=nox_ppm)
    lamb = _brettschneider(gas)
    symptoms = _detect_gas_symptoms(gas, lamb, nox_suppressed=nox_supp)
    if expected_absent is not None:
        assert expected_absent not in symptoms, (
            f"Expected {expected_absent} to be absent, got {symptoms}"
        )
