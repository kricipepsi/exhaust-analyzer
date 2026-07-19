"""VE-as-evidence circularity gate tests for T-COMV2-VE-GATE-1."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

import comlab.core.fault_atlas_router as router_module
from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter, RegistryRow
from comlab.schemas.ingestion import OBDLiveDataPayload, UserInputEchoAudit
from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    EngineStateBucket,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    TrimAnalyticsGate,
    VEValidity,
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


def _ve_router(
    registry_path: Any,
    *,
    enable_ve_gate: bool,
) -> FaultAtlasRouter:
    """Build a controlled router with global, lean, and sensor candidates."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_ve_gate=enable_ve_gate,
    )
    router.registry = [
        _rule("ERR-MW-003", 0.79),
        _rule("ERR-LC-001", 0.70),
        _rule("ERR-LC-002", 0.69),
        _rule("ERR-SF-008", 0.68),
    ]
    return router


@pytest.mark.parametrize("ve_validity", [VEValidity.VALID, VEValidity.UNKNOWN])
def test_ve_gate_inert_when_off_or_unavailable(
    registry_path: Any,
    ve_validity: VEValidity,
) -> None:
    """Flag-off, trusted/unknown VE, and absent architecture are byte-identical."""
    fault_request = _make_request()
    fault_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    fault_request.metadata.air_metering_strategy = (
        AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK
    )
    assert fault_request.obd_live_data is not None
    fault_request.obd_live_data.ve_pct = 45.0
    fault_request.obd_live_data.ve_validity = VEValidity.FAULT_VE_IDLE_COLLAPSE

    unavailable_request = fault_request.model_copy(deep=True)
    assert unavailable_request.obd_live_data is not None
    unavailable_request.obd_live_data.ve_validity = ve_validity

    absent_architecture = fault_request.model_copy(deep=True)
    absent_architecture.metadata.air_metering_strategy = None

    disabled = _ve_router(registry_path, enable_ve_gate=False)
    enabled = _ve_router(registry_path, enable_ve_gate=True)

    baseline = disabled.route(_sanitized(fault_request))
    assert enabled.route(_sanitized(unavailable_request)) == baseline
    assert enabled.route(_sanitized(absent_architecture)) == baseline


def test_ve_dual_promotes_lean(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dual-sensor idle-collapse evidence promotes the vacuum-leak member."""
    request = _make_request()
    request.metadata.air_metering_strategy = (
        AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK
    )
    assert request.obd_live_data is not None
    request.obd_live_data.ve_pct = 45.0
    request.obd_live_data.ve_validity = VEValidity.FAULT_VE_IDLE_COLLAPSE

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    result = _ve_router(
        registry_path,
        enable_ve_gate=True,
    ).execute_triage_loop(_sanitized(request))

    assert result["winner"] is not None
    assert result["winner"].fault_id == "ERR-LC-001"
    assert result["winner_score"] == 0.80
    assert any(
        name == "ve_evidence_applied"
        for name, _attributes in tracer.spans["phase.score"].events
    )


def test_ve_single_sensor_is_circular(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Single-sensor VE faults emit rationality evidence without a lean lift."""
    request = _make_request()
    request.metadata.air_metering_strategy = (
        AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY
    )
    assert request.obd_live_data is not None
    request.obd_live_data.ve_pct = 45.0
    request.obd_live_data.ve_validity = VEValidity.FAULT_VE_IDLE_COLLAPSE

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    result = _ve_router(
        registry_path,
        enable_ve_gate=True,
    ).execute_triage_loop(_sanitized(request))

    assert result["winner"] is not None
    assert result["winner"].fault_id == "ERR-MW-003"
    events = tracer.spans["phase.score"].events
    assert any(name == "ve_circular_rationality" for name, _attributes in events)
    assert not any(name == "ve_evidence_applied" for name, _attributes in events)


def test_ve_pct_accepts_overshoot() -> None:
    """The COMLab mirror accepts the emitter's thermal-shock overshoot range."""
    payload = OBDLiveDataPayload(
        engine_warmed=True,
        total_trim_correction_delta=0.0,
        normalized_obd_lambda=1.0,
        ve_pct=150.0,
        ve_validity=VEValidity.VALID,
        rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
        trim_analytics_gate=TrimAnalyticsGate.VALID,
        o2_failure_mode=O2FailureMode.NO_FAULT,
        maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
        map_status=NodeMAPStatus.REAL_SENSOR_FEED,
    )

    assert payload.ve_pct == 150.0
