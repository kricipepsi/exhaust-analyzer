# Skill-Eval — START HERE (coder bootstrap)

Read this as **message 1 of every fresh coder session** on a `T-SE-*` task. The
**architect** authors specs; **this file drives the coder**. Produce no other
output until the Start sequence (§1) is done.

> Skills are local: load **only** from `_skills/`. Never import *code/docs*
> from `ARCHIVE/`, `v2/`, or `v6/`.

---

## 0. Non-negotiables

- **No graphify rebuild.** `graphify-out/graph.json` is canonical. Never run
  `graphify update .` / `/graphify` / `Skill(graphify)`.
- **One task per session — HARD STOP.** Finish one row, fill both gate blocks,
  update the ledger, STOP.
- **Gate of record is Windows `.venv-wired`**, not the sandbox (sandbox can serve
  truncated files).
- **Eval arms control skill loading.** In an A/B task the **arm** dictates which
  skill-under-test loads (CONTRACT §2). Do **not** also hand-load the skill under
  test into your own session — that contaminates the measurement. Your session
  loads only the harness/runner skills below.
- **Git:** only action is the final commit by the user, by explicit path.

## 1. Start sequence

1. Read this file.
2. Read `SKILL_EVAL_PROGRESS.md` (the ledger — next task, dispositions) and
   `SKILL_EVAL_CONTRACT.md` (the methodology) once.
3. Set up Python 3.14: **agent bash** → run the sandbox block (root `CLAUDE.md`);
   **Windows/PowerShell** → `.venv-wired` is the env, confirm `python --version` = 3.14.x.
   Load the mandatory pair:
   - language + inner loop → `_skills/codingskills/pythonskill/python/SKILL.md`
   - verification loop → `_skills/codingskills/ecc-subset/verification-loop/SKILL.md`

   For harness/runner tasks, also load `_skills/codingskills/ecc-subset/eval-harness/SKILL.md`.
   (Exception: when the task **under test** is verification-loop/python itself, the
   arm logic — not your session — loads it. See §0.)
4. **Pick the task the ledger picks:** the first `pending`/`runnable` row whose
   `Blocked-by` are all `done`. Not a `blocked` or `author at unblock` row. If none
   is runnable, **STOP and report**. (T-SE-1 is runnable with no blocker — the cheap
   triage is the natural first session.)
5. **Post a one-paragraph scope confirm** (files, metrics, which skills' verdicts
   this task produces) before writing code. Unclear scope → **ask one question**.

## 2. Working rules (STRICT)

- **Inner loop after EVERY meaningful edit:** `ruff → pyright → pytest -x -q`.
- **Dual-gate before `done`:** `VERIFICATION GATE` + `CODE REVIEW` clean in
  `tasks/progress_notes/<task-id>.md`, which **opens with the confirmed `## Plan`**.
- **Measure per the CONTRACT.** Never score a skill on gated final state; use the
  gate-invisible metrics (§3) and the blinded rubric (§4). Report effect vs
  variance (§5) — a sub-variance difference is a **null**, not a win.
- **A skill is credited only for its own claim's metric** (CONTRACT §3).
- **Reports/notes in `.md`.** Off-scope discoveries → ledger *Unplanned follow-ups*.

## 3. Pack map

- `SKILL_EVAL_PROGRESS.md` — ledger + per-skill disposition (source of truth).
- `SKILL_EVAL_CONTRACT.md` — methodology (arms, metrics, judge, success bar, two tracks).
- `tasks/T-SE-*.md` — task specs (architect-authored).
- `tasks/progress_notes/<task-id>.md` — `## Plan` + gate blocks (coder-authored).

## 4. Session-end gate

Both gate blocks clean → update the ledger row (status, verdict, commit) → output
the final commit block for the user → **STOP**.
