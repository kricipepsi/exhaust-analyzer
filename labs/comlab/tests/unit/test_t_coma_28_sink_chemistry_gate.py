"""T-COMA-28 (F-C1-2, F2 half): LC-002 and MF-005 fire only on their own chemistry.

Before, LC-002 fired on `map_kpa < 40` (normal idle vacuum) and MF-005 on `none_present` (no misfire DTC), with no
chemistry match, and took verdicts as sinks. Their chemistry is now GATING.
"""

from __future__ import annotations

import pytest

from registry.integration_shim import RegistryV2Router, _build_observation, _score_rule

FREEZE = {
    "calculated_load_pct": 25.0, "engine_rpm": 800, "coolant_temp_c": 90.0, "short_term_ft1": 0.0,
    "long_term_ft1": 0.0, "manifold_pressure_kpa": 35.0, "vehicle_speed_kmh": 0, "ignition_advance_deg": 10.0,
    "intake_air_temp_c": 30.0, "maf_gps": 3.0, "throttle_pos_pct": 12.0, "fuel_system_status": "CL",
}


@pytest.fixture(scope="module")
def rules():
    return {r.rule_id: r for r in RegistryV2Router().rules}


def _obs(state: str):
    return _build_observation({
        "gas_lab_output": {"chemical_state": state, "sample_validity": "VALID",
                           "gas_hc": 80, "gas_o2": 0.4, "gas_co": 0.3, "gas_co2": 14.8, "gas_nox": 50},
        "dtc_lab_output": {"confirmed_dtcs": [], "routing_tags": [], "freeze_frame": FREEZE},
        "obd_live_data": None,
    })


@pytest.mark.parametrize("state", ["NORMAL_OPERATION", "CAM_TIMING_ADVANCED", "TIMING_RETARDED"])
def test_sinks_do_not_fire_without_their_chemistry(rules, state: str) -> None:
    obs = _obs(state)
    assert _score_rule(rules["LC-002"], obs) is None
    assert _score_rule(rules["MF-005"], obs) is None


def test_lc002_fires_on_lean_chemistry(rules) -> None:
    assert _score_rule(rules["LC-002"], _obs("LEAN_MIXTURE")) is not None


def test_mf005_fires_on_misfire_chemistry_without_dtc(rules) -> None:
    assert _score_rule(rules["MF-005"], _obs("IGNITION_MISFIRE")) is not None


def test_gating_tiers(rules) -> None:
    lc = {c.state.value: c.tier.value for c in rules["LC-002"].chemistry_evidence}
    mf = {c.state.value: c.tier.value for c in rules["MF-005"].chemistry_evidence}
    assert lc == {"LEAN_MIXTURE": "GATING", "TIMING_RETARDED": "SUGGESTIVE"}
    assert mf == {"IGNITION_MISFIRE": "GATING"}
