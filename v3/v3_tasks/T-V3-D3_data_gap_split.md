### Goal ###
For every `DATA_GAP` case (19 in the frozen run), decide the **resolvability fork**: `CORPUS_FILL`
(the discriminating input existed in the source case library but the corpus row was not populated
with it — a cheap fill, no new acquisition) vs `ACQUISITION_GAP` (the input is genuinely not
obtainable from the standard capture — needs a Phase-4 measurement). Output
`v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.md` (+ `.json`): per case — the missing input, the
verdict, the source-library reference, and the action (owner-fill row, or the research cluster it
maps to). Read-only.

### Success criteria ###
- All 19 DATA_GAP case_ids labelled `CORPUS_FILL` or `ACQUISITION_GAP` with evidence.
- For `CORPUS_FILL` cases, the report names the exact missing column/field and cross-references the
  existing owner-fill queue so duplicates are not re-filed.
- For `ACQUISITION_GAP` cases, the report names the missing physical quantity and the research
  cluster it maps to.
- `v3/data_gap_split.py` regenerates the report from on-disk artefacts; exits 0; `.md` + `.json`.
- `py_compile` + `ruff` clean.

### Context ###
Phase-4 scoping diagnostic for `v3/V3_PLAN.md`. The localization labels these 19 `DATA_GAP` (no
expected-family rule scored and the prune reason is missing input evidence — e.g.
`reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]`).
Some of these are *true* signal gaps; others are merely corpus rows that were never populated with
an input the real source library actually had. The existing **owner-fill / incomplete-case queue**
(in the v7 progress ledger — e.g. rows missing `gas.nox`, and source-level incompletes like
`RESEARCH-REAL-006`, `V2-ECU-GROUND-OFFSET`) is the cross-reference for `CORPUS_FILL`. Inputs
(READ-NARROW): the DATA_GAP case list from
`apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md`; the per-case upstream evidence in
`apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json` (`records[*]`); the corpus
`apps/wired/v7/data/cases_petrol_v7.csv`; and the owner-fill queue. Where a case's source library
entry cannot be confirmed from in-tree artefacts, mark the source-confirmation step `owner-confirm`
rather than guessing.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Read-only analysis. Output consumed by the owner-fill workflow
(CORPUS_FILL rows) and Phase-4 scoping (ACQUISITION_GAP rows).

### Deliverables ###
1. `v3/data_gap_split.py` — CREATE.
2. `v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.md` — CREATE.
3. `v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.json` — CREATE.

### Files to touch ###
- `v3/data_gap_split.py` (CREATE)
- `v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.md` (CREATE)
- `v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.json` (CREATE)

### Out of scope ###
No corpus edits — this task *triages* the gap; the actual owner-fill is a separate, owner-run
action. No engine/oracle edits. GRAPH GUARDRAIL: no `graphify`/graph rebuild. No `Vault/` edits.
Surgical: every line traces to a deliverable.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/data_gap_split.py
ruff check v3/data_gap_split.py
/agent_workspace/.venv-wired/bin/python v3/data_gap_split.py
grep -iE 'CORPUS_FILL|ACQUISITION_GAP|19' v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.md
```
All steps must pass; the two labels must reconcile to 19.

### Progress hook ###
PROGRESS.md `T-V3-D3`: Status=done, Files changed=3, Verification="19 DATA_GAP split CORPUS_FILL vs ACQUISITION_GAP; fill rows cross-checked against owner-fill queue; acquisition rows mapped to clusters"
