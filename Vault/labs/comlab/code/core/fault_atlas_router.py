"""Fault Atlas Router — Stage B decision core.

Implements the 5-phase triage walk per COMLab_LLD.md §6.4.
Consumes SanitizedPayload from Stage A, resolves the winning fault_id,
enriches from the KG, runs analytics, and assembles the final UI output.

Source: COMLab_LLD.md §6.4.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypedDict

import yaml

from pydantic import BaseModel, Field

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.ecu_hardware_checker import ECUHardwareChecker
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.perception_contradiction import CompensatedRichResult
from comlab.schemas.ingestion import OrchestratorInboundRequest
from comlab.schemas.kg import KGNode
from comlab.schemas.response import (
    DiagnosticVerdict,
    DifferentialSiblingOut,
    ExecutionMeta,
    FaultEnrichment,
    LabRoutingDirectiveOut,
    OrchestratorFinalUIOutput,
    PerformanceAnalytics,
)
from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    DTCRoutingTag,
    FuelSystemStatus,
    Horizon,
    LabRoutingDirectiveReason,
    Mode06MonitorState,
    O2FailureMode,
    VEValidity,
)

from comlab.observability._tracer import get_tracer

if TYPE_CHECKING:
    from comlab.schemas.ingestion import UserInputEchoAudit

logger = logging.getLogger(__name__)

__all__ = [
    "ConfidenceScoring",
    "CrossDomainMatrix",
    "DTCLabStatusRule",
    "FaultAtlasRouter",
    "OBDConstraint",
    "RegistryFile",
    "RegistryRow",
    "TriageVerdict",
]

# Sentinel fault_id returned when no rule fires (lld: §6.4)
_UNKNOWN_FAULT_ID: str = "ERR-UNKNOWN-000"  # lld: §6.4 sentinel

# P030x pattern for catalyst-damage override (lld: §6.4 step 7)
_P030X_RE = re.compile(r"^P030[0-8]$")  # lld: §6.4 catalyst-damage DTC pattern

# Minimum confidence threshold for fault verdict routing (lld: §6.4)
# Values below this produce no_fault even when a rule matches — the evidence
# is too weak to act on without corroborating data.  Same boundary used for
# HIGH_ASSURANCE vs DEGRADED_ASSURANCE labeling at route() line ~810.
MIN_CONFIDENCE_THRESHOLD: float = 0.70  # lld: §6.4
_OPEN_LOOP_TRIM_CONFIDENCE_CAP = 0.60  # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS
# below MIN_CONFIDENCE_THRESHOLD so open-loop trim evidence cannot win.
_SCORE_CEILING = 1.0  # wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER
_EVIDENCE_PROMOTION_CONFIDENCE = 0.80  # wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER
_EVIDENCE_DEMOTION_CAP = 0.60  # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS
_INCOMPLETE_OXIDATION_SUPPORTED_CAP = 0.90  # wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER
_INCOMPLETE_OXIDATION_UNSUPPORTED_CAP = 0.75  # wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER

_BANK_ASYMMETRY_BOUND_PCT = 5.0
# wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS;
# 02_lab_input_contract.md §2 authority bands.
_NO_EVIDENCE_CONFIDENCE = 0.0
# wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS — unavailable
# and symmetric inputs abstain rather than contribute evidence.
_BANK_ASYMMETRY_CONFIDENCE = 0.80
# wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER provisional high-assurance band.
_BANK_ASYMMETRY_LEGACY_CONFIDENCE_CAP = 0.50
# wiki: 04_horizon_eras.md §CONCEPT_LEGACY (trims unreliable/absent);
# 09_calibration_confidence.md §CONCEPT_CONF_TIER degraded-assurance lower bound.
_ECU_FUSE_RAILED_TRIM_PCT = 25.0  # wiki: 02_lab_input_contract.md §2 line 70
_ECU_FUSE_CONFIDENCE = 0.80  # wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER
_O2_STOICH_LAMBDA_LO = 0.97  # wiki: 02_lab_input_contract.md §1 CONCEPT_GAS_INPUT
_O2_STOICH_LAMBDA_HI = 1.03  # wiki: 02_lab_input_contract.md §1 CONCEPT_GAS_INPUT
_O2_OFFSET_CONFIDENCE = 0.80  # wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER
_VE_EVIDENCE_CONFIDENCE = 0.80
# wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER provisional
# high-assurance band.
_VE_TARGETS: dict[VEValidity, tuple[str, str]] = {
    VEValidity.FAULT_VE_IDLE_COLLAPSE: ("ERR-LC-001", "lean_condition"),
    VEValidity.FAULT_MAF_CONTAMINATION: ("ERR-LC-002", "lean_condition"),
    VEValidity.FAULT_VE_SENSOR_SKEW: ("ERR-SF-008", "sensor_fault"),
}
# wiki: 06_fault_atlas_families.md §CONCEPT_FAM_LEAN / §CONCEPT_FAM_SENSOR;
# 02_lab_input_contract.md §2 line 55 and §4 CONCEPT_DNA_INPUT.
_BANK_LOCALIZED_FAMILIES = frozenset({
    "lean_condition",
    "rich_mixture",
    "sensor_fault",
})
# wiki: 06_fault_atlas_families.md §CONCEPT_FAMILIES — one-bank vacuum leak,
# injector, and O2 causes map to these three fault families.
_NOSTART_CONFIDENCE = 0.80
# wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER
_NOSTART_SECURITY_NODES = frozenset({"ERR-NS-005"})
_NOSTART_MECHANICAL_NODES = frozenset({"ERR-NS-001", "ERR-NS-002", "ERR-NS-003", "ERR-NS-004"})
# wiki: 06_fault_atlas_families.md §CONCEPT_FAM_NONSTART + config/kg/non_starter.json
_MISFIRE_FALSE_LEAN_TRIM_PCT = 15.0  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_SINGLE_CYLINDER_DOMINANCE_RATIO = 0.70  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_MAF_CALIBRATION_DRIFT_PCT = 5.0  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_MAF_COMPONENT_FAULT_PCT = 12.0  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_LTFT_CELL_LEAN_BOUND_PCT = 5.0  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_STANDARD_SEA_LEVEL_BARO_KPA = 101.325  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_DEFAULT_DEVIATION_TOLERANCE_RATIO = 0.10  # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS

# Symptom-prior config path (T-FX-DNA-3)
_PKG_ROOT = Path(__file__).parent.parent
_DEFAULT_PRIOR_PATH = _PKG_ROOT / "config" / "symptom_prior.yaml"
_DEFAULT_DISCRIMINATOR_PATH = _PKG_ROOT / "config" / "tag_discriminator.yaml"
_DEFAULT_TAXONOMY_PATH = _PKG_ROOT / "config" / "proposals" / "taxonomy_backbone.yaml"


# ---------------------------------------------------------------------------
# Registry row models (lld: §8.1)
# ---------------------------------------------------------------------------


def _expected_family_from_trace_context() -> str:
    """Read harness expected family from OTel baggage when tracing is active."""
    try:
        from opentelemetry import baggage
    except ImportError:
        return ""
    value = baggage.get_baggage("harness.expected_family")
    return str(value or "")


def _expected_rule_rank(
    scored_rules: list[dict[str, Any]], expected_family: str
) -> int:
    """Return 1-based rank for the first scored rule in *expected_family*."""
    if not expected_family:
        return -1
    for idx, rule in enumerate(scored_rules, start=1):
        if rule.get("fault_family") == expected_family:
            return idx
    return -1


def _set_expected_rule_attrs(
    span: Any,
    scored_rules: list[dict[str, Any]],
) -> None:
    """Set Phase D expected-rule attrs when the harness supplied an oracle."""
    expected_family = _expected_family_from_trace_context()
    if not expected_family:
        return
    rank = _expected_rule_rank(scored_rules, expected_family)
    span.set_attribute("router.expected_rule_present", rank > 0)
    span.set_attribute("router.expected_rule_rank", rank)


class OBDConstraint(BaseModel):
    """A single PID constraint within a registry rule's obd_live_pids block."""
    operator: str
    value: Any  # scalar or [low, high] for IN_RANGE


class DTCLabStatusRule(BaseModel):
    """DTC matching rule within a registry entry's cross_domain_matrix."""
    active_mil: bool = False
    p_code_match: list[str] = Field(default_factory=list)
    fallback_strategy: str = "PROCEED_ON_MATCH_OR_EMPTY"  # lld: §8.1


class CrossDomainMatrix(BaseModel):
    """Cross-domain evidence matrix for one registry rule."""
    gas_lab_state: str
    obd_live_pids: dict[str, OBDConstraint] = Field(default_factory=dict)
    dtc_lab_status: DTCLabStatusRule = Field(default_factory=DTCLabStatusRule)


class ConfidenceScoring(BaseModel):
    """Confidence scoring parameters for one registry rule."""
    base_weight: float = Field(ge=0.0, le=1.0)  # lld: §8.1
    bonus_on_dtc_match: float = Field(ge=0.0, le=1.0)  # lld: §8.1


class RegistryRow(BaseModel):
    """One rule in the global fault registry. Validated at boot."""
    fault_id: str
    fault_name: str = ""  # lld: §8.1 — optional in some entries
    target_horizons: list[str]
    preconditions: dict[str, Any] = Field(default_factory=dict)
    ui_diagnostic_string: str = ""
    cross_domain_matrix: CrossDomainMatrix
    confidence_scoring: ConfidenceScoring
    fallback_strategy: str | None = None  # top-level fallback override
    routing_tag: str | None = None  # lld: §8.1 — DTCRoutingTag value for tag-based matching
    perception_flag: str | None = None  # lld: §8.1 — ChemicalSignature bias verdict for perception-based matching


class RegistryFile(BaseModel):
    """Top-level shape of global_fault_registry.json."""
    registry: list[RegistryRow]


class TriageVerdict(TypedDict):
    """Internal result from execute_triage_loop → route()."""
    winner: RegistryRow | None  # None → OPTIMAL_HEALTH sentinel
    winner_score: float
    runner_ups: list[tuple[RegistryRow, float]]  # at most 3 (HLD §4.2 step 8)


@dataclass(frozen=True)
class _BankAsymmetryVerdict:
    """Private bank-asymmetry evidence result for Phase-5 fusion."""

    # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS.
    state: Literal["UNAVAILABLE", "SYMMETRIC", "ASYMMETRIC"]
    confidence: float


def _bank_asymmetry_verdict(
    per_bank_trim_delta: float | None,
    resolved_horizon: str,
) -> _BankAsymmetryVerdict:
    """Classify per-bank trim divergence and attach era-bounded confidence."""
    if per_bank_trim_delta is None:
        return _BankAsymmetryVerdict("UNAVAILABLE", _NO_EVIDENCE_CONFIDENCE)
    if abs(per_bank_trim_delta) <= _BANK_ASYMMETRY_BOUND_PCT:
        return _BankAsymmetryVerdict("SYMMETRIC", _NO_EVIDENCE_CONFIDENCE)
    confidence = (
        _BANK_ASYMMETRY_LEGACY_CONFIDENCE_CAP
        if resolved_horizon == Horizon.LEGACY
        else _BANK_ASYMMETRY_CONFIDENCE
    )
    return _BankAsymmetryVerdict("ASYMMETRIC", confidence)


def _ve_evidence_gate(
    ve_pct: float | None,
    ve_validity: VEValidity,
    air_metering_strategy: AirMeteringStrategy | None,
) -> Literal["UNAVAILABLE", "VE_EVIDENCE", "CIRCULAR_RATIONALITY"]:
    """Classify whether an OBD VE fault is independent fusion evidence.

    VE is independent only when MAF and MAP provide a dual-sensor cross-check.
    A fault produced from one air sensor is circular evidence and must route to
    rationality checking rather than promote a VE/mixture verdict.

    # wiki: 02_lab_input_contract.md §2 line 55 and §4 CONCEPT_DNA_INPUT;
    # 06_fault_atlas_families.md §CONCEPT_FAM_LEAN / §CONCEPT_FAM_SENSOR;
    # 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS.
    """
    if (
        ve_pct is None
        or ve_validity in (VEValidity.VALID, VEValidity.UNKNOWN)
        or air_metering_strategy is None
    ):
        return "UNAVAILABLE"
    if air_metering_strategy == AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK:
        return "VE_EVIDENCE"
    return "CIRCULAR_RATIONALITY"


def _fuel_system_gate(
    fuel_system_status: FuelSystemStatus | None,
) -> Literal["CLOSED_LOOP", "OPEN_LOOP_GATED", "UNAVAILABLE"]:
    """Classify whether live fuel trim has closed-loop feedback authority.

    # wiki: 02_lab_input_contract.md §2 CONCEPT_OBD_INPUT line 58;
    # 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS;
    # 13_proposals_register.md T-COMV2-FUELSYS-GATE-1 / EP-OBD-IN-03.
    """
    if fuel_system_status is None:
        return "UNAVAILABLE"
    if fuel_system_status == FuelSystemStatus.CL:
        return "CLOSED_LOOP"
    return "OPEN_LOOP_GATED"


@dataclass(frozen=True)
class _EcuFaultVerdict:
    """Private ECU perception-vs-reality evidence result for Phase-5 fusion."""

    # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS.
    state: Literal["UNAVAILABLE", "NO_FAULT", "ECU_FAULT"]
    confidence: float


def _ecu_fault_verdict(
    normalized_obd_lambda: float | None,
    lambda_chem: float | None,
    era_lambda_tolerance: float | None,
    total_trim_correction_delta: float | None,
    total_trim_correction_delta_b2: float | None,
) -> _EcuFaultVerdict:
    """Classify symmetric trim saturation plus gas↔OBD perception divergence.

    The fuse abstains unless both bank trims, both lambda values, and the active
    era tolerance are available. It contributes conflict-aware evidence only;
    it does not override the existing rank.

    # wiki: 06_fault_atlas_families.md §RULE_COLLISION_SET line 92 and
    # §CONCEPT_FAM_ECU; 02_lab_input_contract.md §2 lines 52-54 and 70;
    # 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS.
    """
    if (
        normalized_obd_lambda is None
        or lambda_chem is None
        or era_lambda_tolerance is None
        or total_trim_correction_delta is None
        or total_trim_correction_delta_b2 is None
    ):
        return _EcuFaultVerdict("UNAVAILABLE", _NO_EVIDENCE_CONFIDENCE)
    if abs(total_trim_correction_delta) < _ECU_FUSE_RAILED_TRIM_PCT:
        return _EcuFaultVerdict("NO_FAULT", _NO_EVIDENCE_CONFIDENCE)
    if (
        abs(total_trim_correction_delta - total_trim_correction_delta_b2)
        > _BANK_ASYMMETRY_BOUND_PCT
    ):
        return _EcuFaultVerdict("NO_FAULT", _NO_EVIDENCE_CONFIDENCE)
    if abs(normalized_obd_lambda - lambda_chem) <= era_lambda_tolerance:
        return _EcuFaultVerdict("NO_FAULT", _NO_EVIDENCE_CONFIDENCE)
    return _EcuFaultVerdict("ECU_FAULT", _ECU_FUSE_CONFIDENCE)


def _resolve_o2_sensor_fault(
    o2_failure_mode: O2FailureMode | None,
    lambda_chem: float | None,
) -> Literal["UNAVAILABLE", "NO_FAULT", "WIDEBAND_OFFSET"]:
    """Confirm a wideband-offset candidate against independent gas-truth lambda.

    The helper abstains when either channel is unavailable. A candidate is
    confirmed only when gas chemistry remains stoichiometric; real lean/rich gas
    leaves mixture-fault routing untouched.

    # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS line 97;
    # 06_fault_atlas_families.md §CONCEPT_FAM_SENSOR line 37;
    # 02_lab_input_contract.md §1 CONCEPT_GAS_INPUT; proposal EP-OBD-17.
    """
    if o2_failure_mode is None or lambda_chem is None:
        return "UNAVAILABLE"
    if o2_failure_mode != O2FailureMode.WIDEBAND_OFFSET_CANDIDATE:
        return "NO_FAULT"
    if not _O2_STOICH_LAMBDA_LO <= lambda_chem <= _O2_STOICH_LAMBDA_HI:
        return "NO_FAULT"
    return "WIDEBAND_OFFSET"


def _misfire_locality(
    per_cylinder_misfire_counts: dict[int, int] | None,
    total_trim_correction_delta: float | None,
) -> Literal["UNAVAILABLE", "SINGLE_CYLINDER", "GLOBAL"]:
    """Classify misfire count distribution.

    # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "Misfire localisation" (>+15 % trim + 1 cyl → SINGLE_CYLINDER; spread → GLOBAL) + 13_proposals_register.md §line48 (EP-OBD-IN-07)
    """
    if not per_cylinder_misfire_counts:
        return "UNAVAILABLE"

    # corroborating context: total trim > +15% (false-lean gate)
    if (
        total_trim_correction_delta is None
        or total_trim_correction_delta <= _MISFIRE_FALSE_LEAN_TRIM_PCT
    ):
        return "UNAVAILABLE"

    valid_counts = {
        cyl: count
        for cyl, count in per_cylinder_misfire_counts.items()
        if count > 0  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
    }
    if not valid_counts:
        return "UNAVAILABLE"

    total_count = sum(valid_counts.values())
    if total_count == 0:
        return "UNAVAILABLE"

    # one cylinder dominates (its count ≫ the rest) -> SINGLE_CYLINDER
    # spread across cylinders -> GLOBAL
    max_count = max(valid_counts.values())
    if max_count / total_count >= _SINGLE_CYLINDER_DOMINANCE_RATIO:
        return "SINGLE_CYLINDER"
    return "GLOBAL"


def _maf_linearity_band(
    sensor_error_delta: float | None,
) -> Literal["WITHIN_SPEC", "CALIBRATION_DRIFT", "COMPONENT_FAULT"]:
    """Determine the MAF linearity band from the sensor error delta.

    # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "MAF linearity ladder" (<3–4 healthy / 5–12 drift→ERR-LC-002 / >12–15 component→P0101; P0102=open-circuit) + 08_scoring_to_fusion_rework.md §line103
    """
    if sensor_error_delta is None:
        return "WITHIN_SPEC"
    err = abs(sensor_error_delta)
    if err < _MAF_CALIBRATION_DRIFT_PCT:
        return "WITHIN_SPEC"
    if err <= _MAF_COMPONENT_FAULT_PCT:
        return "CALIBRATION_DRIFT"
    return "COMPONENT_FAULT"


def _ltft_cell_pattern(
    ltft_cell_vector: dict[int, float] | None,
) -> Literal["UNAVAILABLE", "GLOBAL", "LOCALISED", "WITHIN_SPEC"]:
    """Classify the LTFT load-cell distribution.

    # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "LTFT load-cell distribution" (GLOBAL vs LOCALISED; idle/part-throttle deferred — needs OEM cell map) + 08_scoring_to_fusion_rework.md §line104
    """
    if ltft_cell_vector is None or not ltft_cell_vector:
        return "UNAVAILABLE"

    total_count = len(ltft_cell_vector)
    lean_count = sum(val > _LTFT_CELL_LEAN_BOUND_PCT for val in ltft_cell_vector.values())

    if lean_count == total_count:
        return "GLOBAL"
    if lean_count:
        return "LOCALISED"
    return "WITHIN_SPEC"


@dataclass(frozen=True)
class _NoStartVerdict:
    """Private no-start branch evidence result for Phase-5 fusion.

    # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS.
    """

    state: Literal["UNAVAILABLE", "MECHANICAL", "SECURITY_LOCKOUT"]
    confidence: float


def _no_start_branch(
    mode_06_monitors: dict[str, Any] | None,
    ff_fuel_spark_cut_at_crank: bool | None,
) -> _NoStartVerdict:
    """Classify no-start as security-lockout vs mechanical.

    The helper abstains when no Mode $06 monitors are available, when no
    monitor reports ``MONITOR_ABORTED``, or when the freeze-frame cut-state
    flag is missing. It contributes conflict-aware evidence only; it does
    not override the existing rank.

    # wiki: 08_scoring_to_fusion_rework.md line 98 (Mode-06 monitor-aborted
    # + FF cut-state -> security vs mechanical) + 06_fault_atlas_families.md
    # §CONCEPT_FAM_NONSTART lines 71-73 + DTC_VOCABULARY §10.3/§13
    # (MONITOR_ABORTED CAN-era-gated) + §12.3 (ff_fuel_spark_cut_at_crank)
    # + proposal EP-DTC-NOSTART-1.
    """
    if not mode_06_monitors or ff_fuel_spark_cut_at_crank is None:
        return _NoStartVerdict("UNAVAILABLE", _NO_EVIDENCE_CONFIDENCE)
    has_aborted = any(
        m.state == Mode06MonitorState.MONITOR_ABORTED
        for m in mode_06_monitors.values()
    )
    if not has_aborted:
        return _NoStartVerdict("UNAVAILABLE", _NO_EVIDENCE_CONFIDENCE)
    if ff_fuel_spark_cut_at_crank:
        return _NoStartVerdict("SECURITY_LOCKOUT", _NOSTART_CONFIDENCE)
    return _NoStartVerdict("MECHANICAL", _NOSTART_CONFIDENCE)



# ---------------------------------------------------------------------------
# PID resolver — maps registry PID names to runtime values on the request
# ---------------------------------------------------------------------------

# Each registry PID key resolves to a field on the freeze_frame or OBD data.
# wiki: DTC_VOCABULARY §12 — freeze-frame PID inventory
_PID_SOURCES: dict[str, tuple[tuple[str, str], ...]] = {
    "shrtft1":               (
        ("obd_live_data", "shrtft1"),
        ("dtc_lab_output", "freeze_frame.short_term_ft1"),
    ),
    "longft1":               (
        ("obd_live_data", "longft1"),
        ("dtc_lab_output", "freeze_frame.long_term_ft1"),
    ),
    "shrtft2":               (("dtc_lab_output", "freeze_frame.short_term_ft2"),),
    "longft2":               (("dtc_lab_output", "freeze_frame.long_term_ft2"),),
    "map_kpa":               (("dtc_lab_output", "freeze_frame.manifold_pressure_kpa"),),
    "calc_load_pct":         (("dtc_lab_output", "freeze_frame.calculated_load_pct"),),
    "ect_c":                 (
        ("obd_live_data", "coolant_temp_c"),
        ("dtc_lab_output", "freeze_frame.coolant_temp_c"),
    ),
    "o2_voltage":            (("obd_live_data", "freeze_frame_pids.o2_voltage"),),
    "o2_downstream":         (("obd_live_data", "freeze_frame_pids.o2_downstream"),),
    "o2_b1s1_v":             (("obd_live_data", "freeze_frame_pids.o2_voltage"),),
    "o2_b1s2_v":             (
        ("obd_live_data", "freeze_frame_pids.o2_downstream"),
        ("dtc_lab_output", "freeze_frame.o2_voltage_b1s1"),
    ),
    "ignition_advance_deg":  (("dtc_lab_output", "freeze_frame.ignition_advance_deg"),),
    "maf_gps":               (
        ("obd_live_data", "mass_airflow_gps"),
        ("dtc_lab_output", "freeze_frame.maf_gps"),
    ),
    "throttle_pos_pct":      (("dtc_lab_output", "freeze_frame.throttle_pos_pct"),),
    "engine_rpm":            (("dtc_lab_output", "freeze_frame.engine_rpm"),),
    "vehicle_speed_kmh":     (("dtc_lab_output", "freeze_frame.vehicle_speed_kmh"),),
    "intake_air_temp_c":     (("dtc_lab_output", "freeze_frame.intake_air_temp_c"),),
}


def _resolve_dotted(obj: Any, dotted_path: str) -> float | None:
    for attr in dotted_path.split("."):
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    return float(obj)


def _resolve_pid(request: OrchestratorInboundRequest, pid_name: str) -> float | None:
    """Resolve a registry PID name to a runtime float value.

    Returns None when the PID is not available (missing sensor or legacy vehicle).
    """
    # Computed PID: manifold vacuum (wiki: manifold_vacuum_kpa)
    if pid_name == "manifold_vacuum_kpa":
        if request.dtc_lab_output is None:
            return None
        ff = request.dtc_lab_output.freeze_frame
        baro = ff.barometric_pressure_kpa
        if baro is None:
            baro = _STANDARD_SEA_LEVEL_BARO_KPA
        return baro - ff.manifold_pressure_kpa

    if pid_name in _PID_SOURCES:
        for source, dotted_path in _PID_SOURCES[pid_name]:
            obj = getattr(request, source, None)
            if obj is None:
                continue
            resolved = _resolve_dotted(obj, dotted_path)
            if resolved is not None:
                return resolved
        return None

    logger.warning("Unknown registry PID %r — no resolver mapping", pid_name)
    return None


# ---------------------------------------------------------------------------
# FaultAtlasRouter
# ---------------------------------------------------------------------------


class FaultAtlasRouter:
    """Stage B decision core. 5-phase triage walk per LLD §6.4.

    Constructor accepts *(registry_path, kg, analytics)* per §6.4.
    """

    def __init__(
        self,
        registry_path: str | Path,
        kg: FaultAtlasKG,  # lld: §6.4 — injected KG resolver
        analytics: PowerLossAnalytics,  # lld: §6.4 — injected Stage D
        use_v2_registry: bool = True,  # consumer: router v1/v2 path gate (:742)
        enable_delta: bool = False,  # consumer: Phase 5 delta rank input (T-COMV2-DELTA-1D)
        enable_delta_v2: bool = False,  # consumer: v2 scored_rules re-rank (T-COMV2-DELTA-2)
        enable_bank_fuse: bool = False,  # consumer: Phase 5 bank-asymmetry evidence
        enable_misfire_loc: bool = False,  # consumer: Phase 5 misfire localiser evidence
        enable_maf_lin: bool = False,  # consumer: Phase 5 MAF linearity ladder evidence
        enable_ltft_cell: bool = False,  # consumer: Phase 5 load-cell LTFT classification
        enable_ctxmod: bool = False,  # consumer: Phase 5 load_state context modifier (T-COMV2-CTXMOD-1)
        enable_ecu_fuse: bool = False,  # consumer: Phase 5 ecu_fault evidence
        enable_ve_gate: bool = False,  # consumer: Phase 5 VE circularity evidence
        enable_fuelsys_gate: bool = False,  # consumer: Phase 5 fuel-loop trim gate
        enable_ecu_hw: bool = False,  # consumer: Phase 5 ECU hardware-lie evidence
        enable_o2_offset: bool = False,  # consumer: Phase 5 wideband-offset evidence
        enable_nostart: bool = False,  # consumer: Phase 5 no-start branch (T-COMV2-NOSTART-1)
    ) -> None:
        self.registry_path = Path(registry_path)
        self._kg = kg  # lld: §6.4
        self._analytics = analytics  # lld: §6.4
        self.registry: list[RegistryRow] = []
        self._remediation_map: dict[str, str] = {}
        self._prior_table: dict[str, dict[str, Any]] = {}
        self._prior_weight: float = 0.0
        self._max_symptom_prior_weight: float = 0.65
        self._discriminator_table: dict[str, dict[str, Any]] = {}
        self._discriminator_weight: float = 0.0
        self._load_registry()
        self._load_prior_table()
        self._load_discriminator_table()
        self._load_taxonomy_backbone()
        self._use_v2_registry: bool = use_v2_registry
        self._enable_delta: bool = enable_delta
        self._enable_delta_v2: bool = enable_delta_v2
        self._enable_bank_fuse: bool = enable_bank_fuse
        self._enable_misfire_loc: bool = enable_misfire_loc
        self._enable_maf_lin: bool = enable_maf_lin
        self._enable_ltft_cell: bool = enable_ltft_cell
        self._enable_ctxmod: bool = enable_ctxmod
        self._enable_ecu_fuse: bool = enable_ecu_fuse
        self._enable_ve_gate: bool = enable_ve_gate
        self._enable_fuelsys_gate: bool = enable_fuelsys_gate
        self._enable_ecu_hw: bool = enable_ecu_hw
        self._enable_o2_offset: bool = enable_o2_offset
        self._enable_nostart: bool = enable_nostart
        self._ecu_hw_checker = ECUHardwareChecker()

    # ------------------------------------------------------------------
    # §4.2 step 1 — registry loader
    # ------------------------------------------------------------------

    def _load_registry(self) -> None:
        """Load + validate ``global_fault_registry.json`` at boot.

        Raises ValueError on schema violation or empty registry.
        """
        raw = json.loads(self.registry_path.read_text(encoding="utf-8"))
        try:
            parsed = RegistryFile.model_validate(raw)
        except Exception as exc:
            raise ValueError(
                f"Registry validation failed for {self.registry_path}: {exc}"
            ) from exc

        if not parsed.registry:
            raise ValueError(f"Registry file {self.registry_path} has zero rules")

        self.registry = parsed.registry

        # Load remediation_map for generate_remediation fallback (lld: §6.4)
        remediation_raw = raw.get("remediation_map", {})
        if isinstance(remediation_raw, dict):
            self._remediation_map = remediation_raw

        logger.info(
            "FaultAtlasRouter loaded %d registry rules from %s",
            len(self.registry),
            self.registry_path,
        )

    def _load_prior_table(self) -> None:
        """Load symptom-prior config from YAML (T-FX-DNA-3).

        Graceful degrade: missing or malformed config → empty table (no prior).
        """
        try:
            raw = yaml.safe_load(
                _DEFAULT_PRIOR_PATH.read_text(encoding="utf-8")
            )
        except FileNotFoundError:
            logger.warning(
                "Symptom-prior config not found at %s — prior disabled",
                _DEFAULT_PRIOR_PATH,
            )
            return
        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Symptom-prior config unparseable at %s: %s — prior disabled",
                _DEFAULT_PRIOR_PATH,
                exc,
            )
            return
        if raw is None:
            return
        self._prior_weight = float(raw.get("prior_weight", 0.0))
        self._max_symptom_prior_weight = float(raw.get("max_symptom_prior_weight", 0.65))
        self._prior_table = raw.get("mappings", {})
        logger.warning(
            "FaultAtlasRouter loaded %d symptom-prior mappings (weight=%.2f, max_weight=%.2f) from %s",
            len(self._prior_table),
            self._prior_weight,
            self._max_symptom_prior_weight,
            _DEFAULT_PRIOR_PATH,
        )

    def _load_discriminator_table(self) -> None:
        """Load routing-tag discriminator config from YAML (T-FX-REG-3).

        Graceful degrade: missing or malformed config → empty table (no lift).
        """
        try:
            raw = yaml.safe_load(
                _DEFAULT_DISCRIMINATOR_PATH.read_text(encoding="utf-8")
            )
        except FileNotFoundError:
            logger.warning(
                "Tag-discriminator config not found at %s — discriminator disabled",
                _DEFAULT_DISCRIMINATOR_PATH,
            )
            return
        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Tag-discriminator config unparseable at %s: %s — discriminator disabled",
                _DEFAULT_DISCRIMINATOR_PATH,
                exc,
            )
            return
        if raw is None:
            return
        self._discriminator_weight = float(raw.get("discriminator_weight", 0.0))
        self._discriminator_table = raw.get("mappings", {})
        logger.warning(
            "FaultAtlasRouter loaded %d tag-discriminator mappings (weight=%.2f) from %s",
            len(self._discriminator_table),
            self._discriminator_weight,
            _DEFAULT_DISCRIMINATOR_PATH,
        )

    def _load_taxonomy_backbone(self) -> None:
        """Load the proposals registry taxonomy backbone from YAML (T-SEM-2).

        Graceful degrade: missing or malformed config → empty dictionary/list.
        """
        try:
            raw = yaml.safe_load(
                _DEFAULT_TAXONOMY_PATH.read_text(encoding="utf-8")
            )
        except FileNotFoundError:
            logger.warning(
                "Taxonomy backbone config not found at %s — taxonomy loader disabled",
                _DEFAULT_TAXONOMY_PATH,
            )
            self._taxonomy_backbone = []
            return
        except (yaml.YAMLError, OSError) as exc:
            logger.warning(
                "Taxonomy backbone config unparseable at %s: %s — taxonomy loader disabled",
                _DEFAULT_TAXONOMY_PATH,
                exc,
            )
            self._taxonomy_backbone = []
            return
        if raw is None:
            self._taxonomy_backbone = []
            return
        self._taxonomy_backbone = raw.get("families", [])
        logger.warning(
            "FaultAtlasRouter loaded %d taxonomy backbone families from %s",
            len(self._taxonomy_backbone),
            _DEFAULT_TAXONOMY_PATH,
        )

    # ------------------------------------------------------------------
    # §4.2 step 6 — relational operator evaluator
    # ------------------------------------------------------------------

    @staticmethod
    def evaluate_operator(
        operator: str,
        runtime_value: Any,
        rule_value: Any,
    ) -> bool:
        """Evaluate a single relational operator against a runtime value.

        Operators: EQUALS, IN_RANGE, GREATER_THAN, LESS_THAN,
        LESS_THAN_OR_EQUAL, GREATER_THAN_OR_EQUAL, DEVIATES_FROM_TARGET.

        Returns False when *runtime_value* is None (missing PID).
        """
        if runtime_value is None:
            return False  # lld: §6.4 — missing PID → cannot satisfy constraint

        op = operator.upper()

        if op == "EQUALS":
            return runtime_value == rule_value

        # Guard: runtime_value must be a scalar for numeric comparisons
        if isinstance(runtime_value, (list, tuple, dict)):
            return False  # lld: §6.4 — PID values must be scalars

        if op == "IN_RANGE":
            if not isinstance(rule_value, (list, tuple)) or len(rule_value) != 2:
                return False
            lo, hi = float(rule_value[0]), float(rule_value[1])
            return lo <= float(runtime_value) <= hi

        if op == "GREATER_THAN":
            return float(runtime_value) > float(rule_value)

        if op == "LESS_THAN":
            return float(runtime_value) < float(rule_value)

        if op == "LESS_THAN_OR_EQUAL":
            return float(runtime_value) <= float(rule_value)

        if op == "GREATER_THAN_OR_EQUAL":
            return float(runtime_value) >= float(rule_value)

        if op == "DEVIATES_FROM_TARGET":
            if isinstance(rule_value, (list, tuple)) and len(rule_value) == 2:
                target = float(rule_value[0])
                tolerance = float(rule_value[1])
            elif isinstance(rule_value, (int, float)):
                target = float(rule_value)
                tolerance = target * _DEFAULT_DEVIATION_TOLERANCE_RATIO
            else:
                return False
            return abs(float(runtime_value) - target) > tolerance

        logger.warning("Unknown operator %r — treating as no-match", operator)
        return False

    # ------------------------------------------------------------------
    # §4.2 steps 2 + 3 + 4 — candidate pruning
    # ------------------------------------------------------------------

    def _prune_candidates(
        self,
        rows: list[RegistryRow],
        horizon: str,
        chemical_state: str,
        routing_tags: list[str],
        compensated_rich: CompensatedRichResult | None = None,
        bias_verdict: str | None = None,
        pruned_rules: list[dict[str, str]] | None = None,
    ) -> list[RegistryRow]:
        """Filter registry rows by horizon mask, chemistry, routing tags, and perception flag.

        Phase 1: Horizon — drop rows not targeting this era  (lld: §6.4)
        Phase 2: Chemistry — chemical_state must match gas_lab_state. Rules that
                 carry a routing_tag or perception_flag are gated exclusively by
                 those triggers and skip chemistry matching (wiki: T-P6-11 §Signal/noise gate).
        Additional: preconditions check
        """
        survivors: list[RegistryRow] = []

        for row in rows:
            # Phase 1 — horizon mask (lld: §6.4)
            if horizon not in row.target_horizons:
                if pruned_rules is not None:
                    pruned_rules.append({
                        "rule_id": row.fault_id,
                        "prune_reason": "horizon",
                        "failed_gating_key": "target_horizons",
                    })
                continue

            # Phase 2 — chemistry / tag / perception matching (lld: §6.4)
            if row.routing_tag is not None or row.perception_flag is not None:
                # Specialised rule — gated exclusively by its trigger field,
                # not by GASLab chemical_state (wiki: T-P6-11 §Signal/noise gate)
                tag_hit = (
                    row.routing_tag is not None
                    and row.routing_tag in routing_tags
                )
                perception_hit = (
                    row.perception_flag is not None
                    and bias_verdict is not None
                    and row.perception_flag == bias_verdict
                )
                if not (tag_hit or perception_hit):
                    if pruned_rules is not None:
                        failed_gating_key = (
                            "routing_tag"
                            if row.routing_tag is not None
                            else "perception_flag"
                        )
                        pruned_rules.append({
                            "rule_id": row.fault_id,
                            "prune_reason": "missing_evidence",
                            "failed_gating_key": failed_gating_key,
                        })
                    continue
            else:
                # Standard chemistry-based rule (lld: §6.4)
                if row.cross_domain_matrix.gas_lab_state != chemical_state:
                    # Compensated-rich bypass — when the trim+DTC detector fires,
                    # RICH_MIXTURE rules survive chemistry pruning even though
                    # GASLab sees stoich/lean chemistry.  wiki: T-P6-6a
                    if not (
                        compensated_rich is not None
                        and compensated_rich.is_compensated_rich
                        and row.cross_domain_matrix.gas_lab_state == "RICH_MIXTURE"
                    ):
                        if pruned_rules is not None:
                            pruned_rules.append({
                                "rule_id": row.fault_id,
                                "prune_reason": "chemistry",
                                "failed_gating_key": "gas_lab_state",
                            })
                        continue

            # Precondition check (lld: §8.1)
            pre = row.preconditions
            if pre:
                if "vvt_equipped" in pre:
                    # VVT precondition — checked against VIN DNA
                    # For now, always pass (injector from caller via routing tags)
                    pass

            survivors.append(row)

        return survivors

    # ------------------------------------------------------------------
    # §4.2 step 5 + scoring — triage walk
    # ------------------------------------------------------------------

    def execute_triage_loop(
        self, sanitized: dict[str, Any]
    ) -> TriageVerdict:
        """5-phase triage walk: prune → OBD eval → DTC verify → score → rank.

        Returns TriageVerdict with winner + ≤3 runner-ups.
        """
        tracer = get_tracer("comlab.fault_atlas_router")

        request: OrchestratorInboundRequest = sanitized["request"]
        directive = sanitized.get("routing_directive")

        # Log routing-directive flags (lld: §6.4)
        if directive is not None:
            if getattr(directive, "suppress_mode06_ui", False):
                logger.info(
                    "fault_atlas_router: suppress_mode06_ui=True — "
                    "Mode $06 section skipped (engine monitors not ready)"
                )
            if getattr(directive, "cold_start_mode", False):
                logger.info(
                    "fault_atlas_router: cold_start_mode=True — "
                    "cold-start hypothesis active"
                )

        # Resolve horizon from metadata or VIN DNA
        horizon = sanitized.get("horizon_ctx")
        if horizon is None:
            horizon_str = request.metadata.resolved_horizon
        else:
            horizon_str = str(horizon)

        chemical_state = request.gas_lab_output.chemical_state

        # Synthetic routing tags — POA_HISTORY injection (lld: §6.4)
        dtc_output = request.dtc_lab_output
        routing_tags: list[str] = (
            list(dtc_output.routing_tags) if dtc_output is not None else []
        )
        if chemical_state == "POA_SIGNATURE":
            poa = DTCRoutingTag.POA_HISTORY
            if poa not in routing_tags:
                routing_tags.append(poa)  # lld: §6.4 — POA injection

        if chemical_state == "EGR_DILUTION_MISFIRE":
            egr = DTCRoutingTag.EGR_HISTORY
            if egr not in routing_tags:
                routing_tags.append(egr)  # lld: §6.4 — EGR dilution→EGR_HISTORY injection

        # Perception-contradiction bias verdict (wiki: T-P6-11 §Signal/noise gate)
        perception_result = sanitized.get("perception_result")
        bias_verdict: str | None = None
        if perception_result is not None:
            bv = getattr(perception_result, "bias_verdict", None)
            if bv is not None:
                bias_verdict = bv.value if hasattr(bv, "value") else str(bv)

        with tracer.start_as_current_span("fault_atlas_router.execute_triage_loop"):
            # Phase 1+2 — prune by horizon + chemistry / routing_tag / perception_flag
            with tracer.start_as_current_span("phase.prune") as prune_span:
                prune_span.set_attribute("router.candidates_in", len(self.registry))
                compensated_rich = sanitized.get("compensated_rich_result")
                pruned_rules: list[dict[str, str]] | None = (
                    [] if prune_span.is_recording() else None
                )
                candidates = self._prune_candidates(
                    self.registry, horizon_str, chemical_state, routing_tags,
                    compensated_rich=compensated_rich,
                    bias_verdict=bias_verdict,
                    pruned_rules=pruned_rules,
                )
                if pruned_rules is not None:
                    for event in pruned_rules:
                        prune_span.add_event("rule_pruned", event)
                prune_span.set_attribute("router.candidates_out", len(candidates))

            # Phase 3 — OBD operator checks
            dtc_output: Any = request.dtc_lab_output
            confirmed_dtcs: set[str] = set(dtc_output.confirmed_dtcs)
            active_mil: bool = dtc_output.active_mil

            with tracer.start_as_current_span("phase.obd_eval") as obd_span:
                obd_span.set_attribute("router.candidates_in", len(candidates))
                obd_survivors: list[RegistryRow] = []
                for row in candidates:
                    pids_ok = True
                    for pid_name, constraint in row.cross_domain_matrix.obd_live_pids.items():
                        runtime_val = _resolve_pid(request, pid_name)
                        if not self.evaluate_operator(
                            constraint.operator, runtime_val, constraint.value
                        ):
                            pids_ok = False
                            break
                    if pids_ok:
                        obd_survivors.append(row)
                obd_span.set_attribute("router.candidates_out", len(obd_survivors))

            # Phase 4 — DTC verification with fallback strategy
            with tracer.start_as_current_span("phase.dtc_verify") as dtc_span:
                dtc_span.set_attribute("router.candidates_in", len(obd_survivors))
                dtc_survivors: list[RegistryRow] = []
                for row in obd_survivors:
                    dtc_rule = row.cross_domain_matrix.dtc_lab_status
                    strategy = dtc_rule.fallback_strategy
                    # Determine effective fallback strategy
                    # Top-level fallback_strategy overrides dtc_lab_status (present in
                    # some non_starter / mechanical_wear entries)
                    effective_strategy = row.fallback_strategy or strategy
                    dtc_passed = self._evaluate_dtc_gate(
                        strategy=effective_strategy,
                        rule_p_codes=set(dtc_rule.p_code_match),
                        confirmed_dtcs=confirmed_dtcs,
                        rule_mil=dtc_rule.active_mil,
                        runtime_mil=active_mil,
                    )
                    if dtc_passed:
                        dtc_survivors.append(row)
                dtc_span.set_attribute("router.candidates_out", len(dtc_survivors))

            # Phase 5 — confidence scoring
            scored: list[tuple[RegistryRow, float]] = []
            with tracer.start_as_current_span("phase.score") as score_span:
                score_span.set_attribute("router.candidates_in", len(dtc_survivors))
                for row in dtc_survivors:
                    score = row.confidence_scoring.base_weight
                    # DTC bonus: at least one P-code from the rule matches
                    dtc_rule = row.cross_domain_matrix.dtc_lab_status
                    if rule_dtcs := set(dtc_rule.p_code_match):
                        if rule_dtcs & confirmed_dtcs:
                            score += row.confidence_scoring.bonus_on_dtc_match
                    # MIL bonus: when rule expects active_mil and it is on
                    if dtc_rule.active_mil and active_mil:
                        pass  # already accounted via DTC match bonus

                    score = min(score, _SCORE_CEILING)

                    # INCOMPLETE_OXIDATION confidence capping (lld: §6.4 — T-FX-8)
                    if chemical_state == "INCOMPLETE_OXIDATION":
                        supporting_tags = {
                            DTCRoutingTag.VVT_HISTORY,
                            DTCRoutingTag.THERMAL_HISTORY,
                            DTCRoutingTag.MISFIRE_HISTORY,
                        }
                        has_support = bool(
                            set(routing_tags) & supporting_tags
                        )
                        cap = (
                            _INCOMPLETE_OXIDATION_SUPPORTED_CAP
                            if has_support
                            else _INCOMPLETE_OXIDATION_UNSUPPORTED_CAP
                        )
                        score = min(score, cap)

                    scored.append((row, score))
                score_span.set_attribute("router.candidates_out", len(scored))

                # Symptom prior (T-FX-DNA-3) — bounded additive prior keyed on
                # csv_primary_symptom.  Applied after chemistry/OBD/DTC scoring
                # and INCOMPLETE_OXIDATION capping.  Prior only — no override,
                # no prune-protect.  Blank/absent symptom → neutral.
                csv_symptom = request.symptom_dna.get("_csv_primary_symptom", "")
                if csv_symptom and csv_symptom in self._prior_table:
                    target_family = self._prior_table[csv_symptom]["family"]
                    # Calculate applied weight with load_state modifier if enable_ctxmod is True
                    weight = self._prior_weight
                    if self._enable_ctxmod:
                        # wiki: 10_differential_and_symptom_prior.md §RULE_SYMPTOM_PRIOR line64 (CTXMOD consumes load_state as context modifier, caps at 65 % trust) + config/proposals/entries.yaml COMLab-B (max_symptom_prior_weight 0.65)
                        load_state = request.symptom_dna.get("environmental_conditions", {}).get("load_state")
                        if load_state:
                            symptom_info = self._prior_table[csv_symptom]
                            multiplier = 1.0
                            if isinstance(symptom_info, dict) and "modifiers" in symptom_info:
                                multiplier = float(symptom_info["modifiers"].get(load_state, 1.0))
                            weight *= multiplier
                    for i, (row, score_val) in enumerate(scored):
                        try:
                            kg_node = self._kg.resolve(row.fault_id)
                        except KeyError:
                            continue  # fault_id not in KG — skip prior
                        if kg_node.fault_family == target_family:
                            boosted = score_val + weight
                            if self._enable_ctxmod:
                                # Ceiling is unconditional once symptom-prior is in play, but never drags down score below pre-boost score
                                boosted = min(boosted, max(score_val, self._max_symptom_prior_weight))
                            else:
                                boosted = min(boosted, _SCORE_CEILING)
                            scored[i] = (row, boosted)
                            if score_span.is_recording():
                                score_span.add_event("symptom_prior_applied", {
                                    "rule_id": row.fault_id,
                                    "csv_symptom": csv_symptom,
                                    "target_family": target_family,
                                    "score_before": float(score_val),
                                    "score_after": float(boosted),
                                })

                # Routing-tag discriminator (T-FX-REG-3) — bounded additive lift
                # keyed on routing_tags.  Applied after symptom prior, identical
                # bounded-prior semantics.  Prior only — no override, no prune-
                # protect.  Absent/unmapped tag → neutral.
                for tag in routing_tags:
                    mapping = self._discriminator_table.get(tag)
                    if mapping is None:
                        continue
                    target_family = mapping["family"]
                    for i, (row, score_val) in enumerate(scored):
                        try:
                            kg_node = self._kg.resolve(row.fault_id)
                        except KeyError:
                            continue
                        if kg_node.fault_family == target_family:
                            boosted = min(
                                score_val + self._discriminator_weight,
                                _SCORE_CEILING,
                            )
                            scored[i] = (row, boosted)
                            if score_span.is_recording():
                                score_span.add_event(
                                    "discriminator_applied",
                                    {
                                        "rule_id": row.fault_id,
                                        "tag": tag,
                                        "family": target_family,
                                        "score_before": float(score_val),
                                        "score_after": float(boosted),
                                    },
                                )

                # Per-bank asymmetry (T-COMV2-BANK-FUSE-1) — conflict-aware
                # evidence confidence, never an additive bump or forced override.
                obd_live_data = request.obd_live_data
                if self._enable_bank_fuse and obd_live_data is not None:
                    per_bank_trim_delta = obd_live_data.per_bank_trim_delta
                    bank_verdict = _bank_asymmetry_verdict(
                        per_bank_trim_delta,
                        request.metadata.resolved_horizon,
                    )
                    if (
                        bank_verdict.state == "ASYMMETRIC"
                        and per_bank_trim_delta is not None
                    ):
                        for i, (row, score_val) in enumerate(scored):
                            try:
                                kg_node = self._kg.resolve(row.fault_id)
                            except KeyError:
                                continue
                            if kg_node.fault_family not in _BANK_LOCALIZED_FAMILIES:
                                continue
                            promoted = max(score_val, bank_verdict.confidence)
                            if promoted <= score_val:
                                continue
                            scored[i] = (row, promoted)
                            if score_span.is_recording():
                                score_span.add_event(
                                    "bank_asymmetry_applied",
                                    {
                                        "rule_id": row.fault_id,
                                        "family": kg_node.fault_family,
                                        "per_bank_trim_delta": float(
                                            per_bank_trim_delta
                                        ),
                                        "score_before": float(score_val),
                                        "score_after": float(promoted),
                                        "resolved_horizon": (
                                            request.metadata.resolved_horizon
                                        ),
                                    },
                                )

                # Fuel-system status gate (T-COMV2-FUELSYS-GATE-1) —
                # trim-driven evidence is not diagnostic without O2 feedback.
                if self._enable_fuelsys_gate and obd_live_data is not None:
                    fuel_system_status = obd_live_data.fuel_system_status
                    if (
                        _fuel_system_gate(fuel_system_status)
                        == "OPEN_LOOP_GATED"
                        and fuel_system_status is not None
                    ):
                        for i, (row, score_val) in enumerate(scored):
                            try:
                                kg_node = self._kg.resolve(row.fault_id)
                            except KeyError:
                                continue
                            if kg_node.fault_family not in (
                                "lean_condition",
                                "rich_mixture",
                            ):
                                continue
                            demoted = min(
                                score_val,
                                _OPEN_LOOP_TRIM_CONFIDENCE_CAP,
                            )
                            if demoted >= score_val:
                                continue
                            scored[i] = (row, demoted)
                            if score_span.is_recording():
                                score_span.add_event(
                                    "fuel_system_gated",
                                    {
                                        "rule_id": row.fault_id,
                                        "fuel_system_status": (
                                            fuel_system_status.value
                                        ),
                                        "score_before": float(score_val),
                                        "score_after": float(demoted),
                                    },
                                )

                # ECU perception-vs-reality fuse (T-COMV2-ECU-FUSE-1) —
                # conflict-aware evidence, never an additive bump or override.
                if self._enable_ecu_fuse and obd_live_data is not None:
                    lambda_perception_delta = (
                        obd_live_data.lambda_perception_delta
                    )
                    bank_two_trim = (
                        obd_live_data.total_trim_correction_delta_b2
                    )
                    if (
                        lambda_perception_delta is not None
                        and bank_two_trim is not None
                    ):
                        ecu_verdict = _ecu_fault_verdict(
                            obd_live_data.normalized_obd_lambda,
                            request.gas_lab_output.lambda_chem,
                            sanitized.get("era_lambda_tolerance"),
                            obd_live_data.total_trim_correction_delta,
                            bank_two_trim,
                        )
                        if ecu_verdict.state == "ECU_FAULT":
                            for i, (row, score_val) in enumerate(scored):
                                try:
                                    kg_node = self._kg.resolve(row.fault_id)
                                except KeyError:
                                    continue
                                if kg_node.fault_family != "ecu_fault":
                                    continue
                                promoted = max(score_val, ecu_verdict.confidence)
                                if promoted <= score_val:
                                    continue
                                scored[i] = (row, promoted)
                                if score_span.is_recording():
                                    score_span.add_event(
                                        "ecu_fault_fused",
                                        {
                                            "rule_id": row.fault_id,
                                            "b1": float(
                                                obd_live_data.total_trim_correction_delta
                                            ),
                                            "b2": float(bank_two_trim),
                                            "perception_delta": float(
                                                lambda_perception_delta
                                            ),
                                            "score_before": float(score_val),
                                            "score_after": float(promoted),
                                        },
                                    )

                # Wideband O2 offset confirmation (T-COMV2-O2OFFSET-1) —
                # independent gas truth promotes sensor-fault evidence only.
                if self._enable_o2_offset and obd_live_data is not None:
                    o2_failure_mode = obd_live_data.o2_failure_mode
                    lambda_chem = request.gas_lab_output.lambda_chem
                    if (
                        _resolve_o2_sensor_fault(
                            o2_failure_mode,
                            lambda_chem,
                        )
                        == "WIDEBAND_OFFSET"
                    ):
                        for i, (row, score_val) in enumerate(scored):
                            try:
                                kg_node = self._kg.resolve(row.fault_id)
                            except KeyError:
                                continue
                            if kg_node.fault_family != "sensor_fault":
                                continue
                            promoted = max(score_val, _O2_OFFSET_CONFIDENCE)
                            if promoted <= score_val:
                                continue
                            scored[i] = (row, promoted)
                            if score_span.is_recording():
                                score_span.add_event(
                                    "o2_offset_confirmed",
                                    {
                                        "rule_id": row.fault_id,
                                        "o2_failure_mode": o2_failure_mode.value,
                                        "lambda_chem": float(lambda_chem),
                                        "score_before": float(score_val),
                                        "score_after": float(promoted),
                                    },
                                )

                # ECU hardware digital-lie checker (T-COMV2-ECU-HW-1) —
                # conflict-aware evidence, never an additive bump or override.
                if self._enable_ecu_hw and obd_live_data is not None:
                    ecu_hw_verdict = self._ecu_hw_checker.check(
                        obd_live_data.intake_air_temp_c,
                        obd_live_data.coolant_temp_c,
                        obd_live_data.throttle_pos_pct,
                        obd_live_data.total_trim_correction_delta,
                        obd_live_data.per_bank_trim_delta,
                    )
                    if ecu_hw_verdict.is_ecu_hardware_fault:
                        for i, (row, score_val) in enumerate(scored):
                            try:
                                kg_node = self._kg.resolve(row.fault_id)
                            except KeyError:
                                continue
                            if kg_node.fault_family != "ecu_fault":
                                continue
                            promoted = max(
                                score_val,
                                ecu_hw_verdict.confidence,
                            )
                            if promoted <= score_val:
                                continue
                            scored[i] = (row, promoted)
                            if score_span.is_recording():
                                score_span.add_event(
                                    "ecu_hardware_fault_applied",
                                    {
                                        "rule_id": row.fault_id,
                                        "family": kg_node.fault_family,
                                        "score_before": float(score_val),
                                        "score_after": float(promoted),
                                    },
                                )

                # VE-as-evidence circularity gate (T-COMV2-VE-GATE-1).
                # Only dual MAF/MAP cross-checks provide independent evidence;
                # single-sensor VE faults route to rationality without a score lift.
                if self._enable_ve_gate and obd_live_data is not None:
                    ve_state = _ve_evidence_gate(
                        obd_live_data.ve_pct,
                        obd_live_data.ve_validity,
                        request.metadata.air_metering_strategy,
                    )
                    if ve_state == "VE_EVIDENCE":
                        target = _VE_TARGETS.get(obd_live_data.ve_validity)
                        if target is not None:
                            target_fault_id, target_family = target
                            try:
                                self._kg.resolve(target_fault_id)
                                member_present = True
                            except KeyError:
                                member_present = False
                            for i, (row, score_val) in enumerate(scored):
                                try:
                                    kg_node = self._kg.resolve(row.fault_id)
                                except KeyError:
                                    continue
                                matches_target = (
                                    row.fault_id == target_fault_id
                                    if member_present
                                    else kg_node.fault_family == target_family
                                )
                                if not matches_target:
                                    continue
                                promoted = max(
                                    score_val,
                                    _VE_EVIDENCE_CONFIDENCE,
                                )
                                if promoted <= score_val:
                                    continue
                                scored[i] = (row, promoted)
                                if score_span.is_recording():
                                    score_span.add_event(
                                        "ve_evidence_applied",
                                        {
                                            "rule_id": row.fault_id,
                                            "ve_pct": float(obd_live_data.ve_pct),
                                            "ve_validity": (
                                                obd_live_data.ve_validity.value
                                            ),
                                            "target_member": target_fault_id,
                                            "family_fallback": not member_present,
                                            "score_before": float(score_val),
                                            "score_after": float(promoted),
                                        },
                                    )
                    elif (
                        ve_state == "CIRCULAR_RATIONALITY"
                        and request.metadata.air_metering_strategy is not None
                        and score_span.is_recording()
                    ):
                        score_span.add_event(
                            "ve_circular_rationality",
                            {
                                "ve_pct": float(obd_live_data.ve_pct),
                                "ve_validity": obd_live_data.ve_validity.value,
                                "air_metering_strategy": (
                                    request.metadata.air_metering_strategy.value
                                ),
                                "route": "P0068_MAF_MAP_TPS_RATIONALITY",
                            },
                        )

                # No-start branch: security-lockout vs mechanical (T-COMV2-NOSTART-1)
                # — conflict-aware evidence, never an additive bump or override.
                dtc_lab_output = request.dtc_lab_output
                if self._enable_nostart and dtc_lab_output is not None:
                    ns_verdict = _no_start_branch(
                        dtc_lab_output.mode_06_monitors,
                        dtc_lab_output.freeze_frame.ff_fuel_spark_cut_at_crank,
                    )
                    if ns_verdict.state == "SECURITY_LOCKOUT":
                        node_set = _NOSTART_SECURITY_NODES
                    elif ns_verdict.state == "MECHANICAL":
                        node_set = _NOSTART_MECHANICAL_NODES
                    else:
                        node_set = frozenset()
                    if node_set:
                        for i, (row, score_val) in enumerate(scored):
                            if row.fault_id not in node_set:
                                continue
                            promoted = max(score_val, ns_verdict.confidence)
                            if promoted <= score_val:
                                continue
                            scored[i] = (row, promoted)
                            if score_span.is_recording():
                                score_span.add_event(
                                    "no_start_branch_applied",
                                    {
                                        "rule_id": row.fault_id,
                                        "verdict": ns_verdict.state,
                                        "ff_fuel_spark_cut_at_crank": (
                                            dtc_lab_output.freeze_frame.ff_fuel_spark_cut_at_crank
                                        ),
                                        "score_before": float(score_val),
                                        "score_after": float(promoted),
                                    },
                                )

                # Misfire localisation (T-COMV2-MISFIRE-LOC-1)
                # # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "Misfire localisation" + 13_proposals_register.md §line48 (EP-OBD-IN-07)
                if self._enable_misfire_loc and obd_live_data is not None:
                    misfire_counts = obd_live_data.per_cylinder_misfire_counts
                    trim_delta = obd_live_data.total_trim_correction_delta
                    locality = _misfire_locality(misfire_counts, trim_delta)
                    if locality != "UNAVAILABLE":
                        with tracer.start_as_current_span("misfire_localised") as misfire_span:
                            misfire_span.set_attribute("router.misfire_locality", locality)
                            misfire_span.set_attribute("router.trim_delta", float(trim_delta) if trim_delta is not None else 0.0)
                            misfire_span.add_event("misfire_localised", {
                                "locality": locality,
                                "trim_delta": float(trim_delta) if trim_delta is not None else 0.0,
                            })
                            for i, (row, score_val) in enumerate(scored):
                                try:
                                    kg_node = self._kg.resolve(row.fault_id)
                                except KeyError:
                                    continue
                                rule_family = kg_node.fault_family
                                score_before = score_val
                                applied = False

                                if locality == "SINGLE_CYLINDER":
                                    # Boost cylinder-local ignition/injection and demote trim-driven fuelling
                                    if rule_family in ("misfire", "ignition_fault"):
                                        boosted = max(
                                            score_val,
                                            _EVIDENCE_PROMOTION_CONFIDENCE,
                                        )
                                        if boosted > score_val:
                                            scored[i] = (row, boosted)
                                            applied = True
                                    elif rule_family == "lean_condition":
                                        # Demote below MIN_CONFIDENCE_THRESHOLD to route away
                                        demoted = min(score_val, _EVIDENCE_DEMOTION_CAP)
                                        if demoted < score_val:
                                            scored[i] = (row, demoted)
                                            applied = True
                                elif locality == "GLOBAL":
                                    # Boost fuelling/starvation branch
                                    if rule_family == "lean_condition":
                                        boosted = max(
                                            score_val,
                                            _EVIDENCE_PROMOTION_CONFIDENCE,
                                        )
                                        if boosted > score_val:
                                            scored[i] = (row, boosted)
                                            applied = True

                                if applied:
                                    misfire_span.add_event("misfire_re_ranking_applied", {
                                        "rule_id": row.fault_id,
                                        "family": rule_family,
                                        "score_before": float(score_before),
                                        "score_after": float(scored[i][1]),
                                    })

                # MAF linearity ladder (T-COMV2-MAF-LIN-1)
                # # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "MAF linearity ladder"
                if self._enable_maf_lin and obd_live_data is not None:
                    sensor_error_delta = obd_live_data.sensor_error_delta
                    band = _maf_linearity_band(sensor_error_delta)
                    if band != "WITHIN_SPEC" and sensor_error_delta is not None:
                        with tracer.start_as_current_span("maf_linearity_applied") as maf_span:
                            maf_span.set_attribute("router.maf_linearity_band", band)
                            maf_span.set_attribute("router.sensor_error_delta", float(sensor_error_delta))
                            if obd_live_data.w_theo is not None:
                                maf_span.set_attribute("router.w_theo", float(obd_live_data.w_theo))
                            
                            for i, (row, score_val) in enumerate(scored):
                                score_before = score_val
                                applied = False
                                
                                if band == "CALIBRATION_DRIFT":
                                    if row.fault_id == "ERR-LC-002":
                                        boosted = max(
                                            score_val,
                                            _EVIDENCE_PROMOTION_CONFIDENCE,
                                        )
                                        if boosted > score_val:
                                            scored[i] = (row, boosted)
                                            applied = True
                                    elif row.fault_id == "P0102":
                                        demoted = min(score_val, _EVIDENCE_DEMOTION_CAP)
                                        if demoted < score_val:
                                            scored[i] = (row, demoted)
                                            applied = True
                                elif band == "COMPONENT_FAULT":
                                    if row.fault_id == "P0101":
                                        boosted = max(
                                            score_val,
                                            _EVIDENCE_PROMOTION_CONFIDENCE,
                                        )
                                        if boosted > score_val:
                                            scored[i] = (row, boosted)
                                            applied = True
                                    elif row.fault_id == "P0102":
                                        demoted = min(score_val, _EVIDENCE_DEMOTION_CAP)
                                        if demoted < score_val:
                                            scored[i] = (row, demoted)
                                            applied = True
                                            
                                if applied:
                                    maf_span.add_event("maf_linearity_re_ranking_applied", {
                                        "rule_id": row.fault_id,
                                        "score_before": float(score_before),
                                        "score_after": float(scored[i][1]),
                                    })

                # LTFT load-cell classification (T-COMV2-LTFT-CELL-1)
                # # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "LTFT load-cell distribution"
                if self._enable_ltft_cell and obd_live_data is not None:
                    ltft_cell_vector = obd_live_data.ltft_cell_vector
                    pattern = _ltft_cell_pattern(ltft_cell_vector)
                    if pattern in ("GLOBAL", "LOCALISED") and ltft_cell_vector is not None:
                        with tracer.start_as_current_span("ltft_cell_classified") as cell_span:
                            cell_span.set_attribute("router.ltft_cell_pattern", pattern)
                            cell_span.add_event("ltft_cell_classified", {
                                "pattern": pattern,
                            })
                            for i, (row, score_val) in enumerate(scored):
                                try:
                                    kg_node = self._kg.resolve(row.fault_id)
                                except KeyError:
                                    continue
                                rule_family = kg_node.fault_family
                                score_before = score_val
                                applied = False

                                if pattern == "GLOBAL":
                                    # Boost global cause (MAF / fuel-pressure / O2-bias)
                                    if rule_family in ("lean_condition", "sensor_fault"):
                                        boosted = max(
                                            score_val,
                                            _EVIDENCE_PROMOTION_CONFIDENCE,
                                        )
                                        if boosted > score_val:
                                            scored[i] = (row, boosted)
                                            applied = True
                                elif pattern == "LOCALISED":
                                    # Boost region-specific cause
                                    if rule_family == "lean_condition":
                                        boosted = max(
                                            score_val,
                                            _EVIDENCE_PROMOTION_CONFIDENCE,
                                        )
                                        if boosted > score_val:
                                            scored[i] = (row, boosted)
                                            applied = True

                                if applied:
                                    cell_span.add_event("ltft_cell_re_ranking_applied", {
                                        "rule_id": row.fault_id,
                                        "family": rule_family,
                                        "score_before": float(score_before),
                                        "score_after": float(scored[i][1]),
                                    })

                # Two-point delta signature (T-COMV2-DELTA-1D) — primary rank
                # input. Three falsy short-circuits preserve the static path:
                # key absent (flag off), present=False (single point), or
                # confidence=0.0 (untrusted / architecture-nulled / abstain).
                from comlab.analytics.delta_engine import DeltaEngine

                delta_signature = sanitized.get("delta_signature")
                if delta_signature is not None:
                    for i, (row, score_val) in enumerate(scored):
                        try:
                            kg_node = self._kg.resolve(row.fault_id)
                        except KeyError:
                            continue
                        boosted, applied = DeltaEngine.apply_rank_score(
                            score_val,
                            kg_node.fault_family,
                            delta_signature,
                        )
                        if applied:
                            scored[i] = (row, boosted)
                            if score_span.is_recording():
                                score_span.add_event(
                                    "delta_signature_applied",
                                    {
                                        "rule_id": row.fault_id,
                                        "target_family": (
                                            delta_signature.target_fault_family
                                        ),
                                        "profile": delta_signature.primary_profile,
                                        "score_before": float(score_val),
                                        "score_after": float(boosted),
                                    },
                                )

            # Rank by confidence descending
            with tracer.start_as_current_span("phase.rank") as rank_span:
                rank_span.set_attribute("router.candidates_in", len(scored))
                scored.sort(key=lambda item: item[1], reverse=True)

                winner: RegistryRow | None = None
                winner_score: float = 0.0
                runner_ups: list[tuple[RegistryRow, float]] = []

                if scored:
                    winner, winner_score = scored[0]
                    runner_ups = scored[1:4]  # at most 3 (HLD §4.2 step 8)

                # Emit rule_scored events for Jaeger deep-dive
                for row, score_val in scored:
                    rank_span.add_event("rule_scored", {
                        "rule_id": row.fault_id,
                        "score": float(score_val),
                        "matched_horizon": horizon_str in row.target_horizons,
                        "matched_chemistry": (
                            row.cross_domain_matrix.gas_lab_state == chemical_state
                        ),
                        "matched_obd": True,
                        "matched_dtc": True,
                    })

                # Confidence threshold gate (lld: §6.4)
                # Suppress verdicts with insufficient evidence — a matching rule that
                # scores below threshold is too uncertain to act on.
                if rank_span.is_recording():
                    scored_rule_meta: list[dict[str, Any]] = []
                    for row, score_val in scored:
                        try:
                            rule_family = self._kg.resolve(row.fault_id).fault_family
                        except KeyError:
                            rule_family = ""
                        scored_rule_meta.append({
                            "rule_id": row.fault_id,
                            "fault_family": rule_family,
                            "score": score_val,
                        })
                    _set_expected_rule_attrs(rank_span, scored_rule_meta)

                if winner is not None and winner_score < MIN_CONFIDENCE_THRESHOLD:
                    logger.info(
                        "fault_atlas_router: threshold-miss — %s scored %.2f < %.2f, "
                        "suppressing verdict",
                        winner.fault_id, winner_score, MIN_CONFIDENCE_THRESHOLD,
                    )
                    rank_span.set_attribute("router.threshold_miss", True)
                    rank_span.set_attribute("router.winner_id", winner.fault_id)
                    rank_span.set_attribute("router.winner_score", winner_score)
                    winner = None
                    winner_score = 0.0
                else:
                    rank_span.set_attribute("router.threshold_miss", False)
                    if winner is not None:
                        rank_span.set_attribute("router.winner_id", winner.fault_id)
                        rank_span.set_attribute("router.winner_score", winner_score)
                    else:
                        rank_span.set_attribute("router.winner_id", "__NONE__")
                        rank_span.set_attribute("router.winner_score", 0.0)

                rank_span.set_attribute("router.candidates_out", 1 if winner else 0)

            return TriageVerdict(
                winner=winner,
                winner_score=winner_score,
                runner_ups=runner_ups,
            )

    @staticmethod
    def _evaluate_dtc_gate(
        strategy: str,
        rule_p_codes: set[str],
        confirmed_dtcs: set[str],
        rule_mil: bool,
        runtime_mil: bool,
    ) -> bool:
        """Evaluate DTC fallback strategy for a single rule.

        Strategies (wiki: DTC_VOCABULARY §8):
          - REQUIRE_MATCH: rule fires only with matching DTC
          - PROCEED_ON_MATCH_OR_EMPTY: fire if DTC matches OR rule has no DTCs
          - GAS_ONLY: skip DTC check entirely
        """
        if strategy == "GAS_ONLY":
            return True  # lld: §6.4 — gas chemistry alone decides

        if strategy == "REQUIRE_DTC":
            # Variant seen in cam_timing entries — DTC match is mandatory
            return bool(rule_p_codes & confirmed_dtcs)

        if strategy == "REQUIRE_MATCH":
            # DTC must match and MIL must agree
            if not rule_p_codes:
                return True  # no DTCs to match → pass
            dtc_match = bool(rule_p_codes & confirmed_dtcs)
            mil_ok = (not rule_mil) or runtime_mil
            return dtc_match and mil_ok

        if strategy == "PROCEED_ON_MATCH_OR_EMPTY":
            # Match if DTCs present, or proceed if rule has no DTC requirement
            if not rule_p_codes:
                return True
            dtc_match = bool(rule_p_codes & confirmed_dtcs)
            mil_ok = (not rule_mil) or runtime_mil
            return dtc_match and mil_ok

        # Unknown strategy — allow through (conservative)
        logger.warning("Unknown DTC fallback strategy %r", strategy)
        return True

    # ------------------------------------------------------------------
    # §4.2 step 7 — catalyst-damage override
    # ------------------------------------------------------------------

    def apply_catalyst_damage_override(
        self,
        verdict: TriageVerdict,
        request: OrchestratorInboundRequest,
        analytics_result: PerformanceAnalytics,
    ) -> PerformanceAnalytics:
        """Force CRITICAL_IMMEDIATE_STOP when mil_flashing + P030x DTC present.

        Returns the possibly-mutated analytics block (lld: §6.4 step 7).
        """
        dtc = request.dtc_lab_output
        if dtc is None or not dtc.mil_flashing:
            return analytics_result

        has_p030x = any(_P030X_RE.match(code) for code in dtc.confirmed_dtcs)
        if not has_p030x:
            return analytics_result

        # Force severity to CRITICAL_IMMEDIATE_STOP (lld: §6.4)
        return PerformanceAnalytics(
            kinetic_power_loss_pct=analytics_result.kinetic_power_loss_pct,
            catalyst_efficiency_index_pct=analytics_result.catalyst_efficiency_index_pct,
            lambda_perception_delta=analytics_result.lambda_perception_delta,
            o2_sensor_bias_verdict=analytics_result.o2_sensor_bias_verdict,
            severity_level="CRITICAL_IMMEDIATE_STOP",  # lld: §6.4 — forced override
        )

    # ------------------------------------------------------------------
    # Differential siblings
    # ------------------------------------------------------------------

    @staticmethod
    def build_differential_siblings(
        kg_node: KGNode,
        existing: list[DifferentialSiblingOut] | None = None,
    ) -> list[DifferentialSiblingOut]:
        """Build DifferentialSiblingOut entries from a KG node's
        differential_siblings list.

        Editor-curated siblings are appended after any *existing* runtime-scored
        entries, capped at 5 total per LLD §3.3 Q1.
        """
        result: list[DifferentialSiblingOut] = list(existing or [])
        cap: int = 5  # lld: §3.3 Q1 ruling

        for sibling_id in kg_node.differential_siblings:
            if len(result) >= cap:
                break
            if any(s.fault_id == sibling_id for s in result):
                continue
            result.append(
                DifferentialSiblingOut(
                    fault_id=sibling_id,  # lld: §3.3
                    fault_name=sibling_id,  # lld: §3.3
                    confidence_score=None,  # lld: §3.3 — editor-curated = no runtime score
                    source="editor_curated",  # lld: §3.3 — UI badge
                )
            )

        return result

    def _merge_differential_siblings(
        self,
        runtime_runner_ups: list[tuple[RegistryRow, float]],
        editor_curated: list[str],
    ) -> list[DifferentialSiblingOut]:
        """Merge runtime runner-ups with editor-curated siblings.

        Deduplicate by fault_id, cap at 5. Runtime scores take priority
        over editor-curated entries.
        """
        seen: set[str] = set()
        result: list[DifferentialSiblingOut] = []

        # Runtime entries first (take priority)
        for row, score in runtime_runner_ups:
            if row.fault_id in seen:
                continue
            seen.add(row.fault_id)
            result.append(
                DifferentialSiblingOut(
                    fault_id=row.fault_id,
                    fault_name=row.fault_name or row.fault_id,
                    confidence_score=score,
                    source="runtime",
                )
            )

        # Editor-curated entries (appended if not already present)
        for sibling_id in editor_curated:
            if len(result) >= 5:
                break
            if sibling_id in seen:
                continue
            seen.add(sibling_id)
            result.append(
                DifferentialSiblingOut(
                    fault_id=sibling_id,
                    fault_name=sibling_id,
                    confidence_score=None,
                    source="editor_curated",
                )
            )

        return result[:5]  # lld: §3.3 Q1 — cap at 5

    # ------------------------------------------------------------------
    # Remediation lookup
    # ------------------------------------------------------------------

    def generate_remediation(self, fault_name: str) -> str:
        """Lookup fault_name → repair steps from the registry remediation_map.

        Falls back to a generic message when no entry exists.
        """
        if fault_name in self._remediation_map:
            return self._remediation_map[fault_name]
        # Try fault_id lookup as well
        return self._remediation_map.get(fault_name, "")

    # ------------------------------------------------------------------
    # §4.4 → §4.5 — end-to-end route
    # ------------------------------------------------------------------

    def route(self, sanitized: dict[str, Any]) -> OrchestratorFinalUIOutput:
        """End-to-end Stage B → E entry point (lld: §6.4).

        1. execute_triage_loop → winner + runner-ups
        2. KG resolve → FaultEnrichment
        3. Analytics compute → PerformanceAnalytics
        4. Catalyst-damage override
        5. Assemble OrchestratorFinalUIOutput
        """
        # REG-V2-INTEGRATE: v2 path — delegate to the registry shim.
        # Lazy import keeps the v1 default path free of any registry
        # dependency. The shim returns a plain dict; we reconstruct
        # ``OrchestratorFinalUIOutput`` here to preserve the COMLab API
        # while keeping the registry's COMLab-import firewall intact.
        if self._use_v2_registry:
            from comlab.analytics.delta_engine import DeltaEngine
            from registry.integration_shim import (
                render_ranked_rule as _v2_render_ranked_rule,
                route_case_with_diagnostics as _v2_route_case_with_diagnostics,
            )

            v2_output, diagnostics = _v2_route_case_with_diagnostics(sanitized)
            scored_rules = diagnostics.get("scored_rules", [])
            pruned_rules = diagnostics.get("pruned_rules", [])
            # Symptom dna may arrive via OrchestratorInboundRequest or raw dict
            _req = sanitized.get("request")
            _symptom_dna: dict = (
                _req.symptom_dna
                if _req is not None and hasattr(_req, "symptom_dna")
                else sanitized.get("symptom_dna", {})
            )
            # FT-3: replay the shim's pre-scoring prune attributions as a
            # phase.prune span, mirroring the v1 rule_pruned event contract so
            # 4DLabWired/_jaeger/analyse_failure_modes.py:_prune_event_buckets
            # (and extract_blueprint.py:_rule_pruned_events) can bucket the
            # REG-V2 pruned cases. Telemetry only — no verdict effect.
            with get_tracer(__name__).start_as_current_span("phase.prune") as prune_span:
                prune_span.set_attribute(
                    "router.candidates_in", len(scored_rules) + len(pruned_rules)
                )
                prune_span.set_attribute("router.candidates_out", len(scored_rules))
                for pruned in pruned_rules:
                    prune_span.add_event("rule_pruned", {
                        "rule_id": str(pruned.get("rule_id", "")),
                        "prune_reason": str(pruned.get("prune_reason", "")),
                        "failed_gating_key": str(pruned.get("failed_gating_key", "")),
                    })
            with get_tracer(__name__).start_as_current_span("phase.rank") as rank_span:
                rank_span.set_attribute("router.candidates_in", len(scored_rules))
                for rule in scored_rules:
                    rank_span.add_event("rule_scored", {
                        "rule_id": str(rule.get("rule_id", "")),
                        "score": float(rule.get("score", 0.0)),
                    })
                winner_rule_id = str(diagnostics.get("winner_rule_id", "__NONE__"))
                winner_score = (
                    float(scored_rules[0].get("score", 0.0))
                    if scored_rules and winner_rule_id != "__NONE__"
                    else 0.0
                )
                rank_span.set_attribute("router.threshold_miss", False)
                rank_span.set_attribute("router.winner_id", winner_rule_id)
                rank_span.set_attribute("router.winner_score", winner_score)
                rank_span.set_attribute(
                    "router.candidates_out", 0 if winner_rule_id == "__NONE__" else 1
                )
                if rank_span.is_recording():
                    _set_expected_rule_attrs(rank_span, scored_rules)

            # Symptom prior (T-FX-DNA-3) — v2 path: apply bounded additive
            # prior to scored rules and adjust winner confidence_score.
            csv_symptom_v2 = _symptom_dna.get("_csv_primary_symptom", "")
            if csv_symptom_v2 and csv_symptom_v2 in self._prior_table:
                target_family = self._prior_table[csv_symptom_v2]["family"]
                # Calculate applied weight with load_state modifier if enable_ctxmod is True
                weight = self._prior_weight
                if self._enable_ctxmod:
                    # wiki: 10_differential_and_symptom_prior.md §RULE_SYMPTOM_PRIOR line64 (CTXMOD consumes load_state as context modifier, caps at 65 % trust) + config/proposals/entries.yaml COMLab-B (max_symptom_prior_weight 0.65)
                    load_state = _symptom_dna.get("environmental_conditions", {}).get("load_state")
                    if load_state:
                        symptom_info = self._prior_table[csv_symptom_v2]
                        multiplier = 1.0
                        if isinstance(symptom_info, dict) and "modifiers" in symptom_info:
                            multiplier = float(symptom_info["modifiers"].get(load_state, 1.0))
                        weight *= multiplier
                logger.warning(
                    "symptom_prior v2: applying prior to %s family (weight=%.2f, "
                    "symptom=%s, candidates=%d)",
                    target_family,
                    weight,
                    csv_symptom_v2,
                    len(scored_rules),
                )
                for i, rule in enumerate(scored_rules):
                    if rule.get("fault_family") == target_family:
                        old_score = float(rule.get("score", 0.0))
                        boosted = old_score + weight
                        if self._enable_ctxmod:
                            # Ceiling is unconditional once symptom-prior is in play, but never drags down score below pre-boost score
                            boosted = min(boosted, max(old_score, self._max_symptom_prior_weight))
                        else:
                            boosted = min(boosted, 1.0)
                        scored_rules[i]["score"] = boosted
                        logger.warning(
                            "symptom_prior v2: boosted %s score %.3f → %.3f",
                            rule.get("rule_id", "?"),
                            old_score,
                            boosted,
                        )
                # Re-sort by score descending
                scored_rules.sort(
                    key=lambda r: float(r.get("score", 0.0)), reverse=True
                )
                # Update winner_score in output if top rule is the winner
                if scored_rules and v2_output.get("diagnostic_verdict", {}).get(
                    "is_fault_detected"
                ):
                    new_top_score = float(scored_rules[0].get("score", 0.0))
                    new_top = scored_rules[0]
                    v2_output["diagnostic_verdict"]["confidence_score"] = new_top_score
                    v2_output["diagnostic_verdict"]["confidence"] = new_top_score  # alias
                    logger.warning(
                        "symptom_prior v2: new winner=%s score=%.3f family=%s",
                        new_top.get("rule_id", "?"),
                        new_top_score,
                        new_top.get("fault_family", "?"),
                    )
            else:
                logger.warning(
                    "symptom_prior v2: skipped — symptom=%r in_table=%s table_size=%d weight=%.2f",
                    csv_symptom_v2,
                    csv_symptom_v2 in self._prior_table if csv_symptom_v2 else "N/A (empty)",
                    len(self._prior_table),
                    self._prior_weight,
                )

            # Routing-tag discriminator (T-FX-REG-3) — v2 path.
            # Apply bounded additive lift for each routing_tag whose mapped
            # family appears in scored_rules.
            _v2_routing_tags: list[str] = []
            if (
                _req is not None
                and hasattr(_req, "dtc_lab_output")
                and _req.dtc_lab_output is not None
            ):
                _v2_routing_tags = _req.dtc_lab_output.routing_tags
            for tag in _v2_routing_tags:
                mapping = self._discriminator_table.get(tag)
                if mapping is None:
                    continue
                target_family = mapping["family"]
                for i, rule in enumerate(scored_rules):
                    if rule.get("fault_family") == target_family:
                        old_score = float(rule.get("score", 0.0))
                        boosted = min(old_score + self._discriminator_weight, 1.0)
                        scored_rules[i]["score"] = boosted
            # Re-sort after discriminator
            if _v2_routing_tags:
                scored_rules.sort(
                    key=lambda r: float(r.get("score", 0.0)), reverse=True
                )
                if scored_rules and v2_output.get("diagnostic_verdict", {}).get(
                    "is_fault_detected"
                ):
                    new_top_score = float(scored_rules[0].get("score", 0.0))
                    v2_output["diagnostic_verdict"]["confidence_score"] = new_top_score
                    v2_output["diagnostic_verdict"]["confidence"] = new_top_score

            # Two-point delta signature (T-COMV2-DELTA-2) — production-default
            # v2 scored_rules re-rank. The independent default-off flag contains
            # blast radius; DeltaEngine owns all band/architecture/validity gates.
            if self._enable_delta_v2:
                request: OrchestratorInboundRequest = sanitized["request"]
                delta_signature = DeltaEngine.compute_delta_signature(request)
                delta_applied = False
                for rule in scored_rules:
                    old_score = float(rule.get("score", 0.0))
                    boosted, applied = DeltaEngine.apply_rank_score(
                        old_score,
                        str(rule.get("fault_family", "")),
                        delta_signature,
                    )
                    if applied:
                        rule["score"] = boosted
                        delta_applied = True
                if delta_applied:
                    scored_rules.sort(
                        key=lambda r: float(r.get("score", 0.0)), reverse=True
                    )
                    top_rule = scored_rules[0]
                    v2_output = _v2_render_ranked_rule(
                        sanitized,
                        str(top_rule.get("rule_id", "")),
                        float(top_rule.get("score", 0.0)),
                    )

            return OrchestratorFinalUIOutput(**v2_output)

        request: OrchestratorInboundRequest = sanitized["request"]
        if self._enable_delta and "delta_signature" not in sanitized:
            from comlab.analytics.delta_engine import DeltaEngine

            sanitized["delta_signature"] = DeltaEngine.compute_delta_signature(
                request
            )

        # Step 1 — triage
        verdict = self.execute_triage_loop(sanitized)

        winner = verdict["winner"]
        winner_score = verdict["winner_score"]
        runner_ups = verdict["runner_ups"]

        horizon_str: str = sanitized.get("horizon_ctx") or request.metadata.resolved_horizon
        degradation_mode: str = sanitized.get("degradation_mode", "FULL_FUSION")

        # Step 2 — KG enrichment (Stage C)
        if winner is not None:
            try:
                kg_node = self._kg.resolve(winner.fault_id)
            except KeyError:
                # Winner fault_id not in KG — use sentinel enrichment
                kg_node = None
        else:
            kg_node = None

        # Step 3 — analytics (Stage D)
        cylinder_count = request.metadata.cylinder_count
        dtc_output = request.dtc_lab_output
        downstream_o2 = (
            dtc_output is not None
            and dtc_output.freeze_frame.o2_voltage_b1s1 is not None
        )
        analytics_result = self._analytics.compute(
            request=request,
            cylinder_count=cylinder_count,
            downstream_o2_present=downstream_o2,
            has_catalyst=request.has_catalyst,
        )

        # Step 4 — catalyst-damage override
        analytics_result = self.apply_catalyst_damage_override(
            verdict, request, analytics_result
        )

        # Step 5 — assemble output
        if winner is not None:
            fault_id = winner.fault_id
            fault_name = winner.fault_name or winner.fault_id
            fault_family = kg_node.fault_family if kg_node else "no_fault"  # lld: §3.4

            display_headline = winner.ui_diagnostic_string or fault_name
            remediation = (
                "\n".join(kg_node.ui_remediation_steps)
                if kg_node and kg_node.ui_remediation_steps
                else self.generate_remediation(fault_name)
            )

            # Merge differential siblings
            editor_siblings = kg_node.differential_siblings if kg_node else []
            diff_siblings = self._merge_differential_siblings(
                runner_ups, editor_siblings
            )

            # Build FaultEnrichment from KG node
            if kg_node:
                enrichment = FaultEnrichment(
                    component_group=kg_node.component_group,
                    impacted_subsystems=kg_node.impacted_subsystems,
                    mechanical_failure_mode=kg_node.mechanical_failure_mode,
                    ui_remediation_steps=kg_node.ui_remediation_steps,
                    editor_severity_hint=kg_node.editor_severity_hint,
                )
            else:
                enrichment = FaultEnrichment(
                    component_group="unknown",
                    impacted_subsystems=[],
                    mechanical_failure_mode="KG node not found for resolved fault_id",
                    ui_remediation_steps=["Manual inspection recommended"],
                    editor_severity_hint=None,
                )

            is_fault = True
        else:
            # OPTIMAL_HEALTH / no-match path
            fault_id = "OPTIMAL_HEALTH"  # lld: §6.4 sentinel
            fault_name = "no_fault_detected"
            fault_family = "no_fault"  # lld: §3.1

            # Try KG sentinel node
            try:
                kg_node = self._kg.resolve("OPTIMAL_HEALTH")
                enrichment = FaultEnrichment(
                    component_group=kg_node.component_group,
                    impacted_subsystems=kg_node.impacted_subsystems,
                    mechanical_failure_mode=kg_node.mechanical_failure_mode,
                    ui_remediation_steps=kg_node.ui_remediation_steps,
                    editor_severity_hint=kg_node.editor_severity_hint,
                )
                display_headline = kg_node.mechanical_failure_mode
                remediation = "\n".join(kg_node.ui_remediation_steps)
            except KeyError:
                enrichment = FaultEnrichment(
                    component_group="engine",
                    impacted_subsystems=[],
                    mechanical_failure_mode="No fault detected — all diagnostics within specification",
                    ui_remediation_steps=["Continue routine maintenance"],
                    editor_severity_hint=None,
                )
                display_headline = "No fault detected"
                remediation = "No repair action required."

            diff_siblings = []
            is_fault = False

        verdict_obj = DiagnosticVerdict(
            is_fault_detected=is_fault,
            fault_code=fault_id,
            fault_name=fault_name,
            fault_family=fault_family,  # type: ignore[arg-type]
            display_headline=display_headline[:140],
            confidence_score=winner_score,
            actionable_remediation=remediation,
            differential_siblings=diff_siblings,
        )

        # ExecutionMeta — assembled from sanitized payload context (lld: §6.4)
        directive = sanitized.get("routing_directive")
        if directive is not None:
            reasons_out: list[LabRoutingDirectiveReason] = list(
                getattr(directive, "reasons", [])
            )
            lab_routing = LabRoutingDirectiveOut(
                suppress_gaslab=bool(getattr(directive, "suppress_gaslab", False)),
                suppress_obd_live_pids=bool(getattr(directive, "suppress_obd_live_pids", False)),
                suppress_mode06_ui=bool(getattr(directive, "suppress_mode06_ui", False)),
                cold_start_mode=bool(getattr(directive, "cold_start_mode", False)),
                reasons=reasons_out,
            )
        else:
            lab_routing = LabRoutingDirectiveOut(
                suppress_gaslab=False,
                suppress_obd_live_pids=False,
                suppress_mode06_ui=False,
                cold_start_mode=False,
                reasons=[],
            )
        exec_meta = ExecutionMeta(
            resolved_horizon=horizon_str,  # type: ignore[arg-type]
            degradation_mode=degradation_mode,  # type: ignore[arg-type]
            processing_confidence_rating=(
                "HIGH_ASSURANCE"
                if winner_score >= MIN_CONFIDENCE_THRESHOLD
                else "DEGRADED_ASSURANCE"
            ),
            vin_confidence=request.metadata.vin_confidence.value,  # type: ignore[arg-type]
            lab_routing_directive=lab_routing,  # type: ignore[arg-type]
        )

        return OrchestratorFinalUIOutput(
            session_id=request.metadata.session_id,
            execution_meta=exec_meta,
            diagnostic_verdict=verdict_obj,
            performance_analytics=analytics_result,
            fault_enrichment=enrichment,
            user_input_echo_audit=request.user_input_echo_audit or _sentinel_echo_audit(),
        )


def _sentinel_echo_audit() -> UserInputEchoAudit:
    """Return a minimal sentinel UserInputEchoAudit when none provided."""
    from datetime import datetime, timezone

    from comlab.schemas.ingestion import UserInputEchoAudit

    return UserInputEchoAudit(
        submitted_at=datetime.now(timezone.utc),
        groups=[],
    )
