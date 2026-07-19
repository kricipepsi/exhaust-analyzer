# T-TST-6 — Progress Notes

**Date:** 2026-06-09

## Plan

Single projection script `labs/obdlab/tests/scripts/project_obdlab_cases.py` that:
1. Reads the reconciled master (`TestSuite/cases_petrol_master_v6.csv`)
2. Filters rows where `lab_decidability` contains "OBD" (194 rows)
3. Maps master column names per MASTER_RECON_REPORT inventory
4. Derives `number_of_banks` (from `bank_config`), `has_maf`, `has_map` (from data presence)
5. Adds expected-output columns all marked `gt_method=characterization`
6. Writes `labs/obdlab/tests/fixtures/obdlab_cases.csv`

No rows needed `lab_decidability` re-derivation — the reconciled master's column is used directly.

## VERIFICATION GATE

```
VERIFICATION GATE — T-TST-6
============================
Syntax:         PASS (python -m py_compile)
Type check:     PASS (pyright: 0 errors, 0 warnings)
Lint:           PASS (ruff: All checks passed)
pytest Layer-1: SKIP (data projection, no test suite)
Fast benchmark: SKIP (no model output touched)
Diff review:    2 files created, no scope creep

Byte-consistency: 0 mismatches across all 194 rows × 8 mapped columns (verified via PowerShell cross-check)
CSV loadability: PASS (Python csv.DictReader: 194 rows, 25 columns)

Pythonskill checklist items applied:
  1. Type hints — PASS (all functions annotated)
  2. Docstrings — PASS (module docstring)
  3. No mutable defaults — PASS
  4. No bare except — PASS
  5. No magic numbers — PASS
  6. f-strings — PASS
  7. Pathlib — PASS (pathlib.Path throughout)
  8. Context managers — PASS (with open(...))
  9. is None not == None — PASS
  10. Sorted imports — PASS (stdlib only)

Status: PASS — gates clean
```

## CODE REVIEW

Scope: `labs/obdlab/tests/scripts/project_obdlab_cases.py` (~115 lines) + `labs/obdlab/tests/fixtures/obdlab_cases.csv` (194 rows).

- **Correctness:** All 194 OBD-decidable rows projected (none dropped, none added). Column mapping verified 0 mismatches against master. `number_of_banks` derivation: 190 single (1), 4 dual (2) — matches master `bank_config` distribution. `has_maf`: 57 true (rows with MAF data), `has_map`: 1 true (row with MAP data). `calculated_engine_load_pct`: empty (absent from master, per MASTER_RECON_REPORT recommendation).
- **No unintended changes:** Script is self-contained, imports only stdlib. Does not touch lab code, schemas, or PROJECTION_CONTRACT.md. Output CSV lives at the TEMPLATE.md-prescribed path (`fixtures/obdlab_cases.csv`).
- **Signal/noise:** All 7 expected-output columns marked `gt_method=characterization` — master carries no OBD ground truth. The `gt_source` column is populated per-row with per-column annotations. Consumer: T-TST-8 Mode A1 + `test_cases.py`.
- **Scope creep:** None. The relabel (T-MASTER-RECON), descriptor/generators (T-TST-8), and obdlab code changes are all out of scope per the task spec.

## Unplanned follow-ups logged

| ID | Finding |
|---|---|
| FU-TST6-1 | `PROJECTION_CONTRACT.md` OBDLab consumed columns list `has_maf`/`has_map`/`calculated_engine_load_pct` — absent from master. Derived from data presence / left empty. Contract should be updated to reflect actual master columns. |
| FU-TST6-2 | `PROJECTION_CONTRACT.md` expected-output columns (`expected_ve_pct`, `expected_maf_status`, etc.) have no master source. They will be populated by T-TST-8's first characterization run (decision-rate harness). |
