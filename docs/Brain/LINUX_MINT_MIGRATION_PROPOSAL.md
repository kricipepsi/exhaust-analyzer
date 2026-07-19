# Linux Mint Migration + omp Role-Config Proposal

**Date:** 2026-06-26 · **Author:** Cowork (architect) · **Status:** proposal, for review
**Replaces the generic advice in** `setup.md` **(which assumed OpenAI Codex + `CODEX_HOME`).**

> **Decisions baked in (from you):** workspace root on Linux = `/agent_workspace`; Linux user = `m`
> (home `/home/m`); Cowork architect config = `/home/m/.claude`; omp config home = `/home/m/.omp`;
> two coders keep the labels **Codex** and **Agy**, both running under **omp** (already up). Deliverable =
> this single proposal with the file bodies inline (copy-paste, don't generate separate files yet).

---

## TL;DR — the three things `setup.md` gets wrong for *your* stack

1. **omp does not use `CODEX_HOME`.** That env var belongs to OpenAI Codex. omp keeps its per-machine
   state under `~/.omp/agent/` (config.yml, `agent.db` auth, `memories/`, `sessions/`) and its
   instruction file is **`AGENTS.md`**, discovered from the **cwd** (the project root omp is launched in).
   The documented way to give Codex and Agy separate profiles is the env var **`PI_CODING_AGENT_DIR`**
   (relocates the agent dir — omp's own docs call this "isolating profiles"), paired with a launch-time
   identity pointer. Not `CODEX_HOME`. (Confirmed against omp.sh/docs — see §2.4/§2.6.)
2. **`MEMORY.md` in omp is an *engine-managed* file, not a repo file you hand-write.** With
   `memory.backend: local` (or `mnemopi`), omp auto-consolidates past sessions into
   `~/.omp/agent/memories/<project>/MEMORY.md` and injects it as a "Memory Guidance" block at startup
   (read it with `read memory://root/MEMORY.md`). It's machine-local and per-project. A `MEMORY.md` you
   drop in the repo is **not** wired to that — it's just notes. So set `memory.backend` deliberately
   (§2.5/§2.6); don't assume a repo `MEMORY.md` feeds the agent.
3. **`AGENTS.md` (lowercase) will silently stop loading on Linux.** Linux is case-sensitive; omp and
   Codex look for **`AGENTS.md`**. Your repo currently ships `AGENTS.md`. On Windows that worked by
   accident. Rename it (§1.4) or the coders boot with *no shared rules*.

Everything below adapts `setup.md`'s good instinct (role isolation) onto the structure you actually
run: the **`labs/<lab>/tasks/<id>.md`** task-as-a-file canon, with Cowork as architect and two omp
coders as builders.

---

## Part 1 — Linux folder structure & what to copy vs. rebuild

### 1.1 Migrate with **git**, not a raw file copy

Your repo is already a git repo with a well-formed `.gitignore` and `.gitattributes`. Use them:

```bash
# on the new Linux Mint box, as user m
sudo mkdir -p /agent_workspace && sudo chown m:m /agent_workspace
cd /agent_workspace
git clone <your-remote-or-bundle> .        # see note below if you have no remote
```

Why git over `cp`/USB drag:

* `.gitignore` **automatically excludes** the junk you must not carry: `.venv-wired/`, `.sandbox-py/`,
  `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `graphify-out/`, `DBS/`, `**/mysql_data/`,
  `success.log`, `task.sh`.
* `.gitattributes` (`* text=auto eol=lf`) **normalizes line endings to LF on checkout**, so you don't
  inherit CRLF breakage. A raw copy keeps Windows CRLF and you'd have to `git add --renormalize .` or
  `dos2unix` afterward.

**No remote?** Make a bundle on Windows and move the single file:

```powershell
# Windows (Git Bash / PowerShell) in C:\Workspace
git bundle create 4dlab.bundle --all
```
```bash
# Linux
git clone /path/to/4dlab.bundle /agent_workspace && cd /agent_workspace
git remote remove origin   # detach from the bundle
```

### 1.2 Untracked-but-wanted data (copy separately, with rsync)

A few things are gitignored on purpose but you still need them. Copy *only these* by hand:

```bash
# from a mounted Windows share or USB; --omit-dir-times avoids noise
rsync -av --progress /mnt/win/Workspace/DBS/            /agent_workspace/DBS/
rsync -av --progress /mnt/win/Workspace/**/mysql_data/  ...   # if you run the vinlab DB locally
# Obsidian local app-state is optional; vault content itself IS tracked and comes via git.
```

Per-lab **graphs** (`labs/<lab>/graph/v2_current/`) are under `labs/` and tracked, so they arrive with
the clone — **do not rebuild any graph** (hard prohibition: no `graphify`). Only the root
`graphify-out/` scratch is excluded, which is correct.

### 1.3 Copy / Rebuild / Skip — the decision table

| Item | Action | Why |
|---|---|---|
| Everything tracked by git (`labs/`, `apps/`, `harness/`, `docs/`, `Vault/`, `_skills/`, brain docs, per-lab `graph/`) | **Copy** (via clone) | Source of truth |
| `DBS/`, `**/mysql_data/` | **Copy** (rsync) | Large, gitignored, still needed |
| `.venv-wired/` | **Rebuild** | Windows venv has `Scripts/` + Windows paths; useless on Linux |
| `.sandbox-py/` (Python 3.14) | **Rebuild** | Windows layout; on Linux it's `bin/python3.14` |
| `.pytest_cache/`, `.ruff_cache/`, `__pycache__/`, `*.pyc` | **Skip** | Regenerated on first run |
| `graphify-out/`, `**/graphify-out/` | **Skip** | Frozen KG scratch; never copy, never rebuild |
| `.mounttest_*.del`, `.synctest.del`, `success.log`, `task.sh`, `Thumbs.db`, `Desktop.ini` | **Skip / delete** | Cruft + stray harness artifacts |

### 1.4 The four Linux gotchas (Windows let these slide)

1. **Case sensitivity.** Rename the router so omp/Codex find it:
   ```bash
   cd /agent_workspace && git mv AGENTS.md AGENTS.md
   ```
   Then `grep -rin "agents\.md" .` and fix any doc that points at the lowercase name (CLAUDE.md,
   START_HERE.md both reference it). Also sweep code for case-mismatched imports/paths that "worked" on
   Windows: `git config core.ignorecase false` locally so git stops hiding them.
2. **Line endings.** Covered by `.gitattributes` *if you migrate via git*. If anything looks CRLF:
   `git add --renormalize . && git status`.
3. **Exec bits.** Shell/Python entry scripts need `+x`: `chmod +x scripts/*.py task.sh _skills/**/*.sh`
   (only the ones you actually invoke).
4. **`CLAUDE.md` "Environment Rules" flips.** Today it says *"treat all files as case-insensitive to
   match the Windows host."* On a real Linux host that guidance is now **false** and should be updated to
   "case-sensitive; `AGENTS.md` is exact." (Small edit; flagged, not done — Part 1 is yours to run.)

### 1.5 ⚠ Confirm the **parent `4DLab`** dependency before you clone

Your `CLAUDE.md` says infra (`.venv-wired`, `.sandbox-py`, git ritual) is **inherited from the parent
`4DLab` root**, and it references `../v2-restructure/`. That means **`C:\Workspace` is the `4DLabV2`
*child*, not the whole tree.** If you clone only `C:\Workspace` into `/agent_workspace`, you lose the
parent's venv recipe and the `v2-restructure` execution log.

**Resolved (2026-06-26): child-only.** `/agent_workspace` = the **`4DLabV2` contents only** (keeps
Cowork's mount small to avoid truncation). The full `4DLab` parent stays **on-hand, off-mount**. Bring the
single file `4DLab/CLAUDE.md` (the venv/sandbox/git infra recipe) so the Linux build is reproducible;
`4DLab/v2-restructure/` and the canonical `4DLab/graphify-out/` are fetched from the on-hand copy only if a
task needs them. Expect the in-repo `../` references to dangle on the mount — that's acceptable.

### 1.6 Rebuild infra (Python 3.14 sandbox + wired venv)

Per your memory (`4dlab-python-314-only`): run python/pytest via `.sandbox-py/bin/python3.14`, never
system 3.10. On Linux:

```bash
cd /agent_workspace                       # = the 4DLabV2 contents (D1 resolved, §1.5)
python3.14 -m venv .sandbox-py            # install 3.14 first if Mint lacks it (deadsnakes/pyenv/uv)
python3.14 -m venv .venv-wired
source .venv-wired/bin/activate
# editable-install each lab so ruff/pyright/pytest resolve (exact list per parent 4DLab/CLAUDE.md)
pip install -e labs/gaslab -e labs/obdlab -e labs/dtclab -e labs/comlab ...
```

Then the inner loop must pass before you trust the migration: `ruff check .` → `pyright <pkg>/` →
`.sandbox-py/bin/python3.14 -m pytest -x -q`.

---

## Part 2 — Configuring Codex & Agy (the actual ask)

Since both coders are **already running under omp**, this is about getting the right text into the right
files at the right paths. First, the loading model — *who reads what*:

### 2.1 Who loads which file

| Agent | Tool | Auto-loads | Identity comes from |
|---|---|---|---|
| **Architect** | Cowork (this app) | `/agent_workspace/CLAUDE.md` + `/home/m/.claude` memory | §2.3 file **A** |
| **Codex** (coder) | omp | `/agent_workspace/AGENTS.md` (shared, root) | launch pointer → §2.3 file **C** + lane rule **F** |
| **Agy** (coder) | omp | `/agent_workspace/AGENTS.md` (shared, root) | launch pointer → §2.3 file **D** + lane rule **F** |

The trap: **both omp coders read the same root `AGENTS.md`** (closest-file-wins doesn't separate two
agents launched at the same root). So root `AGENTS.md` carries **shared rules only**; per-coder identity
is injected at launch (§2.4), never baked into the root file.

### 2.2 Reconcile `setup.md`'s `.agent/` plane with your `labs/<lab>/tasks/` canon

`setup.md` invents `.agent/tasks/{codex,agy}/` inboxes and `.agent/reports/{codex,agy}/` outboxes. **Do
not adopt that wholesale** — it would fork your task system. Your canon already says *"a task is a
file"* at `labs/<lab>/tasks/<id>.md`, with gates in `progress_notes/<id>.md` and the ledger in
`PROGRESS.md`. Keep that as the single source of truth. Use a **thin** `.agent/` plane for *identity and
assignment only*:

```text
/agent_workspace/
├── CLAUDE.md                      # A · architect (Cowork) entrypoint  [reframed]
├── AGENTS.md                      # B · shared coder rules (was AGENTS.md) [renamed + small add]
├── labs/<lab>/tasks/<id>.md       #     task SPECS — architect writes, canon source of truth
│   └── progress_notes/<id>.md     #     gates: VERIFICATION GATE + CODE REVIEW (the real "report")
└── .agent/                        # NEW thin plane — identity + assignment pointers ONLY
    ├── coders/
    │   ├── codex/AGENTS.md         # C · Codex identity
    │   ├── codex/MEMORY.md         # E · Codex manual notes (optional; not omp Hindsight)
    │   ├── agy/AGENTS.md           # D · Agy identity
    │   └── agy/MEMORY.md           # E · Agy manual notes
    ├── rules/lane-guard.md         # F · omp stream rule (lane boundaries)
    └── assignments.md              #     manager writes "Codex → T-OBDV2-7" here (pointers, not specs)
```

No duplicated specs, no parallel report tree. Assignment is a one-line pointer to a real task ID.

### 2.3 The files (copy-paste bodies)

#### A · `/agent_workspace/CLAUDE.md` — architect entrypoint (Cowork)

> Audience flips: in the old setup Claude Code was a *coder*. Now Cowork is the **architect** and omp
> does the coding. So `CLAUDE.md` describes the architect contract and imports the shared rules.

```markdown
# CLAUDE.md — 4DLab architect entrypoint (Cowork)

You are the **architect** (Cowork). You author specs and review; you do **not** implement.
Coders are two omp agents — **Codex** and **Agy** — driven by a human manager.

@AGENTS.md            <!-- shared five-rules canon, also read by the coders -->

## Boot (every session)
1. START_HERE.md → ROADMAP.md (stage order: GASLab → OBDLab → DTCLab → COMLab last).
2. The active lab's wiki/ + graph/ (query the graph; never rebuild it).
3. The lab ledger `labs/<lab>/tasks/PROGRESS.md` — first `pending` row is next runnable.

## Architect responsibilities
- Author one task spec per work item at `labs/<lab>/tasks/<id>.md`, following the five rules
  (signal/noise: every new field/fault ships with a NAMED consumer or a proposal that adds its
  consumer in the same change).
- Record the assignment as a pointer in `.agent/assignments.md` (e.g. `Codex → T-OBDV2-7`).
  One task per coder session. Never hand the same task to both.
- Review the coder's gates in `labs/<lab>/tasks/progress_notes/<id>.md` (VERIFICATION GATE +
  CODE REVIEW). Decide accept / revise / split / reassign.

## Architect must NOT
- Implement large coding tasks (delegate to Codex/Agy unless explicitly asked).
- Rebuild any graph (`graphify`). Graphs are frozen — query them.
- Let a coder redefine architecture, or store secrets in files.
```

#### B · `/agent_workspace/AGENTS.md` — shared coder rules (minimal change)

**Keep your current `AGENTS.md` body verbatim** (the five-rules router is already canon-correct). Just
(1) rename the file to `AGENTS.md`, and (2) append this short block so omp coders know their lane:

```markdown

## Coders run under omp (Codex, Agy)

- This file is the SHARED rule set. Your per-coder identity is injected at launch and lives at
  `.agent/coders/<you>/AGENTS.md` — read it first, then obey this file.
- A task is a file: implement exactly the `labs/<lab>/tasks/<id>.md` the manager assigned (see
  `.agent/assignments.md`). One task per session.
- "Done" = both gate blocks filled in `labs/<lab>/tasks/progress_notes/<id>.md`, any contracted field
  grep-confirmed read in a live path, and the `PROGRESS.md` row flipped to `done`. Then STOP.
- Do not act as architect, reassign work, edit `.agent/coders/<the-other-coder>/`, or rebuild a graph.
- Use omp's own tools for the inner loop: `lsp` for navigation/renames, `bash` for
  `ruff check .` → `pyright <pkg>/` → `pytest -x -q`. Curate durable findings with `retain`.
```

#### C · `.agent/coders/codex/AGENTS.md` — Codex identity

```markdown
# Codex — omp coder identity

You are **Codex**, an implementation-only coder for `/agent_workspace`. You run on omp.

Boundaries:
- Read `/agent_workspace/AGENTS.md` (shared rules) before coding.
- Implement only the task ID assigned to you in `.agent/assignments.md`. One task per session.
- Report via the canon gates in `labs/<lab>/tasks/progress_notes/<id>.md` — not a private outbox.
- Do NOT act as architect, touch `.agent/coders/agy/`, take Agy's assignment, or rebuild a graph.
- No secrets in files. Lab isolation: no cross-lab Python imports — mirror types over JSON.

Memory:
- Native: omp **Hindsight** (project-scoped SQLite). `retain` durable build/test facts; `recall`/`reflect` to reuse.
- Manual (optional, human-readable, git-tracked): `.agent/coders/codex/MEMORY.md`. Read/write only your own.

Start of session:
1. Read shared AGENTS.md, then this file.
2. Read your assignment + the task spec it points to.
3. Inner loop: ruff → pyright → pytest. Fill both gate blocks. Flip the ledger. Stop.
```

#### D · `.agent/coders/agy/AGENTS.md` — Agy identity

Identical to **C**, with every `codex` → `agy` and the "do not touch" pointing at `codex/`:

```markdown
# Agy — omp coder identity

You are **Agy**, an implementation-only coder for `/agent_workspace`. You run on omp.
[...same body as Codex, swap codex↔agy, and "Do NOT touch .agent/coders/codex/ or take Codex's assignment"...]
```

#### E · `.agent/coders/<name>/MEMORY.md` — manual notes (optional)

```markdown
# Codex — manual notes (human-readable; NOT omp Hindsight)

Repeated build/test gotchas, local quirks, and patterns worth re-reading. One fact per line.
Do not store secrets. Native durable memory is omp Hindsight (`retain`/`recall`); this file is the
part a human wants to skim and version in git.
```

#### F · `.agent/rules/lane-guard.md` — omp stream rule (the enforcement teeth)

omp supports **time-traveling stream rules**: a regex aborts the stream mid-token and injects a
reminder. Use one to hard-stop a coder that drifts into the other lane or tries to rebuild a graph.
Exact rule-file location/format depends on your omp version — confirm with `omp --help` / the rules
section of omp.sh/docs — but the *intent* to encode is:

```text
# pattern → injected reminder
graphify\b                          → "STOP: graphs are frozen. Query labs/<lab>/graph/, never rebuild."
\.agent/coders/(?!codex/)           → "STOP: Codex may only edit its own coder dir."  (mirror for Agy)
```

### 2.4 Launch so identities don't mix (the `CODEX_HOME` replacement)

omp discovers `AGENTS.md` + rule files from the **cwd**, so both coders launched at `/agent_workspace`
see the *same* root `AGENTS.md` (shared rules, correct). Distinct identity + isolated state come from
**two confirmed levers**:

**Lever 1 — `PI_CODING_AGENT_DIR`: a separate agent dir per coder.** This is omp's documented
profile-isolation var. Each coder gets its own `config.yml`, `agent.db` (auth/OAuth), `memories/`, and
`sessions/` — no cross-talk:

```bash
# Codex
PI_CODING_AGENT_DIR=/home/m/.omp-codex/agent \
VIRTUAL_ENV=/agent_workspace/.venv-wired \
omp --cd /agent_workspace \
    -p "You are Codex. First read .agent/coders/codex/AGENTS.md and obey it, then the task named in .agent/assignments.md."

# Agy
PI_CODING_AGENT_DIR=/home/m/.omp-agy/agent \
VIRTUAL_ENV=/agent_workspace/.venv-wired \
omp --cd /agent_workspace \
    -p "You are Agy. First read .agent/coders/agy/AGENTS.md and obey it, then the task named in .agent/assignments.md."
```

`VIRTUAL_ENV` points omp's Python/`eval` tool at your wired venv (it's the highest-priority venv path).
Confirm the resulting dir with `omp config path` after first launch. Put each command in a 2-line
launcher script (`run-codex.sh` / `run-agy.sh`) so the manager never fat-fingers the wrong profile.

**Lever 2 — the launch identity pointer (the `-p` line above).** Since omp has no per-config "system
prompt" key, the role text is injected at launch by pointing each coder at its own
`.agent/coders/<name>/AGENTS.md`. This always works and is independent of omp version. Back it with the
hard boundaries already in each identity file (**C**/**D**) and, if you confirm the rule-file format
(§ open items), the lane-guard rule (**F**).

> **Auth note (migration):** OAuth/login lives in `~/.omp/agent/agent.db`, *not* in the repo. With
> per-coder agent dirs each coder logs in once (`/login`) into its own `agent.db`. To carry existing
> logins from the old machine, copy each `agent.db` into the matching `PI_CODING_AGENT_DIR`/agent dir.

### 2.5 Memory — pick a backend, keep the layers separate

omp's `memory.backend` (a key in each coder's `config.yml`) has four settings:

| `memory.backend` | What it does | Where it lives |
|---|---|---|
| `off` (default) | nothing extracted or injected | — |
| `local` | consolidates past sessions → "Memory Guidance" block at startup | `~/.omp/agent/memories/<cwd>/MEMORY.md` |
| `mnemopi` | local SQLite bank + first-turn auto-recall; `retain`/`recall`/`reflect` tools | agent dir, on-machine |
| `hindsight` | **remote** bank (Cloud or self-hosted); same three tools | external server you point at |

**Recommendation:** set `memory.backend: mnemopi` for both coders — durable, agent-curated, and
**nothing leaves the machine** (aligns with canon "no secrets in files"). Avoid `hindsight` unless you
deliberately want a shared/remote team bank. Memory is keyed by **cwd**, so with the per-coder
`PI_CODING_AGENT_DIR` from §2.4 each coder automatically gets its **own** bank; without it, both coders
at `/agent_workspace` would share one bank.

Three memory layers exist — don't conflate them:

| Layer | Belongs to | Where | Written by |
|---|---|---|---|
| Architect memory | Cowork | `/home/m/.claude/…` (auto index) | Cowork (your `4dlab-*` facts) |
| omp durable memory | each coder | its own agent dir (`mnemopi`/`local`) | `retain` tool / auto-consolidation |
| Manual notes | each coder | `.agent/coders/<name>/MEMORY.md` (repo, optional) | a human, by hand |

`setup.md` collapses these into one hand-written "MEMORY.md per agent," which both under-uses omp's real
durable memory and wrongly implies the engine reads a repo file. Tell each coder to curate only its own
`mnemopi` bank (via `retain`) and, if you keep them, its own manual notes file.

### 2.6 Per-coder `config.yml` (drop in each agent dir)

After first launch creates the agent dir, set these in `/home/m/.omp-codex/agent/config.yml` (and the
Agy twin). Edit via `omp config set …`, the `/settings` menu, or the file directly (then `omp config
list` to validate — malformed YAML is silently ignored):

```yaml
# /home/m/.omp-codex/agent/config.yml   (mirror for .omp-agy)
modelRoles:
  default: anthropic/claude-sonnet-4-5     # your normal coding model
  smol:    anthropic/claude-haiku-4-5      # cheap subagent fan-out
  plan:    anthropic/claude-opus-4-6:high  # plan-mode planner
memory:
  backend: mnemopi                         # on-machine durable memory; no cloud
tools:
  discoveryMode: explicit                  # coders only get the tools you allow-list
```

Secrets/keys go in a **`.env`**, never in `config.yml` or the repo. omp reads `.env` in this order
(first wins): process env → `/agent_workspace/.env` (project) → `$PI_CODING_AGENT_DIR/.env` →
`~/.omp/.env` → `~/.env`. Keep provider keys per-coder in the agent-dir `.env`, `chmod 600`, and add
`.env` to `.gitignore` if it isn't already:

```bash
# /home/m/.omp-codex/agent/.env   (chmod 600, never committed)
ANTHROPIC_API_KEY=sk-ant-...
```

Other useful env knobs: `PI_SUBPROCESS_CMD` / `PI_BLOCKED_AGENT` (constrain the `task` subagent tool),
`PI_NO_PTY=1` (if the bash PTY misbehaves on Mint), `PI_TASK_MAX_OUTPUT_LINES` (cap subagent output).

---

## Part 3 — Reaching Medium articles behind the paywall

**Right now, from this Cowork session, I cannot run firecrawl:** the `firecrawl` CLI isn't installed in
this sandbox and no `FIRECRAWL_API_KEY` is set (`firecrawl: command not found`). The skill is present at
`_skills/firecrawl-web-scraping-search/` but it needs install + browser login first.

**Also important:** firecrawl renders JavaScript and bypasses *common bot blocks*, but it does **not**
defeat an authenticated paywall. Medium *member-only* stories are gated to your logged-in session — a
plain scrape returns the metered preview, not the full text, unless you hand it your session cookie.
Since you're a paying subscriber, the legitimate ways to get an article to me, best first:

1. **Claude-in-Chrome extension (recommended).** With you logged into Medium in Chrome, I drive the
   page through the extension using *your* authenticated session, so it sees member content. No scraping,
   no ToS gray area — it's your own logged-in browser. (Requires the extension connected.)
2. **Save logged-in → drop in workspace.** Open the article while logged in, *Print → Save as PDF* (or
   *Save page as → Web Page, Complete*), put the file in `/agent_workspace`. I convert it with the **pdf**
   skill or the **html-extractor** skill (it's built for exactly this — math/JS-shell pages → clean
   markdown).
3. **Paste the text.** Quickest for a single article; you copy, I work from it.
4. **firecrawl, properly set up.** `npm i -g firecrawl-cli`, `firecrawl login --browser`, then pass your
   Medium session cookie via headers. More moving parts, and cookie-passing is ToS-sensitive — only worth
   it if you're scraping many of your own subscribed articles in bulk.

For one-off reading of your own subscribed articles, option **1** or **2** is the clean path.

---

## Part 5 — Field-report ideas worth adopting (from the Medium reading)

Seven articles, read in full. The big three: a layering/separation model (Byern), the
Karpathy "four rules + harness loop" (Pandey/Hosni — *nearly identical to your own stated
preferences*), and the Claude auto-memory mechanics (Babich/Hosni). Most of it **validates** the
4DLab canon; a few things are genuinely new for us.

### 5.1 The separation model → map each layer to a file (and stop duplicating)

The cleanest idea: every instruction has exactly one owning layer; adapters *point*, they don't copy.
Mapped to our stack:

| Layer (Byern) | Owns | Our file |
|---|---|---|
| Global preferences | how *you* like to work | your user prefs (concise; don't-assume; minimal) |
| Project rules | repo conventions, tool-agnostic | `AGENTS.md` (the five rules) |
| **Architecture context** | system invariants/truths | `labs/<lab>/wiki/` + `ROADMAP.md` + `DECISIONS.md` |
| Tool adapter (thin) | tool-specific notes only | `CLAUDE.md` → `@AGENTS.md` |
| Skills (active) | reusable "how-to" workflows | `_skills/` |
| Task prompt (ephemeral) | one change's goal + acceptance | `labs/<lab>/tasks/<id>.md` |

**New for us — separate invariants from workflow.** Byern's sharpest point: keep *architecture truth*
(lab isolation, no cross-lab imports, graphs frozen, signal/noise) apart from *workflow* (inner loop,
task lifecycle). Today `AGENTS.md`'s five rules mix both. Consider tagging each rule **[invariant]** vs
**[workflow]** so a workflow tweak never weakens a system boundary. Also: the five rules + "Done means"
are currently restated in both `CLAUDE.md` and `AGENTS.md` — **state once, reference elsewhere** (the
`@AGENTS.md` adapter already lets `CLAUDE.md` stop copying them).

### 5.2 The coder behavioral contract (put this in Codex/Agy identity files)

Pandey's "monster CLAUDE.md" and Hosni's template both reduce to four rules + a harness — and they line
up with your preferences and our canon:

1. **Think before coding** — state assumptions, surface both readings, push back if simpler exists = our
   "scope confirm + ask one question if unclear."
2. **Simplicity / surgical / minimal impact** — touch only what the task needs.
3. **Goal-driven, verifiable end state, then loop** build→check→fix until the harness passes. Our harness
   is **not** empty (the failure mode they warn about): `ruff → pyright → pytest` + grep-confirmed
   consumer. Add an explicit **iteration cap + stop-and-report when stuck** to each coder file.
4. **Never mark done on "looks correct"** — prove it ("would a staff engineer approve?") = our two gate
   blocks + grep-confirm.

**Ban autonomous loops on the wrong work** (their hardest-won lesson): never loop on judgment calls,
design decisions, or long compute — for us that's graph rebuilds (already prohibited) and architecture
choices (architect's call). Wire this onto omp's real slash commands: `/plan` before any multi-file
change, `/review` (reviewer subagents, P0–P3 verdict) before flipping the ledger, `/commit` for atomic
commits. gstack's mantra — **"thin harness, fat skills"** — matches our "lean AGENTS.md + rich `_skills/`."

### 5.3 Memory — adopt two concrete patterns

- **`CLAUDE.local.md` (auto-gitignored)** for machine-specific values — the *exact* migration pain:
  absolute paths (`C:\Workspace` vs `/agent_workspace`), venv locations, sandbox URLs. Keep them out of
  the committed `CLAUDE.md` so it stays portable across the Windows→Linux move.
- **A `lessons.md` self-improvement loop** (Hosni): after any manager correction, the coder appends *the
  pattern + a rule to prevent recurrence* and re-reads it at session start. Lightweight, file-based,
  complements omp's `mnemopi` bank and our `progress_notes/`. Best kept per-lab (`labs/<lab>/tasks/lessons.md`).
- **Record dead-ends, explain WHY, prune monthly** (Babich) — already our `DECISIONS.md` instinct;
  the 200-line/25KB index discipline is exactly how the Cowork architect memory at `/home/m/.claude`
  already loads, so keep that file an index and push detail into topic files.

### 5.4 Wiki/Vault (Karpathy's "LLM-maintained wiki") → tighten the schema

Rusev runs `Vault/`-style Obsidian + an LLM against a **schema file**. Two lessons transfer to our
`labs/<lab>/wiki/` and `Vault/`: **"the schema is everything"** (precise page templates + YAML
frontmatter beat vague prose), and **"constraint improves quality"** — *selective* linking ("only link
where understanding A changes how you see B") beats liberal linking. Note this trades against our
memory-file guidance to "link liberally"; for a **domain wiki**, prefer selective.

### 5.5 The skeptic's counterpoint (from the comments — keep us honest)

Commenters on the "monster" piece pushed back usefully: big instruction files can encode **bloat**, and
the real win came from the author's **mathematical intuition, not the file** — the `CLAUDE.md` was a
forcing function, not a substitute for the spec. Takeaway, and it agrees with your "minimum" preference
and our signal/noise rule: **keep `AGENTS.md`/`CLAUDE.md` lean (~30–50 lines of project rules)**; don't
let them balloon. Pointers surfaced for deeper templates: `github.com/garrytan/gstack`,
`github.com/sumit-ai-ml/claude-md-starter`, and one from a comment — a larger example at
`github.com/liza-mas/liza` *(verify the exact URL)*.

---

## Part 4 — Verification checklist (don't trust the migration until these pass)

- [ ] `AGENTS.md` exists at root (capitalized); `grep -rin "agents\.md"` shows no stale lowercase refs.
- [ ] omp boots and loads the shared rules: ask a coder *"summarize your role and boundaries"* — Codex
      must answer "I am Codex, I implement one assigned task, I report via progress_notes, I am not the
      architect, I don't rebuild graphs." Agy mirrors it.
- [ ] The two coders read *different* identity files (Codex won't touch `agy/`, and vice-versa).
- [ ] Profiles isolated: `omp config path` under each launcher prints the right agent dir
      (`/home/m/.omp-codex/agent` vs `…-agy`); `omp config list` shows `memory.backend: mnemopi`.
- [ ] Each coder's `agent.db` holds its own login (`omp --list-models` resolves a model per role).
- [ ] `.venv-wired` + `.sandbox-py` rebuilt; inner loop green:
      `ruff check .` → `pyright <pkg>/` → `.sandbox-py/bin/python3.14 -m pytest -x -q`.
- [ ] Graphs queryable without rebuild: `python3 scripts/graph_health.py <lab>` (or your equivalent).
- [ ] No CRLF: `git status` clean immediately after clone; `git add --renormalize .` is a no-op.
- [ ] Parent-`4DLab` decision (§1.5) made and paths rewritten accordingly.

## Open items I need from you

1. **§1.5** — does `/agent_workspace` map to the parent `4DLab` or the `4DLabV2` child? (Changes every path table.)
2. **Rule-file format (the only remaining unknown).** omp discovers "rule files" from the cwd, but the
   public docs have no dedicated rules page, so I can't hand you exact lane-guard syntax yet. omp *does*
   ingest inherited rule formats (`.cursor/rules/*.mdc`, `.clinerules`, `.github/copilot`) — tell me
   which you'd prefer, or paste `omp config get` output for any `rules`/`hooks` key, and I'll write a
   ready lane-guard. Until then the AGENTS.md hard-boundaries (§2.3 **C**/**D**) are the guardrail.

---

**Sources (omp behaviour verified against the official docs, read logged-in):**
omp.sh/docs · /docs/quickstart · /docs/settings · /docs/memory · /docs/env · /docs/using · and the
project's own `AGENTS.md` and README on github.com/can1357/oh-my-pi.
```
