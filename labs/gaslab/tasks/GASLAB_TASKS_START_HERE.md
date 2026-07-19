# GASLab v2 — TASKS START HERE

Read this first, every session, before any other action.

## 0. Do NOT run graphify as part of a task (the recurring failure)

GASLab's `graph.json` is a **frozen, verified, off-runtime artefact — no code
reads it.** It is never rebuilt as a side-effect of a normal task.

- **graphify is NOT a step in the inner loop or the verification gate.** Older
  GASLab progress notes wired `graphify update` into the gate (e.g. T-GV2-6c
  rebuilt ~64.9k nodes); that was wrong. Drop that step — it is not a deliverable.
- **Forbidden** in any normal task: `graphify`, `python -m graphify update .`,
  `Skill(graphify)`, or any "keep the graph current / re-extract the wiki" step.
- The **only** sanctioned rebuild is the dedicated KG task **`T-GV2-KG`**
  (deferred), and **only when the owner explicitly instructs it.** If a task is
  not `T-GV2-KG`, graphify does not run. The coding-bootstrap KG pre-step → SKIP.
- If you catch yourself about to run it: **STOP** and escalate to the owner.

## 1. Start sequence

1. Read this file.
2. Read `PROGRESS.md` — the Task log is the source of truth (next task, blocks).
3. Run the sandbox Python 3.14 block (workspace `CLAUDE.md`); load the GASLab
   language + verification-loop skills. KG pre-step → SKIP (§0).
4. **Pick the task the ledger picks:** the first `pending` row whose Blocked-by
   are all `done`. Not a `deferred`/`blocked` row, not one you were handed.
5. Post a one-paragraph scope confirm (field/enum, bound + wiki cite, signal/noise
   consumer) before writing code. Unclear scope/consumer/files → ask one question.

## 2. Non-negotiables

- **North star:** reconcile `ChemicalSignature` to the v2 wiki's **34-value**
  surface (`CHANGE_v2.1_timing_taxonomy.md`) before payload-shape work.
- **Signal/noise:** every new field/enum needs a named existing consumer (or a
  proposal shipping its consumer). "Future use" is not a consumer.
- **No cross-lab Python imports.** Every numeric literal carries a wiki cite.
- **STRICT mode — inner loop after every meaningful edit:** `ruff` → `pyright`
  → `pytest -x -q`. graphify is **not** part of this loop (§0).
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in
  `progress_notes/<id>.md`, flip the ledger row to `done`, then STOP.

## 3. Done means

Both gate blocks clean in the progress note **and** any field the task
contracted to consume is grep-confirmed read in a live path. Green pytest alone
is not done. Git: owner commits by explicit path; never stage `graph/`.
