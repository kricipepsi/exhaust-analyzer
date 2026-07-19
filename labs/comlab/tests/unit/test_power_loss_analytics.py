"""Unit tests for Script 4 (PowerLossAnalytics).

Reference cases from OrchestratorLabBP.md lines 240-281.
"""

from __future__ import annotations

from uuid import UUID


from comlab.analytics.power_loss_analytics import PowerLossAnalytics


def test_4cyl_single_misfire_yields_23pct():
    """BP line 240: HC 3200, O2 5.1, CO 0.1, lambda 1.25, 4 cyl -> 23.3%."""
    loss = PowerLossAnalytics.estimate_kinetic_loss(
        gas_hc=3200, gas_o2=5.1, gas_co=0.1, lambda_chem=1.25, cylinder_count=4
    )
    assert 22.0 <= loss <= 27.0


def test_8cyl_same_chemistry_yields_half_the_loss():
    """BP line 254: 8-cyl is exactly half of 4-cyl for the same gas profile."""
    loss_4 = PowerLossAnalytics.estimate_kinetic_loss(3200, 5.1, 0.1, 1.25, 4)
    loss_8 = PowerLossAnalytics.estimate_kinetic_loss(3200, 5.1, 0.1, 1.25, 8)
    assert loss_8 == round(loss_4 / 2.0, 1)


def test_partial_combustion_yields_intermediate_loss():
    """BP line 269: low O2, high CO, 4 cyl -> 22.9%."""
    loss = PowerLossAnalytics.estimate_kinetic_loss(
        gas_hc=850, gas_o2=0.3, gas_co=3.8, lambda_chem=0.88, cylinder_count=4
    )
    assert 15.0 <= loss <= 25.0


def test_catalyst_health_index_clamps_to_100():
    chi = PowerLossAnalytics.calculate_catalyst_health_index(
        gas_co=0.0, gas_hc=0, pre_cat_lambda=1.000
    )
    assert chi == 100.0


def test_analytics_module_imports():
    """Smoke: module loads, class accessible."""
    assert hasattr(PowerLossAnalytics, "estimate_kinetic_loss")


def test_compute_catalyst_index_none_when_decat():
    """compute() returns catalyst_efficiency_index_pct=None when has_catalyst=False.

    T-FX-11 Success criterion 3: de-cat vehicles get no catalyst health index
    even when a downstream O2 sensor is present.
    """
    from comlab.schemas.ingestion import (
        OrchestratorInboundRequest,
        SessionMetadata,
        GasLabPayload,
        OBDLiveDataPayload,
        DTCLabPayload,
        FreezeFrameRecord,
        HistoricalFaultContext,
    )
    from comlab.schemas.vocabulary import (
        Horizon,
        VinConfidence,
        ChemicalSignature,
        SampleValidity,
        VEValidity,
        TrimAnalyticsGate,
        O2FailureMode,
        NodeMAFStatus,
        NodeMAPStatus,
        EngineStateBucket,
        FuelSystemStatus,
    )

    request = OrchestratorInboundRequest(
        metadata=SessionMetadata(
            session_id=UUID("a1b2c3d4-e5f6-4789-abcd-ef1234567890"),
            vin_dna_string="TESTVIN1234567890",
            resolved_horizon=Horizon.MODERN,
            cylinder_count=4,
            schema_version="1.0",
            vin_confidence=VinConfidence.HIGH,
        ),
        gas_lab_output=GasLabPayload(
            chemical_state=ChemicalSignature.NORMAL_OPERATION,
            gas_co=0.5,
            gas_hc=200,
            gas_co2=14.0,
            gas_o2=0.5,
            gas_nox=50,
            lambda_chem=1.000,
            sample_validity=SampleValidity.VALID,
            lambda_measured=None,
        ),
        obd_live_data=OBDLiveDataPayload(
            engine_warmed=True,
            total_trim_correction_delta=-5.0,
            normalized_obd_lambda=1.01,
            ve_pct=85.0,
            ve_validity=VEValidity.VALID,
            rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
            trim_analytics_gate=TrimAnalyticsGate.VALID,
            o2_failure_mode=O2FailureMode.NO_FAULT,
            maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
            map_status=NodeMAPStatus.REAL_SENSOR_FEED,
        ),
        dtc_lab_output=DTCLabPayload(
            active_mil=False,
            mil_flashing=False,
            confirmed_dtcs=[],
            pending_dtcs=[],
            permanent_dtcs=[],
            routing_tags=[],
            mode_06_monitors={},
            historical_fault_context=HistoricalFaultContext.UNKNOWN,
            freeze_frame=FreezeFrameRecord(
                calculated_load_pct=0.0,
                engine_rpm=0,
                coolant_temp_c=90,
                short_term_ft1=0.0,
                long_term_ft1=0.0,
                manifold_pressure_kpa=100,
                vehicle_speed_kmh=0,
                ignition_advance_deg=10.0,
                intake_air_temp_c=20.0,
                maf_gps=0.0,
                throttle_pos_pct=0.0,
                fuel_system_status=FuelSystemStatus.OL,
                o2_voltage_b1s1=0.45,
                barometric_pressure_kpa=101,
            ),
        ),
    )

    analytics = PowerLossAnalytics()
    # De-cat + downstream O2 present → should still be None
    result = analytics.compute(
        request=request,
        cylinder_count=4,
        downstream_o2_present=True,
        has_catalyst=False,
    )
    assert result.catalyst_efficiency_index_pct is None

    # Catalyst present + downstream O2 present → should compute
    result2 = analytics.compute(
        request=request,
        cylinder_count=4,
        downstream_o2_present=True,
        has_catalyst=True,
    )
    assert result2.catalyst_efficiency_index_pct is not None
