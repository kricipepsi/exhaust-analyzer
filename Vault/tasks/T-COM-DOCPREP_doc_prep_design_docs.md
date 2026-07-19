---
node_type: task
task_id: T-COM-DOCPREP
status: done
pack: VAULT
lab: comlab
mode: architect/author lane
blocked_by:
- T-COM-DOCS-V2
consumers:
- graph/v2_docs — docs graph (frontmatter source; prose graph waived this pack)
- COMLab analytics / fault-atlas routing
- apps/4DLabWired (LabPipelineAggregator consumer)
tags:
- task
- vault
- comlab
---

# T-COM-DOCPREP — Doc-prep the six v2 design docs (`4dlab-doc-prep`)

**Status:** `done` · **Pack:** VAULT (COMLab) · **Mode:** architect/author lane (graph-tooling; no lab inner-loop)
**Origin:** pipeline guide §4 (doc prep) · **Blocked by:** T-COM-DOCS-V2
**Load skills:** `comlab-verification-loop`, **`4dlab-doc-prep`**, **`comlab-vault-prep`**.
**Consumer (signal/noise):** **Adds no schema field.** Splits the monolithic design docs into ingest-ready,
header-anchored blocks with explicit architectural-relation lines, so the docs-tier vault copy's
`implements`/`consumers` frontmatter derives from named consumers (COMLab-internal + the `apps/4DLabWired`
reader). Every `CONSUMES`/`VERIFIES` names a real path/test. No new fields.

### Role note ###

`4dlab-doc-prep` runs `explode → tables → anchor → relations → verify`, writing
`graph/v2_docs/ingest_ready/<doc>/…`. It does **not** write `graph.json` / run graphify. (The docs prose
graph is **waived** this pack — START_HERE §1 — but the prep output still feeds the vault docs frontmatter,
so the prep runs.) `comlab-vault-prep` Rule 3 is the authoritative exclusion file-list.

### Ingest the SIX design docs by explicit file list (never a glob) ###

```
labs/comlab/docs/COMLab_HLD.md
labs/comlab/docs/COMLab_DLD.md
labs/comlab/docs/COMLab_LLD.md
labs/comlab/docs/COMLab_BDD.md
labs/comlab/docs/COMLab_PRD.md
labs/comlab/docs/adr/ADR-0001_*.md … ADR-0011_*.md   ← the 11 ADR records (the "ADR" tier)
```

**Exclude** (per `comlab-vault-prep` Rule 3 / OBDLab exclusion discipline):

- `docs/Vocabulary/{DTC_VOCABULARY,OBD_VOCABULARY,SEMANTIC_CONTRACT}.md` — vocabulary surface → the shared
  `Vault/_vocabulary/` tier (handled in `T-COM-VAULT` step 0). DTC/OBD vocab already have `_vocabulary`
  homes from their packs; COMLab's copies are mirrors.
- `docs/CROSS_LAB_DEPENDENCIES.md` — cross-lab forward registry, not a COMLab design doc.
- `docs/ARCHIVE/` — superseded v1.0 drafts.
- `docs/adr/README.md` — the ADR index, not a record.

### Architectural-relation discipline ###

- Anchor each doc to its lineage (`HLD ← PRD`, `DLD ← HLD`, `LLD ← DLD/HLD`, the ADRs ← the decisions they
  formalise — the docs already carry these baselines in their headers).
- Emit `IMPLEMENTS` / `CONSUMES` / `VERIFIES` lines naming real symbols: the COMLab modules
  (`fault_atlas_router.py`, `lab_pipeline_aggregator.py`, `analytics/*`), the app-layer reader
  (`apps/4DLabWired/wired/composition.py` `from comlab import LabPipelineAggregator`), and the guarding
  tests. **No other lab is a COMLab consumer** (Rule 1).
- **Proposed ADRs / `comlab/config/proposals/` tokens stay labelled proposal** — never a live `CONSUMES` edge.

### Success criteria ###

1. `4dlab-doc-prep explode → tables → anchor → relations → verify` run over the **six** listed docs (HLD,
   DLD, LLD, BDD, PRD + the 11 ADR records); output under `graph/v2_docs/ingest_ready/<doc>/`.
2. `Vocabulary/`, `CROSS_LAB_DEPENDENCIES.md`, `ARCHIVE/`, `adr/README.md` are **excluded** (verify the
   explicit file list, not a glob, was used).
3. Every `CONSUMES`/`VERIFIES` names an existing path/test; zero orphans (or each routed back); no
   lab-as-consumer.
4. Proposal records stay labelled; no proposal appears as a live edge.
5. `verify` clean; lineage anchors present on all six.

### Out of scope ###

- Running graphify (docs Pass-3 **waived** — START_HERE §1) · the vocab notes (→ `T-COM-VAULT` step 0) ·
  re-reconciling doc content (was `T-COM-DOCS-V2`). **GRAPH GUARDRAIL:** no graphify.

### Files to touch ###

- `labs/comlab/graph/v2_docs/ingest_ready/<doc>/…` (prep output; **not** `graph.json`).

### Verification ###

```bash
cd <repo>/labs/comlab
ls graph/v2_docs/ingest_ready/    # HLD/DLD/LLD/BDD/PRD + 11 ADR dirs; no Vocabulary/CROSS_LAB/ARCHIVE/README
test -d graph/v2_docs/ingest_ready/OBD_VOCABULARY && echo "FAIL vocab ingested" || echo "OK vocab excluded"
test -d graph/v2_docs/ingest_ready/CROSS_LAB_DEPENDENCIES && echo "FAIL cross-lab ingested" || echo "OK excluded"
grep -rn 'CONSUMES\|VERIFIES' graph/v2_docs/ingest_ready/ | wc -l
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-DOCPREP.md` opens with the confirmed `## Plan` (the six-doc list +
exclusions); the run session fills `VERIFICATION GATE` (six docs prepped, exclusions held, zero orphans,
proposals labelled, no lab-as-consumer) + `CODE REVIEW` (chunk/table/relation counts). Ledger row → `done`
only when clean.
