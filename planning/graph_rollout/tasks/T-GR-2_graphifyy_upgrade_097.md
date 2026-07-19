### Goal ###
Upgrade `graphifyy` 0.8.36 → 0.9.7 in `.venv-wired` and prove it SAFE for this repo: new builds
work offline, old graphs still readable, `serve` (MCP) present. **No existing graph is rebuilt.**
### Success criteria ###
1. `graphify --version` → 0.9.7 (install via `uv pip install -U 'graphifyy==0.9.7'` into
   `.venv-wired`; record exact command).
2. **Scratch smoke-build:** copy ONE small already-graphed corpus (e.g. `labs/dnalab` code dir) to
   `/tmp/gr2_smoke/`, run `graphify update /tmp/gr2_smoke`, relocate per `4dlab-graphify-run`;
   health: 0 dangling; node/edge counts within ±10% of the existing dnalab v2_code graph; note any
   `graph.json` schema field diffs (new keys OK; renamed/removed keys = STOP and surface).
3. **Back-compat probes on UNTOUCHED existing graphs:** `explain`, `query`, `path`, `affected`
   each run against `labs/obdlab/graph/v2_current/graph.json` and return sane output (record one
   transcript each).
4. **MCP presence check only:** `python -m graphify.serve --help` (or documented equivalent)
   exists and prints usage. Do NOT stand up a server (that is T-GR-8).
5. Rollback line recorded: `uv pip install 'graphifyy==0.8.36'` restores; note stays in the ledger.
### Out of scope ###
No rebuild of ANY graph under `labs/` or `graphify-out/` (the smoke corpus lives in /tmp only). No
LLM/`extract`. No MCP server process. No skill edits beyond noting the verified version in
`_skills/graph/4dlab-graphify-run/SKILL.md` metadata.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/graphify --version
/agent_workspace/.venv-wired/bin/graphify explain "delta_engine" --graph labs/obdlab/graph/v2_current/graph.json | head
ls /tmp/gr2_smoke/graphify-out/ 2>/dev/null || true   # smoke artifacts in /tmp only
git status --porcelain | grep -E 'labs/.*/graph/' && echo "FAIL: lab graph touched" || echo "OK: no lab graph touched"
```
### Progress hook ###
Ledger T-GR-2 → done with version, schema-diff note, and back-compat transcripts.
### Depends on ###
Nothing hard (T-GR-1 can run before or after). **Unblocks T-GR-3…8** — new tiers build on 0.9.7.
