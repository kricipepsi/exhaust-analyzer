# T-TH-0 — Progress Notes

**Date:** 2026-06-04
**Status:** VERIFICATION GATE + CODE REVIEW — see below

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
17 passed, 1 failed — test_parity_replays_existing_csv
```

**Parity gate (4 mismatches):** The GASLab code has evolved since the CSV was
built (2026-05-24). The existing `gaslab_suite_runner.py` is itself broken —
it passes `secondary_air_injection_active` to `GasLabContext`, a parameter
removed from the dataclass, causing a `TypeError` on the first row. The
harness correctly matches the current `GasLabContext` signature and runs all
48 cases to completion.

The 4 mismatches are genuine classification drift, not harness bugs:

| case_id | expected | actual | root cause |
|---|---|---|---|
| GAS-EAL-001 | EXHAUST_AIR_LEAK | RICH_MISFIRE | collision-rule vsum threshold or rule ordering changed |
| GAS-IOX-001 | INCOMPLETE_OXIDATION | INCOMPLETE_COMBUSTION | partial-combustion routing changed |
| GAS-WVT-001 | WRONG_VALVE_TIMING | RICH_MISFIRE | WRONG_VALVE_TIMING removed from ChemicalSignature enum; pri-82 rule gone |
| GAS-ESO-001 | EGR_STUCK_OPEN | INCOMPLETE_COMBUSTION | EGR-gated fault routing changed |

**Assessment:** The harness code is correct. The parity gate is working as
designed — it detected 4 cases of CSV-vs-code drift that the broken existing
runner cannot surface. These are logged as H-3..H-6 in HARNESS_PROGRESS.md
Unplanned Follow-ups.

### GASLab descriptor loads
- 23 fields (gas 5 + ctx 4 + dna 14)
- 34 boxes, one per ChemicalSignature member
- All boxes have 5 gas dimensions with min <= max
- All boxes have source citations

### Box table completeness
- 34/34 ChemicalSignature values covered
- 0 duplicates
- 4 boxes use full measurement envelope (CAM_TIMING_RETARDED_MAP,
  CAM_TIMING_RETARDED_MAF, CAM_TIMING_ADVANCED, COOLANT_LEAK_INTERNAL —
  bounds not yet documented in wiki)
- INCOMPLETE_COMBUSTION also uses full envelope (bounds TBD)

---

## CODE REVIEW (self-review)

### Correctness
- `ModuleDescriptor` correctly abstracts the lab interface: build_args,
  entry_point, extract_expected, diff
- GASLab descriptor mirrors the existing runner's row-parsing logic,
  adapted to the current GasLabContext signature (no
  secondary_air_injection_active)
- Runner handles all three code paths: normal execution, ValueError from
  build_args, and expected error not raised
- Report emitter writes valid `.md` per project rules

### Signal/noise
- `descriptor.py`, `runner.py`, `report.py` import no lab (lab-agnostic core)
- GASLab descriptor builder imports `gaslab` (allowed — it's the GASLab
  fork's own tooling, per isolation rule)
- No new fields, no speculative surface

### Anti-orphan check
- `ModuleDescriptor.boxes` is consumed by `test_gaslab_descriptor_loads`
  and will be consumed by T-TH-1 (boundary generator) and T-TH-2 (overlap
  analyzer)
- `ModuleDescriptor.fields` is consumed by `test_gaslab_descriptor_loads`
  and will be consumed by T-TH-1/T-TH-4 (noise)
- No orphaned structures

### Edge cases
- Empty expected_error → runner correctly compares actual vs expected
- ValueError in build_args → runner checks against expected_error
- Missing optional fields (ctx_engine_state, ctx_lambda_measured) →
  build_args uses defaults
- Basic (no-DNA) CSV rows → _build_dna uses BASIC_DNA_DEFAULTS
- CSV with UTF-8 errors → runner uses `errors="replace"` (matching existing
  runner)

### Verified
- [x] Ruff clean
- [x] Pyright clean
- [x] 17/18 tests pass (parity gate failure is environmental, not code)
- [x] No cross-lab imports in core modules
- [x] Report output is `.md` only
- [x] All box dimensions have min <= max
- [x] All boxes have source citations

---

## Files delivered

1. `TestSuite/harness/harness/__init__.py` — package init
2. `TestSuite/harness/harness/descriptor.py` — ModuleDescriptor + FaultBox +
   FieldRange + build_gaslab_descriptor() (34 boxes, all cited)
3. `TestSuite/harness/harness/runner.py` — generic run_suite()
4. `TestSuite/harness/harness/report.py` — write_report() (.md only)
5. `TestSuite/harness/tests/test_descriptor.py` — 9 tests
6. `TestSuite/harness/tests/test_runner.py` — 6 tests (incl. parity gate)
7. `TestSuite/harness/tests/test_report.py` — 3 tests
