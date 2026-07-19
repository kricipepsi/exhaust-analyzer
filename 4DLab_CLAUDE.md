# 4DLab profile — 4DApp (Linux-adapted infra + canon)

> **What this file is.** The former *parent* `4DLab/CLAUDE.md` (the "4DApp profile"),
> adapted to the Linux Mint native host and brought **in-mount**. The architect
> entrypoint (`CLAUDE.md`) and the coder canon (`AGENTS.md`) point here for the
> infra (venv, inner loop, git ritual) and the load-bearing principle sections
> (role, "progress the app forward"). Adapted 2026-06-27. The original Windows
> copy is preserved at `/home/m/Desktop/claude/CLAUDE.md`.

## Role — architect, not coder (HARD RULE)
In this workspace the Cowork/Claude agent operates as the **architect**. The
architect's deliverable is the **task file** (the spec): it reads the wikis,
ledgers, and code, pins exact bounds/citations/consumers, defines success
criteria and scope, and writes/maintains the `tasks/` rows and files. A
**separate coder session** (an omp agent — Codex or Agy) then implements that
spec — writes the `gaslab/` (etc.) code, runs the inner loop
(`ruff`/`pyright`/`pytest`), and fills the `VERIFICATION GATE` + `CODE REVIEW`
blocks.
- The architect does **not** write implementation code, run the inner loop, or
  execute the gate. Reading code/wiki is allowed and expected — but only to make
  the spec precise (e.g. pin a threshold so the coder doesn't invent it).
- The architect's "done" is a complete, unambiguous task file with a named
  signal/noise consumer (a field/fault that is actually read by a code path) —
  not green tests. Green tests are the coder's gate.

### Which session am I — coder or architect? (decide BEFORE assuming the role above)
- **You are Cowork, talking to the owner directly** to plan, spec, research, or
  author/maintain `tasks/` files: **you are the ARCHITECT** and the rule above
  applies in full (no implementation code).
- **You are an omp session launched via `run-codex.sh` / `run-agy.sh`** with a
  pack bootstrap in play — a `*_START_HERE.md` (e.g. `OBDLAB_TASKS_START_HERE.md`,
  `GASLAB_TASKS_START_HERE.md`): **you are the CODER** for that pack. You write
  the implementation code, run the inner loop, and fill the gate blocks. Your
  per-coder identity at `.agent/coders/<you>/AGENTS.md` plus the START_HERE
  override the architect rule for your session.
Tie-breaker: **a loaded `*_START_HERE.md` wins the role question.** A coder
session never reclassifies itself as the architect because it saw this rule.

## Progress the app forward (v2-rework principle — HARD RULE)
4DLabV2 exists to **rework the non-working v1 engine**, not to preserve it. When
research or a task surfaces a new diagnostic expression — a fault, field, enum
value, or signal — that would genuinely improve the engine, the **default is to
add it together with a named consumer and code path, registered as a proposal.**
"Not in v1" is never a reason to defer.
This **complements, does not weaken, the signal/noise rule:**
- Signal/noise still holds: nothing ships without a **named** consumer and the
  code path that reads it. "Future use" is still not a consumer.
- The clarification: that consumer may be **one you add in the same change**. A
  new field/fault and the new consumer that reads it **ship together as a
  proposal** — the consumer does not have to pre-exist in v1.

### Provisional synthetic signals (pre-launch bootstrap) — supersedes "never synthesize"
Real per-case sensor readings do not exist until the app has users. Until then a
signal pack **MAY seed** its required corpus columns with **research-grounded
synthetic values**, under four binding conditions:
1. **Grounded in ground truth + research band, not back-solved.** Each synthetic
   value is derived from the case's **oracle fault** through the cluster research
   signature (a `rich_mixture` case gets a fuel trim inside the research's rich
   band). It is never reverse-engineered from the consumer rule to force a pass.
2. **Tolerance-wide, not lab-precise.** Real cars vary; the synthetic values **and
   the producer bands that read them** carry realistic spread/margin so a case
   passes robustly under tolerance, not on a knife-edge. **Every signal-pack task
   states its tolerance width** — this is mandatory on each task.
3. **Labeled provisional + tracked.** Synthetic values carry a `synthetic=true`
   provenance flag; the scoreboard keeps a **synthetic-vs-real split** so no metric
   is mistaken for field accuracy. `top3_family` on synthetic data measures *engine
   discrimination given research-consistent input*, not real-world performance.
4. **Correctable.** When real user data lands, synthetic values are replaced/
   calibrated; the flag makes them findable.
5. **Wiki-first, then web-corroborated before commit.** Before ANY web research,
   grep the lab wikis (`labs/<lab>/wiki/`, e.g. dtclab `03_fuel_trim_grammar.md`
   holds the canonical trim-pattern table) — the wiki is the repo's source of
   truth for domain facts, and re-researching it wastes the budget and can
   contradict canon (the 2026-07-06 C5 EGR seed did exactly that). If the wiki
   and external research disagree, STOP and surface the conflict to the owner —
   do not silently pick one. Then, for what the repo does NOT answer,
   cross-check the band against **real-world reported values** via web research
   (documented fuel-trim / Mode $06 / gas ranges for that fault on real vehicles),
   and widen/shift the band to match field reality. **Cite sources.** Do this web research with the
   `firecrawl` skill (`_skills/firecrawl-web-scraping-search/SKILL.md`), never WebFetch/WebSearch. This anchors
   synthetic values to real cars, not just lab/research bands; where the web
   corroborates a wider spread than the research, prefer the wider (tolerance-wide).
The structural **signal/noise rule still holds**: every field ships with a named
producer AND consumer. What changed: *never synthesize* → **synthesize
provisionally — grounded, tolerant, labeled — and calibrate on real data.** Cases
the research cannot ground stay **abstained**, not guessed.
So new content has exactly two dispositions:
1. **Proposal (the default for improvements).** A new fault/field/enum whose
   consumer *can* be named and specced. Mark it as a **proposal** — in the
   manifest/task file **and** in config (a **separate proposals registry**, e.g.
   `comlab/config/proposals/`, never silently inside the live KG/registry) — name
   its consumer + code path, and track it to a task spec. This is forward progress.
2. **Defer / PENDING (the narrow exception).** Only when **no consumer can be
   named at all**, not even a proposed one. Genuine staging.
Reaching for "defer/PENDING" when a consumer *could* be named is the mistake.
Default to **proposal**.

## Author disclosure-first (progressive disclosure — HARD RULE)
When you author a task pack, order and shape tasks so each one **reveals** what
the next decision needs before any task **commits** to that decision:
1. **Disclosure upstream of commitment.** The task that reveals a
   decision-relevant unknown (a measured number, a residual, a feasibility) is
   `Blocked by`-upstream of the tasks whose scope depends on it.
2. **Split disclose-from-commit.** If one task both discloses a fact and commits
   a policy calibrated on it (a threshold, re-tune, re-pin), split it — ship the
   disclosure, defer the commitment as a separate task blocked on it.
3. **One live task at a time.** For the owner's step-by-step loop, fully author
   only the next runnable task; keep the rest forward-registered in the ledger
   until the prior task's disclosure lands.
4. **Tier + surface.** Tier measurement outputs essential-first (headline →
   summary → per-case detail in JSON); every task names what it must **surface,
   not hide**.
This complements one-task-per-session and the signal/noise rule. Full authoring
mechanics: `_skills/coding-bootstrap/SKILL.md` ("Why this works" constraint 4).

## User preferences (rules)
- **Reports always and strictly in `.md` format.** Never deliver `.docx`, `.pdf`,
  or other formats unless the owner explicitly overrides this for a single task.
  Applies to every analysis, study, recommendation, and deliverable here.
- **Gloss coding jargon inline for the non-coder owner.** On the **first** use of
  a coding/tooling/architecture term (lint, stub, shim, refactor, schema, enum,
  consumer, code path) attach a 3–10 word plain-language gloss in a clause — never
  a separate paragraph, never repeated for the same term in one reply. Do **not**
  gloss automotive/diagnostic terms (PID, DTC, lambda, freeze frame, sensor and
  chemistry names) — the owner knows those cold. Keep answer length unchanged.

## Git — minimal fixed ritual (HARD RULE)
> **Status (2026-06-27): git is not yet initialized in `/agent_workspace`.** The
> owner brings the real `.git` later (with the data). Until then there is no undo
> button beyond the Desktop backup (`/home/m/Desktop/migration`). **Never run
> `git init`** — it would clash with the incoming repo. The ritual below is what
> applies **once `.git` lands**.

Git exists only as a safety net (an undo button). Keep interaction to the fixed
minimum below — agents that turn git into a decision are the recurring time-sink
this rule kills.
- **Never raise git as a blocker.** Never create branches, worktrees, or stashes.
  Never ask "which branch?" — the answer is always: proceed in the current
  checkout on **main**.
- **Never touch pre-existing uncommitted changes.** Do not commit, revert, or
  stash them; leave them on disk.
- The **only** git action is the final commit, run **by the owner**, staging the
  task's deliverables **by explicit path** from the workspace root:
  ```bash
  cd /agent_workspace
  git add path/to/file1 path/to/dir2/
  git commit -m "<task-id>: <one-line summary>"
  ```
  Use literal filenames — never `<...>` placeholders. For many paths, use bash
  line-continuation (`\` at end of line):
  ```bash
  git add \
    labs/gaslab/gaslab/foo.py \
    labs/gaslab/tests/test_foo.py \
    labs/gaslab/tasks/progress_notes/T-GAS-X.md
  ```
- If `git add` reports "did not match any files", that path wasn't changed: drop
  it, keep the paths that were.
- **Never stage** `.venv-wired/`, `graphify-out/`, or `labs/vinlab/mysql_data/`.
An agent doing anything with git beyond preparing that one commit is the bug.

## Document readability gate (MANDATORY)
Before using any document as task input, verify all three:
1. **No image placeholders** — search for `![][` in `.md` files. If found, STOP.
2. **Full read confirmed** — if Read returns a truncation warning ("PARTIAL
   view — showing lines X of Y total"), STOP.
3. **Formula content present** — if the doc references equations and none are
   visible as text or LaTeX, STOP.
On any STOP: alert the owner with the exact failure reason and file path; do not
proceed until a readable version is provided. Do not attempt format conversion,
re-reads, or workarounds without explicit instruction.
**Known safe:** `.md` exported from Gemini with plain-text math. **Known unsafe:**
Google Docs `.md`/`.pdf` export (formulas become images); files exceeding the
Read line cap.

## Project context
- 4D Petrol Diagnostic Engine — petrol-only (no diesel in v1, see `PRD_4D_App.md` §5).
- Pipeline layers: L1 idle gas → L2 high-idle gas → L3 DTCs → L4 freeze frame → L5 live PIDs.
- Truth-vs-Perception override: gas chemistry (Brettschneider lambda) is ground truth, ECU is perception.
- Per-lab knowledge graphs are frozen — query them, never re-`graphify` them. (graphify != LLM: code/tests/docs tiers build OFFLINE & FREE via `graphify update` (no key); only the wiki tier needs a backend. Building an index is not an LLM run. Canon: `GRAPH_AUDIT_2026-06-28.md`.)

## Python environment (Linux native — READ BEFORE TOUCHING THE VENV)
This host is **not** an ephemeral sandbox. Cowork (architect) and the omp coders
(Codex, Agy) run **natively on one filesystem** and **share a single venv**
(isolated Python with its own packages). The Windows-era split (Windows
`.venv-wired` vs a resetting Linux sandbox with a `.sandbox-py` cache) **no longer
applies** — there is one venv, built once, persistent.

- **Interpreter:** Python **3.14.6**, uv-managed, permanent, at
  `/home/m/.local/bin/python3.14`. The requirement is **3.14 or later**. The
  system default is 3.12 — **always invoke `python3.14` explicitly**; never bare
  `python`/`python3`.
- **Shared venv:** `/agent_workspace/.venv-wired`. Its interpreter symlinks to the
  host uv 3.14.6 (it *is* the already-installed environment, not a copy). Both
  roles use it.
- **There is no `.sandbox-py` and no per-session download ritual.** If you see
  those in old docs, they are obsolete — do not recreate them.

**Build recipe (run once; idempotent — re-running is harmless):**
```bash
cd /agent_workspace
uv venv --python 3.14 .venv-wired
uv pip install --python .venv-wired/bin/python \
  -e apps/wiredV2 -e labs/comlab -e labs/dnalab -e labs/dtclab \
  -e labs/gaslab -e labs/obdlab -e labs/symptomlab -e labs/vinlab \
  pytest pytest-cov ruff pyright jsonschema
```
(`uv pip install -e` resolves each package's deps — pydantic, PyYAML — automatically.)

**Inner loop (coder gate — run per-lab, not across the whole tree):**
```bash
cd /agent_workspace/labs/<lab>
source /agent_workspace/.venv-wired/bin/activate   # so pyright sees the venv
ruff check .
pyright <pkg>            # or: pyright --pythonpath /agent_workspace/.venv-wired/bin/python <pkg>
pytest -x -q
```
- **Run the loop per-lab.** Collecting `labs` + `apps` together produces spurious
  duplicate-test-basename import errors — an invocation artifact, not a real
  failure. Lab isolation means lab-scoped runs are the truth.
- **pyright needs the interpreter.** Without an activated venv (or `--pythonpath`),
  pyright cannot resolve `pydantic` and reports false "missing import" errors.
- **Coders launched via `run-*.sh` already have `pyright` on PATH.** The launchers
  now export `PATH="$VENV/bin:$PATH"` alongside `VIRTUAL_ENV` (previously only the
  latter, so bare `pyright`/`python` resolved to nothing / system 3.12 and the gate
  reported the tool "not found"). Inside a launched session, bare `pyright` and
  `python` work. If you ever run a coder *outside* these scripts, still
  `source .venv-wired/bin/activate` or call the tool by full path.
- **Never commit `.venv-wired/`** (~90 MB). It goes in `.gitignore` once git lands.

## Session bootstrap (architect: read before responding; coder: the START_HERE leads)
Paths below are **in-mount** under `/agent_workspace` (= the former
`4DLabV2/`). Rows marked **[off-mount]** live one level up in the parent `4DLab/`
tree and **dangle** on this child mount — fetch from the on-hand `4DLab` copy or
the Desktop backup only if a task needs them.

| If the session is about… | Read and execute this file first |
|---|---|
| 4DLabV2 general workspace | `/agent_workspace/START_HERE.md` → `ROADMAP.md` |
| GASLab v2 (Stage 1) | `/agent_workspace/labs/gaslab/tasks/GASLAB_TASKS_START_HERE.md` |
| GAS→Vault pipeline pack | `/agent_workspace/Vault/tasks/GAS_VAULT_TASKS_START_HERE.md` |
| DTC→Vault pipeline pack | `/agent_workspace/Vault/tasks/DTC_VAULT_TASKS_START_HERE.md` |
| OBDLab v2 (Stage 2) | `/agent_workspace/labs/obdlab/tasks/OBDLAB_TASKS_START_HERE.md` |
| DTCLab v2 (Stage 3) | `/agent_workspace/labs/dtclab/README.md` |
| COMLab v2 (Stage 4, last) | `/agent_workspace/labs/comlab/README.md` |
| 4DLabWired v2 — app & composition | `/agent_workspace/apps/wiredV2/WIREDV2_START_HERE.md` |
| Generative test harness | `/agent_workspace/harness/HARNESS_START_HERE.md` |
| Per-lab test-harness rollout | `/agent_workspace/planning/test_rollout/TEST_ROLLOUT_PROGRESS.md` |
| GPF removal (cross-lab) | `/agent_workspace/planning/gpf_removal/GPF_REMOVAL_START_HERE.md` |
| Registry rebuild | **[off-mount]** `4DLab/registry/REGISTRY_START_HERE.md` |
| Jaeger-run remediation patch | **[off-mount]** `4DLab/patch/PATCH_START_HERE.md` |
| DIAG post-patch investigation | **[off-mount]** `4DLab/diag/DIAG_START_HERE.md` |
| FX cross-lab gaps | **[off-mount]** `4DLab/FX_START_HERE.md` |
| Any other lab or module | `README.md` in the lab/app root |

"Execute" means: read each mandatory skill, read the progress ledger, identify
the first unblocked `pending` task, and present a one-paragraph scope confirm —
before any other output. The bootstrap files are procedures, not documentation.

## One task per session — HARD STOP (every pack)
- **Finish exactly one task, update its ledger row, then STOP** and tell the owner
  to clear context. Do not select, author, or begin a second task in the same
  session — not if unblocked, not if the owner named it, not if "there is room."
  The next task starts fresh via the pack's `*_START_HERE.md`.
- **Run the task the ledger picks, not the one you were handed.** The next task is
  the first `pending` row whose Blocked-by IDs are all `done`.
- **Atomic ledger updates.** Authoring a task file and writing its ledger row are
  one operation. Never retro-flip a row to `done` whose deliverable is unmet.
- **Anti-orphan check before `done`.** If a task was contracted to *consume* a
  field/enum, `grep` it and confirm it is read in a live code path — a field
  defined but read nowhere is an orphan and a signal/noise breach, green tests or not.
- **Stale-ledger guard at session start.** If a row isn't `done` but its note
  shows clean gates, or a `done` row's ledger mtime predates its task file, STOP
  and surface the mismatch.

## Skill precedence (plugins)
When a plugin skill conflicts with the instructions in this file, **these
instructions win.** Plugin skills are on-demand guidance, not overrides.
