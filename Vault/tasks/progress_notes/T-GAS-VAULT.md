# T-GAS-VAULT — progress note

**Status:** `done` · **Pack:** VAULT (GASLab) · authored 2026-06-10 (architect); completed 2026-06-11
Task spec: `Vault/tasks/T-GAS-VAULT_*.md` · Pack ledger: `Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`

## Plan
Scope confirmed 2026-06-11 after owner waiver: `T-GAS-VAULT` is no longer blocked by
`T-GAS-GRAPH-LLM`. GASLab vault eligibility requires `labs/gaslab/gaslab/`, `tests/`, `wiki/`, `docs/`,
plus `graph/v2_code/graph.json` and `graph/v2_tests/graph.json`; prose Pass-3 graphs are intentionally
skipped because Phase-2 wiki/doc prep is accepted as sufficient. No graphify command runs in this task.

Author `vault-map.gaslab.yaml` with a conservative framed roster. Each framed note has a named
existing consumer; notes that are index/provenance/proposal/change-log only stay plain.

Framed design docs:

| Note | Primary named consumer |
|---|---|
| `PRD_GASLab.md` | `labs/comlab/comlab/core/lab_pipeline_aggregator.py` GasLabPayload boundary |
| `HLD_GASLab.md` | `labs/comlab/comlab/core/fault_atlas_router.py` chemical_state routing |
| `LLD_GASLab.md` | COMLab analytics/aggregation/perception readers plus `DLD_GASLab.md` |
| `DLD_GASLab.md` | `fault_atlas_router.py`, `power_loss_analytics.py`, `lab_pipeline_aggregator.py`, `perception_contradiction.py`, `schemas/vocabulary.py` |

Framed wiki chunks:

| Note | Primary named consumer |
|---|---|
| `01_role_boundaries_dna_ingestion.md` | COMLab `lab_pipeline_aggregator.py`, `schemas/vocabulary.py`, `fault_atlas_router.py` |
| `02_combustion_foundations.md` | COMLab `power_loss_analytics.py`, `lab_pipeline_aggregator.py`, `perception_contradiction.py` |
| `03_five_gases_reference.md` | COMLab `power_loss_analytics.py` for `gas_co`/`gas_hc`/`gas_o2` |
| `04_inter_gas_grammar_validity_gates.md` | COMLab `lab_pipeline_aggregator.py` + `schemas/vocabulary.py` for `sample_validity` |
| `05_fault_atlas_part_a.md` | COMLab `fault_atlas_router.py` for `chemical_state` |
| `06a_fault_atlas_oil_mechanical.md` | COMLab `fault_atlas_router.py`; `power_loss_analytics.py` |
| `06b_fault_atlas_valvetrain_egr_combustion.md` | COMLab `fault_atlas_router.py`; `power_loss_analytics.py` |
| `07_catalyst_postcat_logic.md` | COMLab `fault_atlas_router.py`; `power_loss_analytics.py` |
| `08_diagnostic_tactics.md` | `gaslab/rule_engine.py` dual-reading/block-test path; COMLab fault/perception readers |
| `09_era_specific_patterns.md` | `gaslab/rule_engine.py` and `gaslab/resolution.py` Euro-threshold paths |
| `10_limited_scope_confidence.md` | `gaslab/ranking.py` top-3 ceiling and rule-engine DNA-scoped suppression |

Plain copies: `ADR_GASLab.md`, `BDD_GASLab.md`, `GAS_VOCABULARY.md`, `00_index.md`,
`11_sources_appendices.md`, and `CHANGE_v2.1_timing_taxonomy.md`. `GAS_VOCABULARY.md` is also added
to the shared `_vocabulary/` map with consumers in `gaslab/contracts.py`, `gaslab/audits.py`, and
`labs/comlab/comlab/schemas/vocabulary.py`.

## VERIFICATION GATE
- Eligibility: `labs/gaslab/gaslab/`, `tests/`, `wiki/`, `docs/`,
  `graph/v2_code/graph.json`, and `graph/v2_tests/graph.json` all present. Prose graph tiers remain
  owner-waived.
- Dry-runs:
  - `python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --vocab --repo . --dry-run`
    planned `OBD_VOCABULARY.md` + `GAS_VOCABULARY.md`.
  - `python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab gaslab --repo . --dry-run`
    planned code/tests/wiki/docs copy, 15 framed notes, 3 base installs, and GAS provenance upsert.
- Build:
  - `python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --vocab --repo .`
  - `python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab gaslab --repo .`
- Outputs present: `Vault/labs/gaslab/{code,tests,wiki,docs,_gaslab.md}`,
  `Vault/_vocabulary/GAS_VOCABULARY.md`, `Vault/_bases/{modules,consumers,drift-guards}.base`,
  `Vault/System-Map.md`, and `Vault/_meta/PROVENANCE.md`.
- Signal/noise audit script over GAS vault notes + `GAS_VOCABULARY.md`: `framed_notes=17`,
  `empty_consumers=0`, `missing_drift_guards=0`.
- Basic link check for `Vault/System-Map.md` and `Vault/labs/gaslab/_gaslab.md`: `wikilink_missing=0`.
- Graph untouched: `git status --porcelain -- labs/gaslab/graph/v2_code labs/gaslab/graph/v2_tests`
  returned empty.
- Idempotence: content hash across `Vault/labs/gaslab`, `Vault/_vocabulary/GAS_VOCABULARY.md`,
  `Vault/_meta/PROVENANCE.md`, and `Vault/System-Map.md` was unchanged after rerunning vocab + GAS build
  (`422610dbeeccfee27ff12aaae41d0b21eb1f7466240c657bd9f22ea92e7c2051` before and after).
- Tooling tests:
  - `python -m unittest _skills.graph.4dlab-vault.tests.test_build_lab_vault` -> 3 tests OK.
  - `python -m py_compile _skills/graph/4dlab-vault/scripts/build_lab_vault.py` -> OK.
- Obsidian desktop was not opened from this session; Bases were verified by installed files plus
  frontmatter/link checks rather than UI rendering.

## CODE REVIEW
- Map authored at `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml` with 15 framed GAS notes.
  Every framed note has named consumers; `gas_co2` and `gas_nox` were not used as sole consumer
  evidence.
- `GAS_VOCABULARY.md` added to `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` with
  consumers in `gaslab/contracts.py`, `gaslab/audits.py`, and COMLab `schemas/vocabulary.py`.
- `build_lab_vault.py` provenance behavior was fixed under test: lab builds now upsert only their own
  `## <lab>` section, preserving existing OBD and `_vocabulary/` provenance.
- `lab-landing.md.tmpl` now names a consumer for `lab-index` notes and uses shared vocabulary +
  `labs/<lab>/graph/` wording, so GAS landing rows do not show as missing-consumer rows.
- No graphify command was run; no `labs/gaslab/graph/v2_code` or `v2_tests` content changed.
- Known limitation: the builder copies `docs/GAS_VOCABULARY.md` into `Vault/labs/gaslab/docs/` as an
  unframed plain source copy while the framed canonical copy lives in `Vault/_vocabulary/`. This matches
  current builder behavior; no extra script exclusion was introduced in this task.

> Flip the ledger row to `done` only when BOTH blocks above are clean (and any contracted consumer is
> grep-confirmed read in a live path).
