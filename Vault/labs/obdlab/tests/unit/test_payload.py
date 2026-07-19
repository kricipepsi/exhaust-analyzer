"""Tests for OBDLivePayload Pydantic model per OBDLab_KG_Wiki.md §5."""

import pytest
from pydantic import ValidationError

from obdlab.schemas.payload import OBDLivePayload
from obdlab.schemas.vocabulary import (
    FuelSystemStatus,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    RpmStateBucket,
    TrimAnalyticsGate,
    VEValidity,
)

# ── canonical 16-field dict ────────────────────────────────────────────

def _canonical_kwargs(**overrides):
    base = {
        "engine_warmed": True,
        "rpm_state_bucket": RpmStateBucket.STABILIZED_IDLE,
        "engine_rpm": 800,
        "coolant_temp_c": 92.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 30.0,
        "shrtft1": -3.0,
        "longft1": -5.0,
        "shrtft2": None,
        "longft2": None,
        "total_trim_correction_delta": -8.0,
        "normalized_obd_lambda": 1.0,
        "ve_pct": 62.0,
        "ve_validity": VEValidity.VALID,
        "trim_analytics_gate": TrimAnalyticsGate.VALID,
        "maf_status": NodeMAFStatus.REAL_SENSOR_FEED,
        "map_status": NodeMAPStatus.REAL_SENSOR_FEED,
        "o2_failure_mode": O2FailureMode.NO_FAULT,
        "fuel_system_status": FuelSystemStatus.CL,
        "freeze_frame_pids": {},
        "intake_air_temp_c": 25.0,
        "throttle_pos_pct": 15.0,
        "control_module_voltage_v": 14.0,
        "per_cylinder_misfire_counts": None,
    }
    base.update(overrides)
    return base


# ── construction ───────────────────────────────────────────────────────

def test_canonical_construction_round_trip():
    """All fields construct and model_dump round-trips."""
    payload = OBDLivePayload(**_canonical_kwargs())
    dumped = payload.model_dump()
    assert set(dumped.keys()) == {
        "engine_warmed", "rpm_state_bucket", "engine_rpm",
        "coolant_temp_c", "calculated_engine_load_pct",
        "mass_airflow_gps", "manifold_vacuum_kpa",
        "shrtft1", "longft1", "shrtft2", "longft2",
        "total_trim_correction_delta", "total_trim_correction_delta_b2",
        "per_bank_trim_delta",
        "normalized_obd_lambda", "lambda_perception_delta",
        "ve_pct", "ve_validity", "trim_analytics_gate",
        "maf_status", "map_status", "o2_failure_mode",
        "fuel_system_status", "freeze_frame_pids",
        "intake_air_temp_c", "throttle_pos_pct",
        "control_module_voltage_v", "per_cylinder_misfire_counts",
        "ltft_cell_vector", "w_theo", "sensor_error_delta",
    }


def test_model_validate_json_round_trip():
    """model_validate_json round-trips the canonical payload."""
    payload = OBDLivePayload(**_canonical_kwargs())
    json_str = payload.model_dump_json()
    reloaded = OBDLivePayload.model_validate_json(json_str)
    assert reloaded == payload


def test_2_bank_payload():
    """2-bank payload: shrtft2 and longft2 populated."""
    kwargs = _canonical_kwargs(
        shrtft2=-8.0, longft2=-12.0, total_trim_correction_delta=-28.0,
    )
    payload = OBDLivePayload(**kwargs)
    assert payload.shrtft2 == -8.0
    assert payload.longft2 == -12.0


# ── field constraints — positive cases ─────────────────────────────────

def test_engine_rpm_at_boundary():
    """engine_rpm at min (0) and max (8000) are accepted."""
    assert OBDLivePayload(**_canonical_kwargs(engine_rpm=0)).engine_rpm == 0
    assert OBDLivePayload(**_canonical_kwargs(engine_rpm=8000)).engine_rpm == 8000


def test_coolant_temp_c_at_boundary():
    """coolant_temp_c at min (-40) and max (140) accepted."""
    assert OBDLivePayload(**_canonical_kwargs(coolant_temp_c=-40)).coolant_temp_c == -40
    assert OBDLivePayload(**_canonical_kwargs(coolant_temp_c=140)).coolant_temp_c == 140


def test_calculated_engine_load_pct_at_boundary():
    """calculated_engine_load_pct at 0 and 100 accepted."""
    assert OBDLivePayload(**_canonical_kwargs(calculated_engine_load_pct=0)).calculated_engine_load_pct == 0
    assert OBDLivePayload(**_canonical_kwargs(calculated_engine_load_pct=100)).calculated_engine_load_pct == 100


def test_shrtft1_at_boundary():
    """shrtft1 at min (-127) and max (127) accepted (widened OBD-rail bounds)."""
    assert OBDLivePayload(**_canonical_kwargs(shrtft1=-127)).shrtft1 == -127
    assert OBDLivePayload(**_canonical_kwargs(shrtft1=127)).shrtft1 == 127


def test_normalized_obd_lambda_at_boundary():
    """normalized_obd_lambda at 0.7 and 1.3 accepted."""
    assert OBDLivePayload(**_canonical_kwargs(normalized_obd_lambda=0.7)).normalized_obd_lambda == 0.7
    assert OBDLivePayload(**_canonical_kwargs(normalized_obd_lambda=1.3)).normalized_obd_lambda == 1.3


def test_mass_airflow_null_accepted():
    """mass_airflow_gps null (None) is accepted (MAP_ONLY routing)."""
    payload = OBDLivePayload(**_canonical_kwargs(mass_airflow_gps=None))
    assert payload.mass_airflow_gps is None


def test_manifold_vacuum_null_accepted():
    """manifold_vacuum_kpa null (None) is accepted (MAF_ONLY routing)."""
    payload = OBDLivePayload(**_canonical_kwargs(manifold_vacuum_kpa=None))
    assert payload.manifold_vacuum_kpa is None


def test_freeze_frame_pids_defaults_to_empty_dict():
    """freeze_frame_pids defaults to {} when not provided."""
    kwargs = _canonical_kwargs()
    del kwargs["freeze_frame_pids"]
    payload = OBDLivePayload(**kwargs)
    assert payload.freeze_frame_pids == {}


# ── field constraints — negative cases ─────────────────────────────────

def test_engine_rpm_below_zero_rejected():
    """engine_rpm < 0 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(engine_rpm=-1))


def test_engine_rpm_above_8000_rejected():
    """engine_rpm > 8000 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(engine_rpm=8001))


def test_coolant_temp_c_below_minus_40_rejected():
    """coolant_temp_c < -40 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(coolant_temp_c=-41))


def test_coolant_temp_c_above_140_rejected():
    """coolant_temp_c > 140 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(coolant_temp_c=141))


def test_calculated_engine_load_negative_rejected():
    """calculated_engine_load_pct < 0 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(calculated_engine_load_pct=-0.1))


def test_calculated_engine_load_above_100_rejected():
    """calculated_engine_load_pct > 100 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(calculated_engine_load_pct=100.1))


def test_shrtft1_below_minus_127_rejected():
    """shrtft1 < -127 raises ValidationError (widened OBD-rail bounds)."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(shrtft1=-127.1))


def test_shrtft1_above_127_rejected():
    """shrtft1 > 127 raises ValidationError (widened OBD-rail bounds)."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(shrtft1=127.1))


def test_normalized_obd_lambda_below_0_7_rejected():
    """normalized_obd_lambda < 0.7 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(normalized_obd_lambda=0.69))


def test_normalized_obd_lambda_above_1_3_rejected():
    """normalized_obd_lambda > 1.3 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(normalized_obd_lambda=1.31))


def test_mass_airflow_negative_rejected():
    """mass_airflow_gps < 0 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(mass_airflow_gps=-0.1))


def test_manifold_vacuum_negative_rejected():
    """manifold_vacuum_kpa < 0 raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(manifold_vacuum_kpa=-0.1))


# ── o2_failure_mode field ────────────────────────────────────────────

def test_o2_failure_mode_defaults_to_no_fault():
    """o2_failure_mode defaults to NO_FAULT when not provided (field is required)."""
    payload = OBDLivePayload(**_canonical_kwargs())
    assert payload.o2_failure_mode == O2FailureMode.NO_FAULT


def test_o2_failure_mode_stuck_lean_round_trip():
    """o2_failure_mode=STUCK_LEAN round-trips through model_dump_json."""
    payload = OBDLivePayload(**_canonical_kwargs(o2_failure_mode=O2FailureMode.STUCK_LEAN))
    assert payload.o2_failure_mode == O2FailureMode.STUCK_LEAN
    json_str = payload.model_dump_json()
    reloaded = OBDLivePayload.model_validate_json(json_str)
    assert reloaded.o2_failure_mode == O2FailureMode.STUCK_LEAN


def test_ve_validity_unknown_when_analytics_frozen():
    """ve_pct=0.0 + ve_validity=UNKNOWN when analytics frozen (wiki: §10)."""
    payload = OBDLivePayload(**_canonical_kwargs(
        ve_pct=0.0,
        ve_validity=VEValidity.UNKNOWN,
    ))
    assert payload.ve_pct == 0.0
    assert payload.ve_validity == VEValidity.UNKNOWN


# ── intake_air_temp_c & throttle_pos_pct boundaries ───────────────────

def test_iat_and_tps_at_boundaries():
    """intake_air_temp_c and throttle_pos_pct at boundaries are accepted."""
    assert OBDLivePayload(**_canonical_kwargs(intake_air_temp_c=-40)).intake_air_temp_c == -40
    assert OBDLivePayload(**_canonical_kwargs(intake_air_temp_c=140)).intake_air_temp_c == 140
    assert OBDLivePayload(**_canonical_kwargs(throttle_pos_pct=0)).throttle_pos_pct == 0
    assert OBDLivePayload(**_canonical_kwargs(throttle_pos_pct=100)).throttle_pos_pct == 100


def test_iat_out_of_bounds_rejected():
    """intake_air_temp_c out of bounds raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(intake_air_temp_c=-41))
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(intake_air_temp_c=141))


def test_tps_out_of_bounds_rejected():
    """throttle_pos_pct out of bounds raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(throttle_pos_pct=-0.1))
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(throttle_pos_pct=100.1))


# ── control_module_voltage_v boundaries ────────────────────────────────

def test_vpwr_at_boundaries():
    """control_module_voltage_v at boundaries is accepted."""
    assert OBDLivePayload(**_canonical_kwargs(control_module_voltage_v=0.0)).control_module_voltage_v == 0.0
    assert OBDLivePayload(**_canonical_kwargs(control_module_voltage_v=18.0)).control_module_voltage_v == 18.0


def test_vpwr_out_of_bounds_rejected():
    """control_module_voltage_v out of bounds raises ValidationError."""
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(control_module_voltage_v=-0.1))
    with pytest.raises(ValidationError):
        OBDLivePayload(**_canonical_kwargs(control_module_voltage_v=18.1))

