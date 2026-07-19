"""Real-routing tests for sensor_fault registry rules — T-P6-11.

Verifies that new ERR-SF-001 (lazy O2) and ERR-SF-002 (fixed voltage) rules
fire via routing_tag and perception_flag triggers on appropriate test payloads.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from tests.fixtures import mock_dtc_lab, mock_gas_lab, mock_obd_lab


def _make_request(*, session_id=None, horizon="HORIZON_MODERN",
                  gas_payload=None, obd_payload=None, dtc_payload=None):
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
# ERR-SF-002 — Upstream O2 Sensor Fixed Voltage (routing_tag: O2_HISTORY)
# ---------------------------------------------------------------------------


def _o2_circuit_dtc() -> dict:
    """P0134 (O2 circuit no activity) + O2_HISTORY routing tag."""
    payload = mock_dtc_lab.no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["P0134"]
    payload["routing_tags"] = ["O2_HISTORY"]
    payload["freeze_frame"] = {
        "calculated_load_pct": 30.0,
        "engine_rpm": 800,
        "coolant_temp_c": 90.0,
        "short_term_ft1": 0.0,
        "long_term_ft1": 0.0,
        "manifold_pressure_kpa": 35.0,
        "vehicle_speed_kmh": 0,
        "ignition_advance_deg": 10.0,
        "intake_air_temp_c": 25.0,
        "maf_gps": 3.5,
        "throttle_pos_pct": 0.0,
        "fuel_system_status": "OL_FAULT",
    }
    return payload


@pytest.mark.e2e
def test_sensor_fault_o2_fixed_voltage_via_routing_tag():
    """ERR-SF-002 fires via O2_HISTORY routing tag + P0134 circuit DTC.

    GASLab sees NORMAL_OPERATION (gas truth is clean) but DTCLab detected
    an O2 circuit fault — the sensor is electrically dead, not just lazy.
    """
    request = _make_request(dtc_payload=_o2_circuit_dtc())
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request)

    verdict = result.diagnostic_verdict
    assert verdict.is_fault_detected is True
    assert verdict.fault_code == "ERR-SF-002"
    assert verdict.fault_family == "sensor_fault"

    fe = result.fault_enrichment
    assert fe.component_group == "Exhaust Gas Sensing System"
    assert fe.mechanical_failure_mode, "mechanical_failure_mode should not be empty"


# ---------------------------------------------------------------------------
# ERR-SF-001 — Upstream O2 Sensor Lazy Response (perception_flag)
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_sensor_fault_o2_lazy_via_perception_biased_high():
    """ERR-SF-001 fires via O2_SENSOR_BIASED_HIGH perception flag.

    OBD lambda (1.12) reads significantly higher than GASLab truth (1.00) —
    the sensor is biased high, reading falsely lean. No O2 circuit DTC present
    (sensor still switches, just too slowly → lazy, not dead).
    """
    request = _make_request(
        obd_payload=mock_obd_lab.sensor_biased_high(),
    )
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request)

    verdict = result.diagnostic_verdict
    assert verdict.is_fault_detected is True
    assert verdict.fault_code == "ERR-SF-001"
    assert verdict.fault_family == "sensor_fault"

    # Perception bias verdict should be in performance analytics
    pa = result.performance_analytics
    assert pa.o2_sensor_bias_verdict == "O2_SENSOR_BIASED_HIGH"

    fe = result.fault_enrichment
    assert fe.component_group == "Exhaust Gas Sensing System"
    assert fe.mechanical_failure_mode, "mechanical_failure_mode should not be empty"


@pytest.mark.e2e
def test_sensor_fault_o2_lazy_via_perception_biased_low():
    """ERR-SF-001 fires via O2_SENSOR_BIASED_LOW perception flag.

    OBD lambda (0.88) reads significantly lower than GASLab truth (1.00) —
    the sensor is biased low, reading falsely rich. No circuit DTC present.
    """
    request = _make_request(
        obd_payload=mock_obd_lab.sensor_biased_low(),
    )
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request)

    verdict = result.diagnostic_verdict
    assert verdict.is_fault_detected is True
    assert verdict.fault_code == "ERR-SF-001"
    assert verdict.fault_family == "sensor_fault"

    pa = result.performance_analytics
    assert pa.o2_sensor_bias_verdict == "O2_SENSOR_BIASED_LOW"

    fe = result.fault_enrichment
    assert fe.component_group == "Exhaust Gas Sensing System"
    assert fe.mechanical_failure_mode, "mechanical_failure_mode should not be empty"


@pytest.mark.e2e
def test_vpwr_default_off_full_pipeline_matches_baseline():
    """The default aggregator ignores low VPWR and preserves pipeline output."""
    session_id = str(uuid4())
    baseline_request = _make_request(
        session_id=session_id,
        obd_payload=mock_obd_lab.sensor_biased_high(),
    )
    low_rail_payload = mock_obd_lab.sensor_biased_high()
    low_rail_payload["control_module_voltage_v"] = 11.0
    low_rail_request = _make_request(
        session_id=session_id,
        obd_payload=low_rail_payload,
    )

    baseline = LabPipelineAggregator(use_v2_registry=False).process(baseline_request)
    low_rail = LabPipelineAggregator(use_v2_registry=False).process(low_rail_request)

    assert low_rail.model_dump(exclude={"user_input_echo_audit"}) == baseline.model_dump(
        exclude={"user_input_echo_audit"}
    )


@pytest.mark.e2e
def test_vpwr_enabled_full_pipeline_suppresses_sensor_bias():
    """The live aggregator path passes low VPWR into the enabled detector gate."""
    low_rail_payload = mock_obd_lab.sensor_biased_high()
    low_rail_payload["control_module_voltage_v"] = 11.0
    request = _make_request(obd_payload=low_rail_payload)

    result = LabPipelineAggregator(
        use_v2_registry=False,
        enable_vpwr_gate=True,
    ).process(request)

    assert result.performance_analytics.o2_sensor_bias_verdict is None
    assert result.diagnostic_verdict.fault_code != "ERR-SF-001"


# ---------------------------------------------------------------------------
# Precedence: circuit DTC (SF-002) beats perception gap (SF-001)
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_sensor_fault_o2_fixed_voltage_beats_lazy_when_dtc_present():
    """ERR-SF-002 wins over ERR-SF-001 when both routing_tag AND
    perception_flag could fire — circuit DTC earns 0.85 base vs 0.70 base.

    P0134 (O2 circuit fault) + O2_HISTORY tag → SF-002 (0.85 + 0.15 DTC bonus).
    Perception gap is also present (sensor_biased_high), but SF-002 wins on score.
    """
    request = _make_request(
        obd_payload=mock_obd_lab.sensor_biased_high(),
        dtc_payload=_o2_circuit_dtc(),
    )
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(request)

    verdict = result.diagnostic_verdict
    assert verdict.is_fault_detected is True
    assert verdict.fault_code == "ERR-SF-002", (
        "ERR-SF-002 (circuit DTC, 0.85+0.15) should outscore "
        "ERR-SF-001 (perception only, 0.70)"
    )
    assert verdict.fault_family == "sensor_fault"

    # Confidence should be high — both DTC match and perception corroborate
    assert verdict.confidence_score >= 0.85
