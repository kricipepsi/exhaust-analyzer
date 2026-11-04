TASK REVIEW — T-VINA-19_registry_majority_filters(1) — 2026-11-04 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 95) — code row; second review (Codex, APPROVE WITH CORRECTIONS)

Branch `fix/T-VINA-19`: spec `c648dfc`, then `52de56f`. Implementer PID 3672 (sonnet, medium). No return.

MECHANICAL GATE
  ✓ deliverables exist           one commit; note with M1, M2; RESULT
  ✓ changed files in scope       `tools/build_wmi_map.py`, `tests/unit/test_build_wmi_map.py` only
  ✓ text equals the rehearsal    both files byte-equal to `make_rh.py`'s copy (`cmp`)
  ✓ tests fail without the fix   new test on the old tool `1 failed`; M1 and M2 each `1 failed`
  ✓ effect visible               rerun by the reviewer: vinlab `344 passed, 8 skipped`; file `9 passed`; ruff clean

CRITERIA
  1 MET · 2 MET

SECOND REVIEW (recheck/codex/T-VINA-19_review.md): M1 and M2 re-derived as decisive (SUBARU 3:2; U+FFFD brand 3:2).
  MEDIUM `brand != "\ufffd\ufffd"` mutant      NOT UPHELD: not a plausible edit; R1 is a substring test as written
  LOW empty-brand guard removed                NOT UPHELD: `csv` gives "" and the guard is unchanged code
  LOW `>= 17` mutant                           NOT UPHELD: same reason
  Tradeoff: a further round of contrived mutants costs more than the defect it guards.
