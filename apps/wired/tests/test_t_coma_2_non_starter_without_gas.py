"""T-COMA-2 (T-AUD-4e residual) — a non-starter is diagnosed without exhaust gas readings.

R1 the inbound schema accepts no gas only for will_not_start; R2 the aggregator runs without gas; R3 the composition
skips GASLab for a non-starter with no gas reading, and partial gas still aborts. Tags: NEW fails on the base
fix/T-COMA-2 spec commit; PIN passes there and after.
"""

from __future__ import annotations

import pytest
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from pydantic import ValidationError
from test_t_aud_1a_inputs import DECODABLE_VIN, TRIAGE, _raw

from v7.load_corpus import load_corpus
from wired.composition import diagnose

NON_START = dict(TRIAGE, tier_1="vehicle_starting_issues", tier_2="prolonged_crank_hard_start",
                 engine_state="will_not_start", csv_primary_symptom="non_starter")
METADATA = {"session_id": "11111111-1111-4111-8111-000000000099", "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": "HORIZON_LEGACY", "cylinder_count": 4}


def _gasless(**over) -> dict:
    raw = _raw(vin=DECODABLE_VIN, triage=dict(NON_START), **over)
    raw.pop("gas", None)
    return raw


def test_non_starter_without_gas_abstains_no_rule() -> None:
    """NEW: no gas, no DTC -> the T-COMA-1 NS-NO-RULE abstain, not an abort."""
    res = diagnose(_gasless())
    v = res.diagnostic_verdict
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"
    assert (v.fault_family, v.fault_code, v.abstain_reason) == ("non_starter", "NS-NO-RULE", "no_rule")


def test_non_starter_without_gas_keeps_the_dtc_rule() -> None:
    """NEW: corpus case_006 without its gas -> NS-004 from its DTC, as with gas."""
    raw = dict({cid: r for cid, r, *_ in load_corpus()}["case_006"])
    raw.pop("gas")
    v = diagnose(raw).diagnostic_verdict
    assert (v.fault_family, v.fault_code, v.abstained) == ("non_starter", "NS-004", False)


def test_non_starter_with_partial_gas_aborts() -> None:
    """NEW: partial gas on a non-starter -> the standard GAS_INPUT_INCOMPLETE message naming the missing keys."""
    res = diagnose(_raw(vin=DECODABLE_VIN, triage=dict(NON_START), gas={"hc": 300, "co": 0.5}))
    v = res.diagnostic_verdict
    assert (res.execution_meta.degradation_mode, v.fault_code) == ("FATAL_INCOMPLETE", "GAS_INPUT_INCOMPLETE")
    assert "co2, o2, nox" in v.actionable_remediation and "not available yet" not in v.actionable_remediation


def test_running_without_gas_still_aborts() -> None:
    """PIN: a running engine without gas -> GAS_INPUT_INCOMPLETE naming all five keys."""
    raw = _raw(vin=DECODABLE_VIN)
    raw.pop("gas")
    v = diagnose(raw).diagnostic_verdict
    assert v.fault_code == "GAS_INPUT_INCOMPLETE" and "hc, co, co2, o2, nox" in v.actionable_remediation


def test_request_without_gas_is_refused_for_a_running_engine() -> None:
    """NEW: OrchestratorInboundRequest without gas_lab_output -> ValidationError unless will_not_start."""
    with pytest.raises(ValidationError, match="gas_lab_output is required unless engine_state is will_not_start"):
        OrchestratorInboundRequest.model_validate(
            {"metadata": METADATA, "symptom_dna": {"environmental_conditions": {"engine_state": "running"}}})


def test_request_without_gas_runs_for_a_non_starter() -> None:
    """NEW: the aggregator processes a will_not_start request with no gas_lab_output (both lambda detectors inert)."""
    req = OrchestratorInboundRequest.model_validate(
        {"metadata": METADATA, "symptom_dna": {"environmental_conditions": {"engine_state": "will_not_start"}}})
    res = LabPipelineAggregator().process(req)
    assert res.diagnostic_verdict.fault_code == "NS-NO-RULE"
    assert res.performance_analytics.lambda_perception_delta == 0.0
    assert res.performance_analytics.o2_sensor_bias_verdict is None
