# The graph / graphify riddle — settled (2026-06-12)
> **[2026-06-28] Inventory below is a stale 06-12 Windows scan — see `GRAPH_AUDIT_2026-06-28.md`
> for the live state. This doc settles the *human-vs-agent* split; the *offline-vs-LLM* split is
> in the CANON block added below.**


There are **two completely different things** in this workspace that both get called
"the graph." Almost every wasted session comes from confusing them.

| | **graphify `graph.json`** | **Obsidian graph view** |
|---|---|---|
| Who it's for | coding **agents** | **humans** (you) |
| What it is | a machine-readable index of code/wiki | a live picture drawn on screen |
| Built by | the `graphify` tool — **offline & free** for code/tests/docs (`graphify update`); only the **wiki** LLM pass costs tokens + needs a backend | Obsidian itself, instantly, free |
| Built from | source code, tests, wiki, docs | the `[[wikilinks]]` between Vault notes |
| Stored as | a `graph.json` file on disk | **nothing is stored** — redrawn each time you open it |
| Purpose | "query the graph before you grep" — find a symbol's file/line | see how modules connect, for transparency |

---

## Graph nomenclature — CANON (strict; added 2026-06-28)
Three different things get called "graph." Keep them apart:

1. **Obsidian graph view** — the live picture Obsidian draws from `[[wikilinks]]`. Human-facing.
   Not a file, never built, never stored. (The Vault deliberately holds no `graph.json`.)
2. **graphify index** (`graph.json`) — the machine index agents *query*. Built two ways:
   - **Offline extraction** — tree-sitter AST (code/tests) or markdown structure (docs).
     **FREE: no LLM, no API key, no backend.** Command: `graphify update <path>`. Edges = `EXTRACTED`.
   - **LLM Pass-3** — semantic inference. Costs tokens + needs a backend. Edges = `INFERRED`.

Tier -> build mode (strict):

| tier | mode | cost | command |
|---|---|---|---|
| `v2_code`  | offline AST       | free, no key | `graphify update` |
| `v2_tests` | offline AST       | free, no key | `graphify update` |
| `v2_docs`  | offline structure | free, no key (after doc-prep, edges come back EXTRACTED) | `graphify update` |
| `v2_wiki`  | LLM Pass-3        | tokens + backend | `graphify extract --backend <name>` |

**`graphify` != `LLM`.** Building a graphify index does NOT imply an LLM run. Only the **wiki** tier
needs a backend. If a code/tests/docs build asks for an API key, the wrong subcommand was used — use
`graphify update` (offline), never `graphify extract` (which adds the semantic-LLM pass).

Evidence (live scan 2026-06-28): registry & obdlab `v2_docs` are 100% EXTRACTED / 0 INFERRED (offline,
verdict GOOD). The strongest LLM tier, obdlab `v2_wiki`, is only ~17% INFERRED (84/494 edges). So the
LLM layer is marginal for docs and modest for wiki.

## 1. What must be graphed (with `graphify`)

Only the **lab material that agents need to query**, one graph per lab, kept under
`labs/<lab>/graph/`. The intended set is four tiers per lab — `v2_code`, `v2_tests`,
`v2_wiki`, `v2_docs` — plus the frozen whole-repo index.

Current state found in the scan:

| Lab | graphs present | tiers built |
|---|---|---|
| gaslab | v1_baseline, v2_current, v2_code, v2_tests, v2_docs | code + tests built; wiki/docs LLM pass **waived by owner** |
| obdlab | v1_baseline, v2_current, v2_code, v2_tests, v2_wiki, v2_docs, v2_docs_llm | most complete |
| dtclab | v1_baseline, v2_current, v2_code, v2_tests, v2_docs | code + tests built |
| comlab | v1_baseline, v2_current | code/tests tiers **not** built |
| dnalab | v1_baseline, v2_current | code/tests tiers **not** built |
| vinlab | v1_baseline, v2_current | code/tests tiers **not** built |
| symptomlab | v1_baseline, v2_current | code/tests tiers **not** built |
| **root** | `graphify-out/graph.json` | whole-repo, ~43k ids, 39 MB — **canonical and FROZEN** |

So "what must be graphed" = each lab's code/tests/wiki/docs into its own `graph/` folder.
The root whole-repo graph is **already done and must not be re-run** except on explicit
instruction.

## 2. Why there are no graphs in the Vault — and why that is correct

This was the design intent, and the scan confirms it works as intended:

- `Vault/_meta/PROVENANCE.md` literally says the canonical graphs are
  **"required (not copied)"** — the Vault points at `labs/<lab>/graph/` by **path**.
  Duplicating a 39 MB `graph.json` into the Vault would be dead weight that goes stale.
- The Vault is an **Obsidian vault** (it has `.obsidian/`, `_bases/`, wikilinked notes).
  Obsidian draws its **own** graph live from the `[[wikilinks]]` in those notes. That is
  exactly your original idea — Obsidian gives module transparency for free, with no
  `graph.json` needed.

**Verdict: the missing graph.json in the Vault is not a bug. It is the design.** If the
Obsidian picture looks thin, the fix is **more/better wikilinks and frontmatter in the
notes**, never copying a graphify graph in.

## 3. Why coding agents constantly try to graphify without need

Five compounding causes, all fixable:

1. **The word "graph" is overloaded.** Skills, tasks, and rules all say "graph," so an
   agent reaches for the `graphify` tool reflexively.
2. **Seven skills live in `_skills/graph/`** (`4dlab-code-prep`, `4dlab-wiki-prep`,
   `4dlab-doc-prep`, `4dlab-graphify-run`, `4dlab-graph` (deprecated), `4dlab-vault`,
   plus copies). Their descriptions trigger on phrases like "graphify the code." Eager
   triggering = unprompted runs.
3. **`AGENTS.md` rule #1 says "Query the graph before you grep."** Agents misread *query*
   (read the existing file) as *build* (re-run extraction). Querying ≠ rebuilding.
4. **Many task files are named `*_graphify_*`** (e.g. `T-GAS-GRAPH-AST`, `T-KG-OBD-1..3`),
   which makes graphifying look like the default chore.
5. **The deprecated `4dlab-graph` skill once had a `build` operation** that re-ran
   extraction and even wrote fake edges — that habit lingers in agent behaviour.

**The one rule that stops the leak:** the canonical `graphify-out/graph.json` is frozen.
Agents *query* existing graphs; they *rebuild* only when a task file explicitly says so.

## 4. Where graphify is mentioned in the docs (the source of the instruction)

- `4DLab/CLAUDE.md` (root) — *"Never re-run the full graphify extraction unless explicitly
  instructed. The verified graph at `graphify-out/graph.json` is the canonical artefact."*
- `4DLabV2/AGENTS.md` — rule #1: *"Query the graph before you grep … Do not re-run the
  root canonical graph."*
- `4DLabV2/.graphifyignore` — exclude list for graphify runs.
- `4DLabV2/_skills/graph/` — 7 graphify-related skills (the main trigger source).
- `4DLabV2/Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`, `DTC_VAULT_TASKS_START_HERE.md`
  and the `T-*-GRAPH-*` / `T-VAULT-DOCGRAPH-*` task files — the pipeline packs.
- `4DLabV2/labs/obdlab/GRAPHIFY_CODE_INGESTION_FORMATTING.md` and `T-KG-OBD-1..3`.
- `planning/{gpf_removal,skill_eval,test_rollout}/*_START_HERE.md`.

## 5. The rule to keep, in one line

> **`graphify` builds the agent's index. Obsidian draws the human's picture.**
> Query the index, don't rebuild it. The Vault never needs a `graph.json`.
