# T-COMA-28 progress note

## Readiness challenge
- (a) Starting state matches: `git branch --show-current` = `fix/T-COMA-28`; `git log --oneline 3cd8541..HEAD` = `a80b5f2 coma: spec(T-COMA-28): ...` (one spec commit); `git status --porcelain` empty. Preconditions: `checked`, no `MISSING`.
- (b) Test fails for the intended reason: the staged new test on the base gives `3 failed, 3 passed`; the failures are `[CAM_TIMING_ADVANCED]`, `[TIMING_RETARDED]` (LC-002 or MF-005 fire with no chemistry) and `test_gating_tiers` (the tiers are still DEFINITIVE).
- (c) Independent expected value: with GATING (no +0.10 DEFINITIVE bonus) plus base +0.10, a rule that has its chemistry scores the same: 0.81+0.10 = 0.91 (LC-002), 0.75+0.10 = 0.85 (MF-005). Comlab count is 563 + 6 new cases = 569, which matches P2.
- (d) No contradiction prevents work. One soft STALE-ANCHOR: R4 says 8 cases, the staged file has 6 (see `T-COMA-28.blocker.json`).
- (e) Teach-back: run `rehearse.py` to make the 12 edits (LC-002 and MF-005 chemistry become GATING with base +0.10, three test hardenings, the new test and four re-stated pins), then commit them as one commit on `fix/T-COMA-28`. The decisive check is the C1 probe printing `LC-002 score: None MF-005 score: None` and the corpus family accuracy rising from 216 to 221 of 314.

## Assumptions worked past
- R4 says "8 cases". I used the staged file (6 cases) unchanged and judged it against P2's counts, which agree with 6.
- `T-COMA-28.blocker.json` is an untracked third file. The header authorises it, so step 5 porcelain lists it beside the note and the RESULT.

## Implementation
`$PY -I C:/4DApp/recheck/T-COMA-28/rehearse.py` printed `applied 12 edits` (exit 0). I read the diff: it matches R2-R5. The copied new test is byte-identical to the staged file (`git diff --no-index` exit 0). Commit `9a32ea6` on `fix/T-COMA-28`.

## VERIFICATION GATE
| step | expected | observed |
|---|---|---|
| 1 comlab / wired / ui | 569 / 186 / 75 passed | `569 passed in 10.76s` / `186 passed in 8.22s` / `75 passed in 5.16s` |
| 2 registry / targeted | `508 passed, 5 skipped` / `29 passed` | `508 passed, 5 skipped in 2.13s` / `29 passed in 2.10s`; case_library.html restored |
| 3 C1 probe | `LC-002 score: None MF-005 score: None map_kpa: 35.0`; `1 failed, 13 passed, 2 deselected` | identical; the one failure is `test_every_chemical_signature_has_a_v2_rule` (`FLAT_CAMSHAFT`, `INCOMPLETE_OXIDATION`, out of scope) |
| 4 corpus | `changed 32 of 314`, `family accuracy 221 of 314 (before 216)`, `gained 9 lost 4` | identical |
| 5 ruff / stat / log / status | `All checks passed!`; `9 files changed, 77 insertions(+), 13 deletions(-)`; spec + one commit; note + RESULT | identical; porcelain also lists the header-authorised `T-COMA-28.blocker.json` |

Absence of the earlier decisive failure: before the edits, the new test gave `3 failed, 3 passed` (LC-002 or MF-005 fired on CAM_TIMING_ADVANCED and TIMING_RETARDED). After the edits it passes inside the `29 passed`.

## CODE REVIEW
- JSON: only the tier, base weight and description of LC-002 and MF-005 changed. TIMING_RETARDED on LC-002 stays SUGGESTIVE (R2). No other rule was touched.
- Tests: no assertion was weakened. The four re-stated pins (R5) now assert the chemistry-correct outcome, and T-COMA-6 gains an assertion (LC-002 attributed to `("chemistry", "gas_lab_state")`).
- The R3 hardenings narrow the skip to one ID and pin tier `GATING` and base 0.9.
- Findings: none.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| whole session (precheck, edits, verification, commit) | 2026-11-13T19:44:01Z | 2026-11-13T19:46:31Z | 2.5 | ABSENT (no context meter is exposed to this session) |

The minutes are computed from the `date -u` reads. The wall time covered by these reads looks short for the work that was done. The figure is reported as measured.
