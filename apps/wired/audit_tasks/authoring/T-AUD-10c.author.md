# T-AUD-10c — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C5_20261017.md` F-C5-12 (and F-C5-9); `audit/scratch/C5/test_c5_probes.py::test_f12_ui_lab_import`.
Rehearsal: `C:/4DApp/recheck/T-AUD-10c/`.

### Verified context ###
1. **One lab import in the UI:** `grep -nE "^\s*(import|from)\s+(vinlab|gaslab|obdlab|dtclab|comlab|dnalab|symptomlab)\b" apps/ui/*.py`
   → only `apps/ui/app.py:330: import vinlab` on `cd6fbca`. `ui_payload.py` imports none. Observed.
2. **The composition decodes with `from vinlab import decode as decode_vin`** (`_diagnose`, the absent-triage branch;
   the triage branch goes through `dnalab.build_vehicle_dna`, which decodes with VINLab too). Observed.
3. **No UI test patches `vinlab`** (`grep -rn vinlab apps/ui/tests` → a comment only). Observed.
4. **Rehearsal** (restored): ui `68 → 70`; wired `110 → 113`; comlab `508 passed, 4 skipped` (equal); ruff clean;
   `2 files changed, 12 insertions(+), 4 deletions(-)`; base: wired test `3 failed`, ui test `2 failed`; mutant
   (`decode_vehicle` calls `vinlab.decode` directly) wired `1 failed, 2 passed`; probe `test_f12_` `1 passed`. Observed.

### Rulings and the tradeoff that lost ###
- **A thin `decode_vehicle` over the composition's `decode_vin`.** Lost: re-exporting `decode_vin` itself (a private
  alias of a lab function would become the UI's API; the wrapper names the contract and can change behind it).
- **The UI keeps its `try` / `except Exception`.** Lost: narrowing it to `VINDecodeError` (a behaviour change outside
  F-C5-12).
- F-C5-9's gating half is done (T-AUD-4o); this row closes the second decode path. Plan NONE, difficulty 1
  (mechanical, scripted). Code row: second-model review at acceptance.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `70 passed`; `113 passed` |
| step 2 | SIMULATED | `3 passed`; `2 passed`; base `3 failed` / `2 failed` |
| step 3 | SIMULATED | ruff `All checks passed!`; `2 files changed, 12 insertions(+), 4 deletions(-)` |
| step 4 | SIMULATED | `1 passed, 18 deselected` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-10c: the UI decodes the VIN through wired.composition.decode_vehicle; app.py imports no lab (F-C5-12).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 4) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R4 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
