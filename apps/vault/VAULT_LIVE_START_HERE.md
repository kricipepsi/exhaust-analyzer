# vault-live — START HERE (paste as message 1 of every vault-live coder session)

## ⚡ EXECUTE IMMEDIATELY
Do not greet the user. Do not ask what to work on. Work through steps 1–8 below
**right now, in order**. Your first user-visible output is the scope-confirmation
paragraph at step 8. If a step reveals a blocker, state it and stop.

---

### Role / lane ###
You are framing the **live** 4DLab tree for Obsidian transparency. The workspace
root is an Obsidian vault; the architect opens it on `/agent_workspace` and reads
it as a graph. Your job: add the vault **node frontmatter** (`§4` schema) to a
lab's live `docs/` + wiki notes so the three `.base` audit views
(`modules`, `consumers`, `drift-guards`) light up for that lab — **on the live
notes, not on a copy.** There is **no mirror build** in this pack: the live notes
*are* the graph. `build_lab_vault.py` is **not** run here.

This is the **vault-tooling / architect-authoring lane**: you add YAML frontmatter
and `.base` files. You do **not** edit lab Python, change a graph, or copy notes
into `Vault/` (that mirror is being archived — editing it is blocked by
`.omp/rules/lane-guard-no-vault-edit.md`).

**Workspace root:** `/agent_workspace/`
**Pack root:** `/agent_workspace/apps/vault/`
**Tasks dir:** `/agent_workspace/apps/vault/vault_live_tasks/`
**Ledger:** `/agent_workspace/apps/vault/VAULT_LIVE_PROGRESS.md`
**Domain skill (authoritative):** `_skills/graph/4dlab-vault/reference/` — the
node schema (`frontmatter-schema.md`) and the views (`bases-and-views.md`).
**Per-lab consumer maps (architect-authored, the source of truth for the
semantic fields):** `_skills/graph/4dlab-vault/assets/vault-map.<lab>.yaml`.

**This pack's goal (it bounds every task):** make the three `.base` views render
**against the live `labs/` tree** in Obsidian-on-root, with every framed note
carrying ≥1 **named** consumer (signal/noise). A task does not flip to `done`
until both its `VERIFICATION GATE` and `CODE REVIEW` blocks are clean in
`vault_live_tasks/progress_notes/<task-id>.md`.

---

### The one rule that bounds the metadata (signal/noise) ###
**Every framed note ships with ≥1 named consumer.** `consumers` is never empty
and never auto-derived — it comes from the lab's `vault-map.<lab>.yaml`, authored
by the architect. Before you write a note's frontmatter, **confirm each named
consumer's file + symbol actually resolves to a live read** (`grep` it) and each
`implements` / `drift_guards` path **exists on disk**. If a path or consumer does
not resolve, **do not invent a substitute** — STOP and route the note back to the
architect (an unframmable note is a signal/noise finding, not a fill-in).

### The mirror→live path remap (pin this; it is the one non-obvious transform) ###
The `vault-map.<lab>.yaml` paths use the **mirror's tier prefixes**. Rewrite each
to its **live** equivalent before writing it into frontmatter:

| Map (mirror) path | Live path | Note |
|---|---|---|
| `labs/<lab>/code/<X>` | `labs/<lab>/<lab>/<X>` | the live package dir == the lab slug |
| `labs/<lab>/tests/<X>` | `labs/<lab>/tests/<X>` | unchanged |
| `labs/<lab>/docs/<X>` | `labs/<lab>/docs/<X>` | unchanged |
| wiki note source | `labs/<lab>/wiki/<X>` (most labs) **or** `labs/<lab>/research/chunks/<X>` (obdlab only) | per the task file |

Confirm the package dir (`labs/<lab>/<lab>/`) exists before remapping. `source:`
points at the **live** note's own path.

---

### CONTEXT BUDGET — read narrow (read this before any Read) ###
The **task file is the spec** — it pins the lab, its map, the wiki-source folder,
and the exact notes to frame. Read the task file, then read only what it names.
**Bootstrap budget: ≤ 25 k tokens of reads before the first edit.**
- **Never whole-read** a large note body, a wiki chunk, or `frontmatter-schema.md`
  in full — you only need the schema block + the lab's `vault-map.<lab>.yaml`.
- Read `vault-map.<lab>.yaml` (small) end-to-end; it is the spec for which notes
  to frame and with what fields.
- A truncation warning means you read too wide — re-do it scoped.

---

### Mandatory bootstrap (in this exact order) ###

**[KG-NAV-GRAPH-ONLY] Pre-step — default SKIP.** The labs ship frozen navigation
graphs at `labs/<lab>/graph/v2_current/`. They are **query-only, never rebuilt.**
No task in this pack builds a graph; running `graphify` is a rule violation, not a
step. SKIP → Step 1.

**1. Load the project design rules (workspace).**
`Read /agent_workspace/AGENTS.md` — the five rules (graph-before-grep, wiki truth,
task-is-a-file, signal/noise, lab isolation) **and the `## Vault conventions`
block**. No work without these.

**2. Load the domain references.**
`Read _skills/graph/4dlab-vault/reference/frontmatter-schema.md` (the `§4` node
schema + the per-field consumer table) and skim
`_skills/graph/4dlab-vault/reference/bases-and-views.md` (what each `.base` view
queries). These are the contract; the `.base` files themselves are
frontmatter-keyed and folder-generic — you do **not** rewrite them.

**3. Find the next task.**
`Read /agent_workspace/apps/vault/VAULT_LIVE_PROGRESS.md`.
**Stale-ledger guard (run before picking):** stop and surface (don't auto-fix) if
a `done` row's progress note is missing/lacks clean gates or its framed notes are
absent, OR a `pending` row's note already shows clean gates. Then take the **first
row** where `Status` is `pending` and every `Blocked by` ID is `done` (or `—`).
`deferred`/`blocked` rows are skipped.

**4. Load the task prompt.**
Open the matching `vault_live_tasks/<task-file>.md` and read it end-to-end before
touching anything. Then `Read` that lab's `vault-map.<lab>.yaml`.

**5. (no extra skill loads — the domain skill in Step 2 is the only one this pack needs).**

**6–7. (reserved — bootstrap continues at scope confirmation).**

**8. Confirm scope, then proceed (do not idle for confirmation).**
Post a one-paragraph plan: which task/lab, the wiki-source folder, how many notes
you'll frame (design docs + wiki notes), and that you'll confirm every consumer +
path resolves before writing. **After posting, proceed directly — do not wait for
the user.** Stop ONLY for a critical ambiguity: (1) a map's named consumer/path
does not resolve on disk; (2) a notes/scope question the task file and repo cannot
resolve; (3) the lab's package dir or wiki-source folder is not where the task
says. Everything else: note the assumption and continue.
**Persist the plan:** create `vault_live_tasks/progress_notes/<task-id>.md` and
write that paragraph as a `## Plan` section at the **top**, before any edit.

---

### Working rules (apply throughout) ###
- **Frontmatter only.** You add a `§4` YAML block at the top of live `.md` notes
  and (pilot only) place `.base` files. No edits to lab Python, wiki/chunk bodies,
  graphs, or `Vault/`.
- **Idempotent.** If a note already carries valid `§4` frontmatter (e.g. obdlab's
  `research/chunks/*/README.md` from `T-VAULT-WIKIFRAME-1`), **verify, don't
  duplicate** — never add a second block.
- **Anti-orphan before write** (the gate of this pack): `grep` each named
  consumer's file+symbol and confirm a live read; confirm each `implements` /
  `drift_guards` path exists. Unresolvable → STOP, route to architect.
- **Tests must stay green.** Adding frontmatter to a note a test parses can break
  that test (it happened in `T-VAULT-WIKIFRAME-1`). After framing a lab, run that
  lab's suite from the shared venv: `/agent_workspace/.venv-wired/bin/python -m
  pytest -q labs/<lab>/tests` — a red suite is a stop.
- **No graph touch.** Confirm `git status --porcelain -- labs/<lab>/graph/` is
  clean before finishing.
- **Stay in scope.** One lab per task (except the pilot's `_bases/` setup).
  Unrelated issues → `Unplanned follow-ups` in `VAULT_LIVE_PROGRESS.md`.

---

### Session-end checklist (mandatory before you stop) ###
1. Run the task's `### Verification ###` section. Paste headline results
   (note count framed; the three `.base` views' row counts for this lab; lab
   pytest result; `git status` of `graph/` clean).
2. Fill the `VERIFICATION GATE` block in the progress note (eligibility, framed
   notes present with valid frontmatter, no empty `consumers`, bases render,
   tests green, graph untouched, anti-orphan confirmed).
3. Fill the `CODE REVIEW` block (schema conformance: fixed `node_type` values;
   paths remapped to live + resolve; signal/noise: every framed note has a named
   consumer; no duplicate frontmatter).
4. **Emit the commit block (mandatory final output).** The user runs it. Explicit
   paths only, one per line, backslash-continued; never `git add -A`; never stage
   `__pycache__/`, `*.egg-info/`, or any graph artefact.
   ```bash
   cd /agent_workspace
   git add \
     apps/vault/vault_live_tasks/progress_notes/<task-id>.md \
     apps/vault/VAULT_LIVE_PROGRESS.md \
     labs/<lab>/docs/<framed-doc>.md \
     labs/<lab>/wiki/<framed-note>.md
   git commit -m "<task-id>: frame <lab> live notes for vault transparency"
   ```
5. **Update `VAULT_LIVE_PROGRESS.md`.** Flip `Status` to `done` (or `blocked` +
   reason); fill Date/Commit/Verification/Notes (one line each). Append the two
   gate blocks to the progress note, **not** the ledger. Promote any dependent
   `deferred → pending` whose blockers are now `done`.
6. Confirm in chat: "Task <id> done — committed `<hash>`, `VAULT_LIVE_PROGRESS.md`
   updated, both gates clean. Safe to clear session."

---

### Now do step 1 of the bootstrap. ###
