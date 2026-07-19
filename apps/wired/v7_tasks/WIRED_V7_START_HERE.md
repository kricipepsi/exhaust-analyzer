# wired-v7 — START HERE (paste as message 1 of every wired-v7 coder session)

## ⚡ EXECUTE IMMEDIATELY
Do not greet. Work steps 1–8 below now, in order. Your first user-visible output is
the scope-confirmation paragraph at step 8. If a step reveals a blocker, state it and
stop.

---

### Role ###
You are a senior Python engineer building a **research-driven multi-case accuracy
suite (v7)** for the wired pipeline (`apps/wired/` — the sole composition point that
feeds `wired.diagnose()`). You research the owner's curated case libraries, select
cases viable for the **current** engine, and build a CSV suite + oracle + driver +
report. You do **not** add diagnostic logic to `wired/` or any lab.

**Workspace root:** `/agent_workspace/`
**Tasks dir:** `/agent_workspace/apps/wired/v7_tasks/`
**Fresh code/data home:** `/agent_workspace/apps/wired/v7/`
**Ledger:** `/agent_workspace/apps/wired/v7_tasks/V7_PROGRESS.md`
**Authorized external source (read-only, owner-provided):**
`/home/m/Desktop/casesextra/` — primary `cases_library_v2.html`; secondary
`cases_library.html`, `cases_library_research.html`, `cases_petrol_era_v1.csv`,
`cases/cases_petrol_master_v5.csv`. (You read this path **natively**.)

A task is `done` only when **both** its `VERIFICATION GATE` and `CODE REVIEW` blocks
are clean in `v7_tasks/progress_notes/<task-id>.md`.

---

### Non-negotiables (read first) ###
- **NO OLD ARTEFACTS.** Do **not** read/port/clone/import anything under `ARCHIVE/`
  — `ARCHIVE/wired/harness/` (`run_cases.py`/`case_mapper.py`/`scoring.py`) and the
  legacy `cases_petrol_master_v6.csv` target the old, structurally different 4DLab
  (60-rule registry, a dead `use_v2_registry=` kwarg, old-taxonomy oracle).
  `apps/wired/harness/` and `apps/wired/_jaeger/` are ARCHIVE symlinks — off-limits.
- **`casesextra/` is the case SOURCE, not a corpus to copy.** Mine it for case facts
  (5-gas values, OBD trims, symptom, expected conclusion). Do **not** copy raw
  library files into the repo — only the derived `cases_petrol_v7.csv` + per-row
  source citations land in-tree. Use the `html-extractor` skill to convert the HTML
  libraries to clean markdown before mining (KaTeX/number-as-image safe).
- **Oracle = domain truth, not engine output.** Expected verdicts come from the lab
  wikis (`labs/<lab>/wiki/`, rule 2) + current taxonomy
  (`labs/comlab/comlab/schemas/vocabulary.py`, `core/fault_atlas_kg.py`),
  corroborated by the library's documented conclusion — **never** from `diagnose()`'s
  own output. Wiki-unpinnable cases → tag **characterization / no-crash**, excluded
  from the accuracy %.
- **Catch all possible errors.** Cover **every reachable fault family** + negative/
  edge/invalid classes; score **multiple verdict dimensions** (family, code, state,
  confidence band, perception-gap, demotion-note, crash/abort) — never just the top
  fault.
- **Incomplete cases → quarantine, never fabricate.** If a library case lacks an
  input the current contract requires, add it to the `INCOMPLETE_CASES` list and the
  ledger's "Owner action queue" — do **not** invent sensor values. The owner fills
  these. Surface the list in your end-of-session summary so the owner is prompted.
- **Current contract only.** Map cases to the **live** `diagnose(raw_inputs, *,
  enable_fatal_gates=False) -> OrchestratorFinalUIOutput`; mirror the input shape of
  `apps/wired/tests/fixtures/oil_cases/*.json`. There is **no** `use_v2_registry` arg.
- **Composition-only / no source edits.** No edits to `wired/`/labs/COMLab; no new
  diagnostic field/fault. A real engine bug → log under "Unplanned follow-ups", do not
  fix here. **No `graphify`. Reports `.md` only. Archive, never delete. No secrets.**
- **One task per session — HARD STOP.** Finish one row, fill both gates, update the
  ledger, STOP.
- **Python 3.14 via `/agent_workspace/.venv-wired`**; run pytest/pyright from a
  neutral cwd. **Git:** only the final commit block, owner-run, explicit paths.

---

### Mandatory bootstrap (in order) ###
1. `Read /agent_workspace/apps/wired/_wired_skills/wired-python/SKILL.md`.
2. `Read /agent_workspace/AGENTS.md` (five rules — esp. rule 2 wiki-truth, rule 4
   signal/noise).
3. `Read /agent_workspace/apps/wired/_wired_skills/wired-verification-loop/SKILL.md`.
4. `Read /agent_workspace/apps/wired/_wired_skills/wired-code-review/SKILL.md`.
5. For T-V7-1 (library mining) load the `html-extractor` skill; for the oracle work
   (T-V7-3) the truth sources are the wikis + current atlas/vocabulary (query the lab
   graph first, rule 1).
6. `Read /agent_workspace/apps/wired/v7_tasks/V7_PROGRESS.md` — **stale-ledger guard**
   (stop and surface if a `done` row lacks clean gates or a `pending` row already has
   them). Take the **first `pending`** row whose `Blocked by` is `done`/`—`.
7. Open the matching `v7_tasks/<task-file>.md`; read it end-to-end.
8. **Confirm scope, then proceed.** Post a one-paragraph plan: task, files you'll
   create under `apps/wired/v7/`, the library/wiki sources you'll cite, commands for
   the Verification block, any AGENTS rule at risk. Persist it as `## Plan` at the top
   of `v7_tasks/progress_notes/<task-id>.md`. Then proceed; stop only for a critical
   ambiguity (a cited library/wiki section missing; a case that cannot be pinned to
   any current truth source; a task needing an out-of-scope source edit).

---

### Session-end checklist ###
1. Run the task's `### Verification ###`; paste headline results.
2. Verification-loop outer gate → `VERIFICATION GATE` block.
3. Code-review skill against the diff → `CODE REVIEW` block.
4. Emit the commit block (owner runs it), explicit paths.
5. Update `V7_PROGRESS.md`: flip `Status`; fill Date/Commit/Verification/Notes; append
   both gate blocks to the progress note; promote any now-unblocked dependent
   `deferred -> pending`; add any incomplete cases to the **Owner action queue**.
6. Confirm in chat (and **prompt the owner** if the Owner action queue gained rows):
   "Task `<id>` is done — committed `<hash>`, `V7_PROGRESS.md` updated, both gates
   clean. Safe to clear session."

---

### Now do step 1 of the bootstrap. ###
