# T-AUD-4j progress note

## Readiness
(a) Starting state matches: branch `fix/T-AUD-4j`, HEAD `8b12cd9` (spec commit, descendant of 5cfcdc4), `git status --porcelain` empty, preconditions print `checked`.
(b) The new tests fail on the base: the UI sends `blue_smoke_on_cold_start_clears`, and `composition.diagnose` sets `symptom_dna = {}` on `VINDecodeError` (confirmed in the red run below).
(c) Expected values from the prior and the corpus (P2): rough idle / shudder -> `running_rough`; prolonged crank + will_not_start -> `non_starter`; prolonged crank + running -> `hard_start_cold`; won't start, cold only, `UNKNOWNVIN0000000` -> `suppress_gaslab` and `cold_start_mode` True.
(d) No contradiction or missing decision: `ui_payload.py:1000-1002` holds the old tag; `composition.py:144-146` holds the `VINDecodeError` branch.
(e) Teach-back: the UI helper `_csv_primary_symptom` maps tier pairs to prior keys, and `_symptom_without_vin` keeps the resolved triage when the VIN fails. The decisive check is the two new test files (4 and 3 passed, each mutant fails) and `tag_rehearse.py` / `census.py` showing `changed 0` / `changes {}`.

## Assumptions worked past
- `apply_fix.py` is the shape for the helpers and tests; I write the files by hand and check them against the real code.

## Red run
Before the edit: `test_t_aud_4j_symptom_tag.py` `4 failed` (tag was None/blue-smoke); `test_t_aud_4j_symptom_without_vin.py` collection ImportError on `_symptom_without_vin`.

## Mutants (R4)
- `symptom_dna = {}` restored on `VINDecodeError`: `test_routing_applies_without_a_decodable_vin` fails (1 failed, 2 passed).
- rough-idle tag back to a non-prior key: `test_tier_pair_tag[…Rough Idle…running_rough]` fails, and `test_every_ui_tag_is_a_prior_key` fails too (2 failed, 2 passed). I used `blue_smoke_on_cold_start_clears`.
Both files restored from a copy; `git diff --stat` unchanged afterwards.

## VERIFICATION GATE
CLEAN. Step 1: 4 passed; 3 passed; ui 38 passed; wired 65 passed. Step 2: comlab `526 passed, 4 skipped, 2 errors` (P4). Step 4: `[base] changed 17`, `[fixed] changed 0`, `cases 64; fixed tag equals corpus tag in 62`; probe `1 passed, 18 deselected`; census `changes {} of 314`. Step 5: ruff `All checks passed!`. pyright, `--select S`, isolation and baseline.sh: NOT RUN (not in the task's Verification).

## CODE REVIEW
Scope: only the four files in Files to touch changed. Contracts: both helpers carry a `# consumer:` comment. Boundaries: no cross-lab import added. No numeric literals added. No findings.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action to commit | 2026-11-05T17:34:54Z | 2026-11-05T17:37:33Z | 2.6 | ABSENT |
