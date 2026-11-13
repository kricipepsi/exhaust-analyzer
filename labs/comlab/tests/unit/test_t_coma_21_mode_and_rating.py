"""T-COMA-21 (F-C1-11, F-C1-12): degradation_mode states lab completeness; the rating is the verdict score's band."""
from __future__ import annotations

import copy
import logging
from typing import Any

import pytest
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from comlab.schemas.response import DiagnosticVerdict

logging.disable(logging.CRITICAL)
A = LabPipelineAggregator


def _request(*, horizon: str = "HORIZON_MODERN", obd: bool = True, engine_state: str = "running") -> OrchestratorInboundRequest:
    raw: dict[str, Any] = {
        "metadata": {
            "session_id": "6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60", "vin_dna_string": "WVWZZZ1JZ3W000001",
            "resolved_horizon": horizon, "cylinder_count": 4, "vin_confidence": "HIGH",
        },
        "gas_lab_output": {
            "chemical_state": "RICH_MIXTURE", "gas_co": 0.3, "gas_hc": 80, "gas_co2": 14.8, "gas_o2": 0.4,
            "gas_nox": 50, "lambda_chem": 1.0, "sample_validity": "VALID",
        },
        "obd_live_data": {
            "engine_warmed": True, "total_trim_correction_delta": 0.0,
            "normalized_obd_lambda": 1.0, "ve_pct": 72.0, "ve_validity": "VALID",
            "rpm_state_bucket": "STABILIZED_IDLE", "trim_analytics_gate": "VALID",
            "o2_failure_mode": "NO_FAULT", "maf_status": "REAL_SENSOR_FEED", "map_status": "REAL_SENSOR_FEED",
        } if obd else None,
        "dtc_lab_output": None,
        "symptom_dna": {"environmental_conditions": {"engine_state": engine_state, "occurs_during": "always"}},
    }
    return OrchestratorInboundRequest.model_validate(copy.deepcopy(raw))


@pytest.mark.parametrize("obd, engine_state, mode", [
    (True, "running", "FULL_FUSION"),
    (False, "running", "GAS_DOMINANT"),
    (True, "cranking", "GAS_DOMINANT"),
])
def test_degradation_mode_states_lab_completeness(obd: bool, engine_state: str, mode: str) -> None:
    out = A().process(_request(obd=obd, engine_state=engine_state))
    assert out.execution_meta.degradation_mode == mode


def test_rating_does_not_depend_on_the_era() -> None:
    legacy = A().process(_request(horizon="HORIZON_LEGACY"))
    modern = A().process(_request(horizon="HORIZON_MODERN"))
    assert legacy.diagnostic_verdict.confidence_score == modern.diagnostic_verdict.confidence_score
    assert legacy.execution_meta.processing_confidence_rating == modern.execution_meta.processing_confidence_rating


def _verdict(score: float, abstained: bool = False) -> DiagnosticVerdict:
    return DiagnosticVerdict(is_fault_detected=True, fault_code="X", fault_name="x", fault_family="misfire",
                             display_headline="x", confidence_score=score, actionable_remediation="",
                             abstained=abstained)


@pytest.mark.parametrize("score, abstained, mode, tier", [
    (0.80, False, "FULL_FUSION", "HIGH_ASSURANCE"),
    (0.79, False, "FULL_FUSION", "DEGRADED_ASSURANCE"),
    (0.50, False, "FULL_FUSION", "DEGRADED_ASSURANCE"),
    (0.49, False, "FULL_FUSION", "LOW_CERTAINTY"),
    (0.95, False, "GAS_DOMINANT", "DEGRADED_ASSURANCE"),
    (0.95, True, "FULL_FUSION", "LOW_CERTAINTY"),
])
def test_tier_is_the_score_band(score: float, abstained: bool, mode: str, tier: str) -> None:
    assert A._confidence_for(_verdict(score, abstained), [], mode) == tier


def test_invalid_sample_is_low_certainty() -> None:
    from comlab.schemas.vocabulary import LabRoutingDirectiveReason as R

    assert A._confidence_for(_verdict(0.95), [R.GAS_SAMPLE_INVALID], "FULL_FUSION") == "LOW_CERTAINTY"


def test_gaslab_suppression_alone_is_gas_dominant() -> None:
    from types import SimpleNamespace as NS

    directive = NS(suppress_gaslab=True, suppress_obd_live_pids=False)
    assert A._map_degradation(directive, _request()) == "GAS_DOMINANT"


def test_process_caps_a_high_score_without_obd() -> None:
    out = A().process(_request(obd=False))
    assert out.diagnostic_verdict.confidence_score >= 0.80
    assert out.execution_meta.degradation_mode == "GAS_DOMINANT"
    assert out.execution_meta.processing_confidence_rating == "DEGRADED_ASSURANCE"
