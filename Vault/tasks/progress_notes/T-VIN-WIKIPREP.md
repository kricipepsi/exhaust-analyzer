# T-VIN-WIKIPREP - Explicit relations in VINLab Wiki Chunks

**Status:** done - **Date:** 2026-06-13 - **Lane:** author (architect session)
**Pack:** VAULT (VINLab) - **Task file:** `Vault/tasks/T-VIN-WIKIPREP_explicit_relations_wiki.md`

## Plan

**Scope confirmed.** VINLab wiki prep covers only `labs/vinlab/wiki/00_index.md`, `10_decode_scope_rules.md`, `11_engine_resolution.md`, and `12_brand_cylinder_rules.md`. The task is append-only prose prep: no code edits, no file moves, no `graphify`, and no edits to the frozen VIN graph directories.

**Operations executed:** `relations -> labels -> roster -> verify` per `_skills/graph/4dlab-wiki-prep/SKILL.md`.

**Named consumers grep-confirmed:** `vinlab.decoder._is_non_petrol`, `vinlab.decoder.RobustVINDecoder.decode_vin_payload`, `vinlab.overlay.horizon.euro_to_horizon`, `vinlab.models.VinDNA.rated_rpm`, `comlab.projection.project`, `comlab.schemas.lab_dna_views.ObdLabDnaView.rated_rpm`, `obdlab.core.pid_ingestion_validator.PIDIngestionValidator._check_dna_rpm`, and `vinlab.overlay.cylinder_heuristic.infer_cylinder`.

**Proposal handling:** `fuel_type` / E5/E10 remains proposal-only/context-only and was not emitted as a live `CONSUMES` edge.

## VERIFICATION GATE

### Block coverage
- **4/4** chunks carry exactly one `## Graph relations (explicit)` block - zero missing, zero duplicates.
- **4/4** chunks carry exactly one `## Core Entities` block - zero missing, zero duplicates.
- Zero empty relation blocks.

### Relation lines
Total: **58** bold relation lines across the corpus.

| Chunk | Lines |
|---|---:|
| `00_index.md` | 9 |
| `10_decode_scope_rules.md` | 13 |
| `11_engine_resolution.md` | 18 |
| `12_brand_cylinder_rules.md` | 18 |

### Append-only confirmed
No sourced prose, numeric literals, tables, citations, or frontmatter were rewritten. Trailer sections were appended at the end of each chunk; body text before `## Graph relations (explicit)` remains the original sourced content.

### Consumer checks
- `CONSUMES` / `VERIFIES` targets are backed by live code or tests in `labs/vinlab/vinlab/`, `labs/vinlab/tests/`, `labs/comlab/comlab/`, or `labs/obdlab/`.
- `vinlab.decoder._is_non_petrol` and H2 year bounds are verified by `labs/vinlab/tests/unit/test_decoder.py`.
- `vinlab.overlay.horizon.euro_to_horizon` is verified by `labs/vinlab/tests/unit/test_horizon.py`.
- `VinDNA.rated_rpm` is verified by `labs/vinlab/tests/unit/test_models.py` and consumed through `comlab.projection.project` into `ObdLabDnaView.rated_rpm`, then by OBDLab's DNA-RPM validator.
- `vinlab.overlay.cylinder_heuristic.infer_cylinder` and the brand fallback chain are verified by `labs/vinlab/tests/unit/test_cylinder_heuristic.py`.
- Zero unflagged orphans found in the appended `CONSUMES` / `VERIFIES` lines.

## CODE REVIEW

- **Honesty gates held.** Relations stay within concepts already present in the VIN wiki chunks and the task's named consumer list.
- **Canonical labels assigned.** Stable labels are used for `VINWIKI-00-INDEX`, `VINWIKI-10-DECODE_SCOPE_RULES`, `VINWIKI-11-IDENTITY_RESOLUTION`, `VINWIKI-12-BRAND_CYLINDER_RULES`, `VinDNA.rated_rpm`, `ObdLabDnaView.rated_rpm`, `_NON_PETROL_KEYWORDS`, `_BRAND_DISPATCH`, and the per-brand cylinder rules.
- **Proposal vs live preserved.** `fuel_type` / `altitude_band` is labelled proposal-only and not framed as a live consumer.
- **No graph side effects.** No graph build, graph update, schema field, or source-code change was made.
