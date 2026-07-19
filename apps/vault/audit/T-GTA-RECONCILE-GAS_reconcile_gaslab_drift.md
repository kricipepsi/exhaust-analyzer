# T-GTA-RECONCILE-GAS — Reconcile gaslab consumer drift (demote pass)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Owner:** one coder (single mutating task — edits the map; not 3x, to avoid an edit race). Architect may reassign.
**Blocked by:** `T-GTA-UNION-GAS` (done — `reports/gaslab__UNION.md`).
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md`.
### Goal ###
Remove the **one** ORPHAN `consumers` edge in `vault-map.gaslab.yaml` (and its mirror in the
live-note frontmatter) per `reports/gaslab__UNION.md` row **G1**. **Demote-only** — no Python,
no new reader, no graph rebuild. Done when the edge is gone from both copies and note 10 still
carries >=1 LIVE consumer.
### Why ###
The gaslab union (3/3) found note 10's `lab_pipeline_aggregator.py chemistry confidence input`
has **no COMLab reader at all**: the aggregator derives confidence only from horizon/VIN/override
and `GasLabPayload` has no confidence field. It is a true ORPHAN, not a wrong-file MISLABEL —
so the fix is to **remove** the edge, not relabel it. gaslab is an emitter map `T-WIRE-1`
composes against; a lying edge must not survive into wiring.
### Success criteria ###
1. The old edge string is gone from the map AND the note-10 frontmatter (grep = 0 in both).
2. Note 10 still carries >=1 LIVE consumer (its gaslab self-consumers + other comlab
   `sample_validity`/`lambda` edges remain — confirm, do not orphan the note).
3. Map `consumers:` block for note 10 is identical to the live-note frontmatter block.
4. `git --no-pager diff --stat` shows only the map + the one note + the ledger.
### Context ###
Map: `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml` (edge at ~line 264 —
re-grep before editing; line numbers drift). Live note (mirror):
`labs/gaslab/wiki/10_limited_scope_confidence.md` (frontmatter `consumers:` block, ~line 23).
**Both copies must change together** — the eval reads the live note, the wiring reads the map.
### Consumer (signal/noise) ###
N/A — removes a consumer with no code reader. Adds no schema surface.
### Decision — the one edge (grep-confirm absence of a reader first) ###
| # | note . map line | edge to REMOVE | why (from union) |
|---|---|---|---|
| G1 | 10_limited_scope_confidence . 264 | `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py chemistry confidence input` | `grep -niE 'confidence' lab_pipeline_aggregator.py | grep -iE 'gas|chem'` -> only a docstring (:324); `GasLabPayload` (`schemas/ingestion.py:165-205`) has no confidence field. No reader -> ORPHAN -> remove. |
**Alternative (only if owner prefers):** repoint to the gaslab-internal ceiling
`labs/gaslab/gaslab/ranking.py _clamped_confidence`. Default is **remove** — note 10 already
frames that gaslab self-consumer separately, so the comlab edge is a wrong-lab duplicate.
### Out of scope ###
- Do **NOT** implement a COMLab chemistry-confidence reader (that is a future proposal with
  its own spec + named consumer, per AGENTS.md rule 4 — not this map pass).
- Note **body**; any non-`consumers` frontmatter key; other labs; any Python; `Vault/`.
- GRAPH GUARDRAIL: do **NOT** run `graphify` / rebuild any graph. This is a text edit.
- Surgical-change rule: the only changed lines are G1's removal in the two files (+ ledger).
### Files to touch ###
- `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml` (MODIFY — remove G1)
- `labs/gaslab/wiki/10_limited_scope_confidence.md` (MODIFY — mirror removal in frontmatter)
- `apps/vault/audit/GRAPH_TRUST_PROGRESS.md` (MODIFY — flip this row to done)
### Verification ###
```bash
cd /agent_workspace
MAP=_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml
N=labs/gaslab/wiki/10_limited_scope_confidence.md
cw(){ awk '/^consumers:/{f=1;next} /^[a-z_]+:/{f=0} f' "$1"; }
# 1. old edge gone from BOTH (each prints nothing):
grep -oE 'lab_pipeline_aggregator.py chemistry confidence input' "$MAP"
cw "$N" | grep -oE 'lab_pipeline_aggregator.py chemistry confidence input'
# 2. note 10 still has >=1 comlab/gaslab consumer (>=1):
cw "$N" | grep -cE 'comlab:|gaslab:'
# 3. scope:
git --no-pager diff --stat -- "$MAP" "$N" apps/vault/audit/GRAPH_TRUST_PROGRESS.md
```
Step 1 prints nothing (both); step 2 prints >=1; step 3 shows only the three files.
### Progress hook ###
`GRAPH_TRUST_PROGRESS.md` `T-GTA-RECONCILE-GAS`: Status=done, Files changed=3,
Verification="1 ORPHAN consumer edge removed (G1 chemistry-confidence input); note 10 retains LIVE consumers; map<=>wiki agree".
