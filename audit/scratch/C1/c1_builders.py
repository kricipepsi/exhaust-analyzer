"""Minimal request builders for C1 probes (audit evidence only)."""
from __future__ import annotations

import copy
import uuid
from typing import Any

from comlab.schemas.ingestion import OrchestratorInboundRequest

SID = "6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60"  # fixed UUID4 for determinism


def gas(chem: str = "NORMAL_OPERATION", **kw: Any) -> dict:
    d = {
        "chemical_state": chem,
        "gas_co": 0.3, "gas_hc": 80, "gas_co2": 14.8, "gas_o2": 0.4,
        "gas_nox": 50, "lambda_chem": 1.0, "sample_validity": "VALID",
    }
    d.update(kw)
    return d


def obd(**kw: Any) -> dict:
    d = {
        "engine_warmed": True, "total_trim_correction_delta": 0.0,
        "normalized_obd_lambda": 1.0, "ve_pct": 72.0, "ve_validity": "VALID",
        "rpm_state_bucket": "STABILIZED_IDLE", "trim_analytics_gate": "VALID",
        "o2_failure_mode": "NO_FAULT", "maf_status": "REAL_SENSOR_FEED",
        "map_status": "REAL_SENSOR_FEED",
    }
    d.update(kw)
    return d


def ff(**kw: Any) -> dict:
    d = {
        "calculated_load_pct": 25.0, "engine_rpm": 800, "coolant_temp_c": 90.0,
        "short_term_ft1": 0.0, "long_term_ft1": 0.0, "manifold_pressure_kpa": 35.0,
        "vehicle_speed_kmh": 0, "ignition_advance_deg": 10.0,
        "intake_air_temp_c": 30.0, "maf_gps": 3.0, "throttle_pos_pct": 12.0,
        "fuel_system_status": "CL",
    }
    d.update(kw)
    return d


def dtc(confirmed=None, mil=False, flashing=False, tags=None, freeze=None, **kw: Any) -> dict:
    d = {
        "active_mil": mil, "mil_flashing": flashing,
        "confirmed_dtcs": list(confirmed or []), "routing_tags": list(tags or []),
        "historical_fault_context": "UNKNOWN", "freeze_frame": freeze or ff(),
    }
    d.update(kw)
    return d


def request(*, chem: str = "NORMAL_OPERATION", gas_kw=None, obd_kw=None,
            dtc_kw=None, horizon: str = "HORIZON_ADAPTIVE", vin_conf: str = "HIGH",
            symptom=None, include_obd: bool = True, include_dtc: bool = True,
            **top: Any) -> OrchestratorInboundRequest:
    raw = {
        "metadata": {
            "session_id": SID, "vin_dna_string": "WVWZZZ1JZ3W000001",
            "resolved_horizon": horizon, "cylinder_count": 4,
            "vin_confidence": vin_conf,
        },
        "gas_lab_output": gas(chem, **(gas_kw or {})),
        "obd_live_data": obd(**(obd_kw or {})) if include_obd else None,
        "dtc_lab_output": dtc(**(dtc_kw or {})) if include_dtc else None,
        "symptom_dna": symptom if symptom is not None else {
            "environmental_conditions": {"engine_state": "running", "occurs_during": "always"}
        },
    }
    raw.update(top)
    return OrchestratorInboundRequest.model_validate(copy.deepcopy(raw))


def aggregator(**kw: Any):
    from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
    return LabPipelineAggregator(**kw)


def run(req: OrchestratorInboundRequest, **agg_kw: Any):
    """Production-equivalent call: wired.composition does
    LabPipelineAggregator(enable_fatal_gates=False).process(request)."""
    return aggregator(**agg_kw).process(req)
