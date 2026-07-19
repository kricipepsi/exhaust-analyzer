### Goal ###
Refresh the **explicitly named** per-lab offline tiers whose source moved since the 06-26/28
builds, so agent queries stop missing recent symbols. Proof of staleness:
`graphify explain "LeanRootCauseState" --graph labs/comlab/graph/v2_current/graph.json` → no node
(state landed in the shim 2026-07-05+). **This task is the sanctioned, task-file-authorized
rebuild** the golden rules require — nothing outside the named list may be rebuilt.
### Named rebuild list (exhaustive — nothing else) ###
- `labs/comlab/graph/v2_code/` and `labs/comlab/graph/v2_tests/` (shim + registry churn: C3B/C6B/C5B)
- `labs/comlab/graph/v2_current/` per the documented compose step for that lab
- ANY other lab ONLY if `git log --since=2026-06-26 -- labs/<lab>/<pkg>` shows code changes — list
  findings in the note first, rebuild only the changed ones.
### Success criteria ###
1. Pre/post node+link counts per rebuilt tier; 0 dangling post; deltas explained (new states,
   deleted code via `--force` only when count-drop is expected and justified).
2. Post-probe: `explain "LeanRootCauseState"` (and `"SensorDynamicsState"`) now resolve to
   `integration_shim.py` with correct line ranges.
3. `GRAPH_AUDIT_2026-06-28.md` inventory appended with dated rebuild rows; pack ledger updated.
4. `graphify-out/`, all docs/wiki tiers, and every unlisted lab graph byte-identical (assert via
   `git status` / checksums recorded pre-run).
### Out of scope ###
Never `graphify-out/`. Never repo root. No docs/wiki tier rebuilds. No LLM. Not before
**T-V3-P4-C5B lands** (otherwise the graph re-stales immediately) — and **owner go required**.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/graphify explain "LeanRootCauseState" --graph labs/comlab/graph/v2_current/graph.json | head
git status --porcelain | grep -E 'graph' | grep -vE 'labs/comlab/graph/(v2_code|v2_tests|v2_current)|planning/graph_rollout/' && echo "FAIL: unlisted graph touched" || echo OK
```
### Progress hook ###
Ledger T-GR-9 → done with pre/post counts and the changed-labs scan result.
### Depends on ###
T-GR-2 done · T-V3-P4-C5B done · **owner go** (explicit rebuild authorization is this task file).
