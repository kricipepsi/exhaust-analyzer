"""Fuel-system-status closed-loop gate tests for T-COMV2-FUELSYS-GATE-1."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

import comlab.core.fault_atlas_router as router_module
from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter, RegistryRow
from comlab.schemas.ingestion import OBDLiveDataPayload, UserInputEchoAudit
from comlab.schemas.vocabulary import FuelSystemStatus
from tests.unit.test_fault_atlas_router import (
    _RecordingTracer,
    _make_request,
    _sanitized,
)


def _rule(fault_id: str, base_weight: float) -> RegistryRow:
    """Build one controlled NORMAL_OPERATION registry row."""
    return RegistryRow.model_validate(
        {
            "fault_id": fault_id,
            "fault_name": fault_id,
            "target_horizons": [
                "HORIZON_LEGACY",
                "HORIZON_ADAPTIVE",
                "HORIZON_MODERN",
            ],
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
                "base_weight": base_weight,
                "bonus_on_dtc_match": 0.0,
            },
        }
    )


def _fuelsys_router(
    registry_path: Any,
    *,
    enable_fuelsys_gate: bool,
    trim_fault_id: str = "ERR-LC-001",
) -> FaultAtlasRouter:
    """Build a controlled router with trim-driven and non-trim candidates."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_fuelsys_gate=enable_fuelsys_gate,
    )
    router.registry = [
        _rule(trim_fault_id, 0.79),
        _rule("ERR-MW-003", 0.69),
    ]
    return router


def test_fuelsys_schema_mirrors_enum() -> None:
    """The optional JSON field validates to COMLab's local enum mirror."""
    request = _make_request()
    assert request.obd_live_data is not None
    payload = request.obd_live_data.model_dump(mode="json")
    payload["fuel_system_status"] = "OL"

    validated = OBDLiveDataPayload.model_validate(payload)

    assert validated.fuel_system_status == FuelSystemStatus.OL


def test_fuelsys_inert_when_off(registry_path: Any) -> None:
    """Flag-off open loop and flag-on closed loop are byte-identical."""
    open_loop_request = _make_request()
    open_loop_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    assert open_loop_request.obd_live_data is not None
    open_loop_request.obd_live_data.fuel_system_status = FuelSystemStatus.OL_FAULT

    closed_loop_request = open_loop_request.model_copy(deep=True)
    assert closed_loop_request.obd_live_data is not None
    closed_loop_request.obd_live_data.fuel_system_status = FuelSystemStatus.CL

    disabled = _fuelsys_router(registry_path, enable_fuelsys_gate=False)
    enabled = _fuelsys_router(registry_path, enable_fuelsys_gate=True)

    baseline = disabled.route(_sanitized(open_loop_request))
    assert enabled.route(_sanitized(closed_loop_request)) == baseline


def test_fuelsys_absent_is_inert(registry_path: Any) -> None:
    """An absent OBD-live fuel-system status preserves baseline output."""
    request = _make_request()
    request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    assert request.obd_live_data is not None
    assert request.obd_live_data.fuel_system_status is None

    disabled = _fuelsys_router(registry_path, enable_fuelsys_gate=False)
    enabled = _fuelsys_router(registry_path, enable_fuelsys_gate=True)

    baseline = disabled.route(_sanitized(request))
    assert enabled.route(_sanitized(request)) == baseline


@pytest.mark.parametrize("trim_fault_id", ["ERR-LC-001", "ERR-RM-003"])
@pytest.mark.parametrize(
    "fuel_system_status",
    [
        FuelSystemStatus.OL,
        FuelSystemStatus.OL_DRIVE,
        FuelSystemStatus.OL_FAULT,
    ],
)
def test_fuelsys_open_loop_demotes_trim(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
    trim_fault_id: str,
    fuel_system_status: FuelSystemStatus,
) -> None:
    """Open loop demotes lean/rich evidence below the winner threshold."""
    request = _make_request()
    assert request.obd_live_data is not None
    request.obd_live_data.fuel_system_status = fuel_system_status

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    result = _fuelsys_router(
        registry_path,
        enable_fuelsys_gate=True,
        trim_fault_id=trim_fault_id,
    ).execute_triage_loop(_sanitized(request))

    assert result["winner"] is None
    assert result["winner_score"] == 0.0
    event = next(
        attributes
        for name, attributes in tracer.spans["phase.score"].events
        if name == "fuel_system_gated"
    )
    assert event["rule_id"] == trim_fault_id
    assert event["fuel_system_status"] == fuel_system_status.value
    assert event["score_before"] == 0.79
    assert event["score_after"] == 0.60
