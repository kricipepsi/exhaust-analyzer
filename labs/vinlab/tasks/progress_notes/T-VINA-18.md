# T-VINA-18 progress note

## Readiness
- (a) Starting state matches: branch `fix/T-VINA-18`, HEAD 65dfb7a `spec(T-VINA-18)`, `git status --porcelain` empty; preconditions print `1`, no MISSING.
- (b) Docs row, no test. Decisive check is Verification step 1; on the base it prints the stale sites (sed of the pinned lines shows 18-pair / `len == 18` / `**18**` / `len==18`).
- (c) Expected value 21: `grep -c "len(self._allowed) != 21" labs/symptomlab/symptomlab/validator.py` printed 1.
- (d) No blocking contradiction. One soft note below.
- (e) Teach-back: change four live "18" catalog-size statements to 21 on lines 191 / 147-148 / 160 / 185 and commit on `fix/T-VINA-18`. Step 1 must print nothing and step 2 must print a count of 1 or more for each file.

## Assumptions worked past
- Context says `(catalog reconciled by T-DNA-8)` becomes `(ADR-0008)`. In DLD that phrase spans lines 148-149 (`by T-DNA-8), so these tests ...` is line 149), but Files to touch allows lines 147-148 only. I stayed in scope: line 148 now reads `... invariant (ADR-0008; catalog reconciled` and line 149 is untouched (`by T-DNA-8), so ...`). Reviewer can switch to the literal wording by editing line 149 if wanted. No blocker record written: no edit was blocked.

## Time
phase | start | end | minutes | context at end
all | 2026-11-04T18:24:18Z | 2026-11-04T18:25:04Z | under 1 (clock read at start and finish only) | ABSENT

## VERIFICATION GATE
CLEAN: steps 1-4 as in the RESULT. No .py file touched, so ruff/pyright/pytest are NOT RUN (docs only).

## CODE REVIEW
CLEAN: 5 lines changed in 4 files, all on the pinned sites. The one wording deviation is under Assumptions worked past.
