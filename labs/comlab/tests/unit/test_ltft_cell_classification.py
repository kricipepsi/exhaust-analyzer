from datetime import datetime, timezone
import pytest
from typing import Any

from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import (
    FaultAtlasRouter,
    RegistryRow,
    _ltft_cell_pattern,
)
from comlab.core import fault_atlas_router as router_module
from comlab.schemas.ingestion import (
    UserInputEchoAudit,
)
from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from tests.unit.test_fault_atlas_router import (
    _RecordingTracer,
    _make_request,
    _sanitized,
)


def _ltft_cell_router(
    registry_path: str,
    *,
    enable_ltft_cell: bool,
) -> FaultAtlasRouter:
    """Build a router with rules for testing load-cell LTFT re-ranking."""
    router = FaultAtlasRouter(
        registry_path,
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_ltft_cell=enable_ltft_cell,
    )
    router.registry = [
        RegistryRow.model_validate({
            "fault_id": "ERR-MW-003",
            "fault_name": "mechanical_wear_candidate",
            "target_horizons": ["HORIZON_LEGACY", "HORIZON_ADAPTIVE", "HORIZON_MODERN"],
            "cross_domain_matrix": {
                "gas_lab_state": "NORMAL_OPERATION",
                "obd_live_pids": {},
                "dtc_lab_status": {
                    "active_mil": False,
                    "p_code_match": [],
                    "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY",
                },
            },
            "confidence_scoring": {
                "base_weight": 0.79,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-LC-001",
            "fault_name": "lean_condition_candidate",
            "target_horizons": ["HORIZON_LEGACY", "HORIZON_ADAPTIVE", "HORIZON_MODERN"],
            "cross_domain_matrix": {
                "gas_lab_state": "NORMAL_OPERATION",
                "obd_live_pids": {},
                "dtc_lab_status": {
                    "active_mil": False,
                    "p_code_match": [],
                    "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY",
                },
            },
            "confidence_scoring": {
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-SF-001",
            "fault_name": "sensor_fault_candidate",
            "target_horizons": ["HORIZON_LEGACY", "HORIZON_ADAPTIVE", "HORIZON_MODERN"],
            "cross_domain_matrix": {
                "gas_lab_state": "NORMAL_OPERATION",
                "obd_live_pids": {},
                "dtc_lab_status": {
                    "active_mil": False,
                    "p_code_match": [],
                    "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY",
                },
            },
            "confidence_scoring": {
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]
    return router


def test_ltft_cell_pattern_classification() -> None:
    """Verify _ltft_cell_pattern handles vectors correctly."""
    assert _ltft_cell_pattern(None) == "UNAVAILABLE"
    assert _ltft_cell_pattern({}) == "UNAVAILABLE"

    # lean (> +5 %) across all populated cells -> GLOBAL
    assert _ltft_cell_pattern({0: 6.0}) == "GLOBAL"
    assert _ltft_cell_pattern({0: 5.1, 1: 10.0}) == "GLOBAL"

    # lean in a subset of cells -> LOCALISED
    assert _ltft_cell_pattern({0: 6.0, 1: 4.9}) == "LOCALISED"
    assert _ltft_cell_pattern({0: 5.0, 1: 5.1}) == "LOCALISED"

    # otherwise -> WITHIN_SPEC
    assert _ltft_cell_pattern({0: 5.0}) == "WITHIN_SPEC"
    assert _ltft_cell_pattern({0: -2.0, 1: 3.0}) == "WITHIN_SPEC"


def test_ltft_cell_inert_when_off(registry_path: Any) -> None:
    """Flag-off, absent-field, and within-spec inputs are byte-identical."""
    baseline_request = _make_request()
    baseline_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )

    # A localized-lean vector
    asymmetric_request = baseline_request.model_copy(deep=True)
    assert asymmetric_request.obd_live_data is not None
    asymmetric_request.obd_live_data.ltft_cell_vector = {0: 10.0, 1: 2.0}

    disabled = _ltft_cell_router(str(registry_path), enable_ltft_cell=False)
    enabled = _ltft_cell_router(str(registry_path), enable_ltft_cell=True)

    baseline = disabled.route(_sanitized(baseline_request))
    flag_off = disabled.route(_sanitized(asymmetric_request))
    field_absent = enabled.route(_sanitized(baseline_request))

    assert flag_off == baseline
    assert field_absent == baseline

    # within spec vector should also be inert
    within_spec_request = baseline_request.model_copy(deep=True)
    assert within_spec_request.obd_live_data is not None
    within_spec_request.obd_live_data.ltft_cell_vector = {0: 3.0, 1: 4.0}
    within_spec = enabled.route(_sanitized(within_spec_request))
    assert within_spec == baseline


def test_ltft_cell_localised_routes_region(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """LOCALISED load-cell evidence boosts lean_condition and fires span."""
    request = _make_request()
    assert request.obd_live_data is not None
    request.obd_live_data.ltft_cell_vector = {0: 10.0, 1: 2.0}  # localized lean

    disabled = _ltft_cell_router(str(registry_path), enable_ltft_cell=False)
    enabled = _ltft_cell_router(str(registry_path), enable_ltft_cell=True)

    # Under disabled, ERR-MW-003 (mechanical_wear, 0.79) wins over ERR-LC-001 (lean_condition, 0.70)
    baseline = disabled.execute_triage_loop(_sanitized(request))
    assert baseline["winner"] is not None
    assert baseline["winner"].fault_id == "ERR-MW-003"

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    # Under enabled, LOCALISED pattern boosts lean_condition (ERR-LC-001) to 0.80.
    # It does NOT boost sensor_fault (ERR-SF-001 stays 0.70) or mechanical_wear.
    # So ERR-LC-001 should win!
    promoted = enabled.execute_triage_loop(_sanitized(request))
    assert promoted["winner"] is not None
    assert promoted["winner"].fault_id == "ERR-LC-001"
    assert promoted["winner_score"] == 0.80

    assert "ltft_cell_classified" in tracer.spans
    span = tracer.spans["ltft_cell_classified"]
    assert span.attributes["router.ltft_cell_pattern"] == "LOCALISED"
    assert any(name == "ltft_cell_classified" for name, _attrs in span.events)


def test_ltft_cell_global_routes_supply(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GLOBAL load-cell evidence boosts both lean_condition and sensor_fault."""
    request = _make_request()
    assert request.obd_live_data is not None
    request.obd_live_data.ltft_cell_vector = {0: 10.0, 1: 12.0}  # global lean

    disabled = _ltft_cell_router(str(registry_path), enable_ltft_cell=False)
    enabled = _ltft_cell_router(str(registry_path), enable_ltft_cell=True)

    baseline = disabled.execute_triage_loop(_sanitized(request))
    assert baseline["winner"] is not None
    assert baseline["winner"].fault_id == "ERR-MW-003"

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    # Under enabled, GLOBAL boosts BOTH lean_condition (ERR-LC-001) AND sensor_fault (ERR-SF-001) to 0.80.
    # So they both tie at 0.80 and beat ERR-MW-003 (0.79).
    # (By order in registry, ERR-LC-001 is placed before ERR-SF-001 so it should be the winner)
    promoted = enabled.execute_triage_loop(_sanitized(request))
    assert promoted["winner"] is not None
    assert promoted["winner"].fault_id == "ERR-LC-001"
    assert promoted["winner_score"] == 0.80

    # Let's verify that BOTH got boosted by checking the scored_rules or event logs.
    assert "ltft_cell_classified" in tracer.spans
    span = tracer.spans["ltft_cell_classified"]
    assert span.attributes["router.ltft_cell_pattern"] == "GLOBAL"

    applied_events = [attrs for name, attrs in span.events if name == "ltft_cell_re_ranking_applied"]
    assert len(applied_events) == 2
    rule_ids = {evt["rule_id"] for evt in applied_events}
    assert rule_ids == {"ERR-LC-001", "ERR-SF-001"}
