# Result

## Status
completed

## Summary
The technician's overrides (`upstream_o2_type`, `de_cat`) now go into `vin_dna["emissions"]` before metadata, the incomplete-input check, GASLab and OBDLab. `_build_obd_dna_view` maps SUPERCHARGED to TURBOCHARGED.

## Files changed
- `apps/wired/wired/composition.py` (R1, R2)
- `apps/wired/tests/test_composition.py` (R3: 4 NEW tests + 1 PIN)
- `apps/wired/audit_tasks/progress_notes/T-AUD-4b.md`, this file

## Commands executed
Verification steps 1-5 as written; mutant runs under `C:/4DApp/recheck/T-AUD-4b/mut/` (PYTHONPATH at the copy).

## Validation evidence
- step 1: `46 passed`
- step 2: ui `30 passed`; dnalab `27 passed`; obdlab `388 passed, 2 skipped`; gaslab `208 passed, 2 skipped, 4 deselected` (= P3)
- step 3: comlab `526 passed, 4 skipped, 2 errors` (the 2 known R0-2 collection errors)
- step 4 (R4):
```
corpus 314 decoded upstream_o2_type {'NARROWBAND': 305, 'WIDEBAND_AFR': 1, 'NARROWBAND_0_TO_1V': 8} wideband cases 1
changes under the override (base -> fixed): {}
base exceptions 0 fixed exceptions 0
SUPERCHARGED projection: ok
```
  P2's before/after: the base (override after the labs) gave `('LC-002', 'RICH_MIXTURE', 'WIDEBAND_LINEAR')` for `era2_015` (`rehearse.out`). With the override first, the code gives the fixed tuple. The rehearsal's hook already applies the override, so it prints no change. `test_upstream_o2_override_requires_its_own_reading` pins the `OBD_INPUT_INCOMPLETE` verdict on `era2_015`'s inputs. Exceptions 0 → 0.
- step 5: `All checks passed!`
- Red gate: before the code change the 4 NEW tests failed (`4 failed, 3 passed`); the PIN passed.
- Mutants: m1 fails 3 override tests; m2 fails `test_supercharged_projects_as_turbocharged`.

## Criteria
1. MET: `46 passed`; m1 and m2 each fail named tests.
2. MET: step 2 equals P3.
3. MET: step 4 prints `changes ... {}`, `fixed exceptions 0`, SUPERCHARGED `ok`. The spec's step-4 text defines this output; the hooked script does not print P2's literal tuple (see above).
4. MET: ruff clean; commit `fcec137` on `fix/T-AUD-4b` after the spec commit; `git status --porcelain` lists the note and this RESULT only.

## Decisions the task did not specify
- The test embeds era2_015's raw inputs instead of reading the v7 corpus.
- `vin_dna["emissions"]` is replaced by `_as_dict(...)` so the override and the request share one dict.
- Mutants run as copies with PYTHONPATH.
- The commit message has no attribution trailer (`bash_guard` refuses it).

## Pre-existing changes preserved
none present (clean tree at start).

## Rollback
`git revert fcec137` on `fix/T-AUD-4b`.

## Remaining risks or uncertainties
Criterion 3 relies on the spec's step-4 text for P2's tuple; the base side comes from `rehearse.out`, not a new run.

Branch: `fix/T-AUD-4b`
```
fcec137 fix(T-AUD-4b): overrides reach GASLab and OBDLab; SUPERCHARGED projects as TURBOCHARGED
```
