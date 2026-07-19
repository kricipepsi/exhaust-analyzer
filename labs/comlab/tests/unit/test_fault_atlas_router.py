"""Unit tests for FaultAtlasRouter Stage B.

Covers T-P6-3 success criteria:
- _load_registry() loads + validates at boot
- evaluate_operator() handles all 7 operators
- _prune_candidates() filters by horizon, chemistry
- execute_triage_loop() 5-phase walk + confidence scoring
- apply_catalyst_damage_override() forces CRITICAL on P030x + flashing MIL
- route() end-to-end assembly
- Per-family fixtures route to correct fault_id
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import pytest

import comlab.core.fault_atlas_router as router_module
import comlab.core.lab_pipeline_aggregator as aggregator_module
from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import (
    FaultAtlasRouter,
    RegistryRow,
    _bank_asymmetry_verdict,
    _ecu_fault_verdict,
    _no_start_branch,
    _resolve_o2_sensor_fault,
    _resolve_pid,
)
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import (
    DTCLabPayload,
    FreezeFramePIDs,
    FreezeFrameRecord,
    GasLabPayload,
    Mode06MonitorResult,
    OBDLiveDataPayload,
    OrchestratorInboundRequest,
    SessionMetadata,
    UserInputEchoAudit,
)
from comlab.schemas.response import OrchestratorFinalUIOutput
from comlab.schemas.vocabulary import (
    DTCRoutingTag,
    EngineStateBucket,
    FuelSystemStatus,
    HistoricalFaultContext,
    Mode06MonitorState,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    SampleValidity,
    TrimAnalyticsGate,
    VEValidity,
    VinConfidence,
)


# ---------------------------------------------------------------------------
# Module-scoped fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def router(registry_path) -> FaultAtlasRouter:
    """Module-scoped — loaded once for all tests."""
    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    return FaultAtlasRouter(str(registry_path), kg, analytics, use_v2_registry=False)


@pytest.fixture(scope="module")
def kg() -> FaultAtlasKG:
    return FaultAtlasKG()


# ---------------------------------------------------------------------------
# Helpers — build test payloads
# ---------------------------------------------------------------------------


def _make_request(
    chemical_state: str = "NORMAL_OPERATION",
    gas_co: float = 0.1,
    gas_hc: int = 50,
    gas_o2: float = 0.3,
    lambda_chem: float = 1.0,
    horizon: str = "HORIZON_MODERN",
    cylinder_count: int = 4,
    confirmed_dtcs: list[str] | None = None,
    active_mil: bool = False,
    mil_flashing: bool = False,
    routing_tags: list[DTCRoutingTag] | None = None,
    short_term_ft1: float = 0.0,
    long_term_ft1: float = 0.0,
    manifold_pressure_kpa: float = 100.0,
    coolant_temp_c: float = 85.0,
    calculated_load_pct: float = 0.0,
    o2_voltage_b1s1: float | None = None,
    barometric_pressure_kpa: float | None = 101.3,
    obd_shrtft1: float | None = None,
    obd_longft1: float | None = None,
    obd_mass_airflow_gps: float | None = 0.0,
    obd_coolant_temp_c: float | None = None,
    obd_o2_voltage: float | None = None,
    obd_o2_downstream: float | None = None,
    per_bank_trim_delta: float | None = None,
    total_trim_correction_delta: float = 0.0,
    total_trim_correction_delta_b2: float | None = None,
    normalized_obd_lambda: float | None = 1.0,
    lambda_perception_delta: float | None = None,
) -> OrchestratorInboundRequest:
    """Build a minimal OrchestratorInboundRequest for router tests."""
    if obd_shrtft1 is None:
        obd_shrtft1 = short_term_ft1
    if obd_longft1 is None:
        obd_longft1 = long_term_ft1
    if obd_coolant_temp_c is None:
        obd_coolant_temp_c = coolant_temp_c

    return OrchestratorInboundRequest(
        metadata=SessionMetadata(
            session_id=uuid4(),
            vin_dna_string="1FA6P8CF0HXXXXXXX",
            resolved_horizon=horizon,
            cylinder_count=cylinder_count,
            vin_confidence=VinConfidence.HIGH,
        ),
        gas_lab_output=GasLabPayload(
            chemical_state=chemical_state,
            gas_co=gas_co,
            gas_hc=gas_hc,
            gas_co2=14.5,
            gas_o2=gas_o2,
            gas_nox=10,
            lambda_chem=lambda_chem,
            sample_validity=SampleValidity.VALID,
        ),
        obd_live_data=OBDLiveDataPayload(
            engine_warmed=True,
            total_trim_correction_delta=total_trim_correction_delta,
            total_trim_correction_delta_b2=total_trim_correction_delta_b2,
            lambda_perception_delta=lambda_perception_delta,
            per_bank_trim_delta=per_bank_trim_delta,
            normalized_obd_lambda=normalized_obd_lambda,
            ve_pct=72.0,
            ve_validity=VEValidity.VALID,
            rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
            trim_analytics_gate=TrimAnalyticsGate.VALID,
            o2_failure_mode=O2FailureMode.STUCK_LEAN,
            maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
            map_status=NodeMAPStatus.REAL_SENSOR_FEED,
            shrtft1=obd_shrtft1,
            longft1=obd_longft1,
            mass_airflow_gps=obd_mass_airflow_gps,
            coolant_temp_c=obd_coolant_temp_c,
            freeze_frame_pids=FreezeFramePIDs(
                calculated_engine_load_pct=0.0,
                freeze_frame_engine_rpm=0,
                o2_voltage=obd_o2_voltage,
                o2_downstream=obd_o2_downstream,
            ),
        ),
        dtc_lab_output=DTCLabPayload(
            active_mil=active_mil,
            mil_flashing=mil_flashing,
            confirmed_dtcs=confirmed_dtcs or [],
            pending_dtcs=[],
            permanent_dtcs=[],
            routing_tags=routing_tags or [],
            mode_06_monitors={},
            historical_fault_context=HistoricalFaultContext.UNKNOWN,
            freeze_frame=FreezeFrameRecord(
                calculated_load_pct=calculated_load_pct,
                engine_rpm=0,
                coolant_temp_c=coolant_temp_c,
                short_term_ft1=short_term_ft1,
                long_term_ft1=long_term_ft1,
                manifold_pressure_kpa=manifold_pressure_kpa,
                vehicle_speed_kmh=0,
                ignition_advance_deg=10.0,
                intake_air_temp_c=20.0,
                maf_gps=0.0,
                throttle_pos_pct=0.0,
                fuel_system_status=FuelSystemStatus.OL,
                o2_voltage_b1s1=o2_voltage_b1s1,
                barometric_pressure_kpa=barometric_pressure_kpa,
            ),
        ),
        symptom_dna={},
    )


def _sanitized(
    request: OrchestratorInboundRequest,
    *,
    era_lambda_tolerance: float | None = None,
) -> dict:
    """Wrap a request in a minimal sanitized payload dict."""
    sanitized: dict[str, Any] = {"request": request}
    if era_lambda_tolerance is not None:
        sanitized["era_lambda_tolerance"] = era_lambda_tolerance
    return sanitized


class _RecordingSpan:
    """Minimal recording span used to assert router evidence events."""

    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []
        self.attributes: dict[str, Any] = {}

    def __enter__(self) -> _RecordingSpan:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def is_recording(self) -> bool:
        return True

    def set_attribute(self, name: str, value: Any) -> None:
        self.attributes[name] = value

    def add_event(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        self.events.append((name, attributes or {}))


class _RecordingTracer:
    """Minimal tracer retaining spans by name."""

    def __init__(self) -> None:
        self.spans: dict[str, _RecordingSpan] = {}

    def start_as_current_span(self, name: str) -> AbstractContextManager[_RecordingSpan]:
        span = _RecordingSpan()
        self.spans[name] = span
        return span


def _bank_fuse_router(
    registry_path: Any,
    *,
    enable_bank_fuse: bool,
) -> FaultAtlasRouter:
    """Build a router with one global and one bank-localized controlled rule."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_bank_fuse=enable_bank_fuse,
    )
    router.registry = [
        RegistryRow.model_validate({
            "fault_id": "ERR-MW-003",
            "fault_name": "global_candidate",
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
                "base_weight": 0.79,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-LC-001",
            "fault_name": "bank_localized_candidate",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]
    return router


def _ecu_fuse_router(
    registry_path: Any,
    *,
    enable_ecu_fuse: bool,
) -> FaultAtlasRouter:
    """Build a router with one global and one ECU-fault controlled rule."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_ecu_fuse=enable_ecu_fuse,
    )
    router.registry = [
        RegistryRow.model_validate({
            "fault_id": "ERR-MW-003",
            "fault_name": "global_candidate",
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
                "base_weight": 0.79,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-EF-001",
            "fault_name": "ecu_fault_candidate",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]
    return router


def _o2_offset_router(
    registry_path: Any,
    *,
    enable_o2_offset: bool,
) -> FaultAtlasRouter:
    """Build a router with global and sensor-fault controlled rules."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_o2_offset=enable_o2_offset,
    )
    router.registry = [
        RegistryRow.model_validate({
            "fault_id": "ERR-MW-003",
            "fault_name": "global_candidate",
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
                "base_weight": 0.79,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-SF-001",
            "fault_name": "wideband_offset_candidate",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]
    return router


# ===================================================================
# _load_registry — §4.2 step 1
# ===================================================================


def test_load_registry_populates_rules(router: FaultAtlasRouter) -> None:
    """Registry loads at least the 3 starter rules + catalyst batches."""
    assert len(router.registry) >= 3


def test_registry_rules_are_parsed(router: FaultAtlasRouter) -> None:
    """Every loaded rule is a RegistryRow with required fields."""
    for row in router.registry:
        assert isinstance(row, RegistryRow)
        assert row.fault_id.startswith("ERR-")
        assert len(row.target_horizons) >= 1
        assert row.cross_domain_matrix.gas_lab_state


def test_registry_remediation_map_loaded(router: FaultAtlasRouter) -> None:
    """Remediation map is loaded from registry JSON."""
    assert len(router._remediation_map) >= 3


def test_generate_remediation_returns_string(router: FaultAtlasRouter) -> None:
    """Known fault_name returns a remediation string."""
    result = router.generate_remediation("stuck_open_egr_valve")
    assert "EGR" in result


def test_generate_remediation_unknown_returns_empty(router: FaultAtlasRouter) -> None:
    """Unknown fault_name returns empty string."""
    result = router.generate_remediation("nonexistent_fault")
    assert result == ""


# ===================================================================
# evaluate_operator — §4.2 step 6
# ===================================================================


class TestOperatorEvaluator:
    """All 7 operators from LLD §6.4."""

    def test_equals_match(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("EQUALS", 5.0, 5.0)

    def test_equals_mismatch(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("EQUALS", 5.0, 3.0)

    def test_in_range_inside(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("IN_RANGE", 35.0, [30.0, 50.0])

    def test_in_range_below(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("IN_RANGE", 20.0, [30.0, 50.0])

    def test_in_range_above(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("IN_RANGE", 60.0, [30.0, 50.0])

    def test_in_range_boundary(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("IN_RANGE", 30.0, [30.0, 50.0])
        assert FaultAtlasRouter.evaluate_operator("IN_RANGE", 50.0, [30.0, 50.0])

    def test_greater_than_true(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("GREATER_THAN", 20.0, 15.0)

    def test_greater_than_false(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("GREATER_THAN", 10.0, 15.0)

    def test_greater_than_equal_is_false(self) -> None:
        """GREATER_THAN is strict — equality does NOT pass."""
        assert not FaultAtlasRouter.evaluate_operator("GREATER_THAN", 15.0, 15.0)

    def test_less_than_true(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("LESS_THAN", 50.0, 75.0)

    def test_less_than_false(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("LESS_THAN", 100.0, 75.0)

    def test_less_than_or_equal_match(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("LESS_THAN_OR_EQUAL", -23.0, -23.0)

    def test_less_than_or_equal_below(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("LESS_THAN_OR_EQUAL", -30.0, -23.0)

    def test_less_than_or_equal_above(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("LESS_THAN_OR_EQUAL", -10.0, -23.0)

    def test_greater_than_or_equal_match(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("GREATER_THAN_OR_EQUAL", 10.0, 10.0)

    def test_greater_than_or_equal_above(self) -> None:
        assert FaultAtlasRouter.evaluate_operator("GREATER_THAN_OR_EQUAL", 15.0, 10.0)

    def test_greater_than_or_equal_below(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("GREATER_THAN_OR_EQUAL", 5.0, 10.0)

    def test_deviates_from_target_scalar(self) -> None:
        """DEVIATES_FROM_TARGET with scalar value uses 10% tolerance."""
        assert FaultAtlasRouter.evaluate_operator(
            "DEVIATES_FROM_TARGET", 15.0, 10.0
        )  # 15.0 deviates > 1.0 from target 10.0

    def test_deviates_from_target_within_tolerance(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator(
            "DEVIATES_FROM_TARGET", 10.5, 10.0
        )  # 10.5 within 1.0 of target 10.0

    def test_deviates_from_target_explicit_tolerance(self) -> None:
        """DEVIATES_FROM_TARGET with [target, tolerance] tuple."""
        assert FaultAtlasRouter.evaluate_operator(
            "DEVIATES_FROM_TARGET", 25.0, [20.0, 3.0]
        )
        assert not FaultAtlasRouter.evaluate_operator(
            "DEVIATES_FROM_TARGET", 22.0, [20.0, 3.0]
        )

    def test_none_runtime_value_returns_false(self) -> None:
        """Missing PID → cannot satisfy constraint."""
        assert not FaultAtlasRouter.evaluate_operator("GREATER_THAN", None, 10.0)

    def test_unknown_operator_returns_false(self) -> None:
        assert not FaultAtlasRouter.evaluate_operator("BOGUS_OP", 5.0, 5.0)

    def test_list_runtime_value_returns_false(self) -> None:
        """Non-scalar runtime values cannot be compared."""
        assert not FaultAtlasRouter.evaluate_operator("GREATER_THAN", [1.0, 2.0], 5.0)


# ===================================================================
# _prune_candidates — §4.2 steps 2+3
# ===================================================================


def test_prune_removes_wrong_horizon(router: FaultAtlasRouter) -> None:
    """Rows not targeting the given horizon are dropped."""
    # ERR-E1-M032 only targets HORIZON_LEGACY
    survivors = router._prune_candidates(
        router.registry,
        horizon="HORIZON_MODERN",
        chemical_state="INCOMPLETE_OXIDATION",
        routing_tags=[],
    )
    ids = {r.fault_id for r in survivors}
    assert "ERR-E1-M032" not in ids  # legacy-only rule


def test_prune_keeps_matching_horizon(router: FaultAtlasRouter) -> None:
    """Rows targeting the given horizon are kept."""
    survivors = router._prune_candidates(
        router.registry,
        horizon="HORIZON_LEGACY",
        chemical_state="INCOMPLETE_OXIDATION",
        routing_tags=[],
    )
    ids = {r.fault_id for r in survivors}
    assert "ERR-E1-M032" in ids  # legacy rule


def test_prune_removes_wrong_chemistry(router: FaultAtlasRouter) -> None:
    """Rows with non-matching gas_lab_state are dropped."""
    survivors = router._prune_candidates(
        router.registry,
        horizon="HORIZON_MODERN",
        chemical_state="NORMAL_OPERATION",
        routing_tags=[],
    )
    ids = {r.fault_id for r in survivors}
    # EGR rule requires INCOMPLETE_OXIDATION
    assert "ERR-E1-M032" not in ids


# ===================================================================
# execute_triage_loop — §4.2 step 5
# ===================================================================


def test_triage_loop_egr_valve_legacy(router: FaultAtlasRouter) -> None:
    """ERR-E1-M032 routes correctly with EGR chemistry + DTC on legacy horizon."""
    req = _make_request(
        chemical_state="INCOMPLETE_OXIDATION",
        horizon="HORIZON_LEGACY",
        confirmed_dtcs=["P0401"],
        active_mil=False,
        manifold_pressure_kpa=65.0,  # vacuum = 101.3 - 65.0 = 36.3 kPa → in [30, 50]
        barometric_pressure_kpa=101.3,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-E1-M032"


def test_triage_loop_hpfp_seal_leak_modern(router: FaultAtlasRouter) -> None:
    """T-FX-PURGE-2: MODERN-only ERR-E3-F501 stripped — no winner expected."""
    req = _make_request(
        chemical_state="GDI_HPFP_INTERNAL_SEAL_LEAK",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0172"],
        active_mil=True,
        long_term_ft1=-25.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is None


def test_triage_loop_coil_arc_misfire(router: FaultAtlasRouter) -> None:
    """ERR-E2-I104 routes with IGNITION_MISFIRE + high SHRTFT + P030x."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0302"],
        active_mil=True,
        short_term_ft1=18.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-E2-I104"


def test_triage_loop_catalyst_masking_rich(router: FaultAtlasRouter) -> None:
    """ERR-CF-005 (catalyst_masking_rich_engine) routes with NORMAL_OPERATION
    chemistry + strongly negative LTFT (GAS_ONLY strategy — no DTC required)."""
    req = _make_request(
        chemical_state="NORMAL_OPERATION",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        long_term_ft1=-15.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-CF-005"
    # GAS_ONLY strategy — no DTC bonus
    assert verdict["winner_score"] == 0.75


def test_triage_loop_no_match_returns_none_winner(router: FaultAtlasRouter) -> None:
    """When no rule fires, winner is None (OPTIMAL_HEALTH path)."""
    req = _make_request(
        chemical_state="STOICHIOMETRIC_BURN",  # not in any registry rule
        horizon="HORIZON_MODERN",
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is None
    assert verdict["winner_score"] == 0.0
    assert verdict["runner_ups"] == []


def test_triage_loop_poa_signature_injects_tag(router: FaultAtlasRouter) -> None:
    """POA_SIGNATURE chemical_state injects POA_HISTORY routing tag."""
    req = _make_request(
        chemical_state="POA_SIGNATURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0420"],
        active_mil=True,
        long_term_ft1=-5.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-CF-006"


def test_triage_loop_dtc_require_match_blocks_when_no_match(
    router: FaultAtlasRouter,
) -> None:
    """REQUIRE_MATCH strategy: rule must NOT fire when DTCs don't match."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0401"],  # EGR code, not P030x
        active_mil=True,
        short_term_ft1=18.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    # ERR-E2-I104 requires P0300-P0304 — P0401 should not pass
    if verdict["winner"] is not None:
        assert verdict["winner"].fault_id != "ERR-E2-I104"


def test_triage_loop_exhaust_leak_with_positive_ltft(
    router: FaultAtlasRouter,
) -> None:
    """ERR-EL-001 routes with EXHAUST_AIR_LEAK + positive LTFT >= 10."""
    req = _make_request(
        chemical_state="EXHAUST_AIR_LEAK",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0171"],
        active_mil=False,
        long_term_ft1=12.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-EL-001"


def test_triage_loop_runner_ups_populated(router: FaultAtlasRouter) -> None:
    """When multiple candidates pass, runner-ups are returned."""
    req = _make_request(
        chemical_state="CATALYST_OVERWHELMED",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0420"],
        active_mil=True,
        o2_voltage_b1s1=0.7,  # > 0.6 triggers ERR-CF-001
        calculated_load_pct=65.0,  # > 60 triggers ERR-CF-002
        long_term_ft1=0.0,
        manifold_pressure_kpa=80.0,  # > 75 triggers ERR-CF-003
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    # Should have runner-ups since multiple catalyst rules match
    assert len(verdict["runner_ups"]) >= 1


def test_bank_fuse_inert_when_off(registry_path: Any) -> None:
    """Flag-off, absent-field, and symmetric bank inputs are byte-identical."""
    baseline_request = _make_request()
    baseline_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    asymmetric_request = baseline_request.model_copy(deep=True)
    assert asymmetric_request.obd_live_data is not None
    asymmetric_request.obd_live_data.per_bank_trim_delta = 12.0
    symmetric_request = baseline_request.model_copy(deep=True)
    assert symmetric_request.obd_live_data is not None
    symmetric_request.obd_live_data.per_bank_trim_delta = 3.0

    disabled = _bank_fuse_router(registry_path, enable_bank_fuse=False)
    enabled = _bank_fuse_router(registry_path, enable_bank_fuse=True)

    baseline = disabled.route(_sanitized(baseline_request))
    flag_off = disabled.route(_sanitized(asymmetric_request))
    field_absent = enabled.route(_sanitized(baseline_request))
    symmetric = enabled.route(_sanitized(symmetric_request))

    assert flag_off == baseline
    assert field_absent == baseline
    assert symmetric == baseline


def test_bank_fuse_asymmetric_biases_family(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Asymmetric bank evidence promotes a bank-localized runner-up and emits a span."""
    request = _make_request(per_bank_trim_delta=12.0)
    disabled = _bank_fuse_router(registry_path, enable_bank_fuse=False)
    enabled = _bank_fuse_router(registry_path, enable_bank_fuse=True)

    baseline = disabled.execute_triage_loop(_sanitized(request))
    assert baseline["winner"] is not None
    assert baseline["winner"].fault_id == "ERR-MW-003"

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    promoted = enabled.execute_triage_loop(_sanitized(request))

    assert promoted["winner"] is not None
    assert promoted["winner"].fault_id == "ERR-LC-001"
    assert promoted["winner_score"] == 0.80
    score_events = tracer.spans["phase.score"].events
    assert any(name == "bank_asymmetry_applied" for name, _attrs in score_events)

    symmetric_request = request.model_copy(deep=True)
    assert symmetric_request.obd_live_data is not None
    symmetric_request.obd_live_data.per_bank_trim_delta = 3.0
    symmetric = enabled.execute_triage_loop(_sanitized(symmetric_request))
    assert symmetric["winner"] is not None
    assert symmetric["winner"].fault_id == "ERR-MW-003"
    assert not any(
        name == "bank_asymmetry_applied"
        for name, _attrs in tracer.spans["phase.score"].events
    )


def test_bank_fuse_legacy_caps_confidence(registry_path: Any) -> None:
    """LEGACY bank evidence is capped below ADAPTIVE/MODERN evidence."""
    legacy = _bank_asymmetry_verdict(12.0, "HORIZON_LEGACY")
    adaptive = _bank_asymmetry_verdict(12.0, "HORIZON_ADAPTIVE")
    modern = _bank_asymmetry_verdict(12.0, "HORIZON_MODERN")
    assert legacy.state == adaptive.state == modern.state == "ASYMMETRIC"
    assert legacy.confidence == 0.50
    assert adaptive.confidence == modern.confidence == 0.80

    enabled = _bank_fuse_router(registry_path, enable_bank_fuse=True)
    legacy_request = _make_request(
        horizon="HORIZON_LEGACY",
        per_bank_trim_delta=12.0,
    )
    modern_request = _make_request(
        horizon="HORIZON_MODERN",
        per_bank_trim_delta=12.0,
    )
    legacy_result = enabled.execute_triage_loop(_sanitized(legacy_request))
    modern_result = enabled.execute_triage_loop(_sanitized(modern_request))

    assert legacy_result["winner"] is not None
    assert legacy_result["winner"].fault_id == "ERR-MW-003"
    assert modern_result["winner"] is not None
    assert modern_result["winner"].fault_id == "ERR-LC-001"


def test_ecu_fuse_inert_when_off(registry_path: Any) -> None:
    """Flag-off and every falsy ECU-fuse guard preserve baseline output."""
    fuse_request = _make_request(
        total_trim_correction_delta=30.0,
        total_trim_correction_delta_b2=30.0,
        normalized_obd_lambda=1.10,
        lambda_perception_delta=0.08,
    )
    fuse_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    fields_absent = fuse_request.model_copy(deep=True)
    assert fields_absent.obd_live_data is not None
    fields_absent.obd_live_data.total_trim_correction_delta_b2 = None
    fields_absent.obd_live_data.lambda_perception_delta = None

    disabled = _ecu_fuse_router(registry_path, enable_ecu_fuse=False)
    enabled = _ecu_fuse_router(registry_path, enable_ecu_fuse=True)
    baseline = disabled.route(
        _sanitized(fields_absent, era_lambda_tolerance=0.02)
    )
    flag_off = disabled.route(
        _sanitized(fuse_request, era_lambda_tolerance=0.02)
    )
    missing_emitter_delta = fuse_request.model_copy(deep=True)
    assert missing_emitter_delta.obd_live_data is not None
    missing_emitter_delta.obd_live_data.lambda_perception_delta = None
    missing_bank_two = fuse_request.model_copy(deep=True)
    assert missing_bank_two.obd_live_data is not None
    missing_bank_two.obd_live_data.total_trim_correction_delta_b2 = None
    missing_obd_lambda = fuse_request.model_copy(deep=True)
    assert missing_obd_lambda.obd_live_data is not None
    missing_obd_lambda.obd_live_data.normalized_obd_lambda = None
    trim_not_railed = fuse_request.model_copy(deep=True)
    assert trim_not_railed.obd_live_data is not None
    trim_not_railed.obd_live_data.total_trim_correction_delta = 20.0
    trim_not_railed.obd_live_data.total_trim_correction_delta_b2 = 20.0

    assert flag_off == baseline
    assert enabled.route(
        _sanitized(missing_emitter_delta, era_lambda_tolerance=0.02)
    ) == disabled.route(
        _sanitized(missing_emitter_delta, era_lambda_tolerance=0.02)
    )
    assert enabled.route(
        _sanitized(missing_bank_two, era_lambda_tolerance=0.02)
    ) == disabled.route(
        _sanitized(missing_bank_two, era_lambda_tolerance=0.02)
    )
    assert enabled.route(
        _sanitized(missing_obd_lambda, era_lambda_tolerance=0.02)
    ) == disabled.route(
        _sanitized(missing_obd_lambda, era_lambda_tolerance=0.02)
    )
    assert enabled.route(_sanitized(fuse_request)) == disabled.route(
        _sanitized(fuse_request)
    )
    assert enabled.route(
        _sanitized(trim_not_railed, era_lambda_tolerance=0.02)
    ) == disabled.route(
        _sanitized(trim_not_railed, era_lambda_tolerance=0.02)
    )


def test_ecu_fuse_promotes_ecu_fault(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Railed symmetric trim plus divergent lambda promotes ECU-fault evidence."""
    request = _make_request(
        total_trim_correction_delta=30.0,
        total_trim_correction_delta_b2=30.0,
        normalized_obd_lambda=1.10,
        lambda_perception_delta=0.08,
    )
    disabled = _ecu_fuse_router(registry_path, enable_ecu_fuse=False)
    enabled = _ecu_fuse_router(registry_path, enable_ecu_fuse=True)

    baseline = disabled.execute_triage_loop(
        _sanitized(request, era_lambda_tolerance=0.02)
    )
    assert baseline["winner"] is not None
    assert baseline["winner"].fault_id == "ERR-MW-003"

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    promoted = enabled.execute_triage_loop(
        _sanitized(request, era_lambda_tolerance=0.02)
    )

    assert promoted["winner"] is not None
    assert promoted["winner"].fault_id == "ERR-EF-001"
    assert promoted["winner_score"] == 0.80
    events = tracer.spans["phase.score"].events
    assert any(name == "ecu_fault_fused" for name, _attrs in events)


def test_ecu_fuse_rejects_real_lean(registry_path: Any) -> None:
    """Perception agreement leaves a real lean/rich candidate untouched."""
    request = _make_request(
        total_trim_correction_delta=30.0,
        total_trim_correction_delta_b2=30.0,
        normalized_obd_lambda=1.01,
        lambda_perception_delta=0.01,
    )
    verdict = _ecu_fault_verdict(1.01, 1.0, 0.02, 30.0, 30.0)
    assert verdict.state == "NO_FAULT"

    enabled = _ecu_fuse_router(registry_path, enable_ecu_fuse=True)
    result = enabled.execute_triage_loop(
        _sanitized(request, era_lambda_tolerance=0.02)
    )
    assert result["winner"] is not None
    assert result["winner"].fault_id == "ERR-MW-003"


def test_ecu_fuse_rejects_asymmetric(registry_path: Any) -> None:
    """Railed but bank-asymmetric trim remains BANK-FUSE territory."""
    request = _make_request(
        total_trim_correction_delta=30.0,
        total_trim_correction_delta_b2=-5.0,
        normalized_obd_lambda=1.10,
        lambda_perception_delta=0.08,
    )
    verdict = _ecu_fault_verdict(1.10, 1.0, 0.02, 30.0, -5.0)
    assert verdict.state == "NO_FAULT"

    enabled = _ecu_fuse_router(registry_path, enable_ecu_fuse=True)
    result = enabled.execute_triage_loop(
        _sanitized(request, era_lambda_tolerance=0.02)
    )
    assert result["winner"] is not None
    assert result["winner"].fault_id == "ERR-MW-003"


def test_o2_offset_inert_when_off(registry_path: Any) -> None:
    """Flag-off, absent OBD, and unavailable helper inputs preserve baseline."""
    baseline = _make_request(lambda_chem=1.0)
    baseline.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    candidate = baseline.model_copy(deep=True)
    assert candidate.obd_live_data is not None
    candidate.obd_live_data.o2_failure_mode = (
        O2FailureMode.WIDEBAND_OFFSET_CANDIDATE
    )
    without_obd = candidate.model_copy(
        update={"obd_live_data": None},
        deep=True,
    )
    disabled = _o2_offset_router(registry_path, enable_o2_offset=False)
    enabled = _o2_offset_router(registry_path, enable_o2_offset=True)

    assert disabled.route(_sanitized(candidate)) == disabled.route(
        _sanitized(baseline)
    )
    assert enabled.route(_sanitized(without_obd)) == disabled.route(
        _sanitized(without_obd)
    )
    assert _resolve_o2_sensor_fault(None, 1.0) == "UNAVAILABLE"
    assert (
        _resolve_o2_sensor_fault(
            O2FailureMode.WIDEBAND_OFFSET_CANDIDATE,
            None,
        )
        == "UNAVAILABLE"
    )


def test_o2_offset_promotes_sensor_fault(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Candidate plus stoichiometric gas truth promotes sensor-fault evidence."""
    request = _make_request(lambda_chem=1.0)
    assert request.obd_live_data is not None
    request.obd_live_data.o2_failure_mode = (
        O2FailureMode.WIDEBAND_OFFSET_CANDIDATE
    )
    disabled = _o2_offset_router(registry_path, enable_o2_offset=False)
    enabled = _o2_offset_router(registry_path, enable_o2_offset=True)

    baseline = disabled.execute_triage_loop(_sanitized(request))
    assert baseline["winner"] is not None
    assert baseline["winner"].fault_id == "ERR-MW-003"

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    promoted = enabled.execute_triage_loop(_sanitized(request))

    assert promoted["winner"] is not None
    assert promoted["winner"].fault_id == "ERR-SF-001"
    assert promoted["winner_score"] == 0.80
    events = tracer.spans["phase.score"].events
    assert any(name == "o2_offset_confirmed" for name, _attrs in events)


def test_o2_offset_rejects_real_lean(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Candidate plus genuinely lean gas remains inert."""
    request = _make_request(lambda_chem=1.20)
    assert request.obd_live_data is not None
    request.obd_live_data.o2_failure_mode = (
        O2FailureMode.WIDEBAND_OFFSET_CANDIDATE
    )
    enabled = _o2_offset_router(registry_path, enable_o2_offset=True)
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    assert (
        _resolve_o2_sensor_fault(
            O2FailureMode.WIDEBAND_OFFSET_CANDIDATE,
            1.20,
        )
        == "NO_FAULT"
    )
    result = enabled.execute_triage_loop(_sanitized(request))
    assert result["winner"] is not None
    assert result["winner"].fault_id == "ERR-MW-003"
    assert not any(
        name == "o2_offset_confirmed"
        for name, _attrs in tracer.spans["phase.score"].events
    )


@pytest.mark.parametrize(
    "mode",
    [O2FailureMode.NO_FAULT, O2FailureMode.STUCK_LEAN],
)
def test_o2_offset_non_candidate_inert(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
    mode: O2FailureMode,
) -> None:
    """Non-candidate O2 modes remain byte-identical with the flag enabled."""
    request = _make_request(lambda_chem=1.0)
    assert request.obd_live_data is not None
    request.obd_live_data.o2_failure_mode = mode
    request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    disabled = _o2_offset_router(registry_path, enable_o2_offset=False)
    enabled = _o2_offset_router(registry_path, enable_o2_offset=True)
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    assert enabled.route(_sanitized(request)) == disabled.route(
        _sanitized(request)
    )
    enabled.execute_triage_loop(_sanitized(request))
    assert not any(
        name == "o2_offset_confirmed"
        for name, _attrs in tracer.spans["phase.score"].events
    )


def test_perception_axis_still_live(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The standard route still invokes the unchanged perception detector."""
    request = _make_request(
        normalized_obd_lambda=1.10,
        lambda_perception_delta=0.08,
    )
    baseline = LabPipelineAggregator(use_v2_registry=False).process(request)
    original_detect = aggregator_module.detect_perception_contradiction
    observed_results: list[Any] = []

    def recording_detect(*args: Any, **kwargs: Any) -> Any:
        result = original_detect(*args, **kwargs)
        observed_results.append(result)
        return result

    monkeypatch.setattr(
        aggregator_module,
        "detect_perception_contradiction",
        recording_detect,
    )
    observed = LabPipelineAggregator(use_v2_registry=False).process(request)

    assert len(observed_results) == 1
    assert (
        observed_results[0].bias_verdict.value
        == baseline.performance_analytics.o2_sensor_bias_verdict
    )
    assert observed.model_dump(
        exclude={"user_input_echo_audit"}
    ) == baseline.model_dump(exclude={"user_input_echo_audit"})


# ===================================================================
# apply_catalyst_damage_override — §4.2 step 7
# ===================================================================


def test_catalyst_override_triggers_on_p030x_flashing(
    router: FaultAtlasRouter,
) -> None:
    """mil_flashing + P030x → CRITICAL_IMMEDIATE_STOP."""
    from comlab.schemas.response import PerformanceAnalytics

    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0302"],
        active_mil=True,
        mil_flashing=True,
    )
    analytics = PerformanceAnalytics(
        kinetic_power_loss_pct=15.0,
        catalyst_efficiency_index_pct=90.0,
        lambda_perception_delta=0.0,
        o2_sensor_bias_verdict=None,
        severity_level="WARNING_DEGRADED_PERFORMANCE",
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    result = router.apply_catalyst_damage_override(verdict, req, analytics)
    assert result.severity_level == "CRITICAL_IMMEDIATE_STOP"


def test_catalyst_override_no_trigger_without_flashing(
    router: FaultAtlasRouter,
) -> None:
    """P030x without mil_flashing does NOT trigger override."""
    from comlab.schemas.response import PerformanceAnalytics

    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0302"],
        active_mil=True,
        mil_flashing=False,
    )
    analytics = PerformanceAnalytics(
        kinetic_power_loss_pct=15.0,
        catalyst_efficiency_index_pct=90.0,
        lambda_perception_delta=0.0,
        o2_sensor_bias_verdict=None,
        severity_level="WARNING_DEGRADED_PERFORMANCE",
    )
    result = router.apply_catalyst_damage_override(
        router.execute_triage_loop(_sanitized(req)), req, analytics
    )
    assert result.severity_level == "WARNING_DEGRADED_PERFORMANCE"


def test_catalyst_override_no_trigger_without_p030x(
    router: FaultAtlasRouter,
) -> None:
    """mil_flashing without P030x does NOT trigger override."""
    from comlab.schemas.response import PerformanceAnalytics

    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0420"],  # catalyst DTC, not misfire
        active_mil=True,
        mil_flashing=True,
    )
    analytics = PerformanceAnalytics(
        kinetic_power_loss_pct=15.0,
        catalyst_efficiency_index_pct=90.0,
        lambda_perception_delta=0.0,
        o2_sensor_bias_verdict=None,
        severity_level="WARNING_DEGRADED_PERFORMANCE",
    )
    result = router.apply_catalyst_damage_override(
        router.execute_triage_loop(_sanitized(req)), req, analytics
    )
    assert result.severity_level == "WARNING_DEGRADED_PERFORMANCE"


# ===================================================================
# route() — end-to-end assembly
# ===================================================================


def test_route_returns_orchestrator_output(router: FaultAtlasRouter) -> None:
    """route() returns a valid OrchestratorFinalUIOutput."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0302"],
        active_mil=True,
        short_term_ft1=18.0,
    )
    result = router.route(_sanitized(req))
    assert isinstance(result, OrchestratorFinalUIOutput)
    assert result.diagnostic_verdict.is_fault_detected
    assert result.diagnostic_verdict.fault_code == "ERR-E2-I104"


def test_route_optimal_health_path(router: FaultAtlasRouter) -> None:
    """When no rule fires, route() returns OPTIMAL_HEALTH."""
    req = _make_request(
        chemical_state="STOICHIOMETRIC_BURN",
        horizon="HORIZON_MODERN",
    )
    result = router.route(_sanitized(req))
    assert isinstance(result, OrchestratorFinalUIOutput)
    assert not result.diagnostic_verdict.is_fault_detected
    assert result.diagnostic_verdict.fault_code == "OPTIMAL_HEALTH"


def test_route_populates_performance_analytics(router: FaultAtlasRouter) -> None:
    """route() includes Stage D analytics in the output."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0302"],
        active_mil=True,
        short_term_ft1=18.0,
    )
    result = router.route(_sanitized(req))
    assert result.performance_analytics.kinetic_power_loss_pct >= 0.0


def test_route_populates_fault_enrichment(router: FaultAtlasRouter) -> None:
    """route() includes KG enrichment for the winning fault."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0302"],
        active_mil=True,
        short_term_ft1=18.0,
    )
    result = router.route(_sanitized(req))
    assert result.fault_enrichment.component_group
    assert len(result.fault_enrichment.ui_remediation_steps) >= 1


# ===================================================================
# _merge_differential_siblings
# ===================================================================


def test_merge_siblings_caps_at_five(router: FaultAtlasRouter) -> None:
    """Max 5 siblings regardless of input sizes."""
    from comlab.core.fault_atlas_router import RegistryRow as RR

    # 6 runtime runner-ups
    runtime = [
        (RR(fault_id=f"ERR-XX-00{i}", fault_name=f"fault_{i}",
            target_horizons=["HORIZON_MODERN"], preconditions={},
            cross_domain_matrix={"gas_lab_state": "NORMAL_OPERATION", "obd_live_pids": {}, "dtc_lab_status": {"active_mil": False, "p_code_match": [], "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY"}},  # type: ignore[arg-type]
            confidence_scoring={"base_weight": 0.5, "bonus_on_dtc_match": 0.0}),  # type: ignore[arg-type]
         0.5) for i in range(6)
    ]
    editor = ["ERR-YY-001", "ERR-YY-002"]
    result = router._merge_differential_siblings(runtime, editor)
    assert len(result) == 5


def test_merge_siblings_runtime_first(router: FaultAtlasRouter) -> None:
    """Runtime entries come before editor-curated ones."""
    from comlab.core.fault_atlas_router import RegistryRow as RR

    runtime = [
        (RR(fault_id="ERR-RT-001", fault_name="runtime_fault",
            target_horizons=["HORIZON_MODERN"], preconditions={},
            cross_domain_matrix={"gas_lab_state": "NORMAL_OPERATION", "obd_live_pids": {}, "dtc_lab_status": {"active_mil": False, "p_code_match": [], "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY"}},  # type: ignore[arg-type]
            confidence_scoring={"base_weight": 0.5, "bonus_on_dtc_match": 0.0}),  # type: ignore[arg-type]
         0.8)
    ]
    editor = ["ERR-ED-001"]
    result = router._merge_differential_siblings(runtime, editor)
    assert result[0].fault_id == "ERR-RT-001"
    assert result[0].source == "runtime"


def test_merge_siblings_deduplicates(router: FaultAtlasRouter) -> None:
    """Same fault_id in both runtime and editor → runtime wins, no duplicate."""
    from comlab.core.fault_atlas_router import RegistryRow as RR

    runtime = [
        (RR(fault_id="ERR-SHARED", fault_name="shared",
            target_horizons=["HORIZON_MODERN"], preconditions={},
            cross_domain_matrix={"gas_lab_state": "NORMAL_OPERATION", "obd_live_pids": {}, "dtc_lab_status": {"active_mil": False, "p_code_match": [], "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY"}},  # type: ignore[arg-type]
            confidence_scoring={"base_weight": 0.5, "bonus_on_dtc_match": 0.0}),  # type: ignore[arg-type]
         0.9)
    ]
    editor = ["ERR-SHARED", "ERR-OTHER"]
    result = router._merge_differential_siblings(runtime, editor)
    ids = [s.fault_id for s in result]
    assert ids.count("ERR-SHARED") == 1


# ===================================================================
# _resolve_pid
# ===================================================================


def test_obd_live_data_payload_mirrors_named_obd_evidence() -> None:
    """OBDLiveDataPayload carries the SF/EF evidence fields COMLab consumes."""
    payload = OBDLiveDataPayload(
        engine_warmed=True,
        total_trim_correction_delta=30.0,
        normalized_obd_lambda=1.0,
        ve_pct=72.0,
        ve_validity=VEValidity.VALID,
        rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
        trim_analytics_gate=TrimAnalyticsGate.VALID,
        o2_failure_mode=O2FailureMode.STUCK_LEAN,
        maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
        map_status=NodeMAPStatus.REAL_SENSOR_FEED,
        shrtft1=20.0,
        longft1=10.0,
        mass_airflow_gps=3.6,
        manifold_vacuum_kpa=28.0,
        coolant_temp_c=59.0,
        freeze_frame_pids=FreezeFramePIDs(
            calculated_engine_load_pct=0.0,
            freeze_frame_engine_rpm=0,
            o2_voltage=0.08,
            o2_downstream=0.72,
        ),
    )

    assert payload.shrtft1 == 20.0
    assert payload.longft1 == 10.0
    assert payload.mass_airflow_gps == 3.6
    assert payload.manifold_vacuum_kpa == 28.0
    assert payload.coolant_temp_c == 59.0
    assert payload.freeze_frame_pids is not None
    assert payload.freeze_frame_pids.o2_voltage == 0.08
    assert payload.freeze_frame_pids.o2_downstream == 0.72


def test_obd_live_trim_payload_rejects_obd_rail_overflow() -> None:
    """Individual OBD fuel trims are bounded to OBDLab's +/-127 rail."""
    with pytest.raises(ValueError):
        OBDLiveDataPayload(
            engine_warmed=True,
            total_trim_correction_delta=128.0,
            normalized_obd_lambda=1.0,
            ve_pct=72.0,
            ve_validity=VEValidity.VALID,
            rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
            trim_analytics_gate=TrimAnalyticsGate.VALID,
            o2_failure_mode=O2FailureMode.STUCK_LEAN,
            maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
            map_status=NodeMAPStatus.REAL_SENSOR_FEED,
            shrtft1=128.0,
            longft1=0.0,
            mass_airflow_gps=3.6,
            coolant_temp_c=59.0,
        )


def test_resolve_pid_known(router: FaultAtlasRouter) -> None:
    """OBD-owned PID names resolve from OBDLiveDataPayload mirror fields."""
    req = _make_request(
        long_term_ft1=-25.0,
        coolant_temp_c=10.0,
        obd_longft1=-12.0,
        obd_mass_airflow_gps=4.2,
        obd_coolant_temp_c=61.0,
    )
    val = _resolve_pid(req, "longft1")
    assert val == -12.0
    assert _resolve_pid(req, "maf_gps") == 4.2
    assert _resolve_pid(req, "ect_c") == 61.0


def test_resolve_o2_pids_from_obd_freeze_frame_pids(
    router: FaultAtlasRouter,
) -> None:
    """Option A: SF O2 evidence comes from ferried OBD freeze_frame_pids."""
    req = _make_request(
        o2_voltage_b1s1=None,
        obd_o2_voltage=0.08,
        obd_o2_downstream=0.72,
    )

    assert _resolve_pid(req, "o2_voltage") == 0.08
    assert _resolve_pid(req, "o2_downstream") == 0.72
    assert _resolve_pid(req, "o2_b1s2_v") == 0.72


def test_resolve_pid_falls_back_to_dtc_freeze_frame_when_obd_mirror_missing(
    router: FaultAtlasRouter,
) -> None:
    """Pre-Wired fixtures keep working until OBDLiveDataPayload is forwarded."""
    req = _make_request(long_term_ft1=-25.0, coolant_temp_c=10.0)
    assert req.obd_live_data is not None
    req.obd_live_data.longft1 = None
    req.obd_live_data.coolant_temp_c = None

    assert _resolve_pid(req, "longft1") == -25.0
    assert _resolve_pid(req, "ect_c") == 10.0


def test_resolve_pid_manifold_vacuum(router: FaultAtlasRouter) -> None:
    """manifold_vacuum_kpa = barometric - manifold pressure."""
    req = _make_request(
        manifold_pressure_kpa=40.0,
        barometric_pressure_kpa=101.3,
    )
    val = _resolve_pid(req, "manifold_vacuum_kpa")
    assert val == pytest.approx(61.3)


def test_resolve_pid_none_when_missing(router: FaultAtlasRouter) -> None:
    """Missing PID returns None."""
    req = _make_request(o2_voltage_b1s1=None)
    val = _resolve_pid(req, "o2_b1s2_v")
    assert val is None


def test_resolve_pid_unknown_returns_none(router: FaultAtlasRouter) -> None:
    """Unknown PID name returns None."""
    req = _make_request()
    val = _resolve_pid(req, "nonexistent_pid")
    assert val is None


# ===================================================================
# build_differential_siblings — already implemented, keep regression
# ===================================================================


def test_build_differential_siblings_from_kg_node(router: FaultAtlasRouter, kg: FaultAtlasKG) -> None:
    """Existing method still works with KG nodes."""
    node = kg.resolve("ERR-RM-001")
    result = router.build_differential_siblings(node)
    assert len(result) <= 5
    for sib in result:
        assert sib.source == "editor_curated"
        assert sib.fault_family
        assert sib.confidence_score is None


# ===================================================================
# Per-family fixture routing — success criterion
# ===================================================================


def test_catalyst_failure_family_routes(router: FaultAtlasRouter) -> None:
    """A catalyst_failure scenario routes to a catalyst rule."""
    req = _make_request(
        chemical_state="CATALYST_OVERWHELMED",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0420"],
        active_mil=True,
        o2_voltage_b1s1=0.7,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id.startswith("ERR-CF-")


def test_exhaust_leak_family_routes(router: FaultAtlasRouter) -> None:
    """An exhaust_leak scenario routes correctly."""
    req = _make_request(
        chemical_state="EXHAUST_AIR_LEAK",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0171"],
        active_mil=False,
        long_term_ft1=12.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id.startswith("ERR-EL-")


def test_ignition_fault_family_routes(router: FaultAtlasRouter) -> None:
    """An ignition_fault scenario routes correctly."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0302"],
        active_mil=True,
        short_term_ft1=18.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id in ("ERR-E2-I104", "ERR-IF-001")


# ===================================================================
# T-P6-9a — emitted-state recovery routing
# ===================================================================


def test_rich_misfire_routes_to_misfire_family(router: FaultAtlasRouter) -> None:
    """RICH_MISFIRE survives Phase-2 pruning and routes to misfire family.

    Rich-mixture misfire with negative LTFT + P0300 misfire DTC.
    wiki: vocabulary.py ChemicalSignature.RICH_MISFIRE
    """
    req = _make_request(
        chemical_state="RICH_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        long_term_ft1=-8.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-MF-002"
    node = router._kg.resolve(verdict["winner"].fault_id)
    assert node.fault_family == "misfire"


def test_vvt_failure_routes_to_cam_timing(router: FaultAtlasRouter) -> None:
    """VVT_FAILURE survives Phase-2 pruning and routes to cam_timing family.

    VVT phaser stuck chemistry with P0014 cam timing DTC.
    wiki: vocabulary.py ChemicalSignature.VVT_FAILURE
    """
    req = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0014"],
        active_mil=True,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-CT-003"
    node = router._kg.resolve(verdict["winner"].fault_id)
    assert node.fault_family == "cam_timing"


# ===================================================================
# T-P6-14 — confidence threshold gate
# ===================================================================


def test_threshold_miss_suppresses_low_confidence_winner(
    router: FaultAtlasRouter,
) -> None:
    """Winner scoring < 0.70 is suppressed → no_fault path.

    ERR-CT-004 (VVT phaser sluggish) has base_weight 0.55, GAS_ONLY,
    no DTC bonus, no PID constraints.  Without corroborating DTCs
    the score is 0.55 < 0.70 — the verdict must be cleared.
    lld: §6.4 — minimum confidence threshold for fault verdict.
    """
    req = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is None, (
        f"Expected winner=None (threshold-miss), got "
        f"{verdict['winner'].fault_id if verdict['winner'] else 'None'} "
        f"with score {verdict['winner_score']:.2f}"
    )
    assert verdict["winner_score"] == 0.0


def test_threshold_pass_when_score_at_or_above_boundary(
    router: FaultAtlasRouter,
) -> None:
    """Winner scoring >= 0.70 still routes correctly (regression guard).

    ERR-CF-005 (catalyst_masking_rich_engine) has base_weight 0.75,
    GAS_ONLY, no DTC bonus — score 0.75 >= 0.70, must pass.
    """
    req = _make_request(
        chemical_state="NORMAL_OPERATION",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        long_term_ft1=-15.0,
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-CF-005"
    assert verdict["winner_score"] == 0.75


# ===================================================================
# T-FX-PURGE-5 — MODERN-only families absent from in-scope
# ===================================================================


class TestModernFamiliesAbsentInScope:
    """T-FX-PURGE-5: MODERN-only fault_ids stripped; in-scope fixtures don't
    surface modern-only families as top-1."""

    _STRIPPED_FAULT_IDS = frozenset({"ERR-E3-F501", "ERR-RM-005"})
    _MODERN_ONLY_FAULT_NAMES = frozenset({
        "gdi_hpfp_internal_seal_leak",
        "hpfp_seal_leak",
    })

    def test_stripped_fault_ids_absent_from_registry(self, registry_path):
        """ERR-E3-F501 and ERR-RM-005 must NOT be in global_fault_registry.json."""
        import json
        with open(registry_path) as f:
            data = json.load(f)
        live_ids = {r["fault_id"] for r in data["registry"]}
        for fid in self._STRIPPED_FAULT_IDS:
            assert fid not in live_ids, (
                f"{fid} found in registry — PURGE-2 should have stripped it"
            )

    def test_stripped_fault_ids_absent_from_live_router_registry(
        self, router: FaultAtlasRouter
    ):
        """The live legacy router registry does not contain stripped rules."""
        live_ids = {r.fault_id for r in router.registry}
        for fid in self._STRIPPED_FAULT_IDS:
            assert fid not in live_ids, (
                f"{fid} found in live router registry — PURGE-2 stripped it from JSON"
            )

    def test_modern_only_fault_names_absent_from_registry(self, registry_path):
        """MODERN-only fault names must NOT appear in any registry rule."""
        import json
        with open(registry_path) as f:
            data = json.load(f)
        live_names = {r.get("fault_name", "") for r in data["registry"]}
        for name in self._MODERN_ONLY_FAULT_NAMES:
            assert name not in live_names, (
                f"MODERN-only fault_name '{name}' found in registry"
            )

    def test_modern_family_not_top1_for_legacy_fixture(
        self, router: FaultAtlasRouter
    ):
        """In-scope LEGACY fixture does NOT surface MODERN-only family as top-1."""
        req = _make_request(
            chemical_state="GDI_HPFP_INTERNAL_SEAL_LEAK",
            horizon="HORIZON_LEGACY",
            confirmed_dtcs=["P0172"],
            active_mil=True,
            long_term_ft1=-25.0,
        )
        verdict = router.execute_triage_loop(_sanitized(req))
        if verdict["winner"] is not None:
            assert verdict["winner"].fault_name not in self._MODERN_ONLY_FAULT_NAMES, (
                f"MODERN-only family '{verdict['winner'].fault_name}' "
                f"appeared as top-1 for in-scope LEGACY fixture"
            )

    def test_modern_family_not_top1_for_adaptive_fixture(
        self, router: FaultAtlasRouter
    ):
        """In-scope ADAPTIVE fixture does NOT surface MODERN-only family as top-1."""
        req = _make_request(
            chemical_state="GDI_HPFP_INTERNAL_SEAL_LEAK",
            horizon="HORIZON_ADAPTIVE",
            confirmed_dtcs=["P0172"],
            active_mil=True,
            long_term_ft1=-25.0,
        )
        verdict = router.execute_triage_loop(_sanitized(req))
        if verdict["winner"] is not None:
            assert verdict["winner"].fault_name not in self._MODERN_ONLY_FAULT_NAMES, (
                f"MODERN-only family '{verdict['winner'].fault_name}' "
                f"appeared as top-1 for in-scope ADAPTIVE fixture"
            )

    def test_legacy_in_scope_routing_unchanged(self, router: FaultAtlasRouter):
        """In-scope LEGACY fixture still routes correctly after denoise."""
        req = _make_request(
            chemical_state="IGNITION_MISFIRE",
            horizon="HORIZON_LEGACY",
            confirmed_dtcs=["P0302"],
            active_mil=True,
            short_term_ft1=18.0,
        )
        verdict = router.execute_triage_loop(_sanitized(req))
        assert verdict["winner"] is not None, (
            "In-scope LEGACY fixture must still produce a winner"
        )
        # Must route to a misfire-family rule, not a MODERN-only family
        assert verdict["winner"].fault_name not in self._MODERN_ONLY_FAULT_NAMES
        node = router._kg.resolve(verdict["winner"].fault_id)
        assert node.fault_family == "misfire", (
            f"Unexpected family for in-scope LEGACY: {node.fault_family}"
        )

    def test_adaptive_in_scope_routing_unchanged(self, router: FaultAtlasRouter):
        """In-scope ADAPTIVE fixture still routes correctly after denoise."""
        req = _make_request(
            chemical_state="RICH_MISFIRE",
            horizon="HORIZON_ADAPTIVE",
            confirmed_dtcs=["P0300"],
            active_mil=False,
            long_term_ft1=-8.0,
        )
        verdict = router.execute_triage_loop(_sanitized(req))
        assert verdict["winner"] is not None, (
            "In-scope ADAPTIVE fixture must still produce a winner"
        )
        node = router._kg.resolve(verdict["winner"].fault_id)
        assert node.fault_family == "misfire", (
            f"Unexpected family for in-scope ADAPTIVE: {node.fault_family}"
        )


def _misfire_loc_router(
    registry_path: Any,
    *,
    enable_misfire_loc: bool,
) -> FaultAtlasRouter:
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_misfire_loc=enable_misfire_loc,
    )
    router.registry = [
        RegistryRow.model_validate({
            "fault_id": "ERR-LC-001",
            "fault_name": "lean_candidate",
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
                "base_weight": 0.75,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-MF-002",
            "fault_name": "misfire_candidate",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]
    return router


def test_misfire_loc_inert_when_off(registry_path):
    """Misfire localiser has no effect if flag is off or counts are absent/unavailable."""
    from datetime import datetime, timezone
    from comlab.schemas.ingestion import UserInputEchoAudit
    baseline_request = _make_request(
        chemical_state="NORMAL_OPERATION",
        confirmed_dtcs=[],
        short_term_ft1=18.0,
    )
    baseline_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    req_with_counts = baseline_request.model_copy(deep=True)
    assert req_with_counts.obd_live_data is not None
    req_with_counts.obd_live_data.per_cylinder_misfire_counts = {3: 40, 1: 1, 2: 0, 4: 1}
    req_with_counts.obd_live_data.total_trim_correction_delta = 18.0

    req_without_counts = baseline_request.model_copy(deep=True)
    assert req_without_counts.obd_live_data is not None
    req_without_counts.obd_live_data.per_cylinder_misfire_counts = None
    req_without_counts.obd_live_data.total_trim_correction_delta = 18.0

    disabled = _misfire_loc_router(registry_path, enable_misfire_loc=False)
    enabled = _misfire_loc_router(registry_path, enable_misfire_loc=True)

    out_disabled_with = disabled.route(_sanitized(req_with_counts))
    out_disabled_without = disabled.route(_sanitized(req_without_counts))
    out_enabled_without = enabled.route(_sanitized(req_without_counts))

    assert out_disabled_with == out_disabled_without
    assert out_enabled_without == out_disabled_without


def test_misfire_loc_single_cylinder(registry_path, monkeypatch):
    """Dominating cylinder misfire + high positive trim biases toward local faults and away from lean_condition."""
    req = _make_request(
        chemical_state="NORMAL_OPERATION",
        confirmed_dtcs=[],
        short_term_ft1=18.0,
    )
    assert req.obd_live_data is not None
    req.obd_live_data.per_cylinder_misfire_counts = {3: 40, 1: 1, 2: 0, 4: 1}
    req.obd_live_data.total_trim_correction_delta = 18.0

    enabled = _misfire_loc_router(registry_path, enable_misfire_loc=True)

    from tests.unit.test_fault_atlas_router import _RecordingTracer, router_module
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    verdict = enabled.execute_triage_loop(_sanitized(req))

    assert "misfire_localised" in tracer.spans
    span = tracer.spans["misfire_localised"]
    events = span.events
    assert len(events) > 0
    # check locality event
    local_event = next(attrs for name, attrs in events if name == "misfire_localised")
    assert local_event["locality"] == "SINGLE_CYLINDER"

    misfire_events = [attrs for name, attrs in events if name == "misfire_re_ranking_applied"]
    assert any(attrs["family"] in ("misfire", "ignition_fault") for attrs in misfire_events)
    assert any(attrs["family"] == "lean_condition" for attrs in misfire_events)

    # With single cylinder bias: ERR-MF-002 (misfire, boosted to 0.80) should win over ERR-LC-001 (lean_condition, demoted to 0.60)
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-MF-002"
    assert verdict["winner_score"] == 0.80


def test_misfire_loc_global(registry_path, monkeypatch):
    """Global spread misfire + high positive trim biases toward fuelling/starvation branch (lean_condition)."""
    req = _make_request(
        chemical_state="NORMAL_OPERATION",
        confirmed_dtcs=[],
        short_term_ft1=18.0,
    )
    assert req.obd_live_data is not None
    req.obd_live_data.per_cylinder_misfire_counts = {1: 10, 2: 10, 3: 10, 4: 10}
    req.obd_live_data.total_trim_correction_delta = 18.0

    enabled = _misfire_loc_router(registry_path, enable_misfire_loc=True)

    from tests.unit.test_fault_atlas_router import _RecordingTracer, router_module
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    verdict = enabled.execute_triage_loop(_sanitized(req))

    assert "misfire_localised" in tracer.spans
    span = tracer.spans["misfire_localised"]
    events = span.events
    assert len(events) > 0
    # check locality event
    local_event = next(attrs for name, attrs in events if name == "misfire_localised")
    assert local_event["locality"] == "GLOBAL"

    misfire_events = [attrs for name, attrs in events if name == "misfire_re_ranking_applied"]
    assert any(attrs["family"] == "lean_condition" for attrs in misfire_events)

    # With global misfire: ERR-LC-001 (lean_condition, boosted to 0.80) wins over ERR-MF-002 (misfire, unaffected at 0.70)
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-LC-001"
    assert verdict["winner_score"] == 0.80


def _maf_lin_router(
    registry_path: Any,
    *,
    enable_maf_lin: bool,
) -> FaultAtlasRouter:
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_maf_lin=enable_maf_lin,
    )
    router.registry = [
        RegistryRow.model_validate({
            "fault_id": "ERR-LC-002",
            "fault_name": "contaminated_maf",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "P0101",
            "fault_name": "maf_range_performance",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "P0102",
            "fault_name": "maf_low_input",
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
                "base_weight": 0.75,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]
    return router


def test_maf_lin_inert_when_off(registry_path):
    """MAF linearity ladder is inert if the flag is off or delta is None."""
    from datetime import datetime, timezone
    from comlab.schemas.ingestion import UserInputEchoAudit
    baseline_request = _make_request(
        chemical_state="NORMAL_OPERATION",
        confirmed_dtcs=[],
    )
    baseline_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )
    req_with_delta = baseline_request.model_copy(deep=True)
    assert req_with_delta.obd_live_data is not None
    req_with_delta.obd_live_data.sensor_error_delta = 18.0
    req_with_delta.obd_live_data.w_theo = 5.0

    req_none_delta = baseline_request.model_copy(deep=True)
    assert req_none_delta.obd_live_data is not None
    req_none_delta.obd_live_data.sensor_error_delta = None

    disabled = _maf_lin_router(registry_path, enable_maf_lin=False)
    enabled = _maf_lin_router(registry_path, enable_maf_lin=True)

    out_disabled_with = disabled.route(_sanitized(req_with_delta))
    out_disabled_none = disabled.route(_sanitized(req_none_delta))
    out_enabled_none = enabled.route(_sanitized(req_none_delta))

    assert out_disabled_with == out_disabled_none
    assert out_enabled_none == out_disabled_none


def test_maf_lin_drift_routes_lc002(registry_path, monkeypatch):
    """Calibration drift (5-12%) raises ERR-LC-002 rank and emits trace."""
    req = _make_request(
        chemical_state="NORMAL_OPERATION",
        confirmed_dtcs=[],
    )
    assert req.obd_live_data is not None
    req.obd_live_data.sensor_error_delta = 8.0
    req.obd_live_data.w_theo = 5.0

    enabled = _maf_lin_router(registry_path, enable_maf_lin=True)

    from tests.unit.test_fault_atlas_router import _RecordingTracer, router_module
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    verdict = enabled.execute_triage_loop(_sanitized(req))

    assert "maf_linearity_applied" in tracer.spans
    span = tracer.spans["maf_linearity_applied"]
    assert span.attributes["router.maf_linearity_band"] == "CALIBRATION_DRIFT"
    assert span.attributes["router.sensor_error_delta"] == 8.0
    assert span.attributes["router.w_theo"] == 5.0

    # ERR-LC-002 has base_weight 0.70, boosted to 0.80. P0102 has base_weight 0.75, demoted to 0.60.
    # So ERR-LC-002 should win.
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-LC-002"
    assert verdict["winner_score"] == 0.80


def test_maf_lin_component_routes_p0101(registry_path, monkeypatch):
    """Component fault (>12%) raises P0101 rank and demotes P0102. 4.0% is inert."""
    req_inert = _make_request(
        chemical_state="NORMAL_OPERATION",
        confirmed_dtcs=[],
    )
    assert req_inert.obd_live_data is not None
    req_inert.obd_live_data.sensor_error_delta = 4.0

    req_fault = _make_request(
        chemical_state="NORMAL_OPERATION",
        confirmed_dtcs=[],
    )
    assert req_fault.obd_live_data is not None
    req_fault.obd_live_data.sensor_error_delta = 18.0
    req_fault.obd_live_data.w_theo = 5.0

    enabled = _maf_lin_router(registry_path, enable_maf_lin=True)

    from tests.unit.test_fault_atlas_router import _RecordingTracer, router_module
    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)

    # 4.0% should be inert, so winner is P0102 (base_weight 0.75 vs 0.70 for others)
    verdict_inert = enabled.execute_triage_loop(_sanitized(req_inert))
    assert verdict_inert["winner"] is not None
    assert verdict_inert["winner"].fault_id == "P0102"
    assert verdict_inert["winner_score"] == 0.75

    # 18.0% should boost P0101 to 0.80, and demote P0102 to 0.60. P0101 should win.
    verdict_fault = enabled.execute_triage_loop(_sanitized(req_fault))
    assert verdict_fault["winner"] is not None
    assert verdict_fault["winner"].fault_id == "P0101"
    assert verdict_fault["winner_score"] == 0.80


# ---------------------------------------------------------------------------
# No-start branch (T-COMV2-NOSTART-1)
# ---------------------------------------------------------------------------


def _nostart_request(
    *,
    monitor_aborted: bool = False,
    ff_fuel_spark_cut_at_crank: bool | None = None,
) -> OrchestratorInboundRequest:
    """Build a request with DTC payload carrying no-start signals."""
    mode_06_monitors: dict[str, Mode06MonitorResult] = {}
    if monitor_aborted:
        mode_06_monitors["MID_02_TID_0B"] = Mode06MonitorResult(
            monitor_id="MID_02_TID_0B",
            state=Mode06MonitorState.MONITOR_ABORTED,
            margin_pct=0.0,
            target_component="O2_SENSOR_B1S1",
        )
    ff_kwargs: dict[str, Any] = {}
    if ff_fuel_spark_cut_at_crank is not None:
        ff_kwargs["ff_fuel_spark_cut_at_crank"] = ff_fuel_spark_cut_at_crank
    request = _make_request()
    request.dtc_lab_output = DTCLabPayload(
        active_mil=False,
        mil_flashing=False,
        confirmed_dtcs=[],
        pending_dtcs=[],
        permanent_dtcs=[],
        routing_tags=[],
        mode_06_monitors=mode_06_monitors,
        historical_fault_context=HistoricalFaultContext.UNKNOWN,
        freeze_frame=FreezeFrameRecord(
            calculated_load_pct=0.0,
            engine_rpm=0,
            coolant_temp_c=85.0,
            short_term_ft1=0.0,
            long_term_ft1=0.0,
            manifold_pressure_kpa=100.0,
            vehicle_speed_kmh=0,
            ignition_advance_deg=10.0,
            intake_air_temp_c=20.0,
            maf_gps=0.0,
            throttle_pos_pct=0.0,
            fuel_system_status=FuelSystemStatus.OL,
            **ff_kwargs,
        ),
    )
    return request


def _nostart_router(
    registry_path: Any,
    *,
    enable_nostart: bool,
) -> FaultAtlasRouter:
    """Build a router with global + security + mechanical controlled rules."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=False,
        enable_nostart=enable_nostart,
    )
    router.registry = [
        RegistryRow.model_validate({
            "fault_id": "ERR-MW-003",
            "fault_name": "global_candidate",
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
                "base_weight": 0.79,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-NS-005",
            "fault_name": "security_lockout_candidate",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            "fault_id": "ERR-NS-001",
            "fault_name": "mechanical_nostart_candidate",
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
                "base_weight": 0.70,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]
    return router


# --- inert / invariant tests ---


def test_nostart_inert_when_off(registry_path: Any) -> None:
    """Flag-off and dtc_lab_output-None are byte-identical to baseline."""
    baseline_request = _make_request()
    baseline_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )

    # Build the aborted variant as a deep copy of baseline
    aborted_request = baseline_request.model_copy(deep=True)
    assert aborted_request.dtc_lab_output is not None
    aborted_request.dtc_lab_output.mode_06_monitors = {
        "MID_02_TID_0B": Mode06MonitorResult(
            monitor_id="MID_02_TID_0B",
            state=Mode06MonitorState.MONITOR_ABORTED,
            margin_pct=0.0,
            target_component="O2_SENSOR_B1S1",
        ),
    }
    aborted_request.dtc_lab_output.freeze_frame.ff_fuel_spark_cut_at_crank = True

    disabled = _nostart_router(registry_path, enable_nostart=False)
    enabled = _nostart_router(registry_path, enable_nostart=True)

    baseline = disabled.route(_sanitized(baseline_request))
    flag_off = disabled.route(_sanitized(aborted_request))
    dtc_absent = enabled.route(_sanitized(baseline_request))

    assert flag_off == baseline
    assert dtc_absent == baseline


def test_nostart_no_aborted_inert(registry_path: Any) -> None:
    """Monitors present but no MONITOR_ABORTED → byte-identical to baseline."""
    baseline_request = _make_request()
    baseline_request.user_input_echo_audit = UserInputEchoAudit(
        submitted_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        groups=[],
    )

    # Build variant with monitors but none aborted as deep copy
    req_no_abort = baseline_request.model_copy(deep=True)
    assert req_no_abort.dtc_lab_output is not None
    req_no_abort.dtc_lab_output.mode_06_monitors = {
        "MID_02_TID_0B": Mode06MonitorResult(
            monitor_id="MID_02_TID_0B",
            state=Mode06MonitorState.PASSED,
            margin_pct=0.0,
            target_component="O2_SENSOR_B1S1",
        ),
    }

    disabled = _nostart_router(registry_path, enable_nostart=False)
    enabled = _nostart_router(registry_path, enable_nostart=True)

    baseline = disabled.route(_sanitized(baseline_request))
    flag_on_no_abort = enabled.route(_sanitized(req_no_abort))

    assert flag_on_no_abort == baseline


# --- activation tests ---


def test_nostart_security_lockout(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """MONITOR_ABORTED + ff_fuel_spark_cut_at_crank=True → ERR-NS-005 promoted."""
    request = _nostart_request(
        monitor_aborted=True,
        ff_fuel_spark_cut_at_crank=True,
    )
    disabled = _nostart_router(registry_path, enable_nostart=False)
    enabled = _nostart_router(registry_path, enable_nostart=True)

    baseline = disabled.execute_triage_loop(_sanitized(request))
    assert baseline["winner"] is not None
    assert baseline["winner"].fault_id == "ERR-MW-003"

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    promoted = enabled.execute_triage_loop(_sanitized(request))

    assert promoted["winner"] is not None
    assert promoted["winner"].fault_id == "ERR-NS-005"
    assert promoted["winner_score"] == 0.80
    score_events = tracer.spans["phase.score"].events
    assert any(name == "no_start_branch_applied" for name, _attrs in score_events)
    # Verify event attributes
    for name, attrs in score_events:
        if name == "no_start_branch_applied":
            assert attrs["verdict"] == "SECURITY_LOCKOUT"
            assert attrs["ff_fuel_spark_cut_at_crank"] is True
            assert attrs["score_after"] == 0.80


def test_nostart_mechanical(
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """MONITOR_ABORTED + ff_fuel_spark_cut_at_crank=False → mechanical node promoted."""
    request = _nostart_request(
        monitor_aborted=True,
        ff_fuel_spark_cut_at_crank=False,
    )
    disabled = _nostart_router(registry_path, enable_nostart=False)
    enabled = _nostart_router(registry_path, enable_nostart=True)

    baseline = disabled.execute_triage_loop(_sanitized(request))
    assert baseline["winner"] is not None
    assert baseline["winner"].fault_id == "ERR-MW-003"

    tracer = _RecordingTracer()
    monkeypatch.setattr(router_module, "get_tracer", lambda _name: tracer)
    promoted = enabled.execute_triage_loop(_sanitized(request))

    assert promoted["winner"] is not None
    assert promoted["winner"].fault_id == "ERR-NS-001"
    assert promoted["winner_score"] == 0.80
    score_events = tracer.spans["phase.score"].events
    assert any(name == "no_start_branch_applied" for name, _attrs in score_events)
    for name, attrs in score_events:
        if name == "no_start_branch_applied":
            assert attrs["verdict"] == "MECHANICAL"
            assert attrs["ff_fuel_spark_cut_at_crank"] is False
            assert attrs["score_after"] == 0.80


# --- helper function unit tests ---


def test_nostart_helper_unavailable() -> None:
    """_no_start_branch returns UNAVAILABLE when inputs are absent."""
    assert _no_start_branch(None, None).state == "UNAVAILABLE"
    assert _no_start_branch({}, True).state == "UNAVAILABLE"
    assert _no_start_branch(None, False).state == "UNAVAILABLE"


def test_nostart_helper_states() -> None:
    """_no_start_branch classifies security vs mechanical correctly."""
    import comlab.core.fault_atlas_router as rmod

    aborted_monitor = Mode06MonitorResult(
        monitor_id="MID_02_TID_0B",
        state=Mode06MonitorState.MONITOR_ABORTED,
        margin_pct=0.0,
        target_component="O2_SENSOR_B1S1",
    )
    passed_monitor = Mode06MonitorResult(
        monitor_id="MID_05_TID_10",
        state=Mode06MonitorState.PASSED,
        margin_pct=0.0,
        target_component="CATALYST_B1",
    )

    # No abort in monitors
    result = _no_start_branch(
        {"mid": passed_monitor}, True,
    )
    assert result.state == "UNAVAILABLE"

    # Aborted + cut = security
    result = _no_start_branch(
        {"mid": aborted_monitor}, True,
    )
    assert result.state == "SECURITY_LOCKOUT"
    assert result.confidence == rmod._NOSTART_CONFIDENCE

    # Aborted + no cut = mechanical
    result = _no_start_branch(
        {"mid": aborted_monitor}, False,
    )
    assert result.state == "MECHANICAL"
    assert result.confidence == rmod._NOSTART_CONFIDENCE


# --- schema round-trip tests ---


def test_nostart_schema_roundtrip() -> None:
    """MONITOR_ABORTED parses and ff_fuel_spark_cut_at_crank round-trips."""
    # MONITOR_ABORTED parses on Mode06MonitorResult.state
    monitor = Mode06MonitorResult(
        monitor_id="MID_02_TID_0B",
        state=Mode06MonitorState.MONITOR_ABORTED,
        margin_pct=0.0,
        target_component="O2_SENSOR_B1S1",
    )
    assert monitor.state == Mode06MonitorState.MONITOR_ABORTED
    assert monitor.state.value == "MONITOR_ABORTED"

    # ff_fuel_spark_cut_at_crank round-trips through FreezeFrameRecord
    ff = FreezeFrameRecord(
        calculated_load_pct=0.0,
        engine_rpm=0,
        coolant_temp_c=85.0,
        short_term_ft1=0.0,
        long_term_ft1=0.0,
        manifold_pressure_kpa=100.0,
        vehicle_speed_kmh=0,
        ignition_advance_deg=10.0,
        intake_air_temp_c=20.0,
        maf_gps=0.0,
        throttle_pos_pct=0.0,
        fuel_system_status=FuelSystemStatus.OL,
        ff_fuel_spark_cut_at_crank=True,
    )
    dumped = ff.model_dump()
    assert dumped["ff_fuel_spark_cut_at_crank"] is True

    ff_default = FreezeFrameRecord(
        calculated_load_pct=0.0,
        engine_rpm=0,
        coolant_temp_c=85.0,
        short_term_ft1=0.0,
        long_term_ft1=0.0,
        manifold_pressure_kpa=100.0,
        vehicle_speed_kmh=0,
        ignition_advance_deg=10.0,
        intake_air_temp_c=20.0,
        maf_gps=0.0,
        throttle_pos_pct=0.0,
        fuel_system_status=FuelSystemStatus.OL,
    )
    assert ff_default.ff_fuel_spark_cut_at_crank is False
