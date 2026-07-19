# T-SYMGRAPH-WIKIPREP — Wiki-prep the SymptomLab corpus for graphify (`4dlab-wiki-prep`)

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE / graph-tooling-author lane (no lab inner-loop/gate)
**Blocked by:** T-SYMGRAPH-WIKI-AUTHOR

> **Lane:** graph tooling. This task **runs** `4dlab-wiki-prep` on the wiki corpus and
> confirms coverage. It never writes `graph.json` and never runs graphify (that is
> T-SYMGRAPH-LLM). It makes implied relations **explicit** in append-only trailer blocks —
> it does **not** rewrite the notes' prose.

### Goal ###

Run `4dlab-wiki-prep` (`relations → labels → roster → verify`) over the canonical wiki corpus
authored in T-SYMGRAPH-WIKI-AUTHOR (`labs/symptomlab/wiki/01_*…04_*.md`), so graphify Pass-3
extracts facts instead of guessing. Proof of done: each live note carries an explicit
relations trailer with canonical entity labels, every `CONSUMES`/`VERIFIES` line names a real
SymptomLab code path or test, and the skill's `verify` step reports coverage clean.

### Success criteria ###

- `4dlab-wiki-prep verify` reports no unresolved relations and no orphan `CONSUMES`/`VERIFIES`
  edges across `labs/symptomlab/wiki/`.
- Every `CONSUMES`/`VERIFIES` line in the trailer blocks grep-resolves to a real symbol in
  `labs/symptomlab/symptomlab/` or `labs/symptomlab/tests/` (orphans flagged, not shipped).
- The roster lists the canonical entity labels (catalog tier_1/tier_2 ids, the 3 axis enums,
  `SymptomDNA`) — and these match the labels the AST `v2_code` tier already uses (so wiki and
  code nodes will merge, not duplicate, at vault time).
- Notes' prose bodies are byte-unchanged except for the appended trailer blocks (append-only).

### Context ###

The wiki tier is Pass-3 (LLM semantic read), so graph quality depends on how explicit the
relationships are in the text. `4dlab-wiki-prep` appends explicit
`**SUBJECT** PREDICATE **OBJECT**` lines + canonical labels so the extractor tags edges
`EXTRACTED` (full confidence) rather than `INFERRED`/`AMBIGUOUS`. This is the wiki analogue of
the code-prep audit T-SYMGRAPH-2 already ran. Wiki is pre-chunked, so it goes straight to
`relations` (no `explode`/`tables` steps — those are doc-prep's).

**Load skills:** `_skills\graph\4dlab-wiki-prep\SKILL.md` — read end-to-end first; it defines
`relations → labels → roster → verify`. Run the wiki branch only.

**READ-NARROW:** read the four live notes (created last task), plus `models.py` /
`allowed_combinations.yaml` only to grep-confirm `CONSUMES`/`VERIFIES` targets resolve. Do not
whole-read the research source again — it is upstream of the authored notes.

### Consumer (signal/noise) ###

**Adds no schema field.** Produces append-only relation trailers that make the wiki's implied
links extractable. The `v2_wiki` graph those feed (built in T-SYMGRAPH-LLM) is consumed by the
vault build (`build_lab_vault.py` reads it to inform frontmatter) and the design→code→test
spine in the `.base` views. Every `CONSUMES`/`VERIFIES` line written here must name a real,
existing SymptomLab code path/test (grep-checked) — the same edge-level signal/noise rule as
the sibling labs.

### Deliverables ###

1. `labs/symptomlab/wiki/01_symptom_catalog.md` … `04_catalog_changelog.md` (MODIFY —
   append-only relation/label trailers, ×4).
2. Whatever roster/verify artefact the skill emits (per its SKILL.md — typically a report
   under the wiki dir or `graph/`; do **not** invent a path, use the skill's own).
3. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-WIKIPREP.md` (CREATE) —
   `## Plan` + the `verify` output + the orphan grep-check for `CONSUMES`/`VERIFIES` targets.

### Files to touch ###

- `labs/symptomlab/wiki/0{1,2,3,4}_*.md` (MODIFY — append-only)
- skill's roster/verify output (CREATE — path per SKILL.md)
- progress note (CREATE)

### Out of scope ###

No graphify run (T-SYMGRAPH-LLM). No edits to the proposal note in `comlab/.../proposals/`
(it is not a graph source). No prose rewrites — trailers are append-only; if a relation can't
be made explicit without rewriting the body, that is a gap routed back to
T-SYMGRAPH-WIKI-AUTHOR, not patched here. No doc-prep operations (`explode`/`tables`/`anchor`)
— those belong to the docs corpus only; running them here is crossing the streams.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2

# Run the skill's verify operation (exact CLI per 4dlab-wiki-prep/SKILL.md)
#   4dlab-wiki-prep relations -> labels -> roster -> verify, scoped to labs/symptomlab/wiki/

# Orphan check — every CONSUMES/VERIFIES target must resolve in code or tests
grep -rhoE "(CONSUMES|VERIFIES) \*\*[^*]+\*\*" labs/symptomlab/wiki/ | sort -u
#   for each named symbol, confirm it exists:
grep -rn "<symbol>" labs/symptomlab/symptomlab/ labs/symptomlab/tests/   # must hit
```

`verify` must report clean; every `CONSUMES`/`VERIFIES` symbol must grep-resolve. Paste both
into the progress note.

### Progress hook ###

PROGRESS `T-SYMGRAPH-WIKIPREP`: Status=done, Files=4 notes + verify report,
Verification="wiki-prep verify clean; all CONSUMES/VERIFIES targets resolve".
