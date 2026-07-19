# T-V3-D3 — progress note (DATA_GAP split)

**Task:** `T-V3-D3_data_gap_split.md` · **Status:** done · **Author:** Codex · **Date:** 2026-07-01
**Report:** `v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.md`
**JSON:** `v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.json`

## Plan

Build a read-only split for every `DATA_GAP` case from frozen on-disk artefacts only:
1. Parse `FL_LOCALIZATION_2026-06-30.md` for the 19 unique per-case `DATA_GAP` labels.
2. Join `FL_UPSTREAM_2026-06-30.json` for predicted family, OBD O2 mode, required gating state where present, and frozen failure evidence.
3. Join `cases_petrol_v7.csv` for exact source references and currently populated gas/OBD inputs.
4. Parse `apps/wired/v7_tasks/V7_PROGRESS.md` owner action queue by exact case ref so any true `CORPUS_FILL` row reuses the existing owner-fill entry instead of duplicating it.
5. Emit per case: missing input, verdict, source-library reference, source-confirmation status, action, missing physical quantity, and research-cluster mapping.

Result: 19 total = 0 `CORPUS_FILL` + 19 `ACQUISITION_GAP`. Acquisition clusters: Cluster 5 = 5, Cluster 6 = 3, Cluster 8 = 1, Cluster 9 = 10. The exact DATA_GAP case ids are not already present in the v7 owner action queue; source-library confirmation remains `owner-confirm` because the original source-library files are not in-tree.

## VERIFICATION GATE

```
Phase 1 Syntax/compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/data_gap_split.py`)
Phase 2 Lint           : PASS (`ruff check v3/data_gap_split.py` -> OK)
Phase 3 Types          : PASS (`/agent_workspace/.venv-wired/bin/python -m pyright v3/data_gap_split.py` -> 0 errors)
Phase 4 Tests          : PASS (`/agent_workspace/.venv-wired/bin/python v3/data_gap_split.py` -> 19 total; CORPUS_FILL=0; ACQUISITION_GAP=19; report+json written)
Phase 5 Contract       : PASS (`grep` equivalent via tool found `CORPUS_FILL`, `ACQUISITION_GAP`, and `19`; report reconciles 19 rows and names source refs, actions, missing physical quantities, and clusters)
Phase 6 Anti-orphan    : N-A (read-only analysis; no new field/enum/fault and no producer/consumer mapping)
Result: CLEAN
```

## CODE REVIEW

```
Scope         : PASS (new split script plus the two contracted report artefacts; no engine/lab/oracle/CSV/scorer edits)
Composition   : PASS (no `wired/` mapping change, no lab edits, no graphify, no Vault edits, no legacy imports)
Consumers     : PASS (N/A for mapped fields; output consumer is the owner-fill workflow and Phase-4 scoping)
Literals      : PASS (19 expected DATA_GAP count is from T-V3-D3/FL_LOCALIZATION; cluster labels mirror `RESEARCH_PROMPT_blocking_measurements.md`; no runtime diagnostic thresholds added)
Docstrings    : PASS (module, dataclasses, and public helpers documented)
Craft (WARN)  : depth: one read-only parse/split/render script; deletion: no unused options or scaffolding; seam: no routing or corpus logic added to wired/labs; interface: public command `python v3/data_gap_split.py` regenerates both artefacts
Result: CLEAN
```
