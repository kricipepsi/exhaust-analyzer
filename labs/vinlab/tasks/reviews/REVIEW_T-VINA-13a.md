TASK REVIEW — T-VINA-13a_tecdoc_1q2019_extract(4) — 2026-11-04 (Windows Cowork; plan correction 01, review correction 02)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT WITH NOTES   (score 89) — second review (second_review.py, off-peak → ds-pro) APPROVE WITH
CORRECTIONS: 6 findings, 2 upheld and fixed in revision 02, 2 nits, 2 not upheld

Branch fix/T-VINA-13a on fix/T-VINA-5: spec e320768, correction 01 f0e26bb, build f836bcf, correction 02 6316a28 +
7b87192, tests aa7cdbf. Implementer impl-T-VINA-13a, PID 9108, t=18 min (8 plan + 8 build + 2 revision). Score: −5
revision round (two rules without a killing test; my plan approval let them through), −3 ×2 nits (N1, N2).

MECHANICAL GATE
  ✓ deliverables exist           tool (stdlib), CSV 1,498 rows, test file (13), note with ## Plan, round 2 and
                                 Revision 02, RESULT with the R6 report
  ✓ changed files in scope       git diff 7ba9368..HEAD: the 3 Files-to-touch paths + spec commits; porcelain: note,
                                 RESULT
  ✓ commits on the task branch   f836bcf, aa7cdbf: `git branch --contains` → fix/T-VINA-13a only
  ✓ tests                        reviewer re-run: vinlab `261 passed, 8 skipped`; new file `13 passed`; dnalab 27,
                                 wired 41, ui 30; ruff clean
  ✓ red                          tool moved aside: `11 errors` (before revision 02)
  ✓ mutants (reviewer run)       implementer M7 (closed-end max) 1 failed, M11 (petrol first) 3 failed; Cowork F2
                                 (whole-part key dropped) 2 failed, F3 (blanks ignored) 1 failed, after revision 02
  ✓ effect visible               fresh real run byte-identical (`identical`); coverage.py real VINs 642 of 1,115
                                 (vref.db today 18)

INDEPENDENT DATA CHECK
  Plan-time re-derivation on the SQLite snapshot (vina13_alias.py): 1,503 petrol rows before C1, 1,498 after
  (5 all-digit pairs). 40 random OK rows against the snapshot (capacity, my_start, my_end with open ends, n_cars,
  petrol EngineType): 0 mismatches.

SECOND REVIEW (ds-pro, embedded 49 KB; out C:/4DApp/recheck/codex/T-VINA-13a_review.md)
  F1 (HIGH) T0A 118 impossible with a 4-entry alias table: NOT UPHELD. P4 groups misses by the full manufacturer set
     (VW appears in several groups); re-derived 118 with the same 4 aliases (the plan review's F8, same misreading).
  F2 (MED) whole-part key untested: UPHELD. Cowork mutant F2 passed 11/11 and changed 7 real rows → revision 02 test.
  F3 (MED) blank-as-value ambiguity untested: UPHELD. Mutant F3 passed 11/11 and changed 10 real rows' status →
     revision 02 test.
  F4 (LOW) Euro4/Euro5, EEV blanked without counts in the report: N1 (the plan's counts exist; the RESULT omits them)
     → T-VINA-13b needs the euro fallback anyway.
  F5 (LOW) fill rates not printed for the 7 key columns: NOT UPHELD (100% by construction; the RESULT states them).
  F6 (LOW) the final rows.sort is redundant with the sorted loop: N2.

FOR T-VINA-13b (from the RESULT, accepted as disclosed)
  44 codes appear under more than one brand with different fields (vref.db is keyed by code only); my_end open on
  36%; euro_norm 7.6%; induction 75%; 34 FAMILY and 42 AMBIGUOUS rows; years are calendar (production) years.
  JV aliases (AUDI→AUDIFAW 5, NISSAN→NISSANDONGFENG 2) stay excluded: Cowork ruling, a JV is another company.
