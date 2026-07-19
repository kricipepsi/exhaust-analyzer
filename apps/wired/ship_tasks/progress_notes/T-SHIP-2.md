# Progress note — T-SHIP-2
**Date:** 2026-07-07 · **Mode:** STRICT · **Runner:** Cowork architect (owner-authorized impl)

## Plan
Add the canon-required synthetic-vs-real split (Provisional-synthetic #3) to the
non-hash-locked scoreboard read side, sourced from the `v3/data/*_synthetic_seed_*.csv`
provenance side files. No engine/corpus/rule/yardstick/`run_suite.py` change.

## Implementation
- `apps/wired/fl_tasks/score_v3_yardstick.py`: `load_synthetic_case_ids()` (side-file
  provenance loader, empty-safe) + split counters in `summarize()` + `SYNTHETIC-VS-REAL
  SPLIT` block in `render_score()` + 4 new summary fields.
- `apps/wired/v7/tests/test_topk_scorer.py::test_synthetic_split_reconciles_with_top3`.

## VERIFICATION GATE — T-SHIP-2
1. Lint    : PASS (ruff clean)
2. Tests   : PASS (test_topk_scorer 4 passed; test_resolution_diff 2 passed)
3. Score   : PASS (`Hash lock: ok`; top3_family unchanged 269/294; split renders
             `191/294 = 64.97 % real` + `78 synthetic (C2 19, C3 16, C4 10, C5 10, C6 13, C9 10)`)
4. Reconcile: PASS (191 + 78 = 269; matches T-SHIP-1 independent map)
5. Contract: PASS (scorer read-side only; `run_suite.py` + yardstick hashes untouched)
Result: CLEAN

## CODE REVIEW — T-SHIP-2
Scope     : PASS (one read-side file + one test)
Consumers : PASS (split read by `render_score` + summary JSON consumers; canon-named requirement)
Honesty   : PASS (header line states the field-accuracy caveat verbatim in the output)
Result: CLEAN
