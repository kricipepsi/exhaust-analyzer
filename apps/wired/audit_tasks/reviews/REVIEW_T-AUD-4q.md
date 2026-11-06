# REVIEW T-AUD-4q — ACCEPT, score 99 (Windows Cowork, 2026-11-06 15:47 CET)

Branch `fix/T-AUD-4q`: spec `f7e1f74` (+ `8d6e8c7`), build `0e0f209`, revision 02 spec `d754f0d`..`c8ecba9`, build
`3609e12`. F-D2-10/11 fixed by retirement: COMLab's DNA projector (`projection.py`, `schemas/lab_dna_views.py`) had no
production caller and is gone; COMLab's design docs, the proposals registry and the three lab view docstrings name the
composition's `_build_*_dna_view` as each view's builder.

## Facts re-derived by Cowork (before the RESULT)
- Build `0e0f209` equals the rehearsal patch (826 of 826 changed lines); revision 02 equals `apply_rev02.py` plus the
  rehearsed test file (byte-identical after line endings).
- On `3609e12`: new file `3 passed`; comlab `503 passed, 4 skipped, 2 errors` (525 − 25 + 3); on `0e0f209`: registry
  5F/502P, gaslab 208, obdlab 391, dtclab 590, vinlab 376, dnalab 27, symptomlab 72, wired 101, ui 52 (all = base);
  corpus 314, 0 differ; ruff clean. Revision 02 touches one doc row and the test file only.

## Second review
ds-flash, APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-AUD-4q_review.md`).
- BLOCKER 2 upheld: the DEP-4 row's last cell still sent readers to `projection.py:79–81` as `pending — runnable`
  (Cowork's `apply_fix.py` edited only the reconcile cell). Revision 02 (R6) fixed it and added a guard test.
- BLOCKER 1 not upheld: COMLab-E is a `proposed` entry; its old consumer lacked `fuel_type` too.
- CONCERN (tests scan few docs): folded into revision 02. CONCERN (criterion 4 not in the prompt): settled by Cowork's
  ruff and status run. NITs (consumer_path wording, a second audit-probe importer): too small.
- The DELTA cold read of revision 02 found the resumed run's start state unstated; patched before the resume.

## Score
100 − 1 (`## Time` minutes written "see timestamps", not a figure; stamps give 2 min) = 99. The revision was a
Cowork spec defect, not the implementer's. Time: 2 min + revision.

## Successors
T-AUD-4u registered (projector mentions in other labs' docs and wikis). Queue: T-AUD-4r, T-COMA-3.
