### Goal ###
Close gap G1 of `GRAPH_VIABILITY_ASSESSMENT_2026-07-06.md`: make wiki content queryable and make
graph-CLI queries the canonical lookup path. Two small deliverables, one session.
### Success criteria ###
1. `_skills/graph/4dlab-vault/scripts/vault_query.py` gains:
   - `wiki <lab> <query>` — body search over `labs/<lab>/wiki/**` (mirror `cmd_docs` shape);
   - `grep <lab> <query>` — combined body search over wiki+docs+code with per-hit path + line no;
   - both honour `--json`; `--vault Vault` default unchanged; existing subcommands untouched.
   Acceptance probe: `wiki dtclab "EGR"` MUST return `labs/dtclab/wiki/03_fuel_trim_grammar.md`
   (the Q-C5-EGR miss — this exact lookup failing is why this task exists).
2. Vault health cleanup (assessment G4): add the missing `consumers:` to the 2 flagged task notes
   (T-UI-VAULT, T-UI-VAULT-SUPPORT-1) **in their live source pack, not in `Vault/`**; re-run
   `vault_query.py health` → the consumers FAIL clears (cross-ledger WARNs may remain, list them).
3. Canon wiring: `AGENTS.md` §"Domain facts — wiki-first" gains the two concrete commands:
   `vault_query.py wiki <lab> "<term>"` and
   `graphify query "<question>" --graph labs/<lab>/graph/v2_current/graph.json`
   (also `explain`/`affected`/`path`) — CLI is the sanctioned access path; MCP is a later pilot.
4. Unit probes recorded in the progress note: wiki hit above; `grep comlab "integration_shim"`
   returns ≥1 code hit; `--json` parses.
### Out of scope ###
No graph builds. No `Vault/` edits (health fix lands in the live pack the note mirrors from). No
new dependencies. No MCP. Never `graphify-out/`.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile _skills/graph/4dlab-vault/scripts/vault_query.py
/agent_workspace/.venv-wired/bin/python -m ruff check _skills/graph/4dlab-vault/scripts/vault_query.py
/agent_workspace/.venv-wired/bin/python _skills/graph/4dlab-vault/scripts/vault_query.py --vault Vault wiki dtclab "EGR"
/agent_workspace/.venv-wired/bin/python _skills/graph/4dlab-vault/scripts/vault_query.py --vault Vault health
```
### Progress hook ###
`../GRAPH_ROLLOUT_PROGRESS.md` T-GR-1 → done; progress note in `../progress_notes/T-GR-1.md`
(dual-gate blocks).
### Depends on ###
Nothing. Highest value-per-hour in the pack — run first.
