"""COMLab canonical enum vocabulary.

Single Python source of truth for cross-lab enum values consumed across
VINLab, GASLab, OBDLab, DTCLab, and COMLab. Every enum value is mechanically
traceable to its cited vocabulary file in ``docs/Vocabulary/``; the drift-guard
test in ``tests/unit/test_vocabulary.py`` enforces that traceability.

The enum **value** (the string literal) is the wire format consumed across
lab JSON boundaries — renames of values are breaking changes to the
SEMANTIC_CONTRACT (§10).

Phase 0b — T-P0b-1 seeded the architecture pair (Horizon, EuroEmissionCategory);
T-P0b-2 appends the three VIN-driven polymorphic switches (AirMeteringStrategy,
O2SensorType, EngineStateBucket); T-P0b-3 appends the four fault-classification
enums (FaultFamily, ChemicalSignature, O2FailureMode, HistoricalFaultContext);
T-P0b-4 appends the five DTC enums (DTCRoutingTag, DTCFallbackStrategy,
DTCSeverityClass, DTCState, Mode06Status); T-P0b-5 appends the four
orchestrator-output enums (ConfidenceRating, VinConfidence, DegradationMode,
SeverityLevel).
Subsequent tasks (T-P0b-7) extend this module with the remaining
items per ``_comlab_skills/comlab-vocabulary/SKILL.md`` §3.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

DTC_REGEX: Final[str] = r"^[BCPU][0-3][0-9A-F]{3}$"  # ISO 15031-6 §5.2 (≡ SAE J2012) / DTC_VOCABULARY §2.3


__all__ = [
    "AirMeteringStrategy",
    "ChemicalSignature",
    "ConfidenceRating",
    "DegradationMode",
    "DownstreamTrimRole",
    "DTCFallbackStrategy",
    "DTC_REGEX",
    "DTCRoutingTag",
    "DTCSeverityClass",
    "DTCState",
    "EngineStateBucket",
    "EuroEmissionCategory",
    "FaultEnrichmentSeverity",
    "FaultFamily",
    "HistoricalFaultContext",
    "Horizon",
    "LabRoutingDirectiveReason",
    "Mode06Status",
    "NodeMAFStatus",
    "NodeMAPStatus",
    "O2FailureMode",
    "PrimaryLoadCalculation",
    "O2SensorType",
    "RpmStateBucket",
    "SampleValidity",
    "SeverityLevel",
    "TrimAnalyticsGate",
    "VEValidity",
    "FuelDeliveryType",
    "FuelSystemStatus",
    "InductionType",
    "Mode06MonitorState",
    "LabRoutingDirective",
    "UpstreamO2Type",
    "VinConfidence",
]


class Horizon(StrEnum):
    """Architecture horizon resolved from the VIN's emission category.

    Used by COMLab for fault-registry pruning. Mapped from
    ``EuroEmissionCategory`` by DNALab per SEMANTIC_CONTRACT.md §6.4.

    Source: OBD_VOCABULARY.md §7.
    """

    LEGACY = "HORIZON_LEGACY"      # Euro 1-2, 1990-2000 — pre-OBD-II / early OBD-II
    ADAPTIVE = "HORIZON_ADAPTIVE"  # Euro 3-4, 2000-2010 — full OBD-II, narrowband O2
    MODERN = "HORIZON_MODERN"      # Euro 5-6, 2010-2020 — wideband O2, GDI, GPF


class EuroEmissionCategory(StrEnum):
    """Euro emission tier emitted by VINLab in ``VinDNA.euro_emission_category``.

    Drives Gas Lab threshold masks (max allowed CO/HC/NO_x per category) and
    feeds the ``Horizon`` mapping in DNALab.

    Source: OBD_VOCABULARY.md §4.1.
    """

    EURO_1 = "EURO_1"  # 1992 onward — first EU emission standard
    EURO_2 = "EURO_2"  # 1996 onward
    EURO_3 = "EURO_3"  # 2000 onward — OBD-II mandated in EU
    EURO_4 = "EURO_4"  # 2005 onward
    EURO_5 = "EURO_5"  # 2009 onward — DPF/GPF era begins
    EURO_6 = "EURO_6"  # 2014 onward — current mainstream
    EURO_7 = "EURO_7"  # 2025+ — future-facing slot


class AirMeteringStrategy(StrEnum):
    """VIN-driven air-metering switch — solves the "missing MAP sensor" problem.

    Emitted by VINLab in ``VinDNA.air_metering_strategy``. OBDLab's Volumetric
    Efficiency calculation dynamically routes to the matching formula per the
    3-Way Polymorphic Math Routing Matrix (OBDLab BP §3.1).

    Source: OBD_VOCABULARY.md §4.2.
    """

    DUAL_MAF_MAP_CROSSCHECK = "DUAL_MAF_MAP_CROSSCHECK"  # both MAF and MAP present — cross-check both
    MAP_ONLY_SPEED_DENSITY = "MAP_ONLY_SPEED_DENSITY"    # no MAF — speed-density emulation via MAP
    MAF_ONLY = "MAF_ONLY"                                # no MAP — infer manifold pressure via MAF


class O2SensorType(StrEnum):
    """VIN-driven upstream O2 sensor type — solves the "narrowband vs wideband" problem.

    Emitted by VINLab in ``VinDNA.upstream_o2_sensor_type``. OBDLab normalizes
    both sensor types to a common virtual node ``normalized_obd_lambda`` per
    OBDLab BP §3.2.

    Source: OBD_VOCABULARY.md §4.3.
    """

    NARROWBAND_0_TO_1V = "NARROWBAND_0_TO_1V"  # 0-1 V switching style, stoich-centered ~0.45 V
    WIDEBAND_LINEAR = "WIDEBAND_LINEAR"        # linear lambda / pumping-current style


class FuelDeliveryType(StrEnum):
    """VIN-driven fuel delivery type — polymorphic switch for fuel system routing.

    Emitted by VINLab in ``VinDNA.fuel_delivery_type``. Consumed by COMLab's
    projection layer and fault-atlas router for fuel-system fault gating.

    Source: SEMANTIC_CONTRACT.md §4; lld: §5.1 GasLabDnaView.
    """

    GDI = "GDI"                          # lld: §5.1 — direct injection, high-pressure pump
    PORT_INJECTION = "PORT_INJECTION"    # lld: §5.1 — multi-point port injection
    CARBURETOR = "CARBURETOR"            # lld: §5.1 — legacy carburetted, no injectors


class InductionType(StrEnum):
    """VIN-driven induction type — forced-induction gating for VE analytics.

    Emitted by VINLab in ``VinDNA.induction_type``. Consumed by COMLab's
    projection layer and VE analytics for boost-aware threshold selection.

    Source: SEMANTIC_CONTRACT.md §4; lld: §5.1 GasLabDnaView.
    """

    NATURALLY_ASPIRATED = "NATURALLY_ASPIRATED"  # lld: §5.1
    TURBOCHARGED = "TURBOCHARGED"                # lld: §5.1
    SUPERCHARGED = "SUPERCHARGED"                # lld: §5.1


class UpstreamO2Type(StrEnum):
    """VIN-driven upstream O2 sensor type — wider taxonomy than O2SensorType.

    Emitted by VINLab in ``VinDNA.upstream_o2_type``. Consumed by COMLab's
    projection layer. Differs from ``O2SensorType`` (which is the OBDLab
    normalised two-way switch); this enum captures the physical sensor
    technology including aftermarket wideband-in-narrowband-simulation.

    Source: SEMANTIC_CONTRACT.md §4; lld: §5.1 GasLabDnaView, ObdLabDnaView.
    """

    NARROWBAND = "NARROWBAND"                # lld: §5.1 — factory 0-1 V zirconia
    WIDEBAND_AFR = "WIDEBAND_AFR"            # lld: §5.1 — factory wideband, AFR output
    WIDEBAND_LAMBDA = "WIDEBAND_LAMBDA"      # lld: §5.1 — factory wideband, lambda output
    WIDEBAND_NB_SIM = "WIDEBAND_NB_SIM"      # lld: §5.1 — aftermarket WB simulating NB signal
    NONE = "NONE"                             # lld: §5.1 — no O2 sensor fitted (pre-catalyst era)


class DownstreamTrimRole(StrEnum):
    """Role of the downstream O2 sensor in the ECU's closed-loop strategy.

    COMLab mirror of a VINLab-owned type (JSON-only boundary — no cross-lab
    import). Consumed by the perception-contradiction detector to qualify
    O2-health verdicts: on a ``SECONDARY_FUEL_TRIM`` vehicle, an in-tolerance
    agreement between ``lambda_chem`` and ``normalized_obd_lambda`` is weak
    evidence of a healthy upstream sensor — the downstream loop may be actively
    masking drift.

    Source: O2_MODEL_STRATEGY.md §3; Osensorguide.md §2.
    """

    NONE = "NONE"  # wiki: O2_MODEL_STRATEGY.md §3 — no downstream sensor or role not assigned
    CATALYST_MONITOR_ONLY = "CATALYST_MONITOR_ONLY"  # wiki: O2_MODEL_STRATEGY.md §3 — cat efficiency monitor only
    SECONDARY_FUEL_TRIM = "SECONDARY_FUEL_TRIM"  # wiki: O2_MODEL_STRATEGY.md §3 — downstream drives secondary fuel-trim loop


class EngineStateBucket(StrEnum):
    """Engine operating regime — coarse RPM × load bucket used to gate analytics.

    OBDLab classifies each sample into one of these four buckets before running
    trim, lambda, or VE analytics. ``COLD_OPEN_LOOP_INVALID`` freezes all trim
    analytics regardless of RPM (ECT < 75 °C precondition not met).

    Source: OBD_VOCABULARY.md §3.3.
    """

    STABILIZED_IDLE = "STABILIZED_IDLE"                # 650-900 RPM, <30% load — closed-loop warm idle
    REGULATORY_HIGH_IDLE = "REGULATORY_HIGH_IDLE"      # 2200-2800 RPM, 15-40% load — two-speed idle test point
    STRESS_IDLE = "STRESS_IDLE"                        # 3500-4500 RPM (VIN-dependent), 40-60% load — clinical load test
    COLD_OPEN_LOOP_INVALID = "COLD_OPEN_LOOP_INVALID"  # ECT < 75 °C — trim analytics frozen


class FaultFamily(StrEnum):
    """Top-level fault classification emitted by COMLab's fault-atlas router.

    These labels map to the ``expected_top_fault_family`` column in the cases
    corpus and are the coarsest diagnostic bucket before the specific fault
    node is resolved.

    Source: OBD_VOCABULARY.md §6.
    """

    LEAN_CONDITION = "lean_condition"  # fuel system too lean — vacuum leak, low fuel pressure, MAF under-read
    RICH_MIXTURE = "rich_mixture"  # fuel system too rich — leaking injector, HPFP seal, regulator rupture
    MISFIRE = "misfire"  # ignition/mechanical combustion failure
    SENSOR_FAULT = "sensor_fault"  # O2 sensor bias/sluggish, MAF contamination, knock sensor drift
    ECU_FAULT = "ecu_fault"  # PCM internal error — memory checksum, 5V reference, driver circuit
    CATALYST_FAILURE = "catalyst_failure"  # lld: §3.1 — cat efficiency, meltdown, masking, lightoff
    EXHAUST_LEAK = "exhaust_leak"  # lld: §3.1 — pre/post-O2 physical exhaust breach, false-lean
    IGNITION_FAULT = "ignition_fault"  # lld: §3.1 — spark generation failure, pre-combustion
    MECHANICAL_WEAR = "mechanical_wear"  # lld: §3.1 — ring/bore/valve guide wear, head gasket; T-P6-2c KG family
    CAM_TIMING = "cam_timing"  # lld: §3.1 — chain/belt stretch, phaser failure, CKP/CMP misalignment; T-P6-2c KG family
    NON_STARTER = "non_starter"  # lld: §3.1 — won't start, no exhaust gas; T-P6-2d KG family
    NO_FAULT = "no_fault"  # all diagnostics pass; no anomaly detected


class ChemicalSignature(StrEnum):
    """34 canonical chemical fingerprints emitted by GASLab in ``chemical_state``.

    COMLab consumes these as opaque labels and routes through the fault registry
    per the DTC reverse-lookup table in DTC_VOCABULARY.md §13.

    Owned by GASLab; COMLab is a consumer. Adding a value is a minor-version
    contract bump (SEMANTIC_CONTRACT.md §10).

    Source: OBD_VOCABULARY.md §17.
    """

    NORMAL_OPERATION = "NORMAL_OPERATION"  # all gases within healthy stoichiometric window
    RICH_MIXTURE = "RICH_MIXTURE"  # lambda < 0.98 — excess fuel
    LEAN_MIXTURE = "LEAN_MIXTURE"  # lambda > 1.02 — excess air
    IGNITION_MISFIRE = "IGNITION_MISFIRE"  # unburned fuel + O2 spike — spark/coil failure
    LEAN_MISFIRE = "LEAN_MISFIRE"  # misfire with lean chemistry signature
    RICH_MISFIRE = "RICH_MISFIRE"  # misfire with rich chemistry signature
    EXHAUST_AIR_LEAK = "EXHAUST_AIR_LEAK"  # post-combustion air ingress — pre-probe exhaust leak
    HIGH_COMBUSTION_TEMP = "HIGH_COMBUSTION_TEMP"  # elevated NOx — over-advanced timing, cooling issue
    CATALYST_NOT_LIGHTING_OFF = "CATALYST_NOT_LIGHTING_OFF"  # cat below light-off temp post-warmup
    CATALYST_OVERWHELMED = "CATALYST_OVERWHELMED"  # raw fuel hitting cat — misfire upstream
    SAMPLE_INVALID = "SAMPLE_INVALID"  # CO+CO2+O2 not in [14,18]% — probe leak or analyzer fault
    TIMING_OVER_ADVANCED = "TIMING_OVER_ADVANCED"  # excessive spark advance — high NOx, knock risk
    TIMING_RETARDED = "TIMING_RETARDED"  # insufficient spark advance — high HC, low power
    O2_SENSOR_BIASED_LOW = "O2_SENSOR_BIASED_LOW"  # sensor reads artificially lean — silicone poisoning
    O2_SENSOR_BIASED_HIGH = "O2_SENSOR_BIASED_HIGH"  # sensor reads artificially rich
    WORN_ENGINE = "WORN_ENGINE"  # rings/bore/valve guide wear — POA + low compression
    FLAT_CAMSHAFT = "FLAT_CAMSHAFT"  # worn cam lobe — reduced valve lift, misfire under load
    GDI_INTAKE_VALVE_CARBON = "GDI_INTAKE_VALVE_CARBON"  # carbon buildup on intake valves — GDI only
    VACUUM_REGULATOR_DIAPHRAGM_RUPTURE = "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE"  # FPR diaphragm — raw fuel into manifold
    GDI_HPFP_INTERNAL_SEAL_LEAK = "GDI_HPFP_INTERNAL_SEAL_LEAK"  # HPFP seal — fuel in oil, P2196
    WORN_VALVE_SEALS = "WORN_VALVE_SEALS"  # oil past valve guides — blue smoke on startup
    WORN_PISTON_RINGS = "WORN_PISTON_RINGS"  # blow-by + oil consumption — blue smoke under load
    POA_SIGNATURE = "POA_SIGNATURE"  # HC normal-high, CO low, lambda ~1 — oil burning
    CAM_TIMING_RETARDED_MAP = "CAM_TIMING_RETARDED_MAP"  # vocab: GAS_VOCABULARY §3 — cam phasing retarded, MAP-sensed; consumer: fault_atlas_router cam_timing family (ERR-CT-001)
    CAM_TIMING_RETARDED_MAF = "CAM_TIMING_RETARDED_MAF"  # vocab: GAS_VOCABULARY §3 — cam phasing retarded, MAF-sensed; consumer: fault_atlas_router cam_timing family (MAF follow-up T-COM-CAMTIMING-MAF-1)
    CAM_TIMING_ADVANCED = "CAM_TIMING_ADVANCED"  # vocab: GAS_VOCABULARY §3 — cam phasing advanced; consumer: fault_atlas_router cam_timing family
    EGR_STUCK_CLOSED = "EGR_STUCK_CLOSED"  # EGR valve not opening — high NOx, normal HC/CO
    EGR_STUCK_OPEN = "EGR_STUCK_OPEN"  # EGR valve not closing — rough idle, lean at cruise
    VVT_FAILURE = "VVT_FAILURE"  # variable valve timing phaser stuck — P0010-P0016
    EVAP_CANISTER_SATURATED = "EVAP_CANISTER_SATURATED"  # charcoal canister saturated — fuel vapor at idle
    EGR_DILUTION_MISFIRE = "EGR_DILUTION_MISFIRE"  # vocab: GAS_VOCABULARY §3 — EGR dilution causing misfire; consumer: fault_atlas_router EGR_HISTORY tag injection
    INCOMPLETE_OXIDATION = "INCOMPLETE_OXIDATION"  # vocab: GAS_VOCABULARY §3 — incomplete combustion; consumer: fault_atlas_router confidence capping → multi-candidate branch
    INCOMPLETE_COMBUSTION = "INCOMPLETE_COMBUSTION"  # vocab: GAS_VOCABULARY §3 — compression-loss partial combustion; consumer: mechanical_wear + non_starter families
    COOLANT_LEAK_INTERNAL = "COOLANT_LEAK_INTERNAL"  # vocab: GAS_VOCABULARY §3 — coolant-in-combustion-chamber; consumer: ERR-MW-002


class SampleValidity(StrEnum):
    """Triangle-gate verdict emitted by GASLab in ``GasLabPayload.sample_validity``.

    COMLab's lab-pipeline aggregator Stage A fatal gate checks this field to
    trigger ``ERR-ABORT-001`` when the sample is invalid. Mirrored from GASLab
    (JSON-only boundary — no cross-lab import).

    Source: GAS_VOCABULARY §5; mirrored in OBD_VOCABULARY.md §5.
    """

    VALID = "VALID"  # CO+CO2+O2 in [14, 16] — sample is clean
    BORDERLINE = "BORDERLINE"  # in [14, 15] or [15.5, 16] — borderline, treat as valid
    INVALID = "INVALID"  # < 14 or > 18 — halts evaluation, ERR-ABORT-001
    EXTERNAL_O2_SUSPECT = "EXTERNAL_O2_SUSPECT"  # in (16, 18] — warn but continue


class O2FailureMode(StrEnum):
    """O2 sensor failure taxonomy.

    Maps to the thresholds in ``OBD_VOCABULARY.md`` §12.4 and is consumed by
    OBDLab's ``normalized_obd_lambda`` pipeline and COMLab's perception-
    contradiction detector.

    Source: OBD_VOCABULARY.md §12.4.
    """

    NO_FAULT            = "NO_FAULT"            # wiki: §6.7 — healthy baseline, no fault detected
    STUCK_LEAN          = "STUCK_LEAN"          # wiki: §6.7 — pinned < 0.2 V (narrowband)
    STUCK_RICH          = "STUCK_RICH"          # wiki: §6.7 — pinned > 0.85 V (narrowband)
    WIDEBAND_OFFSET_CANDIDATE = "WIDEBAND_OFFSET_CANDIDATE"  # wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08


class HistoricalFaultContext(StrEnum):
    """Operating context at the moment a historical DTC was set.

    DTC Lab emits this classification from freeze-frame data. COMLab uses it
    to bias differential diagnosis — an idle-trim fault with
    ``HISTORICAL_LOAD_FAULT`` context suggests a fuel delivery issue, while
    ``HISTORICAL_IDLE_FAULT`` with lean trims points to a vacuum leak.

    Source: OBD_VOCABULARY.md §14.
    """

    HISTORICAL_IDLE_FAULT = "HISTORICAL_IDLE_FAULT"  # ff_engine_speed < 1000 AND ff_calculated_load < 25.0
    HISTORICAL_LOAD_FAULT = "HISTORICAL_LOAD_FAULT"  # ff_engine_speed > 2000 AND ff_calculated_load > 45.0
    COLD_START_TRANSIT_FAULT = "COLD_START_TRANSIT_FAULT"  # ff_coolant_temp < 60 °C
    UNKNOWN = "UNKNOWN"  # freeze-frame data insufficient for classification


class VEValidity(StrEnum):
    """VE cross-check validity emitted by OBDLab in ``OBDLiveDataPayload.ve_validity``.

    COMLab's fault-atlas router uses this to gate VE-based findings — only
    ``VALID`` permits full VE evidence weight. Mirrored from OBDLab
    (JSON-only boundary — no cross-lab import).

    Source: OBD_VOCABULARY.md §5; OBDLab_KG_Wiki.md §6.4.
    """

    VALID = "VALID"  # VE within expected range for engine configuration
    FAULT_VE_IDLE_COLLAPSE = "FAULT_VE_IDLE_COLLAPSE"  # VE < 50% at STABILIZED_IDLE — vacuum leak or ring wear
    FAULT_MAF_CONTAMINATION = "FAULT_MAF_CONTAMINATION"  # VE < 65% at STRESS_IDLE + positive total trim
    FAULT_VE_SENSOR_SKEW = "FAULT_VE_SENSOR_SKEW"  # VE > 85% at idle on NA engine — sensor over-read
    UNKNOWN = "UNKNOWN"  # insufficient inputs to compute VE


class TrimAnalyticsGate(StrEnum):
    """Analytics precondition gate emitted by OBDLab in ``OBDLiveDataPayload.trim_analytics_gate``.

    COMLab's fault-atlas router suppresses trim-based verdicts when this gate
    is anything other than ``VALID``. Mirrored from OBDLab (JSON-only boundary).

    Source: OBD_VOCABULARY.md §5; OBDLab_KG_Wiki.md §6.5.
    """

    VALID = "VALID"  # all preconditions satisfied — trim analytics proceed
    ENGINE_COLD = "ENGINE_COLD"  # coolant_temp_c < 70 — engine not at operating temp
    OPEN_LOOP = "OPEN_LOOP"  # fuel_sys_status != Closed_Loop — no trim feedback
    O2_FAULT_ACTIVE = "O2_FAULT_ACTIVE"  # active P0130–P0161 — O2 sensor fault
    CKP_CMP_FAULT_ACTIVE = "CKP_CMP_FAULT_ACTIVE"  # active P0335 / P0340 — crank/cam sensor
    CODES_RECENTLY_CLEARED = "CODES_RECENTLY_CLEARED"  # < 1 drive cycle since codes cleared
    WOT_ACTIVE = "WOT_ACTIVE"  # throttle at wide-open — open-loop enrichment
    DFCO_ACTIVE = "DFCO_ACTIVE"  # decel fuel cut-off — no fuel delivery
    SEMANTIC_ERROR = "SEMANTIC_ERROR"  # Physics Gate violation — cannot proceed


class NodeMAFStatus(StrEnum):
    """MAF sensor data provenance emitted by OBDLab in ``OBDLiveDataPayload.maf_status``.

    Tells COMLab whether the MAF value is a real sensor reading or a computed
    emulation, weighting VE evidence accordingly. Mirrored from OBDLab
    (JSON-only boundary).

    Source: OBD_VOCABULARY.md §5; OBDLab_KG_Wiki.md §6.6.
    """

    REAL_SENSOR_FEED = "REAL_SENSOR_FEED"  # MAF sensor physically present and reading
    VIRTUAL_EMULATION = "VIRTUAL_EMULATION"  # MAP_ONLY route — MAF value is computed


class NodeMAPStatus(StrEnum):
    """MAP sensor data provenance emitted by OBDLab in ``OBDLiveDataPayload.map_status``.

    Tells COMLab whether the MAP value is a real sensor reading or back-calculated
    from MAF, weighting VE evidence accordingly. Mirrored from OBDLab
    (JSON-only boundary).

    Source: OBD_VOCABULARY.md §5; OBDLab_KG_Wiki.md §6.6.
    """

    REAL_SENSOR_FEED = "REAL_SENSOR_FEED"  # MAP sensor physically present and reading
    BACK_CALCULATED = "BACK_CALCULATED"  # MAF_ONLY route — MAP value is inferred


# ---------------------------------------------------------------------------
# Aliases — reconciled enum names
# ---------------------------------------------------------------------------

# OBDLab emits ``rpm_state_bucket`` typed as ``RpmStateBucket``.
# COMLab's ``EngineStateBucket`` has identical values (same 4 members) —
# alias rather than duplicate per T-FX-1 reconciliation rule.
RpmStateBucket = EngineStateBucket

class FuelSystemStatus(StrEnum):
    """Fuel system loop status at freeze-frame capture.

    Mirrored from DTCLab (JSON-only boundary — no cross-lab import). Consumed
    by ``FreezeFrameRecord.fuel_system_status`` in COMLab's ingestion schema
    for freeze-frame context classification.

    Source: DTC_VOCABULARY.md §8.
    """

    CL = "CL"  # closed loop — O2 feedback active
    OL = "OL"  # open loop — base map (cold start, WOT, decel)
    OL_DRIVE = "OL_DRIVE"  # open loop driving — WOT or decel fuel cut
    OL_FAULT = "OL_FAULT"  # open loop due to O2 sensor fault


class DTCRoutingTag(StrEnum):
    """DTC routing tags — groups related P-codes into actionable diagnostic buckets.

    Emitted by DTCLab in ``DTCLabPayload.routing_tags``. Consumed by COMLab's
    fault-atlas router to narrow the differential diagnosis. The v6 4-value form
    is retired; this 19-value enum is the canonical set (aligned with DTCLab).

    Source: DTC_VOCABULARY.md §11 (full canonical block, including BOOST/KNOCK
    additions from §16).
    """

    # Core (original §3)
    LEAN_HISTORY = "LEAN_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0171, P0174 — fuel system too lean
    RICH_HISTORY = "RICH_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0172, P0175 — fuel system too rich
    MISFIRE_HISTORY = "MISFIRE_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0300-P0312 — ignition/combustion failure
    CATALYST_HISTORY = "CATALYST_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0420, P0430 — catalyst efficiency below threshold
    EGR_HISTORY = "EGR_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0401, P0402 — EGR flow insufficient/excessive
    O2_HISTORY = "O2_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P013x, P014x, P015x, P016x, P2196, P2A0x — O2 sensor faults
    INJECTOR_HISTORY = "INJECTOR_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0201-P0212 — injector circuit faults

    # Added from domain material
    VVT_HISTORY = "VVT_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0010-P0016 — cam timing / VVT phaser faults
    EVAP_HISTORY = "EVAP_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0441-P0456, P0496 — EVAP system leaks/purge
    THERMAL_HISTORY = "THERMAL_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0116, P0128 — thermostat / cold-start faults
    ECU_INTERNAL_HISTORY = "ECU_INTERNAL_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0601-P0606, P0641-P0651 — PCM memory / 5V reference
    POA_HISTORY = "POA_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — no direct DTC — P250C, P0300 fallout — oil-burning markers
    IDLE_CONTROL_HISTORY = "IDLE_CONTROL_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0505-P0507 — idle air control faults

    # Added from §16 (harvested from OBDadd1.md / FFFT$06.md)
    BOOST_HISTORY = "BOOST_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0234, P0299 — turbocharger overboost/underboost (Euro 5+)
    KNOCK_HISTORY = "KNOCK_HISTORY"  # ISO 15031-6 §5.6 / SAE J2012 — P0325, P0327, P0328 — knock sensor circuit faults

    # Added from T-DOC-15 DTC_VOCABULARY canonical (DTCLab 19-value set)
    COOLANT_SYSTEM_MALFUNCTION = "COOLANT_SYSTEM_MALFUNCTION"  # ISO 15031-6 §5.6 / SAE J2012 — P0128/P0117 in OL_FAULT (cross-field) — wiki: DTC_VOCABULARY §4
    CYLINDER_FLUID_MISFIRE = "CYLINDER_FLUID_MISFIRE"  # ISO 15031-6 §5.6 / SAE J2012 — P030x in CL with coolant evidence (cross-field) — wiki: DTC_VOCABULARY §4


class DTCFallbackStrategy(StrEnum):
    """Fallback strategy for fault-registry rule matching when DTC evidence is
    absent or uncertain.

    Consumed by COMLab's fault-atlas router to decide whether a registry rule
    can fire based on chemistry evidence alone or requires corroborating DTCs.

    Source: DTC_VOCABULARY.md §8.
    """

    REQUIRE_MATCH = "REQUIRE_MATCH"  # rule fires only with matching DTC
    PROCEED_ON_MATCH_OR_EMPTY = "PROCEED_ON_MATCH_OR_EMPTY"  # rule fires if DTC matches OR no DTCs present
    PROCEED = "PROCEED"  # DTC ignored; chemistry alone decides


class DTCSeverityClass(StrEnum):
    """DTC severity class per ISO 15031-6 §6 (≡ SAE J2012).

    Governs MIL illumination behavior and is consumed by COMLab to weight
    diagnostic urgency. The four single-letter codes define catalyst-damaging
    vs. emission-relevant vs. informational faults.

    Source: DTC_VOCABULARY.md §4.
    """

    A = "A"  # catalyst-damaging fault — MIL flashes immediately
    B = "B"  # emission-relevant fault — MIL solid after 2 drive cycles
    C = "C"  # driveability / non-emission fault — MIL may light or warning only
    D = "D"  # no MIL required — informational only


class DTCState(StrEnum):
    """DTC lifecycle state per ISO 15031-5 (≡ SAE J1979) Service $03 / $07 / $0A.

    Consumed across all 4DLab modules. Only ``CONFIRMED`` triggers
    ``active_mil = true`` in DTCLab's output payload.

    Source: DTC_VOCABULARY.md §5.
    """

    PENDING = "PENDING"  # Mode $07 — detected once, awaiting confirmation across drive cycles
    CONFIRMED = "CONFIRMED"  # Mode $03 — confirmed across required drive cycles; MIL on
    PERMANENT = "PERMANENT"  # Mode $0A — cleared by tool but not yet by drive cycle; anti-tampering


class Mode06Status(StrEnum):
    """Mode $06 monitor result classification (4 values).

    Emitted by DTCLab in ``mode_06_monitors[].status``. Used by COMLab to
    surface early-warning component degradation before MIL illumination.

    Source: DTC_VOCABULARY.md §14.
    """

    PASSED = "PASSED"  # value < limit — healthy margin
    PENDING_FAIL_MARGINAL = "PENDING_FAIL_MARGINAL"  # value near limit — trending bad
    CRITICAL_FAIL = "CRITICAL_FAIL"  # value >> limit — imminent failure
    MONITOR_ABORTED = "MONITOR_ABORTED"  # wiki: DTC_VOCABULARY §10.3/§13 — Incomplete/all-zero monitor; CAN-era no-start only


# DTCLab emits ``Mode06MonitorState``. COMLab's ``Mode06Status`` has
# identical values (PASSED, PENDING_FAIL_MARGINAL, CRITICAL_FAIL,
# MONITOR_ABORTED) — alias rather than duplicate.
Mode06MonitorState = Mode06Status


class ConfidenceRating(StrEnum):
    """Processing confidence rating — how much trust to place in the final verdict.

    Emitted by COMLab in ``OrchestratorFinalUIOutput``. Reflects the quality and
    completeness of the evidence chain from the four upstream labs.

    Source: OBD_VOCABULARY.md §8.
    """

    HIGH_ASSURANCE = "HIGH_ASSURANCE"  # all four labs reported cleanly, horizon gating resolved
    DEGRADED_ASSURANCE = "DEGRADED_ASSURANCE"  # one or more labs degraded — partial evidence chain
    LOW_CERTAINTY = "LOW_CERTAINTY"  # essential data missing or contradictory — flag for manual review


class VinConfidence(StrEnum):
    """VIN decode confidence — how many fields VINLab resolved from the VIN.

    Emitted by VINLab in ``VinDNA.confidence``. Consumed by COMLab to weight
    VIN-derived gating decisions (horizon pruning, stress-idle target, GPF
    presence) in the fault-atlas router.

    Source: OBD_VOCABULARY.md §8.
    """

    HIGH = "HIGH"  # WMI, year, engine_code all resolved from VIN registry
    PARTIAL = "PARTIAL"  # year resolved but engine_code unknown — some gating degraded
    NONE = "NONE"  # WMI not found in registry — VIN-derived gates fall back to defaults


class DegradationMode(StrEnum):
    """COMLab fallback tier — which evidence sources are available and trusted.

    When one or more labs are degraded, COMLab descends the fallback tree
    defined in OrchestratorLabBP.md. Gas chemistry (Lambda) is the hardest
    evidence — it survives all but the deepest degradation.

    Source: OBD_VOCABULARY.md §9.
    """

    FULL_FUSION = "FULL_FUSION"  # all four labs reported cleanly — full evidence weight
    GAS_DOMINANT = "GAS_DOMINANT"  # OBD/DTC degraded, chemistry dominant — legacy / pre-OBD-II vehicle
    SINGLE_POINT = "SINGLE_POINT"  # wiki: delta-relations/01 — no second operating-point frame; the two-point delta_signature is unavailable so the static single-point signature is the fallback (T-COMV2-DELTA-1)
    FATAL_INCOMPLETE = "FATAL_INCOMPLETE"  # essential data missing — abort diagnostic session


class SeverityLevel(StrEnum):
    """UI-facing severity band — the stoplight the technician sees.

    Mapped from fault-family × chemistry confidence × DTC state in COMLab's
    final serialisation step. Drives the red/amber/green visual in the UI.

    Source: OBD_VOCABULARY.md §10.
    """

    CRITICAL_IMMEDIATE_STOP = "CRITICAL_IMMEDIATE_STOP"  # red — catalyst damage or imminently unsafe
    WARNING_DEGRADED_PERFORMANCE = "WARNING_DEGRADED_PERFORMANCE"  # amber — fault present, driveable
    OPTIMAL_HEALTH = "OPTIMAL_HEALTH"  # green — no fault detected, all systems nominal


@dataclass(frozen=True)
class LabRoutingDirective:
    """SymptomDNA routing output. All flags default False.

    Produced by symptom_router.route_symptom().
    Consumed by LabPipelineAggregator (suppress_gaslab, suppress_obd_live_pids)
    and fault_atlas_router (suppress_mode06_ui, cold_start_mode).

    Source: data_flow_report.md §5.3.
    """
    suppress_gaslab: bool = False
    """engine_state == will_not_start — GASLab absent is expected, not fatal."""

    suppress_obd_live_pids: bool = False
    """engine_state == will_not_start — accept OBD payload with only
    freeze_frame_pids; live PID fields may be absent."""

    suppress_mode06_ui: bool = False
    """engine_state == will_not_start — fault_atlas_router omits Mode $06
    section from the final output (no running engine = monitors not ready)."""

    cold_start_mode: bool = False
    """occurs_during == cold_only — fault_atlas_router activates cold-start
    hypothesis branch (stub: inject routing hint, log, return)."""

    reasons: tuple[LabRoutingDirectiveReason, ...] = ()
    """Why each flag was set. Consumer: response.LabRoutingDirectiveOut.reasons
    per PRD §5.6. Populated by symptom_router.route_symptom()."""


class FaultEnrichmentSeverity(StrEnum):
    """Editor-asserted severity hint for a KG node.

    NOT to be confused with ``PerformanceAnalytics.severity_level``. Surfaced
    only when ``severity_level == OPTIMAL_HEALTH`` so the editor can offer a
    "monitor closely" cue. Not used in FaultAtlas router scoring.

    Consumer: ``response.FaultEnrichment.editor_severity_hint``.

    Source: COMLab_LLD.md §3.1.
    """

    INFORMATIONAL = "INFORMATIONAL"  # lld: §3.1 FaultEnrichmentSeverity
    WATCH = "WATCH"                  # lld: §3.1 FaultEnrichmentSeverity
    REPAIR = "REPAIR"                # lld: §3.1 FaultEnrichmentSeverity
    URGENT = "URGENT"                # lld: §3.1 FaultEnrichmentSeverity


class LabRoutingDirectiveReason(StrEnum):
    """Why a routing-directive flag was set.

    Consumer: ``response.LabRoutingDirectiveOut.reasons`` — UI renders the
    "why was this section greyed out" copy per PRD §5.6.

    Source: COMLab_LLD.md §3.1.
    """

    NON_STARTER_NO_EXHAUST = "NON_STARTER_NO_EXHAUST"                # lld: §3.1 — engine_state == will_not_start
    NON_RUNNING_NO_LIVE_PIDS = "NON_RUNNING_NO_LIVE_PIDS"            # lld: §3.1 — engine_state in {will_not_start, cranking}
    NON_RUNNING_MONITORS_NOT_READY = "NON_RUNNING_MONITORS_NOT_READY"  # lld: §3.1 — engine_state == will_not_start
    COLD_START_HYPOTHESIS = "COLD_START_HYPOTHESIS"                  # lld: §3.1 — occurs_during == cold_only


class PrimaryLoadCalculation(StrEnum):
    """VIN-driven primary load calculation strategy.

    Emitted by VINLab in ``VinDNA.air_metering_architecture.primary_load_calculation``.
    Consumed by OBDLab's Volumetric Efficiency formula routing.

    Source: SEMANTIC_CONTRACT.md §8; lld: §3.2 AirMeteringArchitecture.
    """

    HYBRID_MAF_MAP = "HYBRID_MAF_MAP"  # lld: §3.2 — both MAF and MAP present
    MAP_ONLY = "MAP_ONLY"              # lld: §3.2 — speed-density, no MAF
    MAF_ONLY = "MAF_ONLY"              # lld: §3.2 — MAF-only, no MAP sensor
