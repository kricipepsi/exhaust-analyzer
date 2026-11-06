# T-AUD-4n progress note

## Readiness
(a) Start matches: branch fix/T-AUD-4n, HEAD dd6aa13 (spec commit, descendant of d10bb93), `git status --porcelain` empty, preconditions print `checked`.
(b) New test file on base: `4 failed in 2.26s`, each for the intended reason (widgets, payload key, FIELD_HELP entries still present).
(c) Expected: new file 4 passed, ui 45 passed (41+4), wired 85 passed, grep count 0; mutant (lambda_2500 back in float tuple) fails test_payload_sends_no_lambda_2500.
(d) No contradiction: the grep hits in app.py/ui_payload.py/test_ui.py are exactly the lines the patch deletes; `git apply --check` passes.
(e) Deliverable: delete the Fuel Blend, Mileage and High Idle measured-lambda inputs with their payload and help entries, and add the 4 tests. Decisive check: new file `4 passed` (was `4 failed`), ui `45 passed`, grep `0`.

## Assumptions worked past
- The rehearsed test file has CRLF endings; copied byte-for-byte (rule: keep line endings).
- The commit with the attribution trailer was refused by bash_guard (nested-launch rule); recommitted without the trailer.

## Mutant
`"lambda_2500"` put back into the high-idle float tuple: `1 failed, 3 passed`; failing test `test_payload_sends_no_lambda_2500`. Reverted (diff shows tuple without it).

## VERIFICATION GATE
1 new file `4 passed` (base `4 failed`); ui `45 passed`. 2 wired `85 passed`. 3 grep count `0`. 4 ruff `All checks passed!`.

## CODE REVIEW
Diff = rehearsal.patch (R1-R3) plus the R4 file; every line traces to Files to touch. No new field, so no anti-orphan item. Clean.

## Time
phase | start | end | minutes | context at end
all | 2026-11-06T09:18:27Z | 2026-11-06T09:19:37Z | 1 (date -u diff 70 s) | ABSENT
