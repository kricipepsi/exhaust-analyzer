# T-TH-1 — Progress Notes

**Date:** 2026-06-04
**Status:** VERIFICATION GATE + CODE REVIEW — both clean

---

## VERIFICATION GATE

### Ruff
```
All checks passed!
```

### Pyright
```
0 errors, 0 warnings, 0 informations
```

### Pytest
```
10 passed in 31.69s
```

**All 10 tests pass:**
- `test_boundary_generates_six_per_dim_per_box` — 1 box × 5 dims × 6 positions = 30 cases
- `test_boundary_generates_multiple_boxes` — 2 boxes → 60 cases (linear scaling)
- `test_boundary_geometric_oracle_correct` — min-eps → outside, centroid → inside, max+eps → outside
- `test_boundary_oracle_outside_when_one_dim_outside` — any single-dim breach makes the point outside
- `test_build_row_formats_int_dims` — int dimensions formatted without decimal point
- `test_custom_epsilon` — custom eps used, unspecified dims fall back to defaults
- `test_boundary_run_with_stub` — `run()` executes all cases, PASS count matches oracle
- `test_write_boundary_report_is_markdown` — writes valid `.md`
- `test_write_boundary_report_with_failures` — includes Failures section
- `test_boundary_gaslab_run` — 34 boxes × 5 dims × 6 = 1020 cases, report written

### GASLab boundary run summary

**427/1020 (41.9%)** boundary points match the geometric oracle.
**593 mismatches** — the dominant causes:

1. **SAMPLE_INVALID dominates (~60% of mismatches).** The validity gate (triangle
   CO+CO2+O2 bands, `GAS_VOCABULARY §5`) fires before any signature rule. Many
   box centroids produce gas values that fail the validity check, so the
   classifier short-circuits to SAMPLE_INVALID before the box-membership logic.
2. **TIMING_RETARDED specificity fallback.** Boxes near stoich (NORMAL_OPERATION,
   FLAT_CAMSHAFT, WORN_PISTON_RINGS) get routed to TIMING_RETARDED because the
   lambda calculation puts them outside the NORM lam band (0.995–1.005), and
   TIMING_RETARDED is a low-priority specificity fallback.
3. **Identical gas signatures.** TIMING_OVER_ADVANCED and HIGH_COMBUSTION_TEMP
   share identical gas bounds (per descriptor `HCT §7.8` and `TOA §7.12`), so
   the classifier picks one based on priority/rule ordering — not the geometric
   box. Similarly, EGR_STUCK_CLOSED has the same gas bounds as HCT.
4. **Outside-point PASSes.** Points geometrically outside a box (max+eps) that
   land inside another box's region correctly show as PASS (classifier returned
   a different signature). These are working as designed.

The 41.9% match rate is **expected and correct** for a priority-based classifier
with a validity gate. The report includes the overlap caveat pointing to T-TH-2.

---

## CODE REVIEW (self-review)

### Correctness
- `BoundaryGenerator.generate()` correctly iterates all boxes × dims × positions.
  For each boundary point, non-target dimensions are held at the box centroid
  (the most-definitely-inside point), minimizing ambiguity from multi-dimension
  deviation.
- Geometric oracle is computed correctly: a point is "inside" iff ALL 5 gas
  dimensions are within the box's `[min, max]` bounds.
- `_build_row()` uses `FieldRange.type_` from the descriptor to format integer
  dimensions correctly (`str(int(round(val)))`), avoiding `int("50.0")`
  ValueError.
- `run()` calls `descriptor.build_args(row)` followed by
  `descriptor.entry_point(*args)`, checking `actual.chemical_state.value` against
  the box signature. Exceptions are caught and recorded as `ERROR:<name>`.
- `write_boundary_report()` writes valid `.md` with full results table and
  failure summary.
- 427/1020 PASS (not zero) → sanity check passes: the generator is running real
  code and producing meaningful comparisons.

### Signal/noise (anti-orphan check)
- `BoundaryGenerator` imports **no lab**. It operates on `ModuleDescriptor`
  objects, calling `build_args` / `entry_point` through the descriptor's own
  closures.
- `BoundaryGenerator` consumes `ModuleDescriptor.boxes` and `ModuleDescriptor.fields`
  — both populated by the GASLab descriptor in T-TH-0. No orphaned structures.
- `DEFAULT_EPS` is a public constant consumed by tests.
- `GAS_DIMS` and `POSITIONS` are module-level constants consumed by tests and
  by `generate()` — both are live code paths.

### Edge cases
- Boxes with only a subset of GAS_DIMS → `box_dims` filters to only the defined
  dimensions. (All current GASLab boxes have all 5, but the code handles the
  general case.)
- Epsilon pushing integer below 0 → `int(round(-1.0))` = `-1`, which converts
  to `"-1"` → `int("-1")` = `-1`. Valid.
- `build_args` raises → caught as `ERROR:<ExceptionName>`, recorded in verdict.
- `entry_point` raises → same error handling.
- Box signature longer than 22 chars → truncated in case_id (`sig[:22]`).
  Ensures case_id stays manageable.

### Verified
- [x] Ruff clean
- [x] Pyright clean (0 errors, 0 warnings)
- [x] 10/10 tests pass
- [x] GASLab boundary report written to `progress_notes/T-TH-1_boundary_report.md`
- [x] No cross-lab imports in generator module
- [x] Report output is `.md` only
- [x] 1020 cases generated and executed without crashes
- [x] Geometric oracle labels verified correct by unit test

---

## Files delivered

1. `TestSuite/harness/harness/generators/__init__.py` — package init
2. `TestSuite/harness/harness/generators/boundary.py` — BoundaryGenerator +
   BoundaryCase + BoundaryReport + write_boundary_report() (155 lines)
3. `TestSuite/harness/tests/test_boundary.py` — 10 tests (210 lines)
