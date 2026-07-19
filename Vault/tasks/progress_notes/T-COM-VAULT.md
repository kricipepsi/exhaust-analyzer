# T-COM-VAULT — progress note

**Task:** Author `vault-map.comlab.yaml`, dry-run, build, and install the COMLab vault tier.
**Lane:** architect/author + vault-tooling (no lab inner-loop/gate). **Run:** 2026-06-28.
**Closes:** the COMLab vault pack (last task in the chain). Blockers T-COM-GRAPH-AST + T-COM-PATHS-1 both `done`.

## Plan (confirmed)

COMLab is the **terminal fusion spine** — so unlike the emitter labs (whose maps frame notes
*with COMLab as consumer*), every COMLab note's consumer is **COMLab-internal** (`core/`,
`analytics/`, `schemas/`) or the **app layer** (`apps/4DLabWired/`). **No other diagnostic lab is
ever named as a COMLab consumer** (they are inputs). Consumer evidence taken from the WIKIPREP /
DOCPREP relation trailers and grep-confirmed before framing.

### Framed-note roster (12) + named consumer

**Design docs (node_type prd/hld/lld/dld → docs/ tier):**
- `COMLab_PRD.md` → HLD + wired composition.py
- `COMLab_HLD.md` → LLD + DLD + fault_atlas_router family-routing
- `COMLab_LLD.md` → 15 `implements` (all shipped modules) + 12 drift_guards + wired import
- `COMLab_DLD.md` → aggregator/observability deployment + wired import

**Wiki chunks with live, tested COMLab-internal consumers (8):**
- `01_role_boundaries_fusion_spine` → lab_pipeline_aggregator.process / fault_atlas_router
- `02_lab_input_contract` → fault_atlas_router / ecu_hardware_checker / aggregator (ingestion.py)
- `03_vehicle_dna_pruning` → ecu_hardware_checker RULE_HW_PRUNE / delta_engine / projection
- `04_horizon_eras` → horizon_context_injector RULE_HORIZON_PRUNE
- `05_fault_taxonomy` → fault_atlas_router RULE_GAS_ROUTE / global_fault_registry.json
- `06_fault_atlas_families` → fault_atlas_kg 12-family JSON / config/kg/*.json
- `07_pipeline_stages` → aggregator Stage A–D / power_loss_analytics
- `10_differential_and_symptom_prior` → aggregator RULE_TOPK / symptom_router / response.py

### Plain (NOT framed — signal/noise), with the exclusion reason

- `00_index` (index) · `08_scoring_to_fusion_rework` (FUSE_* all **(proposed)**) ·
  `09_calibration_confidence` (CONCEPT_CALIBRATION/CONF_TIER/CONFORMAL all **(proposed)**) ·
  `11_two_point_delta` (**default-off**, `enable_delta=False`, LIVE_GATED_ON GATE_CAPTURE —
  the task's "default-off flag-gated capability" exclusion) · `12_corpus_eval_discipline`
  (consumers are "COMLab validation", not a code path) · `13_proposals_register` (proposals) ·
  `14_sources_appendices` (sources/glossary) · `COMLab_BDD.md` · `CROSS_LAB_DEPENDENCIES.md`.
- Vocabulary mirrors (`docs/Vocabulary/DTC_VOCABULARY.md`, `OBD_VOCABULARY.md`) NOT re-copied —
  already homed in `Vault/_vocabulary/` (canonical at `labs/semantic/vocabul/`).

### Step 0 — `_vocabulary/` (SEMANTIC_CONTRACT.md added)

`SEMANTIC_CONTRACT.md` had no vault home and COMLab is its natural owner. A named existing
consumer **can** be grep-confirmed (definitional-mirror relationship, same as the other vocab
notes): `schemas/vocabulary.py` and `schemas/lab_dna_views.py` mirror its §4/§5.1/§6.4/§8/§10
field definitions; `core/horizon_context_injector.py` maps EuroEmissionCategory per §6.4. Added to
`vault-map.vocabulary.yaml` (canonical `labs/semantic/vocabul/SEMANTIC_CONTRACT.md`) and built via
`--vocab`. (The 8 code refs are docstring `Source:` cites, not runtime reads — but a definitional
mirror is exactly the consumer relationship DNA_VOCABULARY etc. already use, so it frames honestly.)

## VERIFICATION GATE — PASS

- **Eligibility (Phase 0):** code/tests/wiki/docs + `graph/v2_code/graph.json` +
  `graph/v2_tests/graph.json` all present; prose graphs owner-waived (set by T-COM-PATHS-1). Dry-run
  resolves without `research/chunks` / `v2_wiki` / `v2_docs` abort.
- **Dry-run clean:** 12 framed notes, every one with consumers≥2, no signal/noise breach.
- **Build applied:** `Vault/labs/comlab/{code,tests,wiki,docs}` + `_comlab.md` landing note written;
  `consumers/drift-guards/modules/tasks.base` confirmed in `_bases/` (shared, not re-authored).
- **Criterion 2 (Bases render):** `vault_query modules` shows `== comlab (13) ==` (landing + 4 docs
  + 8 wiki); `consumers --missing` → **no breach**; coverage gate → **0 notes implement code with no
  drift_guard**.
- **Criterion 3 (consumer completeness):** 12/12 framed notes carry a non-empty `consumers:` key;
  zero `consumers: []`; no proposal/flag-gated token framed as live; **no other lab named as a
  consumer** (grep for `gaslab|obdlab|dtclab|dnalab|vinlab|symptomlab:` in the map → none).
- **Criterion 4 (no re-extraction):** `md5sum -c` on `v1_baseline`, `v2_code`, `v2_tests` graph.json
  → **all OK, byte-unchanged**. (`git status` shows `v2_code`/`v2_tests` as `??` only because those
  dirs were never committed — built by T-COM-GRAPH-AST; the md5 check is authoritative. `v1_baseline`
  is git-tracked and clean.) No graphify run.
- **Criterion 5 (idempotent):** re-ran the build; `md5sum -c` on two framed notes → **OK** (identical);
  single frontmatter block (`node_type:` count = 1), no duplication.
- **Criterion 6 (System-Map + PROVENANCE):** COMLab row added to `Vault/System-Map.md` (+ SEMANTIC_
  CONTRACT in the `_vocabulary/` list); `_meta/PROVENANCE.md` `## comlab` section written with
  "framed notes: 12" and the "v2_wiki/v2_docs waived by owner direction" note.
- **Vault health gate:** signal/noise **91/91** (up from 77/77 baseline: +12 COMLab framed +1 vocab +
  prior), coverage 0 gaps, cycles none, `.base` 4/4. Only WARN = the pre-existing 9 cross-ledger
  blocked_by refs (DNAV/OIL/SEM/VIN packs — not introduced by this task).

## CODE REVIEW — PASS

- **Map authored against the prep output + code/test graphs.** Every framed note's `implements`,
  `consumers`, and `drift_guards` trace to the WIKIPREP/DOCPREP relation trailers and were
  grep-confirmed against real files (`apps/4DLabWired/wired/composition.py:33 from comlab.core.
  lab_pipeline_aggregator import LabPipelineAggregator`; every drift_guard test path exists).
- **Terminal-spine discipline held.** Consumers are COMLab-internal or app-layer only; the emitter
  labs / DNALab appear nowhere as consumers.
- **Proposal / flag-gate honesty.** The four notes whose only story is proposed (`08`, `09`) or
  default-off/Gate-gated (`11`) are left `plain:` with the reason documented inline — not framed with
  a fabricated live consumer. `12`/`13`/`14` (validation/proposals/sources) likewise plain.
- **No orphans / unresolved breaches:** `consumers --missing` empty; drift-coverage 0 gaps.
- **Scope respected:** no graphify, no re-extraction, no other lab's tier, registry excluded
  (separate pack), prose-graph waiver not lifted.

**Result:** both gates clean → ledger row T-COM-VAULT → `done`. **This closes the COMLab vault pack.**

### Files touched
- `_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml` (new — architect consumer map)
- `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` (+ SEMANTIC_CONTRACT.md entry)
- `Vault/labs/comlab/…` (generated tier), `Vault/_vocabulary/SEMANTIC_CONTRACT.md` (generated)
- `Vault/System-Map.md` (COMLab row + vocab link), `Vault/_meta/PROVENANCE.md` (build-written)
