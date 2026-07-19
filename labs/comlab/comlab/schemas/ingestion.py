"""OrchestratorIngestionPayload — the single JSON contract for inbound data.

This is the boundary between the four upstream labs (VINLab, GasLab,
OBD Live Lab, DTC Lab) and ComLab. Every lab is responsible for producing a
slice of this payload that conforms to its schema; ComLab does the rest.

Source: OrchestratorLabBP.md lines 731-833.

Status: v0.1 skeleton — class scaffolds only. Field types and validators are
declared but no business logic yet. Phase 1 fills the validators.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Literal

from pydantic import UUID4, BaseModel, Field, field_validator, model_validator

from comlab.schemas.vocabulary import (
    DTC_REGEX,
    AirMeteringStrategy,
    DownstreamTrimRole,
    DTCRoutingTag,
    EngineStateBucket,
    EuroEmissionCategory,
    FuelDeliveryType,
    FuelSystemStatus,
    HistoricalFaultContext,
    Horizon,
    InductionType,
    Mode06MonitorState,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    PrimaryLoadCalculation,
    SampleValidity,
    TrimAnalyticsGate,
    UpstreamO2Type,
    VEValidity,
    VinConfidence,
)


class AirMeteringArchitecture(BaseModel):
    """VIN-driven air metering topology. Consumed by OBDLab VE formula routing.

    Source: lld: §3.2.
    """

    has_maf_sensor: bool  # lld: §3.2
    has_map_sensor: bool  # lld: §3.2
    primary_load_calculation: PrimaryLoadCalculation  # lld: §3.2


class EmissionsConfiguration(BaseModel):
    """VIN-driven emissions equipment inventory.

    Source: lld: §3.2.
    """

    upstream_o2_type: UpstreamO2Type  # lld: §3.2
    downstream_o2_present: bool  # lld: §3.2
    downstream_trim_role: DownstreamTrimRole = Field(default=DownstreamTrimRole.NONE)  # lld: §3.2 — O2_MODEL_STRATEGY.md §3
    egr_equipped: bool  # lld: §3.2

    has_catalyst: bool = True  # lld: §3.2 — near-universal

    @model_validator(mode='after')
    def _downstream_trim_role_implies_sensor(self) -> EmissionsConfiguration:
        """downstream_trim_role != NONE requires downstream_o2_present=True.

        lld: §10 — ERR-CONTRACT-003
        """
        if self.downstream_trim_role != DownstreamTrimRole.NONE and not self.downstream_o2_present:
            raise ValueError(
                f"downstream_trim_role={self.downstream_trim_role.value} requires "
                "downstream_o2_present=True (ERR-CONTRACT-003)"
            )
        return self


class VinDNA(BaseModel):
    """VIN-resolved vehicle identity block. Mirror of DNALab output.

    Every field is populated by DNALab; COMLab is a read-only consumer.

    Source: lld: §3.2.
    """

    vin: str = Field(min_length=17, max_length=17, pattern=r"^[A-HJ-NPR-Z0-9]{17}$")  # lld: §3.2
    make: str  # lld: §3.2
    model: str  # lld: §3.2
    model_year: int = Field(ge=1980, le=2099)  # lld: §3.2
    engine_displacement_liters: float = Field(gt=0, le=10.0)  # lld: §3.2
    cylinder_count: int = Field(ge=2, le=12)  # lld: §3.2
    number_of_banks: int = Field(ge=1, le=2)  # lld: §3.2
    induction_type: InductionType  # lld: §3.2
    fuel_delivery_type: FuelDeliveryType  # lld: §3.2
    air_metering_architecture: AirMeteringArchitecture  # lld: §3.2
    air_metering_strategy: AirMeteringStrategy  # lld: §3.2
    emissions: EmissionsConfiguration  # lld: §3.2
    euro_emission_category: EuroEmissionCategory  # lld: §3.2
    stress_idle_rpm_target: int = Field(ge=2800, le=5000)  # lld: §3.2
    rated_rpm: int | None = Field(default=None, ge=1500, le=12000)  # lld: §3.2
    confidence: VinConfidence  # lld: §3.2
    resolved_horizon: Horizon  # lld: §3.2 — pre-computed by DNALab per NewArchPlan §2

    @model_validator(mode='after')
    def _air_metering_consistency(self) -> VinDNA:
        """ERR-CONTRACT-002: air_metering_strategy must be consistent with
        air_metering_architecture sensor booleans.  # lld: §10
        """
        strategy = self.air_metering_strategy
        arch = self.air_metering_architecture
        if strategy == AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK:
            if not arch.has_maf_sensor or not arch.has_map_sensor:
                raise ValueError(
                    "air_metering_strategy=DUAL_MAF_MAP_CROSSCHECK requires "
                    "has_maf_sensor=True and has_map_sensor=True (ERR-CONTRACT-002)"
                )
        elif strategy == AirMeteringStrategy.MAF_ONLY:
            if not arch.has_maf_sensor:
                raise ValueError(
                    "air_metering_strategy=MAF_ONLY requires has_maf_sensor=True "
                    "(ERR-CONTRACT-002)"
                )
        elif strategy == AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY:
            if not arch.has_map_sensor:
                raise ValueError(
                    "air_metering_strategy=MAP_ONLY_SPEED_DENSITY requires "
                    "has_map_sensor=True (ERR-CONTRACT-002)"
                )
        return self


class VehicleDNA(BaseModel):
    """Top-level vehicle identity payload. Mirror of DNALab output.

    Source: lld: §3.2.
    """

    session_id: UUID4  # lld: §3.2
    timestamp: datetime  # lld: §3.2
    schema_version: str = Field(pattern=r"^\d+\.\d+$")  # lld: §3.2
    vin_dna: VinDNA  # lld: §3.2
    symptom_dna: dict | None = None  # lld: §3.2 — back-compat; new code reads top-level


class SessionMetadata(BaseModel):
    """Per-session context. Cylinder count and horizon come from Script 1."""

    session_id: UUID4
    vin_dna_string: str = Field(..., min_length=17, max_length=17)
    resolved_horizon: str  # "HORIZON_LEGACY" | "HORIZON_ADAPTIVE" | "HORIZON_MODERN"
    cylinder_count: int = Field(..., ge=2, le=12)
    air_metering_strategy: AirMeteringStrategy | None = None
    # wiki: 02_lab_input_contract.md §4 CONCEPT_DNA_INPUT; consumer:
    # fault_atlas_router.execute_triage_loop VE circularity gate.
    schema_version: str = Field(default="1.0", pattern=r"^\d+\.\d+$")  # lld: §6.3 — MIN_SUPPORTED_SCHEMA_VERSION gate
    vin_confidence: VinConfidence = Field(default=VinConfidence.HIGH)  # lld: §10 — ERR-ABORT-004 gate


class GasLabPayload(BaseModel):
    """Output fragment produced by the GasLab module (gas_lab_fresh package).

    ``chemical_state`` is the 34-value canonical fault label (ChemicalSignature).
    ``sample_validity`` is the triangle-gate verdict consumed by COMLab's
    lab-pipeline aggregator Stage A fatal gate (ERR-ABORT-001 when INVALID).
    """

    chemical_state: str
    gas_co: float = Field(..., ge=0.0, le=15.0)
    gas_hc: int = Field(..., ge=0, le=20000)
    gas_co2: float = Field(..., ge=0.0, le=22.0)   # added v1.1, 2026-05-19
    gas_o2: float = Field(..., ge=0.0, le=22.0)
    gas_nox: int = Field(..., ge=0, le=5000)       # added v1.1, 2026-05-19
    lambda_chem: float = Field(..., ge=0.5, le=2.5)
    sample_validity: SampleValidity
    lambda_measured: float | None = Field(
        default=None, ge=0.5, le=2.0
    )  # vocab: GAS_VOCABULARY §2/§6 — optional directly-measured analyser λ;
       # consumer: perception_contradiction.select_perception_lambda (T-FX-7 no-OBD path)
    high_idle_hc: int | None = Field(
        default=None, ge=0, le=20000
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_co: float | None = Field(
        default=None, ge=0.0, le=15.0
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_co2: float | None = Field(
        default=None, ge=0.0, le=22.0
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_o2: float | None = Field(
        default=None, ge=0.0, le=22.0
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_nox: int | None = Field(
        default=None, ge=0, le=5000
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_lambda: float | None = Field(
        default=None, ge=0.5, le=2.5
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    decel_co_pct: float | None = Field(default=None, ge=0.0)
    pre_post_cat_hc_delta_ppm: float | None = Field(default=None, ge=0.0)
    pre_post_cat_co_delta_pct: float | None = Field(default=None, ge=0.0)


class FreezeFramePIDs(BaseModel):
    """Snapshot variables captured by the ECU when a DTC was set.

    Modern cars produce these reliably. Legacy cars often do not — the
    aggregator's fallback tree handles None defaults.
    """

    calculated_engine_load_pct: float = Field(0.0, ge=0.0, le=100.0)
    freeze_frame_misfire_cylinder: int | None = None
    freeze_frame_engine_rpm: int = Field(0, ge=0)
    o2_voltage: float | None = Field(
        default=None, ge=0.0, le=1.5
    )  # consumer: SF-001/002/003/007; freeze-frame b1s1 O2 voltage, not OBDLiveDataPayload analytics
    o2_downstream: float | None = Field(
        default=None, ge=0.0, le=1.5
    )  # consumer: SF-006; freeze-frame downstream O2 voltage, not OBDLiveDataPayload analytics


# ---------------------------------------------------------------------------
# DTCLab mirror types — JSON-only boundary, no cross-lab imports
# ---------------------------------------------------------------------------


class FreezeFrameRecord(BaseModel):
    """Mode $02 freeze-frame snapshot captured at DTC confirmation.

    Mirror of DTCLab's ``FreezeFrameRecord`` (JSON-only boundary).
    12 mandatory PIDs (§12.1), 7 optional extended PIDs (§12.2),
    6 derived symptom flags (§12.3).

    Source: DTC_VOCABULARY.md §12.
    """

    # -- mandatory PIDs (§12.1) --------------------------------------------

    calculated_load_pct: float = Field(ge=0.0, le=100.0)
    engine_rpm: int = Field(ge=0)
    coolant_temp_c: float
    short_term_ft1: float
    long_term_ft1: float
    manifold_pressure_kpa: float = Field(ge=0.0)
    vehicle_speed_kmh: int = Field(ge=0)
    ignition_advance_deg: float
    intake_air_temp_c: float
    maf_gps: float = Field(ge=0.0)
    throttle_pos_pct: float = Field(ge=0.0, le=100.0)
    fuel_system_status: FuelSystemStatus

    # -- extended PIDs (§12.2, all optional) -------------------------------

    short_term_ft2: float | None = None
    long_term_ft2: float | None = None
    o2_voltage_b1s1: float | None = None
    barometric_pressure_kpa: float | None = None
    commanded_egr_pct: float | None = None
    run_time_since_start_sec: int | None = None
    fuel_level_pct: float | None = None

    # -- derived symptom flags (§12.3) -------------------------------------

    ff_open_loop_at_fault: bool = False
    ff_load_high_at_low_rpm: bool = False
    ff_ect_warmup: bool = False
    ff_iat_ect_biased: bool = False
    ff_timing_retard_severe: bool = False
    ff_codes_cleared_invalidated: bool = False
    ff_fuel_spark_cut_at_crank: bool = False
    # consumer: fault_atlas_router no-start branch — T-COMV2-NOSTART-1


class Mode06MonitorResult(BaseModel):
    """Single Mode $06 on-board monitor test result.

    Mirror of DTCLab's ``Mode06MonitorResult`` (JSON-only boundary).

    Source: DTC_VOCABULARY.md §13.
    """

    monitor_id: str = Field(pattern=r"^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$")
    state: Mode06MonitorState
    margin_pct: float
    target_component: str


class DTCLabPayload(BaseModel):
    """Output fragment from the DTC Lab — full payload.

    Replaces the v0.1 stub (active_mil + confirmed_dtcs only). Every field
    has a named consumer in ``fault_atlas_router.py`` §4 Stage B or COMLab
    confidence scoring.

    Source: DTC_VOCABULARY.md §11.
    """

    active_mil: bool
    mil_flashing: bool
    confirmed_dtcs: list[str] = Field(default_factory=list)
    pending_dtcs: list[str] = Field(default_factory=list)
    permanent_dtcs: list[str] = Field(default_factory=list)
    routing_tags: list[DTCRoutingTag] = Field(default_factory=list)
    mode_06_monitors: dict[str, Mode06MonitorResult] = Field(default_factory=dict)
    historical_fault_context: HistoricalFaultContext
    freeze_frame: FreezeFrameRecord

    # -- validators --------------------------------------------------------

    @field_validator("confirmed_dtcs", "pending_dtcs", "permanent_dtcs")
    @classmethod
    def _validate_dtc_list(cls, v: list[str]) -> list[str]:
        """Every DTC string must match DTC_REGEX (wiki: DTC_VOCABULARY §2.3)."""
        compiled = re.compile(DTC_REGEX)
        for code in v:
            if not compiled.match(code):
                raise ValueError(
                    f"DTC {code!r} does not match {DTC_REGEX} (ERR-CONTRACT-001)"
                )
        return v


class OBDLiveDataPayload(BaseModel):
    """Output fragment from the OBD Live Lab.

    Carries the computed analytics fields OBDLab produces and COMLab's
    fault-atlas router consumes. Raw STFT/LTFT are replaced by the aggregated
    ``total_trim_correction_delta`` — COMLab does not re-aggregate what OBDLab
    already owns.

    Every field has a named consumer in ``fault_atlas_router.py``:
      - total_trim_correction_delta → rich/lean differential diagnosis
      - total_trim_correction_delta_b2 + lambda_perception_delta → ECU fuse
      - normalized_obd_lambda → perception-contradiction cross-check vs lambda_chem
      - ve_pct + ve_validity → VE fault verdicts (collapse, contamination, skew)
      - rpm_state_bucket → evidence weighting per operating regime
      - trim_analytics_gate → suppresses trim findings when blocked
      - fuel_system_status → suppresses trim evidence outside closed loop
      - o2_failure_mode → gates trim-based findings when O2 has failed
      - maf_status / map_status → provenance flags for VE evidence weight
      - intake_air_temp_c + throttle_pos_pct → ECU hardware-lie checker
    """

    engine_warmed: bool
    total_trim_correction_delta: float = Field(..., ge=-254.0, le=254.0)
    # Widened from [-200, 200] to [-254, 254] per T-W-6 — railed OBD trim values
    # (±127 each for STFT + LTFT) sum to ±254. The consumer (fault_atlas_router
    # trim-evidence scoring) gates on railed-trim patterns.
    total_trim_correction_delta_b2: float | None = None
    # consumer: fault_atlas_router ecu_fault fuse — T-COMV2-ECU-FUSE-1
    lambda_perception_delta: float | None = None
    # consumer: fault_atlas_router ecu_fault fuse — T-COMV2-ECU-FUSE-1
    per_bank_trim_delta: float | None = None
    # consumer: fault_atlas_router bank-asymmetry verdict — T-COMV2-BANK-FUSE-1
    per_cylinder_misfire_counts: dict[int, int] | None = Field(
        default=None
    )  # consumer: fault_atlas_router misfire localiser — T-COMV2-MISFIRE-LOC-1
    ltft_cell_vector: dict[int, float] | None = Field(
        default=None
    )  # consumer: fault_atlas_router load-cell LTFT classification — T-COMV2-LTFT-CELL-1
    control_module_voltage_v: float | None = Field(
        default=None, ge=0.0, le=18.0  # wiki: 02_lab_input_contract.md §2a
    )  # consumer: perception_contradiction.detect — T-COMV2-VPWR-GATE-1
    w_theo: float | None = Field(
        default=None
    )  # consumer: fault_atlas_router Phase 5 linearity ladder — T-COMV2-MAF-LIN-1
    sensor_error_delta: float | None = Field(
        default=None
    )  # consumer: fault_atlas_router Phase 5 linearity ladder — T-COMV2-MAF-LIN-1
    shrtft1: float | None = Field(
        default=None, ge=-127.0, le=127.0
    )  # OBDLab_KG_Wiki rail; consumer: SF-008, EF-001/002/003
    longft1: float | None = Field(
        default=None, ge=-127.0, le=127.0
    )  # OBDLab_KG_Wiki rail; consumer: SF-008, EF-001/002/003
    mass_airflow_gps: float | None = Field(
        default=None, ge=0.0, le=655.35
    )  # OBDLab_KG_Wiki; consumer: SF-004
    manifold_vacuum_kpa: float | None = Field(
        default=None, ge=0.0, le=255.0
    )  # OBDLab_KG_Wiki; held from map_kpa until absolute-MAP scalar is resolved
    coolant_temp_c: float | None = Field(
        default=None, ge=-40.0, le=140.0
    )  # OBDLab_KG_Wiki; consumer: SF-006
    intake_air_temp_c: float | None = Field(
        default=None, ge=-40.0, le=140.0
    )  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
    # consumer: ecu_hardware_checker.ECUHardwareChecker — T-COMV2-ECU-HW-1
    throttle_pos_pct: float | None = Field(
        default=None, ge=0.0, le=100.0
    )  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
    # consumer: ecu_hardware_checker.ECUHardwareChecker — T-COMV2-ECU-HW-1
    normalized_obd_lambda: float | None = Field(
        default=None, ge=0.7, le=1.3
    )  # lld: §3.2 — None when OBD channel absent (legacy/Euro 1-2 no-OBD sessions)
    ve_pct: float = Field(..., ge=0.0, le=200.0)
    # wiki: OBDLab_KG_Wiki §6.4 — thermal-shock steam overshoot may exceed 100 %.
    ve_validity: VEValidity
    rpm_state_bucket: EngineStateBucket
    trim_analytics_gate: TrimAnalyticsGate
    fuel_system_status: FuelSystemStatus | None = None
    # consumer: fault_atlas_router fuel-system closed-loop gate — T-COMV2-FUELSYS-GATE-1
    o2_failure_mode: O2FailureMode
    maf_status: NodeMAFStatus
    map_status: NodeMAPStatus
    freeze_frame_pids: FreezeFramePIDs | None = None
    mode06_catalyst_margin_pct: float | None = Field(default=None)
    catalyst_index_ratio: float | None = Field(default=None, ge=0.0)
    stft_idle_pct: float | None = Field(default=None, ge=-127.0, le=127.0)
    ltft_idle_pct: float | None = Field(default=None, ge=-127.0, le=127.0)
    stft_2500_pct: float | None = Field(default=None, ge=-127.0, le=127.0)
    ltft_2500_pct: float | None = Field(default=None, ge=-127.0, le=127.0)
    mode06_o2_response_margin_pct: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim SensorDynamicsState O2_LAZY_OR_BIASED branch — T-V3-P4-C6B
    maf_actual_calc_delta_pct_idle: float | None = Field(default=None)
    # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch — T-V3-P4-C6B
    maf_actual_calc_delta_pct_2500: float | None = Field(default=None)
    # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch — T-V3-P4-C6B
    maf_gps_idle: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch — T-V3-P4-C6B
    maf_gps_2500: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch — T-V3-P4-C6B
    calc_airflow_gps_idle: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch — T-V3-P4-C6B
    calc_airflow_gps_2500: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch — T-V3-P4-C6B
    koeo_map_baro_delta_kpa: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch — T-V3-P4-C3B
    module_voltage_loaded_v: float | None = Field(default=None, ge=0.0, le=18.0)
    # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch — T-V3-P4-C3B
    dlc_signal_ground_drop_v: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch — T-V3-P4-C3B
    bidirectional_fuel_response_ok_bool: bool | None = Field(default=None)
    # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch — T-V3-P4-C3B
    stft_load_pct: float | None = Field(default=None, ge=-127.0, le=127.0)
    # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
    ltft_load_pct: float | None = Field(default=None, ge=-127.0, le=127.0)
    # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
    calc_load_wot_pct: float | None = Field(default=None, ge=0.0, le=100.0)
    # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
    fuel_rail_pressure_load_kpa: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
    wideband_lambda_wot: float | None = Field(default=None, ge=0.0)
    # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
    # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
    co2_idle_pct: float | None = Field(default=None)
    # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
    tailpipe_o2_elevation_pct: float | None = Field(default=None)
    # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
    downstream_o2_v: float | None = Field(default=None)
    # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
    propane_trim_shift_pct: float | None = Field(default=None)
    readiness_supported_complete_bool: bool | None = Field(default=None)
    # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
    stored_dtc_count: int | None = Field(default=None, ge=0)
    # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
    pending_dtc_count: int | None = Field(default=None, ge=0)
    # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
    permanent_dtc_count: int | None = Field(default=None, ge=0)
    # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
    mode06_min_margin_pct: float | None = Field(default=None)
    # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
    warmup_cycles_since_clear: int | None = Field(default=None, ge=0)
    # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
    miles_since_clear: int | None = Field(default=None, ge=0)
    # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B


class SecondOperatingPointFrame(BaseModel):
    """Optional elevated/"stress" operating-point snapshot for two-point delta diagnosis.

    Additive and default-absent: when ``OrchestratorInboundRequest.second_operating_point``
    is ``None`` the engine takes the byte-identical single-point path. When present, COMLab's
    stateless ``analytics/delta_engine.py`` differences this frame against the primary (low-idle)
    channels carried on ``gas_lab_output`` / ``obd_live_data`` and emits a ``delta_signature``.

    Per-signal bands (the frame carries its own ``rpm_state_bucket`` so each check can ABSTAIN on
    a band mismatch rather than differencing against a baseline measured at a different RPM):
      - ΔTrim is validated against ``STRESS_IDLE`` (3500-4500).      # wiki: delta-relations/01
      - Δgas / ΔO2 are validated against ``REGULATORY_HIGH_IDLE``.   # wiki: delta-relations/07

    Mirror-typed over the JSON boundary — no cross-lab imports. The emitters stay stateless and
    single-point; the cross-state delta math is COMLab's (T-COMV2-DELTA-1).

    Source: delta-relations/01-08; research/PROPOSAL_DeltaLab_cross_lab_delta_module.md.
    """

    rpm_state_bucket: EngineStateBucket  # wiki: delta-relations/01 (ΔTrim @3500-4500) + /07 (Δgas @~2500)
    engine_rpm: int = Field(..., ge=0)

    # -- ΔTrim channel (delta-relations/01-05); bounds mirror OBDLiveDataPayload --
    total_trim_correction_delta: float | None = Field(default=None, ge=-254.0, le=254.0)  # wiki: delta-relations/01
    shrtft1: float | None = Field(default=None, ge=-127.0, le=127.0)  # wiki: delta-relations/01
    longft1: float | None = Field(default=None, ge=-127.0, le=127.0)  # wiki: delta-relations/01

    # -- Δgas channel (delta-relations/07); bounds mirror GasLabPayload --
    gas_hc: int | None = Field(default=None, ge=0, le=20000)  # wiki: delta-relations/07
    gas_co: float | None = Field(default=None, ge=0.0, le=15.0)  # wiki: delta-relations/07
    gas_co2: float | None = Field(default=None, ge=0.0, le=22.0)  # wiki: delta-relations/07
    gas_o2: float | None = Field(default=None, ge=0.0, le=22.0)  # wiki: delta-relations/07
    gas_nox: int | None = Field(default=None, ge=0, le=5000)  # wiki: delta-relations/07
    lambda_chem: float | None = Field(default=None, ge=0.5, le=2.5)  # wiki: delta-relations/07

    # -- validity inputs for the second reading (delta-relations/08) --
    sample_validity: SampleValidity | None = None  # wiki: delta-relations/08 — vsum/dilution gate on this frame
    rpm_stable: bool = True  # wiki: delta-relations/08 — RPM must have settled before a delta is trusted

    # -- ΔO2 components (named-only; o2-logic deltas not yet quantified — passthrough, never set a profile) --
    o2_switch_freq_hz: float | None = Field(default=None, ge=0.0)  # wiki: SWEEP_MANIFEST §7 Δf_switch (feeder)
    o2_voltage_bias_v: float | None = Field(default=None, ge=0.0, le=1.5)  # wiki: SWEEP_MANIFEST §7 ΔV_bias (feeder)
    o2_downstream_response: float | None = None  # wiki: SWEEP_MANIFEST §7 ΔTI_downstream (feeder)

    # -- architecture-gate inputs (delta-relations/06): carried here because the router's request
    #    has no VinDNA, and the gate is MANDATORY before any ΔTrim profile is applied --
    air_metering_strategy: AirMeteringStrategy | None = None  # wiki: delta-relations/06 — MAP-only nulls ΔTrim for a real leak
    induction_type: InductionType | None = None  # wiki: delta-relations/06 — forced induction inverts ΔTrim sign


class UserInputEchoFieldGroup(BaseModel):
    """One wizard screen's worth of typed values.

    Consumer: PRD §5.5 — render echo audit on Screen 6.

    Source: lld: §3.3.
    """

    screen_id: Literal["vehicle_context", "gas", "obd", "dtc"]  # lld: §3.3
    label: str  # lld: §3.3
    fields: dict[str, Any]  # lld: §3.3 — key = wizard field name, value = raw typed value or None


class UserInputEchoAudit(BaseModel):
    """COMLab-emitted pass-through audit of wizard inputs.

    COMLab does not generate the echo — it carries it through verbatim.
    If omitted, Stage D emits a sentinel with submitted_at=<now> and groups=[].

    Consumer: PRD §5.5 — render echo audit on Screen 6.

    Source: lld: §3.3.
    """

    submitted_at: datetime  # lld: §3.3
    groups: list[UserInputEchoFieldGroup]  # lld: §3.3


class OrchestratorInboundRequest(BaseModel):
    """The complete ingestion payload accepted by ComLab.

    This is the only inbound schema. Adapters produce instances of this;
    callers using raw JSON validate against it.
    """

    metadata: SessionMetadata
    gas_lab_output: GasLabPayload
    obd_live_data: OBDLiveDataPayload | None = None
    dtc_lab_output: DTCLabPayload | None = None
    symptom_dna: dict = Field(default_factory=dict)
    downstream_trim_role: DownstreamTrimRole = Field(default=DownstreamTrimRole.NONE)  # lld: §3.2 — O2_MODEL_STRATEGY.md §3; populated by T-FX-10
    has_catalyst: bool = True  # lld: §3.2 — O2_MODEL_STRATEGY.md §9.1; populated by T-FX-11
    user_input_echo_audit: UserInputEchoAudit | None = None  # lld: §3.2 -- pass-through from assembler
    second_operating_point: SecondOperatingPointFrame | None = None
    # T-COMV2-DELTA-1 — additive; absent → byte-identical single-point path. wiki: delta-relations/01-08
    # consumer: comlab/analytics/delta_engine.py:DeltaEngine.compute_delta_signature -> fault_atlas_router Phase 5
