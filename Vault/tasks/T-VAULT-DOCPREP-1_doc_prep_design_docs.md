---
node_type: task
task_id: T-VAULT-DOCPREP-1
status: done
pack: VAULT · **Mode:** GRAPH-TOOLING lane
lab: obdlab
mode: graph-tooling lane
blocked_by:
- T-VAULT-PRD-V2-1
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- graph/v2_docs — docs graph
- design→code→test spine (.base views)
implements:
- graph/v2_docs/graph.json
tags:
- task
- vault
- obdlab
---

# T-VAULT-DOCPREP-1 — Doc-prep the OBDLab design docs for graphify (TODO-4, part 1)

**Status:** `done` · **Pack:** VAULT · **Mode:** GRAPH-TOOLING lane (prep skill run — no lab inner-loop/gate)
**Origin:** HANDOFF TODO-4 + plan §2 "docs tier pending TODO-4" + owner request 2026-06-10 · **Blocked by:** T-VAULT-PRD-V2-1
**Consumer (signal/noise):** **Adds no schema field.** Produces the prepared chunk tree
`graph/v2_docs/ingest_ready/` that T-VAULT-DOCGRAPH-1 ingests into `graph/v2_docs/`. The docs-tier graph's consumers
are the **vault build** (`build_lab_vault.py` reads the graph to inform frontmatter — wired by T-VAULT-PATHS-1,
`done`) and the **design→code→test spine** in `consumers.base` / `drift-guards.base` via the `implements` /
`consumers` / `drift_guards` frontmatter the build derives (plan §4). Per the doc-prep skill's honesty rule,
**every `CONSUMES` / `VERIFIES` relation line written into a chunk must name a real, existing code path or test**
(grep-checked); a field with no live consumer is not written as an edge — it is flagged for the architect or, if a
consumer can be named, routed as a proposal (`comlab/config/proposals/`). Signal/noise is enforced at the edge level.

### Role note (graph-tooling lane) ###

Running `4dlab-doc-prep` is **graph tooling**, not lab diagnostic code — same lane as the vault-tooling tasks: no
`obdlab/` inner-loop / 6-phase gate. The skill is authored; this task **runs** it (explode → tables → anchor →
relations → verify) and confirms coverage. The skill **never** writes `graph.json` and **never** runs graphify
(that is T-VAULT-DOCGRAPH-1). No `obdlab/` code/test edit; no re-extraction.

### Goal ###

Turn the monolithic OBDLab v2 design docs into hierarchy-preserving, anchored, relation-bearing chunks under
`graph/v2_docs/ingest_ready/<doc>/…`, ready for graphify's Pass-3 LLM ingestion — closing the TODO-4 deferral that
exists because `4dlab-wiki-prep` is the wrong skill for monolithic design docs (it assumes already-chunked prose).

### Ingest set — EXACTLY these six v2 design docs ###

| Include (v2 design docs) | Why |
|---|---|
| `docs/HLD_OBDLab.md` | v2 — system/module decomposition |
| `docs/DLD_OBDLab.md` | v2 — detailed schema/field design |
| `docs/LLD_OBDLab.md` | v2 — low-level logic |
| `docs/ADR_OBDLab.md` | v2 — accepted architecture decisions |
| `docs/BDD_OBDLab.md` | v2 — scenarios (seed `VERIFIES` edges) |
| `docs/PRD_OBDLab.md` | **v2 after T-VAULT-PRD-V2-1** — requirements |

### Exclusions — MUST NOT ingest (pin these explicitly; do not glob the folder) ###

The `docs/` folder also contains files that are **not** OBDLab design docs. Passing an explicit six-file set (not a
`docs/*.md` glob) is the guard:

- `docs/ADR.md` and `docs/BDD.md` — **generic upstream skill stubs** ("Architecture Decision Records are
  lightweight documents…", "Behavior-Driven Development (BDD) Skill"), **not** OBDLab content. The skill's Step-0
  exclusion list (which names only `OBDlab.md` + the vocab duplicate) does **not** mention these — see Deliverable 2.
- `docs/OBD_VOCABULARY.md` — **duplicate** of canonical `labs/semantic/vocabul/OBD_VOCABULARY.md`; it has its own
  vault home via **T-VAULT-VOCAB-1** (the `_vocabulary/` tier). Skill Step-0 already excludes it.
- `docs/DocPrep.md`, `docs/HANDOFF_obdlab_docs_2026-06-10.md` — owner/handoff notes, not design docs.
- `docs/drift_inventory_2026-05-25.md` — inventory artefact, not a design doc (HANDOFF TODO-5).
- `docs/OBDlab.md` — superseded blueprint; **already archived** (not present in `docs/` root) — confirm it is not reachable.

### Success criteria ###

1. `graph/v2_docs/ingest_ready/<doc>/…` exists for **exactly** the six v2 docs, one output subtree per source doc;
   no subtree derived from any excluded file.
2. **explode** — every `##` (and large `###`) section of each source doc produced exactly one chunk, file-named
   after the header, mirroring the heading tree into folders. Section body copied **verbatim** (prose, field defs,
   numeric literals **with their wiki-citation comments**).
3. **tables** — logic-bearing tables (fields, bounds, enum rosters, routing) converted to labelled entity blocks;
   narrative tables left as tables; citation comments preserved exactly.
4. **anchor** — every chunk opens with a `> **Context:**` header naming **module + parent document** (and the
   mirrored contract section where the chunk restates a boundary schema).
5. **relations** — every chunk has exactly one `## Graph relations (explicit)` block, zero empty blocks; every
   `CONSUMES` / `VERIFIES` object **resolves to a real field/enum/code path or test** (grep-checked); proposals
   labelled as proposals, never promoted to live.
6. **verify** — skill `verify` op reports: full section coverage (no lost/double-exploded section), anchors present
   on every chunk, relation-line counts by predicate, zero orphan edges, exclusions honoured, citations intact.
7. **No `graph.json` written; graphify NOT run; no `obdlab/` code/test edit; no re-extraction.**

### Deliverables ###

1. `graph/v2_docs/ingest_ready/{HLD,DLD,LLD,ADR,BDD,PRD}_OBDLab/…` — the prepared chunk trees.
2. `_skills/graph/4dlab-doc-prep/SKILL.md` — **extend the Step-0 exclusion list** to also name the generic
   `docs/ADR.md` and `docs/BDD.md` skill stubs (one line), so a future folder-level run can't sweep them in.
   *(Small skill correction; graph-tooling lane.)*
3. A short coverage report (sections found / chunks written / tables converted / relation lines by predicate),
   per the skill's output conventions — appended to the progress note.

### Files to touch ###

- `labs/obdlab/graph/v2_docs/ingest_ready/…` (new chunk trees)
- `_skills/graph/4dlab-doc-prep/SKILL.md` (extend exclusion list only)

### Out of scope ###

- Running graphify / writing `graph/v2_docs/graph.json` — T-VAULT-DOCGRAPH-1.
- Editing the design docs' content — that is authoring (PRD = T-VAULT-PRD-V2-1; the rest are already v2). Prep is
  structural (explode/anchor/table-block/append relations) only; it never rewrites sourced prose.
- The vault populate build (`build_lab_vault.py --lab obdlab`) — separate step (plan §8).
- Vocabulary note (`_vocabulary/`) — T-VAULT-VOCAB-1.

### Verification (graph-tooling lane) ###

```bash
cd <repo>/labs/obdlab
# 1) exactly six subtrees, none from an excluded file
ls graph/v2_docs/ingest_ready/
#    expect: HLD_OBDLab DLD_OBDLab LLD_OBDLab ADR_OBDLab BDD_OBDLab PRD_OBDLab — and nothing else
for bad in ADR BDD OBD_VOCABULARY DocPrep HANDOFF_obdlab_docs_2026-06-10 drift_inventory_2026-05-25 OBDlab; do
  test -e "graph/v2_docs/ingest_ready/$bad" && echo "FAIL excluded ingested: $bad"
done; echo "exclusion check done"
# 2) every chunk has an anchor + exactly one relations block
missing_anchor=$(grep -rL '> \*\*Context:\*\*' graph/v2_docs/ingest_ready/ | wc -l)
echo "chunks missing anchor: $missing_anchor   (expect 0)"
# 3) no orphan CONSUMES/VERIFIES object — spot a sample back to live code/tests (grep each named path)
grep -rhoE 'CONSUMES \*\*[^*]+\*\*|VERIFIES \*\*[^*]+\*\*' graph/v2_docs/ingest_ready/ | sort -u | head
# 4) graph provenance untouched
git status --porcelain graph/v2_docs/graph.json graphify-out/ 2>/dev/null | grep . \
  && echo "FAIL graph.json/graphify-out changed" || echo "OK no graph write"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-DOCPREP-1.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (the four checks + the skill coverage report) + `CODE REVIEW` (chunk counts per doc, exclusions
honoured, skill exclusion-list line added). The plan §8 row flips to `done` only when both blocks are clean.
Verification = "six v2 docs exploded/anchored/relationed into graph/v2_docs/ingest_ready/, full section coverage,
zero orphan edges, exclusions (generic ADR.md/BDD.md, vocab dup) honoured, citations intact; no graphify run, no
re-extraction".
