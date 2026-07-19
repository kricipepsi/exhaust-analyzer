---
name: coding-bootstrap
description: >
  Build a complete v2-style coding-session infrastructure for any module or
  project, OR turn a monolithic build prompt into a half-session task pack a
  fresh Claude Code session can pick up and finish without re-priming. Load
  this skill whenever the user (a) says "prepare coding session for <X>",
  "set up <module>", "start <module>", "is <module> prepared for coding", or
  similar; (b) hands you a monolithic build prompt longer than ~150 lines;
  (c) asks to "break this into smaller subtasks"; (d) is starting a multi-task
  project and needs a bootstrap pattern so every session begins from the same
  place; or (e) mentions a "session reset", "fresh session", "context budget",
  "task pack", "coder tasks", or "session bootstrap". Apply proactively
  whenever a coding request will plainly exceed one session, and especially
  BEFORE authoring any monolithic bootstrap doc — that anti-pattern is exactly
  what this skill exists to prevent.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Coding Bootstrap Skill

This skill produces the **five-piece session infrastructure** that HFX, v2,
and COMLab all share, so every session starts the same way and no task
spills past half a context window:

1. **`_<module>_skills/`** — the per-module skill bundle: universal skills
   (mandatory at every session start) + on-demand domain skills (loaded when
   a task's surface matches). Has its own `_INDEX.md` master index.
2. **`<MODULE>_START_HERE.md`** — the bootstrap prompt pasted as message 1
   of every fresh session. Loads the right skills via `_INDEX.md`, finds the
   next pending task, fixes the working rules, defines the session-end gate.
3. **`<MODULE>_PROGRESS.md`** — a short task ledger: ID, status, blocked-by,
   commit hash. Stays under ~120 lines so it loads instantly every session.
   Includes an `Architect-level out-of-band patches` table for wiki/skill
   edits the architect applies directly. **Runnability convention:** `pending`
   means runnable now (spec authored, blockers `done`); forward-registered or
   unauthored placeholder rows stay `deferred`, never `pending` (or a
   `pending (...)` variant). The guard takes the first `pending` row top-to-bottom;
   `deferred`/`blocked` are skipped. This is what stops the guard from selecting an
   unauthored placeholder ahead of the real next task.
4. **`<module>_tasks/T-XX-N_<slug>.md`** — one file per ≤ 50%-context task.
   Each file is self-contained: Goal / Context (incl. `Load skills:` line) /
   Deliverables / Files to touch / Out of scope / Verification / Progress hook.
5. **`<module>_tasks/progress_notes/<task-id>.md`** — one file per task. It
   **opens with the confirmed `## Plan`** (written at task start, before any
   code), then gains the full `VERIFICATION GATE` + `CODE REVIEW` blocks at task
   end. Kept out of `PROGRESS.md` so the table stays small. This plan-at-top
   ordering is mandatory every session — see `templates/start_here.md`.

**The ignition — the project `CLAUDE.md`.** The five pieces above are inert
unless something loads `START_HERE.md` at session start. That something is the
project's root `CLAUDE.md` — the only file an agent loads with zero prompting
(it is auto-discovered up the directory tree). coding-bootstrap therefore also
generates or updates that `CLAUDE.md` (Step 4) with a per-session bootstrap
pointer. Without it the process is not self-running — every session has to be
told by hand to read `START_HERE.md`.

**Setup-once vs every-session.** coding-bootstrap is a *setup* skill: run it
**once** per project to lay down the infrastructure. After that, every coding
session is driven by the generated `CLAUDE.md` → `START_HERE.md` chain — this
skill is not re-read. Do not point ongoing coding sessions at coding-bootstrap;
point them at the project, and its `CLAUDE.md` does the rest.

The pattern is lifted from `v2/coder_tasks_v2/`,
which ran 41 V2 tasks across 7 phases without a single session overflow, and
mirrored in `HFX/_hfx_skills/` (13 skills, full diagnostic engine; off-mount
pre-migration example) and on-mount in `labs/comlab/_comlab_skills/` +
`labs/comlab/tasks/` (Phase 0b atomized into 7 task files after a failed first
attempt at a monolithic bootstrap).

---

## When to invoke

Trigger this skill on any of:

- The user pastes or names a monolithic build prompt (≥ ~150 lines, ≥ 5
  numbered steps).
- The user says "break this into smaller tasks", "split for context budget",
  "make a coder task pack", "bootstrap the project", or similar.
- The user is opening a multi-week coding project and asks how to lay it out.
- The user wants to apply the V2 bootstrap pattern to a different project.

Do **not** invoke for: single-edit fixes, one-shot scripts, prompts already
under 100 lines, or non-coding work (those don't need a session boundary).

---

## What you produce — step by step

### Step 0 — Read the source prompt and surface ambiguity

Before generating any file, `Read` the source prompt the user pointed you at.
Then post a short plan in chat:

- Which numbered steps you'll group into each task (and the rough size — file
  count, lines of code, tests).
- Which language skill applies (see `reference/per-language-skills.md`).
- Whether the module already has a `_<module>_skills/` bundle, or whether you
  need to build one (see Step 1).
- Whether you're using **strict** or **lite** rigor (see
  `reference/strict-vs-lite.md`).
- Anything ambiguous in the source prompt — **ask the user, do not guess.**
  Per CLAUDE.md: don't assume, surface tradeoffs.

Wait for the user to confirm the plan before writing files.

### Step 1 — Build the skill bundle (if it doesn't exist yet)

If the module already has a `_<module>_skills/` directory with a populated
`_INDEX.md`, skip to Step 2.

Otherwise, build the bundle now. Read `reference/skill-bundle-creation.md`
for the full procedure. In summary:

- Create `_<module>_skills/<module>-python/SKILL.md`,
  `_<module>_skills/<module>-verification-loop/SKILL.md`, and
  `_<module>_skills/<module>-code-review/SKILL.md` — the **three universal
  skills** every module needs. Adapt from `v2/_v2_skills/` (or `HFX/_hfx_skills/`;
  both off-mount pre-migration examples — the on-mount template is any lab's
  `labs/<lab>/_<lab>_skills/`).
  Re-scope each to the module's actual file paths, forbidden patterns,
  and design rules.
- Create `_<module>_skills/_INDEX.md` — the master index. Three sections:
  *Mandatory at every session start* / *On-demand domain skills* /
  *On-demand verification skills*. Every on-demand row has a **Load when…**
  column. This column is the contract between the task author and the coder.
- For now, the on-demand sections may be empty — domain skills get authored
  per task in Step 3 (see also `reference/custom-skill-authoring.md`).

**Evidence-based bundle composition (do this, not "load every coding skill").**
Before adapting the three universal skills, read `reference/skill-bundle-creation.md`
§2a — the controlled skill-eval (`ARCHIVE/skill_eval/skill_eval_final_report.md`)
that measured 37 skills A/B and found only ~5 measurably improve code. Two
consequences are load-bearing when you build a bundle: (1) the bundle floor is the
three universal skills **plus a structural-craft WARNING axis inside
`<module>-code-review`** — the two highest-effect skills (`improve-codebase-architecture`
*d*=1.79, `uncle-bob-craft` *d*=1.43) are structural craft and were *dropped* from
the first lab bundles; fold their checks in rather than repeating that miss; and
(2) do not pad the bundle with skills the eval marked out-of-scope or dead — they
are pure context cost. On-demand domain skills are the only additions, gated by the
Step 3 ≥3-task trigger.

### Step 2 — Break the prompt into tasks

Read `reference/breakdown-guide.md` and apply its sizing rules. The
half-session target is the constraint that drives every other decision:
each task must fit in ≤ 50 % of a fresh session's context (roughly 5–15
files touched, 200–600 lines of new/changed code plus tests).

**Domain-pattern shortcut.** If the source prompt describes building a static
knowledge graph from an authoritative source document (a wiki, a spec, an
ontology) into a callable diagnostic / classifier / rule-engine module, read
`reference/knowledge-graph-iteration.md` first — it gives you the 7-task
`P0 + 5 phases` shape (schema → extract → resolve → assemble → validate) and
the on-demand provenance skill the pattern almost always needs. The GASLab
build at `4DLab/GASLab/` is the worked example.

**Graph compilation prerequisite (T-PREP phase).** Before P0 can start on a
knowledge-graph module, the wiki must be extracted into a verified
`graphify-out/graph.json`. This is the **T-PREP phase** and it runs *before*
any task in this bootstrap. Read `reference/graph-compilation-guide.md` to
understand when T-PREP applies, how it feeds P1–P5, and the most common silent
failure (direction inversions). The 4dlab-graph skill lives at
`_skills/graph/4dlab-graph/SKILL.md` and
contains the full extraction + verification + patch toolchain. If the module
you are bootstrapping does not yet have a passing T-PREP, add T-PREP-1 as the
first task in the pack (before P0) and point it at that skill.

Also read `reference/code-quality-principles.md` once before drafting
deliverables — it folds together Karpathy's four LLM-coding rules and
the four architecture checks (depth, deletion test, seam discipline,
interface = test surface) that `Improve Codebase Architecture` keeps
surfacing *after* code ships. Running them up-front during breakdown is
how this skill prevents those findings.

Validate every proposed task against `checklists/breakdown-checklist.md`
before writing the file — the new `## Quality` section is the
mechanical version of the principles reference.

**Disclosure-first ordering.** Before you fix the dependency graph, ask of each
task: does it *disclose* a fact a later decision needs, or *commit* to a choice
that fact should inform? Put disclosure upstream and gate the commitment behind
it (`Blocked by`). If a single task does both, split it. For iterative packs the
owner runs step-by-step, author only the next runnable task in full and leave the
rest as forward-registered ledger rows. Full rule: "Why this works" constraint 4.

### Step 3 — Decide on-demand skills per task

For each task, ask: does any task in this phase need a custom on-demand
skill? Read `reference/custom-skill-authoring.md` for the trigger rules. In
short, author a custom on-demand skill when ALL of these hold:

1. The surface gates **≥ 3 atomic tasks**.
2. There is a non-obvious invariant the coder must apply (naming convention,
   forbidden pattern, design rule layer boundary, threshold table, schema
   convention).
3. The invariant is read-only authoritative — the coder consumes it, doesn't
   derive it.

If yes, author the skill at `_<module>_skills/<module>-<surface>/SKILL.md`,
add a row to `_INDEX.md`'s on-demand table, and reference it from the
relevant task files' `Load skills:` line.

If no, inline the rule in each task's `### Context ###` paragraph. Don't
author orphan skills.

### Step 4 — Generate the artefact pieces

Use the templates in `templates/` — they have placeholders in `{CURLY_BRACES}`
that you fill in:

| Piece | Template | Output path |
|---|---|---|
| Skill bundle | (built in Step 1) | `<project_root>/_<module>_skills/` |
| Bootstrap | `templates/start_here.md` | `<project_root>/<MODULE>_START_HERE.md` |
| Tracker | `templates/progress.md` | `<project_root>/<MODULE>_PROGRESS.md` |
| Task files (one per task) | `templates/task_file.md` | `<project_root>/<module>_tasks/T-<phase>-<n>_<slug>.md` |
| Progress notes folder | (folder + `README.md`) | `<project_root>/<module>_tasks/progress_notes/` |
| Ignition | `templates/claude_md.md` | `<project_root>/CLAUDE.md` (create, or insert the block if one exists) |

**Adding a pack to an existing project/lab (not a fresh bootstrap).** When the
project already has the five pieces and you are only appending a new task pack
to one module/lab, you still **create or refresh that module/lab's
`<MODULE>_START_HERE.md` paste-doc** — the user pastes it as message 1 of every
coder session, so a pack with no START_HERE is unstartable. Mirror the sibling
modules' existing START_HERE (house format) rather than the generic template, and
point it at the pack's `PROGRESS.md` + first unblocked task. Do not stop at task
files + ledger rows.

**The ignition (`CLAUDE.md`).** Generate the project's root `CLAUDE.md` from
`templates/claude_md.md`. If the project already has a `CLAUDE.md`, do **not**
overwrite it — insert the `## Session bootstrap` block and leave the rest. That
block is what makes the process self-running: it names the `START_HERE.md` a
session must read before doing anything else. On a full bootstrap run
`START_HERE.md` already exists, so delete the template's `## First-time setup`
section; keep that section only when `CLAUDE.md` is dropped in as a standalone
seed ahead of the rest of the infrastructure. Verify the block in Step 5.

Every task file is written using **prompt-engineering-master** principles —
specifically Principles 3 (break down), 8 (delimiters), 17 (output format),
21 (rich context), 25 (explicit requirements). See
`reference/prompt-rules-applied.md` for the per-section principle mapping.

The `### Success criteria ###` field added to every task file is the
tests-first contract from Karpathy P4 (goal-driven execution). The
`### Out of scope ###` paragraph now carries the surgical-change rule
(Karpathy P3) — both edits are described in
`reference/code-quality-principles.md`.

The `### Consumer (signal/noise) ###` field is **required on any task that adds
or widens a schema** (field, enum, fault, signal). It makes the project's single
governing constraint — every new field has a named, existing-or-proposed consumer
and code path — part of the **spec the architect writes**, not a question the
coder discovers mid-session. Authoring precision here is the actual handoff
bottleneck (status tracking is not); pinning the consumer up front is what keeps
the coder from stalling on START_HERE's critical-ambiguity stop.

### Step 5 — Cross-link and verify

After writing all files:

1. Open `<MODULE>_PROGRESS.md` and confirm every task ID listed has a
   matching `<module>_tasks/T-*.md` file (and vice versa).
2. Open `<MODULE>_START_HERE.md` and confirm every path it references
   exists — including each universal skill in `_<module>_skills/` and the
   `_INDEX.md`.
3. Open `_<module>_skills/_INDEX.md` and confirm every on-demand skill it
   lists exists on disk, AND that every `Load skills:` line in task files
   names skills that are in `_INDEX.md`.
4. Run `wc -l <MODULE>_PROGRESS.md` — must be < 120 lines (it gets re-read
   every session; bloating it taxes every future session).
5. Spot-check 1–2 task files against `checklists/breakdown-checklist.md`.
6. Open `<project_root>/CLAUDE.md` and confirm the `## Session bootstrap`
   block exists and points to the real `<MODULE>_START_HERE.md` path — this is
   the ignition; if it is missing or wrong, the project will not self-run.
7. **Placeholder-residue lint** — grep every generated file for unfilled
   template tokens: `grep -rnE '\{[A-Z][A-Z0-9_]{2,}\}' <MODULE>_START_HERE.md
   <MODULE>_PROGRESS.md <module>_tasks/ CLAUDE.md`. It must return nothing. A
   surviving `{TASK_ID}` / `{REPO_ROOT}` / `{DATE}` means a template placeholder
   was never filled — fix before handing back. (Ignore `{CURLY}` tokens that are
   legitimately literal, e.g. inside a fence documenting the template itself.)
8. **Skill under-authoring guard** (the inverse of item 3's orphan check).
   Tally each domain surface against the number of task files whose
   `### Context ###` inlines the *same* non-obvious invariant (naming rule,
   forbidden pattern, threshold table, schema convention). Any surface that
   inlines one invariant into >= 3 task files crossed the Step 3 threshold and
   should be a skill, not three copies — author/promote it, or record the
   explicit inline justification. Silent skips here are the recurring miss:
   item 3 catches authored-but-unused; this catches needed-but-skipped.

Report the deliverable summary in chat: file count, total lines, the first
unblocked task ID, and the per-surface skill decision (authored / inlined-because).
Stop. Hand back.

---

## Task file naming convention (MANDATORY)

Every task file and its ledger ID use the form:

```
T-<CODE>-<N>_<three_word_slug>
```

- **`<CODE>`** — the pack/phase code (e.g. `OBDV2`, `GAS`, `COM`, `TH`).
- **`<N>`** — the integer sequence within that code.
- **`<three_word_slug>`** — a **three-word, snake_case** descriptor of what the
  task does, appended after the code and number. Three words is the target (two
  is acceptable when a third adds nothing; never one, never a vague filler word
  like `misc`/`update`/`stuff`). Lead with the verb or the object acted on so the
  ID reads as a summary on its own: `dead_classifier_purge`, `orphan_era_fields`,
  `per_bank_trim_emit`, `ecu_perception_delta`.

Why three words: the bare `T-OBDV2-7` tells a future session nothing; the slug is
what makes the PROGRESS.md table, the `tasks/` directory listing, and a commit
message self-describing **without opening the file**. The ID is read far more
often than the file is. A good slug answers "what does this task change?" at a
glance.

Rules:
- The slug in the **filename** and the ID in **PROGRESS.md** must match exactly.
- Keep it stable once authored — renaming a task ID after coders or commits
  reference it breaks the only cross-session link. If scope changes materially,
  prefer a new ID over a rename.
- Do **not** encode status, owner, or dates in the slug — those live in the ledger
  row, not the name.

Worked examples in-tree:
`labs/obdlab/tasks/T-OBDV2-PURGE-1_dead_classifier_purge.md`,
`…/T-OBDV2-BANK-ASYM-1_per_bank_trim_emit.md`.

---

## The two rigor profiles

The skill ships **strict** as the default — it's the V2 regime, proven on 41
tasks. **Lite** drops the dual-gate ceremony for smaller projects where the
session-reset and per-task-verification discipline alone is enough.

Read `reference/strict-vs-lite.md` before choosing. The choice flows into
which `START_HERE.md` sections you keep and which you delete. Don't mix — a
project is one mode for its entire life.

---

## The language skill slot

Every project has exactly one mandatory language skill loaded at bootstrap.
This skill is the one that owns the per-file Inner Loop (syntax → lint →
security → type check after every edit).

For new modules, the language skill is **adapted into the module's bundle**
as `_<module>_skills/<module>-python/SKILL.md` (or `<module>-typescript`,
etc.) — see Step 1 above and `reference/skill-bundle-creation.md`. The
universal v2 / HFX language skills are the templates; the module's copy is
re-scoped to that module's file paths, package list, and forbidden patterns.

Reference templates:

| Language | Reference skill path | Status |
|---|---|---|
| Python | `v2/_v2_skills/python/SKILL.md` | BUILT |
| Others | — | not yet built; surface this and ask the user how to handle |

See `reference/per-language-skills.md` for the slot rules and how to add a
new language. The "one skill per project" rule still applies, but the skill
lives in the project's bundle, not loaded from v2.

---

## Why this works (theory)

V1 of the diagnostic engine hit a 44 % accuracy plateau that 20+ remediation
tasks couldn't break. Root cause wasn't the model or the code — it was
**no session boundary discipline**: tasks bled across sessions, context
rotted, regressions slipped in unnoticed.

V2 fixed this with four constraints, all encoded in this skill:

1. **Half-session sizing.** A task that fits in ≤ 50 % of a fresh session
   can be completed *and* verified before the agent's reasoning quality
   starts degrading from context fill.
2. **Bootstrap-on-clear.** Every session starts from `START_HERE.md`. No
   stateful drift across sessions because there is no state across sessions
   beyond the files in the repo.
3. **Dual-gate finish** (strict mode). A task only flips to `done` when
   both a `VERIFICATION GATE` and a `CODE REVIEW` block are clean. This is
   the mechanism that prevents V1-style silent regressions.
4. **Disclosure-first sequencing (progressive disclosure).** Order and
   shape tasks so each one *reveals* what the next decision needs before any
   task *commits* to that decision. Four moves: (a) sequence
   cheapest-disclosure first — the task that reveals a decision-relevant
   unknown (a measured number, a residual, a feasibility) is
   `Blocked by`-upstream of the tasks whose scope depends on it; (b) split
   disclose-from-commit — if one task both discloses a fact and commits a
   policy calibrated on it (a threshold, a re-tune, a re-pin), ship the
   disclosure and defer the commitment as a separate task blocked on it;
   (c) author one live task at a time for iterative packs — fully author only
   the next runnable task, keep the rest named-but-provisional
   (forward-registered ledger rows) until the prior task's disclosure lands;
   (d) tier every measurement/checkpoint output essential-first (headline →
   per-bucket → per-case detail in JSON), and make each task name what it must
   **surface, not hide** (shortfalls and honest gate labels; never dress a
   partial result as complete). This is NN/g progressive disclosure applied to
   task packs — it keeps the owner's run→reveal→decide loop grounded in
   evidence instead of pre-committing to research-gated or risky work.

When you write a task pack, you're not generating documentation — you're
encoding a finite-state machine that the coder session executes. Treat
every word in `START_HERE.md` and every section in a task file as part of
that machine. If it isn't load-bearing, delete it.

---

## The context budget (READ-NARROW) — every generated bootstrap carries it

Half-session sizing (constraint 1 above) fails if the **bootstrap itself**
spends the budget before code starts. The measured failure mode: a bootstrap
that force-reads large reference files whole — a 25 k wiki, an 8 k vocabulary,
an 8 k ontology YAML, a 9 k test module, a 14 k `CLAUDE.md` — burns ~half the
window before the first edit, so the task can no longer fit in its allotted 50 %.

The fix, baked into `templates/start_here.md`, is a **CONTEXT BUDGET / READ-NARROW
block** every generated `START_HERE.md` must include:

1. **Read the task file first; it is the spec.** It pins the exact sections,
   literals, and code targets. Everything else the session reads is dictated by
   that file — never pre-load reference material "to be safe."
2. **Never whole-read large reference/working files** (wiki, vocabulary, atlas,
   ontology/data YAML, test modules, the parent `CLAUDE.md`). Open the cited part
   only, by line range: `grep -n "<§/anchor>" <file>` → `Read` with
   `offset`/`limit` (~60 lines). For code, read the **target function**
   (`grep -n "def <name>"`), not the module; whole-read a code file only if it is
   < ~150 lines.
3. **State an explicit ceiling** — "≤ 30 k tokens of reads before the first
   edit" — so over-reading trips a stop instead of silently filling the window.
   A truncation warning means the read was too wide; re-do it scoped.

This rule only works if task files give it anchors to narrow to. So
`templates/task_file.md` requires every `### Context ###` / `### Deliverables ###`
to **pin exact citations** — wiki `§N.M` (or line range), exact numeric literal,
and the exact `file.py::function` target. A task file that says "see the wiki"
forces a whole-read; a task file that says "`GAS_WIKI §8.9`, line 941" lets the
coder read 60 lines. **Pinned citations are a bootstrap-budget feature, not just
provenance.** (Existing task files in a healthy pack already do this — verify a
sample rather than rewriting them; the gap is in the bootstrap's read order, not
the specs.)

## Git in generated bootstraps — explicit paths, bash, `\` line-continuation

The git block in `templates/start_here.md` is **not** `git add -A`. The proven
ritual: the **user** runs the commit in a terminal (bash), staging deliverables by
**explicit path**. When the path list wraps across lines, each line ends with a
bash line-continuation **backslash** (`\`) — never `;` — so
the user can paste the whole multi-line block as one command without a broken
line. The backslash must be the last character on the line (no trailing space).
Match whatever the project's root `CLAUDE.md` "Git" section specifies.

---

## Files in this skill

```
coding-bootstrap/
├── SKILL.md                              (this file)
├── templates/
│   ├── claude_md.md                      (project CLAUDE.md — the bootstrap ignition)
│   ├── start_here.md                     (bootstrap prompt template)
│   ├── progress.md                       (task ledger template — incl. architect patches table)
│   └── task_file.md                      (single-task template, incl. Load skills: line)
├── reference/
│   ├── skill-bundle-creation.md          (how to build _<module>_skills/ + _INDEX.md)
│   ├── custom-skill-authoring.md         (when + how to author an on-demand skill)
│   ├── breakdown-guide.md                (how to split a monolith)
│   ├── strict-vs-lite.md                 (rigor-profile selection)
│   ├── per-language-skills.md            (language-skill slot rules)
│   ├── prompt-rules-applied.md           (which prompt-engineering principles map to which section)
│   ├── code-quality-principles.md        (Karpathy 4 + architecture 4 — applied at task authoring)
│   └── knowledge-graph-iteration.md      (5-stage pattern for static-KG modules: schema → extract → resolve → assemble → validate)
└── checklists/
    └── breakdown-checklist.md            (verify a task is genuinely half-session, incl. Quality block)
```

Read templates lazily — only when you're about to fill them. Read references
only when their topic is live in the current decision. The references
collectively run a few hundred lines; loading them all at once wastes
context for no benefit.

---

## Worked examples (where to look)

| Module | Skill bundle | Task pack | What to learn |
|---|---|---|---|
| **v2** | `v2/_v2_skills/` (21 skills, `_INDEX.md`) | `v2/coder_tasks_v2/` (41 tasks across 7 phases) | The most mature pattern — three categories of skills in `_INDEX.md`, dual-gate session-end |
| **HFX** | `HFX/_hfx_skills/` (13 skills, `_INDEX.md`) | (HFX task pack location) | 8 domain skills authored one per major code surface |
| **COMLab** | `4DLab/COMLab/_comlab_skills/` (4 skills) | `4DLab/COMLab/comlab_tasks/` (7 Phase 0b task files) | The recovery case — Phase 0b was first attempted as a monolithic bootstrap and re-done as 7 atomic tasks. The current `_comlab_skills/` includes a phase-specific on-demand skill (`comlab-vocabulary`). |

Each is a worked example of this skill applied. Read the relevant one when
unsure about a specific decision — especially `_INDEX.md` format, on-demand
skill shape, and PROGRESS.md table conventions.

---

## Anti-patterns this skill exists to prevent

- **The monolithic bootstrap.** One giant doc with §A skill-load + §B all
  tasks + §C bootstrap prompt + §D 17 decisions. Overflows context, bundles
  scope, prevents `/clear`. If you find yourself writing a single `.md` longer
  than ~200 lines that contains both the bootstrap AND the task content,
  stop — that's the anti-pattern.
- **The whole-file preamble read.** A bootstrap step that says "Read the wiki /
  the design spec / `CLAUDE.md`" with no section scope, so the coder whole-reads
  a 25 k file to use 60 lines of it. Burns the half-session budget before code.
  Fix: read the task file first, then read only the sections it cites, by line
  range (see "The context budget (READ-NARROW)"). Every `START_HERE.md` must
  carry the CONTEXT BUDGET block.
- **The `git add -A` bootstrap.** A session-end git block that stages
  everything from the repo root. It sweeps in unrelated uncommitted work and
  build caches. Fix: user-run commit in a terminal, explicit paths, `\`
  line-continuation (see "Git in generated bootstraps").
- **The orphan skill.** A skill in `_INDEX.md` that no task file references
  in its `Load skills:` line. Means the rule isn't actually being enforced.
- **The phantom task.** A row in `<MODULE>_PROGRESS.md` with no matching
  `T-*.md` file. The coder can't load what doesn't exist.
- **The pre-committed pack.** Authoring the risky or decision-gated tasks (a
  re-tune, a re-pin, a policy threshold) *before* the cheap task that discloses
  whether they're warranted — so the owner commits blind. Fix: disclosure-first
  sequencing (constraint 4) — reveal the number, then author the task that acts
  on it; if a task both discloses and commits, split it and gate the commit on
  the disclosure.
- **The unnamed-consumer spec.** A task file that adds a field/enum/fault but
  leaves its `### Consumer (signal/noise) ###` blank or vague ("for COMLab",
  "future use"), deferring the project's one governing constraint to the coder.
  The coder then stalls on START_HERE's critical-ambiguity stop, or worse ships
  an orphan. Fix: the architect names the consumer **and** the `file.py::function`
  code path in the task file — or marks it `PROPOSAL` with the same-diff reader.
  This is the single highest-leverage precision check; the breakdown checklist's
  Quality section enforces it.
- **The drifted `done` row.** The ledger is the only cross-session state, so a
  row whose `Status` disagrees with reality silently poisons every later session
  — a `done` row whose consumer field is read nowhere (orphan), whose deliverable
  is absent, or whose progress note lacks clean gates; or a `pending` row whose
  note already shows clean gates. Fix: the generated `START_HERE.md` carries a
  **stale-ledger guard** at session start (surface the mismatch, don't auto-fix)
  and an **anti-orphan grep** before any flip to `done`. Both are baked into
  `templates/start_here.md`.
- **The runaway task.** A task file whose `### Deliverables ###` section
  has more bullets than the coder can hold in one fresh-context session.
- **The in-band wiki edit.** The coder edits a wiki under `docs/wiki/`
  during a coding task. Wiki edits are architect-level — record them in
  the `Architect-level out-of-band patches` table in PROGRESS.md.
- **The silent skill load.** A task says "Load skills:" but the coder
  doesn't read the skill before working. The bootstrap's Step 8 (confirm
  scope in chat) is what catches this — keep it in every START_HERE.
- **The idle-after-scope wait.** A `START_HERE.md` that makes the coder post
  its scope paragraph and then *wait for the user to confirm* before any code.
  The scope paragraph is a checkpoint, not a gate — an unconditional wait stalls
  the session on routine work and trains the owner to rubber-stamp. Fix: the
  generated bootstrap (template Step 9) must say **proceed directly to coding
  after posting the plan; stop only for a critical ambiguity.** "Critical" is
  pinned to three cases so the coder can neither over- nor under-stop: (1) no
  nameable existing consumer (COMLab analytics / fault-atlas routing) for a
  field/enum the task adds, (2) a files/scope question the task file does not
  resolve and the repo cannot, (3) a cited literal/section that does not exist
  where the task says. Everything else: note the assumption in the plan and
  continue. This is the only sanctioned exception to "do not pause between
  steps" — do not widen it into a general confirmation gate.
- **The bootstrap-triggered graph rebuild.** A bootstrap step that says
  "(re)build the knowledge graph" unconditionally on every session start.
  The graph is a verified artefact — it has a verification log (worked
  example: `4DLab/GASLab/graphify-out/STEP1_VERIFICATION_LOG.md`)
  and the project's spec may have augmented the canonical extraction
  prompt with custom relation vocabulary, proof-set edges, and
  deterministic INFERRED-edge relabellings. Re-running the canonical
  graph-build skill (`Skill(graphify)` etc.) on session start will
  clobber that verified state with a generic-prompt extraction and
  silently regress earlier audits. **Default resolution is SKIP:** a
  build runs *only* inside a dedicated KG-lane task (`T-PREP-*` /
  `T-KG-*`) whose own `Deliverables` explicitly name `graph.json`. A
  normal lab task (schema, translator, fixtures, tests) never rebuilds
  the graph — not on session start, not because the log looks stale,
  not because the wiki changed, and never via a "keep the graph
  current" step the coder adds that no task file contains. The
  `[KG-NAV-GRAPH-ONLY]` pre-step in `templates/start_here.md` is the
  canonical guard for this pattern.
