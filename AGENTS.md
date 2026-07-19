# 4DLabV2 — Agent Router

**Auto-loaded entrypoint** — Codex reads this as `AGENTS.md`; Claude Code reads `CLAUDE.md`; both route
here and to `START_HERE.md`. Maps role → where to look. Keep it short; the rules below are load-bearing.

> **Confused about "the graph" / tempted to graphify? Read `GRAPH_MANIFEST.md` first.**
> **graphify != LLM: code/tests/docs tiers build OFFLINE & FREE via `graphify update` (no key); only the wiki tier needs a backend. Building an index is not an LLM run. Canon: `GRAPH_AUDIT_2026-06-28.md`.**
> Query existing graphs, don't rebuild them; the root `graphify-out/` is frozen. Read-only
> `graphify query|explain|path|affected|diagnose --graph …` is coder-allowed (owner ruling
> 2026-07-06); build subcommands (update/extract/serve/…) are architect-lane only. Check a graph
> cheaply (no re-extraction) with `python3 scripts/graph_health.py [lab]`.

> **Web research → firecrawl (not WebFetch/WebSearch).** Any internet lookup — API refs, current
> docs, fact-checking a value, real-world corroboration — uses the `firecrawl` skill
> (`_skills/firecrawl-web-scraping-search/SKILL.md`). Write results to `.firecrawl/` (gitignored) with `-o`,
> then grep/read narrowly; a raw scrape into context blows the half-session budget.

## The five rules (in priority order)

1. **Query the graph before you grep.** Each lab has its own graph at `labs/<lab>/graph/v2_current/`.
   Query it for a symbol's file/line before reading files blindly. Do **not** re-run the root
   `4DLab/graphify-out/` canonical graph — it is regenerated only on explicit instruction.
2. **Read the lab wiki for domain truth.** `labs/<lab>/wiki/` is the canonical source for that lab;
   code reconciles *up to* the wiki. Legacy `v2/`, `v6/`, and v1 wikis are not truth.
3. **A task is a file.** Work items live at `labs/<lab>/tasks/<id>.md` (the spec) with gates recorded in
   `labs/<lab>/tasks/progress_notes/<id>.md`. Follow the task file exactly; one task per session.
   **Ledger runnability:** in `tasks/PROGRESS.md`, `pending` means **runnable now** (spec authored,
   blockers `done`). A forward-registered or otherwise unauthored row stays **`deferred`** until its spec
   exists — never `pending`, and never a `pending (...)` variant. The first `pending` row top-to-bottom is
   the next runnable task; `deferred`/`blocked` rows are skipped.
4. **Signal/noise governs every field — and v2 progresses forward.** A field/fault ships only with a
   **named** consumer + code path in COMLab analytics or fault-atlas routing ("future use" is not a
   consumer). But v2 reworks v1: that consumer **may be one you add in the same change** — a new
   field/fault and its new consumer **ship together as a proposal** (marked in a *separate* proposals
   registry, e.g. `comlab/config/proposals/`, never silently in the live KG, plus its task spec).
   **"Not in v1" is not a reason to defer.** Default new improvements to **proposal**; defer/PENDING
   only when no consumer can be named at all. See `4DLab_CLAUDE.md` → "Progress the app forward".
5. **Lab isolation.** No cross-lab Python imports; consumers mirror the types they need locally over
   JSON boundaries. Reports in `.md` only. Obsolete files are **archived, never deleted**.

## Where to go

| You are… | Read first |
|---|---|
| Orienting (any role) | `START_HERE.md` → `ROADMAP.md` |
| Architect (writing a spec) | the lab's `wiki/` + `graph/` → author `labs/<lab>/tasks/<id>.md` |
| Builder (implementing) | `labs/<lab>/tasks/<id>.md` → inner loop → fill `progress_notes/` gates |
| Restructure status | `../v2-restructure/EXECUTION_LOG.md` |

## Layout (flat by design)

`labs/<lab>/` (package · `tests/` · `tasks/` · `wiki/` · `graph/`) · `apps/{ui,wired}/` ·
`harness/` · `docs/` · brain docs at this root. Infra (shared `.venv-wired`, inner loop, git ritual)
is inherited from `4DLab_CLAUDE.md` (Linux-adapted; one shared host venv, run natively).

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

## Carry-over invariants (from the former CLAUDE.md — apply to all coders)

- **Scope-confirm before code:** post a one-paragraph confirm (field · guard · signal/noise consumer ·
  files) before writing code. Unclear scope/consumer/files → **ask one question first**, don't guess.
- **Numeric literals carry a wiki citation** (`# wiki: §...`).
- **Emitter labs emit channels, not verdicts.** OBDLab/DTCLab emit their own signals; cross-lab fault
  verdicts are COMLab fusion (built last).
- **Git:** owner commits **by explicit path**; **never stage `graphify-out/`**.

## Vault conventions (this repo is an Obsidian vault)

The workspace root is an Obsidian vault; the architect navigates it as a graph. Coders edit the
**live** tree only and leave a navigable trail:

- **Graph before grep** (rule 1): query `labs/<lab>/graph/` for a symbol's file/line before reading
  blind; follow `[[WikiLinks]]` in wikis and progress notes rather than re-discovering paths.
- **Leave backlinks.** When a progress note names a task, wiki topic, or consumer, write it as
  `[[note-name]]` so it surfaces in Obsidian backlinks/graph. Zero cost; pure transparency.
- **Keep node frontmatter intact** when you touch a `wiki/`/`docs/` note: preserve
  `node_type / lab / module / implements / consumers / drift_guards / tags / source` (schema:
  `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`). Never invent `node_type` values.
- **Never edit `Vault/`.** It is an archived architect mirror — edit the live `labs/<lab>/` source.
  (Enforced: `.omp/rules/lane-guard-no-vault-edit.md`.)

## Domain facts — wiki-first (added 2026-07-06)
Every lab ships its own `wiki/` and `docs/` folders — **reference them first whenever in doubt**
about a domain fact (trim grammars, Mode $06, gas chemistry, fault signatures, thresholds):
live source `labs/<lab>/{wiki,docs}/`, readable mirror `Vault/labs/<lab>/{wiki,docs}/` (never edit
Vault). The web (firecrawl) is only for what the repo does not answer; if wiki and web disagree,
STOP and surface the conflict (see 4DLab_CLAUDE.md §Wiki-first and DECISIONS.md Q-C5-EGR).

Query paths (sanctioned CLI baseline):
- Search the wiki: `python3 _skills/graph/4dlab-vault/scripts/vault_query.py --vault Vault wiki <lab> "<term>"` (or `grep` to search wiki, docs, and code)
- Query the graph: `graphify query "<question>" --graph labs/<lab>/graph/v2_current/graph.json` (also supports `explain`, `affected`, and `path`)

## Firecrawl auth (added 2026-07-06)
`FIRECRAWL_API_KEY` is exported automatically by every `run-*.sh` launcher (read at launch from
`_skills/firecrawl-web-scraping-search/API.md`). `firecrawl --status` should report Authenticated;
if it does not, STOP and report — do not fall back to memory-written "citations".
