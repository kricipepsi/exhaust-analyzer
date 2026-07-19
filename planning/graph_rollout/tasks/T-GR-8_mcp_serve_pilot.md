### Goal ###
Pilot graphify's **MCP server mode** (`python -m graphify.serve <graph.json>`) as an OPTIONAL
convenience layer on top of the CLI baseline, and produce a keep/drop recommendation. The CLI
(`query|path|explain|affected --graph …`) remains the sanctioned access path either way — this
pilot must not become a dependency.
### Success criteria ###
1. **Stdio first, no network:** serve `labs/obdlab/graph/v2_current/graph.json` over stdio; list
   the MCP tools exposed; run the same 5 representative lookups via (a) MCP tools and (b) the CLI;
   record side-by-side transcripts + wall time.
2. **Wiring probe (throwaway config, documented not committed):** show how an omp coder profile
   and/or Claude-family session would register the stdio server (config snippet in the report ONLY
   — do not modify shared coder configs in this task).
3. **If (and only if) HTTP is trialled:** bind localhost only, API key set, DNS-rebinding
   protection on (upstream defaults) — no wildcard binds, no exposure. Prefer skipping HTTP
   entirely for the pilot.
4. Report `planning/graph_rollout/REPORT_T-GR-8_mcp_pilot.md`: tool list, transcripts, latency,
   failure modes (server down → CLI fallback), and a recommendation: adopt-for-coders /
   adopt-for-architect-only / drop (CLI sufficient).
### Out of scope ###
No always-on daemon; kill the process at session end. No shared-config edits. No graph builds. No
public binds. No new dependencies beyond `graphifyy[mcp]` extras into `.venv-wired` (record it).
### Verification ###
```bash
cd /agent_workspace
timeout 10 /agent_workspace/.venv-wired/bin/python -m graphify.serve labs/obdlab/graph/v2_current/graph.json --help
ls planning/graph_rollout/REPORT_T-GR-8_mcp_pilot.md
pgrep -f graphify.serve && echo "FAIL: server left running" || echo "OK: no residual process"
```
### Progress hook ###
Ledger T-GR-8 → done + the report's one-line recommendation copied into the ledger row.
### Depends on ###
T-GR-2 done (serve ships with 0.9.x). **Owner go required** (pilot decision, not routine).
