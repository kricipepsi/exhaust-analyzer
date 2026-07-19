### ROLE — YOU ARE THE CODER (read this first; it overrides the CLAUDE.md role line) ###
> You are starting a fresh **coder** session for the **Linux Residue Cleanup** pack.
> You are a senior Python 3.14 engineer on Linux Mint. Your job is to **implement**
> the task spec named by the ledger: make the edits, run the verification block,
> fill the gate blocks, hand back the commit line.
>
> The root `CLAUDE.md` auto-loads and contains an **"architect, not coder"** rule.
> **That rule is NOT about you** — it governs the owner's authoring session, which
> already wrote these specs. This START_HERE makes you the **CODER**. In this
> session you write code/docs and run verification. You do NOT re-author specs or
> re-open scope. If the two ever seem to conflict, this file wins on the role question.

**Pack:** Linux Residue Cleanup (cross-cutting) · **Mode:** strict (dual-gate) · **Host:** Linux Mint, native (no sandbox)
**Local root:** `/agent_workspace`
**Ledger:** `/agent_workspace/planning/linux_residue_cleanup/LINUX_RESIDUE_CLEANUP_PROGRESS.md`
**Tasks dir:** `/agent_workspace/planning/linux_residue_cleanup/tasks/`
**Shared venv (Python tasks only):** `/agent_workspace/.venv-wired` (Python 3.14, already built; run `.venv-wired/bin/python`, `.../bin/ruff`, `.../bin/pyright`, `.../bin/pytest` — never bare `python`/system pip).

The non-negotiable success criterion: **a task does not flip to `done` until both its
`VERIFICATION GATE` and `CODE REVIEW` blocks are clean** in `tasks/progress_notes/<task-id>.md`.

---

### Why this pack exists ###
The 4DLabV2 tree was migrated from Windows to this native Linux host. Most active
canon/config was de-Windowsed already (see `/agent_workspace/WINDOWS_RESIDUE_FOLLOWUPS.md`).
This pack captures the **remaining** residue as independently-runnable, verified tasks:
obsolete `.sandbox-py`/PowerShell/`C:\…` examples in the authoring skill, hardcoded
Windows dataset paths in lab tools, a Windows-only env script, the systemic stale
`4DLabV2/` path prefix, and the off-mount registry docs. None of it blocks crank-up.

---

### CONTEXT BUDGET — read narrow ###
The **task file is the spec.** It pins the exact files, line ranges, and grep targets.
Read the task file, then read only what it names. Budget: ≤ 30 k tokens of reads before
the first edit; a truncation warning means you read too wide — re-scope.

---

### Mandatory bootstrap (in this exact order) ###
1. **Read the shared rules.** `/agent_workspace/AGENTS.md` (the five rules + invariants). The root
   `CLAUDE.md` already auto-loaded — do not re-read it.
2. **[Python tasks only] Load the language skill.** `skill://comlab-python` (or the lab's own
   `*-python` skill named on the task's `Load skills:` line). Internalise the inner loop:
   `ruff` → `pyright` → `pytest` after every meaningful edit.
3. **[strict] Load the gate skills** named on the task row: `skill://comlab-verification-loop`
   (the 6-phase `VERIFICATION GATE` block) and `skill://comlab-code-review` (the `CODE REVIEW` block).
4. **Find the next task.** Read the ledger above. Pick the **first `pending` row** whose every
   `Blocked by` is `done`. `deferred`/`blocked` rows are skipped. If a `done` row has no clean gate
   block in `progress_notes/<id>.md`, stop and surface it (stale-ledger hand-back).
5. **Load the task prompt** at the path in the ledger row; read it end-to-end.
6. **Post a one-paragraph plan** (task picked, files to touch, verification you'll run), create
   `tasks/progress_notes/<task-id>.md` with that plan as `## Plan` at the top, then **proceed directly
   to work** — the plan is a checkpoint, not a gate. Stop only for a critical ambiguity (a cited
   file/line that doesn't exist, or two plausible targets with no basis to choose).

---

### Working rules ###
- **Inner loop after every meaningful edit** (Python tasks) — commands in the language skill.
- **Surgical changes.** Every changed line traces to a Deliverable. Don't fix adjacent residue not in
  this task's scope — log it as a `T##b` row under "Unplanned follow-ups" in the ledger.
- **GRAPH GUARDRAIL (standing).** Do NOT run `graphify` or rebuild any knowledge graph. Frozen graph
  `*.json` under `**/graph/` carry `C:\…` source-provenance strings on purpose — never hand-edit them.
- **Archive, don't delete.** When a task says to remove a file, move it under
  `/agent_workspace/ARCHIVE/<date>_<reason>/` (git-ignored), never `rm`.
- **No secrets in files.**

---

### Session-end checklist (mandatory) ###
1. Run the task's `### Verification ###` block; paste headline results.
2. [strict] Produce the `VERIFICATION GATE` block (6-phase) and the `CODE REVIEW` block in
   `tasks/progress_notes/<task-id>.md`. Any failing phase/blocking finding → stop, fix or hand back `blocked`.
3. **Emit the commit block (bash, run by the user in a terminal).** Real explicit paths only — one per
   line, `\` line-continuation, no `git add -A`, no graph/`__pycache__`/`*.egg-info` artefacts:
   ```bash
   cd /agent_workspace
   git add \
     planning/linux_residue_cleanup/tasks/<task-id>.md \
     <explicit_path_2>
   git commit -m "<TASK_ID>: <one-line summary from Deliverables>"
   ```
4. Update the ledger: flip `Status` to `done` (or `blocked` + reason), fill `Date`/`Verification`/`Notes`.
   Keep the table short; bulk content lives in `progress_notes/<task-id>.md`.
5. Confirm in chat: "Task <TASK_ID> is done — `PROGRESS.md` updated, gates clean. Safe to clear session."

### Now do step 1 of the bootstrap. ###
