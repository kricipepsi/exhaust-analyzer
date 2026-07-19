"""Pytest configuration and shared fixtures for obdlab tests.

Provides the default-shape detector, signal-bearing predicate, and
CSV-row-to-input builder consumed by both A1 (test_cases.py) and
A2 (generative/*) decision-rate harness tests.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Add the shared harness engine to sys.path so per-lab descriptors can
# import from harness.descriptor (PROJECTION_CONTRACT §2).
_HARNESS_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "harness"
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

from obdlab.schemas.dna_view import (  # noqa: E402
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)
from obdlab.schemas.payload import OBDLivePayload  # noqa: E402
from obdlab.schemas.vocabulary import O2FailureMode, VEValidity  # noqa: E402


def is_default_shape(payload: OBDLivePayload) -> bool:
    """Return True when every discriminating channel is at its default/sentinel value.

    Each field's default traces to the freeze path in
    sensor_signal_translator.py lines 134-163.

    normalized_obd_lambda is included with a tolerance: frozen=1.0,
    and genuine stoich also ≈1.0. A deviation > 0.005 from 1.0
    indicates the O2 channel moved (rich or lean reading).
    """
    return (
        payload.o2_failure_mode == O2FailureMode.NO_FAULT
        and abs(payload.normalized_obd_lambda - 1.0) < 0.005
        and payload.ve_pct == 0.0
        and payload.ve_validity == VEValidity.UNKNOWN
        and payload.total_trim_correction_delta == 0.0
        and payload.total_trim_correction_delta_b2 is None
        and payload.per_bank_trim_delta is None
        and payload.lambda_perception_delta is None
        and payload.w_theo is None
        and payload.sensor_error_delta is None
    )


def _parse_float(val: str) -> float | None:
    """Parse a CSV string cell to float; empty / dash → None."""
    stripped = val.strip()
    if stripped == "" or stripped == "-":
        return None
    return float(stripped)


def _parse_int(val: str) -> int | None:
    """Parse a CSV string cell to int; empty / dash → None."""
    stripped = val.strip()
    if stripped == "" or stripped == "-":
        return None
    return int(float(stripped))


def is_signal_bearing(row: dict[str, str]) -> bool:
    """Return True if the CSV row carries enough PID data to move a channel.

    Operates on raw CSV row dicts with string values.
    An empty cell means the datum is absent.

    The row must have engine_rpm > 0 — without RPM the pipeline freezes
    analytics regardless of other signals (COLD_OPEN_LOOP_INVALID).
    """
    ect = _parse_float(row.get("coolant_temp_c", ""))
    if ect is None or ect < 75.0:
        return False  # cold engine → analytics frozen, correct abstention

    rpm = _parse_float(row.get("engine_rpm", ""))
    if rpm is None or rpm <= 0:
        return False

    # Trim signal: non-zero short-term or long-term fuel trim
    stft1 = _parse_float(row.get("shrtft1", ""))
    ltft1 = _parse_float(row.get("longft1", ""))
    if (stft1 is not None and stft1 != 0.0) or (ltft1 is not None and ltft1 != 0.0):
        return True

    # O2 signal: lambda outside the narrowband stoich zone (0.99-1.01)
    # Values inside this zone map to 0.45V (stoich) → no channel moves.
    obd_lambda = _parse_float(row.get("obd_lambda", ""))
    if obd_lambda is not None and (obd_lambda < 0.99 or obd_lambda > 1.01):
        return True

    # VE signal: airflow or manifold pressure present
    maf = _parse_float(row.get("mass_airflow_gps", ""))
    map_kpa = _parse_float(row.get("manifold_vacuum_kpa", ""))
    if maf is not None or map_kpa is not None:
        return True

    # Bank-2 signal: bank-2 trims present on a dual-bank configuration
    stft2 = _parse_float(row.get("shrtft2", ""))
    ltft2 = _parse_float(row.get("longft2", ""))
    n_banks = row.get("number_of_banks", "1").strip()
    if n_banks == "2" and (
        (stft2 is not None and stft2 != 0.0) or (ltft2 is not None and ltft2 != 0.0)
    ):
        return True

    return False


def build_air_metering_strategy(has_maf: str, has_map: str) -> AirMeteringStrategy:
    """Derive AirMeteringStrategy from has_maf / has_map CSV flags."""
    maf = has_maf.strip().lower() == "true"
    map_ = has_map.strip().lower() == "true"
    if maf and map_:
        return AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK
    if maf:
        return AirMeteringStrategy.MAF_ONLY
    if map_:
        return AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY
    # Neither sensor present — default to DUAL (VE engine will use sentinels)
    return AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK


def build_o2_sensor_type(o2_classification: str) -> O2SensorType:
    """Derive O2SensorType from o2_upstream_classification CSV column."""
    val = o2_classification.strip()
    if val == "WIDEBAND_LINEAR":
        return O2SensorType.WIDEBAND_LINEAR
    if val == "WIDEBAND_NB_SIM":
        return O2SensorType.WIDEBAND_NB_SIM
    return O2SensorType.NARROWBAND_0_TO_1V


def build_inputs_from_csv_row(
    row: dict[str, str],
) -> tuple[dict[str, Any], ObdLabDnaView | None]:
    """Build (raw_user_inputs, dna_view) from a CSV row dict.

    Empty-string cells are treated as absent.
    Returns a tuple ready to unpack into SensorSignalTranslator.translate().
    """
    raw: dict[str, Any] = {}

    # --- Required PIDs (always set — validator needs them present) ---
    rpm = _parse_float(row.get("engine_rpm", ""))
    raw["engine_rpm"] = int(rpm) if rpm is not None else 0

    ect = _parse_float(row.get("coolant_temp_c", ""))
    raw["coolant_temp_c"] = ect if ect is not None else 25.0

    load = _parse_float(row.get("calculated_engine_load_pct", ""))
    if load is not None:
        raw["calculated_engine_load_pct"] = load

    # --- Optional sensor PIDs ---
    maf = _parse_float(row.get("mass_airflow_gps", ""))
    if maf is not None:
        raw["mass_airflow_gps"] = maf

    map_kpa = _parse_float(row.get("manifold_vacuum_kpa", ""))
    if map_kpa is not None:
        raw["manifold_vacuum_kpa"] = map_kpa

    # --- Fuel trims ---
    stft1 = _parse_float(row.get("shrtft1", ""))
    raw["shrtft1"] = stft1 if stft1 is not None else 0.0

    ltft1 = _parse_float(row.get("longft1", ""))
    raw["longft1"] = ltft1 if ltft1 is not None else 0.0

    # --- Bank configuration ---
    n_banks_str = row.get("number_of_banks", "1").strip()
    n_banks = int(n_banks_str) if n_banks_str else 1
    raw["number_of_banks"] = n_banks

    # Bank-2 trims (only populate for dual-bank)
    if n_banks == 2:
        stft2 = _parse_float(row.get("shrtft2", ""))
        raw["shrtft2"] = stft2 if stft2 is not None else 0.0
        ltft2 = _parse_float(row.get("longft2", ""))
        raw["longft2"] = ltft2 if ltft2 is not None else 0.0

    # --- O2 sensor data ---
    obd_lambda = _parse_float(row.get("obd_lambda", ""))
    o2_class = row.get("o2_upstream_classification", "").strip()
    o2_sensor_type = build_o2_sensor_type(o2_class)

    if obd_lambda is not None:
        if o2_sensor_type == O2SensorType.WIDEBAND_LINEAR:
            raw["pid_wideband_equivalence_ratio"] = obd_lambda
        else:
            # Narrowband: set pid_oxygen_sensor_volts derived from lambda
            raw["pid_oxygen_sensor_volts"] = _lambda_to_nb_voltage(obd_lambda)

    # --- Supplementary fields ---
    fuel_status = row.get("fuel_status", "").strip()
    raw["fuel_sys_status"] = fuel_status if fuel_status else "CL"

    raw["intake_air_temp_c"] = 25.0
    raw["throttle_pos"] = 0.0
    raw["control_module_voltage_v"] = 14.0
    raw["active_dtcs"] = []
    raw["drive_cycles_since_clear"] = 5

    # --- DNA view ---
    has_maf = row.get("has_maf", "false")
    has_map = row.get("has_map", "false")
    dna_view = ObdLabDnaView(
        air_metering_strategy=build_air_metering_strategy(has_maf, has_map),
        upstream_o2_type=o2_sensor_type,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.NONE,
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
    )

    return raw, dna_view


def _lambda_to_nb_voltage(lamb: float) -> float:
    """Approximate inverse of the OBDLab 3-zone narrowband mapping.

    The forward mapping in o2_normalizer.py produces:
      lean   (>1.01) → ~1.05 lambda
      stoich (~1.0)  → ~1.00 lambda
      rich   (<0.99) → ~0.95 lambda

    This inverse maps back to a representative narrowband voltage
    so the round-trip through translate() exercises the correct zone.
    """
    if lamb > 1.01:
        return 0.2  # lean zone
    if lamb < 0.99:
        return 0.8  # rich zone
    return 0.45  # stoich zone


def point_in_box(
    point: dict[str, float], box_dims: dict[str, tuple[float, float]]
) -> bool:
    """Return True if *point* lies geometrically inside *box_dims*.

    Each dimension in box_dims must have a value in the point within
    [min, max]. Dimensions present in the box but not the point
    are treated as satisfied (centroid assumed).
    """
    for dim, (lo, hi) in box_dims.items():
        val = point.get(dim)
        if val is None:
            continue  # dimension not sampled — treat as centroid (inside)
        if val < lo or val > hi:
            return False
    return True


def channel_moved_for_box(payload: Any, box_sig: str) -> bool:
    """Return True if the payload's discriminating channel moved for *box_sig*.

    Each box signature maps to a specific channel predicate.
    """
    from obdlab.schemas.vocabulary import O2FailureMode, VEValidity

    if box_sig == "trim_positive":
        return bool(payload.total_trim_correction_delta >= 5.0)
    if box_sig == "trim_negative":
        return bool(payload.total_trim_correction_delta <= -5.0)
    if box_sig == "o2_stuck_lean":
        return bool(payload.o2_failure_mode == O2FailureMode.STUCK_LEAN)
    if box_sig == "o2_stuck_rich":
        return bool(payload.o2_failure_mode == O2FailureMode.STUCK_RICH)
    if box_sig == "lambda_delta_rich":
        return bool(
            payload.lambda_perception_delta is not None
            and payload.lambda_perception_delta < 0
        )
    if box_sig == "lambda_delta_lean":
        return bool(
            payload.lambda_perception_delta is not None
            and payload.lambda_perception_delta > 0
        )
    if box_sig == "ve_idle_collapse":
        return bool(payload.ve_validity == VEValidity.FAULT_VE_IDLE_COLLAPSE)
    if box_sig == "bank_asym":
        return bool(payload.per_bank_trim_delta is not None)
    return False

