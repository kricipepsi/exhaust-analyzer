TASK REVIEW — T-VINA-8_symptomlab_contract_fixes(2) — 2026-11-03 (Windows Cowork, round 2 after correction 01)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 93) — second-model review APPROVE WITH CORRECTIONS; F1-F4 applied (R7) and re-verified

Branch `fix/T-VINA-8`: `eeeeaa9` spec, `4d6ee41` round 1, `3f72ac1` correction 01, `597173f` round 2, on `22a6e98`
(`fix/T-VINA-1`). Implementer PID 5592.
Score: -5 for the round-1 gaps the second review found (stale DLD/LLD default text that Cowork's step-5 grep did not
cover; an ADR-0008 misattribution; a pre-existing `TypeError` path in `from_json`); -2 for a history line the
implementer rewrote to 21 under Cowork's own R5.3 (fixed in R7.2).

MECHANICAL GATE
  ✓ deliverables exist           2 commits of code, tests and docs; note + RESULT
  ✓ changed files in scope       round 1: the 11 Files-to-touch paths; round 2: the 5 R7 paths
  ✓ code = rehearsal             models.py, validator.py and both test files equal `make_rh.py` / `make_rh2.py`
                                 copies (CR stripped)
  ✓ mutants killed               3/3 on the real tree, restored byte-identical (cmp): MR1 `1 failed`, MR2 `4 failed`,
                                 MR3 `3 failed`
  ✓ effect visible               C6 probes F-C6-12, F-C6-13: `3 failed` → `3 passed`; `from_json(None)` and a
                                 `None`/`[]`/`"x"` env now raise SymptomValidationError (was TypeError)
  ✓ docs                         diff read: 21 pairs (7 × 3) everywhere outside the ADR; the oil sub-filters in HLD,
                                 LLD, VOCABULARY; ADR-0008 supersedes ADR-0003 and names ADR-0007's alternative 2

VERIFICATION (reviewer re-run, C:/4DApp/repo, final tree)
  1 `72 passed` · 2 `9 passed` · 3 `27`, `41`, `30`, `526 passed, 4 skipped, 2 errors` · 4 `3 passed, 48 deselected` ·
  5 `0 0 1 1` (round 1) and `0 0 0 0 0` (round 2 greps) · 6 ruff clean, status lists only the note and the RESULT
  Repo-wide (round 1 tree): vinlab 216, dtclab 590, gaslab `208 passed, 2 skipped, 4 deselected`, obdlab
  `388 passed, 2 skipped`: equal to the base.

CRITERIA
  1 MET · 2 MET · 3 MET · 4 MET · 5 MET

KNOWN
  The C6 probe `test_f11_combination_count_consistent` stays red by design: it reads the ADR, which keeps its record.

SECOND REVIEW
  `recheck/codex/T-VINA-8_review.md` (gpt-6.1-sol, medium, embedded prompt 43 KB): APPROVE WITH CORRECTIONS; it cites
  `DLD_SymptomLab.md`, `LLD_SymptomLab.md`, ADR-0008, `from_json`. F1-F4 upheld (sidecar correction 01); F1 was wider
  than reported (LLD:115-116 too).
