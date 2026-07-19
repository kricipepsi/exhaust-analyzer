# T-GTA-UNION-COM — comlab graph-trust union (canonical drift list)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Step:** union of the three comlab audits · **Author:** architect · **Date:** 2026-06-29
**Inputs (3 independent passes, all `done`):**
`reports/comlab__codex.md` (commit 998aed6), `reports/comlab__agy.md` (18e8394), `reports/comlab__claude.md` (3d30db3).
**Rule (from the pack):** an edge flagged ORPHAN/MISLABEL by **>=1** agent goes to the
reconcile list, annotated with **agreement count**. The architect then reads the cited
code and issues a single code-grounded ruling per contested edge. Fixes are handed to
`T-GTA-RECONCILE-COM` (do not edit maps here).

## Count reconciliation across the three passes
| Pass | LIVE | MISLABEL | ORPHAN | PENDING | Total |
|---|---|---|---|---|---|
| Codex | 99 | 2 | 1 | 6 | 108 |
| Agy | 98 | 3 | 1 | 6 | 108 |
| Claude | 99 | 2 | 0 | 7 | 108 |

All three enumerate the same 108 edges and agree on every `implements` and `drift_guards`
edge (LIVE) and on all six/seven `wired (pending T-WIRE-1)` edges (PENDING — `T-WIRE-1`
spec confirmed at `apps/wired/wired_tasks/T-WIRE-1_compose_labs_comlab.md`). The PENDING
6-vs-7 delta is a counting artifact (the `COMLab_PRD` wired edge), not a classification
dispute. **Every disagreement is confined to five `consumers` edges**, listed below.

## Canonical drift list (the reconcile superset)
Map = `_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml`. Lines are map line numbers.
"Ruling" is the architect's code-verified classification; evidence greps are in the next
section. Disposition is **relabel only** — no Python, no graph rebuild.

| # | note . map line | edge (as framed) | Codex | Agy | Claude | agree | architect ruling | disposition |
|---|---|---|---|---|---|---|---|---|
| D1 | 02 . 114 | `ecu_hardware_checker.py vin_dna consumption` | MISLABEL | MISLABEL | MISLABEL | **3/3** | **MISLABEL** — `ecu_hardware_checker.py` has 0 `vin_dna` reads; it reads OBD rails. | relabel -> `ecu_hardware_checker.py OBD-rail evidence (intake_air_temp_c / coolant_temp_c / throttle_pos_pct / total_trim_correction_delta / per_bank_trim_delta)`. `vin_dna` lives in horizon_context_injector / projection (notes 03/04), not here. |
| D2 | 02 . 115 | `lab_pipeline_aggregator.py engine_state ingestion` | LIVE | MISLABEL | MISLABEL | **2/3** | **MISLABEL** (code upholds the 2) — aggregator has 0 `engine_state` reads; it only forwards `request.symptom_dna`. | relabel consumer file -> `symptom_router.py route_symptom engine_state suppression (symptom_router.py:60,68)`. |
| D3 | 03 . 129 | `ecu_hardware_checker.py RULE_HW_PRUNE (Stage B Pass 2)` | ORPHAN | ORPHAN | LIVE | **2/3** | **MISLABEL** (resolves the split) — the named *prune* does not exist (precondition branch is a stubbed `pass`), but the file **is** a live reader as **scoring evidence**. Reader exists -> not ORPHAN; reads something other than the named prune -> not LIVE-as-labeled. | relabel -> `ecu_hardware_checker.py ECU-hardware digital-lie evidence in scoring phase (fault_atlas_router.py:1312, ecu_fault family)`. Drop the `RULE_HW_PRUNE (Stage B Pass 2)` claim. |
| D4 | 03 . 131 | `lab_pipeline_aggregator.py DNA-confidence degradation` | MISLABEL | LIVE | LIVE | **1/3** | **MISLABEL** (code upholds Codex) — `vin_confidence` is read only at :350 as a `== NONE` **fatal abort** (ERR-ABORT-004); the degradation mode is driven by the **symptom directive**, not DNA confidence. | relabel -> `lab_pipeline_aggregator.py vin_confidence==NONE fatal gate (ERR-ABORT-004, :350)`; degradation (GAS_DOMINANT/FULL_FUSION) is symptom-directive driven (`_map_degradation` :192-196, :452). |
| D5 | 10 . 202 | `symptom_router.py RULE_SYMPTOM_PRIOR (capped)` | LIVE | MISLABEL | LIVE | **1/3** explicit (+2 file-mismatch flags) | **MISLABEL** — `symptom_router.py` has 0 prior/cap reads; the capped prior lives entirely in `fault_atlas_router.py`. All three passes agree the reader is in the router; only the MISLABEL vote differs. | relabel consumer file -> `fault_atlas_router.py RULE_SYMPTOM_PRIOR capped 0.65 (table load :600-602/:682-684; apply :1078-1090)`. |

**Net:** 5 consumer-edge relabels. **Zero true ORPHANs** (D3's ORPHAN votes collapse to
MISLABEL once the live scoring-phase reader is found). **Zero notes demoted** — every
affected note (02, 03, 10) retains >=1 LIVE consumer after relabeling, and `symptom_router.py`
remains framed in note 10 via `implements:`.

## Architect code verification (evidence for each ruling)
Verified 2026-06-29 against `labs/comlab/comlab`:

**D1 — `ecu_hardware_checker.py vin_dna`:** `grep -nE 'vin_dna|VehicleDNA' core/ecu_hardware_checker.py` -> 0.
`ECUHardwareChecker.check()` (`core/ecu_hardware_checker.py:31-69`) reads only OBD rails:
`intake_air_temp_c`, `coolant_temp_c`, `throttle_pos_pct`, `total_trim_correction_delta`,
`per_bank_trim_delta`. `vin_dna` is read at `core/horizon_context_injector.py:75-79` and
`projection.py:53`. -> MISLABEL (3/3 confirmed).

**D2 — `lab_pipeline_aggregator.py engine_state`:** `grep -nE 'engine_state' core/lab_pipeline_aggregator.py` -> 0.
The aggregator calls `route_symptom(request.symptom_dna)` at `:327`, `:451`, `:634`. The
actual `engine_state` reader is `core/symptom_router.py:60` (`env.get("engine_state", "")`),
used for suppression at `:68-83`. The named file reads neither the field nor anything in
its place -> MISLABEL (code upholds Agy/Claude over Codex's "passes-through-so-LIVE").

**D3 — `RULE_HW_PRUNE (Stage B Pass 2)`:** the precondition branch in `_prune_candidates`
is a no-op: `core/fault_atlas_router.py:902-907` — `if "vvt_equipped" in pre: # For now,
always pass / pass`. So no DNA-flag *prune* reader exists (Codex/Agy correct: not LIVE-as-
labeled). But `ECUHardwareChecker` is instantiated (`:623`) and called live (`:1312`) — as
**scoring evidence** ("conflict-aware evidence, never an additive bump or override", `:1309`),
applied to the `ecu_fault` family (`:1319+`), **not** as a prune (Claude correct: a reader
exists). Reader exists + reads something other than the named prune => **MISLABEL**, not
ORPHAN and not LIVE. This is the union's sharpest resolution.

**D4 — `DNA-confidence degradation`:** `core/lab_pipeline_aggregator.py:350` reads
`request.metadata.vin_confidence == VinConfidence.NONE` -> raises `AggregatorAbort`
("ERR-ABORT-004") — a fatal gate, not graceful degradation. `_map_degradation` (`:192-196`,
applied `:452`) sets `GAS_DOMINANT`/`FULL_FUSION` purely from `directive.suppress_gaslab`
(symptom-router output). No PARTIAL / DNA-confidence degradation path exists. -> MISLABEL
(code upholds Codex's deeper read; Agy/Claude stopped at "vin_confidence is read at :350").

**D5 — `RULE_SYMPTOM_PRIOR (capped)`:** `grep -nE 'RULE_SYMPTOM_PRIOR|prior|cap' core/symptom_router.py`
-> 0. The capped prior is entirely in `core/fault_atlas_router.py`: `_prior_table`,
`_prior_weight`, `_max_symptom_prior_weight = 0.65` (`:600-602`), loaded `:682-684`, applied
`:1078-1090`. The edge names the wrong file -> MISLABEL.

## Cosmetic / optional (0/3 trust defects — not on the reconcile critical path)
Raised by Claude; not drift, but the reconcile may fold them in cheaply while editing the same lines:
- **Wiki rule-ID tokens in edge labels** — `RULE_GAS_ROUTE`, `RULE_HORIZON_PRUNE`, `RULE_SCORING`,
  `CONCEPT_DIFFERENTIAL`, `RULE_TOPK` are wiki anchors, **not code literals** (grep across
  `labs/comlab/comlab` = 0). The contracted behaviour has a live reader in each case (LIVE),
  but the tokens read as code symbols. Optional: strip the anchors so the map names symbols.
  (`RULE_SYMPTOM_PRIOR` and `RULE_COLLISION_SET` **are** real literals — keep them.)
- **Note 03 . 130 `delta_engine.py VE polymorph selection`** — LIVE, but `delta_engine`
  gates on `air_metering_strategy`/`induction_type` (`analytics/delta_engine.py:279-289`),
  not `ve_pct`/`ve_validity` (those are router-gated). Optional tighten of wording.
- **Note 06 . 167 `12-family JSON loading`** — loader is count-agnostic and live; the kg dir
  now holds 13 family files. Optional cosmetic count update.

## Hand-off
Reconcile spec: **`T-GTA-RECONCILE-COM_reconcile_comlab_drift.md`** (map + mirrored live-note
frontmatter for wiki notes 02/03/10; relabel-only; STRICT). Gate: this is one of the maps
`T-WIRE-1` composes against — comlab does not read GREEN until D1-D5 are reconciled.
