"""LabPipelineAggregator.abort_incomplete — the public input-incomplete abort.

wired calls ``abort_incomplete(metadata, error_code, message)`` when a required
input is missing and no ``OrchestratorInboundRequest`` can be built (its
``gas_lab_output`` is required). The output is the same ``FATAL_INCOMPLETE``
shape that the Stage-A fatal gates produce.

Source: T-AUD-1a, ruling R0 (Cowork 008).
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import (
    OrchestratorInboundRequest,
    SessionMetadata,
    UserInputEchoAudit,
)
from comlab.schemas.vocabulary import VinConfidence


def _metadata(
    horizon: str = "HORIZON_LEGACY", vin_confidence: VinConfidence = VinConfidence.PARTIAL
) -> SessionMetadata:
    return SessionMetadata(
        session_id=uuid4(),
        vin_dna_string="WME01MC01XH072806",
        resolved_horizon=horizon,
        cylinder_count=4,
        vin_confidence=vin_confidence,
    )


def _request_payload() -> dict:
    return {
        "metadata": {
            "session_id": str(uuid4()),
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": "HORIZON_ADAPTIVE",
            "cylinder_count": 4,
        },
        "gas_lab_output": {
            "chemical_state": "NORMAL_OPERATION",
            "gas_co": 0.5,
            "gas_hc": 50,
            "gas_co2": 14.0,
            "gas_o2": 1.0,
            "gas_nox": 200,
            "lambda_chem": 1.0,
            "sample_validity": "INVALID",
        },
    }


def test_abort_incomplete_fatal_incomplete_from_metadata_only() -> None:
    """NEW: no request needed; verdict is FATAL_INCOMPLETE / invalid_input."""
    meta = _metadata()
    out = LabPipelineAggregator().abort_incomplete(
        meta, "GAS_INPUT_INCOMPLETE", "Enter the missing low-idle gas values: co2."
    )
    em, v = out.execution_meta, out.diagnostic_verdict
    assert out.session_id == meta.session_id
    assert em.degradation_mode == "FATAL_INCOMPLETE"
    assert em.resolved_horizon == "HORIZON_LEGACY"
    assert em.vin_confidence == "PARTIAL"
    assert em.processing_confidence_rating == "LOW_CERTAINTY"
    assert v.fault_code == "GAS_INPUT_INCOMPLETE"
    assert v.fault_family == "invalid_input"
    assert v.is_fault_detected is False
    assert v.confidence_score == 0.0
    assert v.actionable_remediation == "Enter the missing low-idle gas values: co2."
    assert v.differential_siblings == []


def test_abort_incomplete_unknown_horizon_defaults_modern() -> None:
    """NEW: an unknown horizon string resolves as process() does (MODERN)."""
    out = LabPipelineAggregator().abort_incomplete(_metadata(horizon="HORIZON_UNKNOWN"), "X", "m")
    assert out.execution_meta.resolved_horizon == "HORIZON_MODERN"


def test_abort_incomplete_carries_echo_or_sentinel() -> None:
    """NEW: a given echo passes through verbatim; no echo gives the empty sentinel."""
    agg = LabPipelineAggregator()
    echo = UserInputEchoAudit(submitted_at=datetime(2026, 1, 1, tzinfo=timezone.utc), groups=[])
    assert agg.abort_incomplete(_metadata(), "X", "m", echo=echo).user_input_echo_audit == echo
    sentinel = agg.abort_incomplete(_metadata(), "X", "m").user_input_echo_audit
    assert sentinel.groups == []


def test_fatal_gate_output_fields_pinned() -> None:
    """PIN: the Stage-A fatal-gate output is unchanged by the refactor."""
    request = OrchestratorInboundRequest(**_request_payload())
    out = LabPipelineAggregator(enable_fatal_gates=True).process(request)
    em, v = out.execution_meta, out.diagnostic_verdict
    assert out.session_id == request.metadata.session_id
    assert em.degradation_mode == "FATAL_INCOMPLETE"
    assert em.resolved_horizon == "HORIZON_ADAPTIVE"
    assert em.vin_confidence == "HIGH"
    assert em.lab_routing_directive.reasons == []
    assert v.fault_code == "ERR-ABORT-001"
    assert v.fault_name == "Fatal Abort: ERR-ABORT-001"
    assert v.fault_family == "invalid_input"
    assert v.confidence_score == 0.0
    assert v.display_headline == v.actionable_remediation[: len(v.display_headline)]
    assert out.fault_enrichment.ui_remediation_steps == [v.actionable_remediation]
    assert out.performance_analytics.severity_level == "OPTIMAL_HEALTH"
    assert out.user_input_echo_audit.groups == []
