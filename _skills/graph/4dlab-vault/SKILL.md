---
name: 4dlab-vault
description: >
  Build and maintain the 4DLab Obsidian vault at Vault/ — a graph-aware
  knowledge vault that mirrors FINISHED, graphified labs (code + tests + wiki)
  as navigable Obsidian notes with consumer-aware frontmatter and Bases views.
  Use this skill whenever the user wants to: "build/update the Obsidian vault",
  "add <lab> to the vault", "set up the 4DLab vault", "make the codebase
  navigable in Obsidian", "create the graph-aware vault", or to **query/read** the
  vault ("which task is next", "what consumes X", "what guards Y", "search the
  vault", "query the ledger") via scripts/vault_query.py, or mentions Vault/,
  .base views, the node frontmatter schema (module/implements/consumers/
  drift_guards), or copying a finished lab's code/wiki into Obsidian. Apply it
  before hand-copying any lab into Vault/ — doing that without this skill
  produces inconsistent frontmatter and breaks the Bases views. Do NOT use it
  to re-run graphify (that is 4dlab-graphify-run) or for labs that are not yet
  finished and graphified.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# 4DLab Vault Skill

Build the Obsidian vault at `Vault/` so the team and agents can navigate
**finished** labs — code, tests, and wiki — as a linked graph, with every note
carrying a **named downstream consumer**. The vault is read-mostly: a window
onto the labs, not a second source of truth. The canonical graph stays at each
lab's `graphify-out/graph.json`; the vault never re-extracts it.

## Why this skill exists

Hand-copying a lab into Obsidian gives you browsable files but no graph: no way
to ask "which tests guard `ve_engine`?" or "what consumes the trim payload?".
This skill injects a small, disciplined frontmatter schema and three Bases views
so those questions are answerable in the UI — without duplicating the labs or
inventing relationships the graph doesn't support.

## The one rule that governs the vault

Every frontmatter field must be **read by a named consumer** — a `.base` view or
a documented command. `consumers` lists are **authored by a human, never
auto-derived** from the graph: auto-deriving fabricates consumers and breaks the
signal/noise principle. The schema and its consumer table are authoritative in
`reference/frontmatter-schema.md` — read it before changing any field.

## When a lab is eligible

Copy **only finished, graphified labs.** A lab qualifies when it has its source,
tests, wiki/prose, docs, and the graph tiers required by `build_lab_vault.py`.
OBDLab requires all four tier graphs. GASLab has an owner-approved waiver
(2026-06-11) for prose Pass-3, so it requires `v2_code` and `v2_tests`; the
prepared wiki/docs are copied from the Phase-2 outputs without `v2_wiki` or
`v2_docs/graph.json`.
If asked to add a lab that doesn't, stop and say so — don't half-populate.

## Workflow

Work in this order. Confirm scope in one paragraph (which lab, where its four
inputs are, who the consumers are) before writing anything.

0. **Build the shared `_vocabulary/` area** (once, before or alongside the first
   lab). This is a cross-lab shared resource — it does not live under any single
   lab's folder.
   ```bash
   python3 scripts/build_lab_vault.py --vocab \
     --repo <abs path to 4DLabV2> --dry-run
   python3 scripts/build_lab_vault.py --vocab \
     --repo <abs path to 4DLabV2>
   ```
   Reads `assets/vault-map.vocabulary.yaml`, copies each canonical vocab body,
   injects §4 frontmatter, and records provenance. Idempotent.
1. **Verify eligibility.** Check the four inputs above exist for the lab. If
   `graph.json` is missing, the lab isn't ready — stop.
2. **Author/confirm the consumer map.** Open `assets/vault-map.<lab>.yaml`. It
   maps each wiki note → `module`, `subsystem`, `implements`, `consumers`,
   `drift_guards`. For OBD this is pre-filled; for a new lab, author it from the
   lab's README + DLD + `graph.json` relationships. **Do not leave `consumers`
   empty** — if you can't name one, that note isn't ready to ship.
3. **Dry-run the build.**
   ```bash
   python3 scripts/build_lab_vault.py --lab <lab> \
     --repo <abs path to 4DLabV2> --dry-run
   ```
   Review the planned copies and frontmatter injections.
4. **Build.** Re-run without `--dry-run`. It copies `code/`, `tests/`, `wiki/`,
   `docs/` into `Vault/labs/<lab>/`, injects frontmatter skeletons, merges the
   semantic fields from the map, and writes the lab landing note. Idempotent.
5. **Install the views.** Copy `assets/*.base` into `Vault/_bases/` (the script
   does this; verify). Refresh `Vault/System-Map.md` and `_meta/PROVENANCE.md`.
6. **Check in Obsidian.** Open `Vault/`. Confirm the three Bases render and that
   `orphans` / `unresolved` are empty or explained. See
   `reference/obsidian-cli-optional.md` if you want to script these checks.

## What gets copied (and what does not)

| Copied into `Vault/labs/<lab>/` | Source | Note type in vault |
|---|---|---|
| `code/` | `<lab>/<lab>/` | raw `.py` (link targets, not graph nodes) |
| `tests/` | `<lab>/tests/` | raw test files (link targets) |
| `wiki/` | `<lab>/research/chunks/` | `.md` notes **+ injected frontmatter** |
| `docs/` | `<lab>/docs/` | `.md` design docs **+ injected frontmatter** |

Shared `_vocabulary/` (cross-lab, built via `--vocab`):

| Copied into `Vault/_vocabulary/` | Source | Note type |
|---|---|---|
| `OBD_VOCABULARY.md` | `labs/semantic/vocabul/OBD_VOCABULARY.md` | `.md` canonical body **+ injected frontmatter** |

**Not copied:** `graph.json` / `graphify-out/`, caches, `.egg-info`, `audit/`,
`tasks/`. `research/chunks/` is the wiki tier source; the `wiki/` folder is retired. Graph-awareness comes from the injected frontmatter, not
from dumping the graph. (If the user explicitly wants the graph artefact
in-vault for offline reference, that's a deliberate add — ask first.)

## Querying the vault (read side)

Building the vault is only half the job; the architect also **reads** it to spec
tasks. The native `obsidian` CLI is an IPC remote control for the Windows desktop
app and is **unreachable from the agent's Linux sandbox** (it returns
`command not found`). Do not reach for it in agent flows. Instead use the bundled
script, which treats the mounted vault as raw data — no app, no IPC, no licence —
and reads both the `.base` frontmatter contract and the inline `**Status:**`
ledger markdown, plus Python source via the AST:

```bash
python3 scripts/vault_query.py --vault Vault [--json] <command> [args]
```

| Command | Answers | Mirrors |
|---|---|---|
| `consumers [--missing]` | which framed notes name a consumer (`--missing` = breaches) | `consumers.base` |
| `drift` | code a note implements vs the tests guarding it | `drift-guards.base` |
| `modules` | framed notes grouped by lab | `modules.base` |
| `tasks [STATUS]` | the FX ledger rows (frontmatter, inline fallback) | `tasks.base` |
| `next` | first `pending` task whose `blocked_by` are all `done`/`void` | the one-task-per-session picker |
| `backlinks TARGET` | notes that link to / mention `TARGET` | Obsidian backlinks (looser: string match) |
| `code LAB [SYMBOL]` | AST map of classes/functions/imports in `labs/LAB/code` | — (closes the frontmatter gap on code) |
| `docs LAB QUERY` | content search inside `labs/LAB/docs` | — |
| `health` | one-shot gate report: signal/noise, coverage, ledger integrity, cycles, `.base` presence, next | all of the above + `tasks.base` |

`health` is the re-runnable gate (exit 1 on FAIL, WARN/PASS otherwise) — run it before closing any vault task. `next` is the canonical way to obey the "run