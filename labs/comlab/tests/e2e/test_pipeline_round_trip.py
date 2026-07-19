"""End-to-end pipeline round-trip tests — T-P4-2 / T-P6-4.

Verifies that ``LabPipelineAggregator.process()`` produces a valid
``OrchestratorFinalUIOutput`` with Stage C KG enrichment populated.

Normal-path tests exercise the real ``FaultAtlasRouter`` (no ``fault_code=``
override).  Override-path tests keep ``fault_code=`` for targeted enrichment
and edge-case coverage.

Marked ``e2e`` so unit runs (``pytest -m "not e2e"``) skip it.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from tests.fixtures import mock_dtc_lab, mock_gas_lab, mock_obd_lab


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _make_request(
    *,
    session_id: str | None = None,
    horizon: str = "HORIZON_MODERN",
    gas_payload: dict | None = None,
    obd_payload: dict | None = None,
    dtc_payload: dict | None = None,
) -> OrchestratorInboundRequest:
    """Build a minimal valid ``OrchestratorInboundRequest``."""
    sid = session_id or str(uuid4())
    return OrchestratorInboundRequest.model_validate({
        "metadata": {
            "session_id": sid,
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": horizon,
            "cylinder_count": 4,
        },
        "gas_lab_output": gas_payload or mock_gas_lab.warm_idle_baseline(),
        "obd_live_data": obd_payload or mock_obd_lab.warm_idle_baseline(),
        "dtc_lab_output": dtc_payload or mock_dtc_lab.no_codes(),
        "symptom_dna": {},
    })


# ---------------------------------------------------------------------------
# real routing tests (no fault_code= override)
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_pipeline_real_routing_diagnoses_fault():
    """NORMAL_OPERATION + negative LTFT → router diagnoses ERR-CF-005 (catalyst masking).

    ERR-CF-005 matches NORMAL_OPERATION on all horizons with GAS_ONLY strategy,
    LTFT ≤ -10% PID trigger, base_weight 0.75 ≥ 0.70 confidence threshold.
    lld: §6.4 — minimum confidence threshold gate (T-P6-14).
    """
    import copy
    dtc_payload = copy.deepcopy(mock_dtc_lab.no_codes())
    dtc_payload["freeze_frame"]["long_term_ft1"] = -15.0
    request = _make_request(dtc_payload=dtc_payload)
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request)  # no fault_code= override

    assert result.diagnostic_verdict.is_fault_detected is True
    assert result.diagnostic_verdict.fault_code == "ERR-CF-005"
    assert result.diagnostic_verdict.fault_family == "catalyst_failure"

    fe = result.fault_enrichment
    assert fe.component_group, "component_group should not be empty"
    assert fe.impacted_subsystems, "impacted_subsystems should not be empty"
    assert fe.mechanical_failure_mode, "mechanical_failure_mode should not be empty"
    assert fe.ui_remediation_steps, "ui_remediation_steps should not be empty"

    siblings = result.diagnostic_verdict.differential_siblings
    assert siblings, "differential_siblings should not be empty"
    assert len(siblings) <= 5, "max 5 siblings per LLD §3.3 Q1"


@pytest.mark.e2e
def test_pipeline_real_routing_no_fault_optimal_health():
    """STOICHIOMETRIC_BURN matches no registry rule → OPTIMAL_HEALTH verdict."""
    request = _make_request(gas_payload=mock_gas_lab.healthy_baseline())
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request)  # no fault_code= override

    assert result.diagnostic_verdict.is_fault_detected is False
    assert result.diagnostic_verdict.fault_code == "OPTIMAL_HEALTH"
    assert result.performance_analytics.severity_level == "OPTIMAL_HEALTH"


@pytest.mark.e2e
def test_pipeline_real_routing_echo_audit():
    """Normal path: echo audit is carried through when no user_input_echo_audit."""
    request = _make_request()
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request)  # no fault_code= override

    echo = result.user_input_echo_audit
    assert echo.groups == []
    assert echo.submitted_at is not None


# ---------------------------------------------------------------------------
# override-path tests (fault_code= test hook — targeted enrichment coverage)
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_pipeline_override_fault_enrichment_populated():
    """fault_code=ERR-RM-001 → enrichment populated from KG."""
    request = _make_request()
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request, fault_code="ERR-RM-001")

    fe = result.fault_enrichment
    assert fe.component_group, "component_group should not be empty"
    assert fe.impacted_subsystems, "impacted_subsystems should not be empty"
    assert fe.mechanical_failure_mode, "mechanical_failure_mode should not be empty"
    assert fe.ui_remediation_steps, "ui_remediation_steps should not be empty"

    assert result.session_id is not None
    assert result.execution_meta.resolved_horizon == "HORIZON_MODERN"
    assert result.diagnostic_verdict.fault_code == "ERR-RM-001"


@pytest.mark.e2e
def test_pipeline_override_differential_siblings():
    """fault_code=ERR-RM-001 → editor-curated differential siblings present."""
    request = _make_request()
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request, fault_code="ERR-RM-001")

    siblings = result.diagnostic_verdict.differential_siblings
    assert siblings, "differential_siblings should not be empty"
    assert len(siblings) <= 5, "max 5 siblings per LLD §3.3 Q1"

    for sib in siblings:
        assert sib.source == "editor_curated", f"{sib.fault_id}: expected editor_curated"
        assert sib.fault_id, "fault_id should not be empty"
        assert sib.fault_name, "fault_name should not be empty"


@pytest.mark.e2e
def test_pipeline_override_degraded_unknown_fault():
    """fault_code=ERR-UNKNOWN-999 → degraded FaultEnrichment."""
    request = _make_request()
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request, fault_code="ERR-UNKNOWN-999")

    fe = result.fault_enrichment
    assert fe.component_group == ""
    assert fe.impacted_subsystems == []
    assert fe.mechanical_failure_mode == ""
    assert len(fe.ui_remediation_steps) == 1
    assert "Unknown fault code" in fe.ui_remediation_steps[0]
    assert result.diagnostic_verdict.fault_code == "ERR-UNKNOWN-999"
