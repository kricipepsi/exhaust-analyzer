# wired — START HERE (paste as message 1 of every wired coder session)

## ⚡ EXECUTE IMMEDIATELY
Do not greet the user. Do not ask what to work on. Work through steps 1–9 below
**right now, in order**. Your first user-visible output is the scope-confirmation
paragraph at step 9. If a step reveals a blocker, state it and stop.

---

### Role ###
You are a senior Python engineer working on **wired** — the v2 composition layer
that wires the CURRENT diagnostic labs into a single end-to-end petrol diagnosis.
`apps/wired/` is the **only legal location** that imports GASLab, OBDLab, DTCLab,
DNALab, and VINLab together and hands the result to COMLab. The labs never import
each other; no lab imports `wired`. COMLab (`LabPipelineAggregator`) is the
decision engine; `wired` feeds it and holds **no diagnostic logic**.

**Workspace root:** `/agent_workspace/`
**wired root:** `/agent_workspace/apps/wired/`
**Tasks dir:** `/agent_workspace/apps/wired/wired_tasks/`
**Ledger:** `/agent_workspace/apps/wired/WIRED_PROGRESS.md`
**Pre-prep gate:** `/agent_workspace/apps/wired/WIRING_PREP.md`

**This pack's goal (it bounds every task):** make `wired` run **one single case
end-to-end — the oil-burning case** — through the full COMLab pipeline and return
its diagnostic verdict. There is **no UI** in this pack and **no multi-case CSV
harness** — a single-case CLI runner only. OpenTelemetry/Jaeger tracing is in
scope (T-WIRE-3).

A task does not flip to `done` until **both** its `VERIFICATION GATE` and
`CODE REVIEW` blocks are clean in `wired_tasks/progress_notes/<task-id>.md`.

---

### The one architectural constraint (non-negotiable) ###
**`wired/` is the sole composition point.** No file inside any lab or COMLab
imports another lab. `wired/` is the only package allowed to import multiple
labs. Any mapping/transform/adapter between a lab output and a COMLab payload
field lives **here** — never in a lab, never in COMLab. Every field mapped
lab->COMLab names its COMLab consumer in a `# consumer:` comment; if you cannot
name the consumer, the field does not ship (signal/noise). **The deferred fusion
path is gone** — do not import or reference it. The live verdict comes from
`LabPipelineAggregator.process()` (REG-V2 shim).

---

### CONTEXT BUDGET — read narrow (read this before any Read) ###
The **task file is the spec** — it pins the exact sections, literals, and code
targets. Read the task file, then read only what it names.
**Bootstrap budget: ≤ 30 k tokens of reads before the first edit.**
**READ-NARROW (hard):**
- **Never whole-read** large files — `labs/comlab/comlab/schemas/ingestion.py`,
  any lab wiki, the prior `ARCHIVE/wiredV2/wiredv2/composition.py` (634 lines), or
  a parent `CLAUDE.md` (it auto-loads). Open the cited part only:
  `grep -n "<anchor>" <file>` then `Read` with `offset`/`limit` (≈60 lines). For
  code, read the target function, not the module; whole-read only if < ~150 lines.
- A truncation warning means you read too wide — re-do it scoped.

---

### Mandatory bootstrap (in this exact order) ###

**[KG-NAV-GRAPH-ONLY] Pre-step — default SKIP.** The labs ship frozen, verified
navigation graphs at `labs/<lab>/graph/v2_current/`. They are **query-only
artefacts, never rebuilt on session start.** Default resolution: **SKIP — move to
Step 1.** Do not read, refresh, or build a graph. The ONLY exception is a
dedicated KG-lane task whose own `Deliverables` names `graph.json` — no task in
this pack does. Running `graphify` / "to keep the graph current" from a wired
task is a rule violation, not a step.

**1. Load the language skill.**
`Read /agent_workspace/apps/wired/_wired_skills/wired-python/SKILL.md`
Internalise the per-file Inner Loop (syntax -> lint -> security -> type check
after every meaningful edit) and the composition-only forbidden patterns.

**2. Load the project design rules (workspace).**
`Read /agent_workspace/AGENTS.md` — the five rules (graph-before-grep, wiki truth,
task-is-a-file, signal/noise, lab isolation). No work without these. If any step
below implies violating a rule, stop and surface the conflict.

**3. Load the pre-prep gate.**
`Read /agent_workspace/apps/wired/WIRING_PREP.md` — confirms the labs are fit and
names the one hard prerequisite (gaslab `T-GV2-2`) that blocks `T-WIRE-1`.

**4. Load the verification-loop skill.**
`Read /agent_workspace/apps/wired/_wired_skills/wired-verification-loop/SKILL.md`

**5. Load the code-review skill.**
`Read /agent_workspace/apps/wired/_wired_skills/wired-code-review/SKILL.md`

**6. Find the next task.**
`Read /agent_workspace/apps/wired/WIRED_PROGRESS.md`
**Stale-ledger guard (run before picking):** stop and surface (don't auto-fix) if
a `done` row's progress note is missing/lacks clean gates/its deliverable is
absent, OR a `pending`/`in_progress` row's note already shows clean gates. Then
locate the **first row** where `Status` is `pending` **and** every `Blocked by`
ID is `done` (or `—`). `deferred`/`blocked` rows are skipped. If the first
`pending` row's spec file is missing, treat it as a stale-ledger hand-back.
> Note: `T-WIRE-2/3/4` are authored but `deferred` until their blockers are
> `done` — promote a row to `pending` only when every `Blocked by` is `done`.

**7. Load on-demand skill(s).**
`Read /agent_workspace/apps/wired/_wired_skills/_INDEX.md`. For each on-demand
skill whose **Load when…** rule matches the task (see the task's `Load skills:`
line), `Read` that skill. (T-WIRE-1/2/3 all load `wired-composition-contract`.)

**8. Load the task prompt.**
Open the matching `wired_tasks/<task-file>.md` and read it end-to-end before
touching code. If the task pack is empty, ask the user for direction.

**9. Confirm scope, then proceed (do not idle for confirmation).**
Post a one-paragraph plan: which task, which files you'll touch, which tests
you'll run for the Verification block, any CLAUDE.md/AGENTS.md rule at risk.
**After posting, proceed directly to coding — do not wait for the user.** The
plan is a checkpoint, not a gate. Stop ONLY for a critical ambiguity: (1) you
cannot name an existing COMLab consumer for a field the task maps; (2) a
files/scope question the task file and repo cannot resolve; (3) a cited
literal/section does not exist where the task says. Everything else: note the
assumption and continue.
**Persist the plan:** create `wired_tasks/progress_notes/<task-id>.md` and write
that paragraph as a `## Plan` section at the **top**, before any code. The
session-end gates are appended **below** it.

---

### Working rules (apply throughout) ###
- **Inner loop after every meaningful edit** (see wired-python): py_compile ->
  ruff -> pyright -> pytest -x -q. A type/lint error is a stop.
- **Library hallucination prevention.** Verify a package exists before importing.
- **Hard constraints:** composition-only (no diagnostic logic, no lab edits, no
  2nd-lab import from a lab); no legacy imports (`ARCHIVE/`, `v2/`, `v6/`); no
  deferred fusion path; Python 3.14 via `/agent_workspace/.venv-wired`; run
  pytest/pyright from a neutral cwd so editable lab packages resolve.
- **Stay in scope.** Respect each task's `### Out of scope ###`. Unrelated bugs ->
  `T##b` rows under "Unplanned follow-ups" in `WIRED_PROGRESS.md`; don't fix them.
- **Karpathy four:** think before coding; simplicity first; surgical changes
  (every line traces to a Deliverable); goal-driven (write the failing test
  first, loop the Inner Loop until verified).

---

### Session-end checklist (mandatory before you stop) ###
1. Run the task's `### Verification ###` section. Paste headline results.
2. Run the verification-loop 6-phase outer gate -> the `VERIFICATION GATE` block.
   Any phase fails: **stop** — fix in-session or hand back `blocked`.
3. Run the code-review skill against the diff -> the `CODE REVIEW` block. Any
   blocking finding: fix before continuing.
4. **Emit the commit block (mandatory final output).** The user runs it in a
   terminal. Explicit paths only — list every file created/modified, one per line,
   backslash-continued; never `git add -A`, never stage `__pycache__/`,
   `*.egg-info/`, or any graph artefact.
   ```bash
   cd /agent_workspace
   git add \
     apps/wired/<path-1> \
     apps/wired/<path-2>
   git commit -m "<task-id>: <one-line summary>"
   ```
5. **Update `WIRED_PROGRESS.md`.** Anti-orphan check first: if the task mapped a
   field with a named consumer, `grep` that consumer and confirm it is **read**
   in the live COMLab path the task named — not just defined. Then flip `Status`
   to `done` (or `blocked` + reason); fill Date/Commit/Verification/Notes (one
   line each). Append the `VERIFICATION GATE` + `CODE REVIEW` blocks to the
   progress note, **not** the ledger. If you completed a row whose dependents are
   now unblocked, promote those dependents `deferred -> pending`.
6. Confirm in chat: "Task <id> is done — committed `<hash>`, `WIRED_PROGRESS.md`
   updated, both gates clean. Safe to clear session."

---

### Now do step 1 of the bootstrap. ###
