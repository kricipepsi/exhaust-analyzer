# SymptomLab Graph — Progress Ledger

**Pack:** `planning\symptomlab_graph\`
**Bootstrap:** `SYMPTOMLAB_GRAPH_START_HERE.md` (paste as message 1 of each session)
**Tasks dir:** `planning\symptomlab_graph\tasks\`
**Guide:** `planning\LAB_TO_VAULT_PIPELINE_GUIDE.md` · **Manifest:** `GRAPH_MANIFEST.md`
**Mode:** LITE · **Last updated:** 2026-06-12

Only file `START_HERE.md` reads to find the next task. Keep under ~120 lines.
Bulk verification write-ups go in `tasks\progress_notes\<task-id>.md`, not here.

**Scope (owner decisions):** code-clean DONE (no task) · AST tiers `v2_code`+`v2_tests` DONE
(T-SYMGRAPH-1..4). **Pass-3 skip LIFTED 2026-06-12** — owner authorised the canonical-wiki
vault-mirror track. Wiki is now **canonical, not reference-only** (the old `kg_ingestion: none`
rested on a false "no numeric literals" premise; `dnalab/research/DNAresearch.md` refutes it).
Priors/chemistry/trust-ceiling have **no live symptomlab consumer** → ship as a **PROPOSAL**
(consumer = COMLab `FaultAtlasRouter`) in the existing registry
`labs/comlab/comlab/config/proposals/entries.yaml`, never in the live wiki. Most is already
registered: `COMLab-A` (catalog routing) + `COMLab-B` (load_state + 65% trust-ceiling);
WIKI-AUTHOR only **extends** it with the missing prior-band + chemistry-footprint entries.

---

## Task log

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-SYMGRAPH-1 | `tasks/T-SYMGRAPH-1_tests_green_confirm.md` | done | — | 2026-06-12 | (session) | pytest green; 5 unit modules mapped to rules | confirm suite green + meaningful |
| T-SYMGRAPH-2 | `tasks/T-SYMGRAPH-2_code_prep_audit.md` | done | — | 2026-06-12 | (session) | code-prep 0 violations; inner loop green | 4dlab-code-prep on package |
| T-SYMGRAPH-3 | `tasks/T-SYMGRAPH-3_test_prep_audit.md` | done | T-SYMGRAPH-1 | 2026-06-12 | (session) | tests code-prep 0 violations; pytest green | 4dlab-code-prep on tests/ |
| T-SYMGRAPH-4 | `tasks/T-SYMGRAPH-4_graphify_ast_tiers.md` | done | T-SYMGRAPH-2, T-SYMGRAPH-3 | 2026-06-12 | (session) | v2_code + v2_tests built, both GOOD, 0 collateral | **KG-lane**: builds v2_code + v2_tests |
| T-SYMGRAPH-WIKI-AUTHOR | `tasks/T-SYMGRAPH-WIKI-AUTHOR_build_wiki_corpus.md` | done | — | 2026-06-12 | (session) | live/proposal grep clean; catalog matches YAML (21 pairs); kg_ingestion=extract; COMLab-F/G added, A/B intact | 4 live notes + index rewrite + COMLab-F/G; 21-pair (owner: oil live); AnswerSymLab.md ingested |
| T-SYMGRAPH-WIKIPREP | `tasks/T-SYMGRAPH-WIKIPREP_wiki_prep_audit.md` | done | T-SYMGRAPH-WIKI-AUTHOR | 2026-06-12 | (session) | wiki-prep verify clean; all CONSUMES/VERIFIES targets resolve; 0 orphans; 0 collateral | 4dlab-wiki-prep relations+labels+roster+verify on 4 notes |
| T-SYMGRAPH-DOCPREP | `tasks/T-SYMGRAPH-DOCPREP_doc_prep_design_docs.md` | done | — | 2026-06-12 | (session) | doc-prep verify clean; 47 chunks (6 docs), anchors+relations present, 35 edges all resolve, vocab excluded | 4dlab-doc-prep on 6 v2 docs (excl. vocab); docs already v2 |
| T-SYMGRAPH-LLM | `tasks/T-SYMGRAPH-LLM_graphify_wiki_docs.md` | done | T-SYMGRAPH-WIKIPREP, T-SYMGRAPH-DOCPREP | 2026-06-12 | (session) | v2_wiki (109n/123e, GOOD) + v2_docs (78n/169e, GOOD), both EXTRACTED-dominant, 4 arch predicates present, 0 collateral | **KG-lane** (token cost): builds v2_wiki + v2_docs |
| T-SYMGRAPH-VAULT | `tasks/T-SYMGRAPH-VAULT_build_symptomlab_vault.md` | done | T-SYMGRAPH-LLM | 2026-06-12 | (session) | 4 tiers copied, 9 framed notes all w/ named consumer, vocab built, no graph.json in vault, 0 graph collateral; health gate 58/58 PASS | vault-map + build 4 tiers + SYMPTOM_VOCABULARY; FU-5 script path entry added |

**Status values:** `pending` · `in_progress` · `done` · `blocked`
**Run order (AST track, done):** 1∥2 → 3 (needs 1) → 4 (needs 2+3).
**Run order (vault-mirror track):** WIKI-AUTHOR → WIKIPREP; DOCPREP independent; LLM needs
WIKIPREP+DOCPREP; VAULT needs LLM (+ AST tiers from T-SYMGRAPH-4). WIKI-AUTHOR may wait on the
owner's supplemental research (`WIKI_COVERAGE_RESEARCH_PROMPT.md`) for full wiki coverage.

---

## Unplanned follow-ups

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| FU-1 | WIKI-AUTHOR authoring | `entries.yaml` COMLab-A/B/C `source:` paths point to `labs/dnalab/docs/research/DNAresearch.md`; actual file is `labs/dnalab/research/DNAresearch.md` (no `docs/`) — stale path | open |
| FU-2 | WIKI-AUTHOR exec | Task file text says "18-pair (6 tier_1)" but live code enforces 21 pairs / 7 tier_1 (`oil_consumption`). Wiki authored to mirror code (21) per owner confirm + code-is-truth rule; task file prose still reads 18 — fix on next edit of that file. | open |
| FU-3 | WIKI-AUTHOR exec | `occurs_during` context modifiers (cold_only/hot_only promotions, in DNAresearch/AnswerSymLab) have no registry entry; COMLab-B covers `load_state` only. Candidate COMLab-B extension or new proposal entry. | open |
| FU-4 | DOCPREP currency confirm | All 6 docs describe 18-pair invariant; code enforces 21 pairs (`oil_consumption` 7th tier_1 landed). Doc string in `models.py:9` also stale (says 18). Docs need refresh to 21. | open |
| FU-5 | VAULT exec | `build_lab_vault.py` `LAB_SRC_PATHS` had no `symptomlab` entry (only obdlab/gaslab/dtclab) → defaulted to OBDLab `research/chunks` layout and aborted on eligibility. No `T-SYMGRAPH-PATHS` task existed (DTC had `T-DTC-PATHS-1`). Added a 4-line entry (`wiki_subpath: wiki`, 4 tiers required) mirroring gaslab/dtclab; no logic change. Architect gap — confirm the in-task script edit is acceptable. | open |

---

## Vault-mirror track (ACTIVE — Pass-3 skip lifted 2026-06-12)

The four would-be parked tasks are now authored full task files (above), **plus** a new
Phase-1 `T-SYMGRAPH-WIKI-AUTHOR` (the parked plan assumed the wiki was already a corpus; it was
a single reference-only index, so the corpus must be authored first). Reconciliation vs the old
parked plan: DOCS-V2 reconcile is **not** a task — the 6 docs are already v2 (currency-confirm
folded into DOCPREP). The wiki half of LLM is **kept** (wiki is now canonical), not dropped.

---

## Architect-level out-of-band patches

| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-12 | (pack) | authored `symptomlab_graph` pack from the graph audit | symptomlab had no build tiers (`GRAPH_MANIFEST.md` §4) |
| 2026-06-12 | (pack) | authored vault-mirror track (5 task files) + lifted Pass-3 skip; wiki reclassified canonical | owner go-ahead; `DNAresearch.md` refutes the reference-only premise |
