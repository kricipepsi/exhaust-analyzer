---
node_type: task
task_id: T-DTC-DOCPREP
status: pending
pack: VAULT
lab: dtclab
mode: architect/author lane
blocked_by:
- T-DTC-DOCS-V2
consumers:
- graph/v2_docs — docs graph
- COMLab analytics / fault-atlas routing
tags:
- task
- vault
- dtclab
---

# T-DTC-DOCPREP — Doc-prep the six v2 design docs (`4dlab-doc-prep`)

**Status:** `pending` · **Pack:** VAULT (DTCLab) · **Mode:** architect/author lane (graph-tooling; no lab inner-loop)
**Origin:** pipeline guide §4 (doc prep) · **Blocked by:** T-DTC-DOCS-V2
**Consumer (signal/noise):** **Adds no schema field.** Splits the monolithic design docs into
ingest-ready, header-anchored blocks with explicit architectural-relation lines, so the docs-tier vault
copy's `implements`/`consumers` frontmatter derives from named COMLab consumers. Every `CONSUMES`/
`VERIFIES` line must name a real, existing code path or test. No new fields.

### Role note ###

`4dlab-doc-prep` runs `explode → tables → anchor → relations → verify`, writing
`graph/v2_docs/ingest_ready/<doc>/…`. It does **not** write `graph.json` and does **not** run graphify.
(The docs prose graph itself is **waived** this pack — "skip graph testing" — but the prep output still
feeds the vault docs-tier frontmatter, so the prep runs.)

### Ingest the SIX design docs by explicit file list (never a glob) ###

Per OBDLab exclusion discipline (guide §3·1D), `docs/` holds non-design-doc files that must be
**excluded**. Ingest exactly:

```
labs/dtclab/docs/HLD_DTCLab.md
labs/dtclab/docs/DLD_DTCLab.md
labs/dtclab/docs/LLD_DTCLab.md
labs/dtclab/docs/ADR_DTCLab.md
labs/dtclab/docs/BDD_DTCLab.md
labs/dtclab/docs/PRD_DTCLab.md
```

**Exclude:**
- `DTC_VOCABULARY.md` — the vocabulary surface; it has its own `_vocabulary/` vault home (built by
  `T-DTC-VAULT` step 0), exactly like OBDLab's `OBD_VOCABULARY.md` / GASLab's `GAS_VOCABULARY.md`.
- `docs/_archive/` (e.g. `DTC_WIKI_v1_single.md`) — superseded.

### Architectural-relation discipline ###

- Anchor each doc to its lineage (`HLD ← PRD`, `DLD ← HLD`, `LLD ← DLD/HLD`, etc. — the docs already
  carry these baselines in their headers).
- Emit `IMPLEMENTS` / `CONSUMES` / `VERIFIES` relation lines that name real symbols: the COMLab
  consumers (fault-atlas router, aggregator, Bayesian `combine()` FU-1 via the Wired adapter `T-DTW-1`),
  and the test files that guard each rule.
- **ADR-0009 (`EP-DTC-NOSTART-1`) is a Proposed record** — its relations must be labelled proposal, not
  emitted as a live `CONSUMES` edge.

### Success criteria ###

1. `4dlab-doc-prep explode → tables → anchor → relations → verify` run over the **six** listed docs;
   output under `graph/v2_docs/ingest_ready/<doc>/`.
2. `DTC_VOCABULARY.md` and `_archive/` are **excluded** (verify the file list, not a glob, was used).
3. Every `CONSUMES`/`VERIFIES` names an existing code path/test; zero orphans (or each routed back).
4. Proposal records (ADR-0009; PRD §8) stay labelled; no proposal appears as a live edge.
5. `verify` step clean; lineage anchors present on all six.

### Out of scope ###

- Running graphify (docs Pass-3 **waived** this pack) · the vocab note (→ `T-DTC-VAULT` `_vocabulary/`).
- Re-reconciling doc content (that was `T-DTC-DOCS-V2`) · the GPF decision (START_HERE §5).

### Files to touch ###

- `labs/dtclab/graph/v2_docs/ingest_ready/<doc>/…` (prep output; **not** `graph.json`).

### Verification ###

```bash
cd <repo>/labs/dtclab
ls graph/v2_docs/ingest_ready/    # six doc dirs, no DTC_VOCABULARY, no _archive
grep -rn 'CONSUMES\|VERIFIES' graph/v2_docs/ingest_ready/ | wc -l
test -d graph/v2_docs/ingest_ready/DTC_VOCABULARY && echo "FAIL vocab ingested" || echo "OK vocab excluded"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-DOCPREP.md` opens with the confirmed `## Plan` (the six-file list +
exclusions); the run session fills `VERIFICATION GATE` (six docs prepped, vocab excluded, zero orphans,
proposals labelled) + `CODE REVIEW` (chunk/table/relation counts). Ledger row → `done` only when clean.
