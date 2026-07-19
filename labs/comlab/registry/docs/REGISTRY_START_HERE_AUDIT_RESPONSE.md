# Response to coder audit of `REGISTRY_START_HERE.md`

**Author:** assistant (verification pass)
**Date:** 2026-05-28
**Source under review:** `C:\Users\muto\claude\4DApp\4DLab\registry\REGISTRY_START_HERE.md` (239 lines)
**Input:** coder's 20-item ambiguity report + 6-item priority list

Per user feedback memory ("verify-relayed-diagnoses"), every finding below was
checked against the source file and against the surrounding repo state before
agreeing. Verdicts: **Valid** = real, applies as stated. **Partial** = real but
narrower / wider than the coder framed it. **Invalid** = the claim does not hold
once the source is read carefully.

---

## Verification table

| # | Coder claim | Verdict | One-line rationale |
|---|---|---|---|
| 1 | "1–9 without pausing" vs. "wait at step 9" | **Valid** | Header (L3–4) and step 9 (L156) literally collide. |
| 2 | Step 8 fallback is a second un-anticipated pause | **Valid** | L144–146 introduces a second `ask the user to confirm` not covered by the header. |
| 3 | Who runs the venv check — PowerShell or bash? | **Valid** | L58–64 powershell block has no addressee; only inferable from `4DLab/CLAUDE.md`. |
| 4 | Inner-loop interpreter unspecified | **Valid** | L163–164 names tools but no interpreter; sandbox `python3.14` ≠ `.venv-wired\python.exe`. |
| 5 | "any lab" wording singles `comlab` out | **Partial** | L33 is grammatically correct; the friction is cosmetic, not a real ambiguity. |
| 6 | "Petrol-only, v1" — which v1? | **Valid** | Adjacent registry-v1/v2 usage makes this ambiguous on first read. |
| 7 | `schema_v2` location not stated | **Partial — but stale, not missing** | `registry/schema_v2.py` **already exists** (REG-V2-SCHEMA shipped). The stale text is L166 `"(once schema exists)"`, not the missing pointer. |
| 8 | `passes_cases:` / `// wiki:` in "JSON" | **Valid** | `//` line comments and bare `key:` are not strict JSON. Either the format is JSONC or the example syntax is misleading. |
| 9 | "Threshold" not defined | **Partial** | L48–49 already narrows it to "Numeric literals"; the heading word "threshold" mismatches. Worth a one-line tighten. |
| 10 | Which `CLAUDE.md` files exist? | **Valid** | Confirmed: `registry/CLAUDE.md` does **not** exist. The bootstrap should say "these two are the complete set." |
| 11 | "or —" — em-dash convention undefined | **Partial** | True but trivial; one-sentence clarification suffices. |
| 12 | Template lives outside registry → violates "self-contained" | **Invalid** | L32 defines "self-contained" *strictly via Python imports* ("Registry tooling imports only its own modules + stdlib + Pydantic"). Reading a markdown template is not an import. The path resolves (verified). No real collision. |
| 13 | "Audit-only" defined by example | **Valid** | L137 conflates "empty `Load skills:`" with "audit-only." A non-audit task with an empty line would silently skip skill loading. |
| 14 | Session-end `git add` block tagged `bash` | **Valid — scope expanded** | The shell-tag fix is correct, but the real per-session friction is a **two-round-trip** flow (agent writes `<COMMIT_HASH>` placeholder → user commits → user pastes hash back → agent patches ledger → session closes). Edit 11 below now collapses both round-trips into one PowerShell paste. |
| 15 | Final confirm string quoting style | **Invalid (not worth a fix)** | Markdown renders the backticks correctly; agent emits the line into chat, not as code. No functional effect. |
| 16 | Timestamped jaeger path will break if pruned | **Valid** | Confirmed path exists today (`...20260527-044325/...`). A short "do not prune" comment is cheap insurance. |
| 17 | Banned `v2/` path vs. "registry v2" workstream name | **Valid** | Same literal in two meanings. Disambiguate by scoping the ban to a concrete repo subpath. |
| 18 | "Pydantic schema" could be misread as "Python rules" | **Partial** | Current text is correct but dense; one tighten line removes the trap. |
| 19 | Inner loop has no explicit fail-stop rule | **Valid** | L163–166 lists steps but doesn't say non-zero exit = stop. The skill probably does, but the bootstrap shouldn't depend on a downstream read. |
| 20 | "Every file you will touch" pre-exploration | **Valid** | L151 demands enumeration before the agent has read code. Soften to "currently plan to touch" + allow updates. |

**Counts:** Valid 12 · Partial 5 · Invalid 2 · "trivial — skip" 1.

---

## Two findings I disagree with (and why)

### #12 — "Template path violates self-contained rule" — **Invalid**

The coder reads "the registry is self-contained" as a global rule covering all
file references. The actual definition immediately following (L32–34) is
strictly about **Python imports**: *"Registry tooling imports only its own
modules + stdlib + Pydantic."* The template at
`_skills/coding-bootstrap/templates/task_file.md` is a markdown skeleton read
by the human-in-the-loop bootstrap, not imported by registry tooling. The
path resolves (verified). No fix needed.

*Optional softening*: rephrase L32 as **"The registry's Python is
self-contained"** so the rule's scope is unambiguous on first read. This is
preventive, not corrective.

### #15 — Quoting style of the final confirm string — **Skip**

The straight-quoted string with embedded backticks (L233–234) renders fine in
markdown and is intended to be pasted into chat. No functional issue.

### #7 — "Define schema_v2" — **Partial; the real issue is different**

The coder thought `schema_v2` was a forward reference with no defined location.
**It already exists** at `C:\Users\muto\claude\4DApp\4DLab\registry\schema_v2.py`
(REG-V2-SCHEMA is done; `registry/registry_tasks/progress_notes/REG-V2-SCHEMA.md`
confirms). The stale text is on L166:

> `JSON rule file: json.load → schema_v2 validate (once schema exists) → case-ID resolve`

The `(once schema exists)` parenthetical was written when the schema did not
yet exist and should now be removed. The coder's recommended fix ("until then,
validators are stubs") would re-introduce a stale state. Replace with a
positive pointer instead — see edit below.

---

## Proposed exact edits

Each block names the rule, the **old** text (verbatim from source), and the
**new** text. Apply them in order. None of them touch other content.

### Edit 1 — Header (fixes #1)

**Old (L3–5):**
```
Do not greet the user. Do not ask what to work on. Work through steps 1–9
below **right now, in order, without pausing between them**. Your first
user-visible output is the scope confirmation paragraph at step 9.
```

**New:**
```
Do not greet the user. Do not ask what to work on. Work through steps 1–8
below **right now, in order, without pausing between them**. Pause for user
confirmation at step 9 (and only at step 9, unless step 8 triggers its
written-spec fallback — see step 8).
```

Addresses #1 and #2 together.

### Edit 2 — Step 0 addressee for the venv check (fixes #3)

**Old (L58–64):**
```
```powershell
cd C:\Users\muto\claude\4DApp\4DLab
.\.venv-wired\Scripts\activate

# Confirm Python 3.14 + Pydantic v2 + pytest are present
.\.venv-wired\Scripts\python.exe -c "import sys, pydantic, pytest; print(sys.version, pydantic.VERSION, pytest.__version__)"
```
```

**New:** (insert a one-line caption before the fenced block)
```
**The user runs this in Windows PowerShell** — the agent does not activate
or rebuild venvs from the bash sandbox:
```powershell
cd C:\Users\muto\claude\4DApp\4DLab
.\.venv-wired\Scripts\activate

# Confirm Python 3.14 + Pydantic v2 + pytest are present
.\.venv-wired\Scripts\python.exe -c "import sys, pydantic, pytest; print(sys.version, pydantic.VERSION, pytest.__version__)"
```
```

### Edit 3 — Name the inner-loop interpreter (fixes #4)

**Old (L163–166):**
```
**Inner loop — after every meaningful edit (not just at task end).**
- Python file: py_compile → ruff → pyright → pytest -x -q
- JSON rule file: json.load → schema_v2 validate (once schema exists) →
  case-ID resolve
```

**New:**
```
**Inner loop — after every meaningful edit (not just at task end).**
Agent runs the inner loop in the **sandbox `python3.14`** (installed per
`4DLab/CLAUDE.md` § Sandbox Python). Venv work (`.venv-wired`) is
user-only and stays in PowerShell.

- Python file: `python3.14 -m py_compile <file>` → `ruff check` →
  `pyright` → `pytest -x -q`
- JSON rule file: `json.load` → `schema_v2` (validator at
  `registry/schema_v2.py`) → case-ID resolve

**Any non-zero exit from any inner-loop step = stop and fix before the next
step.** Do not bundle fixes.
```

Addresses #4, #7 (real issue), and #19 in one edit.

### Edit 4 — Lab-list wording (fixes #5)

**Old (L33–34):**
```
**No imports from any lab (`gaslab`,
`obdlab`, `dtclab`, `dnalab`), from `comlab`, or from `4DLabWired`.** The
```

**New:**
```
**No imports from any lab — `gaslab`, `obdlab`, `dtclab`, `dnalab`,
`comlab` — or from `4DLabWired`.** The
```

Optional softening only; the original is technically correct.

### Edit 5 — Disambiguate "v1" (fixes #6)

**Old (L176):**
```
- Petrol-only, v1.
```

**New:**
```
- Petrol-only (4DApp product v1, per `PRD_4D_App.md` §5 — *not* registry
  v1/v2 versioning).
```

### Edit 6 — JSON-with-comments format (fixes #8)

**Old (L38–49):** the block from `**Rules-as-data first.**` through
`carry a \`// wiki: <FILE> §<n>\` comment naming the wiki source.`

**New — add this sentence at the end of the block:**
```
**Rule file format:** files under `registry/rules/` are **JSONC**
(JSON with `//` line comments). The registry loader strips comments before
`json.load`. Strict-JSON tooling will reject these files; use the registry
loader, not raw `json.load`, when reading rules.
```

### Edit 7 — Tighten "threshold" → "numeric literal" (fixes #9)

**Old (L48–49):**
```
**Every threshold carries a wiki citation.** Numeric literals in rules
carry a `// wiki: <FILE> §<n>` comment naming the wiki source.
```

**New:**
```
**Every numeric literal carries a wiki citation.** Numeric literals
(thresholds, integer counts, percentages, durations) in rules carry a
`// wiki: <FILE> §<n>` comment naming the wiki source. String enums and
arrays of IDs do not require citations.
```

### Edit 8 — `CLAUDE.md` set is complete (fixes #10)

**Old (L106–112):**
```
**4. Load workspace memory.**
```
Read C:\Users\muto\claude\4DApp\CLAUDE.md
Read C:\Users\muto\claude\4DApp\4DLab\CLAUDE.md
```
The workspace `CLAUDE.md` files carry user preferences (reports always
in .md; document readability gate; no `.docx`/`.pdf` unless overridden).
```

**New:** add a sentence after the existing closing line:
```
These two files are the **complete `CLAUDE.md` set** for this workstream
— there is no `registry/CLAUDE.md`. The agent's global
`~/.claude/CLAUDE.md` (user rules) is loaded automatically and does not
need to be re-read here.
```

### Edit 9 — Define the `—` convention (fixes #11)

**Old (L127–129):**
```
First row where `Status = pending` AND every ID under `Blocked by` is
`done` (or `—`). If no unblocked task exists, state which blockers
remain and stop.
```

**New:**
```
First row where `Status = pending` AND every ID under `Blocked by` is
`done`, or the `Blocked by` cell is `—` (em-dash, meaning no blockers).
If no unblocked task exists, state which blockers remain and stop.
```

### Edit 10 — "Audit-only" decoupled from "empty skills line" (fixes #13)

**Old (L136–137):**
```
For each skill in the task's `Load skills:` line whose **Load when…**
rule matches, `Read` that skill's SKILL.md. If the task's `Load skills:`
line is empty (audit-only tasks), skip this step.
```

**New:**
```
For each skill in the task's `Load skills:` line whose **Load when…**
rule matches, `Read` that skill's SKILL.md. If the `Load skills:` line is
literally empty, skip this step — but verify the task is genuinely
audit-only (no diff produced). A coding task with an empty `Load skills:`
line is a bug in the task file; stop and report it instead of proceeding
unequipped.
```

### Edit 11 — Commit + ledger patch in one paste (fixes #14, eliminates hash-paste-back round-trip)

**Why this is bigger than the original #14:** the original audit only asked to
mark the shell as PowerShell. In practice the workflow has a second pain
point: the agent writes a `<COMMIT_HASH>` placeholder in the ledger, the user
commits and pastes the hash back, the agent then re-edits the ledger to
substitute the hash, *then* the session can close. Two round-trips across the
host/sandbox boundary. Architecture forces **one** paste (top-level `.git` is
not in the sandbox mount — only sub-repos like `COMLab/.git` and `GASLab/.git`
are visible). This edit collapses both round-trips into that one paste by
letting PowerShell do the substitution.

**Old (L196–234, entire `### Session-end checklist` section):** the full
"Session-end checklist (mandatory before you stop)" block as currently
written.

**New (replace the whole section):**
```
### Session-end checklist (mandatory before you stop) ###

1. **Run the task's `### Verification ###` section.** Paste headline results.

2. **Run the verification-loop 6-phase outer gate.** Produce the structured
   `VERIFICATION GATE` block. If any phase fails, **stop** — do not commit,
   do not flip the task to `done`. Either fix in this session, or hand
   back with status `blocked` and a reason.

3. **Run the code-review skill** against the diff. Produce the `CODE REVIEW`
   block. If it surfaces any blocking finding, stop and fix before continuing.

4. **Write the progress note + ledger row (agent does both, from sandbox).**

   a. Write `registry/registry_tasks/progress_notes/<task-id>.md` containing:
      - The full `VERIFICATION GATE` block.
      - The full `CODE REVIEW` block.
      - Which checklist items were skipped, with reason.
      - Any unplanned follow-up rows.

   b. Edit `REGISTRY_PROGRESS.md` task table only — keep it short:
      - Flip the task's `Status` to `done` (or `blocked` with a reason).
      - Fill `Date`, `Verification` (one-line summary), `Notes`.
      - In the `Commit` cell, write the **literal string** `<COMMIT_HASH>`
        (angle brackets included). The PowerShell block in step 5 replaces
        it. Use exactly this literal once per session — no extra occurrences.

   **Do NOT paste VERIFICATION GATE or CODE REVIEW blocks into
   `REGISTRY_PROGRESS.md` directly.** The task table must stay under ~120
   lines so it loads fast every session.

5. **Emit the commit-and-patch PowerShell block (agent emits; user pastes once).**
   Git is host-only — top-level `.git` is not reachable from the bash
   sandbox. The agent does **not** run `git`. The agent emits this exact
   block for the user to paste in **Windows PowerShell** at
   `C:\Users\muto\claude\4DApp\4DLab\`:

   ```powershell
   git add -A
   git commit -m "<TASK_ID>: <one-line summary from the task Deliverables section>"
   if ($LASTEXITCODE -eq 0) {
     $h = git rev-parse --short HEAD
     (Get-Content registry\REGISTRY_PROGRESS.md -Raw) `
       -replace '<COMMIT_HASH>', $h `
       | Set-Content registry\REGISTRY_PROGRESS.md -NoNewline
     Write-Host "Committed $h; ledger patched."
   } else {
     Write-Warning "Commit failed; ledger NOT patched. Fix the commit, then re-run only the patch lines."
   }
   ```

   Substitute `<TASK_ID>` and the one-line summary into the `git commit -m`
   message before emitting. Do **not** substitute `<COMMIT_HASH>` inside
   the `-replace` argument — that literal must reach PowerShell unchanged
   so it matches the placeholder the agent wrote into the ledger in step 4.

6. **Confirm in chat and close — no hash round-trip:**
   "Task <TASK_ID> ready to commit. Progress note written, ledger row
   updated with `<COMMIT_HASH>` placeholder. Paste the PowerShell block
   above; it commits and patches the ledger in one step. Session closes
   after you run it — no need to send the hash back."
```

**Notes for the coder applying this edit:**
- This single edit covers the original #14 (PowerShell shell tag) and the
  newly-surfaced two-round-trip issue. There is no separate "Edit 16."
- After this edit lands, the bootstrap's session-end checklist grows by ~15
  lines. The trade is acceptable because it kills a recurring per-session
  friction.
- The `-replace '<COMMIT_HASH>', $h` works because angle brackets are not
  regex metacharacters. If the ledger ever needs a literal `<COMMIT_HASH>`
  for a different reason (it shouldn't), revisit this.

### Edit 12 — Mark canonical jaeger run (fixes #16)

**Old (L17–18):**
```
cases have all 53 rules pruned before evaluation (`4DLabWired/_jaeger/
runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md`).
```

**New:**
```
cases have all 53 rules pruned before evaluation (`4DLabWired/_jaeger/
runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md` — **canonical
v1 baseline; do not prune this run directory**).
```

### Edit 13 — Disambiguate banned `v2/` path (fixes #17)

**Old (L178):**
```
- No imports from `ARCHIVE/`, `ARCHIVECOMLab/`, `v2/`, or `v6/`.
```

**New:**
```
- No imports from the legacy directories `ARCHIVE/`, `ARCHIVECOMLab/`,
  `4DLab/v2/`, or `4DLab/v6/`. (The registry-v2 rebuild lives in
  `registry/` — that is **not** the banned `v2/`.)
```

### Edit 14 — Optional Pydantic-vs-JSON tightening (fixes #18)

**Old (L38–42):**
```
**Rules-as-data first.** Rules live in JSON files under `registry/rules/`.
Python in this workstream appears only as schema (Pydantic), loader,
validator, and the integration shim. There is no Python evaluation logic
inside rules — if a rule needs a new evaluation behaviour, the schema_v2
gets a new evidence-tier field.
```

**New (one-line insert after the second sentence):**
```
**Rules-as-data first.** Rules live in JSON files under `registry/rules/`.
Python in this workstream appears only as schema (Pydantic), loader,
validator, and the integration shim. **Pydantic models validate the JSON;
the source of truth is the JSON, not the Python.** There is no Python
evaluation logic inside rules — if a rule needs a new evaluation
behaviour, the schema_v2 gets a new evidence-tier field.
```

### Edit 15 — Soften "every file" pre-exploration (fixes #20)

**Old (L150–152):**
```
- The task ID and goal in one sentence
- Every file you will touch (create / modify / delete)
- The success criterion you will verify against
```

**New:**
```
- The task ID and goal in one sentence
- Every file you currently plan to touch (create / modify / delete). If
  scope shifts after exploration, post a one-line scope-update before the
  diff grows.
- The success criterion you will verify against
```

---

## Edits NOT proposed

| # | Why skipped |
|---|---|
| 12 | Coder's interpretation of "self-contained" is too broad. The rule is scoped to Python imports; the template path is fine. Optional softening of L32 wording is mentioned above but not edited here. |
| 15 | Quoting style has no functional effect. |

---

## Priority ranking (matches coder's framing, refined)

A fresh agent hits these in this order during the first 10 minutes:

1. **Edit 1** (header pause rule) — agent will literally not know when to stop.
2. **Edit 11** (commit + auto-patch flow) — kills the two-round-trip
   commit/hash-paste-back loop on **every** task close. Highest
   recurring-friction payoff; affects every session, not just the first.
3. **Edit 3** (inner-loop interpreter) — agent will pick a wrong Python and waste cycles.
4. **Edit 6** (JSONC format) — first rule-file write fails on strict JSON.
5. **Edit 2** (venv check addressee) — agent may try to activate venv in sandbox.
6. **Edit 13** (banned `v2/`) — confusion about workstream identity.

Everything else (Edits 4, 5, 7, 8, 9, 10, 12, 14, 15) is friction reduction —
worth doing in a single follow-up pass, not session-blocking.

---

## Recommended next action

Single follow-up task: `REG-BOOTSTRAP-CLARIFY` (new row in
`REGISTRY_PROGRESS.md`) — apply Edits 1–15 in one diff, verification gate =
"agent re-bootstraps cleanly with no clarifying questions on a dry run."
Suggested skills line: empty (this is a docs-only task; inner loop is N/A).
Out-of-scope for that task: any change to skills referenced from the
bootstrap, any change to the schema, any change to the task ledger format.
