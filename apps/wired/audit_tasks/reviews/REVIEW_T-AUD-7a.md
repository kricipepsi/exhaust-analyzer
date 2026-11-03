TASK REVIEW — T-AUD-7a_git_rule_main_production(1) — 2026-11-03 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 100) — docs row; no second review (CLAUDE.md step 6)

Branch `fix/T-AUD-7a`: spec `d97d92e`, then `3090b1c docs(T-AUD-7a): git rule agrees with main = production (F-D3-1)`.
Implementer PID 6472.

MECHANICAL GATE
  ✓ deliverables exist           2 docs edited in one commit; note, RESULT
  ✓ changed files in scope       `4DLab_CLAUDE.md`, `v3/CLAUDE.md` only (diff stat); text equals R1 and R2 verbatim
                                 (diff read)
  ✓ effect visible               D3 probe X1: the 4 "never branch / work on main" sides NOT FOUND, the 2 production
                                 sides found; `sides not found: 4` (base 0), as rehearsed

CRITERIA
  1 MET · 2 MET · 3 MET

NOTE
  `audit/scratch/D3/rules.py` crashes on cp1252 when its output is piped; run it with `PYTHONIOENCODING=utf-8`.
  The other T-AUD-7 items (F-D3-2…9, 13; R0-3, R0-5) stay open in FIX_PLAN.
