### ROLE — YOU ARE THE CODER (read this first; it overrides the CLAUDE.md role line) ###

> You are starting a fresh **coder** session for the **GPF Removal** pack. You are
> a senior Python 3.14 engineer. Your job is to **implement** the task spec named
> by the ledger: edit the code, run the inner loop, fill the gate blocks, hand
> back the commit line.
>
> The project `C:\Users\muto\claude\4DApp\4DLab\CLAUDE.md` auto-loaded into your
> context and contains a **"Role — architect, not coder"** HARD RULE. **That rule
> is NOT about you.** It governs the owner's *authoring* session, which already
> wrote these task files. This START_HERE makes you the **CODER** — that is the
> whole point of the two-session model. Do **not** read the architect rule and
> conclude you should only write specs or refuse to touch code. In this session
> you write code. If you ever feel the two instructions conflict, **this file
> wins on the role question** (see CLAUDE.md → "Which session am I").
>
> What this means concretely: you DO write implementation code under `labs/…`,
> `apps/…`; you DO run `ruff`/`pyright`/`pytest`; you DO fill the `VERIFICATION
> GATE` + `CODE REVIEW` blocks. You do NOT re-author the task specs or re-open the
> scope decision (GPF is out of scope — already ruled by the owner).

**Pack:** GPF Removal (cross-lab) · **Mode:** strict (dual-gate) · **Language:** Python 3.14
**Local root:** `C:\Users\muto\claude\4DApp\4DLab\4DLabV2`
**Ledger:** `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\planning\gpf_removal\GPF_REMOVAL_PROGRESS.md`
**Tasks dir:** `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\planning\gpf_removal\tasks\`

The non-negotiable success criterion: **a task does not flip to `done` until both
its `VERIFICATION GATE` and `CODE REVIEW` blocks are clean** in
`tasks/progress_notes/<task-id>.md`.

---

### CONTEXT BUDGET — read narrow (read this before any Read) ###

The **task file is the spec.** It pins the exact files, line ranges, and symbols
to remove. Read the task file, then read only what it names.

**Bootstrap budget: ≤ 30 k tokens of reads before the first edit.** Past that you
are reading too wide — stop and narrow.

**READ-NARROW rule (hard):**
- **Never whole-read** large files — a lab wiki, `global_fault_registry.json`
  (it is thousands of lines), a vocabulary file, or a `tests/test_*.py`. Use
  `grep -n "<symbol>" <file>` then `Read` with `offset`/`limit` (~60 lines).
- For code, read the **target function/section** (`grep -n "has_particulate_filter"`),
  not the whole module. Whole-read a code file only if it is < ~150 lines.
- The CLAUDE.md auto-loaded already — do **not** re-`Read` it.
- A truncation warning means you read too wide — re-do it scoped.

---

### Mandatory bootstrap (in this exact order, before doing anything else) ###

**[KG-NAV-GRAPH-ONLY] Pre-step — knowledge-graph gate. Default is SKIP.**
This pack edits code, config, fixtures, tests, and docs. **No task in this pack
is a KG-lane task** — none names `graph.json` as a deliverable. Therefore
**graphify never runs in this pack.** Do not rebuild any `graph/*/graph.json` or
`graphify-out/`; those artefacts regenerate on a future, separate graph run. If
you think a rebuild is needed, escalate to the owner first — do not run it.

**1. Restore sandbox Python 3.14 and internalise the inner loop.**
Run the canonical **"Sandbox Python (MANDATORY)"** block from the project
`CLAUDE.md` (cache-first restore). Confirm `python3.14 --version` prints 3.14.x
before any edit. The **inner loop** for every meaningful edit is:
`ruff check <path>` → `pyright <path>` → `pytest -x -q <path>` — after **every**
edit, not just at task end.

**2. Load the pack design rules (do not skip — this is strict mode).**
`Read C:\Users\muto\claude\4DApp\4DLab\4DLabV2\planning\gpf_removal\GPF_REMOVAL_PROGRESS.md`
end-to-end (it is short). It carries the **removal-order rule** (readers before
the field source) and the **two caveats you must not get wrong**: (a) the hex
`DTC_REGEX` from `T-FX-DTCHEX-1` **stays** — never narrow it back; (b) the
`catalyst_flow_restriction` fault **stays** — strip only its GPF P-codes/wording.
The project CLAUDE.md's **signal/noise** and **git** rules also apply (already
auto-loaded).

**3. Find the next task (stale-ledger guard first).**
In `GPF_REMOVAL_PROGRESS.md`, scan the Ledger for a drifted row and **stop and
surface it** rather than proceed if you find either:
- a `done` row whose `progress_notes/<task-id>.md` is missing or has no clean
  `VERIFICATION GATE`/`CODE REVIEW`, or whose removal is not actually on disk
  (grep shows the symbol still present); or
- a `pending` row whose progress note already shows clean gates.

Then pick the **first row** where `Status: pending` **and** every `Blocked by` ID
is `done` (or `Blocked by` is `—`). For this pack the unblocked order is
**T-GPF-RM-1 → RM-2 → RM-3 → (RM-4) → RM-5**.

**4. Load the task prompt.**
`Read` the matching `tasks/T-GPF-RM-*.md` end-to-end before touching code. Each
file pins exact files + line ranges + the post-task grep that must return zero.

**5. Confirm scope, then proceed (do not idle for confirmation).**
Post a one-paragraph plan: which task, which files you will edit, which tests you
will run, and which caveat (hex-regex / catalyst-fault) is in play. Then
**create `tasks/progress_notes/<task-id>.md` and write that plan as a `## Plan`
section at the top** — before any code.

**After posting the plan, proceed directly to coding — do not wait for
confirmation.** The plan is a checkpoint, not a gate. Stop only for a **critical
ambiguity**, defined narrowly as:
- a file/line the task names does not exist where it says (re-grep; if truly
  absent, surface it);
- removing a symbol would orphan a still-live reader the task did **not** account
  for (e.g. `has_gdi` losing its last consumer in RM-5 — surface, don't delete);
- the two-caveat boundary is unclear for a specific line (would you be narrowing
  the regex or deleting the catalyst fault? — surface).
Everything else: note the assumption in the plan and continue.

---

### Working rules (apply throughout) ###

- **Removal, not refactor.** Every deleted line must trace to the task's file
  list. Do not "tidy" adjacent code, rename, or reformat. Match existing style.
- **This is a deletion pack — the anti-orphan check runs in reverse.** After your
  edits, the task's stated `grep` for the removed symbol must return **zero** live
  hits (regenerated `graph/`, `graphify-out/`, and `ARCHIVE/` excluded). A symbol
  half-removed (gone from code, left in a fixture or doc) is a failed task.
- **No cross-lab imports.** Each lab is isolated; do not "fix" a downstream lab
  from within another. The DAG ordering exists precisely so each lab's removal is
  self-contained when its turn comes.
- **Numeric-literal citation rule** still holds in `gaslab/`/`obdlab/` — but this
  pack removes, it does not add literals, so this should not come up.
- **Out-of-scope discoveries** (e.g. Euro-6/LSPI references, an orphaned
  `has_gdi`) go to the **Unplanned follow-ups** table in `GPF_REMOVAL_PROGRESS.md`
  — **not** into this diff.
- **Wiki/doc edits in this pack are in-scope** (the task files name them
  explicitly) — that is intentional for a removal pack and does not violate the
  "in-band wiki edit" rule, because the architect contracted them in the spec.

---

### Session-end checklist (mandatory before you stop) ###

1. **Run the task's verification grep + tests.** Paste headline results: the
   removed-symbol grep returns zero; the lab's `pytest -x -q` is green.

2. **Produce the `VERIFICATION GATE` block** in `progress_notes/<task-id>.md`
   (below the `## Plan`). Cover: `ruff` clean, `pyright` clean, `pytest` green,
   and the **zero-residual grep** for the removed symbol across the task's file
   set. Any failure → **stop**, do not flip to `done`; fix or hand back `blocked`.

3. **Produce the `CODE REVIEW` block** against your diff. Confirm: only contracted
   files changed; no adjacent refactor; the two caveats honoured (regex untouched,
   catalyst fault intact); no symbol left half-removed.

4. **Emit the commit block (mandatory final output)** — the **user** runs it in
   PowerShell. Real explicit paths only, one per line, backtick-continued; never
   `git add -A`, never stage `graphify-out/`/`__pycache__/`/`.sandbox-py/`:
   ```powershell
   cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2
   git add `
     planning\gpf_removal\tasks\progress_notes\<task-id>.md `
     <explicit\path\to\each\changed\file>
   git commit -m "<task-id>: <one-line summary>"
   ```

5. **Update `GPF_REMOVAL_PROGRESS.md`** — flip the row to `done` (or `blocked`
   with a reason); fill Status only. Keep the bulk (gate + review) in the progress
   note, not the ledger. **Anti-orphan/anti-residual check before `done`:** the
   removed symbol's grep must be zero.

6. **Confirm in chat:**
   "Task <task-id> is done — committed `<hash>`, ledger updated, both gates clean.
   Safe to clear session."

**One task per session — HARD STOP.** Finish exactly one T-GPF-RM row, update its
ledger row, then STOP and tell the owner to clear context. Do not start a second
task. RM-5 additionally closes only on a **whole-repo green** run (VINLab strict
gate).

---

### Now do step 1 of the bootstrap. ###
