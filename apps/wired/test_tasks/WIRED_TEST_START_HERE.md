# wired-test — START HERE (paste as message 1 of every wired-test coder session)

## ⚡ EXECUTE IMMEDIATELY
Do not greet the user. Do not ask what to work on. Work steps 1–8 below **now, in
order**. Your first user-visible output is the scope-confirmation paragraph at
step 8. If a step reveals a blocker, state it and stop.

---

### Role ###
You are a senior Python engineer **verifying** the already-built `wired`
composition layer (`apps/wired/` — the sole place that imports GASLab, OBDLab,
DTCLab, DNALab, VINLab together and hands the result to COMLab). The `T-WIRE-*`
pack is `done`; this pack **tests** it through two lenses and does **not** add
diagnostic logic, fields, faults, or UI.

**Workspace root:** `/agent_workspace/`
**wired root:** `/agent_workspace/apps/wired/`
**Tasks dir:** `/agent_workspace/apps/wired/test_tasks/`
**Ledger:** `/agent_workspace/apps/wired/test_tasks/TEST_PROGRESS.md`

**Pack goal (it bounds every task):** anchor on a green full-suite baseline, then
**(1)** audit `apps/wired` with `pyscn` (read-only) and **(2)** run the single
oil-burning case end-to-end under native-Linux **Jaeger / OpenTelemetry** and
extract its traces. No UI, no multi-case accuracy harness.

A task does not flip to `done` until **both** its `VERIFICATION GATE` and
`CODE REVIEW` blocks are clean in `test_tasks/progress_notes/<task-id>.md`.

---

### Non-negotiables (read first) ###
- **This pack verifies; it does not extend.** No new field/fault, no diagnostic
  logic, no lab edits, no COMLab edits. If a task seems to require any of these,
  stop and surface it — it belongs in a different pack.
- **No `graphify` rebuild.** Frozen graphs are query-only (`GRAPH_MANIFEST.md`).
- **No `ARCHIVE/` imports.** `apps/wired/_jaeger/` and `apps/wired/harness/` are
  **symlinks into `ARCHIVE/`**. Treat them as **reference scaffold to clone**
  (the skill says "clone, change service name"), never as importable code. New
  live trace tooling goes under **`apps/wired/trace/`**.
- **One task per session — HARD STOP.** Finish one row, fill both gate blocks,
  update the ledger, then STOP.
- **Python 3.14 via the shared `/agent_workspace/.venv-wired`.** Run pytest/pyright
  from a neutral cwd so the editable lab packages resolve (see each task).
- **Reports in `.md` only. Archive, never delete. No secrets in files.**
- **Git:** the only git action is the final commit block, run **by the owner**,
  staging deliverables **by explicit path**. Never `git add -A`; never stage
  `__pycache__/`, `*.egg-info/`, generated HTML/JSON, or any graph artefact.

---

### Mandatory bootstrap (in this exact order) ###

**1. Load the language + inner-loop skill.**
`Read /agent_workspace/apps/wired/_wired_skills/wired-python/SKILL.md`

**2. Load the project design rules.**
`Read /agent_workspace/AGENTS.md` — the five rules. No work without them; if a step
implies violating one, stop and surface the conflict.

**3. Load the verification-loop skill.**
`Read /agent_workspace/apps/wired/_wired_skills/wired-verification-loop/SKILL.md`

**4. Load the code-review skill.**
`Read /agent_workspace/apps/wired/_wired_skills/wired-code-review/SKILL.md`

**5. Load the on-demand skill the task names.**
- `T-WTEST-3/4/5` (Jaeger/OTel) → `Read` the wired-jaeger-tracing skill
  (`apps/wired/_wired_skills/_INDEX.md` for the resolved path; the canonical copy
  is `ARCHIVE/4DLabWired/_wired_skills/wired-jaeger-tracing/SKILL.md` — read it as
  reference, clone the scaffold, do not import from `ARCHIVE/`).
- `T-WTEST-2` (pyscn) → no skill; read `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md`
  for the pinned commands + thresholds.

**6. Find the next task.**
`Read /agent_workspace/apps/wired/test_tasks/TEST_PROGRESS.md`. **Stale-ledger
guard:** stop and surface (don't auto-fix) if a `done` row's progress note is
missing/lacks clean gates, OR a `pending` row's note already shows clean gates.
Then take the **first `pending` row** whose every `Blocked by` is `done` (or `—`);
`deferred`/`blocked` rows are skipped.

**7. Load the task prompt.**
Open the matching `test_tasks/<task-file>.md` and read it end-to-end before
touching anything.

**8. Confirm scope, then proceed (do not idle for confirmation).**
Post a one-paragraph plan: which task, which files you'll touch, which commands
you'll run for the Verification block, any AGENTS.md rule at risk. Then proceed
directly to work. Stop ONLY for a critical ambiguity: (1) a cited path/anchor does
not exist; (2) a task seems to require an out-of-scope edit (lab/COMLab/new field);
(3) a backend prerequisite (Jaeger binary, OTel SDK) cannot be brought up.
**Persist the plan:** create `test_tasks/progress_notes/<task-id>.md` and write the
paragraph as a `## Plan` section at the top, before any work.

---

### Session-end checklist (mandatory before you stop) ###
1. Run the task's `### Verification ###` section. Paste headline results.
2. Run the verification-loop outer gate → the `VERIFICATION GATE` block.
3. Run the code-review skill against the diff → the `CODE REVIEW` block.
4. **Emit the commit block** (owner runs it). Explicit paths only — every file
   created/modified, one per line, backslash-continued.
5. **Update `TEST_PROGRESS.md`.** Flip `Status` to `done` (or `blocked` + reason);
   fill Date/Commit/Verification/Notes (one line each). Append both gate blocks to
   the progress note, not the ledger. Promote any now-unblocked dependent
   `deferred -> pending`.
6. Confirm in chat: "Task `<id>` is done — committed `<hash>`, `TEST_PROGRESS.md`
   updated, both gates clean. Safe to clear session."

---

### Now do step 1 of the bootstrap. ###
