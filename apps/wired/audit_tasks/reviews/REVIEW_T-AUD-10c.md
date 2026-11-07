# REVIEW T-AUD-10c — ACCEPT, score 100 (Windows Cowork, 2026-11-07)

Facts first: `fix/T-AUD-10c` on `fix/T-AUD-10e` `cd6fbca`: spec `545746c`; build `7101cb4`
(`wired.composition.decode_vehicle`, `app.py` calls it; two tests). The source diff is byte-identical to
`C:/4DApp/recheck/T-AUD-10c/rehearsal.patch`; both tests `cmp` equal to Cowork's copies. `git log cd6fbca..HEAD`:
the spec and the build. Porcelain: note and RESULT only.

## Gates re-run by Cowork
- ui `70 passed` (base 68); wired `113 passed` (base 110); comlab `508 passed, 4 skipped` (unchanged); ruff clean;
  `2 files changed, 12 insertions(+), 4 deletions(-)`; audit probe `test_f12_ui_lab_import` `1 passed`
  (base: `lab imports in apps/ui/app.py: ['vinlab']`).
- R4 (note): base wired `3 failed`, ui `2 failed`; mutant (`decode_vehicle` calls `vinlab.decode` directly) wired
  `1 failed, 2 passed`; restored by hand, diff stat back to 12/4.

## Second review
ds-flash APPROVE, 3 LOW (`C:/4DApp/recheck/codex/T-AUD-10c_review.md`; cites the embedded hunks). Not upheld
(re-derived): #1 the tag "fails on the base fix/T-AUD-10e" is correct (`cd6fbca` is that branch's tip); #2 the
`\b<lab>\.` assertion is strict on purpose (an attribute use of a lab is the same boundary breach); #3 the commit
count and porcelain were measured by Cowork (above), not shown by a two-endpoint diff.

## Score
100.

## Follow-up
None. F-C5-12 closed; F-C5-9's gating half was T-AUD-4o.
