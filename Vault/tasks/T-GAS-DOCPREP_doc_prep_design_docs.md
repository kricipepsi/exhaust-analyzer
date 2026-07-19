---
node_type: task
task_id: T-GAS-DOCPREP
status: pending
pack: VAULT
lab: gaslab
mode: graph-tooling / author lane
blocked_by:
- T-GAS-DOCS-V2
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
- gaslab
---

# T-GAS-DOCPREP — Doc-prep the GASLab design docs for graphify (`4dlab-doc-prep`)

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** GRAPH-TOOLING / author lane (prep skill — no lab inner-loop/gate)
**Origin:** pipeline guide §4 (doc prep) + OBDLab `T-VAULT-DOCPREP-1` model · **Blocked by:** T-GAS-DOCS-V2
**Consumer (signal/noise):** **Adds no schema field.** Produces the prepared chunk tree
`graph/v2_docs/ingest_ready/<doc>/…` that T-GAS-GRAPH-LLM ingests into `graph/v2_docs/`. That graph's
consumers are the **vault build** (`build_lab_vault.py` reads it to inform frontmatter) and the
**design→code→test spine** in `consumers.base` / `drift-guards.base` via derived `implements` /
`consumers` / `drift_guards` (plan §4). Every `CONSUMES` / `VERIFIES` line written into a chunk must
name a real, existing GASLab code path or test (grep-checked); orphans flagged, proposals stay proposals.

### Role note ###

`4dlab-doc-prep` is graph tooling — no `gaslab/` inner-loop/gate. This task **runs** the skill
(`explode → tables → anchor → relations → verify`) and confirms coverage. It never writes `graph.json`
and never runs graphify (that is T-GAS-GRAPH-LLM). No design-doc *content* edit (that was T-GAS-DOCS-V2);
prep is structural only.

### Ingest set — EXACTLY these six v2 design docs ###

| Include | Why |
|---|---|
| `docs/HLD_GASLab.md` | system/module decomposition |
| `docs/DLD_GASLab.md` | detailed schema/field design |
| `docs/LLD_GASLab.md` | low-level rule logic |
| `docs/ADR_GASLab.md` | accepted architecture decisions (v2 after T-GAS-DOCS-V2) |
| `docs/BDD_GASLab.md` | scenarios (seed `VERIFIES` edges) (v2 after T-GAS-DOCS-V2) |
| `docs/PRD_GASLab.md` | requirements (v2.1) |

### Exclusions — MUST NOT ingest (pin explicitly; never glob `docs/*.md`) ###

- `docs/GAS_VOCABULARY.md` — vocabulary; it has its own vault home via the `_vocabulary/` tier
  (built `--vocab`). Mirrors OBDLab's `OBD_VOCABULARY.md` exclusion.
- `docs/audits/` (e.g. `AUDIT_2026-06-10_gaslab_state.md`) — assessment artefact, not a design doc.
- Any generic upstream skill stub (`ADR.md` / `BDD.md` with no `_GASLab` suffix), handoff/inventory
  notes, or superseded blueprints if present — confirm none are reachable. (OBDLab's
  `T-VAULT-DOCPREP-1` extended the skill's Step-0 exclusion list to name the generic `ADR.md`/`BDD.md`
  stubs; reuse that exclusion here.)

### Success criteria (mirror OBDLab `T-VAULT-DOCPREP-1`) ###

1. `graph/v2_docs/ingest_ready/{HLD,DLD,LLD,ADR,BDD,PRD}_GASLab/…` exists for **exactly** the six docs;
   no subtree from any excluded file.
2. **explode** — every `##` (and large `###`) section → exactly one chunk, file-named after the
   header, heading tree mirrored to folders; body copied **verbatim** (prose, field defs, numeric
   literals **with their wiki-citation comments**).
3. **tables** — logic-bearing tables (fields, bounds, enum rosters, routing) → labelled entity blocks;
   narrative tables left as tables; citations preserved.
4. **anchor** — every chunk opens with a `> **Context:**` header naming module + parent document.
5. **relations** — exactly one `## Graph relations (explicit)` block per chunk, zero empty; every
   `CONSUMES` / `VERIFIES` object resolves to a real GASLab field/enum/code path or test (grep-checked);
   proposals labelled, never promoted.
6. **verify** — full section coverage, anchors on every chunk, relation counts by predicate, zero
   orphan edges, exclusions honoured, citations intact.
7. **No `graph.json` written; graphify NOT run; no code/test edit; no re-extraction.**

### Out of scope ###

- Running graphify / writing `graph/v2_docs/graph.json` — T-GAS-GRAPH-LLM.
- Editing doc content — T-GAS-DOCS-V2 (already done before this runs).
- The wiki corpus — T-GAS-WIKIPREP (do not cross the streams).
- The vocabulary note — `_vocabulary/` tier at build time.

### Files to touch ###

- `labs/gaslab/graph/v2_docs/ingest_ready/…` (new chunk trees).
- If the skill's Step-0 exclusion list needs a GAS-specific line, extend `_skills/graph/4dlab-doc-prep/SKILL.md` (one line).

### Verification ###

```bash
cd <repo>/labs/gaslab
ls graph/v2_docs/ingest_ready/   # expect: HLD_GASLab DLD_GASLab LLD_GASLab ADR_GASLab BDD_GASLab PRD_GASLab — nothing else
for bad in GAS_VOCABULARY audits ADR BDD; do
  test -e "graph/v2_docs/ingest_ready/$bad" && echo "FAIL excluded ingested: $bad"; done; echo "exclusion check done"
echo "chunks missing anchor: $(grep -rL '> \*\*Context:\*\*' graph/v2_docs/ingest_ready/ | wc -l)  (expect 0)"
git status --porcelain graph/v2_docs/graph.json 2>/dev/null | grep . && echo "FAIL graph write" || echo "OK no graph write"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-DOCPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (six subtrees, full coverage, anchors, zero orphan edges, exclusions honoured,
citations intact) + `CODE REVIEW` (chunk counts per doc). Ledger row flips to `done` only when clean.
