# GRAPH AUDIT — 2026-06-28 (graphify output vs LLM graph)
Supersedes the inventory in `docs/Brain/GRAPH_VS_GRAPHIFY_SETTLED.md` and `GRAPH_MANIFEST.md` (both a 2026-06-12
Windows scan). Authored from a live scan of `/agent_workspace` on Linux.

## Why this audit exists
A coder stalled on `T-RVAULT-4` hunting for an API key on an **offline AST** task. Root cause: the
docs and the `4dlab-graphify-run` skill conflated "run graphify" with "run an LLM." They don't mean
the same thing. This audit sets the strict nomenclature and records the current state.

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


## Live inventory (2026-06-28) — what actually exists on disk
Every lab now has the offline tiers built (the 06-12 docs claimed four labs had none):

| lab | offline tiers (free) | LLM tier | notes |
|---|---|---|---|
| obdlab | v2_code, v2_tests, v2_docs | **v2_wiki** (+v2_docs_llm cross-check) | most complete |
| symptomlab | v2_code, v2_tests, v2_docs | v2_wiki | docs/wiki mostly EXTRACTED |
| comlab | v2_code, v2_tests | — | docs/wiki waived (T-COM-GRAPH-LLM) |
| comlab/registry | v2_code, v2_tests, v2_docs | — | docs built **offline**, EXTRACTED-only, GOOD |
| comlab (main) | v2_code, v2_tests, **v2_docs** | — | v2_docs built **offline** 2026-07-06 (T-GR-7): 445n/365e, 0 dangling, 0 isolated, 100% EXTRACTED/0 INFERRED, edges all `contains`; architectural-predicate layer pending future LLM `extract` (out of scope for this pack) |
| dnalab | v2_code, v2_tests, **v2_docs** | — | v2_docs built **offline** 2026-07-06 (T-GR-6): 215n/164e, 0 dangling, 0 isolated, 100% EXTRACTED/0 INFERRED, edges all `contains`; architectural-predicate layer pending future LLM `extract` (out of scope for this pack); prose Pass-3 waived by owner |
| vinlab | v2_code, v2_tests, **v2_docs** | — | v2_docs built **offline** 2026-07-06 (T-GR-5): 396n/328e, 0 dangling, 0 isolated, 100% EXTRACTED/0 INFERRED, edges all `contains`; architectural-predicate layer pending future LLM `extract` (out of scope for this pack) |
| dtclab | v2_code, v2_tests, **v2_docs** | — | v2_docs built **offline** 2026-07-06 (T-GR-4): 375n/300e, 0 dangling, 0 isolated, 100% EXTRACTED/0 INFERRED, edges all `contains`; architectural-predicate layer pending future LLM `extract` (out of scope for this pack) |
| gaslab | v2_code, v2_tests, **v2_docs** | — | v2_docs built **offline** 2026-07-06 (T-GR-3): 344n/273e, 0 dangling, 0 isolated, 100% EXTRACTED/0 INFERRED, edges all `contains`; architectural-predicate layer pending future LLM `extract` (out of scope for this pack) |

**Refresh 2026-07-06 (T-GR-9, post-C5B staleness):** rebuilt offline (`graphify update`, scoped /tmp):
comlab `v2_code` 1611n/3107e · `v2_tests` 1713n/2419e · `v2_current` 3972n/7911e (fresh compose;
old had stale `C:\` paths + pre-#1504 ID scheme) · registry `v2_code` 220n/419e (now indexes
`LeanRootCauseState`/`SensorDynamicsState`, shim L178/L170) · registry `v2_tests` 824n/1258e ·
obdlab `v2_tests` 878n/1196e. All 0 dangling. **Tool caveat: built with pinned graphifyy 0.8.36 —
0.9.7 extracts zero nodes from JSON files (upstream #1666); do NOT rebuild JSON-bearing corpora on
0.9.7.** Details: planning/graph_rollout/progress_notes/T-GR-9.md.

All graphs: 0 dangling edges. `v2_current` per lab remains the agent-query graph; `v1_baseline` is a
pre-rework snapshot (diff only).

**Migration note:** the root `graphify-out/graph.json` that `GRAPH_MANIFEST.md` calls the "canonical
FROZEN ~43k-node" artifact is **not present** in the Linux workspace. Rules pointing at it are moot.

## Is T-COM-GRAPH-LLM (comlab wiki+docs prose graphs) worth implementing? — NO, keep waived
- **Feasible, not blocked.** obdlab + symptomlab proved the Pass-3 pipeline. The waiver is a
  cost/dependency decision, not infeasibility.
- **The vault doesn't need it.** `build_lab_vault.py` requires only `v2_code` + `v2_tests` for comlab
  (both built, GOOD). `Vault/_meta/PROVENANCE.md` records comlab wiki/docs as waived.
- **Prep already did the work.** `T-COM-WIKIPREP` and `T-COM-DOCPREP` are `done`, so the relations a
  prose graph would infer are already explicit in the prose; frontmatter consumers are
  architect-named, not graph-derived.
- **Low marginal value, real cost.** The LLM layer adds ~0 edges to docs and ~17% to wiki, against
  token cost + the external-backend dependency that caused the stall.
- **If you ever want comlab docs coverage:** build `v2_docs` **offline** (like registry did) — zero
  tokens, no backend. Only lift the full LLM task for the semantic *wiki* layer specifically.

## LLM Pass-3 prose graphs across ALL labs — not worth implementing (evidence)
The question "should we build the LLM prose graphs for every lab?" is settled by the architecture and by
the one real run.

**By design, the LLM graph can never be a deliverable.** `_skills/graph/eval/PASS3_EVAL_PROTOCOL.md`:
the deterministic (offline) graph is canonical truth, and Pass-3 is run **as a checker, not an adder** —
*"nothing is promoted into a canonical graph."* A confirmed gap is fixed at source and re-derived offline,
never patched in from the LLM graph. So the LLM tier can only *audit*, never *improve*, a graph.

**The one real run found nothing.** `T-VAULT-DOCGRAPH-2` (obdlab docs, 2026-06-10,
`graph/v2_docs/PASS3_CROSSCHECK.md`):

- **Verdict: 0 real GAPs.** 84 LLM edges vs the deterministic 1045 — all 84 noise (75 invented-node, 3
  INFERRED, 6 generic-vocab edges already present in baseline).
- Vocabulary divergence: the LLM emits `references`/`implements`; the baseline uses the controlled set
  (`CONSUMES`/`GATED_BY`/`ROUTES_TO`/…). 0 relation overlap; only 24 of 111 LLM node-ids existed in the
  480-id baseline — so no LLM edge could even line up (tuple-match) with a baseline edge.
- Cost: ~$0.024 + 22 min wall, and it failed to parse 38 of 68 chunks (a sparse, conservative probe that
  *can't* prove completeness anyway — completeness comes from the offline 100%-EXTRACTED build).

**The real bottleneck is consumers, not coverage.** Architect handoff (`labs/obdlab/graph/
HANDOFF_graph_saga_2026-06-10.md`): *"the edges are built but nothing reads them yet… wire a consumer,
then let Pass 3 verify,"* with an explicit *"recommend HOLDING [DOCGRAPH-2] until consumer wiring exists."*

**The tooling is not the gap.** The skill A/B benchmark (`_skills/graph/skilltest-out/iteration-2`):
with-skill 100% vs without-skill 61%. The prep/run skills work — waiving the LLM tasks is a value
decision, not a tooling shortfall.

### Standing decision (all labs)
- **Per-lab prose-graph tasks stay waived/void:** `T-GAS-GRAPH-LLM` (void), `T-COM-GRAPH-LLM` (waived);
  DTC/VIN/DNA waived in `Vault/_meta/PROVENANCE.md`. Do not lift.
- **Vault cross-check tier stays the OBDLab pilot only:** `DOCGRAPH-1` (offline docs build) = the real
  deliverable, `done`. `DOCGRAPH-2` (LLM doc cross-check) = `done`, **0 gaps**. `WIKIGRAPH-1` /
  `CODEGRAPH-1` = held — each would *re-extract a canonical graph* (hard rule) for a checker the docs run
  already showed yields nothing; code-tier is the worst case (AST is already truth, ~50% INFERRED noise).
- **Only-ever trigger for a single Pass-3 run:** after a lab's edges gain a *named consumer* AND a specific
  diagnostic edge is suspected missing — run docs-tier only, expect ~nothing, promote nothing.

## Files updated in this pass (2026-06-28)
- `docs/Brain/GRAPH_VS_GRAPHIFY_SETTLED.md` — added offline-vs-LLM canon; fixed "costs tokens" cell; staleness banner.
- `GRAPH_MANIFEST.md` — added canon; staleness + missing-root-graph banner.
- `_skills/graph/4dlab-graphify-run/SKILL.md` — code branch uses `graphify update`; docs branch marked offline-capable.
- `_skills/graph/4dlab-doc-prep/SKILL.md` — docs extract offline (EXTRACTED) after prep; LLM optional.
- `AGENTS.md`, `CLAUDE.md`, `4DLab_CLAUDE.md` — one-line graphify!=LLM nomenclature pointer.
- `labs/comlab/registry/docs/registry_tasks/T-RVAULT-4_graph_ast_build.md` — offline/no-key recipe (earlier).
- `Vault/tasks/T-VAULT-DOCGRAPH-2_pass3_llm_crosscheck.md` — status `pending` -> `done` (0 gaps; deliverable already existed).
