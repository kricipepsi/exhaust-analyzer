TASK REVIEW — T-VINA-15_zero_zero_sensors_unknown(2) — 2026-11-04 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 92) — code row; second review run on round 1 (Codex, APPROVE WITH CORRECTIONS)

Branch `fix/T-VINA-15`: spec `51566ca`, round 1 `32d3d1c`, correction 01 `511ffbd`, round 2 `18b60a1`.
Implementer PID 1796 (sonnet, medium). One return (correction 01, the spec's gap).

MECHANICAL GATE
  ✓ deliverables exist           2 code commits; note and RESULT with `## Round 2`
  ✓ changed files in scope       `vinlab/decoder.py`, `tests/unit/test_sensor_unknown.py`; `vref.db` and the builder
                                 untouched (R4)
  ✓ text equals the rehearsal    round 1 = `make_rh.py`, round 2 = `make_rh2.py` copies, byte for byte (`cmp`)
  ✓ tests fail without the fix   M1, M2 `3 failed`; M3 `1 failed`; M4 `2 failed`; M5 `1 failed`
  ✓ effect visible               rerun by the reviewer: vinlab `354 passed, 8 skipped` (base 344); file `10 passed`;
                                 dnalab 27, wired 41, ui 30, probes 14 (as base); against `51566ca` exactly 13 real C6
                                 VINs change, all `MAP_ONLY_SPEED_DENSITY` (no sensor) → `DUAL_MAF_MAP_CROSSCHECK`

CRITERIA
  1 MET · 2 MET · 3 MET · 4 MET

SECOND REVIEW (recheck/codex/T-VINA-15_review.md, re-derived on a copy)
  MEDIUM one-sided reset mutant survives      UPHELD → R5.2, fixed in round 2 (M4)
  LOW rule not scoped to injected engines     UPHELD → R5.1, R5.3, fixed in round 2 (M5)
  NOTE "13 is a corpus count, the rule reaches all 68 rows": true; the 68 rows are all injected, and the change
       is the documented unknown path for each.

FINDINGS
  concern  The heuristic gives DUAL_MAF_MAP for the 13 because their rows store has_egr = 1. Per-engine sourcing of
           MAF/MAP is not possible on this host; no row registered (no source to measure against).
