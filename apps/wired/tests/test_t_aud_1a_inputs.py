"""T-AUD-1a — wired.diagnose never raises on missing triage, gas, OBD or freeze-frame input.

A missing required input returns COMLab's ``abort_incomplete`` verdict
(``FATAL_INCOMPLETE`` / ``invalid_input``) with the missing fields named.
Rulings R2-R5 of the task; K1-K2 of plan correction 01. Tags: NEW fails on the
base ``audit-r2`` commit; PIN passes there and after.
"""

from __future__ import annotations

from typing import Any

import pytest

from wired.composition import diagnose

DECODABLE_VIN = "WME01MC01XH072806"  # vinlab: PARTIAL, HORIZON_LEGACY (the fallback DNA is MODERN)
TRIAGE = {
    "tier_1": "lack_of_power_hesitation",
    "tier_2": "flat_sluggish_always",
    "occurs_during": "always",
    "engine_state": "running",
    "load_state": "idle",
}
GAS = {"hc": 80, "co": 0.3, "co2": 14.8, "o2": 0.3, "nox": 50, "engine_state": "STABILIZED_IDLE"}
OBD = {
    "pid_oxygen_sensor_volts": 0.45,
    "shrtft1": 1.0,
    "longft1": 2.0,
    "engine_rpm": 800,
    "coolant_temp_c": 90.0,
    "number_of_banks": 1,
    "shrtft2": None,
    "longft2": None,
}


def _raw(**over: Any) -> dict[str, Any]:
    raw: dict[str, Any] = {"vin": "UNKNOWNVIN0000000", "triage": dict(TRIAGE), "gas": dict(GAS)}
    raw.update(over)
    return raw


def _assert_abort(res, code: str, *named: str) -> None:
    v = res.diagnostic_verdict
    assert res.execution_meta.degradation_mode == "FATAL_INCOMPLETE"
    assert v.fault_family == "invalid_input"
    assert v.fault_code == code
    for name in named:
        assert name in v.actionable_remediation


# --- R2: absent or incomplete triage is the absent-symptom case ------------------


def test_r2_absent_triage_decodes_vin() -> None:
    """NEW: no triage, decodable VIN -> the VIN is still decoded and the run continues."""
    raw = _raw(vin=DECODABLE_VIN)
    del raw["triage"]
    res = diagnose(raw)
    assert res.execution_meta.resolved_horizon == "HORIZON_LEGACY"
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"


def test_r2_incomplete_triage_runs_without_symptom() -> None:
    """NEW: Tier 1 only -> no SymptomValidationError; empty symptom_dna."""
    res = diagnose(_raw(vin=DECODABLE_VIN, triage={"tier_1": "lack_of_power_hesitation"}))
    assert res.execution_meta.resolved_horizon == "HORIZON_LEGACY"


def test_r2_blank_triage_value_runs_without_symptom() -> None:
    """NEW (correction C8): all five keys present, one blank -> the empty-symptom path."""
    res = diagnose(_raw(vin=DECODABLE_VIN, triage=dict(TRIAGE, tier_2="")))
    assert res.execution_meta.resolved_horizon == "HORIZON_LEGACY"


def test_r2_undecodable_vin_keeps_fallback() -> None:
    """PIN: VINDecodeError keeps the _build_fallback_vin_dna path."""
    res = diagnose(_raw())
    assert res.execution_meta.resolved_horizon == "HORIZON_MODERN"
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"


def test_k1_validate_triage() -> None:
    """NEW (correction K1): public validate_triage returns the error message or None."""
    from wired import validate_triage

    assert validate_triage(TRIAGE) is None
    bad = validate_triage(dict(TRIAGE, tier_1="vehicle_starting_issues"))
    assert bad is not None and "vehicle_starting_issues" in bad
    assert validate_triage({"tier_1": "lack_of_power_hesitation"}) is None


def test_k2_triage_keys_match_dnalab() -> None:
    """PIN (correction K2): _TRIAGE_KEYS equals dnalab's required triage keys."""
    from dnalab import build_vehicle_dna
    from symptomlab import SymptomValidationError

    from wired.composition import _TRIAGE_KEYS

    with pytest.raises(SymptomValidationError) as exc:
        build_vehicle_dna(DECODABLE_VIN, {})
    assert str(list(_TRIAGE_KEYS)) in str(exc.value)


def test_k2_freeze_frame_keys_match_dtclab() -> None:
    """PIN (correction K2): _FREEZE_FRAME_KEYS equals DTCLab's _MANDATORY_PIDS."""
    from dtclab.core.freeze_frame_extractor import _MANDATORY_PIDS

    from wired.composition import _FREEZE_FRAME_KEYS

    assert _FREEZE_FRAME_KEYS == _MANDATORY_PIDS


# --- R3 / R4: low-idle gas ------------------------------------------------------


@pytest.mark.parametrize("key", ["hc", "co", "co2", "o2", "nox"])
def test_r3_missing_low_idle_gas_aborts(key: str) -> None:
    """NEW: one low-idle gas value absent -> GAS_INPUT_INCOMPLETE naming it, no KeyError."""
    gas = dict(GAS)
    del gas[key]
    _assert_abort(diagnose(_raw(gas=gas)), "GAS_INPUT_INCOMPLETE", key)


def test_r3_gas_absent_aborts() -> None:
    """NEW: no gas dict at all -> GAS_INPUT_INCOMPLETE naming all five."""
    raw = _raw()
    del raw["gas"]
    _assert_abort(diagnose(raw), "GAS_INPUT_INCOMPLETE", "hc", "co", "co2", "o2", "nox")


def test_r3_partial_high_idle_is_ignored() -> None:
    """PIN: high idle stays all-or-nothing; a partial set runs as low idle only."""
    res = diagnose(_raw(gas=dict(GAS, hc_high=60)))
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"


def test_r4_non_starter_without_gas_aborts_with_message() -> None:
    """NEW: non-starter, GASLab unticked -> GAS_INPUT_INCOMPLETE; non-start without gas is not available yet."""
    raw = _raw(
        vin=DECODABLE_VIN,
        triage=dict(
            TRIAGE,
            tier_1="vehicle_starting_issues",
            tier_2="prolonged_crank_hard_start",
            engine_state="will_not_start",
        ),
    )
    del raw["gas"]
    res = diagnose(raw)
    _assert_abort(res, "GAS_INPUT_INCOMPLETE", "hc")
    assert "not available yet" in res.diagnostic_verdict.actionable_remediation


# --- R5: OBD and freeze frame ---------------------------------------------------


@pytest.mark.parametrize(
    "key", ["pid_oxygen_sensor_volts", "shrtft1", "longft1", "engine_rpm", "coolant_temp_c"]
)
def test_r5_partial_obd_aborts(key: str) -> None:
    """NEW: one of the 5 required OBD fields absent -> OBD_INPUT_INCOMPLETE naming it."""
    obd = dict(OBD)
    del obd[key]
    _assert_abort(diagnose(_raw(obd=obd)), "OBD_INPUT_INCOMPLETE", key)


def test_r5_complete_obd_runs() -> None:
    """PIN: the 5 required OBD fields typed -> the run continues."""
    res = diagnose(_raw(obd=dict(OBD)))
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"


def test_r5_two_bank_obd_needs_bank2_trims() -> None:
    """NEW: number_of_banks == 2 and no bank-2 trims -> OBD_INPUT_INCOMPLETE, no PIDValidationError."""
    _assert_abort(
        diagnose(_raw(obd=dict(OBD, number_of_banks=2))), "OBD_INPUT_INCOMPLETE", "shrtft2", "longft2"
    )


def test_r5_wideband_obd_needs_equivalence_ratio() -> None:
    """NEW: a WIDEBAND_LINEAR car needs pid_wideband_equivalence_ratio, not the narrowband volts."""
    from wired.composition import _build_fallback_vin_dna, _obd_required_keys

    vin_dna = _build_fallback_vin_dna("")
    assert _obd_required_keys(OBD, vin_dna)[0] == "pid_oxygen_sensor_volts"
    vin_dna["emissions"]["upstream_o2_type"] = "WIDEBAND_LAMBDA"
    assert _obd_required_keys(OBD, vin_dna)[0] == "pid_wideband_equivalence_ratio"


def test_r5_obd_lab_needs_o2_key() -> None:
    """PIN (correction C5): OBDLab raises without the O2 key (the measurement behind the engine check)."""
    from obdlab import SensorSignalTranslator

    from wired.composition import _build_fallback_vin_dna, _build_obd_dna_view

    obd = dict(OBD)
    del obd["pid_oxygen_sensor_volts"]
    with pytest.raises(Exception, match="pid_oxygen_sensor_volts"):
        SensorSignalTranslator().translate(obd, _build_obd_dna_view(_build_fallback_vin_dna("")))


def test_r5_dtc_without_freeze_frame_aborts() -> None:
    """NEW: a confirmed code with no freeze frame -> FREEZE_FRAME_INCOMPLETE naming the missing PIDs."""
    dtc = {"raw_dtcs": {"$03": ["P0171"]}, "codes_cleared": False}
    _assert_abort(
        diagnose(_raw(dtc=dtc)), "FREEZE_FRAME_INCOMPLETE", "calculated_load_pct", "fuel_system_status"
    )
