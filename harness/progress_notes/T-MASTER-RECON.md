# T-MASTER-RECON — Progress Notes

**Date:** 2026-06-09

## Plan

Single script `TestSuite/harness/scripts/reconcile_master.py` that:
1. Backs up `cases_petrol_master_v6.csv`
2. Maps `expected_top_fault_family` to the 12-value FaultFamily enum (`invalid_input` → `no_fault`; blank → `no_fault`)
3. Fills 40 blank `expected_perception_gap` → `False`
4. Adds `lab_decidability` column (perception_gap/sentinel → `COMLab`, else → `GASLab|OBD|DTC`)
5. Quarantines rows with both blank family AND blank perception_gap (3 rows: case_011, case_020, case_021)
6. Writes `MASTER_RECON_REPORT.md` with the OBD column-name inventory

No rows had `single` or blank `expected_top_fault` — the H-10 25+14 claim was not reproducible on this file version.

## VERIFICATION GATE

```
VERIFICATION GATE — T-MASTER-RECON
==================================
Syntax:         PASS (python -m py_compile)
Type check:     PASS (pyright: 0 errors, 0 warnings)
Lint:           PASS (ruff: All checks passed)
pytest Layer-1: SKIP (data reconciliation script, no test suite)
Fast benchmark: SKIP (no model output touched)
Diff review:    4 files changed, no scope creep

Pythonskill checklist items applied:
  1. Type hints — PASS (all functions annotated)
  2. Docstrings — PASS (module docstring + per-function)
  3. No mutable defaults — PASS
  4. No bare except — PASS
  5. No magic numbers — PASS
  6. f-strings — PASS
  7. Pathlib — PASS (pathlib.Path throughout)
  8. Context managers — PASS (with open(...))
  9. is None not == None — PASS
  10. Sorted imports — PASS

Status: PASS — gates clean
```

## CODE REVIEW

Scope: `TestSuite/harness/scripts/reconcile_master.py` (single script, ~265 lines).

- **Correctness:** All 3 owner-ratified decisions applied. Family mapping verified: 0 rows with invalid FaultFamily values post-recon. Column inventory matches actual master header.
- **No unintended changes:** Script is self-contained, imports only stdlib. Does not touch lab code, schemas, or PROJECTION_CONTRACT.md.
- **Error handling:** BOM handled (utf-8-sig). Backup skip is deliberate (idempotent re-run). Assertion on final valid-family count catches regressions.
- **Scope creep:** None. The 3 quarantined rows are the only rows matching the "blank family + blank perception_gap" criterion. No malformed `single`/blank top_fault rows were found — Decision 3 quarantine criteria documented as a no-op for those specific patterns.

## Unplanned follow-ups logged

| ID | Finding |
|---|---|
| FU-RECON-1 | `PROJECTION_CONTRACT.md` OBDLab input names don't match master header (inventory in report). Reconcile at T-TST-6 implementation. |
| FU-RECON-2 | File a proposal for `invalid_input` sentinel family if COMLab fusion needs to distinguish analyzer failures from genuine no_fault. |
