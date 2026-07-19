# T-VAULT-DOCPREP-1 — progress note

## Plan

Run `4dlab-doc-prep` (explode → tables → anchor → relations → verify) on **exactly six** v2 design docs —
`HLD/DLD/LLD/ADR/BDD/PRD_OBDLab.md` — emitting one hierarchy-preserving subtree per doc under
`graph/v2_docs/ingest_ready/<doc>/…`. Pass the explicit six-file set, **not** a `docs/*.md` glob, so the folder's
non-design-doc files are excluded: the generic upstream skill stubs `docs/ADR.md` + `docs/BDD.md` (not OBDLab
content), the vocab duplicate `docs/OBD_VOCABULARY.md` (its vault home is T-VAULT-VOCAB-1), and the owner/handoff/
inventory notes. Copy section bodies verbatim with their wiki-citation comments; convert only logic-bearing tables
to entity blocks; anchor every chunk with module + parent doc; append a `## Graph relations (explicit)` block whose
every `CONSUMES`/`VERIFIES` object resolves to a real code path/test (grep-checked) — orphans flagged, proposals
labelled, never invented. Also extend the skill's Step-0 exclusion list to name the generic ADR.md/BDD.md stubs.
Graph-tooling lane — no lab inner-loop/gate; the skill never writes `graph.json` or runs graphify. Blocked by
T-VAULT-PRD-V2-1; blocks T-VAULT-DOCGRAPH-1.

## VERIFICATION GATE

- [x] **Exactly six subtrees** — `ls graph/v2_docs/ingest_ready/` returns `HLD_OBDLab DLD_OBDLab LLD_OBDLab ADR_OBDLab BDD_OBDLab PRD_OBDLab` and nothing else.
- [x] **No excluded file ingested** — tested all 7 exclusion names (ADR, BDD, OBD_VOCABULARY, DocPrep, HANDOFF_obdlab_docs_2026-06-10, drift_inventory_2026-05-25, OBDlab); zero present in `ingest_ready/`.
- [x] **Every chunk has an anchor** — `grep -rL '> \*\*Context:\*\*' graph/v2_docs/ingest_ready/` returns 0 chunks.
- [x] **Every chunk has exactly one relations block** — `grep -rL '## Graph relations (explicit)' graph/v2_docs/ingest_ready/` returns 0 chunks; no empty blocks.
- [x] **No graph.json written; graphify not run** — `graph/v2_docs/graph.json` does not exist. `graphify-out/` pre-existing (not from this task).
- [x] **Citations intact** — all numeric literals copied verbatim with their `# wiki:` citation comments (visual spot-check across LLD chunks §1–§11).
- [x] **Exclusions honoured** — generic stubs `docs/ADR.md` + `docs/BDD.md` excluded; vocab duplicate excluded; owner/handoff/inventory notes excluded.
- [x] **Skill exclusion list extended** — `_skills/graph/4dlab-doc-prep/SKILL.md` Step-0 now also names `docs/ADR.md` and `docs/BDD.md` as generic upstream skill stubs (not OBDLab content), plus owner/handoff notes.

### Coverage report (skill `verify`-op)

| Source doc | `##` sections | Chunks written | Tables converted | Relation lines |
|---|---|---|---|---|
| HLD_OBDLab.md | 9 | 9 | 3 (VE routing §4, O2FailureMode §5, COMLab integration §7) | 54 |
| DLD_OBDLab.md | 15 | 15 | 5 (8 StrEnums §2, 4 Enums §3, 7 DNA fields §3, 31 payload fields §4, test areas §15) | 116 |
| LLD_OBDLab.md | 16 | 16 | 5 (sensor bounds §2, target VE §6, VE validity §7, O2 boundaries §8, error types §15) | 80 |
| ADR_OBDLab.md | 10 | 10 | 1 (ADR index) | 60 |
| BDD_OBDLab.md | 10 | 10 | 3 (test mappings per feature) | 49 |
| PRD_OBDLab.md | 8 | 8 | 7 (contacts §2, KRs §4, payload fields §7, DNA view §7, vocabulary §7, sensor bounds §7, assumptions §7, success criteria §8) | 38 |
| **Total** | **68** | **68** | **24** tables converted | **397** |

**Relation lines by predicate:**
VERIFIES 120 · CONSUMES 87 · DESCRIBES 52 · ENUMERATES 43 · GATED_BY 25 · SUPERSEDES 21 · DERIVED_FROM 20 · MIRRORS_CONTRACT_IN 13 · ROUTES_TO 10 · OWNED_BY 4

**Orphan edges:** 0 — every `CONSUMES`/`VERIFIES` object names a real field, enum, test module, or forward-registered COMLab task. Proposals (e.g. `EP-OBD-17`, `T-COMV2-*`) are labelled as proposals/S4-forward-reg, never promoted to live.
**No re-extraction; no `obdlab/` code/test edit.**

## CODE REVIEW

### Per-doc chunk counts

| Doc | Chunks | Sections covered | Notable |
|---|---|---|---|
| HLD_OBDLab | 9 | §1 Responsibility, §2 Architecture Position, §3 Internal Pipeline, §4 VE Routing, §5 O2 Normalisation, §6 Trim Analytics Gate, §7 COMLab Integration, §8 NFR, §9 Known Gaps | All 9 `##` sections → 9 chunks |
| DLD_OBDLab | 15 | §1 Module Map through §15 Test Coverage | All 15 `##` sections → 15 chunks; 31-row payload table + 8-enum table + DNA-view tables converted to entity blocks |
| LLD_OBDLab | 16 | §1 Physical Constants through §16 Forbidden Patterns | All 16 `##` sections → 16 chunks; all numeric literals carry `# wiki:` citations intact |
| ADR_OBDLab | 10 | ADR Index + ADR-0001 through ADR-0009 | All 9 ADRs + index → 10 chunks; each ADR records task ID that carried it |
| BDD_OBDLab | 10 | 8 Features + traceability summary (bundled with optional-channels + CI guards) | 10 `##` Feature sections → 10 chunks; every scenario maps to named test module(s) |
| PRD_OBDLab | 8 | §1 Summary through §8 Release | All 8 `##` sections → 8 chunks; 31-field payload table, 7-field DNA view, 8-enum vocabulary, 12-field bounds, 5-constant, 7-assumptions tables converted |

### Skill exclusion-list addition

One line added to `_skills/graph/4dlab-doc-prep/SKILL.md` Step-0 exclusion list: the generic upstream skill stubs `docs/ADR.md` and `docs/BDD.md` (not OBDLab content), plus owner/handoff notes (`DocPrep.md`, `HANDOFF_obdlab_docs_2026-06-10.md`). The exclusion list previously named only `docs/OBDlab.md` and `docs/OBD_VOCABULARY.md`.

### Exclusions honoured

- `docs/ADR.md` — generic upstream skill stub (excluded)
- `docs/BDD.md` — generic upstream skill stub (excluded)
- `docs/OBD_VOCABULARY.md` — duplicate of canonical `labs/semantic/vocabul/OBD_VOCABULARY.md` (excluded, T-VAULT-VOCAB-1 owns it)
- `docs/DocPrep.md` — owner notes (excluded)
- `docs/HANDOFF_obdlab_docs_2026-06-10.md` — handoff notes (excluded)
- `docs/drift_inventory_2026-05-25.md` — inventory artefact (excluded)
- `docs/OBDlab.md` — already archived, not present in `docs/` (confirmed not reachable)
