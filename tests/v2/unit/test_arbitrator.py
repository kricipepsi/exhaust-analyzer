"""Unit tests for arbitrator.py (M3) — perception gap, trim-trend, bank symmetry, flood control.

Covers: perception gap detection, trim-trend Option A classification (L2 present
→ no CF penalty, L2 absent → 30% penalty), bank symmetry analysis (V-engine
only), flood control (cascade grouping), and end-to-end evidence vector assembly
via arbitrate().
"""

from __future__ import annotations

import pathlib
from typing import Any

import pytest

from engine.v2.arbitrator import (
    _SYM_BANK_ASYM_FAULT,
    _SYM_O2_HARNESS_SWAP,
    _SYM_PERCEPTION_LEAN_SEEN_RICH,
    _SYM_PERCEPTION_RICH_SEEN_LEAN,
    _SYM_TRIM_LEAN_IDLE_ONLY,
    _SYM_TRIM_RICH_IDLE_ONLY,
    MasterEvidenceVector,
    PerceptionGap,
    _analyse_bank_symmetry,
    _analyse_trim_trend,
    _apply_flood_control,
    _classify_trim_trend,
    _detect_perception_gap,
    arbitrate,
)
from engine.v2.digital_parser import DigitalParserOutput
from engine.v2.dna_core import DNAOutput
from engine.v2.gas_lab import GasLabOutput
from engine.v2.input_model import (
    DiagnosticInput,
    GasRecord,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)

# ── helpers ─────────────────────────────────────────────────────────────────────


def _sample_ctx(engine_code: str = "EA111_1.2_TSI", my: int = 2012) -> VehicleContext:
    return VehicleContext(
        brand="VOLKSWAGEN",
        model="Golf",
        engine_code=engine_code,
        displacement_cc=1197,
        my=my,
    )


def _obd(**kwargs: Any) -> OBDRecord:
    defaults: dict[str, Any] = {
        "stft_b1": None,
        "stft_b2": None,
        "ltft_b1": None,
        "ltft_b2": None,
        "rpm": 800,
        "ect_c": 90.0,
        "iat_c": 30.0,
        "fuel_status": "CL",
        "obd_lambda": None,
    }
    defaults.update(kwargs)
    return OBDRecord(**{k: v for k, v in defaults.items() if k in OBDRecord.__slots__})


def _validated(obd: OBDRecord | None = None, gas_idle: GasRecord | None = None) -> ValidatedInput:
    return ValidatedInput(
        raw=DiagnosticInput(
            vehicle_context=_sample_ctx(),
            dtcs=[],
            analyser_type="5-gas",
            obd=obd,
            gas_idle=gas_idle,
        ),
        valid_channels={"obd", "gas_idle", "dtcs"},
    )


def _dna_output(
    engine_state: str = "warm_closed_loop",
    era_bucket: str = "ERA_CAN",
    is_v_engine: bool = False,
    has_turbo: bool = True,
) -> DNAOutput:
    return DNAOutput(
        engine_state=engine_state,
        era_bucket=era_bucket,
        tech_mask={
            "has_vvt": True,
            "has_gdi": True,
            "has_turbo": has_turbo,
            "is_v_engine": is_v_engine,
            "has_egr": False,
            "has_secondary_air": False,
        },
        o2_type="WB",
        target_rpm_u2=2500,
        target_lambda_v112=1.000,
        vref_missing=False,
        confidence_ceiling=1.00,
    )


def _digital_output(symptoms: list[str] | None = None) -> DigitalParserOutput:
    return DigitalParserOutput(
        symptoms=symptoms if symptoms is not None else [],
        breathing_cluster_efficiency=None,
        open_loop_suppression=False,
        cold_engine=False,
        codes_cleared=False,
    )


def _gas_output(
    analyser_lambda_idle: float | None = None,
    analyser_lambda_high: float | None = None,
    symptoms_idle: list[str] | None = None,
    symptoms_high: list[str] | None = None,
) -> GasLabOutput:
    return GasLabOutput(
        symptoms_idle=symptoms_idle if symptoms_idle is not None else [],
        symptoms_high=symptoms_high if symptoms_high is not None else [],
        dual_state_tag=None,
        analyser_lambda_idle=analyser_lambda_idle,
        analyser_lambda_high=analyser_lambda_high,
        baseline_deviation_high=None,
    )


def _gas_record(co_pct: float = 0.5, hc_ppm: float = 100.0, co2_pct: float = 14.0,
                o2_pct: float = 1.0) -> GasRecord:
    return GasRecord(co_pct=co_pct, hc_ppm=hc_ppm, co2_pct=co2_pct, o2_pct=o2_pct)


# ── perception gap detection ────────────────────────────────────────────────────


class TestPerceptionGap:
    """Perception gap detection — truth-vs-perception lambda disagreement (L01)."""

    def test_leaning_seen_rich(self) -> None:
        """analyser_lambda=0.90, obd_lambda=1.10 → SYM_PERCEPTION_LEAN_SEEN_RICH."""
        vi = _validated(obd=_obd(obd_lambda=1.10))
        go = _gas_output(analyser_lambda_idle=0.90)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in evidence.active_symptoms
        cf = evidence.active_symptoms[_SYM_PERCEPTION_LEAN_SEEN_RICH]
        assert 0.0 < cf <= 0.70
        assert evidence.perception_gap is not None
        assert evidence.perception_gap.gap_type == "LEAN_SEEN_RICH"

    def test_rich_seen_lean(self) -> None:
        """analyser_lambda=1.10, obd_lambda=0.90 → SYM_PERCEPTION_RICH_SEEN_LEAN."""
        vi = _validated(obd=_obd(obd_lambda=0.90))
        go = _gas_output(analyser_lambda_idle=1.10)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert _SYM_PERCEPTION_RICH_SEEN_LEAN in evidence.active_symptoms
        cf = evidence.active_symptoms[_SYM_PERCEPTION_RICH_SEEN_LEAN]
        assert 0.0 < cf <= 0.70
        assert evidence.perception_gap is not None
        assert evidence.perception_gap.gap_type == "RICH_SEEN_LEAN"

    def test_delta_below_threshold_no_gap(self) -> None:
        """Delta <= 0.05 → no perception gap emitted."""
        vi = _validated(obd=_obd(obd_lambda=1.02))
        go = _gas_output(analyser_lambda_idle=1.00)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert _SYM_PERCEPTION_LEAN_SEEN_RICH not in evidence.active_symptoms
        assert _SYM_PERCEPTION_RICH_SEEN_LEAN not in evidence.active_symptoms
        assert evidence.perception_gap is None

    def test_delta_large_but_both_lean_no_gap(self) -> None:
        """Delta > 0.05 but analyser not lean (<0.97) → no gap (L01 guard)."""
        vi = _validated(obd=_obd(obd_lambda=1.10))
        go = _gas_output(analyser_lambda_idle=0.98)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert evidence.perception_gap is None

    def test_no_obd_lambda_no_crash(self) -> None:
        """Missing OBD lambda → function returns without error."""
        vi = _validated(obd=_obd(obd_lambda=None))
        go = _gas_output(analyser_lambda_idle=0.90)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert evidence.perception_gap is None

    def test_no_obd_record_no_crash(self) -> None:
        """No OBD record at all → function returns without error."""
        vi = _validated(obd=None)
        go = _gas_output(analyser_lambda_idle=0.90)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert evidence.perception_gap is None

    def test_no_analyser_lambda_no_crash(self) -> None:
        """Missing analyser lambda → function returns without error."""
        vi = _validated(obd=_obd(obd_lambda=1.10))
        go = _gas_output(analyser_lambda_idle=None, analyser_lambda_high=None)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert evidence.perception_gap is None

    def test_falls_back_to_high_lambda(self) -> None:
        """Uses analyser_lambda_high when idle lambda is None."""
        vi = _validated(obd=_obd(obd_lambda=1.10))
        go = _gas_output(analyser_lambda_idle=None, analyser_lambda_high=0.90)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in evidence.active_symptoms

    def test_cf_clamped_at_max(self) -> None:
        """CF is clamped at 0.70 even for very large deltas (L01 — CF-weight, not authority)."""
        vi = _validated(obd=_obd(obd_lambda=1.50))
        go = _gas_output(analyser_lambda_idle=0.70)  # delta = 0.80
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert evidence.active_symptoms[_SYM_PERCEPTION_LEAN_SEEN_RICH] == pytest.approx(0.70)


# ── trim-trend: idle-only fallback ──────────────────────────────────────────────


class TestTrimTrendIdleOnly:
    """Trim-trend idle-only fallback — when cruise/high-idle data is unavailable."""

    def test_idle_positive_strong_emits_lean_idle_only(self) -> None:
        """idle STFT+LTFT >= +8% → SYM_TRIM_LEAN_IDLE_ONLY with reduced CF."""
        vi = _validated(obd=_obd(stft_b1=8.0, ltft_b1=0.0))
        go = _gas_output()
        evidence = MasterEvidenceVector()

        _analyse_trim_trend(vi, go, evidence)

        assert _SYM_TRIM_LEAN_IDLE_ONLY in evidence.active_symptoms
        # CF = 0.65 * 0.70 = 0.455
        assert evidence.active_symptoms[_SYM_TRIM_LEAN_IDLE_ONLY] == pytest.approx(0.65 * 0.70)

    def test_idle_negative_strong_emits_rich_idle_only(self) -> None:
        """idle STFT+LTFT <= -8% → SYM_TRIM_RICH_IDLE_ONLY with reduced CF."""
        vi = _validated(obd=_obd(stft_b1=-8.0, ltft_b1=0.0))
        go = _gas_output()
        evidence = MasterEvidenceVector()

        _analyse_trim_trend(vi, go, evidence)

        assert _SYM_TRIM_RICH_IDLE_ONLY in evidence.active_symptoms
        assert evidence.active_symptoms[_SYM_TRIM_RICH_IDLE_ONLY] == pytest.approx(0.65 * 0.70)

    def test_idle_inband_no_trim_tag(self) -> None:
        """idle STFT+LTFT in (-8%, +8%) → no trim-trend symptom emitted."""
        vi = _validated(obd=_obd(stft_b1=3.0, ltft_b1=2.0))
        go = _gas_output()
        evidence = MasterEvidenceVector()

        _analyse_trim_trend(vi, go, evidence)

        assert _SYM_TRIM_LEAN_IDLE_ONLY not in evidence.active_symptoms
        assert _SYM_TRIM_RICH_IDLE_ONLY not in evidence.active_symptoms

    def test_no_obd_no_crash(self) -> None:
        """Missing OBD → function returns without error."""
        vi = _validated(obd=None)
        go = _gas_output()
        evidence = MasterEvidenceVector()

        _analyse_trim_trend(vi, go, evidence)

        assert len(evidence.active_symptoms) == 0

    def test_no_trim_data_no_crash(self) -> None:
        """Both STFT and LTFT are None → function returns without error."""
        vi = _validated(obd=_obd(stft_b1=None, ltft_b1=None))
        go = _gas_output()
        evidence = MasterEvidenceVector()

        _analyse_trim_trend(vi, go, evidence)

        assert len(evidence.active_symptoms) == 0

    def test_only_ltft_contributes(self) -> None:
        """STFT None, LTFT >= +8% → trim-trend fires on LTFT alone."""
        vi = _validated(obd=_obd(stft_b1=None, ltft_b1=10.0))
        go = _gas_output()
        evidence = MasterEvidenceVector()

        _analyse_trim_trend(vi, go, evidence)

        assert _SYM_TRIM_LEAN_IDLE_ONLY in evidence.active_symptoms

    def test_exactly_at_threshold_emits(self) -> None:
        """idle total exactly at +8.0% fires symptom (≥ boundary)."""
        vi = _validated(obd=_obd(stft_b1=8.0, ltft_b1=0.0))
        go = _gas_output()
        evidence = MasterEvidenceVector()

        _analyse_trim_trend(vi, go, evidence)

        assert _SYM_TRIM_LEAN_IDLE_ONLY in evidence.active_symptoms


# ── trim-trend: classification ─────────────────────────────────────────────────


class TestClassifyTrimTrend:
    """Direct tests for _classify_trim_trend — Option A idle-only classification.

    L2 present → CF = 0.65 (no penalty — L2 confirms operating point).
    L2 absent → CF = 0.65 * 0.70 = 0.455 (30% penalty — idle-only).
    """

    # ── lean, L2 absent ─────────────────────────────────────────────────────

    def test_lean_no_l2_reduced_cf(self) -> None:
        """Lean idle, L2 absent → CF = 0.455 (30% penalty)."""
        evidence = MasterEvidenceVector()
        _classify_trim_trend(idle_total=10.0, has_l2=False, evidence=evidence)

        assert _SYM_TRIM_LEAN_IDLE_ONLY in evidence.active_symptoms
        assert evidence.active_symptoms[_SYM_TRIM_LEAN_IDLE_ONLY] == pytest.approx(0.455)

    # ── lean, L2 present ────────────────────────────────────────────────────

    def test_lean_with_l2_no_penalty(self) -> None:
        """Lean idle, L2 present → CF = 0.65 (no penalty)."""
        evidence = MasterEvidenceVector()
        _classify_trim_trend(idle_total=10.0, has_l2=True, evidence=evidence)

        assert _SYM_TRIM_LEAN_IDLE_ONLY in evidence.active_symptoms
        assert evidence.active_symptoms[_SYM_TRIM_LEAN_IDLE_ONLY] == pytest.approx(0.65)

    # ── rich, L2 absent ─────────────────────────────────────────────────────

    def test_rich_no_l2_reduced_cf(self) -> None:
        """Rich idle, L2 absent → CF = 0.455 (30% penalty)."""
        evidence = MasterEvidenceVector()
        _classify_trim_trend(idle_total=-10.0, has_l2=False, evidence=evidence)

        assert _SYM_TRIM_RICH_IDLE_ONLY in evidence.active_symptoms
        assert evidence.active_symptoms[_SYM_TRIM_RICH_IDLE_ONLY] == pytest.approx(0.455)

    # ── rich, L2 present ────────────────────────────────────────────────────

    def test_rich_with_l2_no_penalty(self) -> None:
        """Rich idle, L2 present → CF = 0.65 (no penalty)."""
        evidence = MasterEvidenceVector()
        _classify_trim_trend(idle_total=-10.0, has_l2=True, evidence=evidence)

        assert _SYM_TRIM_RICH_IDLE_ONLY in evidence.active_symptoms
        assert evidence.active_symptoms[_SYM_TRIM_RICH_IDLE_ONLY] == pytest.approx(0.65)

    # ── in-band ─────────────────────────────────────────────────────────────

    def test_inband_no_emission(self) -> None:
        """Trim within ±8% → no symptom emitted (regardless of L2)."""
        evidence = MasterEvidenceVector()
        _classify_trim_trend(idle_total=5.0, has_l2=False, evidence=evidence)

        assert len(evidence.active_symptoms) == 0

    # ── deletion confirmation ───────────────────────────────────────────────

    def test_dead_code_removed(self) -> None:
        """_classify_trim_full and _get_cruise_trim_total must not exist."""
        src = pathlib.Path(__file__).parent.parent.parent.parent / "engine" / "v2" / "arbitrator.py"
        text = src.read_text()
        assert "_get_cruise_trim_total" not in text, "stub still present"
        assert "_classify_trim_full" not in text, "dead code still present"
        assert "_classify_trim_trend" in text, "renamed function not found"


# ── bank symmetry ───────────────────────────────────────────────────────────────


class TestBankSymmetry:
    """Bank-to-bank trim asymmetry detection (V-engine only)."""

    def test_opposite_signs_harness_swap(self) -> None:
        """b1=+15%, b2=-12% with V-engine → SYM_O2_HARNESS_SWAP."""
        dna = _dna_output(is_v_engine=True)
        vi = _validated(obd=_obd(stft_b1=15.0, ltft_b1=0.0, stft_b2=-12.0, ltft_b2=0.0))
        evidence = MasterEvidenceVector()

        _analyse_bank_symmetry(dna, vi, evidence)

        assert _SYM_O2_HARNESS_SWAP in evidence.active_symptoms
        assert evidence.active_symptoms[_SYM_O2_HARNESS_SWAP] == 0.65
        assert evidence.bank_asym is True

    def test_same_sign_bank_asym_fault(self) -> None:
        """b1=+15%, b2=+3% with V-engine (diff=12 > 10) → SYM_BANK_ASYM_FAULT."""
        dna = _dna_output(is_v_engine=True)
        vi = _validated(obd=_obd(stft_b1=15.0, ltft_b1=0.0, stft_b2=3.0, ltft_b2=0.0))
        evidence = MasterEvidenceVector()

        _analyse_bank_symmetry(dna, vi, evidence)

        assert _SYM_BANK_ASYM_FAULT in evidence.active_symptoms
        assert evidence.active_symptoms[_SYM_BANK_ASYM_FAULT] == 0.55
        assert evidence.bank_asym is True

    def test_not_v_engine_skips_analysis(self) -> None:
        """Inline-4 engine → bank symmetry analysis skipped entirely."""
        dna = _dna_output(is_v_engine=False)
        vi = _validated(obd=_obd(stft_b1=15.0, ltft_b1=0.0, stft_b2=-12.0, ltft_b2=0.0))
        evidence = MasterEvidenceVector()

        _analyse_bank_symmetry(dna, vi, evidence)

        assert _SYM_O2_HARNESS_SWAP not in evidence.active_symptoms
        assert _SYM_BANK_ASYM_FAULT not in evidence.active_symptoms
        assert evidence.bank_asym is False

    def test_diff_below_threshold_no_asymmetry(self) -> None:
        """|b1 - b2| <= 10% → no bank asymmetry emitted."""
        dna = _dna_output(is_v_engine=True)
        vi = _validated(obd=_obd(stft_b1=12.0, ltft_b1=0.0, stft_b2=3.0, ltft_b2=0.0))
        evidence = MasterEvidenceVector()

        _analyse_bank_symmetry(dna, vi, evidence)

        assert _SYM_O2_HARNESS_SWAP not in evidence.active_symptoms
        assert _SYM_BANK_ASYM_FAULT not in evidence.active_symptoms

    def test_missing_b2_trim_no_crash(self) -> None:
        """Bank 2 trim unavailable → function returns without error."""
        dna = _dna_output(is_v_engine=True)
        vi = _validated(obd=_obd(stft_b1=15.0, ltft_b1=0.0, stft_b2=None, ltft_b2=None))
        evidence = MasterEvidenceVector()

        _analyse_bank_symmetry(dna, vi, evidence)

        assert evidence.bank_asym is False

    def test_no_obd_no_crash(self) -> None:
        """Missing OBD → function returns without error."""
        dna = _dna_output(is_v_engine=True)
        vi = _validated(obd=None)
        evidence = MasterEvidenceVector()

        _analyse_bank_symmetry(dna, vi, evidence)

        assert evidence.bank_asym is False

    def test_ltft_contributes_to_trim_total(self) -> None:
        """Bank 2 trim computed from STFT + LTFT."""
        dna = _dna_output(is_v_engine=True)
        vi = _validated(obd=_obd(
            stft_b1=5.0, ltft_b1=10.0,   # b1 total = +15%
            stft_b2=-5.0, ltft_b2=-7.0,   # b2 total = -12%
        ))
        evidence = MasterEvidenceVector()

        _analyse_bank_symmetry(dna, vi, evidence)

        assert _SYM_O2_HARNESS_SWAP in evidence.active_symptoms


# ── flood control ───────────────────────────────────────────────────────────────


class TestFloodControl:
    """Flood control — prevent single root cause from dominating score distribution (R8)."""

    def test_five_siblings_top_kept_rest_reduced(self) -> None:
        """5 symptoms in same group → top-CF kept, rest reduced 30%."""
        import engine.v2.arbitrator as arb

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(arb, "_FLOOD_GROUP_KEYS", {
            "SYM_TRIM_LEAN_IDLE_ONLY": "TRIM_LEAN",
            "SYM_TRIM_LEAN_LOAD_BIAS": "TRIM_LEAN",
            "SYM_TEST_A": "TRIM_LEAN",
            "SYM_TEST_B": "TRIM_LEAN",
            "SYM_TEST_C": "TRIM_LEAN",
        })

        try:
            evidence = MasterEvidenceVector(active_symptoms={
                "SYM_TRIM_LEAN_IDLE_ONLY": 0.65,
                "SYM_TRIM_LEAN_LOAD_BIAS": 0.55,
                "SYM_TEST_A": 0.45,
                "SYM_TEST_B": 0.50,
                "SYM_TEST_C": 0.40,
            })
            _apply_flood_control(evidence)

            # Top CF (0.65) kept
            assert evidence.active_symptoms["SYM_TRIM_LEAN_IDLE_ONLY"] == 0.65
            # Others reduced by 30%
            assert evidence.active_symptoms["SYM_TRIM_LEAN_LOAD_BIAS"] == pytest.approx(0.55 * 0.70)
            assert evidence.active_symptoms["SYM_TEST_A"] == pytest.approx(0.45 * 0.70)
            assert evidence.active_symptoms["SYM_TEST_B"] == pytest.approx(0.50 * 0.70)
            assert evidence.active_symptoms["SYM_TEST_C"] == pytest.approx(0.40 * 0.70)
            # cascading_consequences has the 4 reduced symptoms
            assert len(evidence.cascading_consequences) == 4
            assert "SYM_TRIM_LEAN_LOAD_BIAS" in evidence.cascading_consequences
        finally:
            monkeypatch.undo()

    def test_two_symptoms_no_reduction(self) -> None:
        """Only 2 symptoms in a group (default _FLOOD_GROUP_KEYS) → no reduction."""
        evidence = MasterEvidenceVector(active_symptoms={
            "SYM_TRIM_LEAN_IDLE_ONLY": 0.65,
            "SYM_TRIM_LEAN_LOAD_BIAS": 0.55,
        })
        _apply_flood_control(evidence)

        assert evidence.active_symptoms["SYM_TRIM_LEAN_IDLE_ONLY"] == 0.65
        assert evidence.active_symptoms["SYM_TRIM_LEAN_LOAD_BIAS"] == 0.55
        assert len(evidence.cascading_consequences) == 0

    def test_exactly_three_no_reduction(self) -> None:
        """3 siblings (threshold boundary) → no reduction (only > 3 triggers)."""
        import engine.v2.arbitrator as arb

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(arb, "_FLOOD_GROUP_KEYS", {
            "SYM_TRIM_LEAN_IDLE_ONLY": "TRIM_LEAN",
            "SYM_TRIM_LEAN_LOAD_BIAS": "TRIM_LEAN",
            "SYM_TEST_A": "TRIM_LEAN",
        })

        try:
            evidence = MasterEvidenceVector(active_symptoms={
                "SYM_TRIM_LEAN_IDLE_ONLY": 0.65,
                "SYM_TRIM_LEAN_LOAD_BIAS": 0.55,
                "SYM_TEST_A": 0.45,
            })
            _apply_flood_control(evidence)

            assert evidence.active_symptoms["SYM_TRIM_LEAN_IDLE_ONLY"] == 0.65
            assert evidence.active_symptoms["SYM_TRIM_LEAN_LOAD_BIAS"] == 0.55
            assert evidence.active_symptoms["SYM_TEST_A"] == 0.45
            assert len(evidence.cascading_consequences) == 0
        finally:
            monkeypatch.undo()

    def test_ungrouped_symptoms_unaffected(self) -> None:
        """Symptoms not in any flood group are never reduced."""
        evidence = MasterEvidenceVector(active_symptoms={
            "SYM_UNKNOWN_XYZ": 0.80,
            "SYM_TRIM_LEAN_IDLE_ONLY": 0.65,
        })
        _apply_flood_control(evidence)

        assert evidence.active_symptoms["SYM_UNKNOWN_XYZ"] == 0.80

    def test_multiple_groups_independent(self) -> None:
        """Flood control is per-group — one group's reduction doesn't affect another."""
        import engine.v2.arbitrator as arb

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(arb, "_FLOOD_GROUP_KEYS", {
            "SYM_TRIM_LEAN_IDLE_ONLY": "TRIM_LEAN",
            "SYM_TEST_A": "TRIM_LEAN",
            "SYM_TEST_B": "TRIM_LEAN",
            "SYM_TEST_C": "TRIM_LEAN",
            "SYM_TRIM_RICH_STATIC": "TRIM_RICH",
            "SYM_TEST_D": "TRIM_RICH",
        })

        try:
            evidence = MasterEvidenceVector(active_symptoms={
                "SYM_TRIM_LEAN_IDLE_ONLY": 0.65,
                "SYM_TEST_A": 0.55,
                "SYM_TEST_B": 0.45,
                "SYM_TEST_C": 0.35,
                "SYM_TRIM_RICH_STATIC": 0.60,
                "SYM_TEST_D": 0.40,
            })
            _apply_flood_control(evidence)

            # TRIM_LEAN group had 4 entries → top kept, rest reduced
            assert evidence.active_symptoms["SYM_TRIM_LEAN_IDLE_ONLY"] == 0.65
            assert evidence.active_symptoms["SYM_TEST_A"] == pytest.approx(0.55 * 0.70)
            # TRIM_RICH group had 2 entries → no reduction
            assert evidence.active_symptoms["SYM_TRIM_RICH_STATIC"] == 0.60
            assert evidence.active_symptoms["SYM_TEST_D"] == 0.40
        finally:
            monkeypatch.undo()


# ── evidence collection (M1 / M2 carry-forward) ─────────────────────────────────


class TestEvidenceCollection:
    """Digital and gas symptoms are carried into the evidence vector at correct CF."""

    def test_digital_symptoms_carried_forward(self) -> None:
        """M1 symptoms appended at CF 0.70."""
        dna = _dna_output()
        vi = _validated(obd=_obd(ect_c=90.0, rpm=800, fuel_status="CL"))
        digital = _digital_output(symptoms=["SYM_DTC_P0171", "SYM_DTC_P0420"])
        go = _gas_output()
        result = arbitrate(vi, dna, digital, go)

        assert result.active_symptoms.get("SYM_DTC_P0171") == 0.70
        assert result.active_symptoms.get("SYM_DTC_P0420") == 0.70

    def test_gas_symptoms_carried_forward(self) -> None:
        """M2 symptoms appended at CF 0.85."""
        dna = _dna_output()
        vi = _validated(obd=_obd())
        digital = _digital_output()
        go = _gas_output(
            symptoms_idle=["SYM_LAMBDA_LOW"],
            symptoms_high=["SYM_HC_HIGH"],
            analyser_lambda_idle=0.95,
        )
        result = arbitrate(vi, dna, digital, go)

        assert result.active_symptoms.get("SYM_LAMBDA_LOW") == 0.85
        assert result.active_symptoms.get("SYM_HC_HIGH") == 0.85

    def test_no_duplicate_digital_gas_cf_override(self) -> None:
        """When same symptom ID appears in both M1 and M2, later write wins (gas CF 0.85)."""
        dna = _dna_output()
        vi = _validated(obd=_obd())
        digital = _digital_output(symptoms=["SYM_LAMBDA_LOW"])
        go = _gas_output(symptoms_idle=["SYM_LAMBDA_LOW"], analyser_lambda_idle=0.95)
        result = arbitrate(vi, dna, digital, go)

        assert result.active_symptoms["SYM_LAMBDA_LOW"] == 0.85


# ── integration: arbitrate() end-to-end ─────────────────────────────────────────


class TestArbitrateEndToEnd:
    """Full arbitrate() pipeline — M1 + M2 + perception + trim-trend + bank + flood."""

    def test_empty_inputs_returns_empty_evidence(self) -> None:
        """Minimal valid inputs → empty evidence vector, no crash."""
        dna = _dna_output()
        vi = _validated(obd=_obd())
        digital = _digital_output()
        go = _gas_output()

        result = arbitrate(vi, dna, digital, go)

        assert isinstance(result, MasterEvidenceVector)
        assert result.perception_gap is None
        assert result.bank_asym is False
        assert len(result.cascading_consequences) == 0

    def test_perception_gap_through_arbitrate(self) -> None:
        """Perception gap detected and emitted through full arbitrate() pipeline."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.10))
        digital = _digital_output()
        go = _gas_output(analyser_lambda_idle=0.90)

        result = arbitrate(vi, dna, digital, go)

        assert result.perception_gap is not None
        assert result.perception_gap.gap_type == "LEAN_SEEN_RICH"
        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in result.active_symptoms

    def test_trim_trend_through_arbitrate(self) -> None:
        """Trim-trend idle-only path fires through full arbitrate() pipeline."""
        dna = _dna_output()
        vi = _validated(obd=_obd(stft_b1=10.0, ltft_b1=0.0))
        digital = _digital_output()
        go = _gas_output()

        result = arbitrate(vi, dna, digital, go)

        assert _SYM_TRIM_LEAN_IDLE_ONLY in result.active_symptoms

    def test_bank_symmetry_through_arbitrate(self) -> None:
        """Bank asymmetry detected through full arbitrate() pipeline (V-engine)."""
        dna = _dna_output(is_v_engine=True)
        vi = _validated(obd=_obd(stft_b1=15.0, ltft_b1=0.0, stft_b2=-12.0, ltft_b2=0.0))
        digital = _digital_output()
        go = _gas_output()

        result = arbitrate(vi, dna, digital, go)

        assert _SYM_O2_HARNESS_SWAP in result.active_symptoms
        assert result.bank_asym is True

    def test_result_structure_matches_contract(self) -> None:
        """MasterEvidenceVector fields match v2-arbitrator §3 output contract."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.10))
        digital = _digital_output(symptoms=["SYM_DTC_P0171"])
        go = _gas_output(symptoms_idle=["SYM_LAMBDA_LOW"], analyser_lambda_idle=0.90)

        result = arbitrate(vi, dna, digital, go)

        assert isinstance(result.active_symptoms, dict)
        assert isinstance(result.perception_gap, (PerceptionGap, type(None)))
        assert isinstance(result.cascading_consequences, list)
        assert isinstance(result.bank_asym, bool)
        # perception_gap is informational — M4 uses active_symptoms for scoring (L01)
        if result.perception_gap is not None:
            assert "SYM_PERCEPTION" in [
                k for k in result.active_symptoms
                if "PERCEPTION" in k
            ][0]
