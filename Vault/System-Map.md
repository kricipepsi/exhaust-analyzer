---
tags: [vault, system-map]
source: "Vault/System-Map.md"
---

# 4DLab Vault System Map

This vault is a read-mostly mirror of finished labs. Edit canonical lab sources, then rebuild the vault.

## Labs

| Lab | Landing note | Mirrored tiers | Graph source |
|---|---|---|---|
| OBDLab | [[_obdlab]] | code, tests, wiki, docs | `labs/obdlab/graph/` (`v2_code`, `v2_tests`, `v2_wiki`, `v2_docs`) |
| GASLab | [[_gaslab]] | code, tests, wiki, docs | `labs/gaslab/graph/` (`v2_code`, `v2_tests`; prose graphs waived) |
| DTCLab | [[_dtclab]] | code, tests, wiki, docs | `labs/dtclab/graph/` (`v2_code`, `v2_tests`; prose graphs waived) |
| SymptomLab | [[_symptomlab]] | code, tests, wiki, docs | `labs/symptomlab/graph/` (`v2_code`, `v2_tests`, `v2_wiki`, `v2_docs`) |
| VINLab | [[_vinlab]] | code, tests, wiki, docs | `labs/vinlab/graph/` (`v2_code`, `v2_tests`; prose graphs waived) |
| DNALab | [[_dnalab]] | code, tests, wiki, docs | `labs/dnalab/graph/` (`v2_code`, `v2_tests`; prose graphs waived) |
| COMLab | [[_comlab]] | code, tests, wiki, docs | `labs/comlab/graph/` (`v2_code`, `v2_tests`; prose graphs waived) |
| Registry | [[_registry]] | code, tests, docs | `labs/comlab/registry/graph/` (`v2_code`, `v2_tests`, `v2_docs`) |
| UI (design corpus) | [[_ui]] | docs | none (doc-only design corpus) |

## Shared Areas

- `_vocabulary/`: [[OBD_VOCABULARY]], [[GAS_VOCABULARY]], [[DTC_VOCABULARY]], [[SYMPTOM_VOCABULARY]], [[VIN_VOCABULARY]], [[DNA_VOCABULARY]], [[SEMANTIC_CONTRACT]]
- `_bases/`: [[modules.base]], [[consumers.base]], [[drift-guards.base]]

- `_meta/PROVENANCE.md`: source paths, build dates, and graph requirements

## Vault Checks

- `consumers.base`: every framed note should have at least one named consumer.
- `drift-guards.base`: every implemented code target should have guarding tests.
- `modules.base`: grouped lab/module navigation for framed notes.
