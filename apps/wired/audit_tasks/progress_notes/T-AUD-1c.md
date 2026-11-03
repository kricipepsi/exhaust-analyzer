# T-AUD-1c progress note

## Readiness
(a) Starting state matches: branch `fix/T-AUD-1c`, base `f4f8fc1`, `git status --porcelain` empty; preconditions printed `checked`.
(b) New test file run on the base: `test_r1_pending_only_requires_ff` fails because the 12 `ff_*` keys are absent from the issues (only gas keys reported). Intended reason.
(c) Decisive expected value: `apps/ui/tests` 24 base + 6 new = 30 passed; derived from the task's P1 and the six listed tests.
(d) No contradiction found; every cited anchor resolved (`if confirmed:` ui_payload.py:950, `"gas_module": FieldHelp(` :139, composition.py:241).
(e) Deliverable: R1 makes the 12 freeze-frame fields required whenever the payload has a `dtc` dict, R2 names GASLab in the gas message and help. Decisive check: `apps/ui/tests` shows `30 passed` with P2/P3/P4 colours unchanged.

## Assumptions worked past
- The shell test file imports `from wired import diagnose` directly (apps/ui tests run with wired installed in the venv).
- The commit carries no attribution trailer: `bash_guard` refused any command whose text names the assistant. The commit message follows AGENTS.md.
- Also reworded the `validate_widgets` docstring line ("A confirmed code" -> "Any DTC data") in `ui_payload.py`, so the docstring matches R1.
- `diagnose()` returns a pydantic object, so the R2 test reads `result.diagnostic_verdict.fault_code` / `.actionable_remediation`.

## VERIFICATION GATE
CLEAN. Step 1 `30 passed`; step 2 `9 passed`; step 3 C1 `42 failed, 2 passed`, C4 `9 failed, 3 passed`, C5 `13 failed, 6 passed`; step 4 `36 passed`; step 5 `All checks passed!`; step 6 one commit (e37bf50). Pyright (report-only) `0 errors, 0 warnings`.

## CODE REVIEW
Scope: only the 3 touched `.py` files plus the note and RESULT. Contracts: no new field or key. The R1 predicate `"dtc" in payload` is the same payload `build_diagnose_payload` builds, so UI and engine cannot drift. `split_dtc_tokens` is still used by the other `dtc_module` checks (no orphan import). No findings.

## Time
phase | start | end | minutes | context at end
all | 2026-11-03T07:00:24Z | 2026-11-03T07:05:30Z | 5 | ABSENT
