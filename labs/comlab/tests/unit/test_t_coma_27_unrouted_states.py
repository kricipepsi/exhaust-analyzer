"""T-COMA-27 (F-C1-2): every GASLab chemical state with a REG-V2 rule routes to that rule, not to a sink.

Each rule added by T-COMA-27 names `UNIT-COMA27-<STATE>` in `passes_cases`; this file is the case that executes it.
The family is GASLab's own (`labs/gaslab/gaslab/family_map.py`). FLAT_CAMSHAFT and INCOMPLETE_OXIDATION stay
unrouted by ruling: their corpus labels do not match the GASLab family.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from tests.fixtures import mock_dtc_lab, mock_gas_lab, mock_obd_lab

ROUTED = {  # state -> (rule, family)
    "CAM_TIMING_RETARDED_MAP": ("CT-009", "cam_timing"),
    "CAM_TIMING_ADVANCED": ("CT-010", "cam_timing"),
    "EGR_DILUTION_MISFIRE": ("MF-007", "misfire"),
    "EGR_STUCK_OPEN": ("MF-008", "misfire"),
    "EGR_STUCK_CLOSED": ("LC-004", "lean_condition"),
    "HIGH_COMBUSTION_TEMP": ("LC-005", "lean_condition"),
    "EVAP_CANISTER_SATURATED": ("RM-005", "rich_mixture"),
    "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE": ("RM-006", "rich_mixture"),
    "GDI_INTAKE_VALVE_CARBON": ("MW-010", "mechanical_wear"),
    "TIMING_OVER_ADVANCED": ("IF-004", "ignition_fault"),
}


# The F-C1-2 probe's gas numbers (audit/scratch/C1/c1_builders.py `gas`): CO 0.3 % sits outside NF-001's clean band,
# so the no-fault rules stay out and the contest is the new rule against the LC-002 / MF-005 sinks.
PROBE_GAS = {"gas_co": 0.3, "gas_hc": 80, "gas_co2": 14.8, "gas_o2": 0.4, "gas_nox": 50, "lambda_chem": 1.0}


def _request(state: str, *, with_obd_dtc: bool = True) -> OrchestratorInboundRequest:
    gas = mock_gas_lab.warm_idle_baseline() | PROBE_GAS | {"chemical_state": state}
    return OrchestratorInboundRequest.model_validate({
        "metadata": {
            "session_id": str(uuid4()),
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": "HORIZON_MODERN",
            "cylinder_count": 4,
        },
        "gas_lab_output": gas,
        "obd_live_data": mock_obd_lab.warm_idle_baseline() if with_obd_dtc else None,
        "dtc_lab_output": mock_dtc_lab.no_codes() if with_obd_dtc else None,
        "symptom_dna": {},
    })


@pytest.mark.parametrize("with_obd_dtc", [True, False])
@pytest.mark.parametrize("state", sorted(ROUTED))
def test_state_routes_to_its_rule(state: str, with_obd_dtc: bool) -> None:
    rule, family = ROUTED[state]
    verdict = LabPipelineAggregator().process(_request(state, with_obd_dtc=with_obd_dtc)).diagnostic_verdict
    assert (verdict.fault_code, verdict.fault_family) == (rule, family)


def test_each_new_rule_names_its_unit_case() -> None:
    from registry.integration_shim import RegistryV2Router

    rules = {r.rule_id: r for r in RegistryV2Router().rules}
    for state, (rule, _family) in ROUTED.items():
        assert rules[rule].passes_cases == [f"UNIT-COMA27-{state}"]
        assert [c.state.value for c in rules[rule].chemistry_evidence] == [state]
