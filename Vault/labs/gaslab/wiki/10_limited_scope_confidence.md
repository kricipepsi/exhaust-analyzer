---
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "confidence-ranking"
implements:
  - "labs/gaslab/code/ranking.py"
  - "labs/gaslab/code/dna_view.py"
  - "labs/gaslab/code/rule_engine.py"
  - "labs/gaslab/code/resolution.py"
consumers:
  - "gaslab: labs/gaslab/gaslab/ranking.py top-3 confidence ceiling"
  - "gaslab: labs/gaslab/gaslab/rule_engine.py DNA-scoped candidate suppression"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py chemistry confidence input"
drift_guards:
  - "labs/gaslab/tests/unit/test_rank_candidates.py"
  - "labs/gaslab/tests/unit/test_classify_top3.py"
  - "labs/gaslab/tests/unit/test_dna_view.py"
  - "labs/gaslab/tests/unit/test_rule_engine.py"
tags: [gaslab, finished, wiki]
source: "labs/gaslab/wiki/10_limited_scope_confidence.md"
---

# 10. Limited-Scope Behaviour & Confidence Ceilings

> **Chunk summary.** The deliberate scope restriction at low DNA confidence, and the confidence-ceiling model that bounds emitted certainty as a function of match type × DNA tier (never of the fault family).

User decision (2026-05-19): "vehicle without clear DNA profile — there will be limited diagnostic scope in order not to break the diagnostic engine."

## 10.1 Confidence levels {#CONCEPT_CONFIDENCE_LEVEL}

`GasLabDnaView.confidence` ∈ `HIGH | PARTIAL | NONE`.

| Confidence | Meaning |
|---|---|
| `HIGH` | VIN decoded fully; all OEM lookup fields present |
| `PARTIAL` | VIN structurally valid; some fields defaulted from era heuristics |
| `NONE` | VIN unparseable or absent; technician proceeded without DNALab |

## 10.2 Scope shrinkage {#CONCEPT_SCOPE_SHRINKAGE}

When `confidence != HIGH`, GASLab restricts the `chemical_state` candidate set. Equipment-gated values fall out unless DNA still confirms the equipment:

| `chemical_state` | HIGH | PARTIAL | NONE |
|---|---|---|---|
| Chemistry-pure: `NORMAL_OPERATION`, `RICH_MIXTURE`, `LEAN_MIXTURE`, `IGNITION_MISFIRE`*, `LEAN_MISFIRE`, `RICH_MISFIRE`, `EXHAUST_AIR_LEAK`, `HIGH_COMBUSTION_TEMP`, `SAMPLE_INVALID`, `TIMING_OVER_ADVANCED`, `TIMING_RETARDED`, `O2_SENSOR_BIASED_LOW/HIGH`, `WORN_ENGINE`, `FLAT_CAMSHAFT`, `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE`, `WORN_VALVE_SEALS`, `WORN_PISTON_RINGS`, `POA_SIGNATURE`, `CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED`, `VVT_FAILURE`, `EVAP_CANISTER_SATURATED`, `INCOMPLETE_OXIDATION`, `INCOMPLETE_COMBUSTION`, `COOLANT_LEAK_INTERNAL` | ✓ | ✓ | ✓ |
| `CATALYST_NOT_LIGHTING_OFF`, `CATALYST_OVERWHELMED` | ✓ | ✓ if `has_catalyst` known | ✗ |
| `GDI_INTAKE_VALVE_CARBON`, `GDI_HPFP_INTERNAL_SEAL_LEAK` | ✓ if `GDI` | ✗ | ✗ |
| `EGR_STUCK_CLOSED`, `EGR_STUCK_OPEN`, `EGR_DILUTION_MISFIRE` | ✓ if `egr_equipped` | ✗ | ✗ |

\* `IGNITION_MISFIRE` available at all tiers, but cylinder-count math needs `cylinder_count`.

Rule: at `NONE`, GASLab identifies chemistry-pure faults but cannot name equipment-specific ones; at `PARTIAL`, equipment faults only when DNA confirms the equipment. The shrinkage prevents false-positive identification of e.g. a "GDI HPFP leak" on a port-injected engine.

## 10.3 Threshold widening {#CONCEPT_THRESHOLD_WIDENING}

When `target_lambda_v112` / `co_low_idle` / `co_high_idle` are absent, GASLab uses per-era defaults (→ CONCEPT_EURO_SCALING) instead of per-vehicle CoC bounds. Recommended widening: **±30 % at PARTIAL, ±50 % at NONE** on each numeric threshold, to avoid brittle pass/fail boundaries without a vehicle-specific reference.

## 10.4 What COMLab sees

`GasLabPayload.chemical_state` is always one of the 34 enum values. Limited scope is reflected as a smaller candidate set at the engine layer; COMLab sees the chosen value and a confidence note in the warnings stream. There is no separate `LIMITED_SCOPE` enum value.

Known confidence limit: when `has_catalyst` is true / known, a clean tailpipe downstream of a healthy catalyst cannot exonerate the engine on gas alone. The healthy-cat masking trap routes to → CONCEPT_HEALTHY_CAT_MASKING (GASWIKI-07 §7.8) and needs OBDLab/COMLab evidence to resolve.

## 10.5 Confidence ceiling for the top-3 emission {#CONCEPT_CONFIDENCE_CEILING}

Licenses the numeric confidence bounds GASLab uses when it emits a ranked **top-3** `(family, confidence)` list (the statistical-architecture exit). It is the gas-chemistry grounding for those literals.

**Principle.** A reading's diagnostic confidence is bounded by two things GASLab actually has: (a) **how specifically the chemistry pinned the verdict** — a multi-channel named override (→ RULE_MASKING…RULE_LAMBDA_MISMATCH) or a narrow single-fault band is more certain than a deliberately broad catch-all (`POA_SIGNATURE`, `VVT_FAILURE`) or a no-match fallback; and (b) **how tight the reference bounds were** — the DNA-confidence tier, because `HIGH` applies per-vehicle CoC bounds while `PARTIAL`/`NONE` widen them ±30 %/±50 %. Confidence is therefore a **ceiling = f(match type × DNA tier)** — never a function of the family. There is no per-family constant to inflate (deliberate: it forecloses per-family literal-tuning).

**Match types** (by chemistry specificity):

| Match type | Chemistry meaning |
|---|---|
| `DEFINITIVE` | a named override fired (masking / collision / coolant-intrusion) or an RPM-differential route resolved — a corroborated multi-gas pattern. The cam-timing override (→ RULE_WVT) now resolves to SPECIFIC, not DEFINITIVE |
| `SPECIFIC` | one non-catch-all fault won 5-gas + λ bound matching and survived differentiator resolution |
| `CATCH_ALL` | the winner is a catch-all (`POA_SIGNATURE`, `VVT_FAILURE`) — ranked last by `_candidate_rank` |
| `FALLBACK` | no signature matched; `NORMAL_OPERATION` emitted by absence |

**Ceiling table.** The `HIGH` column holds the four anchors; `PARTIAL`/`NONE` are *derived* — the `HIGH` value ÷ the §10.3 widening factor (`PARTIAL` ÷ 1.30, `NONE` ÷ 1.50). The only free parameters are the four `HIGH` anchors.

| Match type | `HIGH` (anchor) | `PARTIAL` (÷1.30) | `NONE` (÷1.50) |
|---|---|---|---|
| `DEFINITIVE` | 0.90 | 0.69 | 0.60 |
| `SPECIFIC`   | 0.80 | 0.62 | 0.53 |
| `CATCH_ALL`  | 0.55 | 0.42 | 0.37 |
| `FALLBACK`   | 0.50 | 0.38 | 0.33 |

**Why the anchors sit there.** `1.00` is reserved — GASLab reads one evidence channel and must not claim certainty alone (cross-lab corroboration is COMLab's job). `DEFINITIVE` 0.90 reflects multi-gas agreement (e.g. masking: HC ≫ 1000 **and** O₂ > 3 % **and** NOₓ < 50). `SPECIFIC` 0.80 is a single narrow-band match. `CATCH_ALL` 0.55 mirrors "ranked last". `FALLBACK` 0.50 is honest uncertainty (absence of a match is weak evidence of health).

**Application.** The per-candidate raw score (signature specificity + count of corroborating channels) is **clamped** to the ceiling for its `(match type, DNA tier)`: emitted confidence = `min(raw_score, ceiling)` ∈ [0,1]. Each candidate is scored/clamped on its own match type. GASLab emits per-candidate confidences and **does not normalise them to sum to 1** — ensemble normalisation across labs is COMLab's Bayesian fusion step.

## Graph relations (explicit)

**CONCEPT_CONFIDENCE_LEVEL** ENUMERATES **HIGH**, **PARTIAL**, **NONE** — DNA-driven confidence tiers
**CONCEPT_CONFIDENCE_LEVEL** CONSUMED_BY **GasLabDnaView.confidence** — HIGH applies CoC bounds, PARTIAL/NONE widen thresholds
**CONCEPT_SCOPE_SHRINKAGE** TRIGGERED_BY **confidence = NONE** — DNALab triage failure narrows diagnostic surface
**CONCEPT_SCOPE_SHRINKAGE** GATED_BY **CONCEPT_DNA_GATED_INGESTION** (GASWIKI-01) — no per-vehicle bounds, no HIGH lane
**CONCEPT_SCOPE_SHRINKAGE** DESCRIBES **cat-masking undetectable without cat**, **cam-timing needs RPM dual-reading**, **GDI needs DNA**, **EGR needs DNA**, **O₂-sensor bias needs trims**, **oil-burn sub-modes need RPM dual-reading**
**CONCEPT_THRESHOLD_WIDENING** DERIVED_FROM **HIGH anchor ÷ widening factor** — PARTIAL ÷ 1.30, NONE ÷ 1.50
**CONCEPT_THRESHOLD_WIDENING** CONSUMED_BY **gaslab.rule_engine._coc_adjust_normal_bounds**
**CONCEPT_CONFIDENCE_CEILING** GATED_BY **match_type** (DEFINITIVE/SPECIFIC/CATCH_ALL/FALLBACK) × **DNA tier** (HIGH/PARTIAL/NONE)
**CONCEPT_CONFIDENCE_CEILING** STATES **DEFINITIVE 0.90, SPECIFIC 0.80, CATCH_ALL 0.55, FALLBACK 0.50** (HIGH anchors)
**CONCEPT_CONFIDENCE_CEILING** CONSUMED_BY **COMLab Bayesian fusion** — GASLab emits per-candidate confidences, never normalises to sum=1
**match_class** GATED_BY **CONCEPT_CONFIDENCE_CEILING** — FALLBACK → 0.50, SPECIFIC → 0.80, DEFINITIVE → 0.90, CATCH_ALL → 0.55

## Core Entities

- **CONCEPT_CONFIDENCE_LEVEL** — HIGH (per-vehicle CoC bounds), PARTIAL (÷1.30 widening), NONE (÷1.50 widening). Consumer: `GasLabDnaView.confidence` → `rule_engine._coc_adjust_normal_bounds`.
- **CONCEPT_SCOPE_SHRINKAGE** — when `confidence = NONE`, the diagnostic surface shrinks: features gated on DNA, RPM dual-reading, OBD trims, or cat-presence are disabled. Consumer: `rule_engine.classify` path selection.
- **CONCEPT_THRESHOLD_WIDENING** — PARTIAL ÷1.30, NONE ÷1.50 from HIGH anchors. Consumer: `rule_engine._coc_adjust_normal_bounds`.
- **CONCEPT_CONFIDENCE_CEILING** — ceiling = f(match_type × DNA tier): anchors 0.90/0.80/0.55/0.50. Consumer: `rule_engine._definitive_match` → COMLab fusion.
