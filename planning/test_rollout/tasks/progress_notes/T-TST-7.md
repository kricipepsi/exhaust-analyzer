# T-TST-7 - Progress Notes

**Date:** 2026-06-10

## Plan

Single projection script `labs/dtclab/tests/scripts/project_dtclab_cases.py` that:
1. Reads the reconciled master (`TestSuite/cases_petrol_master_v6.csv`) from the 4DLab root.
2. Filters rows where `lab_decidability` contains `DTC` (expected 194 rows).
3. Projects the master's real DTCLab-consumed input columns byte-for-byte: `dtcs`, `ff_dtcs`, `ff_ect`, `ff_rpm`, `ff_load`, `ff_map`, `ff_stft_b1`, `ff_ltft_b1`, and `fuel_status`.
4. Carries `dtcs` and `ff_dtcs` as raw strings while keeping a local comma-split helper for validation/counting only.
5. Emits empty `expected_routing_tags`, `expected_historical_context`, and `expected_freeze_frame_status` columns, with `gt_source` marking each as `characterization`.
6. Writes `labs/dtclab/tests/fixtures/dtclab_cases.csv`.

No DTCLab runtime code, schemas, descriptor, generators, `PROJECTION_CONTRACT.md`, or graphify artefacts are in scope.

## VERIFICATION GATE

```
VERIFICATION GATE - T-TST-7
===========================
Syntax:         PASS (python -m py_compile)
Imports:        PASS (stdlib-only script executed successfully)
Type check:     PASS (pyright: 0 errors, 0 warnings)
Lint:           PASS (ruff: All checks passed)
pytest Layer-1: PASS collection (labs/dtclab/tests/test_cases.py exited 0; existing T-TST-9 skip remains)
Fast benchmark: SKIP (no model output touched)
Diff review:    3 files created, no scope creep

Projection count:     PASS (194 DTC-decidable rows)
Byte-consistency:     PASS (0 mismatches across 194 rows x 9 projected input columns)
CSV loadability:      PASS (csv.DictReader: 194 rows, 14 columns)
Expected outputs:     PASS (3 expected-output columns empty on every row)
gt_source annotation: PASS (gt_method=characterization plus per-column annotations on every row)
DTC cells:            PASS (115 non-empty dtcs rows, 1 non-empty ff_dtcs row)

Pythonskill checklist items applied:
  1. Type hints - PASS (all functions annotated)
  2. Docstrings - PASS (module and public helpers documented)
  3. No mutable defaults - PASS
  4. No bare except - PASS
  5. No magic numbers - PASS (expected row count named)
  6. f-strings - PASS
  7. Pathlib - PASS (pathlib.Path throughout)
  8. Context managers - PASS (Path.open with context managers)
  9. is None not == None - PASS
  10. Sorted imports - PASS (stdlib only)

Status: PASS - gates clean
```

## CODE REVIEW

Scope: `labs/dtclab/tests/scripts/project_dtclab_cases.py` + `labs/dtclab/tests/fixtures/dtclab_cases.csv`.

- **Correctness:** The projection uses `lab_decidability` containing `DTC`, not a re-derived predicate. It emits exactly 194 rows. All nine input columns are copied byte-for-byte from the master, including raw `dtcs` and `ff_dtcs` cells.
- **Boundaries:** The script is self-contained and stdlib-only. It does not import DTCLab runtime code, the shared harness engine, graphify, schemas, descriptors, or generators.
- **Signal/noise:** `expected_routing_tags`, `expected_historical_context`, and `expected_freeze_frame_status` are intentionally empty because the master has no DTCLab ground truth. `gt_source` marks each as characterization for T-TST-9.
- **Failure paths:** The script fails early if the master file is missing, the CSV has no header, required projection columns are absent, or the projected row count drifts from 194.
- **Scope creep:** None. No changes to DTCLab runtime code, `PROJECTION_CONTRACT.md`, graphify artefacts, or unrelated dirty worktree files.

## Unplanned follow-ups logged

| ID | Finding |
|---|---|
| FU-TST7-1 | `PROJECTION_CONTRACT.md` DTCLab consumed-input list (`dtcs_mode_03/07/0a`, `mode_06_monitor_results`, `codes_cleared`, `active_mil`, `mil_flashing`) does not match the master's real columns (`dtcs`, `ff_*`, `ff_dtcs`, `fuel_status`). Contract should be reconciled to disk. |
| FU-TST7-2 | DTCLab payload fields `active_mil` / `mil_flashing` / `mode_06_monitors` have no master source column; they should be populated by T-TST-9 characterization, not projected here. |
