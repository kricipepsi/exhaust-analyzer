# REVIEW T-VINA-7a — ACCEPT, score 100 (Windows Cowork, 2026-11-07)

Facts first: `fix/T-VINA-7a` on `fix/T-VINA-11c` `0552976`: spec `f621680` (with the T-VINA-7 split); build `fba4eb4`
(`closing()` on both `lookup_engine_ref` connections, the `open_vref_readonly` docstring, `wmi_brand_missing` → NONE
in `_compute_confidence`, vocabulary + HLD + `test_decoder.py` lines; one new test). The diff is byte-identical to
`C:/4DApp/recheck/T-VINA-7a/rehearsal.patch`; the test `cmp` equal. Porcelain: note and RESULT only.

## Gates re-run by Cowork
- vinlab `393 passed, 8 skipped` (base 389); wired `113`, ui `70`, dnalab `27`, comlab `508 passed, 4 skipped`
  (unchanged); ruff clean; C6 probes f9/f14 `3 passed` (base: `'PARTIAL' == 'NONE'`, three unclosed connections).
- R4 (note): base `4 failed, 57 passed, 2 skipped`; mutant (second connection unclosed) `1 failed, 60 passed,
  2 skipped`; restored, `cmp` identical.

## Second review
ds-flash APPROVE, 3 LOW (`C:/4DApp/recheck/codex/T-VINA-7a_review.md`; cites R1-R4 and the embedded test lines).
Not upheld (re-derived): #1 the miss case accepts `{}` (no path returns `{}`; `lookup_engine_ref` returns `None`);
#2 the §4 grade line "PARTIAL (any downgrade flag)" (the same wording already stood beside `engine_not_in_csv` →
NONE; the flag table is the authority); #3 the second lookup outside `catch_warnings` (the first call covers the
same paths).

## Score
100.

## Follow-up
T-VINA-7b (F-C6-7) and T-VINA-7c (F-C6-10) registered.
