# T-GR-8 — graphify MCP serve pilot (stdio)
**Date:** 2026-07-06 · **Executor:** Architect (Cowork) · **Owner go:** received 2026-07-06.
**Graph under test:** `labs/obdlab/graph/v2_current/graph.json` (1245 nodes / 1664 edges / 103 communities; 91% EXTRACTED).
**Transport:** stdio only. HTTP **not** trialled (kept out per success-criterion 3 — no binds, no exposure).
**Dependency:** `mcp` extra already present in `.venv-wired` from T-GR-2 (`graphifyy[mcp]`); no new install this task.

## 1. Tools the stdio server exposes (10)
`query_graph` (BFS/DFS free-text), `get_node` (node detail by label/ID), `get_neighbors`
(direct edges), `get_community`, `god_nodes` (most-connected), `graph_stats`, `shortest_path`,
plus three GitHub-PR tools: `list_prs`, `get_pr_impact`, `triage_prs`.
Note: MCP tool names differ from CLI subcommands — CLI `query|explain|path|affected`
map to MCP `query_graph | get_node`(+`get_neighbors`)`| shortest_path | get_pr_impact`.

## 2. Five representative lookups — MCP vs CLI (same graph, same host)
| Lookup | MCP tool | MCP ms | CLI ms | Agreement |
|---|---|---:|---:|---|
| L1 free-text "how does o2 normalization work" | query_graph | 31 | 389 | same seed nodes; MCP default depth=3 vs CLI depth=2 |
| L2 node detail "O2FailureMode" | get_node | 4 | 388 | identical (vocabulary.py L90, degree 9) |
| L3 neighbors "O2FailureMode" | get_neighbors | 6 | 383 | same edge set (CLI folds neighbors into `explain`) |
| L4 path O2FailureMode→TrimAnalyticsGate | shortest_path | 8 | 397 | both 2 hops; equivalent route (via _EvidenceTier / MatchType) |
| L5 "OBDLivePayload schema fields" | query_graph | 20 | 408 | identical seeds + context heuristic |

**Latency:** MCP 4–31 ms/call (graph loaded once, stays warm); CLI ~380–410 ms/call (reloads the
1 MB graph.json every invocation — a fixed ~380 ms cold-load tax). MCP is ~10–100× faster per call
for a warm session; the crossover is amortising one load across many queries in a session.

## 3. Wiring probe (throwaway config — documented, NOT committed)
An omp coder profile or a Claude-family session registers the stdio server as (illustrative only):
```jsonc
// mcpServers entry — do NOT commit to shared coder config in this task
{
  "graphify-obdlab": {
    "command": "/agent_workspace/.venv-wired/bin/python",
    "args": ["-m", "graphify.serve", "labs/obdlab/graph/v2_current/graph.json"],
    "cwd": "/agent_workspace"
  }
}
```
One server = one graph (the positional path); a multi-graph setup needs one entry per tier, or the
`project_path` argument that every tool accepts to redirect at call time.

## 4. Failure modes
- **Server down / not started →** CLI is unaffected: `graphify explain … --graph …` needs no server
  and returned correct results with the pilot server killed. CLI remains the always-available baseline.
- **Residual process risk:** stdio server is a child of the client; on a clean client exit it is reaped,
  but a client that errors mid-session can orphan it (observed during the pilot). Mitigation: run under
  `timeout`, and `pkill -9 -f graphify.serve` at session end. Verified 0 residual at pilot close.
- **Stale-graph note:** this graph carries the pre-#1504 node-ID scheme (harmless warning); unrelated to serve.

## 5. Recommendation — **adopt-for-architect-only** (CLI stays the sanctioned baseline)
The warm-session speedup is real and useful for interactive, many-query architect sessions on a single
graph. It is **not** worth making a coder dependency: coders do occasional read-only lookups where the
CLI's ~380 ms cold load is irrelevant, the per-session server lifecycle adds an orphan-process failure
mode, and the golden rule already names the CLI as the baseline. Keep serve as an **optional** architect
convenience (stdio, per-session, killed at end); do **not** wire it into shared coder configs and do
**not** run it as an always-on daemon. HTTP transport stays out until there's a concrete multi-user need.

## VERIFICATION GATE — T-GR-8
1. Stdio serve + tool list : PASS (10 tools enumerated over stdio, no network)
2. 5 lookups MCP vs CLI + timing : PASS (table above; results agree)
3. HTTP : N/A by design (not trialled; no binds)
4. Report written : PASS (this file)
5. No residual process : PASS (`pgrep` clean at close)
Result: CLEAN · Recommendation: adopt-for-architect-only.
