"""Unit tests for MAF linearity calculations and translator integration."""

import math

from obdlab.core.maf_linearity import calculate_sensor_error_delta, calculate_w_theo
from obdlab.core.sensor_signal_translator import (
    LinearityAccumulator,
    SensorSignalTranslator,
)
from obdlab.schemas.dna_view import (
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)


def _dna_view(strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK):
    return ObdLabDnaView(
        engine_displacement_liters=2.0,  # wiki: research/chunks/pids-protocol/05
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=strategy,
        upstream_o2_type=O2SensorType.NARROWBAND_0_TO_1V,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )



def _warm_idle_input(**overrides):
    base = {
        "engine_rpm": 750,  # wiki: research/chunks/pids-protocol/05
        "coolant_temp_c": 92.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 2.85,  # wiki: research/chunks/pids-protocol/05
        "manifold_vacuum_kpa": 30.0,  # wiki: research/chunks/pids-protocol/05
        "intake_air_temp_c": 25.0,  # wiki: research/chunks/pids-protocol/05
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


def test_calculate_w_theo():
    """Test W_theo calculation with standard parameters."""
    # eta_v=0.65, disp=2.0, map=30.0, rpm=750.0, iat_c=25.0
    w_theo = calculate_w_theo(0.65, 2.0, 30.0, 750.0, 25.0)  # wiki: research/chunks/pids-protocol/05
    # W_theo = (0.65 * 2.0 * 30.0 * 750.0) / (120.0 * 0.287 * (25.0 + 273.15))
    # W_theo = 29250.0 / (120.0 * 0.287 * 298.15) ≈ 2.84857
    assert math.isclose(w_theo, 2.84857, rel_tol=1e-4)  # wiki: research/chunks/pids-protocol/05


def test_calculate_sensor_error_delta_clean():
    """Test delta calculation for clean MAF sensor."""
    w_idle = 2.84857  # wiki: research/chunks/pids-protocol/05
    maf_idle = 2.85  # wiki: research/chunks/pids-protocol/05
    w_stress = 30.15259  # wiki: research/chunks/pids-protocol/05
    maf_stress = 30.15  # wiki: research/chunks/pids-protocol/05

    delta = calculate_sensor_error_delta(maf_stress, w_stress, maf_idle, w_idle)
    # err_stress = |30.15 - 30.15259| / 30.15259 ≈ 0.000086 = 0.0086%
    # err_idle = |2.85 - 2.84857| / 2.84857 ≈ 0.0005 = 0.05%
    # delta = (0.000086 - 0.0005) * 100 = -0.0414%
    assert math.isclose(delta, -0.0414, abs_tol=1e-2)  # wiki: research/chunks/pids-protocol/05


def test_calculate_sensor_error_delta_dirty():
    """Test delta calculation for dirty MAF sensor."""
    w_idle = 2.84857  # wiki: research/chunks/pids-protocol/05
    maf_idle = 2.80  # wiki: research/chunks/pids-protocol/05
    w_stress = 30.15259  # wiki: research/chunks/pids-protocol/05
    maf_stress = 26.00  # wiki: research/chunks/pids-protocol/05

    delta = calculate_sensor_error_delta(maf_stress, w_stress, maf_idle, w_idle)
    # err_stress = |26.0 - 30.15259| / 30.15259 ≈ 0.13772 = 13.772%
    # err_idle = |2.80 - 2.84857| / 2.84857 ≈ 0.01705 = 1.705%
    # delta = (0.13772 - 0.01705) * 100 = 12.067%
    assert math.isclose(delta, 12.067, abs_tol=1e-2)  # wiki: research/chunks/pids-protocol/05


def test_translator_two_point_guard():
    """Verify that fields are None until both idle bands are captured."""
    translator = SensorSignalTranslator()
    dna = _dna_view()
    accum = LinearityAccumulator()

    # 1. Translate stabilized idle frame -> only one band captured -> should emit None
    pids_idle = _warm_idle_input(engine_rpm=750, mass_airflow_gps=2.85, manifold_vacuum_kpa=30.0)  # wiki: research/chunks/pids-protocol/05
    payload1 = translator.translate(pids_idle, dna, accumulator=accum)
    assert payload1.w_theo is None
    assert payload1.sensor_error_delta is None

    # 2. Translate stress idle frame -> both bands captured -> should compute and emit
    pids_stress = _warm_idle_input(engine_rpm=4000, mass_airflow_gps=30.15, manifold_vacuum_kpa=50.0, intake_air_temp_c=35.0)  # wiki: research/chunks/pids-protocol/05
    payload2 = translator.translate(pids_stress, dna, accumulator=accum)
    assert payload2.w_theo is not None
    assert payload2.sensor_error_delta is not None
    # Clean delta should be near 0
    assert abs(payload2.sensor_error_delta) < 1.0  # wiki: research/chunks/pids-protocol/05

    # 3. Subsequent stabilized idle frame should also emit now that both bands are captured
    payload3 = translator.translate(pids_idle, dna, accumulator=accum)
    assert payload3.w_theo is not None
    assert payload3.sensor_error_delta is not None


def test_translator_none_on_missing_dna():
    """Verify that fields are None when dna_view is None (no displacement)."""
    translator = SensorSignalTranslator()

    # Even if we send multiple bands, no displacement -> cannot compute W_theo
    pids_idle = _warm_idle_input(engine_rpm=750, mass_airflow_gps=2.85, manifold_vacuum_kpa=30.0)  # wiki: research/chunks/pids-protocol/05
    payload1 = translator.translate(pids_idle, dna_view=None)
    assert payload1.w_theo is None
    assert payload1.sensor_error_delta is None


def test_translator_none_on_alternative_strategy():
    """Verify that fields are None when strategy is not DUAL_MAF_MAP_CROSSCHECK."""
    translator = SensorSignalTranslator()
    dna = _dna_view(strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY)

    pids_idle = _warm_idle_input(engine_rpm=750, mass_airflow_gps=2.85, manifold_vacuum_kpa=30.0)  # wiki: research/chunks/pids-protocol/05
    payload1 = translator.translate(pids_idle, dna)
    assert payload1.w_theo is None
    assert payload1.sensor_error_delta is None


def test_emitter_discipline():
    """Verify emitter discipline: no diagnostic verdicts are emitted in payload."""
    translator = SensorSignalTranslator()
    dna = _dna_view()
    accum = LinearityAccumulator()

    # Capture both bands
    pids_idle = _warm_idle_input(engine_rpm=750, mass_airflow_gps=2.80, manifold_vacuum_kpa=30.0)  # wiki: research/chunks/pids-protocol/05
    pids_stress = _warm_idle_input(engine_rpm=4000, mass_airflow_gps=26.00, manifold_vacuum_kpa=50.0, intake_air_temp_c=35.0)  # wiki: research/chunks/pids-protocol/05
    translator.translate(pids_idle, dna, accumulator=accum)
    payload = translator.translate(pids_stress, dna, accumulator=accum)

    # Ensure w_theo and delta are present but no diagnostic verdicts are on the payload class
    assert payload.w_theo is not None
    assert payload.sensor_error_delta is not None
    assert not hasattr(payload, "maf_fault")
    assert not hasattr(payload, "ERR_LC_002")
    assert not hasattr(payload, "maf_sensor_contaminated")


def test_translator_stateless_isolation():
    """Verify state isolation and order independence of the translator."""
    translator = SensorSignalTranslator()
    dna = _dna_view()

    # 1. Order-independence: STRESS_IDLE first, then STABILIZED_IDLE
    accum_reverse = LinearityAccumulator()
    pids_idle = _warm_idle_input(engine_rpm=750, mass_airflow_gps=2.85, manifold_vacuum_kpa=30.0)
    pids_stress = _warm_idle_input(engine_rpm=4000, mass_airflow_gps=30.15, manifold_vacuum_kpa=50.0, intake_air_temp_c=35.0)

    payload_stress = translator.translate(pids_stress, dna, accumulator=accum_reverse)
    assert payload_stress.w_theo is None
    assert payload_stress.sensor_error_delta is None

    payload_idle = translator.translate(pids_idle, dna, accumulator=accum_reverse)
    assert payload_idle.w_theo is not None
    assert payload_idle.sensor_error_delta is not None

    # 2. State isolation: sequential calls on same translator without accumulator do not leak state
    payload_no_state1 = translator.translate(pids_idle, dna)
    assert payload_no_state1.w_theo is None
    assert payload_no_state1.sensor_error_delta is None

    payload_no_state2 = translator.translate(pids_stress, dna)
    assert payload_no_state2.w_theo is None
    assert payload_no_state2.sensor_error_delta is None

    # 3. State isolation: two different accumulators do not cross-talk
    accum_a = LinearityAccumulator()
    accum_b = LinearityAccumulator()

    # Feed STABILIZED_IDLE to accum_a
    translator.translate(pids_idle, dna, accumulator=accum_a)
    # Feed STRESS_IDLE to accum_b
    translator.translate(pids_stress, dna, accumulator=accum_b)

    # Neither should emit delta yet
    res_a = translator.translate(pids_idle, dna, accumulator=accum_a)
    assert res_a.sensor_error_delta is None

    res_b = translator.translate(pids_stress, dna, accumulator=accum_b)
    assert res_b.sensor_error_delta is None
