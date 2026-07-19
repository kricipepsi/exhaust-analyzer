---
node_type: report
lab: apps/wired
module: fl_tasks/score_v3_yardstick.py
implements: T-V3-D6-SCORERWIN
consumers: [scoreboard top3_family metric, owner acceptance read]
tags: [v3, scorer, top3, family-aware]
source: v3/v3_tasks/T-V3-D6-SCORERWIN_family_aware_top3_window.md
---

# V3 SCORERWIN — `top3_family` counts 3 DISTINCT families

**Task:** [[T-V3-D6-SCORERWIN_family_aware_top3_window]] · **Date:** 2026-07-01 · **Mode:** STRICT
**Yardstick:** `V3_YARDSTICK_2026-07-01` (csv `5e41bafe…`, oracle `3088a7c3…`, `run_suite.py` untouched)
**Run scored:** `apps/wired/v7/runs/POST_T_V3_3D/results.json` · **Denominator:** 294

## What changed (a definition correction, not new engine accuracy)

The `top3_family` metric claims to count whether the expected family is in a **top-3** window
(winner + two runner-up families). Both scorer sites, however, took the first **two sibling
*entries*** (`differential_siblings[:2]`). When a same-family duplicate occupies an early slot,
the effective window shrinks to fewer than three *distinct* families and a genuine top-3 hit is
undercounted.

Both sites now compute **winner + the first two *distinct* non-winner sibling families** (walk
siblings in rank order; skip `unspecified`, skip the winner's own family, skip already-collected
families; stop at two). This mirrors the already-accepted family-aware dedupe precedent in
[[T-V3-3C_family_aware_abstain_margin]] (dedupe siblings to the first different family), applied
here to the top-3 acceptance window rather than the abstain margin.

**No prediction changed.** The engine's verdict, ranks, and scores are identical; only the scorer's
*read* of the differential is corrected. `single_verdict` (primary family+state) is unchanged.

## Measured delta (reproduced read-only)

| Metric | Before (`[:2]` entries) | After (distinct families) |
|---|---|---|
| `top3_family` | 193/294 = 65.65 % | **197/294 = 67.01 %** |
| `top3_on_covered` | 155/216 = 71.76 % | 158/216 = 73.15 % |
| `single_verdict` (family+state) | 126/294 = 42.86 % | 126/294 = 42.86 % (unchanged) |
| `coverage` | 0.73 (216/294) | 0.73 (216/294, unchanged — MARGIN=0.02) |
| Hash lock | ok | **ok** (no re-mint; only the non-locked scorer read-site changed) |

**Newly passing (4):** `era1_011`, `era3_008`, `era3_015`, `YAML-CSV95` — each was masked because a
same-family duplicate crowded the first two sibling entries, so the distinct runner-up family fell
outside the old two-entry window.

**Monotonic — no regression possible.** For every case the old set `{winner} ∪ {sib[:2]}` is a subset
of the distinct set `{winner} ∪ {first 2 distinct non-winner families}` (the distinct walk can only
reach *further* down the sibling list, never fewer families). Verified directly on all 294 accuracy
rows: `newly_pass = 4`, **`newly_fail = 0`**. The `diff` self-compare (current code both sides) also
reports `REGRESSIONS: (empty)`, confirming harness stability.

### Covered-vs-abstained honesty note (MARGIN=0.02)

Of the 4 newly-passing cases, **3 are covered** (`era1_011`, `era3_008`, `era3_015`), so
`top3_on_covered` rises 155→158. **`YAML-CSV95` is abstained** (`reason=margin`): the distinct-family
fix banks it into `top3_family` but not into the covered-accuracy denominator, so it lifts
`top3_family` (193→197) without moving `top3_on_covered` by itself. Reported so the covered-accuracy
number (158/216) is not misread as "+4 covered wins" — it is +3.

## Declined: naive `[:3]` top-4 widen (a separate owner call)

A naive `differential_siblings[:3]` (winner + three sibling *entries* = up to **four** families) is a
real **top-3 → top-4 loosening**, not a correctness fix, and is **out of scope / not shipped**.
Measured here so a future owner sees the option without it being smuggled in.

Beyond the distinct-family window, naive `[:3]` would newly-pass **7** cases, **all genuinely at
overall position 4** (their expected family first appears at the *third* sibling entry, i.e. the
4th-ranked family overall):

| Case | Expected family | First matching sibling entry | Overall position |
|---|---|---|---|
| CASE-020 | lean_condition | index 2 | ~4 |
| EXP-N020 | sensor_fault   | index 2 | ~4 |
| EXT-211  | lean_condition | index 2 | ~4 |
| EXT-212  | lean_condition | index 2 | ~4 |
| era1_006 | sensor_fault   | index 2 | ~4 |
| era2_011 | lean_condition | index 2 | ~4 |
| era2_016 | misfire        | index 2 | ~4 |

**Discrepancy vs the spec estimate:** the task spec estimated "+10 (incl. 6 rank-4 cases)". On the
current `POST_T_V3_3D` run I measure the naive-widen extra set as **7 cases, all rank-4** — not 10/6.
The estimate predates the post-4B/post-repin run and the distinct-family baseline; the measured 7 is
authoritative for this run. All 7 are declined regardless (each is a true rank-4, i.e. a top-4 pass).

## Stale target corrected

The forward-registered note framed this as "widen the sibling window top-2 → top-3 to bank the 2 FREE
cases (`EXP-N010`, `era3_008`)". That framing is obsolete:
- **`EXP-N010` already banks** post-reweight/re-pin — winner family = expected = `rich_mixture`
  (window `{rich_mixture, catalyst_failure, lean_condition}`). It is not a target here.
- **`era3_008`** *is* one of the 4 genuinely recovered by the distinct-family fix.

## Verification

- Inner loop: `py_compile` + `ruff` + `pyright` all clean on `score_v3_yardstick.py`.
- Scorer suite: `test_topk_scorer.py` — 3 passed (2 existing + 1 new distinct-window test). The new
  test uses siblings `[misfire, misfire, lean_condition]`, winner `misfire`, expected
  `lean_condition`: passes under the distinct-family window, fails under the old `[:2]` logic.
- `git status` touches only the two scorer files + this report (no `run_suite.py`, corpus, oracle,
  registry, lab, or engine file).
