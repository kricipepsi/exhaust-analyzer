# Progress Note — T-V3-D6-SCORERWIN: `top3_family` counts 3 distinct families

Corrected both `top3_family` scorer sites in [[score_v3_yardstick]] to count **winner + the first
two *distinct* non-winner sibling families** instead of the first two sibling *entries*
(`differential_siblings[:2]`). A new shared helper `collect_top3_families()` implements the distinct
walk (skip `unspecified`, the winner's own family, and already-collected families; stop at two), and
both the `summarize()` main loop and the `top3_family_pass()` helper now call it so they agree.
Mirrors the family-aware dedupe precedent in [[T-V3-3C_family_aware_abstain_margin]]. No engine, lab,
registry, corpus, oracle, `run_suite.py`, or yardstick change — only the non-locked scorer read-site.

Full delta report: [[V3_SCORERWIN_TOP3_DISTINCT_2026-07-01]].

## Disclosure

- `top3_family`: **193/294 → 197/294** (65.65% → 67.01%). This is a **definition correction**, not new
  engine accuracy — no prediction changed; the metric now counts 3 *distinct* families as its name
  claims.
- Newly passing (4): `era1_011`, `era3_008`, `era3_015`, `YAML-CSV95` — each was masked by a
  same-family duplicate crowding the first two sibling entries.
- **Monotonic, no regression.** Old window ⊆ distinct window for every case; verified directly on all
  294 rows: `newly_pass = 4`, `newly_fail = 0`. `diff` self-compare reports `REGRESSIONS: (empty)`.
- `single_verdict` (family+state) unchanged: **126/294**. `coverage` unchanged: **0.73** (MARGIN=0.02).
- `top3_on_covered`: **155/216 → 158/216** (71.76% → 73.15%). Only **+3** covered wins, not +4:
  `YAML-CSV95` is abstained (`reason=margin`), so it lifts `top3_family` but not covered-accuracy.
- **Naive `[:3]` top-4 widen declined & flagged:** on this run it would add **7** cases, all
  genuinely rank-4 (`CASE-020`, `EXP-N020`, `EXT-211`, `EXT-212`, `era1_006`, `era2_011`, `era2_016`).
  The spec estimated "+10 incl. 6 rank-4"; measured on `POST_T_V3_3D` it is 7, all rank-4 — discrepancy
  recorded in the report. All 7 are declined (a top-3→top-4 loosening = separate owner call).
- **Stale target corrected:** `EXP-N010` already banks (winner=expected=`rich_mixture`); it is not a
  target. `era3_008` is one of the 4 genuinely recovered here.

## VERIFICATION GATE — T-V3-D6-SCORERWIN
1. Compile : PASS  (`py_compile` on `apps/wired/fl_tasks/score_v3_yardstick.py`, `apps/wired/v7/tests/test_topk_scorer.py`)
2. Lint    : PASS  (`ruff check` on both touched files — All checks passed)
3. Types   : PASS  (`pyright apps/wired/fl_tasks/score_v3_yardstick.py` — 0 errors, 0 warnings)
4. Tests   : PASS  (`pytest apps/wired/v7/tests/test_topk_scorer.py -q` -> 3 passed: 2 existing + 1 new distinct-window test; new test passes under the distinct window, fails under old `[:2]` logic — verified)
5. Contract: PASS  (`score --results POST_T_V3_3D` -> `top3_family = 197/294`, `single_verdict` unchanged 126/294, `Hash lock: ok` no re-mint; per-case old-vs-new: `newly_pass={era1_011,era3_008,era3_015,YAML-CSV95}`, `newly_fail=(empty)`; naive top-4 widen declined; `run_suite.py`/corpus/oracle/yardstick untouched)
6. Orphan  : N-A  (No new engine field/signal emitted; consumer is the existing scoreboard `top3_family`/`top3_on_covered` metrics + owner acceptance read — a scorer read-site correctness fix only)
Result: CLEAN

## CODE REVIEW — T-V3-D6-SCORERWIN
Scope         : PASS  (Only the shared helper + the two scorer sites, one new test, one report — every line traces to a Deliverable; no adjacent refactor)
Composition   : PASS  (No `run_suite.py`, corpus, oracle, yardstick, registry, lab, engine, graph, or `Vault/` edit; no cross-lab import added)
Consumers     : PASS  (Consumer named: scoreboard `top3_family`/`top3_on_covered` + owner acceptance read; no new signal/field/enum)
Literals      : PASS  (No new boundary literal; the "two distinct families" window is the metric's own top-3 definition, cited to [[T-V3-3C_family_aware_abstain_margin]])
Docstrings    : PASS  (New `collect_top3_families()` documented; `top3_family_pass()` docstring updated to the distinct-window definition)
Craft (WARN)  : Depth: one small helper, no branching accreted; both sites deduplicated onto it. Deletion: removed the duplicated inline `[:2]` loops — no dead code left. Seam: the distinct-family window lives in exactly one function; main loop and helper share it (they previously each hand-rolled the walk and could drift). Interface: tests exercise `summarize()` through its public signature, not the private helper.
Result: CLEAN
