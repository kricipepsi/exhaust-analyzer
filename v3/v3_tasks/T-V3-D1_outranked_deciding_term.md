### Goal ###
For every `OUTRANKED` case (107 in the frozen run), produce a per-case "why it lost" map so each
can be resolved deterministically. Output `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md` (+ `.json`):
per case — the expected family's best-scoring rule, its score and **1-based rank position** among
all scored rules; the winner's rule + family + score; the **score margin**; and the **specific
scoring term(s)** that produced the loss (which evidence weight / prior / modifier tipped it).
Then bucket each case into **FREE** (expected family already within top-3 → resolved by surfacing
the differential, no rank change), **TUNABLE** (just outside top-3, recoverable by one named,
neighbour-safe term change), or **HARD** (expected rule scored deep/low). Read-only.

### Success criteria ###
- `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md` lists all 107 OUTRANKED case_ids with the seven
  fields above and a FREE/TUNABLE/HARD label; counts per bucket reconcile to 107.
- `v3/outranked_map.py` regenerates the report from on-disk artefacts (no engine re-run, no
  network): `python v3/outranked_map.py` exits 0 and writes `.md` + `.json`.
- Every "deciding term" claim cites the trace field/span it rests on; anything not directly
  observable is marked `inferred`.
- The FREE count equals the number of OUTRANKED cases whose expected family is in the engine's
  top-3 — i.e. it must agree with T-V3-0's measured top-3 result for the OUTRANKED bucket (cross-check).
- `py_compile` + `ruff` clean on `v3/outranked_map.py`.

### Context ###
Phase-0 diagnostic for `v3/V3_PLAN.md` section 4. The localization already labels these 107 cases
`OUTRANKED` (the expected rule scored but `router.winner_id` belongs to another family) but does
**not** give the per-case rank depth or the deciding term — without that you cannot tell a case
that is rank-2 by 0.01 (free once the differential is surfaced) from one that is rank-6 (needs
real rank work). This task supplies that. Inputs (READ-NARROW, all on disk): the trace run
`apps/wired/v7/runs/20260630_190651/` (the `phase.rank` `rule_scored` events carry per-rule
scores; the localization's per-case table shows the exact shape, e.g. an OUTRANKED row reads
`rule_scored EL-001=0.90 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False`);
the per-case mode labels in `apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md`; the
rule-id→family map used by `apps/wired/fl_tasks/score_v3_yardstick.py` (reuse it, do not re-derive).
If a case's full scored-rule list is not in the spans, fall back to the surfaced winner + runner-ups
and say so per case.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Read-only analysis. Output consumed by the deferred rank-recovery
task (T-V3-4) — the TUNABLE list with named terms is its exact work list — and by the architect
finalizing T-V3-3.

### Deliverables ###
1. `v3/outranked_map.py` — CREATE. Builds the per-case map from trace + localization + CSV.
2. `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md` — CREATE.
3. `v3/reports/V3_OUTRANKED_MAP_2026-06-30.json` — CREATE.

### Files to touch ###
- `v3/outranked_map.py` (CREATE)
- `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md` (CREATE)
- `v3/reports/V3_OUTRANKED_MAP_2026-06-30.json` (CREATE)

### Out of scope ###
No engine/oracle/scorer/CSV edits; no rank re-tuning (that is the gated T-V3-4 — this task only
*names the term* to change). No suite re-run; reuse the frozen trace. GRAPH GUARDRAIL: do not run
`graphify` or rebuild any graph — query only. No `Vault/` edits. Surgical: every line in
`outranked_map.py` traces to a deliverable.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/outranked_map.py
ruff check v3/outranked_map.py
/agent_workspace/.venv-wired/bin/python v3/outranked_map.py
test -f v3/reports/V3_OUTRANKED_MAP_2026-06-30.md
# FREE+TUNABLE+HARD must reconcile to 107:
grep -iE 'FREE|TUNABLE|HARD|107' v3/reports/V3_OUTRANKED_MAP_2026-06-30.md
```
All steps must pass; the bucket counts must sum to 107 and the FREE count must match T-V3-0's
OUTRANKED-in-top-3 figure.

### Progress hook ###
PROGRESS.md `T-V3-D1`: Status=done, Files changed=3, Verification="107 OUTRANKED mapped to rank-depth + deciding term; FREE/TUNABLE/HARD reconcile to 107; FREE matches T-V3-0"
