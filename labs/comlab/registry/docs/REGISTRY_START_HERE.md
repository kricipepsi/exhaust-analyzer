# REGISTRY_START_HERE — paste as message 1 of every registry session

> **Linux host, in-mount (rewritten 2026-06-28).** Repo root is `/agent_workspace`.
> All paths below are repo-relative. Cowork and the omp coders run **natively on this
> host and share one venv** (`/agent_workspace/.venv-wired`, Python 3.14) — there is no
> separate sandbox interpreter. Canonical env + git ritual: `4DLab_CLAUDE.md` →
> "Python environment" / "Git". The old Windows bootstrap (PowerShell, `C:\Users\...`,
> a second sandbox python) is retired.

## ⚡ EXECUTE IMMEDIATELY

Do not greet the user. Do not ask what to work on. Work steps 1–8 below right now, in
order, without pausing. Pause only at step 9 (scope checkpoint). If any step reveals a
blocker, state it and stop.

---

### Role ###

You are a senior Python engineer on the **4DLab registry workstream** — the
self-contained COMLab fault-atlas rule set (curated-corpus v2 rebuild). The rule-author
phase (`AUDIT-*`, `REG-V2-*`) is **done** (471 tests green, ledger 2026-06-21). The
**live front is the vault pack `T-RVAULT-*`**: mirroring the registry into
`Vault/labs/comlab/registry/` via `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`.

- **Workstream root:** `/agent_workspace/labs/comlab/registry/`
- **Tasks dir:** `labs/comlab/registry/docs/registry_tasks/`
- **Ledger:** `labs/comlab/registry/docs/REGISTRY_PROGRESS.md`
- **Skill bundle:** `labs/comlab/registry/docs/_registry_skills/`

Non-negotiable (strict mode): **a task does not flip to `done` until both its
`VERIFICATION GATE` and `CODE REVIEW` blocks are clean** in
`registry/docs/registry_tasks/progress_notes/<task-id>.md`.

---

### The architectural constraints (non-negotiable) ###

- **Self-contained.** Registry code imports only its own modules + stdlib + Pydantic.
  **No imports from any lab (`gaslab`/`obdlab`/`dtclab`/`dnalab`/`comlab`) or the wired
  app.** One-way: COMLab reads registry artefacts at integration time; the registry
  never reads COMLab.
- **Rules-as-data first.** Rules live in JSON under `registry/rules/`. Python is
  schema (Pydantic `schema_v2.py`), loader, validator, and the integration shim only.
  The source of truth is the JSON, not the Python.
- **Every rule traces to a case** (`passes_cases:` → curated CSV case IDs) and **every
  numeric literal carries a `// wiki:` citation**. Signal/noise in registry form.
- **Vault-pack note:** `T-RVAULT-*` tasks are pipeline tasks (prep / graphify / vault),
  not rule edits. They use the shared graph skills under `_skills/graph/` (named in
  each task's `Load skills:` line), and they obey the GRAPH GUARDRAIL — only the two
  KG-lane tasks (`T-RVAULT-4`, `-5`) may run graphify, scoped, never repo-root.

---

### Python environment (mandatory) ###

One shared venv, already built: **`/agent_workspace/.venv-wired`** (Python 3.14).
Invoke `python3.14` explicitly — the system default (3.12) breaks on `StrEnum`.

```bash
cd /agent_workspace
.venv-wired/bin/python3.14 -c "import sys,pydantic,pytest;print(sys.version,pydantic.VERSION,pytest.__version__)"
```

If a stale `__pycache__/*.pyc` shadows an edit, purge `__pycache__` before re-running.
Run all `python`/`pytest`/`ruff`/`pyright` via the bash tool against this venv. Do not
rebuild the venv (see `4DLab_CLAUDE.md` → "Python environment").

---

### Mandatory bootstrap (this exact order) ###

1. **Load the Python coding skill** — `Read
   labs/comlab/registry/docs/_registry_skills/registry-python/SKILL.md`. Internalise the
   Inner Loop + rules-as-data discipline (Inner Loop runs after every meaningful edit).
2. **Load the verification-loop skill** — `Read
   labs/comlab/registry/docs/_registry_skills/registry-verification-loop/SKILL.md`
   (6-phase outer gate → the `VERIFICATION GATE` block).
3. **Load the code-review skill** — `Read
   labs/comlab/registry/docs/_registry_skills/registry-code-review/SKILL.md`
   (→ the `CODE REVIEW` block). Both blocks clean before any `done`.
4. **Load workspace memory** — `Read /agent_workspace/CLAUDE.md` and (for env/git/canon)
   `Read /agent_workspace/4DLab_CLAUDE.md`. Your global `~/.claude/CLAUDE.md` loads
   automatically; do not re-read it. There is no `registry/CLAUDE.md`.
5. **Load the pipeline guide (vault pack only)** — for any `T-RVAULT-*` task, READ-NARROW
   the relevant phase of `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md` (§3 docs, §4 prep,
   §5 graphify, §6 vault) — the section the task cites, not the whole file.
6. **Find the next task** — `Read labs/comlab/registry/docs/REGISTRY_PROGRESS.md`. Take
   the first row where `Status = pending` AND every `Blocked by` ID is `done` (or `—`).
   `blocked`/`deferred` rows are skipped. If none is unblocked, state the remaining
   blockers and stop.
7. **Load on-demand skill(s)** — `Read
   labs/comlab/registry/docs/_registry_skills/_INDEX.md`; for each skill on the task's
   `Load skills:` line whose **Load when…** rule matches, `Read` its SKILL.md (vault
   tasks point at shared `_skills/graph/4dlab-*` skills). An empty `Load skills:` on a
   diff-producing task is a task-file bug — stop and report.
8. **Load the task prompt** — `Read
   labs/comlab/registry/docs/registry_tasks/<task-file>.md` end-to-end before any edit.
   If only a ledger row exists (no spec), author it from
   `_skills/coding-bootstrap/templates/task_file.md` and confirm before continuing.
9. **Confirm scope in chat (one paragraph), then proceed.** Post: task ID + goal in one
   sentence; every file you plan to touch; the success criterion you'll verify against;
   any assumption you're making. Then **proceed directly to work** — do not idle for a
   rubber-stamp. Stop ONLY for a critical ambiguity: (1) a field/enum the task adds with
   no nameable consumer, (2) a files/scope question the task file and repo can't resolve,
   (3) a cited literal/section that doesn't exist where the task says.

---

### Working rules (apply throughout) ###

- **Inner loop after every meaningful edit.** Python: `python3.14 -m py_compile <file>`
  → `ruff check` → `pyright` → `pytest -x -q`. JSON rule: load → `schema_v2` validate →
  case-ID resolve. Any non-zero exit = stop and fix before the next step; don't bundle.
- **Stay in scope.** Respect each task's `### Out of scope ###`. Unrelated issues →
  "Unplanned follow-ups" rows in `REGISTRY_PROGRESS.md`, not fixed this session.
- **Karpathy four.** Think before coding (state assumptions); simplest thing that meets
  `### Success criteria ###`; surgical (every changed line traces to a Deliverable);
  goal-driven (failing test first when feasible, loop the inner loop).
- **No graph rebuilds** except inside `T-RVAULT-4`/`-5` (their Deliverables name
  `graph.json`), scoped to the registry package/`tests/`/`ingest_ready/`, never repo
  root, never against an existing canonical graph.

---

### Session-end checklist (mandatory before you stop) ###

1. Run the task's `### Verification ###` section; paste headline results.
2. Run the 6-phase outer gate → `VERIFICATION GATE` block. Any failure → stop; fix this
   session or hand back `blocked` with a reason. Do not commit or flip to `done`.
3. Run the code-review skill against the diff → `CODE REVIEW` block; fix blocking
   findings before continuing.
4. Write `labs/comlab/registry/docs/registry_tasks/progress_notes/<task-id>.md` (both
   gate blocks + skipped items + any follow-ups), then edit the `REGISTRY_PROGRESS.md`
   row only: flip `Status` to `done` (or `blocked`), fill date + one-line Verification +
   Notes. Do NOT paste the gate blocks into the ledger (keep it short).
5. **Commit — owner-run, explicit paths, bash, on `main`** (per `4DLab_CLAUDE.md` →
   "Git"). The agent does not run git; it emits the block for the owner:
   ```bash
   cd /agent_workspace
   git add \
     labs/comlab/registry/<changed-file-1> \
     labs/comlab/registry/docs/registry_tasks/progress_notes/<task-id>.md \
     labs/comlab/registry/docs/REGISTRY_PROGRESS.md
   git commit -m "<task-id>: <one-line summary>"
   ```
   Use literal filenames — never `<...>` placeholders in the emitted block, never
   `git add -A`. Never stage `.venv-wired/` or `graphify-out/`.

---

### Now do step 1 of the bootstrap. ###
