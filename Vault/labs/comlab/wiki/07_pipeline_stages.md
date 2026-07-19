---
node_type: "wiki"
lab: "comlab"
module: "comlab"
subsystem: "pipeline-orchestration"
implements:
  - "labs/comlab/comlab/core/lab_pipeline_aggregator.py"
  - "labs/comlab/comlab/core/fault_atlas_router.py"
  - "labs/comlab/comlab/core/fault_atlas_kg.py"
  - "labs/comlab/comlab/analytics/power_loss_analytics.py"
consumers:
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py Stage A-D orchestration"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py Stage D severity"
  - "wired: apps/4DLabWired/wired/composition.py LabPipelineAggregator import"
drift_guards:
  - "labs/comlab/tests/unit/test_lab_pipeline_aggregator.py"
  - "labs/comlab/tests/unit/test_fatal_gate_wiring.py"
  - "labs/comlab/tests/unit/test_power_loss_analytics.py"
  - "labs/comlab/tests/e2e/test_diagnostic_engine.py"
tags: [comlab, finished, wiki]
source: "labs/comlab/wiki/07_pipeline_stages.md"
---

# The Pipeline — Stage A → B → C → D

This is COMLab's operational spine today. The rework (`COMWIKI-08`–`12`) is **additive and
default-off at the seams**: when no second frame and no calibration data exist, the engine
behaves exactly as described here. This path is the `SINGLE_POINT` degradation mode and is
**byte-identical** under the regression-lock rule.

```
OrchestratorInboundRequest
   ▼
Stage A  lab_pipeline_aggregator.py   → SanitizedPayload   (or FATAL_INCOMPLETE)
Stage B  fault_atlas_router.py        → TriageVerdict (winner + runner-ups)
Stage C  fault_atlas_kg.py            → FaultEnrichment
Stage D  power_loss_analytics.py      → OrchestratorFinalUIOutput
   ▼
UI
```

## Stage A — fatal gates & sanitisation {#STAGE_A}

Stage A validates, gates, projects DNA (`COMWIKI-03`), and assembles the sanitized payload. Three
**fatal gates** abort the session *before* any fault evaluation — understanding them prevents
misreading an aborted session as "no fault."

- **GATE_GAS_SAMPLE (`ERR-ABORT-001`)** {#GATE_GAS_SAMPLE} — `sample_validity != VALID` (and not
  BORDERLINE). The Rule-of-16 / exhaust-gas-triangle: `CO+CO₂+O₂` must fall ~14–18 %; outside =
  probe air leak / disconnected probe / engine off. Suppressed when `suppress_gaslab`
  (`will_not_start`). [GAS_WIKI §2]
- **GATE_ENGINE_WARMED (`ERR-ABORT-002`)** {#GATE_ENGINE_WARMED} — `engine_warmed == false`.
  Closed-loop trims are meaningless below coolant temp; cold trims are open-loop enrichment
  artifacts. (The 70 °C/75 °C reconciliation is `COMWIKI-04`/`F3`.) Suppressed when
  `suppress_obd_live_pids`.
- **GATE_VIN (`ERR-ABORT-004`)** {#GATE_VIN} — `vin_dna.confidence == NONE`. Without hardware
  architecture the DNA pruning cannot filter inapplicable rules; diagnosis without architecture
  is unsafe.

## Stage B — prune → score {#STAGE_B}

Pruning runs in three passes before any rule is scored (each removes impossibilities, never
creates a verdict):

1. **Horizon prune** (Pass 1) — drop rows whose `target_horizons` excludes the resolved era
   (`COMWIKI-04` `RULE_HORIZON_PRUNE`).
2. **Hardware prune** (Pass 2) — drop rows whose `preconditions` contradict the DNA flags
   (`COMWIKI-03` `RULE_HW_PRUNE`).
3. **POA synthetic tag** (Pass 3) — if `chemical_state == POA_SIGNATURE`, inject
   `DTCRoutingTag.POA_HISTORY` (bridges the GASLab oil-burn signal to the DTC layer with no
   cross-lab import).

### Scoring {#RULE_SCORING}

Each surviving row evaluates its `cross_domain_matrix`:

1. **Gas-state match** — `chemical_state` must equal the row's `gas_lab_state` exactly.
2. **OBD operator checks** — each `obd_live_pids` clause evaluates a field with an operator
   (`GREATER_THAN`, `IN_RANGE`, `DEVIATES_FROM_TARGET`, …).
3. **DTC clause** — per `fallback_strategy`: `REQUIRE_MATCH` (no DTC match → score 0);
   `PROCEED_ON_MATCH_OR_EMPTY` (match adds `bonus_on_dtc_match` to `base_weight`; no match → still
   scores at `base_weight`); `PROCEED` (DTC ignored).

The highest-scoring row wins. **On a tie, the higher `base_weight` (excluding DTC bonus) wins.**
If no row scores above zero → `OPTIMAL_HEALTH`.

> **This tie-break is the measured ceiling (R2).** A generic rule's higher `base_weight` beats
> the correct specific rule, and the intended tie-breaker (the DTC routing tag, weight 0.10) is
> *starved* — 64/90 OUTRANKED cases carry no DTC. Bounded-additive nudges have moved **0 pp**.
> The rework replaces this scoring step with calibrated, conflict-aware late fusion
> (`COMWIKI-08`). [v2: AUDIT Part 1 §1.1]

### Catalyst-damage-imminent override {#RULE_CAT_OVERRIDE}

If `mil_flashing == true` **and** any confirmed DTC matches `^P030[0-9]$` (cylinder-specific
misfire), `severity_level` is forced to `CRITICAL_IMMEDIATE_STOP` regardless of the winning
fault's normal severity. Physical reason: a flashing MIL with a live misfire code means raw fuel
is hitting the catalyst, which can destroy it within minutes. Fires on top of any verdict.

## Stage C — KG enrichment {#STAGE_C}

`fault_id → KGNode` lookup against the frozen `comlab/config/kg/*.json`; assembles
`FaultEnrichment`. Always safe to display even when Stage-B confidence is low (the uncertainty is
in scoring, not enrichment).

## Stage D — power-loss analytics {#STAGE_D}

Quantifies severity of the already-decided verdict: `kinetic_power_loss_pct`,
`catalyst_efficiency_index_pct` (only when `downstream_o2_present`), `severity_level`. Analytics
**quantify**, they do not decide.

## Degradation modes {#CONCEPT_DEGRADATION_MODE}

- **FULL_FUSION** — all four labs valid; full cross-domain evaluation.
- **GAS_DOMINANT** — OBD absent/suppressed (non-starter or no scanner); gas-only verdict;
  confidence ceiling applies.
- **FATAL_INCOMPLETE** — Stage A aborted; no verdict.
- **SINGLE_POINT** *(rework term)* — no second frame / no calibration data → the additive path
  above runs unchanged. The rework's seams are inert in this mode (`COMWIKI-08`/`11`).

`OPEN_LEVERS M2` measures the `FULL_FUSION` vs `GAS_DOMINANT` split to decide whether the ceiling
is gas-bound (`COMWIKI-12`).

## Symptom-routing → lab suppression {#RULE_LAB_SUPPRESSION}

`symptom_dna…engine_state` drives suppression before any fault evaluation:

| engine_state | suppress_gaslab | suppress_obd | suppress_mode06 | cold_start_mode |
|---|---|---|---|---|
| running + always | false | false | false | false |
| running + cold_only | false | false | false | **true** |
| cranking | false | **true** | false | false |
| will_not_start | **true** | **true** | **true** | false |

Suppression skips that lab's fatal gates and excludes its data from the matrix; OBD suppression
sets `degradation_mode = GAS_DOMINANT`.

## Graph relations (explicit)

**STAGE_A** PRODUCES **SanitizedPayload** OR **FATAL_INCOMPLETE**
**STAGE_B** PRODUCES **TriageVerdict** VIA **prune passes → RULE_SCORING**
**RULE_SCORING tie-break** IS **the additive ceiling** REPLACED_BY **FUSE_CONFLICT_AWARE (COMWIKI-08)**
**STAGE_C** ENRICHES_VIA **frozen comlab/config/kg/*.json**
**STAGE_D** QUANTIFIES_SEVERITY (does not decide)
**this additive path** RETAINED_AS **SINGLE_POINT degradation mode** (byte-identical, regression-locked)
**STAGE_A** IMPLEMENTED-BY **comlab/core/lab_pipeline_aggregator.py**
**STAGE_B** IMPLEMENTED-BY **comlab/core/fault_atlas_router.py**
**STAGE_C** IMPLEMENTED-BY **comlab/core/fault_atlas_kg.py**
**STAGE_D** IMPLEMENTED-BY **comlab/analytics/power_loss_analytics.py**

## Core Entities

- **STAGE_A** — Input validation, lab suppression, and DNA projection phase. Consumer: `comlab/core/lab_pipeline_aggregator.py`.
- **STAGE_B** — Candidate fault pruning and operator scoring phase. Consumer: `comlab/core/lab_pipeline_aggregator.py`.
- **STAGE_C** — Knowledge graph enrichment lookup phase. Consumer: `comlab/core/lab_pipeline_aggregator.py and comlab/core/fault_atlas_kg.py`.
- **STAGE_D** — Power-loss and severity analytics phase. Consumer: `comlab/core/lab_pipeline_aggregator.py and comlab/analytics/power_loss_analytics.py`.
- **GATE_GAS_SAMPLE** — Abort check for exhaust gas chemical validity. Consumer: `comlab/core/lab_pipeline_aggregator.py (ERR-ABORT-001)`.
- **GATE_ENGINE_WARMED** — Abort check verifying closed-loop coolant temperature. Consumer: `comlab/core/lab_pipeline_aggregator.py (ERR-ABORT-002)`.
- **GATE_VIN** — Abort check verifying hardware architecture availability. Consumer: `comlab/core/lab_pipeline_aggregator.py (ERR-ABORT-004)`.
- **RULE_SCORING** — Evaluation of row-level cross domain matrices. Consumer: `comlab/core/fault_atlas_router.py`.
- **RULE_CAT_OVERRIDE** — Critical stop override for cylinder-specific misfires. Consumer: `comlab/core/fault_atlas_router.py / comlab/core/lab_pipeline_aggregator.py`.
- **CONCEPT_DEGRADATION_MODE** — Graceful fallback modes (FULL_FUSION, GAS_DOMINANT, FATAL_INCOMPLETE). Consumer: `comlab/core/lab_pipeline_aggregator.py`.
- **RULE_LAB_SUPPRESSION** — Symptom-based suppression of gas/OBD live data. Consumer: `comlab/core/lab_pipeline_aggregator.py`.
