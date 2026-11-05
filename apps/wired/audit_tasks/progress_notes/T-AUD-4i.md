# T-AUD-4i progress note

## Readiness
(a) Starting state matches: branch `fix/T-AUD-4i`, HEAD `d9aa5c4` (spec commit, descendant of 916df88), `git status --porcelain` empty, preconditions print `checked`.
(b) The new test fails on the base for the intended reason: the AFR branch sends the raw value (P4: `3 failed, 1 passed`); confirmed in the red run below.
(c) Expected values derived independently: 14.7/14.7 = 1.0; 10.0/14.7 = 0.68027 -> 0.6803; 20.0/14.7 = 1.36054 -> 1.3605.
(d) No contradiction or missing decision: `ui_payload.py:1103-1104` holds the combined branch; the constant goes beside line 74.
(e) Teach-back: split the WIDEBAND_AFR branch so the typed AFR is divided by a new constant 14.7 and rounded to 4 places, leaving WIDEBAND_LAMBDA unchanged. The decisive check is the new test file (4 passed, mutant 3 failed) and `rehearse.py` printing `sent` equal to `lambda` on every line.

## Assumptions worked past
- The commit trailer from the session attribution rule was refused by `bash_guard` (nested-launch text match), so the commit carries no trailer (AGENTS.md form).
- A hook reported F-821 between the two ui_payload edits; the constant edit followed immediately, ruff is clean at the end.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action to commit | 2026-11-05T17:09:27Z | 2026-11-05T17:13:00Z | 3.6 | ABSENT |

## Red run
`tests/test_t_aud_4i_afr.py` on the base: `3 failed, 1 passed` (matches P4).

## VERIFICATION GATE
CLEAN. New file `4 passed`; ui `34 passed`; wired `62 passed`; rehearse.py `sent` equals `lambda` on all 3 lines; ruff `All checks passed!`; mutant (AFR branch sends raw value) `3 failed, 1 passed`, restored then `4 passed`.

## CODE REVIEW
Scope: only ui_payload.py (constant + split branch) and the new test. Provenance: the constant carries a comment citing the 14.7 petrol scale. Anti-orphan: `WIDEBAND_AFR_STOICH` is read in the AFR branch. No findings.
