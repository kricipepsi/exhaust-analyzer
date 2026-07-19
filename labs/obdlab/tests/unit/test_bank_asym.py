"""Unit tests for T-OBDV2-BANK-ASYM-1 (per-bank trim delta and emitter discipline)."""


from obdlab.core.sensor_signal_translator import SensorSignalTranslator
from obdlab.schemas.payload import OBDLivePayload


def _warm_idle_input(**overrides):
    """Return a valid raw user input dict for warm steady idle tests."""
    base = {
        "engine_rpm": 800,
        "coolant_temp_c": 92.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 30.0,
        "intake_air_temp_c": 35.0,
        "shrtft1": -3.0,
        "longft1": -5.0,
        "number_of_banks": 1,
        "fuel_sys_status": "Closed_Loop",
        "pid_oxygen_sensor_volts": 0.45,
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }
    base.update(overrides)
    return base


def test_single_bank_trim_delta_is_none():
    """Single-bank engines must emit None for per_bank_trim_delta."""
    translator = SensorSignalTranslator()

    inp = _warm_idle_input(
        shrtft1=-2.0,
        longft1=5.0,
        number_of_banks=1,
    )
    payload = translator.translate(inp)

    assert payload.total_trim_correction_delta == 3.0
    assert payload.total_trim_correction_delta_b2 is None
    assert payload.per_bank_trim_delta is None


def test_v_engine_trim_delta_is_float():
    """V-engines (2-bank) must compute B1 - B2 as a signed float."""
    translator = SensorSignalTranslator()

    inp = _warm_idle_input(
        shrtft1=-2.0,
        longft1=5.0,
        shrtft2=4.0,
        longft2=-1.0,
        number_of_banks=2,
    )
    payload = translator.translate(inp)

    # B1 total = -2.0 + 5.0 = 3.0
    # B2 total = 4.0 + -1.0 = 3.0
    # delta = B1 - B2 = 3.0 - 3.0 = 0.0
    assert payload.total_trim_correction_delta == 3.0
    assert payload.total_trim_correction_delta_b2 == 3.0
    assert payload.per_bank_trim_delta == 0.0

    # With different values to test signed difference
    inp_diff = _warm_idle_input(
        shrtft1=10.0,
        longft1=5.0,  # B1 = 15.0
        shrtft2=-2.0,
        longft2=1.0,   # B2 = -1.0
        number_of_banks=2,
    )
    payload_diff = translator.translate(inp_diff)
    assert payload_diff.total_trim_correction_delta == 15.0
    assert payload_diff.total_trim_correction_delta_b2 == -1.0
    assert payload_diff.per_bank_trim_delta == 16.0  # 15.0 - (-1.0) = 16.0


def test_emitter_only_discipline():
    """OBDLab must not emit any bank-asymmetry verdict or fault labels."""
    forbidden_fields = {
        "bank_asym",
        "asymmetry_verdict",
        "fault_family",
        "FaultFamily"
    }

    for field in forbidden_fields:
        assert field not in OBDLivePayload.model_fields, f"OBDLivePayload contains forbidden field: {field}"
