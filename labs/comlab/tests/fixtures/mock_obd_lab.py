"""Mock OBD Live Lab payload builders.

Until the real OBD Live Lab ships, tests use these dict builders. They match
``comlab.schemas.ingestion.OBDLiveDataPayload``.
"""

from __future__ import annotations


def warm_idle_baseline(
    total_trim_correction_delta: float = 0.0,
) -> dict:
    """Warm engine, neutral fuel trims, healthy VE, all gates valid."""
    return {
        "engine_warmed": True,
        "total_trim_correction_delta": total_trim_correction_delta,
        "normalized_obd_lambda": 1.0,
        "ve_pct": 72.0,
        "ve_validity": "VALID",
        "rpm_state_bucket": "STABILIZED_IDLE",
        "trim_analytics_gate": "VALID",
        "o2_failure_mode": "STUCK_LEAN",  # nominal — no failure active
        "maf_status": "REAL_SENSOR_FEED",
        "map_status": "REAL_SENSOR_FEED",
        "freeze_frame_pids": None,
    }


def hpfp_leak_signature() -> dict:
    """ECU hard-trimming negative trying to fight an unmetered fuel intrusion."""
    return {
        "engine_warmed": True,
        "total_trim_correction_delta": -50.0,
        "normalized_obd_lambda": 0.88,
        "ve_pct": 68.0,
        "ve_validity": "VALID",
        "rpm_state_bucket": "STABILIZED_IDLE",
        "trim_analytics_gate": "VALID",
        "o2_failure_mode": "STUCK_LEAN",
        "maf_status": "REAL_SENSOR_FEED",
        "map_status": "REAL_SENSOR_FEED",
        "freeze_frame_pids": {
            "calculated_engine_load_pct": 35.0,
            "freeze_frame_misfire_cylinder": None,
            "freeze_frame_engine_rpm": 850,
        },
    }


def coil_arc_under_load(misfire_cylinder: int = 3) -> dict:
    """High-load freeze-frame with positive trim delta — COP insulation arc."""
    return {
        "engine_warmed": True,
        "total_trim_correction_delta": 30.0,
        "normalized_obd_lambda": 1.12,
        "ve_pct": 78.0,
        "ve_validity": "VALID",
        "rpm_state_bucket": "STRESS_IDLE",
        "trim_analytics_gate": "VALID",
        "o2_failure_mode": "STUCK_LEAN",
        "maf_status": "REAL_SENSOR_FEED",
        "map_status": "REAL_SENSOR_FEED",
        "freeze_frame_pids": {
            "calculated_engine_load_pct": 82.5,
            "freeze_frame_misfire_cylinder": misfire_cylinder,
            "freeze_frame_engine_rpm": 2450,
        },
    }


def legacy_missing_trims() -> dict:
    """Old Euro 1/2 car — VE unknown, O2 not present, trims at zero.

    Returned dict has zero trim delta and UNKNOWN VE validity so the
    aggregator's fallback tree degrades gracefully.
    """
    return {
        "engine_warmed": True,
        "total_trim_correction_delta": 0.0,
        "normalized_obd_lambda": 1.0,
        "ve_pct": 0.0,
        "ve_validity": "UNKNOWN",
        "rpm_state_bucket": "STABILIZED_IDLE",
        "trim_analytics_gate": "VALID",
        "o2_failure_mode": "NO_FAULT",
        "maf_status": "VIRTUAL_EMULATION",
        "map_status": "BACK_CALCULATED",
        "freeze_frame_pids": None,
    }



def no_obd_channel() -> dict:
    """Legacy Euro 1/2 car with no OBD channel.

    normalized_obd_lambda is None to signal the OBD channel was not run.
    All other OBD fields are present (trims zero, VE unknown, O2 dead).

    Consumer: perception_contradiction.select_perception_lambda (T-FX-7) --
    selector falls back to GASLab lambda_measured when this is None.
    """
    return {
        "engine_warmed": True,
        "total_trim_correction_delta": 0.0,
        "normalized_obd_lambda": None,
        "ve_pct": 0.0,
        "ve_validity": "UNKNOWN",
        "rpm_state_bucket": "STABILIZED_IDLE",
        "trim_analytics_gate": "VALID",
        "o2_failure_mode": "NO_FAULT",
        "maf_status": "VIRTUAL_EMULATION",
        "map_status": "BACK_CALCULATED",
        "freeze_frame_pids": None,
    }


def cold_engine() -> dict:
    """Engine not yet at operating temperature -- triggers FATAL_INCOMPLETE."""
    return {
        "engine_warmed": False,
        "total_trim_correction_delta": 0.0,
        "normalized_obd_lambda": 1.0,
        "ve_pct": 0.0,
        "ve_validity": "UNKNOWN",
        "rpm_state_bucket": "COLD_OPEN_LOOP_INVALID",
        "trim_analytics_gate": "ENGINE_COLD",
        "o2_failure_mode": "STUCK_LEAN",
        "maf_status": "REAL_SENSOR_FEED",
        "map_status": "REAL_SENSOR_FEED",
        "freeze_frame_pids": None,
    }


def sensor_biased_high() -> dict:
    """O2 sensor reads artificially lean (high lambda) -- ECU perception is
    leaner than GASLab ground truth.

    Use with mock_gas_lab.warm_idle_baseline() (lambda_chem=1.00) to
    trigger O2_SENSOR_BIASED_HIGH in the perception-contradiction detector.
    """
    return {
        "engine_warmed": True,
        "total_trim_correction_delta": 18.0,
        "normalized_obd_lambda": 1.12,
        "ve_pct": 72.0,
        "ve_validity": "VALID",
        "rpm_state_bucket": "STABILIZED_IDLE",
        "trim_analytics_gate": "VALID",
        "o2_failure_mode": "STUCK_LEAN",
        "maf_status": "REAL_SENSOR_FEED",
        "map_status": "REAL_SENSOR_FEED",
        "freeze_frame_pids": None,
    }


def sensor_biased_low() -> dict:
    """O2 sensor reads artificially rich (low lambda) -- ECU perception is
    richer than GASLab ground truth.

    Use with mock_gas_lab.warm_idle_baseline() (lambda_chem=1.00) to
    trigger O2_SENSOR_BIASED_LOW in the perception-contradiction detector.
    """
    return {
        "engine_warmed": True,
        "total_trim_correction_delta": -18.0,
        "normalized_obd_lambda": 0.88,
        "ve_pct": 72.0,
        "ve_validity": "VALID",
        "rpm_state_bucket": "STABILIZED_IDLE",
        "trim_analytics_gate": "VALID",
        "o2_failure_mode": "STUCK_LEAN",
        "maf_status": "REAL_SENSOR_FEED",
        "map_status": "REAL_SENSOR_FEED",
        "freeze_frame_pids": None,
    }
