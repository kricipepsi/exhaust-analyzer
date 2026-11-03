TASK REVIEW — T-VINA-1_year_scope_gate(3) — 2026-11-03 (Windows Cowork, round 2 after correction 01)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 95) — second-model review APPROVE WITH CORRECTIONS; F1 applied (R7) and re-verified

Branch `fix/T-VINA-1`: `baf9129` spec, `1a32e3c` round 1, `7b7134b` correction 01, `4191fba` round 2, on `9fe682d`
(`fix/T-AUD-7a`). Implementer session 2956ed69, 11.3 min wall-clock (estimate 45-75: every edit was rehearsed).
Score: -5 for the round-1 test gap the second review found (it was in Cowork's R4, not an implementer miss).

MECHANICAL GATE
  ✓ deliverables exist           2 commits of code and tests, note + RESULT
  ✓ changed files in scope       round 1: exactly the 15 Files-to-touch paths (`git diff --name-status`); round 2:
                                 `test_year_scope.py` only; no line-ending churn
  ✓ code = rehearsal             decoder.py, test_decoder.py, test_year_scope.py (round 1) and the fixture equal
                                 `recheck/T-VINA-1/make_rh.py`'s copy with CR stripped; round 2 differs in a name only
  ✓ mutants killed               3/3, run by the reviewer on the real decoder, restored byte-identical (cmp):
                                 M1 `_YEAR_MAX = 2020` → 10 failed; M2 `candidates[-1]` → 2 failed;
                                 M3 `candidates[0]` → 1 failed (it passed the whole suite before R7)
  ✓ effect visible               C6 probes 33 → 28 failed (F-C6-3 ×3, F-C6-8 ×2 now pass); real VINs: 229 of 1,364
                                 refused as out of scope; corpus 8 of 314 refused, 259 move from 2020 to the 1990s
  ✓ docs                         diff read: every bound says 2010, the comlab scope line is cited, the `L` rule and
                                 the `era_hint_unrecognised` flag are gone from wiki and docs; ADR untouched

VERIFICATION (reviewer re-run, C:/4DApp/repo, final tree)
  1 `216 passed, 8 skipped` · 2 `17 passed` · 3 `27`, `41`, `30 passed` · 4 `3 failed, 5 passed` · 5 `0`, `0`, `1` ·
  6 ruff clean, status lists only the note and the RESULT
  Repo-wide: comlab `526 passed, 4 skipped, 2 errors`, dtclab 590, gaslab `208 passed, 2 skipped, 4 deselected`,
  obdlab `388 passed, 2 skipped`, symptomlab 63: all equal to the base.

CRITERIA
  1 MET · 2 MET · 3 MET · 4 MET · 5 MET

NIT
  wiki/11 says `B`-`K` "are 2011-2019" and omits their 1980s reading; harmless (both are out of scope).

SECOND REVIEW
  `recheck/codex/T-VINA-1_review.md` (gpt-6.1-sol, medium, embedded prompt 44.9 KB): APPROVE WITH CORRECTIONS; it
  cites `_resolve_year`, `years.csv`, the §10.5 heading. F1 upheld (R7), F2 not upheld (sidecar correction 01).

KNOWN AND OWNED ELSEWHERE
  Mercedes position-10 VINs decode as 2001 (T-VINA-2); `WBA4W9C5ZLYYYYYYY` decodes as a 1990 BMW with Euro 6
  (F-C6-4, T-VINA-3).
