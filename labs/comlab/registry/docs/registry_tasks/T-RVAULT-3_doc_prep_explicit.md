### Goal ###

Run `4dlab-doc-prep` (explode → tables → anchor → relations → verify) over the
**explicit docs list** pinned in T-RVAULT-1, producing the ingest-ready doc corpus at
`labs/comlab/registry/graph/v2_docs/ingest_ready/<doc>/…` with implied links made
EXTRACTED-explicit. Done when `verify` passes and every `CONSUMES`/`VERIFIES` relation
line names a real, existing registry code path or test (orphans flagged, proposals
labelled).

### Success criteria ###

- `labs/comlab/registry/graph/v2_docs/ingest_ready/` exists, one subtree per INCLUDE
  doc from `docs/VAULT_DOCS_MANIFEST.md` (no globbed extras).
- `4dlab-doc-prep verify` exits clean: monoliths split by header, tables → entity
  blocks, each doc carries a lineage anchor + explicit `**SUBJECT** PREDICATE
  **OBJECT**` relation lines.
- Every `CONSUMES`/`VERIFIES` line resolves to an existing path under
  `labs/comlab/registry/` (rule JSON, `integration_shim.py`, `schema_v2.py`, or a
  `tests/` file) — verified by the skill's orphan check; any unresolved line is a
  prep gap to fix here, never a promoted proposal.

### Context ###

Phase 2 doc-prep from `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md §4`. Docs are `.md`
prose (+ one `.html`) → graphify reads them with **Pass 3 (LLM)**, which tags an edge
EXTRACTED only when the text states it directly; doc-prep appends the explicit relation
lines so the LLM extracts facts instead of guessing. Input is the **deglobbed** list
from T-RVAULT-1 (`docs/VAULT_DOCS_MANIFEST.md` INCLUDE table) — do not re-glob `docs/`.

`case_library.html` is an HTML render of the 252 curated cases; if doc-prep cannot
ingest HTML directly, convert it to markdown first with the `html-extractor` skill
(its case rows become entity blocks). The registry's natural relations are
`<rule-family> CONSUMES <ChemistryState>` and `<rule-family> VERIFIES <case-id>` —
keep these pointed at real `rules/*.json` ids and `corpus_curated.csv` case ids.

Load skills: `_skills/graph/4dlab-doc-prep`; `anthropic-skills:html-extractor` (only
if `case_library.html` needs markdown conversion).

### Consumer (signal/noise) ###

N/A — no new field/enum/fault. Doc-prep makes existing relations explicit; it adds no
schema. (The ingest-ready corpus is consumed by graphify in T-RVAULT-5.)

### Deliverables ###

1. `labs/comlab/registry/graph/v2_docs/ingest_ready/` — exploded, anchored,
   relation-annotated doc corpus (one subtree per INCLUDE doc).
2. `labs/comlab/registry/graph/v2_docs/DOC_PREP_REPORT.md` — verify output + the
   orphan-relation resolution log.

### Files to touch ###

- `labs/comlab/registry/graph/v2_docs/ingest_ready/**` (CREATE)
- `labs/comlab/registry/graph/v2_docs/DOC_PREP_REPORT.md` (CREATE)

### Out of scope ###

Do NOT run graphify / build `graph.json` (that is T-RVAULT-5 — doc-prep never writes a
graph). Do NOT edit the source docs' prose (figure reconciliation already happened in
T-RVAULT-1); doc-prep writes ONLY into `ingest_ready/`. Do NOT invent a relation whose
target doesn't exist to satisfy the extractor — flag it.

GRAPH GUARDRAIL (standing): doc-prep produces ingest-ready text only; it does NOT run
`graphify` and does NOT touch any existing `graph.json`.

### Verification ###

```bash
cd /agent_workspace
test -d labs/comlab/registry/graph/v2_docs/ingest_ready && echo "ingest_ready present"
# one subtree per INCLUDE doc, no extras
ls labs/comlab/registry/graph/v2_docs/ingest_ready
# verify report shows clean + zero unresolved relation orphans
grep -i "unresolved\|orphan" labs/comlab/registry/graph/v2_docs/DOC_PREP_REPORT.md || echo "no orphans logged"
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-RVAULT-3`: Status=done, Files changed={COUNT}, Verification="doc-prep ingest_ready built; relations EXTRACTED; 0 orphans"
