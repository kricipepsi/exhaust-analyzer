"""T-COMA-8 (F-C1-9): both ExecutionMeta builders in LabPipelineAggregator.process echo metadata.vin_confidence.

Tags: NEW fails on the base (both sites hard-coded "HIGH").
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from tests.fixtures import mock_dtc_lab, mock_gas_lab, mock_obd_lab


def _request(vin_confidence: str) -> OrchestratorInboundRequest:
    return OrchestratorInboundRequest.model_validate({
        "metadata": {
            "session_id": str(uuid4()),
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": "HORIZON_MODERN",
            "cylinder_count": 4,
            "vin_confidence": vin_confidence,
        },
        "gas_lab_output": mock_gas_lab.warm_idle_baseline(),
        "obd_live_data": mock_obd_lab.warm_idle_baseline(),
        "dtc_lab_output": mock_dtc_lab.no_codes(),
        "symptom_dna": {},
    })


@pytest.mark.parametrize("fault_code", [None, "ERR-RM-001"])  # the routed path and the fault_code path
def test_partial_decode_is_echoed_on_both_paths(fault_code):
    """NEW: a PARTIAL decode reads PARTIAL in execution_meta, whichever ExecutionMeta builder runs."""
    out = LabPipelineAggregator(enable_fatal_gates=False).process(_request("PARTIAL"), fault_code=fault_code)
    assert out.execution_meta.degradation_mode != "FATAL_INCOMPLETE"
    assert out.execution_meta.vin_confidence == "PARTIAL"
