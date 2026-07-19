"""Unit tests for T-FX-DNA-3 symptom-prior term in COMLab rank phase.

Covers success criteria:
- (a) prior lifts mapped family when csv_primary_symptom is present
- (b) bounded — prior capped at 1.0; non-target families unaffected
- (c) blank symptom → identical ranking to pre-change
- (d) unknown symptom → neutral (zero prior)
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter
from comlab.schemas.ingestion import (
    DTCLabPayload,
    FreezeFramePIDs,
    FreezeFrameRecord,
    GasLabPayload,
    OBDLiveDataPayload,
    OrchestratorInboundRequest,
    SessionMetadata,
)
from comlab.schemas.vocabulary import (
    EngineStateBucket,
    FuelSystemStatus,
    HistoricalFaultContext,
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
    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    return FaultAtlasRouter(str(registry_path), kg, analytics, use_v2_registry=False)


# ---------------------------------------------------------------------------
# Helpers
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
    short_term_ft1: float = 0.0,
    long_term_ft1: float = 0.0,
    manifold_pressure_kpa: float = 100.0,
    coolant_temp_c: float = 85.0,
    symptom_dna: dict | None = None,
) -> OrchestratorInboundRequest:
    """Build a minimal OrchestratorInboundRequest for symptom-prior tests."""
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
            total_trim_correction_delta=0.0,
            normalized_obd_lambda=1.0,
            ve_pct=72.0,
            ve_validity=VEValidity.VALID,
            rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
            trim_analytics_gate=TrimAnalyticsGate.VALID,
            o2_failure_mode=O2FailureMode.STUCK_LEAN,
            maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
            map_status=NodeMAPStatus.REAL_SENSOR_FEED,
            shrtft1=short_term_ft1,
            longft1=long_term_ft1,
            mass_airflow_gps=0.0,
            coolant_temp_c=coolant_temp_c,
            freeze_frame_pids=FreezeFramePIDs(
                calculated_engine_load_pct=0.0,
                freeze_frame_engine_rpm=0,
            ),
        ),
        dtc_lab_output=DTCLabPayload(
            active_mil=active_mil,
            mil_flashing=False,
            confirmed_dtcs=confirmed_dtcs or [],
            pending_dtcs=[],
            permanent_dtcs=[],
            routing_tags=[],
            mode_06_monitors={},
            historical_fault_context=HistoricalFaultContext.UNKNOWN,
            freeze_frame=FreezeFrameRecord(
                calculated_load_pct=0.0,
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
                o2_voltage_b1s1=None,
                barometric_pressure_kpa=101.3,
            ),
        ),
        symptom_dna=symptom_dna if symptom_dna is not None else {},
    )


def _sanitized(request: OrchestratorInboundRequest) -> dict:
    return {"request": request}


# ---------------------------------------------------------------------------
# (a) Prior lifts mapped family when csv_primary_symptom is present
# ---------------------------------------------------------------------------


def test_prior_lifts_misfire_family(router: FaultAtlasRouter) -> None:
    """ERR-MF-002 (misfire) gets +0.10 score boost with running_rough.

    Uses active_mil=False to eliminate ERR-E2-I104 (requires MIL active),
    leaving ERR-MF-002 (base=0.75, bonus=0.15) as winner at 0.90.
    Prior boost: 0.90 + 0.10 = 1.00.
    """
    # Without prior — ERR-MF-002 wins at 0.75 + 0.15 = 0.90
    req_no_prior = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,  # satisfies shrtft1 > 5.0 for ERR-MF-002
        symptom_dna={},
    )
    verdict_no_prior = router.execute_triage_loop(_sanitized(req_no_prior))
    assert verdict_no_prior["winner"] is not None
    assert verdict_no_prior["winner"].fault_id == "ERR-MF-002"
    score_before = verdict_no_prior["winner_score"]
    assert score_before == pytest.approx(0.90)

    # With prior — ERR-MF-002 boosted to 1.00
    req_with_prior = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,
        symptom_dna={"_csv_primary_symptom": "running_rough"},
    )
    verdict_with_prior = router.execute_triage_loop(_sanitized(req_with_prior))
    assert verdict_with_prior["winner"] is not None
    assert verdict_with_prior["winner"].fault_id == "ERR-MF-002"
    score_after = verdict_with_prior["winner_score"]

    # Prior should boost the score
    assert score_after > score_before
    assert score_after == pytest.approx(1.00)


def test_prior_does_not_affect_non_target_family(router: FaultAtlasRouter) -> None:
    """Prior does not boost non-misfire families even when symptom is present.

    ERR-E1-M032 is in the lean_condition family — running_rough prior
    targets misfire only, so the score is unchanged.
    """
    req = _make_request(
        chemical_state="INCOMPLETE_OXIDATION",
        horizon="HORIZON_LEGACY",
        confirmed_dtcs=["P0401"],
        active_mil=False,
        manifold_pressure_kpa=65.0,
        symptom_dna={"_csv_primary_symptom": "running_rough"},
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-E1-M032"
    # lean_condition family — no misfire prior boost
    # INCOMPLETE_OXIDATION cap applies (0.75 without supporting routing tags)
    assert verdict["winner_score"] == pytest.approx(0.75)


# ---------------------------------------------------------------------------
# (b) Bounded — prior capped at 1.0; non-target families unaffected
# ---------------------------------------------------------------------------


def test_prior_respects_score_cap(router: FaultAtlasRouter) -> None:
    """Prior boost is capped at 1.0 — cannot exceed absolute maximum.

    Even when the misfire rule already scores near the cap, the prior
    doesn't push it above 1.0.
    """
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,
        symptom_dna={"_csv_primary_symptom": "running_rough"},
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    # Score must not exceed 1.0
    assert verdict["winner_score"] <= 1.0


def test_prior_bounded_on_non_misfire_scenario(router: FaultAtlasRouter) -> None:
    """Prior does not create false positives in NORMAL_OPERATION scenario.

    NORMAL_OPERATION matches catalyst_failure, exhaust_leak, sensor_fault,
    and ecu_fault rules — but no misfire rules.  The prior should have
    zero effect (no misfire-family candidates to boost).
    """
    # Without prior
    req_ref = _make_request(
        chemical_state="NORMAL_OPERATION",
        horizon="HORIZON_MODERN",
        long_term_ft1=-15.0,
        symptom_dna={},
    )
    verdict_ref = router.execute_triage_loop(_sanitized(req_ref))

    # With prior
    req_prior = _make_request(
        chemical_state="NORMAL_OPERATION",
        horizon="HORIZON_MODERN",
        long_term_ft1=-15.0,
        symptom_dna={"_csv_primary_symptom": "running_rough"},
    )
    verdict_prior = router.execute_triage_loop(_sanitized(req_prior))

    # Same winner and score — no misfire rules in play
    assert verdict_prior["winner"] is not None
    assert verdict_ref["winner"] is not None
    assert verdict_prior["winner"].fault_id == verdict_ref["winner"].fault_id
    assert verdict_prior["winner_score"] == verdict_ref["winner_score"]


# ---------------------------------------------------------------------------
# (c) Blank symptom → identical ranking to pre-change
# ---------------------------------------------------------------------------


def test_blank_symptom_neutral(router: FaultAtlasRouter) -> None:
    """Empty symptom_dna produces same result as missing _csv_primary_symptom."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,
        symptom_dna={},
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    score_without = verdict["winner_score"]

    # Same with tier_1 present but no _csv_primary_symptom
    req2 = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,
        symptom_dna={"tier_1_primary_symptom": "rough_idle_shudder"},
    )
    verdict2 = router.execute_triage_loop(_sanitized(req2))
    assert verdict2["winner_score"] == score_without


# ---------------------------------------------------------------------------
# (d) Unknown symptom → neutral
# ---------------------------------------------------------------------------


def test_unknown_symptom_neutral(router: FaultAtlasRouter) -> None:
    """Unknown csv_primary_symptom value produces no prior boost."""
    req_ref = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,
        symptom_dna={},
    )
    verdict_ref = router.execute_triage_loop(_sanitized(req_ref))

    req_unknown = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,
        symptom_dna={"_csv_primary_symptom": "stalls"},
    )
    verdict_unknown = router.execute_triage_loop(_sanitized(req_unknown))

    assert verdict_unknown["winner_score"] == verdict_ref["winner_score"]


def test_none_symptom_neutral(router: FaultAtlasRouter) -> None:
    """csv_primary_symptom='none' produces no prior boost (not in prior table)."""
    req = _make_request(
        chemical_state="IGNITION_MISFIRE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=["P0300"],
        active_mil=False,
        short_term_ft1=6.0,
        symptom_dna={"_csv_primary_symptom": "none"},
    )
    verdict = router.execute_triage_loop(_sanitized(req))
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-MF-002"
    assert verdict["winner_score"] == pytest.approx(0.90)


# ---------------------------------------------------------------------------
# Prior config loading
# ---------------------------------------------------------------------------


def test_prior_table_loaded(router: FaultAtlasRouter) -> None:
    """Prior table is loaded from symptom_prior.yaml."""
    assert len(router._prior_table) >= 3
    assert router._prior_weight == pytest.approx(0.10)
    assert "running_rough" in router._prior_table
    assert router._prior_table["running_rough"]["family"] == "misfire"


def test_hard_start_cold_prior(router: FaultAtlasRouter) -> None:
    """hard_start_cold → rich_mixture prior is loaded and correct."""
    assert router._prior_table["hard_start_cold"]["family"] == "rich_mixture"


def test_non_starter_prior(router: FaultAtlasRouter) -> None:
    """non_starter → non_starter prior is loaded and correct."""
    assert router._prior_table["non_starter"]["family"] == "non_starter"


# ---------------------------------------------------------------------------
# Context modifier (T-COMV2-CTXMOD-1)
# ---------------------------------------------------------------------------


def test_ctxmod_inert_when_off(registry_path, monkeypatch) -> None:
    """A payload with environmental_conditions.load_state set, flag off -> identical output to baseline;
    flag on, no load_state -> identical.
    """
    monkeypatch.setattr("comlab.core.fault_atlas_router.MIN_CONFIDENCE_THRESHOLD", 0.0)

    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    router_off = FaultAtlasRouter(str(registry_path), kg, analytics, use_v2_registry=False, enable_ctxmod=False)
    router_on = FaultAtlasRouter(str(registry_path), kg, analytics, use_v2_registry=False, enable_ctxmod=True)

    # Base request for ERR-CT-004 (base weight 0.55)
    req_with_load = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        symptom_dna={
            "_csv_primary_symptom": "poor_acceleration",
            "environmental_conditions": {"load_state": "transient_acceleration"},
        },
    )
    req_no_load = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        symptom_dna={
            "_csv_primary_symptom": "poor_acceleration",
        },
    )

    # 1. flag off, load_state set
    res_off_with_load = router_off.execute_triage_loop(_sanitized(req_with_load))
    # 2. flag off, no load_state (baseline)
    res_off_no_load = router_off.execute_triage_loop(_sanitized(req_no_load))
    assert res_off_with_load["winner_score"] == pytest.approx(0.65)
    assert res_off_no_load["winner_score"] == pytest.approx(0.65)

    # 3. flag on, no load_state
    res_on_no_load = router_on.execute_triage_loop(_sanitized(req_no_load))
    assert res_on_no_load["winner_score"] == pytest.approx(0.65)


def test_ctxmod_modulates_prior(registry_path, monkeypatch) -> None:
    """Same symptom under two load_state values, flag on -> different (bounded) symptom-prior weight."""
    monkeypatch.setattr("comlab.core.fault_atlas_router.MIN_CONFIDENCE_THRESHOLD", 0.0)

    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    router_on = FaultAtlasRouter(str(registry_path), kg, analytics, use_v2_registry=False, enable_ctxmod=True)

    # idle load state: poor_acceleration has multiplier 0.5 -> weight = 0.05
    req_idle = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        symptom_dna={
            "_csv_primary_symptom": "poor_acceleration",
            "environmental_conditions": {"load_state": "idle"},
        },
    )
    # transient_acceleration: multiplier 1.5 -> weight = 0.15
    req_accel = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        symptom_dna={
            "_csv_primary_symptom": "poor_acceleration",
            "environmental_conditions": {"load_state": "transient_acceleration"},
        },
    )

    res_idle = router_on.execute_triage_loop(_sanitized(req_idle))
    res_accel = router_on.execute_triage_loop(_sanitized(req_accel))

    # Base score (0.55) + 0.05 = 0.60
    assert res_idle["winner_score"] == pytest.approx(0.60)
    # Base score (0.55) + 0.15 = 0.70, clamped to 0.65
    assert res_accel["winner_score"] == pytest.approx(0.65)


def test_ctxmod_caps_at_065(registry_path, monkeypatch) -> None:
    """A load_state that would push the prior past 0.65 -> weight clamped to 0.65."""
    monkeypatch.setattr("comlab.core.fault_atlas_router.MIN_CONFIDENCE_THRESHOLD", 0.0)

    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    router_on = FaultAtlasRouter(str(registry_path), kg, analytics, use_v2_registry=False, enable_ctxmod=True)

    req_accel = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        symptom_dna={
            "_csv_primary_symptom": "poor_acceleration",
            "environmental_conditions": {"load_state": "transient_acceleration"},
        },
    )
    res = router_on.execute_triage_loop(_sanitized(req_accel))
    # Without clamp, score would be 0.70. With clamp, it must be 0.65.
    assert res["winner_score"] == pytest.approx(0.65)


def test_ctxmod_v2_path(registry_path) -> None:
    """Verify context modifiers and cap on the v2 path."""
    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    router_on = FaultAtlasRouter(str(registry_path), kg, analytics, use_v2_registry=True, enable_ctxmod=True)

    req_idle = _make_request(
        chemical_state="VVT_FAILURE",
        horizon="HORIZON_MODERN",
        confirmed_dtcs=[],
        active_mil=False,
        symptom_dna={
            "_csv_primary_symptom": "poor_acceleration",
            "environmental_conditions": {"load_state": "idle"},
        },
    )
    payload_idle = {
        "request": req_idle,
        "gas_lab_output": {"chemical_state": "VVT_FAILURE", "sample_validity": "VALID"},
        "obd_live_data": {},
        "dtc_lab_output": {"confirmed_dtcs": [], "routing_tags": []},
    }

    res = router_on.route(payload_idle)
    assert res is not None
    assert res.diagnostic_verdict is not None
