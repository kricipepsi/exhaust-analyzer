# OBDLab v2 — TASKS START HERE

Read this first, every session, before any other action.

## 0. Do NOT run graphify (the recurring failure)

**No OBDLab task touches the knowledge graph.** The graph is a frozen, verified
artefact — never rebuilt here.

- **Forbidden:** `graphify`, `graphify update .`, `Skill(graphify)`, or any
  self-added "refresh the KG / keep the graph current" step. None of these are
  in any OBDLab task spec.
- If you catch yourself about to run one: **STOP.** It is not part of the task.
- The coding-bootstrap KG pre-step resolves to **SKIP** for this lab.
- A build runs *only* inside a dedicated KG-lane task (`T-PREP-*`/`T-KG-*`)
  whose own Deliverables name `graph.json`. No OBDLab task here is one.

## 1. Start sequence

1. Read this file.
2. Read `PROGRESS.md` — the Task log table is the source of truth.
3. Run the sandbox Python 3.14 block (workspace `CLAUDE.md`); load the language
   + verification-loop skills. KG pre-step → SKIP (§0).
4. **Pick the task the ledger picks:** the first `pending` row whose Blocked-by
   are all `done`. Not a later one, not one you were handed.
5. Post a one-paragraph scope confirm (field, guard, signal/noise consumer)
   before writing code. Unclear scope/consumer/files → ask one question first.

## 2. Non-negotiables

- **Emitter-only:** OBDLab emits its own channels; **no** fault verdicts
  (`ecu_fault` etc. are COMLab fusion). Verifications grep-guard this.
- **Signal/noise:** every new field needs a named existing consumer (or a
  proposal shipping its consumer). "Future use" is not a consumer.
- **No cross-lab Python imports.** Numeric literals carry a wiki cite.
- **Inner loop after every meaningful edit:** `ruff` → `pyright` → `pytest -x -q`.
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in
  `progress_notes/<id>.md`, flip the ledger row to `done`, then STOP.

## 3. Done means

Both gate blocks clean in the progress note **and** any field the task
contracted to consume is grep-confirmed read in a live path. Green pytest alone
is not done. Git: owner commits by explicit path; never stage `graphify-out/`.
