"""C1 probes: healthy car / unrouted chemistry routed to sink rules (REG-V2 default path).

Each test asserts the CLAIM; a failure is the observation that refutes it.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from c1_builders import ff, request, run

logging.disable(logging.CRITICAL)

RULES_DIR = Path(__file__).resolve().parents[3] / "labs/comlab/registry/rules"


def _rule_chem_refs() -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    for f in sorted(RULES_DIR.glob("*.json")):
        for r in json.loads(f.read_text())["rules"]:
            for e in r.get("chemistry_evidence", []):
                refs.setdefault(e["state"], []).append(r["rule_id"])
    return refs


# --- F1: a healthy car is diagnosed with a fault ---------------------------------

def test_healthy_car_normal_chemistry_is_not_a_fault():
    """NORMAL_OPERATION chemistry, lambda 1.00, trims 0, no DTCs, idle MAP 35 kPa,
    HC 80 ppm (inside ADAPTIVE gas_hc_max_ppm 200). ADR-0007: chemistry is ground truth."""
    out = run(request(chem="NORMAL_OPERATION"))
    v = out.diagnostic_verdict
    print("verdict:", v.fault_code, v.fault_family, v.confidence_score, v.is_fault_detected,
          out.performance_analytics.severity_level)
    assert v.fault_family == "no_fault" or not v.is_fault_detected


def test_healthy_car_without_dtc_lab_is_not_a_fault():
    out = run(request(chem="NORMAL_OPERATION", include_dtc=False, include_obd=False))
    v = out.diagnostic_verdict
    print("verdict:", v.fault_code, v.fault_family, v.confidence_score, v.is_fault_detected)
    assert v.fault_family == "no_fault" or not v.is_fault_detected


def test_mechanism_lc002_and_mf005_fire_on_normal_values_only():
    """Show WHICH evidence fires the sink rules: map_kpa<40 (normal idle vacuum) for LC-002
    and DTC 'none_present' (no misfire code at all) for MF-005 — no chemistry match."""
    from registry.integration_shim import RegistryV2Router, _build_observation, _score_rule
    router = RegistryV2Router()
    rules = {r.rule_id: r for r in router.rules}
    payload = {
        "gas_lab_output": {"chemical_state": "NORMAL_OPERATION", "sample_validity": "VALID",
                           "gas_hc": 80, "gas_o2": 0.4, "gas_co": 0.3, "gas_co2": 14.8, "gas_nox": 50},
        "dtc_lab_output": {"confirmed_dtcs": [], "routing_tags": [], "freeze_frame": ff()},
        "obd_live_data": None,
    }
    obs = _build_observation(payload)
    lc002 = _score_rule(rules["LC-002"], obs)
    mf005 = _score_rule(rules["MF-005"], obs)
    print("LC-002 score:", lc002, "MF-005 score:", mf005, "map_kpa:", obs.obd_pids["map_kpa"])
    # Claim (LC-002/MF-005 descriptions): LC-002 needs lean chemistry, MF-005 needs misfire chemistry.
    assert lc002 is None and mf005 is None


# --- F2: GASLab chemical states with no REG-V2 consumer ---------------------------

UNROUTED_EXPECTED_FAMILY = {
    # state -> family its own vocabulary comment / GAS_VOCABULARY names
    "CAM_TIMING_RETARDED_MAP": "cam_timing",
    "CAM_TIMING_ADVANCED": "cam_timing",
    "EGR_STUCK_OPEN": None,
    "EGR_STUCK_CLOSED": None,
    "EGR_DILUTION_MISFIRE": "misfire",
    "INCOMPLETE_OXIDATION": None,
    "HIGH_COMBUSTION_TEMP": None,
    "TIMING_OVER_ADVANCED": None,
    "FLAT_CAMSHAFT": None,
    "GDI_INTAKE_VALVE_CARBON": None,
    "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE": None,
    "EVAP_CANISTER_SATURATED": None,
}


def test_every_chemical_signature_has_a_v2_rule():
    from comlab.schemas.vocabulary import ChemicalSignature
    refs = _rule_chem_refs()
    unrouted = sorted(c.value for c in ChemicalSignature if c.value not in refs)
    print("unrouted chemical states:", len(unrouted), unrouted)
    assert unrouted == []


@pytest.mark.parametrize("chem", sorted(UNROUTED_EXPECTED_FAMILY))
def test_unrouted_state_does_not_fall_into_sink_rule(chem):
    out = run(request(chem=chem))
    v = out.diagnostic_verdict
    print(chem, "->", v.fault_code, v.fault_family, round(v.confidence_score, 3))
    # Claim: the verdict is derived from the chemistry (ADR-0007), not from a rule whose
    # chemistry evidence the case does not satisfy.
    assert v.fault_code not in {"LC-002", "MF-005"}
