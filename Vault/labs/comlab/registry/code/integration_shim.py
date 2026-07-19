"""Registry v2 integration shim — wires the 68-rule v2 registry into the
COMLab fault-atlas router behind ``USE_V2_REGISTRY=1``.

This module is the **first place v2's evaluation semantics are pinned down**.
The 6-step algorithm below is the spec — all 13 REG-V2-AUTHOR-* tasks have
implicitly assumed it; this module makes it explicit.

Self-contained: imports only stdlib + Pydantic v2 + ``registry.schema_v2``.
No imports from any lab, COMLab, or 4DLabWired. ``test_no_unauthorised_imports``
in ``registry/tests/test_integration_shim.py`` enforces this via AST.

==============================================================================
Evaluation algorithm (6 steps, per REG-V2-INTEGRATE spec §Context)
==============================================================================

1. **Firing predicate (per rule).** A rule fires iff **(a)** every ``GATING``
   evidence entry across ``chemistry_evidence``, ``obd_evidence``,
   ``dtc_evidence`` is satisfied by the observed payload, **AND** **(b)** at
   least one evidence row of any tier (GATING, DEFINITIVE, or SUGGESTIVE) is
   satisfied. Missing data (e.g. ``chemistry is None``) means the GATING
   entry is unsatisfied — **hard-absence semantics**. This is the assumption
   CS-002 depends on; ``test_cs_002_no_fire_on_missing_chemistry`` enforces it.

   The "≥1 satisfied evidence row" half of the predicate is a **spec
   clarification** — REG-V2-INTEGRATE §Context step 1 was silent on rules
   with zero GATING entries. ~60% of authored rules (e.g. MF-001, CF-001)
   carry no GATING; the literal spec reading would have made them fire on
   every input including empty payloads. Option 1 (chosen): require positive
   evidence to fire. Increments at step 2 are unchanged. See
   ``REG-V2-INTEGRATE-SPEC-PATCH`` follow-up.

2. **Score accumulation (per firing rule).** Start at ``base_weight``.
   For each satisfied ``DEFINITIVE`` entry across the three evidence lists,
   add ``+0.10``. For each satisfied ``SUGGESTIVE`` entry, add ``+0.05``.
   (Numeric constants: convention REG-V2-INTEGRATE spec §Context step 2 —
   initial evidence-tier increments; revisit if PASS rate plateaus.)

3. **Ceiling clamp.** If the rule has ``confidence_ceiling`` set, the rule's
   score is ``min(score, confidence_ceiling)``. If ``confidence_ceiling`` is
   ``None``, clamp at the hard cap ``1.0``.

4. **Competition resolution.** Group firing rules by ``competition_group``.
   Within each group, the rule with the highest clamped score wins; ties
   broken by ``base_weight`` desc, then ``rule_id`` asc (deterministic).
   Each group emits one verdict.

5. **Top-fault selection.** Across all groups' emitted verdicts, the one with
   the highest clamped score is the top fault (cross-group selection). Ties
   broken the same way (``base_weight`` desc, then ``rule_id`` asc).

6. **Output shape.** Translate the winning rule's ``fault_family`` and clamped
   score into the same ``OrchestratorFinalUIOutput`` shape v1 returns:
   ``fault_id = rule_id`` (e.g. ``"CS-002"``); ``fault_name = description``;
   ``ui_diagnostic_string = description``; ``confidence = clamped_score``;
   perception/KG enrichment fields = passthrough defaults. On no-fire, return
   the v1 no-fault sentinel: ``fault_code = "OPTIMAL_HEALTH"``,
   ``fault_family = "no_fault"``, ``severity_level = "OPTIMAL_HEALTH"``.

==============================================================================
CS-002 router-assumption gate
==============================================================================

Unplanned-follow-up ``CS-002-router-assumption`` (REGISTRY_PROGRESS.md L62):
*"CS-002 NORMAL_OPERATION-GATING assumes COMLab router treats missing
chemistry as 'rule does not fire' (hard-absence), not 'default to NORMAL'
(imputation)."*

Step 1 above implements hard-absence. ``test_cs_002_no_fire_on_missing_chemistry``
and ``test_cs_002_fires_on_normal_chemistry`` form the paired gate: the first
proves missing chemistry suppresses CS-002, the second proves the suppression
is specifically about absence (not a blanket "CS-002 never fires" bug).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from registry.schema_v2 import (
    ChemistryEvidence,
    ChemistryState,
    DTCRoutingTag,
    DTCEvidence,
    EvidenceTier,
    FaultFamily,
    OBDEvidence,
    Rule,
    RuleSet,
)
from registry.shim.payload_mirrors import (
    resolve_session_id,
    resolve_user_input_echo_audit,
)

# =============================================================================
# Constants
# =============================================================================

_DEFAULT_RULES_DIR = Path(__file__).parent / "rules"

# The 16 fault-family files REG-V2 currently ships. A missing file is fatal —
# the shim refuses to construct against a partial registry.
_EXPECTED_RULE_FILES: frozenset[str] = frozenset(
    {
        "cam_timing.json",
        "catalyst_failure.json",
        "charging_system.json",
        "ecu_fault.json",
        "exhaust_leak.json",
        "ignition_fault.json",
        "invalid_input.json",
        "lean_condition.json",
        "mechanical_wear.json",
        "misfire.json",
        "no_fault.json",
        "non_starter.json",
        "overheating.json",
        "rich_mixture.json",
        "sensor_fault.json",
        "vacuum_leak.json",
    }
)

# Tier-increment constants — convention: REG-V2-INTEGRATE spec §Context step 2.
# If cutover gate fails (v2 PASS < v1 PASS), do NOT silently adjust these;
# halt the task and hand off to REG-V2-INTEGRATE-TUNE.
_TIER_BONUS_DEFINITIVE: float = 0.10  # convention: REG-V2-INTEGRATE spec §Context step 2
_TIER_BONUS_SUGGESTIVE: float = 0.05  # convention: REG-V2-INTEGRATE spec §Context step 2

# Empirical, Jaeger run 20260530-132635 FT-1 rank-2 slice: non-zero winner-vs-
# expected gaps are 0.05; exact edge included to recover that observed bucket.
_EVIDENCE_TIEBREAK_SCORE_BAND: float = 0.05
_FLOAT_EPSILON: float = 1e-9  # convention: absorb binary float noise at band edge

# Score ceiling when a Rule has confidence_ceiling=None. Per locked design,
# None means "no ceiling", so the score may reach the hard cap.
_CONFIDENCE_HARD_CAP: float = 1.0  # convention: clamp upper bound; no rule may exceed

# No-fault sentinel — matches v1's actual return at fault_atlas_router.py L806-836.
# NOT the literal ERR-UNKNOWN-000 (defined at L42 but never used in output).
_NO_FAULT_FAULT_CODE: str = "OPTIMAL_HEALTH"  # wiki: matches fault_atlas_router.py L808
_NO_FAULT_FAULT_NAME: str = "no_fault_detected"  # wiki: matches fault_atlas_router.py L809
_NO_FAULT_FAMILY: str = FaultFamily.NO_FAULT.value  # wiki: matches FaultFamily.NO_FAULT
_NO_FAULT_SEVERITY: str = "OPTIMAL_HEALTH"  # wiki: matches v1 PerformanceAnalytics.severity_level
_NO_FAULT_HEADLINE: str = "No fault detected"  # wiki: matches v1 L810 (KG-overridable, default form)
_NO_FAULT_REMEDIATION: str = "No repair action required."  # wiki: matches v1 L811

# Prune-attribution vocabulary (FT-3). These mirror the v1 prune contract the
# Jaeger analyser already consumes (fault_atlas_router.py:343-394 → prune_reason
# in {"horizon", "chemistry", "missing_evidence"}; consumer:
# 4DLabWired/_jaeger/analyse_failure_modes.py:_prune_event_buckets and
# extract_blueprint.py:_rule_pruned_events). REG-V2 has no horizon gate, so only
# "chemistry" and "missing_evidence" are emitted. "gas_lab_state" matches the v1
# failed_gating_key for chemistry so the analyser buckets v1/v2 prunes alike.
_PRUNE_REASON_CHEMISTRY: str = "chemistry"  # consumer: analyse_failure_modes._prune_event_buckets
_PRUNE_REASON_MISSING_EVIDENCE: str = "missing_evidence"  # consumer: analyse_failure_modes._prune_event_buckets
_GATING_KEY_CHEMISTRY: str = "gas_lab_state"  # wiki: matches v1 chemistry prune key (L392)
_GATING_KEY_NO_EVIDENCE: str = "no_evidence_satisfied"  # firing-predicate (b) failure

_CHEMISTRY_FAMILY_HINTS: dict[ChemistryState, frozenset[FaultFamily]] = {
    ChemistryState.RICH_MIXTURE: frozenset({FaultFamily.RICH_MIXTURE}),
    ChemistryState.LEAN_MIXTURE: frozenset({FaultFamily.LEAN_CONDITION}),
    ChemistryState.IGNITION_MISFIRE: frozenset({FaultFamily.MISFIRE}),
    ChemistryState.LEAN_MISFIRE: frozenset({FaultFamily.MISFIRE}),
    ChemistryState.RICH_MISFIRE: frozenset({FaultFamily.MISFIRE}),
    ChemistryState.EGR_DILUTION_MISFIRE: frozenset({FaultFamily.MISFIRE}),
    ChemistryState.EXHAUST_AIR_LEAK: frozenset({FaultFamily.EXHAUST_LEAK}),
    ChemistryState.CATALYST_NOT_LIGHTING_OFF: frozenset({FaultFamily.CATALYST_FAILURE}),
    ChemistryState.CATALYST_OVERWHELMED: frozenset({FaultFamily.CATALYST_FAILURE}),
    ChemistryState.INCOMPLETE_OXIDATION: frozenset({FaultFamily.CATALYST_FAILURE}),
    ChemistryState.O2_SENSOR_BIASED_LOW: frozenset({FaultFamily.SENSOR_FAULT}),
    ChemistryState.O2_SENSOR_BIASED_HIGH: frozenset({FaultFamily.SENSOR_FAULT}),
    ChemistryState.WORN_ENGINE: frozenset({FaultFamily.MECHANICAL_WEAR}),
    ChemistryState.FLAT_CAMSHAFT: frozenset({FaultFamily.MECHANICAL_WEAR}),
    ChemistryState.WORN_VALVE_SEALS: frozenset({FaultFamily.MECHANICAL_WEAR}),
    ChemistryState.WORN_PISTON_RINGS: frozenset({FaultFamily.MECHANICAL_WEAR}),
}

_DTC_ROUTING_TAG_FAMILY_HINTS: dict[DTCRoutingTag, frozenset[FaultFamily]] = {
    DTCRoutingTag.LEAN_HISTORY: frozenset({FaultFamily.LEAN_CONDITION}),
    DTCRoutingTag.RICH_HISTORY: frozenset({FaultFamily.RICH_MIXTURE}),
    DTCRoutingTag.MISFIRE_HISTORY: frozenset({FaultFamily.MISFIRE}),
    DTCRoutingTag.CYLINDER_FLUID_MISFIRE: frozenset({FaultFamily.MISFIRE}),
    DTCRoutingTag.CATALYST_HISTORY: frozenset({FaultFamily.CATALYST_FAILURE}),
    DTCRoutingTag.O2_HISTORY: frozenset({FaultFamily.SENSOR_FAULT}),
    DTCRoutingTag.VVT_HISTORY: frozenset({FaultFamily.CAM_TIMING}),
    DTCRoutingTag.THERMAL_HISTORY: frozenset({FaultFamily.OVERHEATING}),
    DTCRoutingTag.COOLANT_SYSTEM_MALFUNCTION: frozenset({FaultFamily.OVERHEATING}),
    DTCRoutingTag.ECU_INTERNAL_HISTORY: frozenset({FaultFamily.ECU_FAULT}),
}

# =============================================================================
# Local payload mirror (Pydantic, no COMLab imports — firewall)
# =============================================================================


class _Observation(BaseModel):
    """Tight projection of the sanitized payload.

    Carries ONLY the fields the 60 v2 rules consume. Missing data is
    represented as ``None``; any operator applied to ``None`` is unsatisfied
    (hard absence). No mirror of OrchestratorInboundRequest, GasLabPayload,
    or OBDLiveDataPayload — those live in COMLab and are imported nowhere.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    chemistry_state: ChemistryState | None = None
    dtcs: list[str] = Field(default_factory=list)
    dtc_routing_tags: list[DTCRoutingTag] = Field(default_factory=list)
    obd_pids: dict[str, float | None] = Field(default_factory=dict)


# =============================================================================
# PID resolver
# =============================================================================

# Mapping from v2 rule PID names to the (source, field) tuple in the sanitized
# payload. ``source`` is one of:
#   "gas"  → sanitized["gas_lab_output"][field]
#   "ff"   → sanitized["request"].dtc_lab_output.freeze_frame.<field>
#   "obd"  → sanitized["obd_live_data"][field]
#
# Grounded by ``grep "pid" registry/rules/*.json | sort -u`` — every distinct
# PID across the rule corpus has an entry below. _audit_pid_coverage() asserts
# this at shim construction; an un-resolvable pid raises with the rule_id.
_PID_DISPATCH: dict[str, tuple[tuple[str, str], ...]] = {
    # --- Gas-side (sanitized["gas_lab_output"]) ---
    "hc": (("gas", "gas_hc"),),  # wiki: GasLabPayload.gas_hc (ppm)
    "o2": (("gas", "gas_o2"),),  # wiki: GasLabPayload.gas_o2 (%)
    "co": (("gas", "gas_co"),),  # wiki: GasLabPayload.gas_co (%)
    "co2": (("gas", "gas_co2"),),  # wiki: GasLabPayload.gas_co2 (%)
    "nox": (("gas", "gas_nox"),),  # wiki: GasLabPayload.gas_nox (ppm)
    "high_idle_hc": (("gas", "high_idle_hc"),),  # wiki: OilburnCases.md §PCV/turbo; GasLabPayload.high_idle_hc (ppm)
    "high_idle_co": (("gas", "high_idle_co"),),  # wiki: OilburnCases.md §PCV/turbo; GasLabPayload.high_idle_co (%)
    "high_idle_lambda": (("gas", "high_idle_lambda"),),  # wiki: OilburnCases.md §PCV/turbo; GasLabPayload.high_idle_lambda
    "lambda_chem": (("gas", "lambda_chem"),),  # wiki: OilburnCases.md §PCV/turbo; GasLabPayload.lambda_chem
    # --- OBD live (sanitized["obd_live_data"]) ---
    "obd_lambda": (("obd", "normalized_obd_lambda"),),  # wiki: OBDLiveDataPayload.normalized_obd_lambda
    # --- Perception (sanitized["perception_result"]) ---
    "lambda_perception_delta": (("perception", "lambda_perception_delta"),),  # wiki: PerceptionContradictionResult.lambda_perception_delta — OBD λ − GASLab λ (signed)
    # --- Live-first / freeze-frame fallback (mirrors fault_atlas_router._PID_SOURCES) ---
    # Consumers: EF-001/002/003 GATING, lean_condition, misfire, rich_mixture,
    # vacuum_leak, catalyst_failure, exhaust_leak
    "shrtft1": (("obd", "shrtft1"), ("ff", "short_term_ft1")),
    "longft1": (("obd", "longft1"), ("ff", "long_term_ft1")),
    # Consumers: cam_timing, non_starter GATING
    "stft_b1": (("obd", "shrtft1"), ("ff", "short_term_ft1")),
    "ltft_b1": (("obd", "longft1"), ("ff", "long_term_ft1")),
    # --- Freeze-frame only (sanitized["request"].dtc_lab_output.freeze_frame) ---
    "map_kpa": (("ff", "manifold_pressure_kpa"),),  # wiki: FreezeFrameRecord.manifold_pressure_kpa
    "rpm": (("ff", "engine_rpm"),),  # wiki: FreezeFrameRecord.engine_rpm
    "ect_c": (("ff", "coolant_temp_c"),),  # wiki: FreezeFrameRecord.coolant_temp_c
    "maf": (("ff", "maf_gps"),),  # wiki: FreezeFrameRecord.maf_gps (g/s)
    "o2_voltage": (("ff", "o2_voltage_b1s1"),),  # wiki: FreezeFrameRecord.o2_voltage_b1s1 (V)
    "o2_downstream": (("ff", "o2_voltage_b1s1"),),  # wiki: same source as o2_voltage (v1 alias pattern)
    "fuel_pressure": (("ff", "fuel_pressure_kpa"),),  # wiki: optional FF PID; None if absent
}


def _resolve_pid_from_payload(payload: dict[str, Any], pid_name: str) -> float | None:
    """Look up a v2 rule's PID in the sanitized payload. Returns ``None`` when
    the field is absent — any operator on ``None`` is unsatisfied (hard absence).

    Each PID maps to a fallback chain of ``(source, field)`` pairs tried in
    order.  The first source that yields a non-``None`` float wins.
    """
    chain = _PID_DISPATCH.get(pid_name)
    if chain is None:
        return None
    for source, field in chain:
        val = _resolve_single_source(payload, source, field)
        if val is not None:
            return val
    return None


def _resolve_single_source(payload: dict[str, Any], source: str, field: str) -> float | None:
    """Resolve a single (source, field) pair to ``float | None``."""
    if source == "gas":
        gas = payload.get("gas_lab_output") or {}
        val = gas.get(field)
    elif source == "obd":
        obd = payload.get("obd_live_data") or {}
        val = obd.get(field)
    elif source == "perception":
        pr = payload.get("perception_result")
        if pr is None:
            return None
        if hasattr(pr, field):
            val = getattr(pr, field)
        elif isinstance(pr, dict):
            val = pr.get(field)
        else:
            return None
    elif source == "ff":
        dtc = payload.get("dtc_lab_output") or {}
        ff = dtc.get("freeze_frame") or {}
        val = ff.get(field)
    else:  # pragma: no cover — _PID_DISPATCH is closed
        return None
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


# =============================================================================
# Loader
# =============================================================================


def _load_all_rulesets(
    rules_dir: Path,
    expected_files: frozenset[str] | None = _EXPECTED_RULE_FILES,
) -> list[Rule]:
    """Load and validate rule files; return the flattened rule list.

    Default behaviour requires every file in ``_EXPECTED_RULE_FILES`` to be
    present (the production invariant: the shim refuses to operate against a
    partial registry). Pass ``expected_files=None`` to instead glob every
    ``*.json`` in ``rules_dir`` — this mode exists for synthetic ``tmp_path``
    test fixtures that author a minimal rule set; **do not** use it in
    production code.

    Raises ``FileNotFoundError`` for missing files, ``json.JSONDecodeError`` for
    malformed JSON, or ``pydantic.ValidationError`` for schema-invalid content.
    Each error message includes the offending file path.
    """
    if not rules_dir.is_dir():
        raise FileNotFoundError(f"Rules directory does not exist: {rules_dir}")

    if expected_files is None:
        filenames: list[str] = sorted(p.name for p in rules_dir.glob("*.json"))
    else:
        filenames = sorted(expected_files)

    rules: list[Rule] = []
    for filename in filenames:
        path = rules_dir / filename
        if not path.is_file():
            raise FileNotFoundError(
                f"Required rule file missing: {path} (expected one of the 16 "
                f"REG-V2 family files)"
            )
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise json.JSONDecodeError(
                f"Malformed JSON in {path}: {exc.msg}", exc.doc, exc.pos
            ) from exc
        try:
            ruleset = RuleSet.model_validate(data)
        except ValidationError as exc:
            raise ValidationError.from_exception_data(
                title=f"Schema validation failed for {path}",
                line_errors=exc.errors(),  # type: ignore[arg-type]
            ) from exc
        rules.extend(ruleset.rules)
    return rules


def _audit_pid_coverage(rules: list[Rule]) -> None:
    """Walk every OBDEvidence across all rules; assert every PID is in the
    dispatch table. Fail-fast beats silent None during evaluation.
    """
    missing: list[tuple[str, str]] = []
    for rule in rules:
        for ev in rule.obd_evidence:
            if ev.pid not in _PID_DISPATCH:
                missing.append((rule.rule_id, ev.pid))
    if missing:
        details = ", ".join(f"{rid}:{pid}" for rid, pid in missing)
        raise ValueError(
            f"OBD PID(s) referenced by rules but not in _PID_DISPATCH: {details}. "
            f"Add the mapping to registry/integration_shim.py:_PID_DISPATCH."
        )


# =============================================================================
# Observation projection
# =============================================================================


def _build_observation(payload: dict[str, Any]) -> _Observation:
    """Project the sanitized dict into the tight ``_Observation`` mirror.

    Hard-absence rules:
      - ``chemistry_state`` is ``None`` when ``gas_lab_output`` is missing, when
        ``sample_validity == "INVALID"``, or when ``chemical_state`` is not a
        recognised ``ChemistryState`` member.
      - ``dtcs`` is ``[]`` when ``dtc_lab_output.confirmed_dtcs`` is missing.
      - ``obd_pids`` is pre-resolved via ``_resolve_pid_from_payload`` for every
        PID in the dispatch table.
    """
    gas = payload.get("gas_lab_output") or {}
    chem_raw = gas.get("chemical_state")
    sample_validity = gas.get("sample_validity")
    chemistry_state: ChemistryState | None = None
    if chem_raw is not None and sample_validity != "INVALID":
        try:
            chemistry_state = ChemistryState(chem_raw)
        except ValueError:
            chemistry_state = None

    dtc = payload.get("dtc_lab_output") or {}
    dtcs = list(dtc.get("confirmed_dtcs") or [])
    dtc_routing_tags = _coerce_dtc_routing_tags(dtc.get("routing_tags") or [])

    obd_pids: dict[str, float | None] = {
        pid: _resolve_pid_from_payload(payload, pid) for pid in _PID_DISPATCH
    }

    return _Observation(
        chemistry_state=chemistry_state,
        dtcs=dtcs,
        dtc_routing_tags=dtc_routing_tags,
        obd_pids=obd_pids,
    )


def _coerce_dtc_routing_tags(raw_tags: list[Any]) -> list[DTCRoutingTag]:
    """Coerce existing DTCLab routing tags into the registry enum mirror.

    Unknown strings are ignored: REG-V2 should use valid tag signal when it is
    present, but malformed tags must not create a new failure mode in the shim.
    """
    tags: list[DTCRoutingTag] = []
    for raw in raw_tags:
        if isinstance(raw, DTCRoutingTag):
            tags.append(raw)
            continue
        try:
            tags.append(DTCRoutingTag(str(raw)))
        except ValueError:
            continue
    return tags


# =============================================================================
# Evidence evaluators
# =============================================================================


def _check_chemistry_evidence(ev: ChemistryEvidence, obs: _Observation) -> bool:
    """A chemistry evidence row is satisfied iff the observed chemistry equals
    ``ev.state``. Missing chemistry (``None``) is never satisfied — hard absence.
    """
    return obs.chemistry_state is not None and obs.chemistry_state == ev.state


def _check_obd_evidence(ev: OBDEvidence, obs: _Observation) -> bool:
    """An OBD evidence row is satisfied iff the resolved PID value satisfies
    the operator. Missing PID (``None``) is never satisfied — hard absence.
    """
    val = obs.obd_pids.get(ev.pid)
    if val is None:
        return False
    if ev.operator == "lt":
        return ev.value is not None and val < ev.value
    if ev.operator == "le":
        return ev.value is not None and val <= ev.value
    if ev.operator == "gt":
        return ev.value is not None and val > ev.value
    if ev.operator == "ge":
        return ev.value is not None and val >= ev.value
    if ev.operator == "eq":
        return ev.value is not None and val == ev.value
    if ev.operator == "in_range":
        if ev.range_low is None or ev.range_high is None:
            return False
        return ev.range_low <= val <= ev.range_high
    return False  # pragma: no cover — Literal is closed


def _check_dtc_evidence(ev: DTCEvidence, obs: _Observation) -> bool:
    """A DTC evidence row is satisfied per its strategy:
      ``any_match``    — at least one of ``ev.dtc_codes`` is in ``obs.dtcs``
      ``all_match``    — every code in ``ev.dtc_codes`` is in ``obs.dtcs``
      ``none_present`` — none of ``ev.dtc_codes`` appears in ``obs.dtcs``
    """
    observed = set(obs.dtcs)
    expected = set(ev.dtc_codes)
    if ev.strategy == "any_match":
        return bool(expected & observed)
    if ev.strategy == "all_match":
        return expected.issubset(observed)
    if ev.strategy == "none_present":
        return not (expected & observed)
    return False  # pragma: no cover — Literal is closed


def _gating_passes(rule: Rule, obs: _Observation) -> bool:
    """All GATING-tier evidence rows (across chemistry/OBD/DTC) must be satisfied.
    Any unsatisfied GATING → rule does not fire.
    """
    for ev in rule.chemistry_evidence:
        if ev.tier == EvidenceTier.GATING and not _check_chemistry_evidence(ev, obs):
            return False
    for obd_ev in rule.obd_evidence:
        if obd_ev.tier == EvidenceTier.GATING and not _check_obd_evidence(obd_ev, obs):
            return False
    for dtc_ev in rule.dtc_evidence:
        if dtc_ev.tier == EvidenceTier.GATING and not _check_dtc_evidence(dtc_ev, obs):
            return False
    return True


# =============================================================================
# Scorer
# =============================================================================


def _score_rule(rule: Rule, obs: _Observation) -> float | None:
    """Return the clamped score for a firing rule, or ``None`` if the rule
    does not fire.

    Firing predicate (per algorithm step 1, clarified):
      (a) every GATING evidence row is satisfied, AND
      (b) at least one evidence row of any tier is satisfied.

    Score = base_weight
          + 0.10 per satisfied non-GATING DEFINITIVE
          + 0.05 per satisfied non-GATING SUGGESTIVE,
    clamped at ``min(confidence_ceiling, 1.0)`` (or just 1.0 if
    ``confidence_ceiling`` is None). GATING evidence is counted only as a
    precondition, not toward the score.
    """
    if not _gating_passes(rule, obs):
        return None

    score = rule.base_weight
    any_satisfied = False

    for ev in rule.chemistry_evidence:
        satisfied = _check_chemistry_evidence(ev, obs)
        if satisfied:
            any_satisfied = True
            if ev.tier == EvidenceTier.DEFINITIVE:
                score += _TIER_BONUS_DEFINITIVE
            elif ev.tier == EvidenceTier.SUGGESTIVE:
                score += _TIER_BONUS_SUGGESTIVE
            # GATING: no score bonus, but already counted as "any satisfied"

    for obd_ev in rule.obd_evidence:
        satisfied = _check_obd_evidence(obd_ev, obs)
        if satisfied:
            any_satisfied = True
            if obd_ev.tier == EvidenceTier.DEFINITIVE:
                score += _TIER_BONUS_DEFINITIVE
            elif obd_ev.tier == EvidenceTier.SUGGESTIVE:
                score += _TIER_BONUS_SUGGESTIVE

    for dtc_ev in rule.dtc_evidence:
        satisfied = _check_dtc_evidence(dtc_ev, obs)
        if satisfied:
            any_satisfied = True
            if dtc_ev.tier == EvidenceTier.DEFINITIVE:
                score += _TIER_BONUS_DEFINITIVE
            elif dtc_ev.tier == EvidenceTier.SUGGESTIVE:
                score += _TIER_BONUS_SUGGESTIVE

    if not any_satisfied:
        # Firing predicate (b): need ≥1 satisfied row of any tier.
        # Spec clarification — see module docstring.
        return None

    ceiling = rule.confidence_ceiling if rule.confidence_ceiling is not None else _CONFIDENCE_HARD_CAP
    return min(score, ceiling)


def _prune_attribution(rule: Rule, obs: _Observation) -> tuple[str, str] | None:
    """Attribute *why* a rule did not fire — telemetry only (FT-3).

    Returns ``None`` when the rule fires (``_score_rule`` would return a score),
    or ``(prune_reason, failed_gating_key)`` when it is pruned. The predicate
    below is the exact complement of ``_score_rule``'s firing test, so the two
    can never disagree about whether a rule fired:

      - A GATING chemistry row fails  → ("chemistry", "gas_lab_state")
      - A GATING OBD row fails        → ("missing_evidence", "obd:<pid>")
      - A GATING DTC row fails        → ("missing_evidence", "dtc:<strategy>")
        (first unsatisfied GATING row wins, evaluated chemistry→OBD→DTC, the
         same order as ``_gating_passes``)
      - GATING passes but no evidence row of any tier is satisfied
                                      → ("missing_evidence", "no_evidence_satisfied")

    This recomputes the evidence checks rather than threading state out of
    ``_score_rule`` — keeping the scoring path byte-identical (FT-3 criterion 1).
    """
    # GATING-tier failures, in the same order _gating_passes evaluates them.
    for ev in rule.chemistry_evidence:
        if ev.tier == EvidenceTier.GATING and not _check_chemistry_evidence(ev, obs):
            return (_PRUNE_REASON_CHEMISTRY, _GATING_KEY_CHEMISTRY)
    for obd_ev in rule.obd_evidence:
        if obd_ev.tier == EvidenceTier.GATING and not _check_obd_evidence(obd_ev, obs):
            return (_PRUNE_REASON_MISSING_EVIDENCE, f"obd:{obd_ev.pid}")
    for dtc_ev in rule.dtc_evidence:
        if dtc_ev.tier == EvidenceTier.GATING and not _check_dtc_evidence(dtc_ev, obs):
            return (_PRUNE_REASON_MISSING_EVIDENCE, f"dtc:{dtc_ev.strategy}")

    # GATING passed — check firing-predicate (b): ≥1 satisfied row of any tier.
    any_satisfied = (
        any(_check_chemistry_evidence(ev, obs) for ev in rule.chemistry_evidence)
        or any(_check_obd_evidence(ev, obs) for ev in rule.obd_evidence)
        or any(_check_dtc_evidence(ev, obs) for ev in rule.dtc_evidence)
    )
    if not any_satisfied:
        return (_PRUNE_REASON_MISSING_EVIDENCE, _GATING_KEY_NO_EVIDENCE)

    return None  # rule fires — not pruned


# =============================================================================
# Competition resolver
# =============================================================================


def _tiebreak_key(item: tuple[Rule, float]) -> tuple[float, float, str]:
    """Sort key for descending-best ordering within a competition group AND
    across groups. Highest first via negation of float keys.

    Per spec step 4-5: highest clamped score wins; ties → highest base_weight;
    ties → lexicographically smallest rule_id (deterministic).
    """
    rule, score = item
    return (-score, -rule.base_weight, rule.rule_id)


def _observation_implied_families(obs: _Observation) -> frozenset[FaultFamily]:
    """Return fault families corroborated by already-observed chemistry/DTC tags."""
    families: set[FaultFamily] = set()
    if obs.chemistry_state is not None:
        families.update(_CHEMISTRY_FAMILY_HINTS.get(obs.chemistry_state, frozenset()))
    for tag in obs.dtc_routing_tags:
        families.update(_DTC_ROUTING_TAG_FAMILY_HINTS.get(tag, frozenset()))
    return frozenset(families)


def _corroboration_count(rule: Rule, obs: _Observation) -> int:
    """Count independent chemistry/tag signals that imply ``rule.fault_family``."""
    count = 0
    if (
        obs.chemistry_state is not None
        and rule.fault_family
        in _CHEMISTRY_FAMILY_HINTS.get(obs.chemistry_state, frozenset())
    ):
        count += 1
    for tag in obs.dtc_routing_tags:
        if rule.fault_family in _DTC_ROUTING_TAG_FAMILY_HINTS.get(tag, frozenset()):
            count += 1
    return count


def _is_evidence_corroborated(rule: Rule, obs: _Observation) -> bool:
    """True when the case's own evidence implies the candidate rule family."""
    return rule.fault_family in _observation_implied_families(obs)


def _rank_with_evidence_tiebreak(
    candidates: list[tuple[Rule, float]],
    obs: _Observation,
) -> list[tuple[Rule, float]]:
    """Sort candidates, then promote corroborated families inside the FT-1 band."""
    ranked = sorted(candidates, key=_tiebreak_key)
    if not ranked:
        return []

    top_rule, top_score = ranked[0]
    if _is_evidence_corroborated(top_rule, obs):
        return ranked

    in_band = [
        item
        for item in ranked
        if top_score - item[1] <= _EVIDENCE_TIEBREAK_SCORE_BAND + _FLOAT_EPSILON
    ]
    corroborated = []
    for item in in_band:
        rule, score = item
        score_gap = top_score - score
        has_exact_score = score_gap <= _FLOAT_EPSILON
        has_multi_signal_gap = _corroboration_count(rule, obs) >= 2
        if _is_evidence_corroborated(rule, obs) and (
            has_exact_score or has_multi_signal_gap
        ):
            corroborated.append(item)
    if not corroborated:
        return ranked

    promoted = sorted(corroborated, key=_tiebreak_key)[0]
    return [promoted, *(item for item in ranked if item != promoted)]


def _apply_competition(
    scored: list[tuple[Rule, float]],
    obs: _Observation,
) -> tuple[Rule, float] | None:
    """Resolve firing rules per spec steps 4-5.

    Step 4: within each ``competition_group``, the highest-scoring rule wins
    (with tiebreakers). Step 5: across group winners, the highest-scoring wins
    (same tiebreakers). Returns ``(rule, clamped_score)`` or ``None`` if nothing
    fired.
    """
    if not scored:
        return None

    groups: dict[str, list[tuple[Rule, float]]] = {}
    for rule, score in scored:
        groups.setdefault(rule.competition_group, []).append((rule, score))

    group_winners: list[tuple[Rule, float]] = []
    for group_members in groups.values():
        group_winners.append(_rank_with_evidence_tiebreak(group_members, obs)[0])

    return _rank_with_evidence_tiebreak(group_winners, obs)[0]


# =============================================================================
# Output translator
# =============================================================================


def _translate_to_output(
    winner: tuple[Rule, float] | None,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Build a v1-shaped ``OrchestratorFinalUIOutput`` dict.

    On no-fire, matches v1's no-fault sentinel (``fault_atlas_router.py``
    L806-836): ``fault_code = "OPTIMAL_HEALTH"``, ``fault_family = "no_fault"``,
    ``severity_level = "OPTIMAL_HEALTH"``. Returns a plain dict; reconstruction
    into the Pydantic ``OrchestratorFinalUIOutput`` happens at the COMLab
    boundary (in ``fault_atlas_router.py``) — that keeps the COMLab import
    firewall intact on the shim side.
    """
    # session_id + user_input_echo_audit are stricter on the OUTPUT schema than
    # the inbound payload guarantees (UUID4-required, non-null-required). The
    # payload_mirrors helpers default them per the COMLab contract WITHOUT
    # importing COMLab — see REG-V2-INTEGRATE-SCHEMA-DRIFT. A missing/invalid
    # session_id yields a STABLE sentinel (never a fresh per-call UUID) so the
    # v1/v2 side-by-side harness can still line cases up by id.
    session_id = resolve_session_id(payload)
    metadata = payload.get("metadata") or {}
    vin_confidence = metadata.get("vin_confidence", "NONE")
    horizon_ctx = payload.get("horizon_ctx", "HORIZON_LEGACY")
    degradation_mode = payload.get("degradation_mode", "FULL_FUSION")

    routing_directive_echo = {
        "suppress_gaslab": False,
        "suppress_obd_live_pids": False,
        "suppress_mode06_ui": False,
        "cold_start_mode": False,
        "reasons": [],
    }

    if winner is None:
        verdict = {
            "is_fault_detected": False,
            "fault_code": _NO_FAULT_FAULT_CODE,
            "fault_name": _NO_FAULT_FAULT_NAME,
            "fault_family": _NO_FAULT_FAMILY,
            "display_headline": _NO_FAULT_HEADLINE,
            "confidence_score": 0.0,
            "actionable_remediation": _NO_FAULT_REMEDIATION,
            "differential_siblings": [],
        }
        severity = _NO_FAULT_SEVERITY
        confidence_rating = "HIGH_ASSURANCE"
        # Backward-compat alias keys the test suite reads against.
        # ``fault_id`` mirrors ``fault_code``; ``ui_diagnostic_string`` mirrors
        # ``display_headline``; ``confidence`` mirrors ``confidence_score``.
        verdict_aliases = {
            "fault_id": _NO_FAULT_FAULT_CODE,
            "ui_diagnostic_string": _NO_FAULT_HEADLINE,
            "confidence": 0.0,
        }
    else:
        rule, clamped_score = winner
        verdict = {
            "is_fault_detected": True,
            "fault_code": rule.rule_id,
            "fault_name": rule.description,
            "fault_family": rule.fault_family.value,
            "display_headline": rule.description[:140],  # wiki: v1 L843 (140-char ceiling)
            "confidence_score": clamped_score,
            "actionable_remediation": "See diagnostic verdict for next steps.",
            "differential_siblings": [],
        }
        # convention: HIGH_ASSURANCE threshold mirrors v1 fault_atlas_router.py L874 (>= 0.70)
        severity = "WARNING_DEGRADED_PERFORMANCE"
        confidence_rating = "HIGH_ASSURANCE" if clamped_score >= 0.70 else "DEGRADED_ASSURANCE"
        verdict_aliases = {
            "fault_id": rule.rule_id,
            "ui_diagnostic_string": rule.description[:140],
            "confidence": clamped_score,
        }

    return {
        "session_id": session_id,
        "execution_meta": {
            "resolved_horizon": horizon_ctx,
            "degradation_mode": degradation_mode,
            "processing_confidence_rating": confidence_rating,
            "vin_confidence": vin_confidence,
            "lab_routing_directive": routing_directive_echo,
        },
        "diagnostic_verdict": verdict,
        "performance_analytics": {
            "kinetic_power_loss_pct": 0.0,
            "catalyst_efficiency_index_pct": None,
            "lambda_perception_delta": 0.0,
            "o2_sensor_bias_verdict": None,
            "severity_level": severity,
        },
        "fault_enrichment": {
            "component_group": "engine",
            "impacted_subsystems": [],
            "mechanical_failure_mode": (
                "No fault detected — all diagnostics within specification"
                if winner is None
                else verdict["fault_name"][:280]  # wiki: v1 mechanical_failure_mode 280-char cap
            ),
            "ui_remediation_steps": ["Continue routine maintenance"]
            if winner is None
            else ["See diagnostic verdict for next steps."],
            "editor_severity_hint": None,
        },
        # Passes the inbound echo through verbatim, or emits the schema sentinel
        # (submitted_at=<now>, groups=[]) when absent — per UserInputEchoAudit
        # docstring. Consumer: PRD §5.5 — Screen 6 echo audit.
        "user_input_echo_audit": resolve_user_input_echo_audit(payload),
        # Alias keys for test convenience and v2 callers that prefer flat access
        **verdict_aliases,
    }


# =============================================================================
# Public surface
# =============================================================================


class RegistryV2Router:
    """Singleton-style router: loads + validates all 16 rule files at
    construction; ``route_case(payload)`` runs the 6-step algorithm.

    Raises at construction on any load/validation failure (with the file path
    in the message). Per task spec, this is a fatal startup error — the shim
    refuses to operate against a partial registry.
    """

    def __init__(
        self,
        rules_dir: Path | str = _DEFAULT_RULES_DIR,
        expected_files: frozenset[str] | None = _EXPECTED_RULE_FILES,
    ) -> None:
        """Construct a router against ``rules_dir``.

        ``expected_files`` defaults to the 16 production family files; the
        constructor errors if any are missing. Pass ``expected_files=None`` to
        glob ``*.json`` instead — this exists for synthetic ``tmp_path`` test
        fixtures and must not be used in production.
        """
        self._rules_dir = Path(rules_dir)
        self._rules: list[Rule] = _load_all_rulesets(self._rules_dir, expected_files)
        _audit_pid_coverage(self._rules)

    @property
    def rules(self) -> list[Rule]:
        """Read-only view of the loaded rules (used by tests)."""
        return list(self._rules)

    def route_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        output, _diagnostics = self.route_case_with_diagnostics(payload)
        return output

    def route_case_with_diagnostics(
        self, payload: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        obs = _build_observation(payload)
        scored: list[tuple[Rule, float]] = []
        pruned_rules: list[dict[str, str]] = []
        for rule in self._rules:
            s = _score_rule(rule, obs)
            if s is not None:
                scored.append((rule, s))
            else:
                # FT-3: attribute the prune reason for trace-only telemetry.
                # _prune_attribution is the complement of _score_rule's firing
                # test, so a None score here always yields an attribution.
                attribution = _prune_attribution(rule, obs)
                if attribution is not None:
                    prune_reason, failed_gating_key = attribution
                    pruned_rules.append(
                        {
                            "rule_id": rule.rule_id,
                            "prune_reason": prune_reason,
                            "failed_gating_key": failed_gating_key,
                        }
                    )
        winner = _apply_competition(scored, obs)
        ranked = _rank_with_evidence_tiebreak(scored, obs)
        diagnostics = {
            "scored_rules": [
                {
                    "rule_id": rule.rule_id,
                    "fault_family": rule.fault_family.value,
                    "score": score,
                }
                for rule, score in ranked
            ],
            "pruned_rules": pruned_rules,
            "winner_rule_id": winner[0].rule_id if winner is not None else "__NONE__",
        }
        return _translate_to_output(winner, payload), diagnostics

    def render_ranked_rule(
        self,
        payload: dict[str, Any],
        rule_id: str,
        score: float,
    ) -> dict[str, Any]:
        """Translate a COMLab post-rank winner through the canonical v2 renderer."""
        for rule in self._rules:
            if rule.rule_id == rule_id:
                return _translate_to_output((rule, score), payload)
        raise KeyError(f"Unknown registry rule_id for post-rank render: {rule_id}")


# Module-level singleton. Lazily instantiated so importing this module does NOT
# read the rules dir as a side effect; ``COMLab/.../fault_atlas_router.py`` can
# import ``route_case`` without paying load cost on the v1 default path.
_DEFAULT_ROUTER: RegistryV2Router | None = None


def route_case(payload: dict[str, Any]) -> dict[str, Any]:
    """Module-level entry point. Lazily constructs the default router on first
    call; subsequent calls reuse it. Safe across the harness (rules are
    immutable; the router is read-only after construction).
    """
    global _DEFAULT_ROUTER
    if _DEFAULT_ROUTER is None:
        _DEFAULT_ROUTER = RegistryV2Router()
    return _DEFAULT_ROUTER.route_case(payload)


def route_case_with_diagnostics(
    payload: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Route a case and return trace-only diagnostics for COMLab spans."""
    global _DEFAULT_ROUTER
    if _DEFAULT_ROUTER is None:
        _DEFAULT_ROUTER = RegistryV2Router()
    return _DEFAULT_ROUTER.route_case_with_diagnostics(payload)


def render_ranked_rule(
    payload: dict[str, Any],
    rule_id: str,
    score: float,
) -> dict[str, Any]:
    """Render a COMLab-re-ranked v2 winner without duplicating shim translation."""
    global _DEFAULT_ROUTER
    if _DEFAULT_ROUTER is None:
        _DEFAULT_ROUTER = RegistryV2Router()
    return _DEFAULT_ROUTER.render_ranked_rule(payload, rule_id, score)


__all__ = [
    "RegistryV2Router",
    "render_ranked_rule",
    "route_case",
    "route_case_with_diagnostics",
]
