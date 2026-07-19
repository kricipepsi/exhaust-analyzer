# SHIP pack — coder bootstrap (read fully, then execute)
You are the CODER for the ship pack. One task per session. STRICT dual-gate
(VERIFICATION GATE + CODE REVIEW blocks in `ship_tasks/progress_notes/<id>.md`).

## Boot sequence
1. Read root `AGENTS.md` (the five rules) and `4DLab_CLAUDE.md` (infra: Python 3.14
   sandbox `.sandbox-py/bin/python3.14`; wired venv `.venv-wired`; inner loop
   ruff/pyright/pytest; git is owner-run — never commit/branch/stash).
2. Read `planning/SHIP_AUDIT_2026-07-07.md` — why each task exists.
3. Open `ship_tasks/SHIP_PROGRESS.md`; take the first `pending` row whose
   Blocked-by are all `done` (or the task ID the manager assigned).
4. Post a one-paragraph scope confirmation (plan-at-top) before any other output.

## Hard rules for this pack
- **No score chasing.** The owner stop ruling (2026-07-06) closed accuracy work at
  269/294. If your task moves `top3_family`, something is wrong — STOP and surface.
- **Yardstick discipline:** `run_suite.py` and pinned yardsticks are hash-locked
  (a stored checksum that refuses silently changed files). Never edit them; T-SHIP-2
  touches only the non-locked `score_v3_yardstick.py` read side.
- Never edit `Vault/` (archived mirror). Never run `graphify` builds. No secrets in files.
- Reports in `.md`. One task ≤ 50% of a fresh context.
