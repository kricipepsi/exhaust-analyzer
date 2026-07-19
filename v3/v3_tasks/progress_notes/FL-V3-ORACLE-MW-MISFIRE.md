# FL-V3-ORACLE-MW-MISFIRE — progress note

**Task:** `v3/v3_tasks/FL-V3-ORACLE-MW-MISFIRE_oracle_repin.md`  
**Date:** 2026-07-01  
**Result:** done — re-pinned 10 ORACLE_SUSPECT mechanical_wear rows to misfire and minted `V3_YARDSTICK_2026-07-01`.

## Implementation

- Modified `apps/wired/v7/data/cases_petrol_v7.csv` for exactly 10 rows: `CSV-118`, `CSV-119`, `CSV-120`, `EXT-222`, `EXT-223`, `EXT-224`, `MECH-002`, `MECH-006`, `era1_002`, `era1_015`.
- Set the target oracle fields to `expected_fault_family=misfire`, `expected_fault_code=MF-001`, `expected_state=named_fault`, `expected_confidence_min=0.80`, `expected_confidence_max=1.00`.
- Preserved excluded mechanical-wear rows: `CSV-117`, `EXP-N030`, `MECH-001`, `case_044`.
- Bound `apps/wired/fl_tasks/score_v3_yardstick.py` to `V3_YARDSTICK_2026-07-01`:
  - CSV SHA: `5e41bafe85f634f07050627661d411df20c71bdb0e4390b54d6b9787c108a809`
  - Oracle subset SHA: `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127`
  - Scorer SHA unchanged: `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966`
- Wrote result set: `apps/wired/v7/runs/POST_ORACLE_MW/results.json`.
- Wrote change record: `v3/reports/V3_ORACLE_REPIN_MW_MISFIRE_2026-07-01.md`.

## Verification observations

- `score`: `Hash lock: ok` on `V3_YARDSTICK_2026-07-01`.
- `top3_family`: 184/294 → 193/294 (+9). `CSV-120` was already old-top3 because mechanical_wear appeared as a sibling, so top3 gain is +9 rather than +10.
- scoreboard `family+state`: 80/294 → 85/294 (+5). Five target cases remain abstained under the current margin dial, so raw dimensions pass but the non-abstained primary summary only gains five.
- Targeted raw primary-dimension check: exactly the 10 intended rows flipped primary fail→pass; `primary_new_fail = 0`.
- `diff`: `REGRESSIONS: (empty)`.

## VERIFICATION GATE — FL-V3-ORACLE-MW-MISFIRE

1. Compile : PASS (`py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_oracle_repin.py apps/wired/v7/tests/test_topk_scorer.py`)
2. Lint    : PASS (`ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_oracle_repin.py apps/wired/v7/tests/test_topk_scorer.py`)
3. Types   : PASS (`pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_oracle_repin.py apps/wired/v7/tests/test_topk_scorer.py`, 0 errors)
4. Tests   : PASS (`pytest apps/wired/v7/tests/test_oracle_repin.py apps/wired/v7/tests/test_yardstick_rebind.py apps/wired/v7/tests/test_topk_scorer.py -q` -> 12 passed)
5. Contract: PASS (10 signed-off ORACLE_SUSPECT rows re-pinned; 4 excluded mechanical_wear rows preserved; active yardstick SHA tuple matches live CSV/oracle/scorer; `run_suite.py` untouched)
6. Orphan  : N-A (oracle acceptance gate + hash-lock consumer only; no new runtime field/consumer)
Result: CLEAN

## CODE REVIEW — FL-V3-ORACLE-MW-MISFIRE

Scope         : PASS (changed lines trace to CSV re-pin, active yardstick hashes, guard tests, result/report/progress artifacts)
Composition   : PASS (no engine/router/composition/lab edits; no `run_suite.py` edit; no cross-lab import change)
Consumers     : PASS (no mapped runtime field added; consumer is v3 acceptance gate and frozen-yardstick guard)
Literals      : PASS (new numeric bands are the existing misfire confidence band copied from the Option-B family band convention)
Docstrings    : PASS (new tests have task-specific docstrings; no new public runtime function)
Craft (WARN)  : Depth: no abstraction added; changes remain at data/test/hash seam. Deletion: no helper or shim added. Seam: oracle change lives in CSV; hash-lock change in scorer constants; no engine leakage. Interface: verification uses public scoreboard commands plus guard tests.
Result: CLEAN

## Known out-of-scope observation

`apps/wired/tests/test_oil_cases.py::test_oil_cases_route_to_expected_faults` expects the `MW-003` fixture to route to `MW-003`, but the live engine routes it to `MF-001`. This is outside this oracle-data task: engine and fixture code were not changed here.
