# Per-Lab Test-Harness Rollout — START HERE (coder bootstrap)

Read this as **message 1 of every fresh coder session** on a `T-TST-*` task. The
**architect** authors the task specs; **this file drives the coder** — the inner
loop, the dual-gate, the ledger update. Do not produce any other output until the
Start sequence (§1) is done.

> **Skills are local now.** This pack's skills live under `_skills/…`
> (copied 2026-06-09 so no path crosses into `v2/` or `4DApp/_skills`). Load skills
> **only** from `_skills/`. Never import *code/docs* from `ARCHIVE/`, `v2/`,
> or `v6/` — the wikis and specs are truth.

---

## 0. Non-negotiables (read first)

- **No graphify rebuild.** `graphify-out/graph.json` is the canonical artefact.
  Never run `graphify update .`, `/graphify`, or `Skill(graphify)`. If you catch
  yourself about to: **STOP** and escalate to the owner.
- **Shared generative engine is imported, never copied** — from
  `harness/harness/` (`from harness.descriptor import ModuleDescriptor`,
  `from harness.runner import run_generative_suite`). Copying engine files into a
  lab is a bug (PROJECTION_CONTRACT §2).
- **No cross-lab Python imports.** A lab's tests import only that lab + the shared
  engine. COMLab mirrors types locally.
- **One task per session — HARD STOP.** Finish one row, fill both gate blocks,
  update the ledger, then STOP. Do not start a second row, even if unblocked or
  named.
- **Git:** the only git action is the final commit, run **by the user** in
  PowerShell, staging deliverables **by explicit path**. Never branch/stash; never
  raise git as a blocker.
- **Do not load the redirect stub** at `_skills/pythonskill/python/SKILL.md`
  — it is a dead pointer. The real skill paths are in §1.3 and §3.

## 1. Start sequence

1. **Read this file.**
2. **Read `TEST_ROLLOUT_PROGRESS.md`** — the Task log is the source of truth (next
   task, blocks, commit). Read `TEMPLATE.md` (canonical `tests/` layout) and
   `PROJECTION_CONTRACT.md` (master→per-lab CSV rules) once.
3. **Set up Python 3.14.** In an **agent bash** session, run the sandbox Python 3.14
   block (root `CLAUDE.md` → "Sandbox Python"). In a **Windows / PowerShell** session
   that bash block does not apply — `.venv-wired` is the environment; just confirm
   `.venv-wired\Scripts\python.exe --version` prints 3.14.x. Then **load the mandatory
   skill pair**:
   - language + inner loop → `_skills/codingskills/pythonskill/python/SKILL.md`
   - verification loop → `_skills/codingskills/ecc-subset/verification-loop/SKILL.md`

   Then load any **on-demand** skills named in the task file's `Load skills:` line (§3).
4. **Pick the task the ledger picks:** the first `pending` row whose `Blocked-by`
   are **all** `done`. Not a `blocked` row, not an `authored · impl blocked` row,
   not one you were handed. **If no row is runnable** (every `pending` row still has
   an open blocker), **STOP and report** — never start a blocked row. The ledger,
   not this file, is the live record of which rows are blocked and why.
5. **Post a one-paragraph scope confirm** (files, tests, signal/noise consumer)
   before writing code. Unclear scope/consumer/files → **ask one question**, do not
   guess.

## 2. Working rules (STRICT)

- **Inner loop after EVERY meaningful edit:** `ruff` → `pyright` → `pytest -x -q`.
  Gates **of record** run on the Windows `.venv-wired`, not the sandbox — the
  sandbox mount can serve truncated files, so never trust sandbox tool output as
  the gate.
- **Dual-gate before `done`:** `VERIFICATION GATE` + `CODE REVIEW` both clean in
  `tasks/progress_notes/<task-id>.md`. The progress note **opens with the confirmed
  `## Plan`** (written before any code), then gains the two gate blocks at the end.
- **Per-lab CSV is a projection** of `cases_petrol_master_v6.csv`
  (PROJECTION_CONTRACT) — consumed columns × lab-decidable rows. The **full** master
  is the *wired* integration gate, not a per-lab fixture.
- **Signal/noise (fixture variant):** every expected-output cell and every
  fault-box bound cites a live source file + wiki section in its `gt_source`;
  uncited values are `gt_method=characterization` (regression net, not correctness).
- **Reports and progress notes in `.md` only.** Never `.docx`/`.pdf`.
- **Deliverables only.** Off-scope discoveries → the ledger's *Unplanned follow-ups*
  table, not the diff.

## 3. On-demand skills (load when a task's `Load skills:` line names them)

All under `_skills/codingskills/`:

| Task surface | Skill |
|---|---|
| harness build / generators / fixtures | `ecc-subset/eval-harness/SKILL.md`, `ecc-subset/python-testing/SKILL.md` |
| regression / golden / decision-rate nets | `ecc-subset/ai-regression-testing/SKILL.md` |
| the `CODE REVIEW` gate | `code-reviev/SKILL.md`, `uncle-bob-code-craftsmanship/SKILL.md` |

(The mandatory pair in §1.3 always loads; this table is task-dependent.)

## 4. Pack map

- `TEST_ROLLOUT_PROGRESS.md` — ledger (source of truth).
- `TEMPLATE.md` — canonical per-lab `tests/` layout.
- `PROJECTION_CONTRACT.md` — master → per-lab CSV column/row rules.
- `tasks/T-TST-*.md` — task specs (architect-authored).
- `tasks/progress_notes/<task-id>.md` — `## Plan` + the two gate blocks (coder-authored).

## 5. Session-end gate

Both gate blocks clean in the progress note → update the ledger row (status +
commit) → output the final commit block for the user (PowerShell, explicit paths)
→ **STOP**. One task per session.
