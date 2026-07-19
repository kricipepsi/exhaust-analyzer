# T-COM-DOCPREP — Progress Notes

**Status:** done · **Date:** 2026-06-27 · **Lane:** author (architect session)
**Pack:** VAULT (COMLab) · **Task file:** `Vault/tasks/T-COM-DOCPREP_doc_prep_design_docs.md`

## Plan

`4dlab-doc-prep explode → tables → anchor → relations → verify` on the five COMLab design docs in `labs/comlab/docs/` and the 11 individual ADR files. Explicit file list: COMLab_HLD.md, COMLab_DLD.md, COMLab_LLD.md, COMLab_BDD.md, COMLab_PRD.md and `adr/ADR-0001_...md` through `adr/ADR-0011_...md`. Exclude: `Vocabulary/`, `CROSS_LAB_DEPENDENCIES.md`, `ARCHIVE/`, and `adr/README.md`. Output under `labs/comlab/graph/v2_docs/ingest_ready/`. No graphify, no source doc edits, no schema fields.

## VERIFICATION GATE

### Explode
- **80 chunks** across 16 doc subtrees (HLD: 14, DLD: 15, LLD: 13, BDD: 14, PRD: 13, and 11 ADR files: 1 chunk each).
- Every `##` section of each source doc produced exactly one chunk; zero lost, zero double-explode.
- 16 doc folders confirmed under `labs/comlab/graph/v2_docs/ingest_ready/`; Vocabulary, CROSS_LAB_DEPENDENCIES, ARCHIVE, adr/README.md excluded.

### Tables (logic tables → entity blocks)
Tables converted in 14 chunks:
- **HLD §5** (`5._The_Fault-Atlas_Knowledge_Graph_(KG)_—_the_new_piece.md`): 1 table
- **HLD §11** (`11._What_was_kept,_what_was_rejected_from_COMLabDesign.md.md`): 1 table
- **DLD §2** (`2._Resource_manifest.md`): 1 table
- **DLD §3** (`3._Latency_budget_—_per-stage_allocation.md`): 1 table
- **DLD §5** (`5._Logging_strategy.md`): 1 table
- **DLD §6** (`6._Observability_surfaces.md`): 1 table
- **DLD §9** (`9._Cross-version_compatibility.md`): 1 table
- **DLD §11** (`11._Failure_modes_and_recovery.md`): 1 table
- **LLD §10** (`10._Error-code_taxonomy.md`): 1 table
- **PRD §2** (`2._Users.md`): 1 table
- **PRD §4** (`4._Defensive_input_gates_—_who_runs_which_check.md`): 2 tables
- **PRD §6** (`6._Error_&_abort_UX.md`): 1 table
- **PRD §9** (`9._Out_of_scope_for_v1_(candidates_for_v2+).md`): 1 table
- Narrative/Glossary tables left as-is per skill rule.

### Anchors
- **80/80** chunks carry a `> **Context:**` anchor header naming module (COMLab) + parent document (or ADR ID).
- Zero missing anchors.

### Relations
- **107** bold relation lines across all 80 chunks, zero empty blocks.
- Every chunk carries exactly one `## Graph relations (explicit)` block.
- Total relation lines: 107.

| Doc | Relation lines |
|---|---:|
| COMLab_HLD.md | 24 |
| COMLab_DLD.md | 19 |
| COMLab_LLD.md | 27 |
| COMLab_BDD.md | 15 |
| COMLab_PRD.md | 14 |
| 11 ADR files | 22 (2 lines per ADR) |
| **Total** | **107** |

### Consumer checks (CONSUMES/VERIFIES grep-backed)
- `OrchestratorInboundRequest` — confirmed in `comlab/schemas/ingestion.py`
- `OrchestratorFinalUIOutput` — confirmed in `comlab/schemas/response.py`
- `LabPipelineAggregator` — confirmed in `comlab/core/lab_pipeline_aggregator.py`
- `FaultAtlasRouter` — confirmed in `comlab/core/fault_atlas_router.py`
- `FaultAtlasKG` — confirmed in `comlab/core/fault_atlas_kg.py`
- `ECUHardwareChecker` — confirmed in `comlab/core/ecu_hardware_checker.py`
- `DeltaEngine` — confirmed in `comlab/analytics/delta_engine.py`
- `PerceptionContradictionResult` — confirmed in `comlab/core/perception_contradiction.py`
- All BDD VERIFIES lines name real test modules: `test_vocabulary_sae_iso_conformance.py`, `test_fatal_gate_wiring.py`, `test_symptom_router.py`, `test_perception_contradiction.py`, `test_fault_atlas_router.py`, `test_kg_registry_consistency.py`, `test_vocabulary.py`, `test_delta_engine.py`, `test_ecu_hardware_checker.py`, `test_lab_pipeline_aggregator.py`.
- All CONSUMES targets reference real code paths: `apps/4DLabWired/wired/composition.py` (which imports `LabPipelineAggregator`), `comlab/core/lab_pipeline_aggregator.py`, `comlab/core/fault_atlas_router.py`, `comlab/core/ecu_hardware_checker.py`.

### Proposal discipline
- Proposed features (`CONCEPT_PROPOSAL_REGISTER`, `CONCEPT_PROVENANCE`, `FUSE_CONFLICT_AWARE`, `FUSE_INV_VARIANCE`, `FUSE_LOGODDS`, `FUSE_DS_PCR5`, `CONCEPT_EVIDENCE_INPUTS`, `CONCEPT_CALIBRATION`, `CONCEPT_CONF_TIER`, `CONCEPT_CONFORMAL`, `RULE_LOWSUPPORT_FLAG`, `RULE_CROSSREF`, `RULE_ABSTAIN_LOWSUPPORT`) are labelled proposed or proposals.
- Zero proposals framed as live consumers; zero live consumers downgraded to proposals; zero unflagged orphans.

### Source docs + frozen graphs untouched
- Zero edits to `labs/comlab/docs/*.md`.
- Output isolated to `graph/v2_docs/ingest_ready/`.
- No graphify, no graph.json written, no schema field added.

### Exclusions honoured
- `Vocabulary/` directory (with `SEMANTIC_CONTRACT.md`, `OBD_VOCABULARY.md`, `DTC_VOCABULARY.md`) excluded from doc-prep.
- `CROSS_LAB_DEPENDENCIES.md` and `adr/README.md` excluded.
- `ARCHIVE/` folder excluded.
- Explicit list of docs used, no glob.

## CODE REVIEW

- **Honesty gates held.** Every CONSUMES/VERIFIES line references a real, existing code path or test, grep-confirmed. No fabricated consumers. Proposals labelled as proposals.
- **Table conversion consistent.** All logic-bearing tables (fields, model configs, user tables, logging strategies) converted to entity blocks following the skill's `### Field:` / `### Component:` pattern. Narrative tables left as markdown grids.
- **Anchors consistent.** Every chunk's `> **Context:**` header names COMLab module + parent document (or context value).
- **Relations canonical.** Entities use canonical labels matching the shipped code. Predicate vocabulary follows the skill's table.
- **No graph side effects.** No graph build, graph update, or graphify run. Output isolated to `graph/v2_docs/ingest_ready/`.
