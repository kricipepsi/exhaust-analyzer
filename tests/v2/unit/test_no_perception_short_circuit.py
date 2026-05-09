"""Guard test for L01 — perception must never globally override other layers.

Asserts that SYM_PERCEPTION_* symptoms enter the MasterEvidenceVector as normal
CF-weighted symptoms and never zero out or suppress other evidence.  This pins
the structural guarantee that prevented V1's perception short-circuit plateau.

v2-arbitrator §2.1: perception gap detection adds CF-weighted evidence only.
v2-design-rules L01: perception fires as a KG symptom, never as a global override.
"""

from __future__ import annotations

from typing import Any

import pytest

from engine.v2.arbitrator import (
    _SYM_PERCEPTION_LEAN_SEEN_RICH,
    _SYM_PERCEPTION_RICH_SEEN_LEAN,
    MasterEvidenceVector,
    _detect_perception_gap,
    arbitrate,
)
from engine.v2.digital_parser import DigitalParserOutput
from engine.v2.dna_core import DNAOutput
from engine.v2.gas_lab import GasLabOutput
from engine.v2.input_model import (
    DiagnosticInput,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)

# ── helpers ─────────────────────────────────────────────────────────────────────


def _sample_ctx() -> VehicleContext:
    return VehicleContext(
        brand="VOLKSWAGEN",
        model="Golf",
        engine_code="EA111_1.2_TSI",
        displacement_cc=1197,
        my=2012,
    )


def _obd(**kwargs: Any) -> OBDRecord:
    defaults: dict[str, Any] = {
        "stft_b1": None, "stft_b2": None,
        "ltft_b1": None, "ltft_b2": None,
        "rpm": 800, "ect_c": 90.0, "iat_c": 30.0,
        "fuel_status": "CL", "obd_lambda": None,
    }
    defaults.update(kwargs)
    return OBDRecord(**{k: v for k, v in defaults.items() if k in OBDRecord.__slots__})


def _validated(obd: OBDRecord | None = None) -> ValidatedInput:
    return ValidatedInput(
        raw=DiagnosticInput(
            vehicle_context=_sample_ctx(),
            dtcs=[],
            analyser_type="5-gas",
            obd=obd,
        ),
        valid_channels={"obd", "gas_idle", "dtcs"},
    )


def _dna_output(is_v_engine: bool = False) -> DNAOutput:
    return DNAOutput(
        engine_state="warm_closed_loop",
        era_bucket="ERA_CAN",
        tech_mask={
            "has_vvt": True, "has_gdi": True,
            "has_turbo": True, "is_v_engine": is_v_engine,
            "has_egr": False, "has_secondary_air": False,
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
    symptoms_idle: list[str] | None = None,
) -> GasLabOutput:
    return GasLabOutput(
        symptoms_idle=symptoms_idle if symptoms_idle is not None else [],
        symptoms_high=[],
        dual_state_tag=None,
        analyser_lambda_idle=analyser_lambda_idle,
        analyser_lambda_high=None,
        baseline_deviation_high=None,
    )


# ── structural L01 guard tests ──────────────────────────────────────────────────


class TestNoPerceptionShortCircuit:
    """L01: perception gap adds evidence — never globally overrides other layers."""

    def test_perception_symptom_coexists_with_digital_symptoms(self) -> None:
        """Digital symptoms survive alongside active perception gap symptom."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.10))
        digital = _digital_output(symptoms=["SYM_DTC_P0171", "SYM_DTC_P0420"])
        go = _gas_output(analyser_lambda_idle=0.90)

        result = arbitrate(vi, dna, digital, go)

        # Perception gap was detected
        assert result.perception_gap is not None
        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in result.active_symptoms
        # Digital symptoms still present at correct CF
        assert result.active_symptoms.get("SYM_DTC_P0171") == 0.70
        assert result.active_symptoms.get("SYM_DTC_P0420") == 0.70

    def test_perception_symptom_coexists_with_gas_symptoms(self) -> None:
        """Gas symptoms survive alongside active perception gap symptom."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.10))
        digital = _digital_output()
        go = _gas_output(
            analyser_lambda_idle=0.90,
            symptoms_idle=["SYM_LAMBDA_LOW", "SYM_HC_HIGH"],
        )

        result = arbitrate(vi, dna, digital, go)

        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in result.active_symptoms
        assert result.active_symptoms.get("SYM_LAMBDA_LOW") == 0.85
        assert result.active_symptoms.get("SYM_HC_HIGH") == 0.85

    def test_no_non_perception_symptom_zeroed(self) -> None:
        """When perception fires, no other active_symptom CF drops to zero."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.10))
        digital = _digital_output(symptoms=["SYM_DTC_P0171"])
        go = _gas_output(
            analyser_lambda_idle=0.90,
            symptoms_idle=["SYM_LAMBDA_LOW"],
        )

        result = arbitrate(vi, dna, digital, go)

        # Perception gap active
        assert result.perception_gap is not None
        # Every non-perception symptom still has CF > 0
        for sym_id, cf in result.active_symptoms.items():
            if "PERCEPTION" not in sym_id:
                assert cf > 0.0, (
                    f"{sym_id} CF={cf} — perception must not zero out other evidence (L01)"
                )

    def test_perception_gap_is_never_invalid_input_marker(self) -> None:
        """Perception gap detection never returns invalid_input state at M3 level."""
        vi = _validated(obd=_obd(obd_lambda=1.10))
        go = _gas_output(analyser_lambda_idle=0.90)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        # Evidence vector is produced — no invalid_input marker
        assert evidence.perception_gap is not None
        assert isinstance(evidence, MasterEvidenceVector)
        # MasterEvidenceVector has no state field (R9 state is M5's domain)
        assert not hasattr(evidence, "state")

    def test_perception_cf_never_exceeds_max(self) -> None:
        """Perception CF is clamped — it can never dominate scoring by magnitude."""
        # Extreme delta: analyser_lambda=0.70 (very lean), obd_lambda=1.50 (very rich)
        vi = _validated(obd=_obd(obd_lambda=1.50))
        go = _gas_output(analyser_lambda_idle=0.70)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in evidence.active_symptoms
        cf = evidence.active_symptoms[_SYM_PERCEPTION_LEAN_SEEN_RICH]
        assert cf == pytest.approx(0.70)  # clamped at max, not delta*6.0
        # 0.70 is ≤ CF for gas symptoms (0.85) — perception never outranks chemistry

    def test_perception_gap_field_is_informational_only(self) -> None:
        """M4 must use active_symptoms entries, not perception_gap field (L01)."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.10))
        digital = _digital_output(symptoms=["SYM_DTC_P0171"])
        go = _gas_output(analyser_lambda_idle=0.90)

        result = arbitrate(vi, dna, digital, go)

        # perception_gap is populated for display purposes
        assert result.perception_gap is not None
        # BUT the symptom emitted into active_symptoms is what M4 scores
        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in result.active_symptoms
        # M4 should use active_symptoms dict, not perception_gap field
        # Structural guarantee: active_symptoms dict is flat — no override layer
        assert all(isinstance(cf, float) for cf in result.active_symptoms.values())

    def test_rich_seen_lean_also_no_override(self) -> None:
        """Both perception gap types (LEAN_SEEN_RICH, RICH_SEEN_LEAN) are safe."""
        vi = _validated(obd=_obd(obd_lambda=0.90))
        go = _gas_output(analyser_lambda_idle=1.10)
        evidence = MasterEvidenceVector()

        _detect_perception_gap(vi, go, evidence)

        assert _SYM_PERCEPTION_RICH_SEEN_LEAN in evidence.active_symptoms
        # Evidence is additive only — no zeroed entries
        assert all(cf > 0.0 for cf in evidence.active_symptoms.values())

    def test_no_perception_gap_means_no_perception_symptoms(self) -> None:
        """When no perception gap detected, no perception symptoms in vector."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.00))
        digital = _digital_output(symptoms=["SYM_DTC_P0171"])
        go = _gas_output(analyser_lambda_idle=1.00)

        result = arbitrate(vi, dna, digital, go)

        assert result.perception_gap is None
        perception_symptoms = [s for s in result.active_symptoms if "PERCEPTION" in s]
        assert len(perception_symptoms) == 0

    def test_arbitrator_output_has_no_global_override_mechanism(self) -> None:
        """MasterEvidenceVector has no field for global overrides (L01 structural)."""
        dna = _dna_output()
        vi = _validated(obd=_obd(obd_lambda=1.10, stft_b1=10.0, ltft_b1=0.0))
        digital = _digital_output(symptoms=["SYM_DTC_P0171", "SYM_DTC_P0420"])
        go = _gas_output(
            analyser_lambda_idle=0.90,
            symptoms_idle=["SYM_LAMBDA_LOW", "SYM_HC_HIGH"],
        )

        result = arbitrate(vi, dna, digital, go)

        # Full smoke test: perception + trim-trend + digital + gas all coexist
        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in result.active_symptoms
        assert result.active_symptoms.get("SYM_DTC_P0171") == 0.70
        assert result.active_symptoms.get("SYM_LAMBDA_LOW") == 0.85
        # No symptom was removed or zeroed
        all_cfs = list(result.active_symptoms.values())
        assert all(cf > 0.0 for cf in all_cfs), (
            f"All symptom CFs must be > 0 (L01): {result.active_symptoms}"
        )
        # cascading_consequences may be non-empty (flood control) but perception
        # symptoms are never added there as a side effect of short-circuit logic
        for sym in result.cascading_consequences:
            assert "PERCEPTION" not in sym, (
                f"Perception symptom {sym} in cascading_consequences — "
                "perception must not suppress itself (L01)"
            )
