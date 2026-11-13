"""T-COMA-20 (F-C1-16): the v1 path (USE_V2_REGISTRY=0) gives a verdict when DTCLab output is absent."""
from __future__ import annotations

import copy
import logging

import pytest
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest

logging.disable(logging.CRITICAL)


def _request(chem: str) -> OrchestratorInboundRequest:
    raw = {
        "metadata": {
            "session_id": "6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60", "vin_dna_string": "WVWZZZ1JZ3W000001",
            "resolved_horizon": "HORIZON_ADAPTIVE", "cylinder_count": 4, "vin_confidence": "HIGH",
        },
        "gas_lab_output": {
            "chemical_state": chem, "gas_co": 0.3, "gas_hc": 80, "gas_co2": 14.8, "gas_o2": 0.4,
            "gas_nox": 50, "lambda_chem": 1.0, "sample_validity": "VALID",
        },
        "obd_live_data": {
            "engine_warmed": True, "total_trim_correction_delta": 0.0,
            "normalized_obd_lambda": 1.0, "ve_pct": 72.0, "ve_validity": "VALID",
            "rpm_state_bucket": "STABILIZED_IDLE", "trim_analytics_gate": "VALID",
            "o2_failure_mode": "NO_FAULT", "maf_status": "REAL_SENSOR_FEED", "map_status": "REAL_SENSOR_FEED",
        },
        "dtc_lab_output": None,
        "symptom_dna": {"environmental_conditions": {"engine_state": "running", "occurs_during": "always"}},
    }
    return OrchestratorInboundRequest.model_validate(copy.deepcopy(raw))


@pytest.mark.parametrize("chem", ["RICH_MIXTURE", "LEAN_MIXTURE", "NORMAL_OPERATION"])
def test_v1_path_without_dtc_output_gives_a_verdict(chem: str) -> None:
    out = LabPipelineAggregator(use_v2_registry=False).process(_request(chem))
    assert out.diagnostic_verdict.fault_code
    assert out.execution_meta.degradation_mode != "FATAL_INCOMPLETE"
