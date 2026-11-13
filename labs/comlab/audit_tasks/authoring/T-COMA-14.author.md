# T-COMA-14 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-21 and F-C1-6; `labs/comlab/registry/integration_shim.py`
(`_PID_DISPATCH`, `_audit_pid_coverage`); `labs/comlab/registry/rules/rich_mixture.json` (RM-004);
`labs/comlab/comlab/schemas/ingestion.py`. Rehearsal: `C:/4DApp/recheck/T-COMA-14/`.

### Verified context ###
1. **Still open on `e531528`:** `"fuel_pressure": (("ff", "fuel_pressure_kpa"),)`; FreezeFrameRecord has no
   `fuel_pressure_kpa`. Nothing else in `labs` or `apps` references the PID. RM-004 (GDI HPFP seal leak) uses it as
   `lt 3000 kPa`, SUGGESTIVE. `obd.fuel_rail_pressure_load_kpa` exists (wired fills it), but RM-004's `gdi_equipped`
   precondition is never read (F-C1-6). Observed.
2. **Rehearsal** (restored): new test `3 passed`, base `2 failed, 1 passed`; mutant (dispatch line back) `1 failed`;
   comlab `510 passed, 4 skipped` (equal); wired `167 → 170`; ui `70`; corpus `changed 0 of 314`; ruff clean;
   `2 files changed, 9 deletions(-)` plus the 39-line test. The audit probe `test_fuel_pressure_pid_resolvable`
   raises `KeyError` after R1 (it indexes the removed key). Observed.

### Rulings and the tradeoff that lost ###
- **Remove the dead row.** Lost: remapping to `fuel_rail_pressure_load_kpa`. That revives a GDI-only row on every car
  while the GDI precondition is unread. On a non-NORMAL gas reading (the permissive predicate), one satisfied row
  fires RM-004, so a port-injected car at about 350 kPa would get a GDI pump fault. F-C1-6 can reintroduce the row
  behind the gate.
- **The test checks every dispatch field against its schema** (obd and freeze frame), not only this PID. Lost: a
  one-key test.
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `510 passed, 4 skipped`; `170 passed`; `70 passed` |
| step 2 | SIMULATED | `3 passed`; base `2 failed, 1 passed` |
| step 3 | SIMULATED | `0` and `0` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `3 files changed, 39 insertions(+), 9 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-14: the dead fuel_pressure PID and RM-004's row on it are removed (F-C1-21).

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 2) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-5 and R3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
