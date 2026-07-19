"""ECU-hardware digital-lie consumer tests for T-COMV2-ECU-HW-1."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest
from pydantic import ValidationError

import comlab.core.fault_atlas_router as router_module
from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.ecu_hardware_checker import ECUHardwareChecker
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter, RegistryRow
from comlab.schemas.ingestion import (
    OBDLiveDataPayload,
    OrchestratorInboundRequest,
    UserInputEchoAudit,
)
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


def _ecu_hw_router(
    registry_path: Any,
    *,
    enable_ecu_hw: bool,
) -> FaultAtlasRouter:
    """Build a controlled router with global and ECU-fault candidates."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_ecu_hw=enable_ecu_hw,
    )
    router.registry = [
        _rule("ERR-MW-003", 0.79),
        _rule("ERR-EF-001", 0.70),
    ]
    return router


def _digital_lie_request() -> OrchestratorInboundRequest:
    """Build the full coherent ECU hardware-lie request."""
    request = _make_request(
        total_trim_correction_delta=30.0,
        per_bank_trim_delta=3.0,
    )
    assert request.obd_live_data is not None
    request.obd_live_data.intake_air_temp_c = -40.0
    request.obd_live_data.coolant_temp_c = -40.0
    request.obd_live_data.throttle_pos_pct = 100.0
    return request


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("intake_air_temp_c", -40.1),
        ("throttle_pos_pct", 100.1),
    ],
)
def test_ecu_hw_schema_mirrors_bounds(
    field_name: str,
    invalid_value: float,
) -> None:
    """The optional mirrors accept emitter bounds and reject drift."""
    request = _digital_lie_request()
    assert request.obd_live_data is not None
    payload = request.obd_live_data.model_dump(mode="json")

    validated = OBDLiveDataPayload.model_validate(payload)

    assert validated.intake_air_temp_c == -40.0
    assert validated.throttle_pos_pct == 100.0
    payload[field_name] = invalid_value
    with pytest.raises(ValidationError):
        OBDLiveDataPayload.model_validate(payload)


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({}, True),
        ({"intake_air_temp_c": 20.0}, False),
        ({"coolant_temp_c": 20.0}, False),
        ({"throttle_pos_pct": 99.0}, False),
        ({"total_trim_correction_delta": 24.0}, False),
        ({"per_bank_trim_delta": 6.0}, False),
        ({"intake_air_temp_c": None}, False),
        ({"coolant_temp_c": None}, False),
        ({"throttle_pos_pct": None}, False),
        ({"total_trim_correction_delta": None}, False),
        ({"per_bank_trim_delta": None}, True),
    ],
)
def test_ecu_hw_checker_unit(
    overrides: dict[str, float | None],
    expected: bool,
) -> None:
    """The pure checker requires the full coherent, bank-symmetric tuple."""
    values: dict[str, float | None] = {
        "intake_air_temp_c": -40.0,
        "coolant_temp_c": -40.0,
        "throttle_pos_pct": 100.0,
        "total_trim_correction_delta": 30.0,
        "per_bank_trim_delta": 3.0,
    }
    values.update(overrides)

    verdict = ECUHardwareChecker().check(**values)

    assert verdict.is_ecu_hardware_fault is expected
    assert verdict.confidence == (0.80 if expected else 0.0)


def test_ecu_hw_inert_when_off(registry_path: Any) -> None:
    """Flag-off and signature-not-met requests preserve baseline output."""
    request = _digital_lie_request()
    request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    normal_request = request.model_copy(deep=True)
    assert normal_request.obd_live_data is not None
    normal_request.obd_live_data.intake_air_temp_c = 20.0
    absent_request = request.model_copy(deep=True)
    assert absent_request.obd_live_data is not None
    absent_request.obd_live_data.throttle_pos_pct = None

    disabled = _ecu_hw_router(registry_path, enable_ecu_hw=False)
    enabled = _ecu_hw_router(registry_path, enable_ecu_hw=True)

    baseline = disabled.route(_sanitized(normal_request))
    assert disabled.route(_sanitized(request)) == baseline
    assert enabled.route(_sanitized(normal_request)) == baseline
    assert enabled.route(_sanitized(absent_request)) == baseline


def test_ecu_hw_promotes_ecu_fault(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The coherent lie promotes an ECU-fault row and emits evidence."""
    request = _digital_lie_request()
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    result = _ecu_hw_router(
        registry_path,
        enable_ecu_hw=True,
    ).execute_triage_loop(_sanitized(request))

    assert result["winner"] is not None
    assert result["winner"].fault_id == "ERR-EF-001"
    assert result["winner_score"] == 0.80
    assert any(
        name == "ecu_hardware_fault_applied"
        for name, _attributes in tracer.spans["phase.score"].events
    )


def test_ecu_hw_rejects_bank_asymmetry(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bank-asymmetric railed trim remains BANK-FUSE territory."""
    request = _digital_lie_request()
    assert request.obd_live_data is not None
    request.obd_live_data.per_bank_trim_delta = 6.0
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    result = _ecu_hw_router(
        registry_path,
        enable_ecu_hw=True,
    ).execute_triage_loop(_sanitized(request))

    assert result["winner"] is not None
    assert result["winner"].fault_id == "ERR-MW-003"
    assert not any(
        name == "ecu_hardware_fault_applied"
        for name, _attributes in tracer.spans["phase.score"].events
    )
