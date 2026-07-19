# T-GR-2 — progress note
**Task:** graphifyy 0.8.36 → 0.9.7 upgrade + safety verification. **Lane:** ARCHITECT (owner ruling
Q-GRAPH-LANES). **Date:** 2026-07-06 · **Executor:** Architect (Cowork)
## What was done
1. `VIRTUAL_ENV=.venv-wired uv pip install -U 'graphifyy[mcp]==0.9.7'` → `graphify 0.9.7`
   (`[mcp]` extras included for T-GR-8: starlette/uvicorn added).
2. **Scratch smoke-build** (/tmp/gr2_smoke, dnalab code copy): `update` + `cluster-only --no-viz
   --no-label` → 25 nodes / 28 links / **0 dangling** (existing 0.8.x tier: 26/38/0). Link count
   −10 explained: upstream noise suppression — lost edges are stdlib (`datetime→…`) and self-loop
   (`vindna→vindna`) `uses` noise. Node −1 within tolerance.
3. **Schema diff (raw vs old):** top-level `built_at_commit` REMOVED in 0.9.7 output (the
   GRAPH_MANIFEST §3 cheap-check prints it — new builds show blank; staleness now via file mtime
   or GRAPH_REPORT). Node key `community_name` ADDED. Links unchanged. No renames.
4. **Back-compat probes on UNTOUCHED existing graphs** (obdlab v2_current): `query` ✓ (BFS, 106
   nodes, file+line resolution; CLI notes old graphs use pre-#1504 node-ID scheme — informational),
   `explain SensorSignalTranslator` ✓ (file+line), `path` ✓ (1-hop), `affected` ✓ (correct
   ambiguity handling). Old graphs fully readable.
5. **MCP presence:** `python -m graphify.serve --help` ✓ — stdio + http transports, api-key,
   session-timeout flags. T-GR-8 unblocked (presence check only; no server run).
6. **Nothing touched:** sha256 pre/post identical for obdlab v2_current + dnalab v2_code; smoke
   artifacts confined to /tmp.
## Rollback
`VIRTUAL_ENV=.venv-wired uv pip install 'graphifyy==0.8.36'`
## VERIFICATION GATE — T-GR-2
1. Version : PASS (0.9.7)
2. Smoke   : PASS (0 dangling; deltas explained)
3. Compat  : PASS (4 read-only subcommands on existing graphs)
4. Serve   : PASS (--help; not run)
5. Isolation: PASS (hash-verified; /tmp only)
Result: CLEAN
## CODE REVIEW — T-GR-2
Scope: PASS (venv + this note + ledger + SKILL metadata note; no graph, no lab, no Vault).
Composition: PASS (no lab graph rebuilt; graphify-out/ untouched — does not exist on Linux).
Result: CLEAN
