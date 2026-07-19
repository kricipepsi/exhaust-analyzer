"""Pydantic v2 schema for 4DLab registry rules.

Self-contained — imports only stdlib + Pydantic v2.
No imports from any lab, COMLab, or 4DLabWired.

Source-of-truth mirrors (maintained manually — the registry never imports labs):
  ChemistryState  ← GASLab/gaslab/contracts.py ChemicalSignature
  DTCRoutingTag   ← DTCLab/code/dtclab/schemas/vocabulary.py DTCRoutingTag
"""

from enum import StrEnum
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


# =============================================================================
# Vocabulary enums
# =============================================================================


class EvidenceTier(StrEnum):
    """Weight class for a piece of evidence in the v2 rule model.

    Replaces v1's single hard-coded chemistry-gate key.  Every piece of
    chemistry / OBD / DTC evidence carries a tier that the router consumes
    during scoring.
    """

    DEFINITIVE = "DEFINITIVE"  # Pathognomonic — alone nearly confirms the fault
    SUGGESTIVE = "SUGGESTIVE"  # Consistent with the fault but not diagnostic alone
    GATING = "GATING"  # Must be present for the rule to evaluate (v1 prune analogue)


class ChemistryState(StrEnum):
    """Mirror of GASLab ``ChemicalSignature`` (34 values).

    Source: ``GASLab/gaslab/contracts.py``; vocabulary: ``GAS_VOCABULARY §3``.
    Updated: 2026-06-21.
    """

    NORMAL_OPERATION = "NORMAL_OPERATION"
    RICH_MIXTURE = "RICH_MIXTURE"
    LEAN_MIXTURE = "LEAN_MIXTURE"
    IGNITION_MISFIRE = "IGNITION_MISFIRE"
    LEAN_MISFIRE = "LEAN_MISFIRE"
    RICH_MISFIRE = "RICH_MISFIRE"
    EXHAUST_AIR_LEAK = "EXHAUST_AIR_LEAK"
    HIGH_COMBUSTION_TEMP = "HIGH_COMBUSTION_TEMP"
    CATALYST_NOT_LIGHTING_OFF = "CATALYST_NOT_LIGHTING_OFF"
    CATALYST_OVERWHELMED = "CATALYST_OVERWHELMED"
    SAMPLE_INVALID = "SAMPLE_INVALID"
    TIMING_OVER_ADVANCED = "TIMING_OVER_ADVANCED"
    TIMING_RETARDED = "TIMING_RETARDED"
    O2_SENSOR_BIASED_LOW = "O2_SENSOR_BIASED_LOW"
    O2_SENSOR_BIASED_HIGH = "O2_SENSOR_BIASED_HIGH"
    WORN_ENGINE = "WORN_ENGINE"
    FLAT_CAMSHAFT = "FLAT_CAMSHAFT"
    GDI_INTAKE_VALVE_CARBON = "GDI_INTAKE_VALVE_CARBON"
    VACUUM_REGULATOR_DIAPHRAGM_RUPTURE = "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE"
    GDI_HPFP_INTERNAL_SEAL_LEAK = "GDI_HPFP_INTERNAL_SEAL_LEAK"
    WORN_VALVE_SEALS = "WORN_VALVE_SEALS"
    WORN_PISTON_RINGS = "WORN_PISTON_RINGS"
    POA_SIGNATURE = "POA_SIGNATURE"
    CAM_TIMING_RETARDED_MAP = "CAM_TIMING_RETARDED_MAP"
    CAM_TIMING_RETARDED_MAF = "CAM_TIMING_RETARDED_MAF"
    CAM_TIMING_ADVANCED = "CAM_TIMING_ADVANCED"
    EGR_STUCK_CLOSED = "EGR_STUCK_CLOSED"
    EGR_STUCK_OPEN = "EGR_STUCK_OPEN"
    VVT_FAILURE = "VVT_FAILURE"
    EVAP_CANISTER_SATURATED = "EVAP_CANISTER_SATURATED"
    EGR_DILUTION_MISFIRE = "EGR_DILUTION_MISFIRE"
    INCOMPLETE_OXIDATION = "INCOMPLETE_OXIDATION"
    INCOMPLETE_COMBUSTION = "INCOMPLETE_COMBUSTION"
    COOLANT_LEAK_INTERNAL = "COOLANT_LEAK_INTERNAL"


class FaultFamily(StrEnum):
    """Fault families in the v2 curated corpus (16 total).

    13 existing families from the v1 corpus + 3 new families from cvsgaps.md.
    Source: ``registry/CORPUS_AUDIT.md`` §2 table.
    """

    LEAN_CONDITION = "lean_condition"
    MISFIRE = "misfire"
    ECU_FAULT = "ecu_fault"
    RICH_MIXTURE = "rich_mixture"
    CATALYST_FAILURE = "catalyst_failure"
    SENSOR_FAULT = "sensor_fault"
    NO_FAULT = "no_fault"
    MECHANICAL_WEAR = "mechanical_wear"
    CAM_TIMING = "cam_timing"
    EXHAUST_LEAK = "exhaust_leak"
    NON_STARTER = "non_starter"
    IGNITION_FAULT = "ignition_fault"
    INVALID_INPUT = "invalid_input"
    # New families per cvsgaps.md gap analysis
    VACUUM_LEAK = "vacuum_leak"
    OVERHEATING = "overheating"
    CHARGING_SYSTEM = "charging_system"


class DTCRoutingTag(StrEnum):
    """Mirror of DTCLab ``DTCRoutingTag`` (19 values).

    Source: ``DTCLab/code/dtclab/schemas/vocabulary.py``.
    Updated: 2026-05-27.  Includes ``CYLINDER_FLUID_MISFIRE`` which is
    added by FIX-ENUM-1 in the COMLab vocabulary (not yet present in DTCLab
    source but required for the misfire routing gap).
    """

    LEAN_HISTORY = "LEAN_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0171, P0174
    RICH_HISTORY = "RICH_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0172, P0175
    MISFIRE_HISTORY = "MISFIRE_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0300-P0312
    CATALYST_HISTORY = "CATALYST_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0420, P0430
    EGR_HISTORY = "EGR_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0400-P0409
    O2_HISTORY = "O2_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0130-P0161
    INJECTOR_HISTORY = "INJECTOR_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0200-P0212
    VVT_HISTORY = "VVT_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0010-P0023
    EVAP_HISTORY = "EVAP_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0440-P0459
    THERMAL_HISTORY = "THERMAL_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0116-P0128
    ECU_INTERNAL_HISTORY = "ECU_INTERNAL_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0600-P0699
    POA_HISTORY = "POA_HISTORY"  # wiki: DTC_VOCABULARY §4 — gas-chem signature only
    IDLE_CONTROL_HISTORY = "IDLE_CONTROL_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0505-P0511
    GPF_HISTORY = "GPF_HISTORY"  # wiki: DTC_VOCABULARY §4 — P244A, P2459
    BOOST_HISTORY = "BOOST_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0234, P0299
    KNOCK_HISTORY = "KNOCK_HISTORY"  # wiki: DTC_VOCABULARY §4 — P0325-P0334
    COOLANT_SYSTEM_MALFUNCTION = "COOLANT_SYSTEM_MALFUNCTION"  # wiki: DTC_VOCABULARY §4 — P0128/P0117 OL_FAULT
    CYLINDER_FLUID_MISFIRE = "CYLINDER_FLUID_MISFIRE"  # wiki: DTC_VOCABULARY §4 — P030x CL coolant evidence
    UNKNOWN_FORMAT = "UNKNOWN_FORMAT"  # wiki: DTC_VOCABULARY §4 — sentinel for malformed DTC strings


# =============================================================================
# Evidence models
# =============================================================================


class ChemistryEvidence(BaseModel):
    """A chemistry state with evidence weight.

    Replaces v1's single hard-coded ``gas_lab_state`` gate key.  A rule can
    accept multiple chemistry states, each at a different evidence tier.
    """

    state: ChemistryState
    tier: EvidenceTier
    wiki_ref: str | None = Field(default=None, description="// wiki: <FILE> §<n>")

    # Prevent field injection from v1 patterns
    model_config: ClassVar[ConfigDict] = {"extra": "forbid"}


class OBDEvidence(BaseModel):
    """An OBD PID constraint with evidence weight.

    Replaces v1's OBD constraints block.  Each PID constraint is individually
    weighted so the router can accumulate partial evidence.
    """

    pid: str = Field(description="OBD PID name, e.g. longft1, shrtft1, map_kpa, ect_c")
    operator: Literal["lt", "le", "gt", "ge", "eq", "in_range"] = Field(
        description="Comparison operator"
    )
    value: float | None = Field(default=None, description="Scalar threshold (required unless operator is in_range)")
    range_low: float | None = Field(default=None, description="Lower bound (required for in_range)")
    range_high: float | None = Field(default=None, description="Upper bound (required for in_range)")
    tier: EvidenceTier
    units: str | None = Field(default=None, description="e.g. %, kPa, degC, V (informational)")
    wiki_ref: str | None = Field(default=None, description="// wiki: <FILE> §<n>")

    model_config: ClassVar[ConfigDict] = {"extra": "forbid"}

    @model_validator(mode="after")
    def _check_operator_values(self):
        if self.operator == "in_range":
            if self.range_low is None or self.range_high is None:
                raise ValueError(
                    f"OBD {self.pid}: operator 'in_range' requires range_low and range_high"
                )
            if self.range_low >= self.range_high:
                raise ValueError(
                    f"OBD {self.pid}: range_low ({self.range_low}) must be < range_high ({self.range_high})"
                )
        else:
            if self.value is None:
                raise ValueError(
                    f"OBD {self.pid}: operator '{self.operator}' requires a value"
                )
        return self


class DTCEvidence(BaseModel):
    """DTC pattern with evidence weight.

    Replaces v1's DTC fallback strategies (REQUIRE_MATCH, REQUIRE_DTC,
    PROCEED_ON_MATCH_OR_EMPTY).  DTC presence contributes evidence rather
    than acting as a mandatory prune gate.
    """

    dtc_codes: list[str] = Field(min_length=1, description="DTC codes, e.g. ['P0171', 'P0174']")
    strategy: Literal["any_match", "all_match", "none_present"] = Field(
        default="any_match",
        description="How to evaluate the dtc_codes set against observed DTCs"
    )
    tier: EvidenceTier = EvidenceTier.SUGGESTIVE
    wiki_ref: str | None = Field(default=None, description="// wiki: <FILE> §<n>")

    model_config: ClassVar[ConfigDict] = {"extra": "forbid"}


# =============================================================================
# Rule model
# =============================================================================


class Rule(BaseModel):
    """A single v2 diagnostic rule.

    Every rule MUST carry:
    - ``passes_cases`` — at least one curated case ID this rule must PASS
    - ``competition_group`` — which pool of rules it competes in (typically
      the fault family name)
    - ``base_weight`` — starting confidence weight before evidence modifiers

    Numeric thresholds MUST carry ``wiki_ref`` citations on the evidence
    objects that contain them — no bare magic numbers.
    """

    rule_id: str = Field(description="Unique rule identifier, e.g. 'LC-001'")
    fault_family: FaultFamily
    description: str = Field(description="One-sentence description of what this rule detects")

    chemistry_evidence: list[ChemistryEvidence] = Field(default_factory=list)
    obd_evidence: list[OBDEvidence] = Field(default_factory=list)
    dtc_evidence: list[DTCEvidence] = Field(default_factory=list)

    base_weight: float = Field(default=0.70, ge=0.0, le=1.0)
    competition_group: str = Field(description="Rules in the same group compete by score")
    confidence_ceiling: float | None = Field(
        default=None, ge=0.0, le=1.0,
        description="Max confidence when only one rule in a competition group fires "
                    "(no-solo-survivor discipline).  If unset on a solo rule, "
                    "code review must flag it."
    )

    passes_cases: list[str] = Field(min_length=1, description="Curated case IDs this rule must PASS")
    perception_flag: str | None = Field(
        default=None, description="Truth-vs-perception hint, e.g. 'perception_only'"
    )
    precondition: str | None = Field(
        default=None, description="Free-text precondition, e.g. 'vvt_equipped: true'"
    )
    source_wiki_refs: list[str] = Field(
        default_factory=list, description="Wiki sources for this rule's thresholds"
    )

    model_config: ClassVar[ConfigDict] = {"extra": "forbid"}


# =============================================================================
# RuleSet — collection with cross-rule validation
# =============================================================================


class RuleSet(BaseModel):
    """A collection of v2 rules, typically one fault-family file.

    Provides cross-rule validation that cannot be done on individual Rule
    objects (duplicate IDs, solo-survivor detection).
    """

    version: Literal["2.0"] = "2.0"
    fault_family: FaultFamily
    rules: list[Rule] = Field(min_length=1)

    model_config: ClassVar[ConfigDict] = {"extra": "forbid"}

    @model_validator(mode="after")
    def _no_duplicate_rule_ids(self):
        ids = [r.rule_id for r in self.rules]
        seen: set[str] = set()
        for rid in ids:
            if rid in seen:
                raise ValueError(f"Duplicate rule_id '{rid}' in RuleSet")
            seen.add(rid)
        return self

    @model_validator(mode="after")
    def _solo_survivor_check(self):
        """Warn (do not reject) if only one rule has no confidence_ceiling set.

        The 'no solo survivor' discipline: if a competition group has exactly
        one rule, that rule MUST carry a confidence_ceiling.  We validate
        this here as a hard error because the RuleSet is one family file
        and we expect ≥ 2 rules per family at authoring time.
        """
        if len(self.rules) == 1:
            solo = self.rules[0]
            if solo.confidence_ceiling is None:
                raise ValueError(
                    f"Rule '{solo.rule_id}' is the only rule in family "
                    f"'{self.fault_family.value}' — it must set a "
                    f"confidence_ceiling (no-solo-survivor discipline)"
                )
        return self


__all__ = [
    "EvidenceTier",
    "ChemistryState",
    "FaultFamily",
    "DTCRoutingTag",
    "ChemistryEvidence",
    "OBDEvidence",
    "DTCEvidence",
    "Rule",
    "RuleSet",
]
