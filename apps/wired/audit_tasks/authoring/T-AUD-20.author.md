# T-AUD-20 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: T-AUD-16 sidecar fact 3 (the cold-bucket probe); `GAS_VOCABULARY.md` §7. Rehearsal: `C:/4DApp/recheck/T-AUD-20/`
(`apply_fix.py`, `tests/test_cold_open_loop.py`, `rehearsal.patch`, `corpus_fix.json`). Canary of T-LOOP-18b: this
row's second review is the first product-row use of `ops/review_live.py`.

### Verified context ###
1. **Base (`fix/T-COMA-3c`):** `classify()` checks `CRANKING` first and has no cold check; with the cold bucket a
   normal reading returns `NORMAL_OPERATION` / `VALID` (no fault entry carries that operating state). Observed.
2. **Rehearsal:** new test base `3 failed, 1 passed`, fix `4 passed`; gaslab `215` → `219 passed, 2 skipped,
   4 deselected`; ruff clean; corpus `differ 0` of 314 against `T-COMA-3c/cw/corpus.json`; wired `106 passed`; census
   `notimpl 8`. Observed.
3. **Callers:** the UI sends `gas_engine_state` `STABILIZED_IDLE`; the composition sends `CRANKING` for
   `will_not_start`, else the gas form's value. Only a direct `gas_inputs.engine_state` reaches the cold state. Observed.
4. **Test coupling:** `test_contracts.py` pins the enum value and `len(EngineStateBucket) == 5`; neither changes. Observed.

### Rulings and the tradeoff that lost ###
- **R1 early return in `classify`.** Lost: a YAML validity gate keyed on the operating state (a new grammar key for one
  enum value).
- **R2 no reason field.** Lost: a `rejection_reason` payload field (no named consumer; the signal/noise rule).
- Code row: second-model review at acceptance. Plan NONE (rehearsed), difficulty 2: Sonnet medium.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `4 passed`; `219 passed, 2 skipped, 4 deselected`; ruff clean |
| step 2 | SIMULATED | `corpus 314`; `differ 0`; `106 passed`; `notimpl 8` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-20: GASLab rejects a COLD_OPEN_LOOP_INVALID sample as SAMPLE_INVALID / INVALID (GAS_VOCABULARY §7).

### Cold read ###
own pass 2026-11-07: P1-P4 measured (fact 2) · `apply_fix.py` exits on any literal count other than 1 · traceability: criteria 1-3 → steps 1-3 · 1c hits: R1 "Nothing else" = `rule_engine.py` only (Files to touch); criterion 3 "only" = note + RESULT · test coupling: `test_contracts.py` enum pins unchanged (fact 4) · no finding.
cold read 2026-11-07 FOCUSED reader; trigger 1c grep hit (R1 "Nothing else"); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
