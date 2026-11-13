"""Unit tests for Script 2 (LabPipelineAggregator).

v0.1 skeleton.
"""

from __future__ import annotations

import pytest

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator


def test_aggregator_accepts_valid_payload(hpfp_leak_payload):
    agg = LabPipelineAggregator()
    out = agg.validate_payload(hpfp_leak_payload)
    assert out["metadata"]["cylinder_count"] == 4


def test_aggregator_rejects_malformed_dtc(hpfp_leak_payload):
    hpfp_leak_payload["dtc_lab_output"]["confirmed_dtcs"] = ["invalid_p0302"]
    agg = LabPipelineAggregator()
    with pytest.raises(Exception):  # pydantic.ValidationError
        agg.validate_payload(hpfp_leak_payload)


def test_aggregator_smoke():
    LabPipelineAggregator()
