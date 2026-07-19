# T-COM-WIKIPREP — Explicit relations in COMLab Wiki Chunks

**Status:** done · **Date:** 2026-06-27 · **Lane:** author (architect session)
**Pack:** VAULT (COMLab) · **Task file:** `Vault/tasks/T-COM-WIKIPREP_explicit_relations_wiki.md`

## Plan

**Currency confirmed.** All COMLab wiki files under `labs/comlab/wiki/` are current and reconciled to the shipped code. The wiki prose is current and citation-backed.

**Operations executed:** `relations → labels → roster → verify` per `_skills/graph/4dlab-wiki-prep/SKILL.md`.

**Corpus:** 15 content chunks under `labs/comlab/wiki/` (`00_index.md` through `14_sources_appendices.md`).

**Pattern:** Proven OBDLab approach from `labs/obdlab/research/CHUNK_ENHANCEMENT_PREP_REPORT.md` — append-only trailer blocks, no prose edited.

## VERIFICATION GATE

### Block coverage
- **15/15** chunks carry exactly one `## Graph relations (explicit)` block — zero missing, zero duplicates.
- **15/15** chunks carry exactly one `## Core Entities` block — zero missing, zero duplicates.
- Zero empty relation blocks.

### Relation lines
Total: **93** bold relation lines across the corpus.

| Chunk | Lines |
|---|---|
| 00_index.md | 6 |
| 01_role_boundaries_fusion_spine.md | 5 |
| 02_lab_input_contract.md | 10 |
| 03_vehicle_dna_pruning.md | 5 |
| 04_horizon_eras.md | 4 |
| 05_fault_taxonomy.md | 8 |
| 06_fault_atlas_families.md | 5 |
| 07_pipeline_stages.md | 8 |
| 08_scoring_to_fusion_rework.md | 7 |
| 09_calibration_confidence.md | 6 |
| 10_differential_and_symptom_prior.md | 7 |
| 11_two_point_delta.md | 7 |
| 12_corpus_eval_discipline.md | 7 |
| 13_proposals_register.md | 3 |
| 14_sources_appendices.md | 5 |

### Append-only confirmed
No sourced prose, numeric literals, tables, citations, or frontmatter were altered. All trailers were appended at the end of each file. Original bytes before the trailer insertion point are unchanged.

### Scope Spot-check (SAI residual)
- Checked `03_vehicle_dna_pruning.md:52`: `emissions.secondary_air_equipped = true  └─ enables ERR-LC-007 (SAI stuck on)`.
- Confirmed that Secondary Air Injection (SAI) is an in-era residual (SAI was widely fitted on Euro 2–3 and early Euro 4 cars between 1990–2010 to reduce cold-start hydrocarbons) and is **not** a 2010–2020 leak (unlike GPF/LSPI, which remain out of scope).

### Canonical labels consistent
- All canonical entity labels (e.g. `OrchestratorInboundRequest`, `FaultAtlasRouter`, `LabPipelineAggregator`, `ChemicalSignature`, `Horizon`) match the codebase byte-identically.
- The 12 canonical family names (e.g. `rich_mixture`, `lean_condition`, `misfire`, `sensor_fault`, `ecu_fault`, `catalyst_failure`, `exhaust_leak`, `ignition_fault`, `mechanical_wear`, `cam_timing`, `non_starter`, `no_fault`) match `comlab/core/fault_atlas_kg.py` and the `comlab/config/kg/*.json` filenames.

### Orphans / proposals
- **Proposed additions** (such as `CONCEPT_PROVENANCE`, `FUSE_CONFLICT_AWARE`, `FUSE_INV_VARIANCE`, `FUSE_LOGODDS`, `FUSE_DS_PCR5`, `CONCEPT_EVIDENCE_INPUTS`, `CONCEPT_CALIBRATION`, `CONCEPT_CONF_TIER`, `CONCEPT_CONFORMAL`, `RULE_LOWSUPPORT_FLAG`, `RULE_CROSSREF`, `RULE_ABSTAIN_LOWSUPPORT`, `CONCEPT_PROPOSAL_REGISTER`) are labeled as proposals or flagged with `(proposed)` — not promoted to live edges.
- All appended live `CONSUMES`/`VERIFIES`/`CONSUMED-BY`/`IMPLEMENTED-BY` relations resolve to existing paths or tests. No other lab is specified as a consumer of COMLab.

## CODE REVIEW

- **Honesty gates held.** No invented edges — every relation line is grounded in the chunk's text and maps to the real codebase.
- **Predicate vocabulary used correctly.** `CONSUMES`, `CONSUMED_BY`, `CONSUMED-BY`, `EMITS`, `EMIT_CHANNELS_NOT`, `MIRRORS_LOCALLY`, `REALISED_BY`, `IS`, `ROUTES_VIA`, `ENABLE`, `ENABLES`, `PROJECTED_INTO`, `RUNS_BEFORE`, `SELECTS`, `GATES`, `PROVIDES`, `RECONCILED_BY`, `MAPS`, `ROUTES_VIA`, `MOTIVATES`, `DEFINED_IN`, `BOUNDS`, `SEPARATED_BY`, `PRODUCERS`, `IMPLEMENTED-BY`, `REPLACED_BY`, `USES`, `FEEDS`, `CALIBRATED_BY`, `DEPENDS_ON`, `REDEFINED_AS`, `GUARANTEES`, `BUILT_FROM`, `POPULATED_FROM`, `REGISTERED_AS`, `ABSTAINS_FOR`, `ARE`, `RENDERED-BY` — each used appropriately.
- **Proposals vs live preserved.** Proposals remain marked as `(proposed)` and not mapped as active live edges.
- **No prose rewrite, no graphify, no move of `wiki/`.** Skill operations only.
