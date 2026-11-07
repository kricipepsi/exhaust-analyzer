# REVIEW T-VINA-11c — ACCEPT, score 100 (Windows Cowork, 2026-11-07)

Facts first: `fix/T-VINA-11c` = `fix/T-AUD-10c` `76feb81` + merged `fix/T-VINA-6` (`0f5f570`); spec `68b86c3`;
build `f005a0d` (`_WEAK_SHARE_FLOOR`, `_weak_share`, the weak-row drop after H1, the `engine_not_in_csv` guard, one
vocabulary row; two test files). The source diff is byte-identical to `C:/4DApp/recheck/T-VINA-11c/rehearsal.patch`;
both tests `cmp` equal to Cowork's copies. Porcelain: note and RESULT only.

## Gates re-run by Cowork
- vinlab `389 passed, 8 skipped` (base 381); wired `113`, ui `70`, dnalab `27`, comlab `508 passed, 4 skipped`
  (all unchanged); ruff clean; `2 files changed, 20 insertions(+), 3 deletions(-)`.
- R4 (note): base decoder `8 failed, 17 passed`; mutant (weak graded NONE) `2 failed, 23 passed`; restored, stat
  back to 20/3. Cowork's rehearsal mutants (`<=` floor, floor before H1): each killed.
- Evidence for the floor: held-out Nio file 3, share < 0.50: 39,867 petrol VINs, engine code 0.336, displacement
  0.497 (`recheck/T-VINA-11c/heldout_disp.py`).

## Second review
ds-flash APPROVE, 1 LOW (`C:/4DApp/recheck/codex/T-VINA-11c_review.md`; cites R1, R2, P2, P4). Not upheld
(re-derived): #1 a `None` share needs a short CSV row (`awk -F, 'NR>1 && NF<9'` → 0 rows), and `_resolve_engine`
calls `.strip()` on the same field first, so `_weak_share` cannot meet one.

## Score
100.

## Follow-up
T-VINA-11b keeps the 12602 key and the RGX keys. The HLD/DLD flag lists do not name `vds_engine_weak` (the vocabulary
does): too small for a row; the next VINLab docs row picks it up.
