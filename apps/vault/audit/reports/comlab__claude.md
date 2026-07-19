# Graph-Trust Audit — comlab — agent: claude

## Plan
Running **T-GTA-COM·claude** (first `pending` row owned by Claude, no blockers) per
`T-GTA-METHOD.md`. I audit `_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml` —
classifying every `implements` / `drift_guards` / `consumers` edge across its 9 framed
notes (4 design docs: PRD/HLD/LLD/DLD + 5 wiki chunks: 01/02/03/04/05/06/07/10 = 9 total)
as LIVE / MISLABEL / ORPHAN / PENDING with `file:line` evidence, verifying each named
symbol actually **reads the named field** (not just the label). COMLab has **no seeded
case** (the seeded cases are dtclab/dnalab; COMLab is the terminal fusion spine). Read-only:
I write only this report, touch no map/note/code/graph, and did not read the other agents'
reports (independence). Paths are relative to `/agent_workspace`.

## Counts
- **Total edges classified: 108**
  - **LIVE: 99**
  - **MISLABEL: 2**
  - **ORPHAN: 0**
  - **PENDING: 7**
- Seeded case: **N/A for comlab** (none defined in `GRAPH_TRUST_AUDIT.md`). Self-check below.

All `implements` (33 entries) and `drift_guards` (29 entries) paths resolve with `test -f`
(every path exists — verified in one batch). The two MISLABELs and all PENDINGs are
`consumers` edges; the doc-tier consumer chains (PRD→HLD→LLD→DLD) all resolve.

---

## Classification table

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| **COMLab_PRD.md** | consumers: `hld: …/COMLab_HLD.md` | LIVE | `labs/comlab/docs/COMLab_HLD.md` exists (test -f OK) | — |
| COMLab_PRD.md | consumers: `wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator integration` | PENDING | `apps/wired/wired/composition.py` absent; task spec exists `apps/wired/wired_tasks/T-WIRE-1_compose_labs_comlab.md` | keep `(pending T-WIRE-1)` marker |
| COMLab_PRD.md | implements: `[]` / drift_guards: `[]` | — | empty (PRD requirements tier) | — |
| **COMLab_HLD.md** | consumers: `lld: …/COMLab_LLD.md` | LIVE | `labs/comlab/docs/COMLab_LLD.md` exists | — |
| COMLab_HLD.md | consumers: `dld: …/COMLab_DLD.md` | LIVE | `labs/comlab/docs/COMLab_DLD.md` exists | — |
| COMLab_HLD.md | consumers: `comlab: …/fault_atlas_router.py family-routing architecture` | LIVE | family routing live: `core/fault_atlas_router.py:884` (`cross_domain_matrix.gas_lab_state != chemical_state`), `:1096`/`:1127` (`kg_node.fault_family == target_family`) | — |
| **COMLab_LLD.md** | implements: 15 module paths (lines 38–53) | LIVE | all 15 `test -f` OK (core/*, analytics/delta_engine.py, analytics/power_loss_analytics.py, projection.py, schemas/*) | — |
| COMLab_LLD.md | consumers: `dld: …/COMLab_DLD.md` | LIVE | file exists | — |
| COMLab_LLD.md | consumers: `comlab: …/lab_pipeline_aggregator.py five-phase pipeline implementation` | LIVE | `core/lab_pipeline_aggregator.py:366` `def process(...)`; docstring `:373-374` "Stages: A → symptom routing → B → C → differential → D" | — |
| COMLab_LLD.md | consumers: `wired (pending T-WIRE-1): …composition.py LabPipelineAggregator import` | PENDING | composition.py absent; T-WIRE-1 spec exists | keep marker |
| COMLab_LLD.md | drift_guards: 12 test paths (lines 59–70) | LIVE | all 12 `test -f` OK (unit/* + e2e/test_diagnostic_engine.py) | — |
| **COMLab_DLD.md** | implements: 7 module paths (lines 76–82) incl. `observability/_tracer.py` | LIVE | all 7 `test -f` OK (`observability/_tracer.py` present, 6860 B) | — |
| COMLab_DLD.md | consumers: `comlab: …/lab_pipeline_aggregator.py deployment / latency-budget / observability surfaces` | LIVE | aggregator is the deployment entrypoint `core/lab_pipeline_aggregator.py:366 def process`; observability tier `observability/_tracer.py` exists | — |
| COMLab_DLD.md | consumers: `wired (pending T-WIRE-1): …composition.py LabPipelineAggregator import` | PENDING | composition.py absent; T-WIRE-1 spec exists | keep marker |
| COMLab_DLD.md | drift_guards: 4 test paths (lines 87–90) | LIVE | all 4 `test -f` OK (unit/test_lab_pipeline_aggregator, unit/test_fatal_gate_wiring, e2e/test_pipeline_round_trip, e2e/test_error_codes) | — |
| **01_role_boundaries_fusion_spine.md** | implements: `fault_atlas_router.py`, `schemas/ingestion.py` | LIVE | both `test -f` OK | — |
| 01 | consumers: `comlab: …/lab_pipeline_aggregator.py .process fusion-spine orchestration` | LIVE | `core/lab_pipeline_aggregator.py:366 def process`, orchestrates Stage A→D (`:373-374`); injects router+kg+analytics `:124-132` | — |
| 01 | consumers: `comlab: …/fault_atlas_router.py family-map verdict` | LIVE | `core/fault_atlas_router.py:1096`/`:1127` `kg_node.fault_family == target_family`; `:884` gas_lab_state gating | — |
| 01 | consumers: `wired (pending T-WIRE-1): …composition.py LabPipelineAggregator import` | PENDING | composition.py absent; T-WIRE-1 spec exists | keep marker |
| 01 | drift_guards: `test_fault_atlas_router.py`, `test_lab_pipeline_aggregator.py` | LIVE | both `test -f` OK | — |
| **02_lab_input_contract.md** | implements: `schemas/ingestion.py` | LIVE | `test -f` OK | — |
| 02 | consumers: `comlab: …/fault_atlas_router.py chemical_state / total_trim_correction_delta / confirmed_dtcs routing` | LIVE | `core/fault_atlas_router.py:949` `chemical_state = request.gas_lab_output.chemical_state`; `:312`/`:333` reads `total_trim_correction_delta`; `:995` `set(dtc_output.confirmed_dtcs)`, `:1045` `rule_dtcs & confirmed_dtcs` | — |
| 02 | consumers: `comlab: …/ecu_hardware_checker.py vin_dna consumption` | **MISLABEL** | `core/ecu_hardware_checker.py` `check()` (`:31-74`) reads `intake_air_temp_c`, `coolant_temp_c`, `throttle_pos_pct`, `total_trim_correction_delta`, `per_bank_trim_delta` — **grep `vin_dna` in ecu_hardware_checker.py = 0 hits**. `vin_dna` is read by `core/horizon_context_injector.py:75-79` and `projection.py:53`, not here. | relabel edge → `ecu_hardware_checker.py reads OBD rails (intake_air_temp_c / coolant_temp_c / throttle_pos_pct / total_trim_correction_delta / per_bank_trim_delta)`; move any `vin_dna` consumer claim to note 03/04 (horizon_context_injector / projection) |
| 02 | consumers: `comlab: …/lab_pipeline_aggregator.py engine_state ingestion` | **MISLABEL** | **grep `engine_state` in lab_pipeline_aggregator.py = 0 hits.** The aggregator forwards `request.symptom_dna` to `route_symptom` (`:327`, `:451`, `:634`); the actual `engine_state` reader is `core/symptom_router.py:60` `engine_state = env.get("engine_state", "")` (`:68-83`). | relabel edge → `symptom_router.py route_symptom engine_state suppression (symptom_router.py:60,68)` — the aggregator only passes `symptom_dna` through, it does not read `engine_state` |
| 02 | drift_guards: `test_ingestion_high_idle.py`, `test_fuel_system_gate.py`, `test_fault_atlas_router.py` | LIVE | all 3 `test -f` OK | — |
| **03_vehicle_dna_pruning.md** | implements: `ecu_hardware_checker.py`, `schemas/lab_dna_views.py`, `projection.py` | LIVE | all 3 `test -f` OK | — |
| 03 | consumers: `comlab: …/ecu_hardware_checker.py RULE_HW_PRUNE (Stage B Pass 2)` | LIVE | `ecu_hardware_checker.ECUHardwareChecker.check` invoked live at `core/fault_atlas_router.py:1312` (`self._ecu_hw_checker.check(...)`), instantiated `:623`, applied `:1319`. `RULE_HW_PRUNE` is a **wiki rule-ID, not a code literal** (grep = 0); reader of the contracted hardware logic exists → LIVE. | optional: drop the `RULE_HW_PRUNE` token (wiki-ID, not a symbol) to avoid implying a code literal |
| 03 | consumers: `comlab: …/delta_engine.py VE polymorph selection` | LIVE (note) | `analytics/delta_engine.py:215`/`:279-289` `_architecture_gate` reads `air_metering_strategy` + `induction_type` (the VIN-driven polymorphic switches, schemas/vocabulary.py:111,138,152) BEFORE any ΔTrim profile (`:17-20`). Reader exists. **Caveat:** the edge says "VE polymorph"; delta_engine gates on air-metering/induction polymorphs, not `ve_pct`/`ve_validity` (those are router-gated: schemas/vocabulary.py:341). Borderline-MISLABEL on wording, but a real reader of the VIN polymorph selection exists → **LIVE**. | tighten wording → `delta_engine.py architecture-gate selection (air_metering_strategy / induction_type)`; `ve_pct`/`ve_validity` gating is in fault_atlas_router, not delta_engine |
| 03 | consumers: `comlab: …/lab_pipeline_aggregator.py DNA-confidence degradation` | LIVE | `core/lab_pipeline_aggregator.py:350` `if request.metadata.vin_confidence == VinConfidence.NONE` (fatal-gate degradation); `:270` emits `vin_confidence`; `_map_degradation` `:192-196` | — |
| 03 | drift_guards: `test_ecu_hardware_checker.py`, `test_projection.py` | LIVE | both `test -f` OK | — |
| **04_horizon_eras.md** | implements: `horizon_context_injector.py` | LIVE | `test -f` OK | — |
| 04 | consumers: `comlab: …/horizon_context_injector.py RULE_HORIZON_PRUNE / era-mask thresholds` | LIVE | `core/horizon_context_injector.py:35` `resolved_horizon`, `:38` `threshold_mask` (from eras_sensitivity_masks.yaml), `:63-67` `_load_masks`. `RULE_HORIZON_PRUNE` is a wiki rule-ID (not a code literal); the era-mask threshold reader exists → LIVE. | optional: drop `RULE_HORIZON_PRUNE` wiki-ID token |
| 04 | consumers: `comlab: …/fault_atlas_router.py per-era RULE_SCORING thresholds` | LIVE | `core/fault_atlas_router.py:311` `era_lambda_tolerance`, `:340` `abs(normalized_obd_lambda - lambda_chem) <= era_lambda_tolerance`; ConfidenceScoring class `:199-213`. `RULE_SCORING` is a wiki rule-ID; per-era scoring reader exists → LIVE. | optional: drop `RULE_SCORING` wiki-ID token |
| 04 | drift_guards: `test_horizon_context_injector.py` | LIVE | `test -f` OK | — |
| **05_fault_taxonomy.md** | implements: `fault_atlas_router.py`, `config/global_fault_registry.json` | LIVE | both `test -f` OK | — |
| 05 | consumers: `comlab: …/fault_atlas_router.py RULE_GAS_ROUTE / taxonomy-table routing` | LIVE | taxonomy loader live: `core/fault_atlas_router.py:608` `self._load_taxonomy_backbone()`, `:726-753` loads `config/proposals/taxonomy_backbone.yaml` families; gas-state routing `:884`. `RULE_GAS_ROUTE` is a **wiki rule-ID, not a code literal** (grep = 0 across comlab); the taxonomy-table reader exists → LIVE. | optional: drop `RULE_GAS_ROUTE` wiki-ID token (keep "taxonomy-table routing") |
| 05 | consumers: `comlab: …/fault_atlas_kg.py fault_id enrichment` | LIVE | `core/fault_atlas_kg.py:58 resolve(fault_id)` → `KGNode`; consumed by router `:1093`/`:1124` `kg_node = self._kg.resolve(row.fault_id)` and aggregator `:521` `self._kg.resolve(fc)` → `kg_node.fault_family` `:524` | — |
| 05 | drift_guards: `test_fault_atlas_router.py`, `e2e/test_kg_registry_consistency.py` | LIVE | both `test -f` OK | — |
| **06_fault_atlas_families.md** | implements: `fault_atlas_kg.py`, `config/kg/rich_mixture.json` | LIVE | both `test -f` OK | — |
| 06 | consumers: `comlab: …/fault_atlas_kg.py 12-family JSON loading` | LIVE | `core/fault_atlas_kg.py:93-105` `_load_all` globs `kg/*.json` (skips `_`-prefixed `:97`). Dir has **13** family files (cam_timing, catalyst_failure, ecu_fault, exhaust_leak, ignition_fault, invalid_input, lean_condition, mechanical_wear, misfire, no_fault, non_starter, rich_mixture, sensor_fault) + `_kg_schema.json`. Loader is live; "12-family" count is approximate (now 13). | optional: update count "12-family" → "13-family" (cosmetic; loader is count-agnostic) |
| 06 | consumers: `comlab: …/fault_atlas_router.py family routing` | LIVE | `core/fault_atlas_router.py:1096`/`:1127` `kg_node.fault_family == target_family` | — |
| 06 | consumers: `comlab: …/delta_engine.py collision-set -> delta motivation` | LIVE | `analytics/delta_engine.py:13` "delta-matched fault family is promoted above base-weighted static signatures"; `:237-255` promotion of `candidate_family` vs `target_fault_family`. `RULE_COLLISION_SET` referenced as wiki-ID in router comment `core/fault_atlas_router.py:321`. Reader exists → LIVE. | — |
| 06 | drift_guards: `test_fault_atlas_kg.py`, `test_kg_schema.py`, `test_kg_population.py` | LIVE | all 3 `test -f` OK | — |
| **07_pipeline_stages.md** | implements: `lab_pipeline_aggregator.py`, `fault_atlas_router.py`, `fault_atlas_kg.py`, `power_loss_analytics.py` | LIVE | all 4 `test -f` OK | — |
| 07 | consumers: `comlab: …/lab_pipeline_aggregator.py Stage A-D orchestration` | LIVE | `core/lab_pipeline_aggregator.py:366 def process`, docstring `:373-374` Stage A→D | — |
| 07 | consumers: `comlab: …/power_loss_analytics.py Stage D severity` | LIVE | live on the normal path (NOT just stubbed): injected into router `core/fault_atlas_router.py:579`, called `:2117` `self._analytics.compute(...)`; `analytics/power_loss_analytics.py:183 def compute` → `:244 _map_severity` → `severity_level`. Aggregator's "stubbed" comment (`:561,374`) is the **override/test path only**; live path reads `router_perf.severity_level` `:499`. | — |
| 07 | consumers: `wired (pending T-WIRE-1): …composition.py LabPipelineAggregator import` | PENDING | composition.py absent; T-WIRE-1 spec exists | keep marker |
| 07 | drift_guards: `test_lab_pipeline_aggregator.py`, `test_fatal_gate_wiring.py`, `test_power_loss_analytics.py`, `e2e/test_diagnostic_engine.py` | LIVE | all 4 `test -f` OK | — |
| **10_differential_and_symptom_prior.md** | implements: `lab_pipeline_aggregator.py`, `symptom_router.py`, `schemas/response.py` | LIVE | all 3 `test -f` OK | — |
| 10 | consumers: `comlab: …/lab_pipeline_aggregator.py CONCEPT_DIFFERENTIAL / RULE_TOPK` | LIVE | differential siblings live: aggregator `:522` `self._router.build_differential_siblings(kg_node)` → router `:1792 def build_differential_siblings`; top-K cap enforced in schema `schemas/response.py:103` `differential_siblings: list[...] = Field(..., max_length=5)`. `CONCEPT_DIFFERENTIAL`/`RULE_TOPK` are wiki concept-IDs; readers exist → LIVE. | optional: drop wiki concept-IDs from the edge label |
| 10 | consumers: `comlab: …/symptom_router.py RULE_SYMPTOM_PRIOR (capped)` | LIVE | the **capped symptom prior** is implemented in `core/fault_atlas_router.py:1078-1090` (`self._prior_table`, `self._prior_weight`, cap `_max_symptom_prior_weight = 0.65` `:602,683`), not in `symptom_router.py` (which only does lab-suppression routing, no `prior`/`cap` — grep = 0). `RULE_SYMPTOM_PRIOR` literal lives in router `:1083`. Reader exists and is unit-tested (`test_symptom_prior.py`) → **LIVE**, but the edge names the wrong file. | borderline-MISLABEL on file attribution: the capped-prior reader is `fault_atlas_router.py:1078`, not `symptom_router.py`. Recommend relabel → `fault_atlas_router.py RULE_SYMPTOM_PRIOR (capped 0.65)`. Classed LIVE because a real reader exists; flagging the file mismatch for the union. |
| 10 | consumers: `wired (pending T-WIRE-1): …composition.py OrchestratorFinalUIOutput rendering` | PENDING | composition.py absent; `OrchestratorFinalUIOutput` is produced by `core/lab_pipeline_aggregator.py:308,504,575` but the *renderer* is the unbuilt wired app | keep `(pending T-WIRE-1)` marker |
| 10 | drift_guards: `test_symptom_router.py`, `test_symptom_prior.py`, `test_lab_pipeline_aggregator.py` | LIVE | all 3 `test -f` OK | — |

---

## Self-check (no seeded case for comlab)
`GRAPH_TRUST_AUDIT.md` defines seeded cases only for **dtclab** (power_loss_analytics ORPHAN;
perception_contradiction MISLABEL) and **dnalab** (VehicleDNA readers LIVE). None apply to
comlab. I applied the **same method** the seeded cases test:
- **LIVE-but-unwired is LIVE, not ORPHAN:** all 7 `apps/wired/.../composition.py` edges are
  marked **PENDING** (the file doesn't exist yet; `T-WIRE-1` spec exists) — not ORPHAN. The
  COMLab-internal readers exercised only by unit tests (e.g. delta_engine, power_loss_analytics)
  are **LIVE**, matching the dnalab ruling ("no live caller pre-wire is expected").
- **MISLABEL = reader of a different field:** note 02's `ecu_hardware_checker.py vin_dna` and
  `lab_pipeline_aggregator.py engine_state` are MISLABEL by the exact dtclab-perception logic —
  a reader exists, but reads different fields than the edge names.
- **Crucial COMLab note (mirrors the power_loss ORPHAN trap, inverted):** comlab note 07 frames
  `power_loss_analytics.py Stage D severity` and the aggregator carries a "Stage D stubbed"
  comment. A shallow audit would call this ORPHAN. It is **LIVE** — the analytics is injected
  into and called by the router (`fault_atlas_router.py:579,2117`); only the override/test path
  is stubbed. Verified by grepping the live call site, not the comment.

## Notes / out-of-scope observations (tail — not chased)
- Several `consumers` edges embed **wiki rule-IDs** (`RULE_GAS_ROUTE`, `RULE_HW_PRUNE`,
  `RULE_HORIZON_PRUNE`, `RULE_SCORING`, `CONCEPT_DIFFERENTIAL`, `RULE_TOPK`) that are **not code
  literals** (grep across `labs/comlab/comlab` = 0 for these). The contracted *behaviour* has a
  live reader in every case, so they classify LIVE, but the tokens read as code symbols when they
  are wiki anchors. Only `RULE_SYMPTOM_PRIOR` and `RULE_COLLISION_SET` are real code literals
  (`fault_atlas_router.py:1083,321`). The reconcile pass may want to strip wiki-IDs from edge
  labels so the map names symbols, not anchors. Not a trust defect — flagged for cosmetic clarity.
- Two edges (note 03 "VE polymorph", note 10 "RULE_SYMPTOM_PRIOR") attribute live behaviour to a
  plausible-but-imprecise file/field; classed LIVE (a real reader exists) with a relabel proposal,
  so the union can decide whether the wording rises to MISLABEL.
