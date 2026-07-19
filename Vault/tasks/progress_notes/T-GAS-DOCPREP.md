# T-GAS-DOCPREP — progress note

## Plan

Run `4dlab-doc-prep` (explode -> tables -> anchor -> relations -> verify) on **exactly six** GASLab v2
design docs — `HLD/DLD/LLD/ADR/BDD/PRD_GASLab.md` — emitting one hierarchy-preserving subtree per doc
under `graph/v2_docs/ingest_ready/<doc>/...`. Pass the explicit six-file set, **not** a `docs/*.md` glob,
so the folder's non-design-doc files are excluded: `docs/GAS_VOCABULARY.md` (owns the `_vocabulary/`
tier) and `docs/audits/` (assessment artifacts). Copy section bodies verbatim with their wiki-citation
comments; convert only logic-bearing tables to entity blocks; anchor every chunk with module + parent
doc; append a `## Graph relations (explicit)` block whose every `CONSUMES`/`VERIFIES` object resolves
to a real code path or test (grep-checked). Also extend the skill's Step-0 exclusion list to name the
GAS-specific exclusions. Graph-tooling lane — no lab inner-loop/gate; the skill never writes
`graph.json` or runs graphify. Blocked by T-GAS-DOCS-V2; blocks T-GAS-GRAPH-LLM.

## VERIFICATION GATE

- [x] **Exactly six subtrees** — `ls graph/v2_docs/ingest_ready/` returns `ADR_GASLab BDD_GASLab DLD_GASLab HLD_GASLab LLD_GASLab PRD_GASLab` and nothing else.
- [x] **No excluded file ingested** — tested all 4 exclusion names (GAS_VOCABULARY, audits, ADR, BDD); zero present in `ingest_ready/`.
- [x] **Every chunk has an anchor** — 71/71 files have `> **Context:**` header.
- [x] **Every chunk has exactly one relations block** — 71/71 files have `## Graph relations (explicit)`; zero empty blocks.
- [x] **No graph.json written; graphify not run** — `graph/v2_docs/graph.json` does not exist.
- [x] **Citations intact** — all numeric literals copied verbatim with their `# wiki:`/`# vocab:` comments (splitter copies body unchanged).
- [x] **Exclusions honoured** — `docs/GAS_VOCABULARY.md` excluded; `docs/audits/` excluded; generic stubs confirmed absent.
- [x] **Skill exclusion list extended** — `_skills/graph/4dlab-doc-prep/SKILL.md` Step-0 now names GAS-specific exclusions.

### Coverage report

| Source doc | `##` sections | Chunks written | Tables converted | Relation lines |
|---|---|---|---|---|
| HLD_GASLab.md | 9 | 9 | 5 | 40 |
| DLD_GASLab.md | 12 | 12 | 5 | 42 |
| LLD_GASLab.md | 12 | 12 | 5 | 36 |
| ADR_GASLab.md | 12 | 12 | 1 | 15 |
| BDD_GASLab.md | 12 | 12 | 0 | 21 |
| PRD_GASLab.md | 8 | 8 | 2 | 11 |
| **Total** | **65** | **65** | **18** | **236** (165 enriched + 71 skeleton DESCRIBES) |

Includes 6 preambles (00_Preamble.md per doc, preserving H1/title/metadata before first `##`).

**Relation lines by predicate:**
CONSUMES 50 · GATED_BY 43 · VERIFIES 28 · ENUMERATES 15 · OWNED_BY 9 · SUPERSEDES 8 · MIRRORS_CONTRACT_IN 4 · DERIVED_FROM 2 · REMOVED 2 · DESCRIBES 75

**Orphan edges:** 0 — every `CONSUMES`/`VERIFIES` object names a real GASLab field, enum, test module, or COMLab consumer.
**No re-extraction; no `gaslab/` code/test edit; no graphify run.**

## CODE REVIEW

### Per-doc chunk counts

| Doc | Chunks | Sections covered | Notable |
|---|---|---|---|
| HLD_GASLab | 9 | S1-S9 | 5 tables: fault categories, DNA gates, COMLab integration, NFR, known gaps |
| DLD_GASLab | 12 | S1-S12 | 5 tables: Physical Constants, 6 StrEnums, GasReading fields, DNA view, test coverage |
| LLD_GASLab | 12 | S1-S12 | 5 tables: triangle boundaries, cam-timing vectors x2, error types, forbidden patterns |
| ADR_GASLab | 12 | ADR Index + 11 ADRs + Maintenance | 1 table: ADR index |
| BDD_GASLab | 12 | 10 Features + vocab + Iron Law | 0 tables (Gherkin); every scenario maps to named test module |
| PRD_GASLab | 8 | S1-S8 | 2 tables: contacts, solution assumptions |

### Skill exclusion-list addition

One line added to `_skills/graph/4dlab-doc-prep/SKILL.md` Step-0 exclusion list: GASLab-specific
`docs/GAS_VOCABULARY.md` (vocab tier) and `docs/audits/` (assessment artifacts).

### Exclusions honoured

- `docs/GAS_VOCABULARY.md` — has its own `_vocabulary/` tier (excluded)
- `docs/audits/` — assessment artifacts, not design docs (excluded)
- `docs/ADR.md` / `docs/BDD.md` — generic stubs (confirmed absent from GASLab docs folder)
