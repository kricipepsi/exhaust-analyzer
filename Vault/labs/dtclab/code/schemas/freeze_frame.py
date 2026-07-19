"""FreezeFrameRecord — Mode $02 snapshot at fault confirmation.

Every field name is bare (no freeze_frame_ prefix) per DTC_VOCABULARY.md §12.
The older COMLab prefix convention is superseded.
"""

from typing import Optional

from pydantic import BaseModel, Field

from dtclab.schemas.vocabulary import FuelSystemStatus


class FreezeFrameRecord(BaseModel):
    """Mode $02 freeze-frame snapshot captured at DTC confirmation.

    Source: DTC_VOCABULARY.md §12.

    The 12 mandatory PIDs (§12.1) are the minimum required set; missing
    any one marks the payload FREEZE_FRAME_INCOMPLETE.  Extended PIDs
    (§12.2) are optional — absent is not an error.

    The derived symptom flags (§12.3) are computed by
    ``freeze_frame_extractor.extract_freeze_frame`` and default to False.
    """

    # ---- mandatory PIDs (§12.1) -----------------------------------------------

    calculated_load_pct: float = Field(ge=0, le=100)
    # wiki: §12.1 — PID $04, peak available torque % at current RPM

    engine_rpm: int = Field(ge=0)
    # wiki: §12.1 — PID $0C, RPM

    coolant_temp_c: float
    # wiki: §12.1 — PID $05, °C; negative values legal (cold ambient)

    short_term_ft1: float
    # wiki: §12.1 — PID $06, short-term fuel trim Bank 1 %

    long_term_ft1: float
    # wiki: §12.1 — PID $07, long-term fuel trim Bank 1 %

    manifold_pressure_kpa: float = Field(ge=0)
    # wiki: §12.1 — PID $0B, kPa

    vehicle_speed_kmh: int = Field(ge=0)
    # wiki: §12.1 — PID $0D, km/h

    ignition_advance_deg: float
    # wiki: §12.1 — PID $0E, ° BTDC; negative = ATDC (retard)

    intake_air_temp_c: float
    # wiki: §12.1 — PID $0F, °C; negative values legal

    maf_gps: float = Field(ge=0)
    # wiki: §12.1 — PID $10, g/s

    throttle_pos_pct: float = Field(ge=0, le=100)
    # wiki: §12.1 — PID $11, %

    fuel_system_status: FuelSystemStatus
    # wiki: §12.1 — PID $03, loop status enum

    # ---- extended PIDs (§12.2, all optional) ----------------------------------

    short_term_ft2: Optional[float] = None  # wiki: §12.2
    long_term_ft2: Optional[float] = None  # wiki: §12.2
    o2_voltage_b1s1: Optional[float] = None  # wiki: §12.2
    barometric_pressure_kpa: Optional[float] = None  # wiki: §12.2
    commanded_egr_pct: Optional[float] = None  # wiki: §12.2
    run_time_since_start_sec: Optional[int] = None  # wiki: §12.2
    fuel_level_pct: Optional[float] = None  # wiki: §12.2

    # ---- derived symptom flags (§12.3) ----------------------------------------

    ff_open_loop_at_fault: bool = False
    # wiki: §12.3 — fuel_system_status ∈ {OL, OL_FAULT, OL_DRIVE}

    ff_load_high_at_low_rpm: bool = False
    # wiki: §12.3 — calculated_load_pct > 70 AND engine_rpm < 1500

    ff_ect_warmup: bool = False
    # wiki: §12.3 — coolant_temp_c < 60

    ff_iat_ect_biased: bool = False
    # wiki: §12.3 — |intake_air_temp_c − coolant_temp_c| > 30 AND engine_rpm == 0

    ff_timing_retard_severe: bool = False
    # wiki: §12.3 — ignition_advance_deg < −10

    ff_codes_cleared_invalidated: bool = False
    # wiki: §12.3 — set by caller when codes_cleared is True in session context

    ff_fuel_spark_cut_at_crank: bool = False
    # wiki: 10_nonstart_diagnostics.md §10.3 — OL_FAULT in a stationary no-run snapshot
