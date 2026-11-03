# T-AUD-1c — authoring sidecar (Windows Cowork, 2026-11-03)

### Verified context ###
1. **Base:** `audit-r2` fast-forwarded to `d1fe367` (T-AUD-1a accepted; `origin/audit-r2` = `d1fe367`). The spec
   commit lands on top; `fix/T-AUD-1c` is cut from it.
2. **ID:** the audit `id_pattern` (`^T-[A-Z0-9]+-\d+[a-z]?(?:-(?:[0-9]+[a-z]?|orig))?$`) rejects `T-AUD-1a-c` and
   `T-AUD-1a-b`, so 018's names became `T-AUD-1c` and `T-AUD-1d` (reported in the next channel message).
3. **R1 rehearsed on the base** (`if confirmed:` → `if "dtc" in payload:` in a scratch edit, restored): `apps/ui/tests`
   `24 passed`; C5 `13 failed, 6 passed` with the same 6 PASSED node ids as the T-AUD-1a review run.
4. **No pins on the texts R2 changes:** `grep -rn "Enables tailpipe exhaust\|Low-idle gas readings"` over `apps`,
   `labs/comlab`, `audit` → only the two source sites; the wired tests check codes and field names, not prose.
5. **DTCLab freeze frame:** `labs/dtclab/dtclab/core/data_fusion_sanitizer.py` calls `extract_freeze_frame` (2 hits).
6. **Pins on the base `d1fe367`** (T-AUD-1a review, 2026-11-03): UI `24 passed`; 9 probes `9 passed`; C1 42/2, C4
   9/3, C5 13/6; wired `36 passed` with `--basetemp`; ruff `All checks passed!`; pyright `0 errors` on the two files.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | asserts `30 passed`; the new file does not exist (base `24 passed`) |
| step 2 | RAN | `9 passed in 7.22s` (T-AUD-1a review, same code) |
| step 3 | RAN | C1 `42 failed, 2 passed`; C4 `9 failed, 3 passed`; C5 `13 failed, 6 passed` |
| step 4 | RAN | `36 passed` (baseline.sh with basetemp) |
| step 5 | RAN | `All checks passed!` on the two source files |
| step 6 | DEFERRED | asserts 1 commit; none before the row |

### Exclusivity ###
None: T-AUD-1a and T-LOOP-3 are closed; no other implementer runs.

### Progress hook ###
T-AUD-1c: check FF is required for pending/MIL/Mode 06-only forms and the gas message names GASLab.

### Cold read ###
own pass 2026-11-03: literals ok (9 anchors, each `grep -cF` = 1) · rule rehearsal through the real functions on
the base: pending-only, MIL-only and Mode 06-only forms send a DTC dict with 0 `ff_` issues (the three NEW tests are
red); nothing typed sends no DTC dict (the PIN holds); GASLab unticked → `GAS_INPUT_INCOMPLETE`, remediation "Low-idle
gas readings are incomplete. Enter: hc, co, co2, o2, nox." (NEW red) · counts: 6 tests enumerated, `24 + 6 = 30 passed`
· traceability: criteria 1-2 → step 1, 3 → steps 2-4, 4 → step 6; every CREATE/MODIFY → a deliverable · check 19
PATCHED (`018` restated, cut to one mention) · JUDGEMENT criteria: 0.
cold read 2026-11-03 FOCUSED reader; trigger grep hit (rulings); 0 findings, 0 patched, 0 not-a-conflict. Its one
UNSETTLED item (GASLab unticked returns GAS_INPUT_INCOMPLETE) settled by the own-pass rehearsal above.
