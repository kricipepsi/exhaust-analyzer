"""OBDLivePayload Pydantic model per OBDLab_KG_Wiki.md §5 / SEMANTIC_CONTRACT.md §4.4.

31 canonical fields (15 original + total_trim_correction_delta_b2 per T-FX-1
+ lambda_perception_delta per T-OBDV2-ECU-PERCEPT-1 + per_bank_trim_delta per T-OBDV2-BANK-ASYM-1
+ 6 analytics fields per T-OBD-WIRE-1 + intake_air_temp_c & throttle_pos_pct per T-OBDV2-7
+ control_module_voltage_v per T-OBDV2-8 + per_cylinder_misfire_counts per T-OBDV2-9
+ w_theo & sensor_error_delta per T-OBDV2-10 + ltft_cell_vector per T-OBDV2-11).
All internally-computed analytics are now emitted so COMLab's OBDLiveDataPayload mirror loses no data.
"""

from pydantic import BaseModel, Field

from obdlab.schemas.vocabulary import (
    FuelSystemStatus,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    RpmStateBucket,
    TrimAnalyticsGate,
    VEValidity,
)


class OBDLivePayload(BaseModel):
    """OBDLab output payload — canonical fields per §5 / SEMANTIC_CONTRACT §4.4.

    This is the JSON contract surface emitted by SensorSignalTranslator
    and consumed by COMLab's lab_pipeline_aggregator.
    """

    engine_warmed: bool
    # wiki: §5

    rpm_state_bucket: RpmStateBucket
    # wiki: §5 — per SEMANTIC_CONTRACT.md §8

    engine_rpm: int = Field(ge=0, le=8000)
    # wiki: §3.1 — 0..8000 RPM

    coolant_temp_c: float = Field(ge=-40, le=140)
    # wiki: §3.1 — −40..140 °C

    calculated_engine_load_pct: float = Field(ge=0, le=100)
    # wiki: §3.1 — 0..100 %

    mass_airflow_gps: float | None = Field(default=None, ge=0, le=655.35)
    # wiki: §3.1 — null when MAP_ONLY routing (§10.2)

    manifold_vacuum_kpa: float | None = Field(default=None, ge=0, le=255)
    # wiki: §3.1 — null when MAF_ONLY routing (§10.2)

    shrtft1: float = Field(ge=-127, le=127)
    # Widened from OBD-nominal [-100, 99.22] to OBD-rail [-127, 127] per T-W-6.
    # Rail values are a sensor_fault signal; rejecting them causes signal loss.

    longft1: float = Field(ge=-127, le=127)
    # Widened per T-W-6 — see shrtft1 note.

    shrtft2: float | None = Field(default=None, ge=-127, le=127)
    # Widened per T-W-6 — see shrtft1 note.

    longft2: float | None = Field(default=None, ge=-127, le=127)
    # Widened per T-W-6 — see shrtft1 note.

    total_trim_correction_delta: float
    # wiki: §5 / §12 — shrtft1 + longft1 (Bank 1 only)

    total_trim_correction_delta_b2: float | None = None
    # wiki: §5 / §12 — shrtft2 + longft2 (Bank 2); null when number_of_banks != 2

    per_bank_trim_delta: float | None = None
    # wiki: §5 / §12.1 — signed total_trim_correction_delta (B1) - total_trim_correction_delta_b2 (B2); null when single-bank

    normalized_obd_lambda: float = Field(ge=0.7, le=1.3)
    # wiki: §5 / §11 — unified lambda scalar

    lambda_perception_delta: float | None = None
    # perception delta = normalized_obd_lambda - commanded_lambda (PID 0x44); null when not wideband/0x44

    ve_pct: float = Field(ge=0.0, le=200.0)  # wiki: §6.4 — max 200 to accommodate thermal shock steam overshoot
    # wiki: §5 / §10 — calculated volumetric efficiency; 0.0 sentinel when analytics frozen
    # (ve_validity==UNKNOWN suppresses all VE-based router decisions)

    ve_validity: VEValidity
    # wiki: §5 / §10 — VE cross-check validity per §6.4; replaces ve_state_isValid

    trim_analytics_gate: TrimAnalyticsGate
    # wiki: §5 / §9 — analytics precondition gate; suppresses trim findings unless VALID

    maf_status: NodeMAFStatus
    # wiki: §5 / §10 — MAF sensor data provenance (REAL_SENSOR_FEED / VIRTUAL_EMULATION)

    map_status: NodeMAPStatus
    # wiki: §5 / §10 — MAP sensor data provenance (REAL_SENSOR_FEED / BACK_CALCULATED)

    o2_failure_mode: O2FailureMode
    # wiki: §5 / §6.7 — O2 sensor failure taxonomy; NO_FAULT when healthy

    fuel_system_status: FuelSystemStatus
    # wiki: §5 — fuel system loop status (CL/OL/OL_DRIVE/OL_FAULT)

    freeze_frame_pids: dict = Field(default_factory=dict)
    # wiki: §5 — cross-ref DTC_VOCABULARY §17; ferried through from DTCLab

    intake_air_temp_c: float = Field(ge=-40, le=140)
    # wiki: §3.1 / §5 — intake air temperature (-40..140 °C)

    throttle_pos_pct: float = Field(ge=0, le=100)
    # wiki: §3.1 / §5 — throttle position percentage (0..100 %)

    control_module_voltage_v: float = Field(default=14.0, ge=0, le=18)
    # wiki: §3.1 / §5 — control module voltage (0..18 V)

    per_cylinder_misfire_counts: dict[int, int] | None = Field(default=None)
    # wiki: research/chunks/fuel-trim/17 — per-cylinder misfire counts (dict of cyl -> count); None if pre-CAN

    ltft_cell_vector: dict[int, float] | None = Field(default=None)
    # wiki: research/chunks/fuel-trim/13 — per-cell LTFT (%), indexed by cell; None if cell PIDs unavailable

    w_theo: float | None = Field(default=None)
    # wiki: research/chunks/pids-protocol/05 — speed-density theoretical airflow (g/s)

    sensor_error_delta: float | None = Field(default=None)
    # wiki: research/chunks/pids-protocol/05 — two-point non-linearity delta (%)
