"""OBDLab ModuleDescriptor — fault-box table + entry point for the decision-rate harness.

Consumed by A1 (test_cases.py over obdlab_cases.csv) and A2
(generative/* channel-move generators).
"""

from __future__ import annotations

from typing import Any

from harness.descriptor import FaultBox, FieldRange, ModuleDescriptor

from obdlab.core.sensor_signal_translator import SensorSignalTranslator
from obdlab.schemas.dna_view import (
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)

# ---------------------------------------------------------------------------
# Fault-box table — one box per discriminating channel.
# Each box cites its source file + line range.
# ---------------------------------------------------------------------------

_BOX_DEFS: list[dict[str, Any]] = [
    # -- Trim channel boxes --
    {
        "sig": "trim_positive",
        "dims": {"shrtft1": (5.0, 127.0), "longft1": (0.0, 127.0)},
        "channel": "total_trim_correction_delta",
        "default": 0.0,
        "predicate": ">= 5.0",
        "src": "obdlab/core/trim_vector_aggregator.py:17-32",
    },
    {
        "sig": "trim_negative",
        "dims": {"shrtft1": (-127.0, -5.0), "longft1": (-127.0, 0.0)},
        "channel": "total_trim_correction_delta",
        "default": 0.0,
        "predicate": "<= -5.0",
        "src": "obdlab/core/trim_vector_aggregator.py:17-32",
    },
    # -- O2 failure-mode boxes (narrowband) --
    {
        "sig": "o2_stuck_lean",
        "dims": {"pid_oxygen_sensor_volts": (0.0, 0.09)},
        "channel": "o2_failure_mode",
        "default": "NO_FAULT",
        "predicate": "== STUCK_LEAN",
        "src": "obdlab/core/o2_normalizer.py:122-128",
        "dna": {"upstream_o2_type": "NARROWBAND_0_TO_1V"},
    },
    {
        "sig": "o2_stuck_rich",
        "dims": {"pid_oxygen_sensor_volts": (0.91, 5.0)},
        "channel": "o2_failure_mode",
        "default": "NO_FAULT",
        "predicate": "== STUCK_RICH",
        "src": "obdlab/core/o2_normalizer.py:129-135",
        "dna": {"upstream_o2_type": "NARROWBAND_0_TO_1V"},
    },
    # -- Lambda perception delta boxes (wideband) --
    {
        "sig": "lambda_delta_rich",
        "dims": {"pid_wideband_equivalence_ratio": (0.5, 0.949)},
        "channel": "lambda_perception_delta",
        "default": None,
        "predicate": "< 0",
        "src": "obdlab/core/sensor_signal_translator.py:172-180",
        "dna": {"upstream_o2_type": "WIDEBAND_LINEAR"},
    },
    {
        "sig": "lambda_delta_lean",
        "dims": {"pid_wideband_equivalence_ratio": (1.051, 2.0)},
        "channel": "lambda_perception_delta",
        "default": None,
        "predicate": "> 0",
        "src": "obdlab/core/sensor_signal_translator.py:172-180",
        "dna": {"upstream_o2_type": "WIDEBAND_LINEAR"},
    },
    # -- VE validity boxes --
    {
        "sig": "ve_idle_collapse",
        "dims": {
            "mass_airflow_gps": (0.0, 30.0),
            "manifold_vacuum_kpa": (46.0, 100.0),
            "engine_rpm": (650, 900),
        },
        "channel": "ve_validity",
        "default": "UNKNOWN",
        "predicate": "== FAULT_VE_IDLE_COLLAPSE",
        "src": "obdlab/core/ve_engine.py:89-118",
        "dna": {"air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK"},
    },
    # -- Bank asymmetry box --
    {
        "sig": "bank_asym",
        "dims": {
            "shrtft1": (10.0, 127.0),
            "shrtft2": (-127.0, -10.0),
            "number_of_banks": (2, 2),
        },
        "channel": "per_bank_trim_delta",
        "default": None,
        "predicate": "is not None",
        "src": "obdlab/core/trim_vector_aggregator.py:44-66",
    },
]

# ---------------------------------------------------------------------------
# FieldRange list — one per input column the generators may sample.
# ---------------------------------------------------------------------------

_FIELDS: list[FieldRange] = [
    FieldRange(name="engine_rpm", type_="int", min_=0, max_=8000),
    FieldRange(name="coolant_temp_c", type_="float", min_=-40, max_=140),
    FieldRange(name="calculated_engine_load_pct", type_="float", min_=0, max_=100),
    FieldRange(name="mass_airflow_gps", type_="Optional[float]", min_=0, max_=655.35),
    FieldRange(name="manifold_vacuum_kpa", type_="Optional[float]", min_=0, max_=255),
    FieldRange(name="shrtft1", type_="float", min_=-127, max_=127),
    FieldRange(name="longft1", type_="float", min_=-127, max_=127),
    FieldRange(name="shrtft2", type_="Optional[float]", min_=-127, max_=127),
    FieldRange(name="longft2", type_="Optional[float]", min_=-127, max_=127),
    FieldRange(name="number_of_banks", type_="int", min_=1, max_=2),
    FieldRange(name="pid_oxygen_sensor_volts", type_="Optional[float]", min_=0, max_=5),
    FieldRange(name="pid_wideband_equivalence_ratio", type_="Optional[float]", min_=0.5, max_=2.0),
    FieldRange(name="intake_air_temp_c", type_="float", min_=-40, max_=140),
    FieldRange(name="throttle_pos", type_="float", min_=0, max_=100),
]

# Sentinel translator instance created once at descriptor-build time.
_translator = SensorSignalTranslator()


def _coerce_float(val: Any) -> float | None:
    """Coerce a CSV or generator value to float; empty/dash/None → None."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if s == "" or s == "-":
        return None
    return float(s)


def _coerce_int(val: Any, default: int = 0) -> int:
    """Coerce a CSV or generator value to int."""
    if val is None:
        return default
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    s = str(val).strip()
    if s == "":
        return default
    return int(float(s))


def _build_dna_view(meta: dict[str, Any] | None = None) -> ObdLabDnaView:
    """Build an ObdLabDnaView from optional meta overrides."""
    kwargs: dict[str, Any] = {
        "air_metering_strategy": AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        "upstream_o2_type": O2SensorType.NARROWBAND_0_TO_1V,
        "induction_type": InductionType.NATURALLY_ASPIRATED,
        "confidence": VinConfidence.NONE,
        "engine_displacement_liters": 2.0,
        "rated_rpm": 6500,
        "stress_idle_rpm_target": 4000,
    }
    if meta:
        for key, val in meta.items():
            if key == "upstream_o2_type" and isinstance(val, str):
                kwargs[key] = O2SensorType(val)
            elif key == "air_metering_strategy" and isinstance(val, str):
                kwargs[key] = AirMeteringStrategy(val)
            else:
                kwargs[key] = val
    return ObdLabDnaView(**kwargs)


def _build_args(row: dict[str, Any]) -> tuple[dict[str, Any], ObdLabDnaView | None]:
    """Build (raw_user_inputs, dna_view) from a CSV or generator row.

    Accepts both CSV column names and raw PID names.
    Returns a tuple ready to unpack into translate().
    """
    raw: dict[str, Any] = {}

    # Required PIDs
    rpm = _coerce_int(row.get("engine_rpm", 0))
    raw["engine_rpm"] = rpm

    ect = _coerce_float(row.get("coolant_temp_c", 25.0))
    raw["coolant_temp_c"] = ect if ect is not None else 25.0

    load = _coerce_float(row.get("calculated_engine_load_pct"))
    if load is not None:
        raw["calculated_engine_load_pct"] = load

    # Optional sensor PIDs
    maf = _coerce_float(row.get("mass_airflow_gps"))
    if maf is not None:
        raw["mass_airflow_gps"] = maf

    map_kpa = _coerce_float(row.get("manifold_vacuum_kpa"))
    if map_kpa is not None:
        raw["manifold_vacuum_kpa"] = map_kpa

    # Fuel trims
    raw["shrtft1"] = _coerce_float(row.get("shrtft1", 0.0)) or 0.0
    raw["longft1"] = _coerce_float(row.get("longft1", 0.0)) or 0.0

    # Bank config
    n_banks = _coerce_int(row.get("number_of_banks", 1), default=1)
    raw["number_of_banks"] = n_banks

    if n_banks == 2:
        stft2 = _coerce_float(row.get("shrtft2"))
        if stft2 is not None:
            raw["shrtft2"] = stft2
        ltft2 = _coerce_float(row.get("longft2"))
        if ltft2 is not None:
            raw["longft2"] = ltft2

    # O2 sensor PIDs (may be set by generators directly)
    o2v = _coerce_float(row.get("pid_oxygen_sensor_volts"))
    if o2v is not None:
        raw["pid_oxygen_sensor_volts"] = o2v

    wb_eq = _coerce_float(row.get("pid_wideband_equivalence_ratio"))
    if wb_eq is not None:
        raw["pid_wideband_equivalence_ratio"] = wb_eq
        # Set commanded_equivalence_ratio for lambda_perception_delta
        raw["commanded_equivalence_ratio"] = 1.0

    # Supplementary
    raw["fuel_sys_status"] = str(row.get("fuel_sys_status", "CL"))
    raw["intake_air_temp_c"] = _coerce_float(row.get("intake_air_temp_c", 25.0)) or 25.0
    raw["throttle_pos"] = _coerce_float(row.get("throttle_pos", 0.0)) or 0.0
    raw["control_module_voltage_v"] = 14.0
    raw["active_dtcs"] = []
    raw["drive_cycles_since_clear"] = 5

    # DNA view
    dna_meta = row.get("_dna_meta")
    dna_view = _build_dna_view(dna_meta)

    # Default O2 sensor PID for narrowband branch — the translator requires
    # pid_oxygen_sensor_volts when upstream_o2_type is NARROWBAND.
    if (
        dna_view.upstream_o2_type == O2SensorType.NARROWBAND_0_TO_1V
        and "pid_oxygen_sensor_volts" not in raw
    ):
        raw["pid_oxygen_sensor_volts"] = 0.45  # stoich default

    return raw, dna_view


def _extract_expected(row: dict[str, Any]) -> dict[str, Any]:
    """No ground-truth expecteds — all characterization."""
    return {}


def _diff(actual: Any, expected: dict[str, Any]) -> list[str]:
    """No per-row diff assertions for the bounce-rate harness."""
    return []


def build_obdlab_descriptor() -> ModuleDescriptor:
    """Build the OBDLab ModuleDescriptor for the decision-rate harness.

    Fault boxes are per-channel (not per-signature) — multiple boxes
    may fire simultaneously, which is correct multi-channel behaviour.
    """
    boxes: dict[str, FaultBox] = {}
    for bd in _BOX_DEFS:
        boxes[bd["sig"]] = FaultBox(
            signature=bd["sig"],
            dimensions=bd["dims"],
            source=bd["src"],
        )

    return ModuleDescriptor(
        name="OBDLab",
        fields=_FIELDS,
        boxes=boxes,
        build_args=_build_args,
        entry_point=_translator.translate,
        extract_expected=_extract_expected,
        diff=_diff,
    )
