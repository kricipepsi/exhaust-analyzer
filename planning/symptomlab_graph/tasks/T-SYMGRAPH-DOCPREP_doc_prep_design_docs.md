# T-SYMGRAPH-DOCPREP — Doc-prep the SymptomLab design docs for graphify (`4dlab-doc-prep`)

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE / graph-tooling-author lane (no lab inner-loop/gate)
**Blocked by:** — (independent; the 6 docs are already v2 — see Context. Runs in parallel with the wiki track.)

> **Lane:** graph tooling. This task **runs** `4dlab-doc-prep` (`explode → tables → anchor →
> relations → verify`) and confirms coverage. It never writes `graph.json` and never runs
> graphify (that is T-SYMGRAPH-LLM). It is structural prep, not a content rewrite.

### Goal ###

Produce the prepared chunk tree `labs/symptomlab/graph/v2_docs/ingest_ready/<doc>/…` from the
six v2 SymptomLab design docs, so T-SYMGRAPH-LLM can ingest them into `graph/v2_docs/`. Proof
of done: an `ingest_ready/` tree with one subtree per included doc (monolith split by header,
tables → entity blocks, lineage anchor + architectural relation lines), and `verify` clean.

### Success criteria ###

- A quick **currency confirm** (folded in per owner decision — no separate DOCS-V2 task): each
  of the six docs' field/bound/enum claims still matches AST ground-truth in
  `labs/symptomlab/symptomlab/` (`models.py`, `validator.py`, `allowed_combinations.yaml`). Any
  mismatch is logged as an Unplanned follow-up — it does **not** block prep unless a doc
  describes a pruned/renamed symbol, in which case STOP and surface it.
- `4dlab-doc-prep verify` reports coverage clean over the six-doc ingest set.
- Every `CONSUMES`/`VERIFIES` relation line emitted into a chunk names a real, existing
  SymptomLab code path or test (orphans flagged; proposals stay labelled proposals).
- `ingest_ready/` contains exactly six doc subtrees — the excluded files (below) are absent.

### Context ###

The six design docs must describe the shipped code. Checked 2026-06-12, all six already carry
v2 `Current`/`Approved` headers (`HLD/DLD/LLD` v2.1, `PRD` v2.1, `ADR`/`BDD` current) — so
**no standalone DOCS-V2 reconcile task is needed**; the currency confirm above is folded into
this prep run (owner decision). Docs are monolithic (unlike the pre-chunked wiki), which is why
doc-prep adds the `explode`/`tables`/`anchor` steps the wiki skill doesn't have.

**Load skills:** `_skills\graph\4dlab-doc-prep\SKILL.md` — read end-to-end first; it defines
`explode → tables → anchor → relations → verify`. Confirm the skill ingests an **explicit file
list**, never a `docs/*.md` glob (the OBDLab exclusion-discipline lesson).

**READ-NARROW:** open each doc's header + the sections the skill flags; do not whole-read all
six. Grep the AST symbols only to confirm `CONSUMES`/`VERIFIES` targets resolve.

### Ingest set — EXACTLY these six v2 design docs ###

| Include | Why |
|---|---|
| `docs/HLD_SymptomLab.md` | system/module decomposition |
| `docs/DLD_SymptomLab.md` | detailed schema/field design |
| `docs/LLD_SymptomLab.md` | low-level validator logic |
| `docs/ADR_SymptomLab.md` | accepted architecture decisions (sibling-split back-fill) |
| `docs/BDD_SymptomLab.md` | scenarios (seed `VERIFIES` edges from the live test suite) |
| `docs/PRD_SymptomLab.md` | requirements (v2.1) |

### Exclusions — MUST NOT ingest (pin explicitly; never glob `docs/*.md`) ###

- `docs/SYMPTOM_VOCABULARY.md` — vocabulary; it has its own vault home via the `_vocabulary/`
  tier (built in T-SYMGRAPH-VAULT). Ingesting it here would duplicate it in the docs graph.

### Consumer (signal/noise) ###

**Adds no schema field.** Produces the prepared chunk tree that T-SYMGRAPH-LLM ingests into
`graph/v2_docs/`. That graph's consumers are the **vault build** (`build_lab_vault.py` reads it
to inform frontmatter) and the **design→code→test spine** in `consumers.base` /
`drift-guards.base` via derived `implements`/`consumers`/`drift_guards`. Every `CONSUMES`/
`VERIFIES` line written into a chunk must name a real, existing SymptomLab code path/test
(grep-checked).

### Deliverables ###

1. `labs/symptomlab/graph/v2_docs/ingest_ready/<doc>/…` (CREATE) — one prepared subtree per
   included doc.
2. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-DOCPREP.md` (CREATE) — `## Plan`
   + currency-confirm result + `verify` output + the `CONSUMES`/`VERIFIES` orphan grep-check +
   confirmation the six-doc set (not the vocab file) was ingested.

### Files to touch ###

- `labs/symptomlab/graph/v2_docs/ingest_ready/` (CREATE — skill output)
- progress note (CREATE)
- (design-doc bodies: **no edits** — prep is structural; content was already v2)

### Out of scope ###

No graphify run (T-SYMGRAPH-LLM). No design-doc content edits — if currency confirm finds
drift, log it, don't fix it here. No ingest of `SYMPTOM_VOCABULARY.md`. No wiki-prep operations
(that is T-SYMGRAPH-WIKIPREP) — crossing the streams is the most common mistake. Do not write
into `graph/v2_docs/graph.json` (it does not exist yet; the LLM task creates it).

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2

# Run the skill (exact CLI per 4dlab-doc-prep/SKILL.md), explicit 6-file list, NOT a glob.

# Confirm exactly the six doc subtrees exist and the vocab file was NOT ingested
ls labs/symptomlab/graph/v2_docs/ingest_ready/
test ! -e labs/symptomlab/graph/v2_docs/ingest_ready/SYMPTOM_VOCABULARY && echo "OK: vocab excluded"

# Orphan check — CONSUMES/VERIFIES targets must resolve in code or tests
grep -rhoE "(CONSUMES|VERIFIES) \*\*[^*]+\*\*" labs/symptomlab/graph/v2_docs/ingest_ready/ | sort -u
#   for each: grep -rn "<symbol>" labs/symptomlab/symptomlab/ labs/symptomlab/tests/   # must hit
```

`verify` must report clean; six subtrees present; vocab absent; all edge targets resolve.

### Progress hook ###

PROGRESS `T-SYMGRAPH-DOCPREP`: Status=done, Files=ingest_ready/ (6 subtrees),
Verification="doc-prep verify clean; 6 docs ingested, vocab excluded; edges resolve".
