# T-COMV2-LAMBDAPROJ-1 progress note

Status: done
Date: 2026-06-21

## Plan / Scope Confirm

`projection.py::project` reads three CoC λ-window fields (`target_lambda_v112`,
`co_high_idle`, `co_low_idle`) from `emissions.get()` instead of `vin.get()` —
the wrong dict nesting level per the upstream vinlab/DNALab contract. The upstream
`vinlab/models.py::VinDNA` declares them at top level (`:228/:231/:232`) and the
DNALab fixture confirms the same JSON shape. Because the path is wrong,
`GasLabDnaView` silently receives `None` for all three. Re-point to `vin.get()`
(3 lines), fix the test fixture to match the upstream contract, add regression
tests, mark proposal graduated. No schema change, no flag — pure path correction.

## Changed Files

- `comlab/projection.py` — re-pointed `target_lambda_v112`, `co_low_idle`,
  `co_high_idle` from `emissions.get()` → `vin.get()` (lines 78–83); removed
  now-unused `emissions` local variable.
- `tests/unit/test_projection.py` — moved CoC fields to top level in
  `modern_vehicle_dna` fixture to match upstream contract; added
  `test_projection_lambda_paths_land_from_top_level`,
  `test_projection_lambda_absent_returns_none`,
  `test_projection_equipment_flags_unchanged`.
- `comlab/config/proposals/entries.yaml` — `vehicle-dna-projection-paths`
  status `proposed → graduated`.

VERIFICATION GATE — T-COMV2-LAMBDAPROJ-1
=========================================
Phase 1 Syntax/import:  PASS (ruff: all checks passed)
Phase 2 Type check:     PASS (pyright: 0 new errors; all 15 pre-existing)
Phase 3 Lint:           PASS (`ruff check .`: all checks passed)
Phase 4 pytest:         PASS (503 passed, 4 skipped; projection target 25 passed)
Phase 5 Read-lands grep:PASS (`target_lambda_v112`/`co_high_idle`/`co_low_idle`
                              re-pointed to `vin.get()` at projection.py:78/80/82)
Phase 6 Diff review:    PASS (projection.py, test_projection.py, entries.yaml,
                              progress note, ledger row only)

CODE REVIEW — T-COMV2-LAMBDAPROJ-1
====================================
Three-line path correction — the minimal change. The `emissions` removal is safe
because that local was only consumed by the three CoC reads now re-pointed.
The test fixture update moves CoC fields to their contract-correct top-level
position; existing tests that asserted projected values continue to pass.
Equipment-flag reads (`has_catalyst`, `egr_equipped`) were not touched — they
remain at `vin.get()` (a separate proposal item, out of scope). No cross-lab
imports. No graphify. No schema change.
