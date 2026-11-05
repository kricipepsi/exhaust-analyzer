# Result

## Status
completed

## Summary
`_resolve_single_source` in `labs/comlab/registry/integration_shim.py` now returns `None` for the live `shrtft1`/`longft1` (so also `stft_b1`/`ltft_b1`) when `obd_live_data.trim_analytics_gate` is present and not `VALID`. The freeze-frame fallback is untouched. Three new tests (10 cases), the obdlab None-lambda filter and the two consumer comments are in.

## Files changed
- `labs/comlab/registry/integration_shim.py` (R1, R2)
- `labs/comlab/registry/tests/test_integration_shim.py` (R3)
- `labs/obdlab/tests/pid_logset/test_pid_logset_wiring_gate.py` (R4)
- `labs/comlab/comlab/schemas/ingestion.py`, `apps/wired/wired/composition.py` (R5, one line each)
- The note and this RESULT (uncommitted, as step 5 expects)

## Commands executed
`### Verification ###` steps 1-5 as written; a red run of the new tests before the guard; a mutant run with the guard disabled; `git log`, `git status`.

## Validation evidence
- Red before the guard: `9 failed, 31 passed`.
- Step 1: `40 passed`; registry/tests `5 failed, 498 passed, 4 deselected` (5 FAILED lines, all `test_build_corpus.py`).
- Step 2: comlab `526 passed, 4 skipped, 2 errors`; obdlab `391 passed, 2 skipped`; wired `46 passed`; ui `30 passed`.
- Mutant (guard disabled): `9 failed, 31 passed`.
- Step 3: only the five source files and the note were changed.
- Step 4 (`rehearse.py ect40 live`):
  ```
  ect40: cases 297 gates {'ENGINE_COLD': 295, None: 2}
    blocked 295; blocked with a live trim 295; blocked with a resolved trim 206
    [live] verdict changes 0 (on unblocked cases 0) | new exceptions 0 | resolved trims left on blocked 206
      base on blocked {'MF-001': 70, 'RM-001': 49, 'LC-001': 42, 'CF-001': 30, 'SF-001': 27, 'LC-002': 23, 'EF-004': 14}
  ```
  The previous decisive failure is absent: the script's patch is now a no-op (0 live verdict changes), and base on blocked equals P2's fixed distribution.
- Step 5: `All checks passed!`.
- R6, P2's 5 ECT-40 verdict changes from `rehearse.out`, each caused by "live trims blocked" (gate ENGINE_COLD): CASE-039 RM-001→SF-001; CSV-025 SF-008→SF-001; EXP-N006 RM-001→CF-001; EXP-N020 RM-001→SF-001; TC-046 SF-008→SF-001. No other change.

## Criteria
1. MET: step 1 counts equal P3; failed names are only `test_build_corpus.py`; the mutant fails 9.
2. MET: step 2 equals P4.
3. MET: step 4 output above; the 5 changes are listed.
4. MET: ruff passes; the commit sits on `fix/T-AUD-4g` after the spec commit; `git status --porcelain` lists only the note and this RESULT.

## Decisions the task did not specify
- Helper `_trims_blocked` and constant `_GATED_LIVE_TRIMS` follow the shape of Cowork's `apply_fix.py`.
- The commit has no Co-Authored-By trailer: `bash_guard` refuses a commit command that holds the word Claude.
- The parametrized gate list is string literals, not an obdlab import (no cross-lab import in comlab tests).

## Pre-existing changes preserved
None; the starting tree was clean.

## Rollback
`git revert 1b0594c` on `fix/T-AUD-4g`, or reset the branch to `4844cdf`.

## Remaining risks or uncertainties
Freeze-frame trims stay ungated (T-AUD-4h). Context at end: ABSENT.

Branch: `fix/T-AUD-4g`
```
1b0594c fix(T-AUD-4g): registry shim honours trim_analytics_gate for live trims
```
(`git log --oneline 4844cdf..HEAD`.)
