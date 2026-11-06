# Result

## Status
completed

## Summary
Ran `recheck/T-AUD-12/apply_fix.py` from `repo/`. The six SymptomLab docs now state the code as it is. The 21-pair cap stays (R1). One commit on `fix/T-AUD-12`.

## Files changed
PRD, HLD, LLD, DLD, BDD and ADR under `labs/symptomlab/docs/`, plus the note and this RESULT.

## Commands executed
- First action, preconditions, census (before), `apply_fix.py`, Verification steps 1-3, `git add` (six paths), `git commit`.

## Validation evidence
- Census before: `stale 18`, `paths 5 missing 0`. After: `stale 0`, `paths 5 missing 0`.
- `cd labs/symptomlab && pytest -q -p no:cacheprovider`: `72 passed in 0.92s`.
- Changed lines equal those of `rehearsal.patch`.

## Criteria
1. MET: census prints `stale 0`, `paths 5 missing 0`.
2. MET: `72 passed`.
3. MET: commit 54edcd4 after spec fb02a79; `git status --porcelain` lists only the note (and this RESULT).

## Decisions the task did not specify
- The commit trailer went in a second `-m`, because bash_guard refused the single-command form.

## Pre-existing changes preserved
none present in `repo/` (porcelain was empty at the start).

## Rollback
`git -C repo reset` is not allowed here. Use `git revert 54edcd4` on `fix/T-AUD-12`, or `git restore` of the six docs from `fb02a79`.

## Remaining risks or uncertainties
Repo-wide gates (wired, ui, registry) NOT RUN; the task assigns them to Cowork. Docs-only change.

Branch: `fix/T-AUD-12`
Log (`71183a9..HEAD`):
54edcd4 docs(T-AUD-12): SymptomLab docs state the code as it is; 21-pair cap kept
fb02a79 spec(T-AUD-12): SymptomLab docs drift fixes; 21-pair cap kept
