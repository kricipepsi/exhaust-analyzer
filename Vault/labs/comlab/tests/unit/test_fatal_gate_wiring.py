"""Stage-A fatal gate wiring tests — process() integration.

Tests that ``enable_fatal_gates`` on ``LabPipelineAggregator`` gates the
``process()`` path: flag-off is byte-identical to baseline, flag-on aborts
with ``FATAL_INCOMPLETE`` on each ``ERR-ABORT-00x`` condition, and flag-on
healthy requests proceed normally.

Source: T-COMV2-FATAL-1.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest


# ---------------------------------------------------------------------------
# Helper — local copy of _minimal_valid_payload (canonical in tests/e2e/test_error_codes.py)
# ---------------------------------------------------------------------------

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _session_id() -> str:
    return str(uuid4())


def _minimal_valid_payload() -> dict:
    """Return a dict that passes ``OrchestratorInboundRequest`` validation."""
    sid = _session_id()
    return {
        "metadata": {
            "session_id": sid,
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": "HORIZON_MODERN",
            "cylinder_count": 4,
        },
        "gas_lab_output": {
            "chemical_state": "NORMAL_OPERATION",
            "gas_co": 0.5,
            "gas_hc": 50,
            "gas_co2": 14.0,
            "gas_o2": 1.0,
            "gas_nox": 200,
            "lambda_chem": 1.0,
            "sample_validity": "VALID",
        },
        "obd_live_data": {
            "engine_warmed": True,
            "total_trim_correction_delta": -5.0,
            "ve_pct": 75.0,
            "ve_validity": "VALID",
            "rpm_state_bucket": "STABILIZED_IDLE",
            "trim_analytics_gate": "VALID",
            "o2_failure_mode": "STUCK_LEAN",
            "maf_status": "REAL_SENSOR_FEED",
            "map_status": "REAL_SENSOR_FEED",
        },
        "dtc_lab_output": {
            "active_mil": False,
            "mil_flashing": False,
            "confirmed_dtcs": [],
            "pending_dtcs": [],
            "permanent_dtcs": [],
            "routing_tags": [],
            "mode_06_monitors": {},
            "historical_fault_context": "UNKNOWN",
            "freeze_frame": {
                "fuel_system_status": "CL",
                "engine_rpm": 750,
                "vehicle_speed_kmh": 0,
                "coolant_temp_c": 90.0,
                "intake_air_temp_c": 25.0,
                "throttle_pos_pct": 5.0,
                "calculated_load_pct": 20.0,
                "maf_gps": 3.5,
                "manifold_pressure_kpa": 30.0,
                "short_term_ft1": -3.0,
                "long_term_ft1": -5.0,
                "ignition_advance_deg": 10.0,
                "o2_voltage_b1s1": 0.45,
            },
        },
        "symptom_dna": {},
    }


# ===================================================================
# Flag-off — inert (byte-identical to baseline)
# ===================================================================

def test_fatal_gates_inert_when_off() -> None:
    """Flag-off: invalid sample, cold engine, and VIN NONE each produce a normal
    (non-FATAL_INCOMPLETE) verdict — gates are inert."""
    # Invalid sample
    invalid_payload = _minimal_valid_payload()
    invalid_payload["gas_lab_output"]["sample_validity"] = "INVALID"
    invalid_request = OrchestratorInboundRequest.model_validate(invalid_payload)
    flag_off_invalid = LabPipelineAggregator().process(invalid_request)
    assert flag_off_invalid.execution_meta.degradation_mode != "FATAL_INCOMPLETE"

    # Cold engine
    cold_payload = _minimal_valid_payload()
    cold_payload["obd_live_data"]["engine_warmed"] = False
    cold_request = OrchestratorInboundRequest.model_validate(cold_payload)
    flag_off_cold = LabPipelineAggregator().process(cold_request)
    assert flag_off_cold.execution_meta.degradation_mode != "FATAL_INCOMPLETE"

    # VIN NONE
    vin_payload = _minimal_valid_payload()
    vin_payload["metadata"]["vin_confidence"] = "NONE"
    vin_request = OrchestratorInboundRequest.model_validate(vin_payload)
    flag_off_vin = LabPipelineAggregator().process(vin_request)
    assert flag_off_vin.execution_meta.degradation_mode != "FATAL_INCOMPLETE"


# ===================================================================
# Flag-on — each ERR-ABORT-00x → FATAL_INCOMPLETE
# ===================================================================

def test_fatal_gate_sample_invalid() -> None:
    """Flag-on: sample_validity=INVALID → FATAL_INCOMPLETE with ERR-ABORT-001."""
    payload = _minimal_valid_payload()
    payload["gas_lab_output"]["sample_validity"] = "INVALID"
    request = OrchestratorInboundRequest.model_validate(payload)

    result = LabPipelineAggregator(enable_fatal_gates=True).process(request)

    assert result.execution_meta.degradation_mode == "FATAL_INCOMPLETE"
    assert result.diagnostic_verdict.fault_code == "ERR-ABORT-001"
    assert result.diagnostic_verdict.fault_family == "invalid_input"
    assert "probe" in result.diagnostic_verdict.actionable_remediation.lower()


def test_fatal_gate_engine_not_warmed() -> None:
    """Flag-on: engine_warmed=False → FATAL_INCOMPLETE with ERR-ABORT-002."""
    payload = _minimal_valid_payload()
    payload["obd_live_data"]["engine_warmed"] = False
    request = OrchestratorInboundRequest.model_validate(payload)

    result = LabPipelineAggregator(enable_fatal_gates=True).process(request)

    assert result.execution_meta.degradation_mode == "FATAL_INCOMPLETE"
    assert result.diagnostic_verdict.fault_code == "ERR-ABORT-002"
    assert result.diagnostic_verdict.fault_family == "invalid_input"
    assert "temperature" in result.diagnostic_verdict.actionable_remediation.lower()


def test_fatal_gate_vin_none() -> None:
    """Flag-on: vin_confidence=NONE → FATAL_INCOMPLETE with ERR-ABORT-004."""
    payload = _minimal_valid_payload()
    payload["metadata"]["vin_confidence"] = "NONE"
    request = OrchestratorInboundRequest.model_validate(payload)

    result = LabPipelineAggregator(enable_fatal_gates=True).process(request)

    assert result.execution_meta.degradation_mode == "FATAL_INCOMPLETE"
    assert result.diagnostic_verdict.fault_code == "ERR-ABORT-004"
    assert result.diagnostic_verdict.fault_family == "invalid_input"
    assert "VIN" in result.diagnostic_verdict.actionable_remediation


# ===================================================================
# Flag-on — healthy request unchanged
# ===================================================================

def test_fatal_gates_healthy_unchanged() -> None:
    """Flag-on: valid request → same degradation_mode and fault_code as flag-off."""
    valid_payload = _minimal_valid_payload()
    valid_request = OrchestratorInboundRequest.model_validate(valid_payload)

    flag_off = LabPipelineAggregator().process(valid_request)
    flag_on = LabPipelineAggregator(enable_fatal_gates=True).process(valid_request)

    assert flag_on.execution_meta.degradation_mode == flag_off.execution_meta.degradation_mode
    assert flag_on.diagnostic_verdict.fault_code == flag_off.diagnostic_verdict.fault_code
    assert flag_on.execution_meta.degradation_mode != "FATAL_INCOMPLETE"
