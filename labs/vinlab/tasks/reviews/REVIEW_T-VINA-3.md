TASK REVIEW — T-VINA-3_vref_year_window(2) — 2026-11-04 (Windows Cowork, round 2 after correction 01)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 88) — hand-back B6 (COWORK, upheld) → R6; second review (second_review.py, peak → codex)
APPROVE WITH CORRECTIONS: F1 not upheld on the shipped data (routed to T-VINA-6), F2 LOW nit

Branch fix/T-VINA-3 on fix/T-VINA-2: spec d5c8c87, fix 869db2a, correction 2d1cc3d, fix 898f9b1. Implementer PID
12864. Score: -7 for B6, my defect (the P2 wired figure was not measured on the change; one round spent); -5 for F2
(the out-of-window tests assert `!= EURO_4` / `!= HIGH`, not exact `PARTIAL` or the flag).

MECHANICAL GATE
  ✓ deliverables exist           R1-R6: decoder.py window guard + flag; test_vref_year_window.py (3); TestDbRowPath on
                                 VF7SA5FR8AW511081 + an out-of-window test; test_models rated_rpm 6000; regenerated
                                 WBA4W9C5ZLYYYYYYY.json; VIN_VOCABULARY flag row; MW-009.json → its 5FR VIN
  ✓ changed files in scope       only Files-to-touch paths (git diff aa69249..HEAD)
  ✓ tests                        reviewer re-run: vinlab `229 passed, 8 skipped`; dnalab 27, wired 41, ui 30, comlab
                                 526/4/2 (known collection errors), dtclab 590, gaslab 208, obdlab 388, symptomlab 72;
                                 ruff clean
  ✓ mutant                       window check off → 4 failed
  ✓ effect visible               C6 probes f3/f8 `1 failed` → `8 passed` (WBA4W9C5ZLYYYYYYY no longer Euro 6); the f4
                                 probe's rows now show EURO_1, NARROWBAND, non-HIGH (red by construction: it lists
                                 every out-of-window VIN)

SECOND REVIEW (gpt-6.1-sol medium, embedded 21 KB)
  F1 a dropped row skips the H1 secondary petrol check: NOT UPHELD as a defect — `vref.db` holds 0 non-petrol rows
  (30 GDI, 42 PORT_INJECTION); latent ordering, routed to T-VINA-6 (petrol guard, F-C6-5). F2 weak assertions: LOW nit.
  No omitted ruling; the regenerated fixture agrees with the accepted fallback (T-VINA-10's).
