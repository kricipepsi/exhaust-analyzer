---
name: 4dlab-doc-prep
description: >
  Prepare 4DLab DESIGN DOCUMENTS (HLD / DLD / LLD / ADR / BDD, PRDs) for graphify knowledge-graph
  ingestion. (After this prep the docs graph extracts **offline** via `graphify update` with edges tagged EXTRACTED — no LLM/API key needed; an LLM Pass-3 is optional and marginal. graphify ≠ LLM.) Design docs carry a hierarchy (System → Module →
  Schema → Field → Task-ID) and architectural relations (a module CONSUMES a field, a doc
  MIRRORS_CONTRACT_IN the semantic contract, a v2 doc SUPERSEDES a v1 blueprint, a BDD VERIFIES a
  schema). Flat chunking destroys that hierarchy and turns tables into "soup". This skill explodes a
  doc by header, converts logic tables to entity blocks, injects anchor context, and appends explicit
  architectural relation lines — so graphify tags edges EXTRACTED (1.0) instead of INFERRED.
  Use this skill whenever the user mentions prepping a design doc / HLD / DLD / LLD / ADR / BDD / PRD
  for ingestion, "graphify the design docs", exploding a doc by headers, table-to-object conversion,
  anchor context headers, or asks why a design-doc edge came back INFERRED/AMBIGUOUS.
  This is the DESIGN-DOC counterpart to 4dlab-wiki-prep and 4dlab-code-prep:
  4dlab-code-prep = SOURCE CODE (Pass 1, AST); 4dlab-wiki-prep = WIKI/RESEARCH CHUNK corpus
  (Pass 3, already chunked prose); THIS skill = monolithic DESIGN DOCS that must be exploded and
  contextualised first, then carry architectural predicates. If the input is a .py package use
  4dlab-code-prep; if it is the already-chunked research/ wiki corpus use 4dlab-wiki-prep. To run
  graphify after prep, use 4dlab-graphify-run.
allowed-tools: Read, Grep, Glob, Bash, Write
metadata:
  version: "0.1"
  argument-hint: "[operation] [doc-or-dir] — operations: explode, tables, anchor, relations, verify"
  model: sonnet
  context: fork
---

## Purpose

graphify ingests prose with its **LLM semantic pass (Pass 3)**: Claude subagents read each chunk and
emit nodes/edges. A relation is tagged **`EXTRACTED` (confidence 1.0) only when it is stated directly
in the text**; otherwise it is `INFERRED` (0.55–0.95) or `AMBIGUOUS`. Two facts about *design docs*
make them different from the research-chunk corpus that `4dlab-wiki-prep` was built for:

1. **They are monolithic and hierarchical.** An HLD/DLD/LLD is one long file whose meaning lives in a
   parent→child tree (`System → Module → Schema → Field → Task-ID`). Fed whole, graphify's chunker
   splits on token budget and a child chunk (e.g. "§4.4 OBDLivePayload fields") loses the parent
   context ("this belongs to OBDLab"), so it is mis-attributed or dropped. The fix is to **explode by
   header and inject an anchor** so every chunk states its own lineage.
2. **Their logic hides in tables.** Design docs bury fields, bounds, and routing in grid tables. The
   LLM pass reads a clean bullet "feature block" as distinct properties but hallucinates on a dense
   ASCII grid. The fix is **table → entity block** conversion for the logic-bearing tables.

On top of that, design docs carry a small, sharp set of **architectural relations** that the
diagnostic graph actually routes on — and that the prose usually only implies. Make them explicit:

| Predicate | Means | Typical subject → object |
|---|---|---|
| `consumes` | a module reads a field on a live code path | `COMLab fault_atlas_router` consumes `obd_live_data.o2_failure_mode` |
| `mirrors_contract_in` | a doc/schema restates a boundary defined elsewhere | `OBDLivePayload` mirrors_contract_in `SEMANTIC_CONTRACT §4.4` |
| `supersedes` | a v2 doc replaces a v1 blueprint | `HLD_OBDLab v2.0` supersedes `OBDlab.md` |
| `verifies` | a BDD/test asserts a schema or rule | `BDD_OBDLab scenario "wideband offset"` verifies `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` |
| `owned_by` | a field's authoritative editor | `obd_live_data.*` owned_by `OBDLab` |
| `derived_from` | a value computed from another | `resolved_horizon` derived_from `euro_emission_category` |

> **What this skill deliberately does NOT do** (same honesty rules as the two sibling skills):
> - **No invented edges.** State only relations the doc actually supports; a `consumes` line must
>   name a *real, existing* code path (signal/noise rule). If the consumer is only proposed, label it
>   a proposal — never assert it as live.
> - **No edge stamping.** Never write `confidence: EXTRACTED, 1.0` into `graph.json`. The honest fix
>   is to make the relation explicit in the *text* and let graphify extract it.
> - **No content rewriting.** Exploding and anchoring are *structural* — the sourced prose, numeric
>   literals (with their wiki citations), and field semantics are copied verbatim into the chunks.

**Operations:**
- `explode`   — split the monolith into per-section files by header, mirroring the heading tree into a
                folder tree (`ingest_ready/<doc>/<section>.md`).
- `tables`    — convert logic-bearing tables (fields, bounds, routing, enum rosters) into bulleted
                entity blocks; leave narrative tables alone.
- `anchor`    — inject a `> **Context:**` lineage header at the top of every exploded chunk.
- `relations` — append a `## Graph relations (explicit)` block of architectural predicate lines.
- `verify`    — confirm coverage, no orphaned chunks, anchors present, no superseded docs in the set.

If no operation is given, run `explode → tables → anchor → relations → verify` in that order.

---

## Boundary — three prep skills, do not cross the streams

| | **4dlab-code-prep** | **4dlab-wiki-prep** | **THIS — 4dlab-doc-prep** |
|---|---|---|---|
| Input | `.py` source package | already-chunked `research/` wiki corpus | monolithic `.md` design doc (HLD/DLD/LLD/ADR/BDD/PRD) |
| graphify pass | Pass 1 — AST, offline | Pass 3 — LLM | Pass 3 — LLM |
| First problem | source legibility | implied links | **monolith + hierarchy + grid tables** |
| Prep lever | imports, `__all__`, types | explicit relation lines | explode + anchor + table→block, **then** architectural relation lines |
| Output | `graph/v2_code/` | `graph/v2_wiki/` | `graph/v2_docs/` |

The research-chunk corpus is *already* split and topic-local, so `4dlab-wiki-prep` skips straight to
relation lines. A design doc is **not** — feeding it to `4dlab-wiki-prep` whole is exactly the
mismatch that got graphify-ingestion of the docs deferred (HANDOFF 2026-06-10, TODO-4). Use this skill
for design docs; never run it on `.py` source (that is `4dlab-code-prep`).

---

## Step 0 — Resolve the target and gate readability

Accept a doc path or a folder of design docs. **Base root:** `/agent_workspace` (repo root).
Before touching anything, run the workspace **document readability gate** on every input (CLAUDE.md):

- no image placeholders (`grep -n '!\[\]\[' <file>` returns nothing);
- the Read tool returned the **whole** file (no "PARTIAL view" truncation);
- any referenced equations are present as text/LaTeX, not images.

On any failure: STOP, report the exact file and reason, do not work around it.

- Exclude:
  - OBDLab: `docs/OBDlab.md` (superseded), `docs/OBD_VOCABULARY.md` (vocab tier), generic stubs (`docs/ADR.md`, `docs/BDD.md`), owner/handoff notes.
  - GASLab: `docs/GAS_VOCABULARY.md` (vocab tier), `docs/audits/` (assessment artifacts).
  - DTCLab: `docs/DTC_VOCABULARY.md` (vocab tier), `docs/audits/` (assessment artifacts).
Confirm the target set excludes these before proceeding.

---

## Step 1 — `explode` (one topic per file, hierarchy → folders)

Don't let graphify guess where a topic ends. Physically split the doc on its `##` (and where a
section is large, `###`) headers, writing each section to its own file and mirroring the heading tree
into a folder tree so the path itself records lineage:

```text
ingest_ready/
  HLD_OBDLab/
    1_System_Overview.md
    3_Module_Decomposition/
      3.1_Translation_Layer.md
      3.2_Physics_Gates.md
    4_Boundary_Schemas/
      4.4_OBDLivePayload.md
```

Rules:
- **Split on headers, never on character count.** graphify still chunks Pass-3 input by
  `--token-budget`; header-splitting just guarantees each chunk is one coherent topic first.
- **Copy verbatim.** The section body — prose, numeric literals **with their wiki-citation
  comments**, field definitions — is moved unchanged. This is a move/copy, not a rewrite.
- **Name files after the header**, prefixed with the section number, spaces → underscores.
- **One source doc → one output subtree.** Never merge two docs into one tree.

A small splitter is acceptable here (header detection is deterministic). Keep it append-safe and have
it log every file it writes.

---

## Step 2 — `tables` (logic tables → entity blocks)

Convert only the **logic-bearing** tables — those that encode fields, bounds, enum rosters, or routing
rules. Each row becomes a labelled block whose properties the LLM reads as distinct facts.

Bad (grid the LLM turns to soup):

```text
| Field | Type | Bounds | Consumer |
|-------|------|--------|----------|
| total_trim_correction_delta | float | −254..+254 % | COMLab trim divergence |
```

Good (entity block):

```markdown
### Field: total_trim_correction_delta
- **Type**: float
- **Bounds**: −254..+254 %   <!-- wiki cite preserved verbatim if present -->
- **Owned by**: OBDLab
- **Consumed by**: COMLab trim-divergence check (fault_atlas_router)
```

Rules:
- **Preserve the citation comment** on any numeric literal exactly (`gaslab/`/`obdlab/` literals carry
  a wiki citation — never drop it).
- **Leave narrative tables alone** — a table that *explains* a concept, not one that encodes
  field/bound/routing rules, stays a table.
- Keep enum rosters as bullet lists of values so each value can become its own node.

---

## Step 3 — `anchor` (inject lineage context per chunk)

A chunk like "§3.2 Physics Gates" loses the fact that it belongs to OBDLab once it is separated.
Inject a context header at the very top of **every** exploded chunk:

```markdown
> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 3.2 Physics Gates ·
> Parent document: HLD_OBDLab.md · Boundary contract: SEMANTIC_CONTRACT §4.4

## 3.2 Physics Gates
...
```

Rules:
- Always name the **module** and the **parent document** — these are the two entities the extractor
  most often mis-attributes.
- Where the section restates a boundary schema, name the contract section it mirrors (this is the
  seed for a `mirrors_contract_in` edge in Step 4).
- The anchor is metadata *about* the chunk; it adds context, it never changes the section body.

---

## Step 4 — `relations` (architectural predicates, make them EXTRACTED)

Append one trailer block per chunk stating the architectural relations the section supports, using the
predicate table at the top:

```markdown
## Graph relations (explicit)

**HLD_OBDLab v2.0** SUPERSEDES **OBDlab.md**
**OBDLivePayload** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.4**
**COMLab fault_atlas_router** CONSUMES **obd_live_data.o2_failure_mode**
**obd_live_data.\*** OWNED_BY **OBDLab**
**BDD_OBDLab "wideband offset"** VERIFIES **O2FailureMode.WIDEBAND_OFFSET_CANDIDATE**
**resolved_horizon** DERIVED_FROM **euro_emission_category**
```

Rules that keep this on-spec:
- **Append-only.** Trailer is a pure append; the section body above it is untouched.
- **Every `consumes`/`verifies` line names a real, existing code path or test.** A field with no live
  consumer is an orphan and a signal/noise breach — do not write the edge; flag it for the architect.
- **Proposals stay proposals.** A field whose consumer is only *proposed* (in
  `comlab/config/proposals/`) is written with its proposed consumer and labelled as a proposal, not
  promoted to live.
- **Entities use canonical labels** — schema names, dotted enum values, and Task-IDs spelled exactly
  as the shipped code/contract spells them (grep before writing; never guess casing). Cross-check the
  `labels` conventions in `4dlab-wiki-prep` so doc and wiki graphs key the same node.

---

## Step 5 — `verify`

Confirm, across the prepared set:
- **Coverage:** every `##` section of each source doc produced exactly one chunk; report any section
  with no chunk (lost) or two (double-explode).
- **Anchors:** every chunk starts with a `> **Context:**` header naming module + parent document.
- **Relations:** every chunk has exactly one `## Graph relations (explicit)` block; zero empty
  blocks; report the total relation-line count by predicate.
- **No orphan edges:** every `CONSUMES`/`VERIFIES` object resolves to a real field/enum/code path
  (grep it); flag any that do not.
- **Exclusions honoured:** no chunk derives from a superseded blueprint or a duplicate (Step 0 list).
- **Citations intact:** numeric literals still carry their original wiki-citation comments.

Report counts and every failing chunk. Never "fix" by inventing content — flag for the architect.

---

## Output conventions

- Output tree: `graph/v2_docs/ingest_ready/<doc>/...` (separate from `v2_wiki/` and `v2_code/`).
- Section header for skill output: `--=={ 4dlab-doc-prep: DOC / OPERATION }==--`
- Always report per-doc coverage: sections found, chunks written, tables converted, relation lines.
- Never alter sourced content or numeric citations; never write to `graph.json`; never run graphify
  itself (that is `4dlab-graphify-run`).

## Relation reference (predicate vocabulary)

Design-doc predicates (most specific that fits): `consumes`, `mirrors_contract_in`, `supersedes`,
`verifies`, `owned_by`, `derived_from`, `routes_to`, `gated_by`, `enumerates`, `describes`. Reuse the
`4dlab-wiki-prep` domain verbs (`monitored_by`, `disambiguated_by`, …) where the doc carries genuine
diagnostic prose, so the doc graph and wiki graph share one vocabulary. graphify still only tags a
line EXTRACTED if the chunk's text supports it.

## Reference

- `labs/obdlab/docs/DocPrep.md` — the owner's source note (Hierarchical Markdown Transformation).
- `labs/obdlab/docs/HANDOFF_obdlab_docs_2026-06-10.md` — TODO-4, the deferral this skill closes;
  exclusion list (`OBDlab.md`, duplicate vocab).
- `_skills/graph/4dlab-wiki-prep/SKILL.md` and `4dlab-code-prep/SKILL.md` — the two sibling skills;
  share their honesty rules and canonical-label conventions.
- graphify pipeline + confidence tags — `https://github.com/safishamsi/graphify/blob/v8/docs/how-it-works.md`.
- Background on hierarchy-preserving KG ingestion: Neo4j knowledge-graph generation; document GraphRAG
  for structured/manufacturing docs (root→section→element node modelling) — see HANDOFF references.
