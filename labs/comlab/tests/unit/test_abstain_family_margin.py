"""T-V3-3C family-aware abstain margin tests."""

from __future__ import annotations

from typing import Any, cast
from uuid import uuid4

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter, RegistryRow
from tests.unit.test_fault_atlas_router import _make_request, _sanitized


class MockKGNode:
    """Mock KGNode for resolving fault family without DB lookup."""
    def __init__(self, fault_family: str):
        self.fault_family = fault_family
        self.component_group = "unknown"
        self.impacted_subsystems: list[str] = []
        self.mechanical_failure_mode = "Mock Failure"
        self.ui_remediation_steps = ["Inspect component"]
        self.editor_severity_hint = None
        self.differential_siblings: list[str] = []


def _registry_row(fault_id: str, fault_name: str) -> RegistryRow:
    """Build a minimal v1 registry row for routing tests."""
    return RegistryRow(
        fault_id=fault_id,
        fault_name=fault_name,
        target_horizons=["HORIZON_MODERN"],
        preconditions={},
        cross_domain_matrix=cast(
            Any,
            {
                "gas_lab_state": "NORMAL_OPERATION",
                "obd_live_pids": {},
                "dtc_lab_status": {
                    "active_mil": False,
                    "p_code_match": [],
                    "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY",
                },
            },
        ),
        confidence_scoring=cast(
            Any,
            {"base_weight": 0.5, "bonus_on_dtc_match": 0.0},
        ),
    )


def _mock_v2_output(is_fault: bool, code: str, score: float) -> dict[str, Any]:
    """Helper to build a mock v2_output payload dict."""
    return {
        "session_id": uuid4(),
        "execution_meta": {
            "resolved_horizon": "HORIZON_MODERN",
            "degradation_mode": "FULL_FUSION",
            "processing_confidence_rating": "DEGRADED_ASSURANCE" if score < 0.70 else "HIGH_ASSURANCE",
            "vin_confidence": "HIGH",
            "lab_routing_directive": {
                "suppress_gaslab": False,
                "suppress_obd_live_pids": False,
                "suppress_mode06_ui": False,
                "cold_start_mode": False,
                "reasons": []
            }
        },
        "diagnostic_verdict": {
            "is_fault_detected": is_fault,
            "fault_code": code,
            "fault_name": "Mock Fault" if is_fault else "no_fault_detected",
            "fault_family": "catalyst_failure" if is_fault else "no_fault",
            "display_headline": "Mock Headline",
            "confidence_score": score,
            "actionable_remediation": "Inspect",
            "differential_siblings": [],
        },
        "performance_analytics": {
            "kinetic_power_loss_pct": 0.0,
            "catalyst_efficiency_index_pct": 0.0,
            "lambda_perception_delta": 0.0,
            "o2_sensor_bias_verdict": "NORMAL",
            "severity_level": "OPTIMAL_HEALTH",
        },
        "fault_enrichment": {
            "component_group": "engine",
            "impacted_subsystems": [],
            "mechanical_failure_mode": "None",
            "ui_remediation_steps": ["Inspect"],
            "editor_severity_hint": None,
        },
        "user_input_echo_audit": {
            "submitted_at": "2026-07-01T12:00:00Z",
            "groups": []
        }
    }


def test_v1_family_aware_margin(monkeypatch, registry_path):
    """V1 path: margin is computed against the first runner-up with a different family."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=False)
    
    row1 = _registry_row("ERR-CF-001", "catalyst_efficiency_below_threshold")
    row2 = _registry_row("ERR-CF-002", "catalyst_efficiency_limit")
    row3 = _registry_row("ERR-IGN-001", "ignition_misfire")
    
    nodes = {
        "ERR-CF-001": MockKGNode("catalyst_failure"),
        "ERR-CF-002": MockKGNode("catalyst_failure"),
        "ERR-IGN-001": MockKGNode("ignition_fault"),
    }
    monkeypatch.setattr(router._kg, "resolve", lambda fault_id: nodes[fault_id])
    
    # CASE 1: Top runner-up (ERR-CF-002) is same family and within margin (0.83 vs 0.85).
    # Next runner-up (ERR-IGN-001) is different family but outside margin (0.70 vs 0.85).
    # Under family-aware margin, we should NOT abstain.
    mock_triage = {
        "winner": row1,
        "winner_score": 0.85,
        "runner_ups": [(row2, 0.83), (row3, 0.70)]
    }
    monkeypatch.setattr(router, "execute_triage_loop", lambda sanitized: mock_triage)
    
    req = _make_request()
    res = router.route(_sanitized(req))
    
    assert res.diagnostic_verdict.abstained is False
    assert res.diagnostic_verdict.abstain_reason is None

    # CASE 2: Different family runner-up is within margin (ERR-IGN-001 at 0.84 vs 0.85; ABSTAIN_MARGIN=0.02 per T-V3-3D).
    # We should abstain.
    mock_triage_2 = {
        "winner": row1,
        "winner_score": 0.85,
        "runner_ups": [(row2, 0.845), (row3, 0.84)]
    }
    monkeypatch.setattr(router, "execute_triage_loop", lambda sanitized: mock_triage_2)
    res_2 = router.route(_sanitized(req))
    assert res_2.diagnostic_verdict.abstained is True
    assert res_2.diagnostic_verdict.abstain_reason == "margin"


def test_v2_family_aware_margin(monkeypatch, registry_path):
    """V2 path: margin is computed against the first rule with a different family."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=True, enable_delta_v2=False)
    
    mock_out = _mock_v2_output(True, "ERR-CF-001", 0.85)
    
    # CASE 1: Top sibling is same family (catalyst_failure) and within margin.
    # Different family rule (ERR-IGN-001) is outside margin (0.70).
    # We should NOT abstain.
    mock_diagnostics = {
        "scored_rules": [
            {"rule_id": "ERR-CF-001", "fault_family": "catalyst_failure", "score": 0.85},
            {"rule_id": "ERR-CF-002", "fault_family": "catalyst_failure", "score": 0.83},
            {"rule_id": "ERR-IGN-001", "fault_family": "ignition_fault", "score": 0.70},
        ],
        "pruned_rules": [],
        "winner_rule_id": "ERR-CF-001"
    }
    
    monkeypatch.setattr(
        "registry.integration_shim.route_case_with_diagnostics",
        lambda payload: (mock_out, mock_diagnostics)
    )
    
    req = _make_request()
    res = router.route(_sanitized(req))
    
    assert res.diagnostic_verdict.abstained is False
    assert res.diagnostic_verdict.abstain_reason is None

    # CASE 2: Different family rule is within margin (ERR-IGN-001 at 0.84 vs 0.85; ABSTAIN_MARGIN=0.02 per T-V3-3D).
    # We should abstain.
    mock_diagnostics_2 = {
        "scored_rules": [
            {"rule_id": "ERR-CF-001", "fault_family": "catalyst_failure", "score": 0.85},
            {"rule_id": "ERR-CF-002", "fault_family": "catalyst_failure", "score": 0.83},
            {"rule_id": "ERR-IGN-001", "fault_family": "ignition_fault", "score": 0.84},
        ],
        "pruned_rules": [],
        "winner_rule_id": "ERR-CF-001"
    }
    monkeypatch.setattr(
        "registry.integration_shim.route_case_with_diagnostics",
        lambda payload: (mock_out, mock_diagnostics_2)
    )
    res_2 = router.route(_sanitized(req))
    assert res_2.diagnostic_verdict.abstained is True
    assert res_2.diagnostic_verdict.abstain_reason == "margin"
