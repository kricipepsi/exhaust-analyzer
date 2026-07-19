"""Freeze-frame extractor — validates Mode $02 data and derives symptom flags.

Source: DTC_VOCABULARY.md §12.
"""

from __future__ import annotations

import logging

from dtclab.schemas.freeze_frame import FreezeFrameRecord
from dtclab.schemas.vocabulary import FuelSystemStatus

logger = logging.getLogger(__name__)

_MANDATORY_PIDS: tuple[str, ...] = (
    "calculated_load_pct",  # wiki: §12.1
    "engine_rpm",  # wiki: §12.1
    "coolant_temp_c",  # wiki: §12.1
    "short_term_ft1",  # wiki: §12.1
    "long_term_ft1",  # wiki: §12.1
    "manifold_pressure_kpa",  # wiki: §12.1
    "vehicle_speed_kmh",  # wiki: §12.1
    "ignition_advance_deg",  # wiki: §12.1
    "intake_air_temp_c",  # wiki: §12.1
    "maf_gps",  # wiki: §12.1
    "throttle_pos_pct",  # wiki: §12.1
    "fuel_system_status",  # wiki: §12.1
)


class FreezeFrameIncompleteError(ValueError):
    """Raised when one or more mandatory freeze-frame PIDs are missing."""

    def __init__(self, missing: list[str]) -> None:
        self.missing = missing
        super().__init__(
            f"Freeze frame incomplete — missing mandatory PIDs: {missing}"
        )


def extract_freeze_frame(
    raw: dict, codes_cleared: bool = False
) -> FreezeFrameRecord:
    """Validate mandatory PIDs and derive symptom flags from *raw*.

    Args:
        raw: Dict of PID name → value from Mode $02.  Keys must use the
             bare canonical names from DTC_VOCABULARY.md §12.1.
        codes_cleared: ``True`` if DTCs were cleared this session (sets
                       ``ff_codes_cleared_invalidated``).

    Returns:
        A fully populated ``FreezeFrameRecord`` with derived flags set.

    Raises:
        FreezeFrameIncompleteError: If any mandatory PID is absent from *raw*.
    """
    missing = [pid for pid in _MANDATORY_PIDS if raw.get(pid) is None]
    if missing:
        raise FreezeFrameIncompleteError(missing)

    # Build record from raw first — Pydantic coerces numeric strings
    # (e.g. "800" → 800) and enums (e.g. "CL" → FuelSystemStatus.CL),
    # and raises ValidationError on bad strings. Derived flags get False
    # defaults; we replace them below after coercion is complete.
    record = FreezeFrameRecord(
        calculated_load_pct=raw["calculated_load_pct"],
        engine_rpm=raw["engine_rpm"],
        coolant_temp_c=raw["coolant_temp_c"],
        short_term_ft1=raw["short_term_ft1"],
        long_term_ft1=raw["long_term_ft1"],
        manifold_pressure_kpa=raw["manifold_pressure_kpa"],
        vehicle_speed_kmh=raw["vehicle_speed_kmh"],
        ignition_advance_deg=raw["ignition_advance_deg"],
        intake_air_temp_c=raw["intake_air_temp_c"],
        maf_gps=raw["maf_gps"],
        throttle_pos_pct=raw["throttle_pos_pct"],
        fuel_system_status=raw["fuel_system_status"],
        # extended PIDs (§12.2) — pass through if present
        short_term_ft2=raw.get("short_term_ft2"),
        long_term_ft2=raw.get("long_term_ft2"),
        o2_voltage_b1s1=raw.get("o2_voltage_b1s1"),
        barometric_pressure_kpa=raw.get("barometric_pressure_kpa"),
        commanded_egr_pct=raw.get("commanded_egr_pct"),
        run_time_since_start_sec=raw.get("run_time_since_start_sec"),
        fuel_level_pct=raw.get("fuel_level_pct"),
    )

    # Derive symptom flags from the typed (coerced) record fields.
    return record.model_copy(
        update={
            "ff_open_loop_at_fault": _derive_open_loop(
                record.fuel_system_status
            ),
            "ff_load_high_at_low_rpm": _derive_load_high_low_rpm(
                record.calculated_load_pct, record.engine_rpm
            ),
            "ff_ect_warmup": record.coolant_temp_c < 60,  # wiki: DTC_WIKI.md §3
            "ff_iat_ect_biased": _derive_iat_ect_bias(
                record.intake_air_temp_c,
                record.coolant_temp_c,
                record.engine_rpm,
            ),
            "ff_timing_retard_severe": record.ignition_advance_deg
            < -10,  # wiki: DTC_WIKI.md §8.2
            "ff_codes_cleared_invalidated": bool(codes_cleared),
            "ff_fuel_spark_cut_at_crank": _derive_fuel_spark_cut_at_crank(
                record.fuel_system_status,
                record.engine_rpm,
                record.vehicle_speed_kmh,
            ),
        }
    )


# ---------------------------------------------------------------------------
# Flag-derivation helpers
# ---------------------------------------------------------------------------


def _derive_open_loop(fuel_status: FuelSystemStatus) -> bool:
    """ff_open_loop_at_fault: loop status is open-loop, open-loop drive, or
    open-loop fault.

    wiki: DTC_VOCABULARY.md §12.3
    """
    return fuel_status in (
        FuelSystemStatus.OL,
        FuelSystemStatus.OL_FAULT,
        FuelSystemStatus.OL_DRIVE,
    )


def _derive_load_high_low_rpm(load_pct: float, rpm: int) -> bool:
    """ff_load_high_at_low_rpm: high load at low RPM.

    wiki: DTC_VOCABULARY.md §12.3; DTC_WIKI.md §2 (70 % CLV threshold)
    """
    return load_pct > 70 and rpm < 1500  # wiki: §12.3


def _derive_iat_ect_bias(
    iat_c: float, ect_c: float, rpm: int
) -> bool:
    """ff_iat_ect_biased: IAT/ECT delta > 30 °C at zero RPM.

    wiki: DTC_VOCABULARY.md §12.3
    """
    return abs(iat_c - ect_c) > 30 and rpm == 0  # wiki: §12.3


def _derive_fuel_spark_cut_at_crank(
    fuel_status: FuelSystemStatus,
    rpm: int,
    speed_kmh: int,
) -> bool:
    """ff_fuel_spark_cut_at_crank: OL_FAULT in a stationary no-run snapshot.

    wiki: 10_nonstart_diagnostics.md §10.3 gives OL_FAULT with cranking
    RPM 150-180 for immobiliser and RPM 0 for CKP/CMP no-start patterns;
    DTC_VOCABULARY.md §12.1 supplies the computable PID fields.
    """
    return (
        fuel_status == FuelSystemStatus.OL_FAULT
        and speed_kmh == 0
        and rpm <= 180
    )


def evaluate_coolant_dtc_context(
    dtc_code: str,
    fuel_status: FuelSystemStatus,
) -> str | None:
    """Evaluate cross-field DTC + fuel status for fluid intrusion signatures.

    Returns a DTCRoutingTag value string if a coolant/fluid signature is
    detected, or None otherwise.

    Source: CoolantLeakSig.md §4 (TS51_DTC, TS52_DTC).
    """
    if dtc_code in ("P0128", "P0117") and fuel_status == FuelSystemStatus.OL_FAULT:
        logger.warning(
            "DTCLab: Coolant system malfunction — P0128/P0117 in OL_FAULT. "
            "Heat energy lost to boiling coolant."
        )
        return "COOLANT_SYSTEM_MALFUNCTION"

    if dtc_code.startswith("P030") and fuel_status == FuelSystemStatus.CL:
        logger.info(
            f"DTCLab: Cylinder fluid misfire on {dtc_code} in closed loop. "
            "Liquid quenching spark plug."
        )
        return "CYLINDER_FLUID_MISFIRE"

    return None
