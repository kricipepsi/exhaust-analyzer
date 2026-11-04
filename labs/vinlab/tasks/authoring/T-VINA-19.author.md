# T-VINA-19 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. Source: T-VINA-12's second code review (`recheck/codex/T-VINA-12_review.md`), re-derived in
   `reviews/REVIEW_T-VINA-12.md`: the MEDIUM (17-char mutant survives on a 2:2 tie) and the LOW (U+FFFD brands counted).
2. Rehearsed (`recheck/T-VINA-19/rehearse.sh` on a copy of `fix/T-VINA-12`): new file `9 passed`; M1 and M2 each
   `1 failed`; the new test on the base tool `1 failed`; vinlab `344 passed, 8 skipped`; ruff clean.

### Rulings and the tradeoff that lost ###
- Skip U+FFFD brands. Lost: a strict decode (`errors="strict"`), which would stop the whole registry read on one byte.
- A small row, not a second return on T-VINA-12. Lost: fixing inside T-VINA-12 (its one return was spent at the plan).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | copy: `344 passed, 8 skipped` |
| step 2 | SIMULATED | copy: `9 passed`; M1, M2 `1 failed` |
| step 3 | SIMULATED (ruff) / DEFERRED (commit) | `All checks passed!` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-VINA-12` (`8aeed6a`).

### Progress hook ###
T-VINA-19: _registry_majority skips U+FFFD brands; its test kills the 17-char and U+FFFD mutants.

### Cold read ###
cold read: not triggered (difficulty 1; rulings are verbatim edits, rehearsed with mutants).

### Correction history ###
