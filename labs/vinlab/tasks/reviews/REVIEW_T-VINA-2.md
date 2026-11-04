TASK REVIEW — T-VINA-2_type_code_year(2) — 2026-11-04 (Windows Cowork, round 2 after correction 01)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 94) — second review (second_review.py, peak → codex) APPROVE WITH CORRECTIONS, 2 LOW upheld
(R6), applied, re-verified

Branch fix/T-VINA-2 on fix/T-VINA-8: spec 0f8dc05, fix 069e188, correction 2257cc9, fix cbd1812. Implementer PID
2940. No hand-back. Score: -6 for the two LOW gaps, both my spec's (the "plant code" wording; a non-Mercedes test that
could not see the WMI condition).

MECHANICAL GATE
  ✓ deliverables exist           R1-R6 in decoder.py, test_decoder.py, test_type_code_year.py (9 cases), wiki/10 §10.6
  ✓ changed files in scope       only Files-to-touch paths (git diff 02ebfba..HEAD)
  ✓ tests                        reviewer re-run: vinlab `225 passed, 8 skipped`; new file `9 passed`; dnalab 27, wired
                                 41, ui 30; comlab 526/4/2 (known collection errors), dtclab 590, gaslab 208, obdlab
                                 388, symptomlab 72 (round 1, unchanged labs); ruff clean
  ✓ mutants killed               M1 isdigit off (3), M2 rule off (3), M3 WMI condition off (1)
  ✓ effect visible               C6 probes `3 failed` → `1 failed, 7 passed`: WDB1240261A102470 and WDD1770441J098476
                                 green; WBA4W9C5ZLYYYYYYY stays T-VINA-3's. Real VINs: the 47 numeric type-code
                                 Mercedes/smart VINs move from 2001 to unknown (P3).

SECOND REVIEW (gpt-6.1-sol medium, embedded 18 KB)
  F1 non-Mercedes test misses the WMI condition UPHELD (R6.2) · F2 unsourced "plant code" UPHELD (R6.1). No regression
  in the H2 gate (`None` passes by design).

FOLLOW-UP
  T-VINA-9 (registered): Renault VF1 position 10, find a source first.
