"""T-COMA-17 (F-C1-13, F-C1-14; ADR-0007 amendment): an INVALID gas sample stays scored but is flagged
LOW_CERTAINTY with reason GAS_SAMPLE_INVALID; EXTERNAL_O2_SUSPECT warns and continues on both paths."""
from __future__ import annotations

import copy
import logging
from typing import Any

import pytest

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest

logging.disable(logging.CRITICAL)

INVALID = "GAS_SAMPLE_INVALID"
O2_SUSPECT = "GAS_SAMPLE_O2_SUSPECT"


def _request(validity: str, *, engine_state: str = "running", horizon: str = "HORIZON_MODERN") -> OrchestratorInboundRequest:
    ff = {
        "calculated_load_pct": 25.0, "engine_rpm": 800, "coolant_temp_c": 90.0,
        "short_term_ft1": 0.0, "long_term_ft1": 0.0, "manifold_pressure_kpa": 35.0,
        "vehicle_speed_kmh": 0, "ignition_advance_deg": 10.0,
        "intake_air_temp_c": 30.0, "maf_gps": 3.0, "throttle_pos_pct": 12.0,
        "fuel_system_status": "CL",
    }
    raw: dict[str, Any] = {
        "metadata": {
            "session_id": "6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60", "vin_dna_string": "WVWZZZ1JZ3W000001",
            "resolved_horizon": horizon, "cylinder_count": 4, "vin_confidence": "HIGH",
        },
        "gas_lab_output": {
            "chemical_state": "RICH_MIXTURE", "gas_co": 0.3, "gas_hc": 80, "gas_co2": 14.8, "gas_o2": 0.4,
            "gas_nox": 50, "lambda_chem": 1.0, "sample_validity": validity,
        },
        "obd_live_data": {
            "engine_warmed": True, "total_trim_correction_delta": 0.0,
            "normalized_obd_lambda": 1.0, "ve_pct": 72.0, "ve_validity": "VALID",
            "rpm_state_bucket": "STABILIZED_IDLE", "trim_analytics_gate": "VALID",
            "o2_failure_mode": "NO_FAULT", "maf_status": "REAL_SENSOR_FEED", "map_status": "REAL_SENSOR_FEED",
        },
        "dtc_lab_output": {
            "active_mil": False, "mil_flashing": False, "confirmed_dtcs": [], "routing_tags": [],
            "historical_fault_context": "UNKNOWN", "freeze_frame": ff,
        },
        "symptom_dna": {"environmental_conditions": {"engine_state": engine_state, "occurs_during": "always"}},
    }
    return OrchestratorInboundRequest.model_validate(copy.deepcopy(raw))


def _meta(validity: str, **kw: Any):
    fatal = kw.pop("fatal", False)
    return LabPipelineAggregator(enable_fatal_gates=fatal).process(_request(validity, **kw)).execution_meta


def _reasons(meta) -> list[str]:
    return [str(r) for r in meta.lab_routing_directive.reasons]


def test_invalid_sample_is_scored_at_low_certainty_with_reason() -> None:
    out = LabPipelineAggregator().process(_request("INVALID"))
    meta = out.execution_meta
    assert meta.degradation_mode != "FATAL_INCOMPLETE"
    assert meta.processing_confidence_rating == "LOW_CERTAINTY"
    assert _reasons(meta) == [INVALID]


@pytest.mark.parametrize("validity, rating, reasons", [
    ("VALID", "HIGH_ASSURANCE", []),
    ("BORDERLINE", "HIGH_ASSURANCE", []),
    ("EXTERNAL_O2_SUSPECT", "HIGH_ASSURANCE", [O2_SUSPECT]),
])
def test_other_validities_keep_the_horizon_rating(validity: str, rating: str, reasons: list[str]) -> None:
    meta = _meta(validity)
    assert meta.processing_confidence_rating == rating
    assert _reasons(meta) == reasons


def test_invalid_sample_still_aborts_with_fatal_gates_on() -> None:
    assert _meta("INVALID", fatal=True).degradation_mode == "FATAL_INCOMPLETE"


def test_o2_suspect_continues_with_fatal_gates_on() -> None:
    meta = _meta("EXTERNAL_O2_SUSPECT", fatal=True)
    assert meta.degradation_mode != "FATAL_INCOMPLETE"
    assert _reasons(meta) == [O2_SUSPECT]


def test_suppressed_gaslab_gets_no_gas_sample_reason() -> None:
    meta = _meta("INVALID", engine_state="will_not_start")
    assert meta.lab_routing_directive.suppress_gaslab is True
    assert INVALID not in _reasons(meta)
