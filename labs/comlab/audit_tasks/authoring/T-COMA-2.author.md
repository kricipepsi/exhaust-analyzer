# T-COMA-2 — authoring sidecar (Windows Cowork, 2026-11-06)

Scripts, patch and dumps: `C:/4DApp/recheck/T-COMA-2/`. Base: the accepted `fix/T-COMA-1` (`b81c50e`).

### Verified context ###
1. **The residual holds** on the base: a non-starter with no gas aborts with "not available yet"; the inbound schema
   requires `gas_lab_output` for every session (P1). Observed.
2. **Production gas readers** (grep `gas_lab_output` outside tests): the schema, the aggregator's two lambda detectors
   and `_build_sanitized_payload`, the composition. The v1 router, `power_loss_analytics` and `delta_engine` read gas
   only on flag-off paths (out of scope). Observed.
3. **Rehearsal** (`rehearsal.patch`, restored): P2-P5 hold; wired 79 → 85 after the R5 rewrite; comlab, registry, ui
   unchanged; the corpus dump equals T-COMA-1's (all 314 cases carry gas). Observed.
4. **UI help text** "Required for every run" (`ui_payload.py`) is pinned by `test_t_aud_1c.py`; R6 changes both.
   Observed.

### Rulings and the tradeoff that lost ###
- **Gas optional only for `will_not_start`**, enforced in the schema. Lost: plain `Optional` (simpler, but a running
  request without gas would then reach the detectors and crash, or score without chemistry).
- **Partial gas on a non-starter still aborts**, with the standard message. Lost: silently dropping a half-entered
  sample (a typing error would vanish).
- **No gas → both lambda detectors inert** (neutral results built directly). Lost: the de-cat configuration qualifier
  for a gasless non-starter (only emitted for de-cat with a secondary trim).
- **Plan NONE, difficulty 3** (`--model claude-sonnet-5-5 --effort medium`): every edit has its literal and a rehearsed
  patch; three mutants pin the new branches. Lost: the plan gate CLAUDE.md asks for risky rows (a contract
  relaxation); the schema check limits it to non-starters and the second review covers the code.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `rehearsal.patch`: new file `6 passed` (base `5 failed, 1 passed`); comlab `531 passed, 4 skipped, 2 errors`; mutants M1 2F, M2 1F, M3 3F |
| step 2 | SIMULATED | registry `5 failed, 502 passed, 4 deselected`; wired `85 passed` (with R5; `1 failed, 78 passed` without it); ui `38 passed` (with R6) |
| step 3 | SIMULATED | `probe.py` 9 lines as P2; corpus 314, equal to T-COMA-1's dump |
| step 4 | SIMULATED | ruff `All checks passed!` on the patched files and the test file (after `--fix` on its imports) |
| step 5 | DEFERRED | the observable: the spec commit then the implementer's commits on `fix/T-COMA-2`; status lists only the note and the RESULT |

### Exclusivity ###
No other implementer runs. T-AUD-4e and T-COMA-3 follow.

### Progress hook ###
T-COMA-2: a non-starter is diagnosed without gas readings; the schema keeps gas required for every other session.

### Cold read ###
own pass 2026-11-06: P1-P5 measured · literals found once (`    gas_lab_output: GasLabPayload`, `"gas_lab_output":
request.gas_lab_output.model_dump(),`, `"Non-start diagnosis without exhaust gas readings is not available yet. "`,
`Required for every run:`, `def test_r4_non_starter_without_gas_aborts_with_message`) · counts: wired 79 + 6 = 85 ·
traceability: criteria 1-4 → steps 1-5 · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit ("all five", "only" in R3/R1); 0 findings, 0 patched; 1
unsettled (the v1 router reads gas; Out of scope names it; no test runs a gasless request with the flag off) — 3 calls.

### Correction history ###
(none)
