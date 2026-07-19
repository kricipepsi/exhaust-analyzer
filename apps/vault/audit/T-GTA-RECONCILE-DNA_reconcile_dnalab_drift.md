# T-GTA-RECONCILE-DNA — Reconcile dnalab consumer drift (relabel pass)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Owner:** one coder (single mutating task — edits the map; not 3x). Architect may reassign.
**Blocked by:** `T-GTA-UNION-DNA` (done — `reports/dnalab__UNION.md`).
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md`.
### Goal ###
Relabel the **one** drifted `consumers` edge (it appears on **two** notes) in
`vault-map.dnalab.yaml` and the mirror live-note frontmatter, per `reports/dnalab__UNION.md`
rows **N1/N2**. **Relabel-only** — no Python, no new reader, no graph rebuild.
### Why ###
The dnalab union (2/3, code-upheld) found the `schema_version` consumer edge names
`ingestion.py`, which only **defines** the field (a Pydantic field, not a reader). The
MIN_SUPPORTED gate that actually reads it is `lab_pipeline_aggregator.check_schema_version`.
A field definition is not a consumer (signal/noise) -> relabel to the real gate. dnalab feeds
the COMLab prior; the seeded `VehicleDNA` case passed 3/3 and is untouched here.
### Success criteria ###
1. Old edge string gone from the map AND both note frontmatters (grep = 0 each).
2. New edge resolves to a real reader (`check_schema_version` reads `request.metadata.schema_version`).
3. Both notes still carry >=1 LIVE consumer (not orphaned).
4. Map `consumers:` blocks for the two notes are identical to their live-note frontmatter blocks.
5. `git --no-pager diff --stat` shows only the map + the two notes + the ledger.
### Context ###
Map: `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml` (edge at ~lines 53 and 79 —
re-grep before editing). Live notes (mirror frontmatter `consumers:` blocks):
`labs/dnalab/docs/DLD_DNALab.md` and `labs/dnalab/wiki/11_schema_versioning.md`.
**Both copies of each must change together.**
### Consumer (signal/noise) ###
N/A — renames an existing consumer edge to the reader that already exists. No schema surface added.
### Decision — the one edge on two notes (grep-confirm the reader first) ###
| # | note . map line | OLD edge | -> NEW edge | reader to grep-confirm |
|---|---|---|---|---|
| N1 | DLD_DNALab . 53 | `comlab: labs/comlab/comlab/schemas/ingestion.py SessionMetadata.schema_version (MIN_SUPPORTED_SCHEMA_VERSION gate)` | `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py check_schema_version (request.metadata.schema_version vs MIN_SUPPORTED_SCHEMA_VERSION; ERR-ABORT-005)` | `core/lab_pipeline_aggregator.py:231` `MIN_SUPPORTED_SCHEMA_VERSION`; `:233-245` `check_schema_version`; applied `:358`. `ingestion.py:160` only declares the field. |
| N2 | 11_schema_versioning . 79 | (identical OLD edge) | (identical NEW edge as N1) | same as N1 |
### Out of scope ###
- Do **NOT** move/alter the `schema_version` field declaration in `ingestion.py` (it is a
  legitimate schema field; only the *consumer edge label* is wrong).
- Note **bodies**; non-`consumers` frontmatter keys; the seeded `VehicleDNA` edges (LIVE, leave);
  other labs; any Python; `Vault/`.
- GRAPH GUARDRAIL: do **NOT** run `graphify` / rebuild any graph.
- Surgical-change rule: every changed line traces to N1/N2 (+ ledger).
### Files to touch ###
- `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml` (MODIFY — relabel N1, N2)
- `labs/dnalab/docs/DLD_DNALab.md` (MODIFY — mirror N1)
- `labs/dnalab/wiki/11_schema_versioning.md` (MODIFY — mirror N2)
- `apps/vault/audit/GRAPH_TRUST_PROGRESS.md` (MODIFY — flip this row to done)
### Verification ###
```bash
cd /agent_workspace
MAP=_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml
cw(){ awk '/^consumers:/{f=1;next} /^[a-z_]+:/{f=0} f' "$1"; }
# 1. old label gone from map + both notes (each prints nothing):
grep -oE 'ingestion.py SessionMetadata.schema_version' "$MAP"
cw labs/dnalab/docs/DLD_DNALab.md          | grep -oE 'ingestion.py SessionMetadata.schema_version'
cw labs/dnalab/wiki/11_schema_versioning.md| grep -oE 'ingestion.py SessionMetadata.schema_version'
# 2. new reader resolves (>=1):
grep -cE 'def check_schema_version' labs/comlab/comlab/core/lab_pipeline_aggregator.py
# 3. both notes keep >=1 consumer (>=1 each):
cw labs/dnalab/docs/DLD_DNALab.md | grep -cE 'comlab:'; cw labs/dnalab/wiki/11_schema_versioning.md | grep -cE 'comlab:'
# 4. scope:
git --no-pager diff --stat -- "$MAP" labs/dnalab/docs/DLD_DNALab.md labs/dnalab/wiki/11_schema_versioning.md apps/vault/audit/GRAPH_TRUST_PROGRESS.md
```
### Progress hook ###
`GRAPH_TRUST_PROGRESS.md` `T-GTA-RECONCILE-DNA`: Status=done, Files changed=4,
Verification="1 consumer edge relabeled on 2 notes (N1/N2 schema_version -> aggregator check_schema_version); seeded VehicleDNA untouched; map<=>notes agree".
