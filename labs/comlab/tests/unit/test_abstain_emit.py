"""T-V3-3B verdict abstain tests."""

from __future__ import annotations

from typing import Any, cast
from uuid import uuid4

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter, RegistryRow
from tests.unit.test_fault_atlas_router import _make_request, _sanitized


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


# ---------------------------------------------------------------------------
# V1 Path Tests
# ---------------------------------------------------------------------------


def test_v1_abstain_floor(monkeypatch, registry_path):
    """V1 path: winner_score < 0.80 abstains with 'floor'."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=False)
    
    row = _registry_row("ERR-CF-001", "catalyst_efficiency_below_threshold")
    mock_triage = {
        "winner": row,
        "winner_score": 0.75,
        "runner_ups": []
    }
    monkeypatch.setattr(router, "execute_triage_loop", lambda sanitized: mock_triage)
    
    req = _make_request()
    res = router.route(_sanitized(req))
    
    assert res.diagnostic_verdict.is_fault_detected is True
    assert res.diagnostic_verdict.abstained is True
    assert res.diagnostic_verdict.abstain_reason == "floor"
    assert res.diagnostic_verdict.fault_code == "ERR-CF-001"


def test_v1_abstain_margin(monkeypatch, registry_path):
    """V1 path: winner_score - top2_score <= ABSTAIN_MARGIN (0.02, T-V3-3D) abstains with 'margin'."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=False)
    
    row1 = _registry_row("ERR-CF-001", "catalyst_efficiency_below_threshold")
    row2 = _registry_row("ERR-IGN-001", "ignition_misfire")
    
    # winner_score = 0.85, top2_score = 0.84 (diff = 0.01 <= ABSTAIN_MARGIN 0.02)
    mock_triage = {
        "winner": row1,
        "winner_score": 0.85,
        "runner_ups": [(row2, 0.84)]
    }
    monkeypatch.setattr(router, "execute_triage_loop", lambda sanitized: mock_triage)
    
    req = _make_request()
    res = router.route(_sanitized(req))
    
    assert res.diagnostic_verdict.is_fault_detected is True
    assert res.diagnostic_verdict.abstained is True
    assert res.diagnostic_verdict.abstain_reason == "margin"
    # Verify top-3 surface is intact
    assert res.diagnostic_verdict.fault_code == "ERR-CF-001"
    assert len(res.diagnostic_verdict.differential_siblings) >= 1
    assert any(sib.fault_id == "ERR-IGN-001" for sib in res.diagnostic_verdict.differential_siblings)


def test_v1_no_abstain(monkeypatch, registry_path):
    """V1 path: winner_score >= 0.80 and margin > ABSTAIN_MARGIN (0.02) does not abstain."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=False)
    
    row1 = _registry_row("ERR-CF-001", "catalyst_efficiency_below_threshold")
    row2 = _registry_row("ERR-IGN-001", "ignition_misfire")
    
    # winner_score = 0.85, top2_score = 0.75 (diff = 0.10 > ABSTAIN_MARGIN 0.02)
    mock_triage = {
        "winner": row1,
        "winner_score": 0.85,
        "runner_ups": [(row2, 0.75)]
    }
    monkeypatch.setattr(router, "execute_triage_loop", lambda sanitized: mock_triage)
    
    req = _make_request()
    res = router.route(_sanitized(req))
    
    assert res.diagnostic_verdict.is_fault_detected is True
    assert res.diagnostic_verdict.abstained is False
    assert res.diagnostic_verdict.abstain_reason is None


def test_v1_healthy_no_abstain(monkeypatch, registry_path):
    """V1 path: no fault detected does not abstain."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=False)
    
    mock_triage = {
        "winner": None,
        "winner_score": 0.0,
        "runner_ups": []
    }
    monkeypatch.setattr(router, "execute_triage_loop", lambda sanitized: mock_triage)
    
    req = _make_request()
    res = router.route(_sanitized(req))
    
    assert res.diagnostic_verdict.is_fault_detected is False
    assert res.diagnostic_verdict.abstained is False
    assert res.diagnostic_verdict.abstain_reason is None


# ---------------------------------------------------------------------------
# V2 Path Tests
# ---------------------------------------------------------------------------


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


def test_v2_abstain_floor(monkeypatch, registry_path):
    """V2 path: winner_score < 0.80 abstains with 'floor'."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=True, enable_delta_v2=False)
    
    mock_out = _mock_v2_output(True, "ERR-CF-001", 0.75)
    mock_diagnostics = {
        "scored_rules": [
            {"rule_id": "ERR-CF-001", "fault_family": "catalyst_failure", "score": 0.75}
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
    
    assert res.diagnostic_verdict.is_fault_detected is True
    assert res.diagnostic_verdict.abstained is True
    assert res.diagnostic_verdict.abstain_reason == "floor"
    assert res.diagnostic_verdict.fault_code == "ERR-CF-001"


def test_v2_abstain_margin(monkeypatch, registry_path):
    """V2 path: margin <= ABSTAIN_MARGIN (0.02, T-V3-3D) abstains with 'margin'."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=True, enable_delta_v2=False)
    
    mock_out = _mock_v2_output(True, "ERR-CF-001", 0.85)
    mock_diagnostics = {
        "scored_rules": [
            {"rule_id": "ERR-CF-001", "fault_family": "catalyst_failure", "score": 0.85},
            {"rule_id": "ERR-IGN-001", "fault_family": "ignition_fault", "score": 0.84},
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
    
    assert res.diagnostic_verdict.is_fault_detected is True
    assert res.diagnostic_verdict.abstained is True
    assert res.diagnostic_verdict.abstain_reason == "margin"
    assert res.diagnostic_verdict.fault_code == "ERR-CF-001"
    # Verify siblings are present
    assert len(res.diagnostic_verdict.differential_siblings) >= 1
    assert any(sib.fault_id == "ERR-IGN-001" for sib in res.diagnostic_verdict.differential_siblings)


def test_v2_no_abstain(monkeypatch, registry_path):
    """V2 path: winner_score >= 0.80 and margin > ABSTAIN_MARGIN (0.02) does not abstain."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=True, enable_delta_v2=False)
    
    mock_out = _mock_v2_output(True, "ERR-CF-001", 0.85)
    mock_diagnostics = {
        "scored_rules": [
            {"rule_id": "ERR-CF-001", "fault_family": "catalyst_failure", "score": 0.85},
            {"rule_id": "ERR-IGN-001", "fault_family": "ignition_fault", "score": 0.75},
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
    
    assert res.diagnostic_verdict.is_fault_detected is True
    assert res.diagnostic_verdict.abstained is False
    assert res.diagnostic_verdict.abstain_reason is None


def test_v2_healthy_no_abstain(monkeypatch, registry_path):
    """V2 path: no fault detected does not abstain."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=True, enable_delta_v2=False)
    
    mock_out = _mock_v2_output(False, "OPTIMAL_HEALTH", 0.0)
    mock_diagnostics = {
        "scored_rules": [],
        "pruned_rules": [],
        "winner_rule_id": "__NONE__"
    }
    
    monkeypatch.setattr(
        "registry.integration_shim.route_case_with_diagnostics",
        lambda payload: (mock_out, mock_diagnostics)
    )
    
    req = _make_request()
    res = router.route(_sanitized(req))
    
    assert res.diagnostic_verdict.is_fault_detected is False
    assert res.diagnostic_verdict.abstained is False
    assert res.diagnostic_verdict.abstain_reason is None
