# GRAPH MANIFEST — 4DLabV2

**Read this before any task that touches "the graph," and any time graphify is tempting.**
Authored 2026-06-12 from a full scan of `4DLabV2` + `Vault`. Companion to
`AGENTS.md` rule #1 and `docs/Brain/GRAPH_VS_GRAPHIFY_SETTLED.md`.
> **[2026-06-28] The inventory in S2/S4 below is a stale 06-12 Windows scan. See
> `GRAPH_AUDIT_2026-06-28.md` for the live state, and `GRAPH_VIABILITY_ASSESSMENT_2026-07-06.md`
> for the current gap list + recommended task sequence (wiki-query gap G1 first). Also: the root `graphify-out/graph.json`
> called 'FROZEN/canonical' here is NOT present in the Linux workspace.**


---

## 0. The one distinction that ends the confusion

- **graphify `graph.json`** = a machine index agents *query* to find a symbol's file/line.
  Built by the `graphify` tool — **offline & free** for code/tests/docs (`graphify update`); token-spending **only** for the wiki LLM tier.
- **Obsidian graph** = the live picture Obsidian draws from `[[wikilinks]]`. Not a file,
  not built — drawn on open. Nobody needs to produce or store it.

**The Vault is agent-facing** (a navigable window onto finished labs, queried via
`_skills/graph/4dlab-vault/` → `scripts/vault_query.py`). It deliberately holds **no
`graph.json`**: it references each lab's canonical graph *by path* (`_meta/PROVENANCE.md`:
"required, not copied"). Do not copy a graph into the Vault.

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

## 1. Golden rules (load-bearing)

1. **Query, don't rebuild.** Agents read existing `graph.json`; they re-run graphify
   **only** when a task file explicitly says so.
2. **The root graph is FROZEN.** `graphify-out/graph.json` (~43k nodes, whole repo) is
   canonical. Never regenerate it except on explicit owner instruction.
3. **Querying ≠ graphifying.** "Query the graph before you grep" means *open the file*,
   not *build it*. This sentence is the #1 source of wasted runs.
4. **Nothing ships without a named consumer** (signal/noise) — applies to graph edges and
   Vault frontmatter too.

## 2. Canonical graph inventory (scan of 2026-06-12)

Per-lab graphs live at `labs/<lab>/graph/<tier>/graph.json`. `v2_current` is the
agent-query graph; `v2_code` / `v2_tests` / `v2_wiki` / `v2_docs` are the build tiers.

| Graph | nodes | links | dangling | isolated | built | status |
|---|--:|--:|--:|--:|---|---|
| **graphify-out/** (root, whole repo) | 43037 | 55709 | 0 | 206 | 06-11 | canonical · **FROZEN** |
| gaslab v2_current | 1345 | 1774 | 0 | 5 | 06-06 | query graph |
| gaslab v2_code | 237 | 407 | 0 | 0 | 06-10 | tier ✓ |
| gaslab v2_tests | 494 | 723 | 0 | 0 | 06-10 | tier ✓ (wiki/docs waived) |
| obdlab v2_current | 1245 | 1664 | 0 | 12 | 06-06 | query graph |
| obdlab v2_code / v2_tests / v2_wiki / v2_docs | 188 / 878 / 451 / 480 | — | 0 | low | 06-08…06-10 | **all 4 tiers ✓** (most complete) |
| dtclab v2_current | 1072 | 1540 | 0 | 11 | 06-06 | query graph |
| dtclab v2_code / v2_tests | 186 / 699 | — | 0 | 0 | 06-11 | tiers ✓ (docs tier not built) |
| comlab v2_current | 3090 | 4139 | 0 | 20 | 06-06 | query graph · **no code/tests tier** |
| dnalab v2_current | 100 | 127 | 0 | 2 | 06-06 | query graph · **no code/tests tier** |
| vinlab v2_current | 1364 | 1723 | 0 | 16 | 06-06 | query graph · **no code/tests tier** |
| symptomlab v2_current | 101 | 180 | 0 | 2 | 06-06 | query graph · **no code/tests tier** |

`v1_baseline` graphs exist for every lab — they are pre-rework snapshots, kept for
DIFF_REPORT comparison only. Do not query them for current truth.

## 3. Consistency check — cheap, read-only, no re-extraction

You do **not** rebuild a graph to check it. Open the JSON and read four numbers. Costs
seconds and zero tokens. This is the whole technique:

```python
import json
d = json.load(open("labs/<lab>/graph/v2_current/graph.json"))
nodes, links = d["nodes"], d["links"]
ids = {n["id"] for n in nodes}
dangling = sum(1 for l in links if l["source"] not in ids or l["target"] not in ids)
deg = {}
for l in links:
    deg[l["source"]] = deg.get(l["source"], 0) + 1
    deg[l["target"]] = deg.get(l["target"], 0) + 1
isolated = sum(1 for n in nodes if deg.get(n["id"], 0) == 0)
print(len(nodes), "nodes", len(links), "links",
      dangling, "dangling", isolated, "isolated",
      d.get("built_at_commit", "")[:8], "commit")
```

How to read the result:

- **dangling > 0 → HARD fail.** An edge points at a node that doesn't exist; the graph is
  corrupt. (Scan result: **0 everywhere** — all graphs are structurally sound.)
- **isolated nodes → SOFT signal.** A few are normal (an unreferenced symbol). A spike means
  the ingestion missed links — worth a look, not an alarm.
- **`built_at_commit` / build date → STALENESS signal.** If it predates recent code changes,
  the graph is out of date and a query may point you at moved code.

The same check is built into `4dlab-graphify-run` as its health pass
(`eval-*-graph --health-only`) — use that when a task already loaded the skill.

## 4. What the check found on 2026-06-12 (act on this, don't re-graphify blindly)

- **Structure is clean** — 0 dangling edges across all 24 graphs. No corruption.
- **The query graphs are the oldest.** Every `v2_current` was built **06-06 at commit
  `f7544224`**, while the build tiers and the root graph moved on to 06-09…06-11. So the
  graph agents are told to query is the *stalest* of the v2 set. If code changed after
  06-06, trust the file but verify a moved symbol by opening it.
- **Four labs have no code/tests tier graphs:** `comlab`, `dnalab`, `vinlab`, `symptomlab`
  only have `v1_baseline` + `v2_current`. These are the real "must be graphed" gaps — and
  each needs a task spec before any graphify run (one task per session).

## 5. Before-a-task checklist (paste into your head)

```
1. Need to look up a symbol?      → QUERY labs/<lab>/graph/v2_current/graph.json
                                     (or the Vault via vault_query.py). Do NOT build.
2. Graph looks wrong / old?       → run the §3 cheap check. dangling>0 = corrupt;
                                     stale commit = note it, don't auto-rebuild.
3. Task literally says "graphify" → only then run 4dlab-graphify-run, into the
                                     named tier dir. Never touch graphify-out/.
4. Tempted to add a graph to the  → STOP. Vault references graphs by path; Obsidian
   Vault?                           draws its own. Nothing to add.
```

> **graphify builds the agent's index; Obsidian draws the human's picture.**
> **Query the index, don't rebuild it. The Vault never needs a `graph.json`.**
