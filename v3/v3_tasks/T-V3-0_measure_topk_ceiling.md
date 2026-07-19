### Goal ###
Produce `v3/reports/V3_TOPK_CEILING_2026-06-30.md` (+ a `.json` sidecar): for every one of
the 294 accuracy cases in the **already-frozen** traced run, determine whether the **expected
fault family** appears within the engine's **top-3 scored rules** (by score, descending), and
report the rate overall, per-family, and per-FL-mode. This is a **read-only measurement** — no
engine, oracle, scorer, or CSV edits. Done when the report prints a measured
`correct-in-top-3` number that replaces the ~85% estimate in `V3_PLAN.md` section 1, plus the
explicit list of OUTRANKED case_ids whose expected family is **outside** top-3 (the only ones
needing later rank work), and a first-pass abstain floor/margin recommendation.

### Success criteria ###
- `v3/reports/V3_TOPK_CEILING_2026-06-30.md` exists and contains: an overall
  `correct_in_top1 / top2 / top3` table; a per-family top-3 table (12 families); a per-FL-mode
  breakdown joined from `FL_LOCALIZATION_2026-06-30.md`; and the OUTRANKED-outside-top3 id list.
- A reproducible script `v3/measure_topk.py` regenerates the report from on-disk artefacts with
  no network and no engine run: `python v3/measure_topk.py` exits 0 and writes the `.md` + `.json`.
- Every number is sourced from a named on-disk field/span (verified, not inferred); anything not
  directly observable is marked `inferred`.
- `py_compile` + `ruff` clean on `v3/measure_topk.py`.

### Context ###
This is Phase 0 of `v3/V3_PLAN.md` (section 4) — the no-regret first task. The owner's goal is
top-3 differential accuracy; the plan estimates ~85% reachable from reframe alone, but that
rests on the assumption that the 107 `OUTRANKED` cases (`FL_LOCALIZATION_2026-06-30.md`
per-mode totals, line ~47) have their correct family in the **top 3**, not merely "scored
somewhere". This task replaces the estimate with a measurement before any code is built.

Inputs, all already on disk (READ-NARROW — do not whole-read):
- Trace run with per-rule scores: `apps/wired/v7/runs/20260630_190651/` (the `--trace` pass,
  T-V7-6; verdicts byte-identical to the untraced run). The per-rule scores live in the
  `phase.rank` spans / `rule_scored` events — the same source `FL_LOCALIZATION` cites in its
  per-case table (e.g. line ~105 `rule_scored EL-001=0.9000... but winner_id=LC-001 score=1`).
- Untraced run verdicts: `apps/wired/v7/runs/20260630_163900/results.json`
  (hash `d9069f8d...` per `FL_YARDSTICK_2026-06-30.md`).
- Oracle expected families: `apps/wired/v7/data/cases_petrol_v7.csv` column
  `expected_fault_family` (CSV hash `a94a7731...`).
- Per-case mode + stage: `apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md`
  (per-case localization table, lines ~129-427) and `FL_UPSTREAM_2026-06-30.json`.
- Rule-id -> family mapping: derive from the live registry the same way the scorer does — see
  `apps/wired/v7/run_suite.py::score_case` (line ~147 reads `verdict["fault_family"]`) and the
  router's KG resolve (`fault_atlas_router.py` `_kg.resolve(row.fault_id).fault_family`). Reuse,
  do not re-derive a parallel map.

If the `phase.rank` spans do not expose the full scored-rule list with scores (only winner +
runner-ups), fall back to `runner_ups` (`fault_atlas_router.py:1654`, `scored[1:4]`) joined
with the winner — that is the top-4 the engine actually surfaces, which is the operative set for
the differential anyway. State which source you used per case.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Read-only measurement; output is two report files consumed by
T-V3-1 (scorer thresholds) and the architect (finalizing T-V3-3 scope).

### Deliverables ###
1. `v3/measure_topk.py` — CREATE. Loads the run JSON + trace + CSV + FL localization, computes
   top-1/2/3 family hit per case, writes the `.md` + `.json`.
2. `v3/reports/V3_TOPK_CEILING_2026-06-30.md` — CREATE. The measured ceiling report.
3. `v3/reports/V3_TOPK_CEILING_2026-06-30.json` — CREATE. Machine-readable per-case rows.

### Files to touch ###
- `v3/measure_topk.py` (CREATE)
- `v3/reports/V3_TOPK_CEILING_2026-06-30.md` (CREATE)
- `v3/reports/V3_TOPK_CEILING_2026-06-30.json` (CREATE)

### Out of scope ###
No engine/oracle/scorer/CSV edits — this task measures only. Do not re-run the suite or mint a
new run artefact (reuse the frozen runs). Do not implement the new scorer (that is T-V3-1) or
the abstain logic in the engine (T-V3-3) — only *recommend* floor/margin values from the
observed score distribution. Surgical-change rule: every line in `measure_topk.py` traces to a
deliverable. GRAPH GUARDRAIL: do not run `graphify` or rebuild any graph. Do not edit `Vault/`.

### Verification ###
```bash
cd /agent_workspace
# Inner loop
/agent_workspace/.venv-wired/bin/python -m py_compile v3/measure_topk.py
ruff check v3/measure_topk.py
# Functional: regenerate the report deterministically from on-disk artefacts
/agent_workspace/.venv-wired/bin/python v3/measure_topk.py
test -f v3/reports/V3_TOPK_CEILING_2026-06-30.md
test -f v3/reports/V3_TOPK_CEILING_2026-06-30.json
# Sanity: denominator is the 294 accuracy cases; top1 rate reproduces the frozen 47.96% family-only
grep -iE 'top1|top-1|294' v3/reports/V3_TOPK_CEILING_2026-06-30.md
```
All steps must pass; `top1` family rate must reproduce the frozen family-only 141/294 = 47.96%
(a cross-check that the join is correct) before the top-3 number is trusted.

### Progress hook ###
PROGRESS.md `T-V3-0`: Status=done, Files changed=3, Verification="top-3 ceiling measured; top1 reproduces 47.96%; OUTRANKED-outside-top3 list emitted"
