# REVIEW T-VINA-7b — ACCEPT, score 98 (Windows Cowork, 2026-11-07)

Facts first: `fix/T-VINA-7b` on `fix/T-VINA-7c` `14f9956`: spec `05acf42`; build `13d0492` (`_NA_REGION_CODES`,
`_is_non_na_region`, the union bypass in `validate_vin_checksum`, wiki 10 §10.3 rows 1 and 3; one new test). The diff
is byte-identical to `C:/4DApp/recheck/T-VINA-7b/rehearsal.patch`; the test `cmp` equal. Porcelain: note and RESULT.

## Gates re-run by Cowork
- vinlab `403 passed, 8 skipped` (base 393); wired `113`, ui `70`, dnalab `27`, comlab `508 passed, 4 skipped`
  (unchanged); ruff clean; `2 files changed, 17 insertions(+), 5 deletions(-)`.
- R3 (note): base `6 failed, 61 passed, 2 skipped`; mutant (country bypass dropped) `1 failed, 66 passed,
  2 skipped`. Cowork's rehearsal mutants (region 1-4, dummy bypass dropped): each killed.
- Registry (750,354 unique petrol VINs): the patched decoder rejects 128 (was 10,334), census flips `{}`.

## Second review
ds-flash APPROVE WITH CORRECTIONS, 1 LOW (`C:/4DApp/recheck/codex/T-VINA-7b_review.md`): the new comment lists "UK"
among countries absent from the sets, but `_EUROPEAN_COUNTRIES` has `"UNITED KINGDOM"`. Re-derived: not upheld as a
defect. The comment means the `wmi.csv` spellings `UNITED KINGDOM (UK)` (44 WMIs) and `ENGLAND` (9), which are not in
the set (audit F-C6-7 census). The wording is loose; it is Cowork's own text, so the score carries it instead of a
revision for one comment.

## Score
100 − 2 (an imprecise comment in Cowork's scripted edit) = 98.

## Follow-up
`3N1` (Nissan Mexico) is 95 of the 128 still rejected and fails today too: a possible OPSI corrupt prefix (ledger
note on T-VINA-7b). The audit probe `test_f7_na_vin_with_bad_check_digit_rejected` stays failing by ruling.
