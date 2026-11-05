TASK REVIEW — T-VINA-16_engine_ref_cylinder_count(5) — 2026-11-05 (Windows Cowork; plan correction 01, review correction 02)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 95) — second reviews (second_review.py, DeepSeek ds-flash): plan APPROVE WITH CORRECTIONS
(4 of 6 findings upheld, C1-C5); code APPROVE WITH CORRECTIONS (2 MEDIUM test gaps upheld and fixed in revision 02,
1 LOW not upheld); no code or data defect found

Branch fix/T-VINA-16 on fix/T-MERGE-1 (3c2d512): ledger 53a06db, spec d681469, correction 01 1bac3f3 + evidence
96d8a43, build 52b834f + 324fd5a, correction 02 daae97d, tests 84c5aa0. Implementer headless (opus xhigh), sessions
ebecaa08 (plan), 80112954 (build), 75d0e65d (revision 02).
t = 34 min (plan 12.4, build 15.6, revision 5.7; session_times.py). Score: −5 revision round (two rules without an
isolating test).

MECHANICAL GATE
  ✓ deliverables exist           build_vref_db.py DDL (R1); merge tool (guard, C2 refusal, rebuild, backfill, G2, report);
                                 decoder R3 (3 lines); vref.db 1,274 → 1,308 rows; banks file +8; merge file +14;
                                 note with ## Plan, round 2, Revision 02; RESULT with reach before/after and the R5 table
  ✓ changed files in scope       git diff 96d8a43..HEAD: the 6 Files-to-touch paths; no dnalab/wired/ui file;
                                 porcelain: note and RESULT only
  ✓ commits on the task branch   52b834f, 324fd5a, 84c5aa0 on fix/T-VINA-16
  ✓ tests                        reviewer re-run: vinlab `376 passed, 8 skipped`; two files `58 passed`; dnalab 27,
                                 wired 41, ui 30; comlab 526/4/2 (known R0-2, --continue-on-collection-errors), dtclab
                                 590, gaslab 208/2/4, obdlab 388/2, symptomlab 72 (all = base); ruff clean
  ✓ mutants (reviewer run)       R3 deleted: 6 failed (decoder file); `all` for `any` in the C2 refusal: 2 failed
                                 (has_maf, has_map cases); `_stated_counts` on the raw code: 1 failed. Both revision-02
                                 mutants survived at 324fd5a (second review F1, F2). RESULT table: 17 named mutants
  ✓ effect visible               reach row_applied 568 → 579, not_in_vref 483 → 468, out_of_window 68 → 72 (predicted);
                                 second merge run prints `inserted 0 rows; cylinder counts filled 0; engine_ref now 1308
                                 rows; schema rebuilt: no`, vref.db sha256 prefix 660e81961e887038 unchanged

INDEPENDENT DATA CHECK (Cowork, against `git show 3c2d512:…/vref.db` and `C:/4DApp/recheck/T-VINA-16/vref_rehearsal.db`)
  1,274 base rows: 0 changed outside cylinder_count, 0 missing. 34 new rows, equal field by field to the rehearsal db.
  cylinder_count equal to the rehearsal on all 1,308 rows (1,259 > 0, 49 NULL). PRAGMA integrity_check ok.

SECOND REVIEWS
  plan (`C:/4DApp/recheck/codex/T-VINA-16_plan_review.md`): F1 HIGH empty executemany rowcount −1 — not upheld
    (measured 0); F6 M11 kill — not upheld (AEB heuristic = 4); F2-F5 and the "0" truthiness — upheld → C1-C5.
  code (`C:/4DApp/recheck/codex/T-VINA-16_review.md`): F1 MED refusal test both sensors NOT NULL — upheld; F2 MED
    cross-spelling conflict untested — upheld; F3 LOW non-integral REAL count — not upheld (no path writes one).

CONCERNS (no change to this row)
  - 71 real VINs take TecDoc's count over the map's (ruling). Spot checks agree with the engines (AEB 4, NG 5, M52
    206S4 6, TU1 HFX 4, X10XE 3, S14 234EA 4, S62 508S1 8); the rest are listed in the RESULT.
  - vref.db 192,512 → 352,256 bytes: free pages from the rebuild plus 34 rows and a column (no VACUUM, by design of
    the idempotence check). Too small for a row.
  - 49 NULL-count rows keep the map count (T-VINA-11b); the builder's unstated sensors stay T-VINA-20's.

FOLLOW-UP ROWS: none new (T-VINA-11b and T-VINA-20 already in the ledger).
