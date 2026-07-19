# Registry Vault Docs Manifest

This manifest defines the explicit list of documentation files to be ingested into the Obsidian vault for the rule registry, replacing wildcard globs. All included files have been audited and reconciled against the v2 ground truth: 16 rule families, 34 chemistry states, and 252 curated cases.

## INCLUDE

| File Path | Description | Reconciled Figures / Comments |
|---|---|---|
| `labs/comlab/registry/docs/SCHEMA_V2_SPEC.md` | Specification document describing the Pydantic v2 rule schema. | Reconciled ChemistryState count from 32 to 34. |
| `labs/comlab/registry/docs/CHEMISTRY_COVERAGE.md` | Inferred GASLab Chemistry State x Fault Family matrix. | Reconciled ChemistryState count from 32 to 34, zero-rule count from 21 (66%) to 23 (68%), and matrix rows count to 34. |
| `labs/comlab/registry/docs/CORPUS_AUDIT.md` | Curation log and breakdown of the curated cases database. | Already matches ground-truth counts (16 families, 252 curated cases). |
| `labs/comlab/registry/docs/REGISTRY_AUDIT.md` | Audit log of v1 rule inventory and rebuild recommendations. | Already matches ground-truth counts (252 curated cases). |
| `labs/comlab/registry/docs/case_library.html` | HTML index of all reference cases used to validate the rule registry. | Already matches ground-truth counts (16 families, 252 cases). |

## EXCLUDE

| File Path / Pattern | Description | Reason for Exclusion |
|---|---|---|
| `labs/comlab/registry/docs/REGISTRY_PROGRESS.md` | Workstream progress ledger. | Internal workstream tracking, not useful for vault users. |
| `labs/comlab/registry/docs/REGISTRY_START_HERE.md` | Session bootstrap instructions. | Internal development guide and session ignition instructions. |
| `labs/comlab/registry/docs/REGISTRY_START_HERE_AUDIT_RESPONSE.md` | Internal audit response scratchpad. | Temp development feedback log. |
| `labs/comlab/registry/docs/cvsgaps.md` | Gap analysis input file. | Temporary gap analysis scratchpad. |
| `labs/comlab/registry/docs/Vol5.md` | Historical literature source extract. | Raw source material, not a curated design document. |
| `labs/comlab/registry/docs/_registry_skills/` | Folder containing development skill markdown files. | Development skills, not part of the vault documentation. |
| `labs/comlab/registry/docs/registry_tasks/` | Folder containing developer task prompt files and logs. | Developer tasks and notes, excluded from end-user vault. |
