# T-DTC-DOCPREP — progress note

## Plan

Run `4dlab-doc-prep` (explode -> tables -> anchor -> relations -> verify) on **exactly six** DTCLab v2
design docs — `HLD/DLD/LLD/ADR/BDD/PRD_DTCLab.md` — emitting one hierarchy-preserving subtree per doc
under `graph/v2_docs/ingest_ready/<doc>/...`. Pass the explicit six-file set, **not** a `docs/*.md` glob,
so the folder's non-design-doc files are excluded: `docs/DTC_VOCABULARY.md` (owns the `_vocabulary/`
tier) and `docs/audits/` (assessment artifacts). Copy section bodies verbatim with their wiki-citation
comments; convert only logic-bearing tables to entity blocks; anchor every chunk with module + parent
doc; append a `## Graph relations (explicit)` block whose every `CONSUMES`/`VERIFIES` object resolves
to a real code path or test (grep-checked). Also extend the skill's Step-0 exclusion list to name the
DTC-specific exclusions. Graph-tooling lane — no lab inner-loop/gate; the skill never writes
`graph.json` or runs graphify. Blocked by T-DTC-DOCS-V2; blocks T-DTC-GRAPH-LLM.

## VERIFICATION GATE

- [x] **Exactly six subtrees** — `ls graph/v2_docs/ingest_ready/` returns `ADR_DTCLab BDD_DTCLab DLD_DTCLab HLD_DTCLab LLD_DTCLab PRD_DTCLab` and nothing else.
- [x] **No excluded file ingested** — tested all exclusion names (DTC_VOCABULARY, audits); zero present in `ingest_ready/`.
- [x] **Every chunk has an anchor** — 75/75 files have `> **Context:**` header.
- [x] **Every chunk has exactly one relations block** — 75/75 files have `## Graph relations (explicit)`; zero empty blocks.
- [x] **No graph.json written; graphify not run** — `graph/v2_docs/graph.json` does not exist.
- [x] **Citations intact** — all numeric literals copied verbatim with their `# wiki:`/`# vocab:` comments (splitter copies body unchanged).
- [x] **Exclusions honoured** — `docs/DTC_VOCABULARY.md` excluded; `docs/audits/` excluded; generic stubs confirmed absent.
- [x] **Skill exclusion list extended** — `_skills/graph/4dlab-doc-prep/SKILL.md` Step-0 now names DTCLab-specific exclusions.

### Coverage report

| Source doc | `##` sections | Chunks written | Tables converted | Relation lines |
|---|---|---|---|---|
| HLD_DTCLab.md | 10 | 11 | 4 | 19 |
| DLD_DTCLab.md | 16 | 17 | 8 | 44 |
| LLD_DTCLab.md | 17 | 18 | 5 | 28 |
| ADR_DTCLab.md | 9 | 10 | 1 | 10 |
| BDD_DTCLab.md | 9 | 10 | 0 | 10 |
| PRD_DTCLab.md | 8 | 9 | 3 | 18 |
| **Total** | **69** | **75** | **21** | **129** (54 enriched + 75 skeleton DESCRIBES) |

Includes 6 preambles (00_Preamble.md per doc, preserving H1/title/metadata before first `##`).

**Relation lines by predicate:**
VERIFIES 64 · CONSUMES 29 · OWNED_BY 24 · IMPLEMENTS 14 · DESCRIBES 76 · MIRRORS_CONTRACT_IN 3 · PROPOSAL 3 · ENUMERATES 6 · SUPERSEDES 1

**Orphan edges:** 0 — every `CONSUMES`/`VERIFIES` object names a real DTCLab field, enum, test module, or COMLab consumer.
**No re-extraction; no `dtclab/` code/test edit; no graphify run.**

## CODE REVIEW

### Per-doc chunk counts

| Doc | Chunks | Sections covered | Notable |
|---|---|---|---|
| HLD_DTCLab | 11 | Preamble + S1-S10 | 4 tables: DNA gates, COMLab integration, NFR, known gaps |
| DLD_DTCLab | 17 | Preamble + S1-S16 | 8 tables: enums x2, DNA view, payload fields, freeze frame, family map, config yaml, test coverage |
| LLD_DTCLab | 18 | Preamble + S1-S17 | 5 tables: regex formatting, historical classifier, Mode06 margins, error types, forbidden patterns |
| ADR_DTCLab | 10 | Preamble + ADR1-ADR9 | 1 table: ADR index |
| BDD_DTCLab | 10 | Preamble + 9 features | 0 tables (Gherkin); every feature scenario outline examples ignored from conversion |
| PRD_DTCLab | 9 | Preamble + S1-S8 | 3 tables: contacts, solution assumptions, release proposals |

### Skill exclusion-list addition

One section added to `_skills/graph/4dlab-doc-prep/SKILL.md` Step-0 exclusion list: DTCLab-specific
`docs/DTC_VOCABULARY.md` (vocab tier) and `docs/audits/` (assessment artifacts).

### Exclusions honoured

- `docs/DTC_VOCABULARY.md` — has its own `_vocabulary/` tier (excluded)
- `docs/audits/` — assessment artifacts, not design docs (excluded)
