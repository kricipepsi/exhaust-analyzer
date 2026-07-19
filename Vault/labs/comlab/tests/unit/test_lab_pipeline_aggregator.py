"""Unit tests for Script 2 (LabPipelineAggregator).

v0.1 skeleton.
"""

from __future__ import annotations

import pytest

from comlab.core.lab_pipeline_aggregator import (
    LabPipelineAggregator,
    DegradationMode,
    AggregatorAbort,
)


@pytest.mark.skip(reason="phase 3: implement Pydantic validation")
def test_aggregator_accepts_valid_payload(hpfp_leak_payload):
    agg = LabPipelineAggregator()
    out = agg.validate_payload(hpfp_leak_payload)
    assert out["metadata"]["cylinder_count"] == 4


@pytest.mark.skip(reason="phase 3: implement DTC regex validator")
def test_aggregator_rejects_malformed_dtc(hpfp_leak_payload):
    hpfp_leak_payload["dtc_lab_output"]["confirmed_dtcs"] = ["invalid_p0302"]
    agg = LabPipelineAggregator()
    with pytest.raises(Exception):  # pydantic.ValidationError
        agg.validate_payload(hpfp_leak_payload)


@pytest.mark.skip(reason="phase 3: implement fallback tree")
def test_modern_vehicle_missing_trims_aborts(hpfp_leak_payload):
    del hpfp_leak_payload["obd_live_data"]["shrtft1"]
    del hpfp_leak_payload["obd_live_data"]["longft1"]
    agg = LabPipelineAggregator()
    with pytest.raises(AggregatorAbort) as excinfo:
        agg.sanitize_and_aggregate(hpfp_leak_payload)
    assert excinfo.value.error_code == "ERR-ABORT-003"


@pytest.mark.skip(reason="phase 3: implement legacy graceful degradation")
def test_legacy_vehicle_missing_trims_degrades_to_gas_dominant(hpfp_leak_payload):
    hpfp_leak_payload["metadata"]["resolved_horizon"] = "HORIZON_LEGACY"
    del hpfp_leak_payload["obd_live_data"]["shrtft1"]
    del hpfp_leak_payload["obd_live_data"]["longft1"]
    agg = LabPipelineAggregator()
    out = agg.sanitize_and_aggregate(hpfp_leak_payload)
    assert out["metadata"]["degradation_mode"] == DegradationMode.GAS_DOMINANT


def test_aggregator_smoke():
    LabPipelineAggregator()
