# T-GTA-RECONCILE-VIN — Reconcile vinlab consumer drift (relabel pass)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Owner:** one coder (single mutating task — edits the map; not 3x). Architect may reassign.
**Blocked by:** `T-GTA-UNION-VIN` (done — `reports/vinlab__UNION.md`).
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md`.
### Goal ###
Relabel the **one** drifted `consumers` edge (it appears on **two** notes) in
`vault-map.vinlab.yaml` and the mirror live-note frontmatter, per `reports/vinlab__UNION.md`
rows **V1/V2**. **Relabel-only** — no Python, no new reader, no graph rebuild.
### Why ###
The vinlab union (3/3) found the `fault_atlas_router.py (FuelSystemStatus.CL, :294)` edge names
an **OBD** read (`_fuel_system_gate` over `obd_live_data.fuel_system_status`), not any vinlab
field — wrong-field reader -> MISLABEL. The router's genuine vinlab read is `vin_confidence`
(`:2239`). vinlab feeds the COMLab prior; this was the subtle VIN map (a 1/3 catch in comlab),
so the edge must point at the real vinlab consumer before wiring.
### Success criteria ###
1. Old edge string gone from the map AND both note frontmatters (grep = 0 each).
2. New edge resolves to a real reader (`vin_confidence` read at `fault_atlas_router.py:2239`).
3. Both notes still carry >=1 LIVE consumer (not orphaned).
4. Map `consumers:` blocks for the two notes are identical to their live-note frontmatter blocks.
5. `git --no-pager diff --stat` shows only the map + the two notes + the ledger.
### Context ###
Map: `_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml` (edge at ~lines 47 and 76 —
re-grep before editing). Live notes (mirror frontmatter `consumers:` blocks):
`labs/vinlab/docs/LLD_VINLab.md` and `labs/vinlab/docs/DLD_VINLab.md`.
**Both copies of each must change together.**
### Consumer (signal/noise) ###
N/A — renames an existing consumer edge to the reader that already exists. No schema surface added.
### Decision — the one edge on two notes (grep-confirm the reader first) ###
| # | note . map line | OLD edge | -> NEW edge | reader to grep-confirm |
|---|---|---|---|---|
| V1 | LLD_VINLab . 47 | `comlab: labs/comlab/comlab/core/fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)` | `comlab: labs/comlab/comlab/core/fault_atlas_router.py vin_confidence (request.metadata.vin_confidence, :2239)` | `core/fault_atlas_router.py:2239` reads `request.metadata.vin_confidence`; `:283-295` `_fuel_system_gate` reads OBD `fuel_system_status`, not vinlab. |
| V2 | DLD_VINLab . 76 | (identical OLD edge) | (identical NEW edge as V1) | same as V1 |
**If a note already carries a `vin_confidence` consumer edge,** drop this one as a duplicate
instead of relabeling (do not leave two identical edges). **Do not** keep it pointed at the
OBD fuel-system gate.
### Out of scope ###
- Do **NOT** touch `_fuel_system_gate` or the `FuelSystemStatus`/`VinConfidence` type defs
  (the double-definition is the expected rule-5 "mirror types over JSON boundaries" pattern).
- Note **bodies**; non-`consumers` frontmatter keys; other labs; any Python; `Vault/`.
- GRAPH GUARDRAIL: do **NOT** run `graphify` / rebuild any graph.
- Surgical-change rule: every changed line traces to V1/V2 (+ ledger).
### Files to touch ###
- `_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml` (MODIFY — relabel V1, V2)
- `labs/vinlab/docs/LLD_VINLab.md` (MODIFY — mirror V1)
- `labs/vinlab/docs/DLD_VINLab.md` (MODIFY — mirror V2)
- `apps/vault/audit/GRAPH_TRUST_PROGRESS.md` (MODIFY — flip this row to done)
### Verification ###
```bash
cd /agent_workspace
MAP=_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml
cw(){ awk '/^consumers:/{f=1;next} /^[a-z_]+:/{f=0} f' "$1"; }
# 1. old label gone from map + both notes (each prints nothing):
grep -oE 'FuelSystemStatus.CL comparison' "$MAP"
cw labs/vinlab/docs/LLD_VINLab.md | grep -oE 'FuelSystemStatus.CL comparison'
cw labs/vinlab/docs/DLD_VINLab.md | grep -oE 'FuelSystemStatus.CL comparison'
# 2. new reader resolves (>=1):
grep -cE 'request.metadata.vin_confidence' labs/comlab/comlab/core/fault_atlas_router.py
# 3. both notes keep >=1 consumer (>=1 each):
cw labs/vinlab/docs/LLD_VINLab.md | grep -cE 'comlab:'; cw labs/vinlab/docs/DLD_VINLab.md | grep -cE 'comlab:'
# 4. scope:
git --no-pager diff --stat -- "$MAP" labs/vinlab/docs/LLD_VINLab.md labs/vinlab/docs/DLD_VINLab.md apps/vault/audit/GRAPH_TRUST_PROGRESS.md
```
### Progress hook ###
`GRAPH_TRUST_PROGRESS.md` `T-GTA-RECONCILE-VIN`: Status=done, Files changed=4,
Verification="1 consumer edge relabeled on 2 notes (V1/V2 FuelSystemStatus OBD gate -> vin_confidence :2239); map<=>notes agree; 0 orphaned".
