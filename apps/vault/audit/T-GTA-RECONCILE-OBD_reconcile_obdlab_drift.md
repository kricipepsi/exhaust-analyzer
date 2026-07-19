# T-GTA-RECONCILE-OBD — Reconcile obdlab consumer drift (relabel pass)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Owner:** one coder (single mutating task — edits the map; not 3x, to avoid an edit race). Architect may reassign.
**Blocked by:** `T-GTA-UNION-OBD` (done — `reports/obdlab__UNION.md`).
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md`.
### Goal ###
Relabel the **six** drifted `consumers` edges (across **four** wiki README notes) in
`vault-map.obdlab.yaml` and their live-note frontmatter mirrors, per `reports/obdlab__UNION.md`
rows **D1-D6**. **Relabel-only** — no Python, no new reader, no graph rebuild.
### Why ###
The obdlab union ruled all six MISLABEL after code-verify: two `delta-relations` edges name
`power_loss_analytics.py` / `perception_contradiction.py` but the cross-operating-point delta
reader is `delta_engine.py`; two `fault_atlas_kg.py` edges name a generic boot-time KG loader
that reads no PID/Mode06/era field (the real readers are in `fault_atlas_router.py`); two
`symptom_router.py` edges name a router that reads only `engine_state`/`occurs_during`. obdlab
is an emitter map `T-WIRE-1` composes against, so its edges must be trustworthy before wiring.
### Success criteria ###
1. None of the six old edge strings survive in the map or the four note frontmatters (grep = 0 each).
2. Each relabeled edge resolves to a real reader (grep confirms the new `file:symbol/field`).
3. Every affected note still carries >=1 LIVE consumer (none orphaned; e.g. truth-perception
   keeps its LIVE `perception_contradiction.py — truth-vs-perception override core` edge).
4. Map `consumers:` blocks for the four notes are identical to their live-note frontmatter blocks.
5. `git --no-pager diff --stat` shows only the map + the four notes + the ledger.
### Context ###
Map: `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml` (edges at ~lines 106,107,127,138,139,150
— re-grep before editing). Live notes (mirror frontmatter `consumers:` blocks):
`labs/obdlab/research/chunks/{delta-relations,pids-protocol,taxonomy,truth-perception}/README.md`.
**Both copies of each edge must change together.**
### Consumer (signal/noise) ###
N/A — renames existing consumer edges to readers that already exist in code (verified in the union).
### Decision — per-edge disposition (grep-confirm each reader before writing) ###
| # | note . map line | OLD edge | -> NEW edge | reader to grep-confirm |
|---|---|---|---|---|
| D1 | delta-relations . 106 | `comlab: ...analytics/power_loss_analytics.py — lambda-delta-vector scoring` | `comlab: labs/comlab/comlab/analytics/delta_engine.py (two-operating-point DeltaSignature)` | `analytics/delta_engine.py:1-22` docstring names `delta-relations/*` as its source; differences `second_operating_point`. |
| D2 | delta-relations . 107 | `comlab: ...core/perception_contradiction.py` | `comlab: labs/comlab/comlab/analytics/delta_engine.py (two-operating-point DeltaSignature)` | `grep -E 'second_operating_point|delta' core/perception_contradiction.py` = 0; reader is `delta_engine.py`. |
| D3 | pids-protocol . 127 | `comlab: ...core/fault_atlas_kg.py — PID/Mode06/readiness fault-atlas keys` | `comlab: labs/comlab/comlab/core/fault_atlas_router.py (mode_06_monitors / Mode06MonitorState)` | `core/fault_atlas_router.py:455` `mode_06_monitors`; `:471-475` `Mode06MonitorState`. `fault_atlas_kg.py` = generic loader (grep PID/Mode06 = 0). |
| D4 | taxonomy . 138 | `comlab: ...core/symptom_router.py — era/emission symptom-prior routing` | `comlab: labs/comlab/comlab/core/horizon_context_injector.py + core/fault_atlas_router.py (era/horizon-mask checks)` | `fault_atlas_router.py:95` `# wiki: 04_horizon_eras.md`; target-horizon filtering. `symptom_router.py` routes only `engine_state`/`occurs_during` (:60-61). |
| D5 | taxonomy . 139 | `comlab: ...core/fault_atlas_kg.py` | `comlab: labs/comlab/comlab/core/fault_atlas_router.py (era/horizon-mask checks) + core/horizon_context_injector.py` | same loader fact as D3; era checks live in the router/injector (grep era/horizon `fault_atlas_kg.py` = 0). |
| D6 | truth-perception . 150 | `comlab: ...core/symptom_router.py — symptom prior` | `comlab: labs/comlab/comlab/core/fault_atlas_router.py RULE_SYMPTOM_PRIOR (capped 0.65)` | `fault_atlas_router.py:600-602` `_max_symptom_prior_weight=0.65`; applied `:1078-1090`. `grep prior core/symptom_router.py` = 0. (Same reader the comlab union D5 located.) |
Rule for every row (`4dlab-doc-prep` Step 4/5, signal/noise): **grep-confirm the read exists
before writing the new edge.** After the six relabels, re-check each of the four notes keeps
>=1 LIVE consumer; if any edit would leave a note with zero, STOP and surface it.
### Out of scope ###
- Do **NOT** add any reader. The union ruled all six MISLABEL — relabel to the existing reader,
  do not build code.
- Note **bodies**; non-`consumers` frontmatter keys; the LIVE truth-perception
  `perception_contradiction.py` override edge (leave); other labs; any Python; `Vault/`.
- GRAPH GUARDRAIL: do **NOT** run `graphify` / rebuild any graph.
- Surgical-change rule: every changed line traces to a D1-D6 row (+ ledger). No adjacent cleanup.
### Files to touch ###
- `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml` (MODIFY — the 6 edges)
- `labs/obdlab/research/chunks/delta-relations/README.md` (MODIFY — mirror D1, D2)
- `labs/obdlab/research/chunks/pids-protocol/README.md` (MODIFY — mirror D3)
- `labs/obdlab/research/chunks/taxonomy/README.md` (MODIFY — mirror D4, D5)
- `labs/obdlab/research/chunks/truth-perception/README.md` (MODIFY — mirror D6)
- `apps/vault/audit/GRAPH_TRUST_PROGRESS.md` (MODIFY — flip this row to done)
### Verification ###
```bash
cd /agent_workspace
MAP=_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml
C=labs/obdlab/research/chunks
cw(){ awk '/^consumers:/{f=1;next} /^[a-z_]+:/{f=0} f' "$1"; }
# 1. old labels gone from map (each prints nothing):
for s in 'power_loss_analytics.py — lambda-delta-vector' 'perception_contradiction.py$' \
         'fault_atlas_kg.py — PID/Mode06' 'symptom_router.py — era/emission' \
         'fault_atlas_kg.py$' 'symptom_router.py — symptom prior'; do grep -oE "$s" "$MAP"; done
# 2. new readers resolve (each >=1):
grep -cE 'delta-relations' labs/comlab/comlab/analytics/delta_engine.py            # D1/D2
grep -cE 'mode_06_monitors' labs/comlab/comlab/core/fault_atlas_router.py          # D3
grep -cE '04_horizon_eras|target_horizon|horizon' labs/comlab/comlab/core/fault_atlas_router.py  # D4/D5
grep -cE '_max_symptom_prior_weight' labs/comlab/comlab/core/fault_atlas_router.py # D6
# 3. each note keeps >=1 consumer (>=1 each):
for n in delta-relations pids-protocol taxonomy truth-perception; do cw "$C/$n/README.md" | grep -cE 'comlab:'; done
# 4. scope:
git --no-pager diff --stat -- "$MAP" "$C"/*/README.md apps/vault/audit/GRAPH_TRUST_PROGRESS.md
```
### Progress hook ###
`GRAPH_TRUST_PROGRESS.md` `T-GTA-RECONCILE-OBD`: Status=done, Files changed=6,
Verification="6 consumer edges relabeled (D1-D6): delta-relations x2 -> delta_engine; fault_atlas_kg x2 -> fault_atlas_router; symptom_router x2 -> router (era/injector + capped prior); map<=>4 notes agree; 0 orphaned".
