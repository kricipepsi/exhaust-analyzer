# COMLab → Vault — PIPELINE PACK · START HERE

Read this first, every session, before any other action in the COM vault pack.
(Paste this file as message 1 of a fresh coder/author session.)

**Pack:** VAULT (COMLab tier) · **Lab:** `labs/comlab` · **Authored:** 2026-06-26 (architect, Cowork)
**Pipeline spec:** `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`
**Vault plan:** `Vault/VAULT_IMPLEMENTATION_PLAN.md`
**Driving skill:** `skill://4dlab-vault` (`_skills/graph/4dlab-vault/`)
**Template pack:** DTCLab (`DTC_VAULT_TASKS_START_HERE.md`) — the full-fresh-lab precedent COMLab mirrors.
**Readiness audit:** `Vault/tasks/COMLAB_VAULT_READINESS_AUDIT_2026-06-26.md` (Phase-0 gate PASS).

(Paths are relative to the workspace root `/agent_workspace` — the former `4DLabV2/` child is now the mount root.)

> **One rule above all (signal/noise):** nothing — no schema field, no graph edge, no vault
> frontmatter key — ships unless a **named, existing consumer** reads it on a real code path.
> "Future use" is not a consumer. A note with an empty `consumers` list is not ready to ship.

---

## 0. COMLab-specific paths — DO NOT copy OBDLab's paths blindly

COMLab shares GASLab/DTCLab's layout (wiki at `wiki/`, not `research/chunks/`). `build_lab_vault.py`
defaults to **OBDLab's layout** for any **unregistered** lab — and COMLab is unregistered today, so the
path fix (`T-COM-PATHS-1`) is a hard blocker on `T-COM-VAULT`.

| Corpus | OBD default (WRONG for COM) | **COMLab actual path** |
|---|---|---|
| code | `labs/<lab>/<lab>/` | `labs/comlab/comlab/` ✓ — 21 modules, ~6,200 LOC (`core/`, `schemas/`, `analytics/`, `observability/`, `projection.py`) |
| tests | `labs/<lab>/tests/` | `labs/comlab/tests/` ✓ — unit / e2e / integration / generative / regression + fixtures |
| wiki | `labs/<lab>/research/chunks/` | **`labs/comlab/wiki/`** — 15 chunks `00_index.md` … `14_sources_appendices.md` |
| docs | `labs/<lab>/docs/` | `labs/comlab/docs/` ✓ — **6 design docs** (HLD/DLD/LLD/BDD/PRD + `adr/` 11 records) + `Vocabulary/` + `CROSS_LAB_DEPENDENCIES.md` + `ARCHIVE/` |
| graph | `labs/<lab>/graphify-out/graph.json` (single) | **tiered** `labs/comlab/graph/v2_code|v2_tests/` (to be built; today only `graph/v1_baseline/` exists — **frozen**) |

`build_lab_vault.py` has **no `comlab` entry** in `LAB_SRC_PATHS`, so a COM build falls through to OBD's
`research/chunks` default and `sys.exit`s. **`T-COM-PATHS-1`** adds the one entry (wiki at `wiki/`, two
AST tiers) and the provenance-branch line, mirroring the `gaslab`/`dtclab` entries.

**Frozen canonical graph:** `graph/v1_baseline/` is the existing single graph. It is **canonical — never
re-extracted.** Phase-3 builds the **new** `v2_code` / `v2_tests` tier dirs only and leaves it byte-unchanged.

## 1. Scope trims applied to this pack (owner direction 2026-06-26)

- **Prose graphs TRIMMED ("skip graph testing") → mirror DTC/VIN/DNA.** The Pass-3 LLM prose graphs
  (`v2_wiki`, `v2_docs`) are **waived**; `T-COM-GRAPH-LLM` is authored only as a **waived, liftable**
  row that records the exact lift condition (a confirmed Pass-3 backend on the coder host). Phase-3 still
  runs the cheap, no-token, no-re-extraction **health-check** (`eval-*-graph` Part-A only) inline. The
  vault copies wiki/docs as raw `.md` + injected frontmatter — no prose graph — exactly as GAS/DTC did.
  *Viability note:* the LLM pass is technically proven (OBDLab + symptomlab built `v2_wiki`/`v2_docs`),
  but it is gated on an LLM backend/API key on the host and costs tokens; the trim avoids blocking the
  vault on an unverified external dependency. Liftable later if the owner confirms a backend (symptomlab
  precedent).
- **Registry EXCLUDED.** `labs/comlab/registry/` is a separate package with its **own** 3-skill bundle
  (`registry/docs/_registry_skills/`) and ledger, and its **F1 consolidation is an open owner-gated
  decision**. It is **out of this pack's scope** — it gets its own vault pack later. This pack migrates
  `comlab/comlab/` + `tests/` + `wiki/` + `docs/` only. (See §5.)
- **DOCS-V2 is DONE.** The 6 design docs were already reconciled to the shipped `comlab/` package
  (`COMLab_{HLD,DLD,LLD,PRD}.md` headed "v2.0 — as-built"; `COMLab_BDD.md` v1.0 baselined to v2 code; the
  `adr/` index has 11 Accepted records — all 2026-06-21). So `T-COM-DOCS-V2` ships `done`; it unblocks DOCPREP.
- **Code-clean is NOT done (full fresh-lab pack).** COMLab has no prior code audit, and the package is
  large (~6,200 LOC; `fault_atlas_router.py` alone is 2,204). `T-COM-CODE-CLEAN` is therefore **split into
  4 sub-tasks by subpackage** (A router/atlas, B schemas, C core-pipeline, D analytics/projection). This is
  the full ≈10–13-session path (guide §7.3), not OBDLab's trimmed docs-only path.
- **Tests are runtime-green but not type-clean.** `pytest` = **509 passed, 4 skipped** (skips are
  intentional phase-3 reservations), but `pyright tests/` reports **19 real errors** (missing ctor args,
  `None` fixtures, Optional member access). `T-COM-TESTS-GREEN` resolves those — real work, ships `pending`.

## 2. The chain (run in dependency order — one task per session)

```
PHASE 1  T-COM-CODE-CLEAN-A   codingskills + AST-legible: core/fault_atlas_router.py + fault_atlas_kg.py   coder
         T-COM-CODE-CLEAN-B   codingskills + AST-legible: schemas/ (ingestion, vocabulary, response, …)     coder
         T-COM-CODE-CLEAN-C   codingskills + AST-legible: rest of core/ (aggregator, perception, …)         coder
         T-COM-CODE-CLEAN-D   codingskills + AST-legible: analytics/ + projection.py + observability/        coder
         T-COM-TESTS-GREEN    whole tests/ tree green + type-clean (resolve 19 pyright errors) + meaningful  coder
         T-COM-DOCS-V2        reconcile 6 design docs to v2  ← DONE 2026-06-21                                author
              │
PHASE 2  T-COM-CODEPREP       4dlab-code-prep on comlab/comlab/   ← CODE-CLEAN-A/B/C/D                        coder
         T-COM-TESTPREP       4dlab-code-prep on tests/           ← TESTS-GREEN  (may fold into CODEPREP)     coder
         T-COM-WIKIPREP       4dlab-wiki-prep on wiki/            ← (wiki current)                            author
         T-COM-DOCPREP        4dlab-doc-prep on the 6 design docs ← DOCS-V2                                   author
              │
PHASE 3  T-COM-GRAPH-AST      graphify code+tests → graph/v2_code, v2_tests ← CODEPREP+TESTPREP              coder
         (T-COM-GRAPH-LLM     WAIVED — "skip graph testing"; prose graphs not built. Liftable — see file)
              │
PHASE 4  T-COM-PATHS-1        add comlab entry to LAB_SRC_PATHS (wiki/, two AST tiers)   ← (none)            coder
         T-COM-VAULT          vault-map.comlab.yaml + dry-run + build + bases ← GRAPH-AST + PATHS-1          author
```

The four corpora are independent until they converge at the vault, so within a phase the sessions run in
any order. **PATHS-1 has no corpus dependency** and can run any time before VAULT.

## 3. Pack ledger (source of truth — the next task is the first `pending` row whose Blocked-by are all `done`)

| ID | Task file | Status | Blocked by | Lane | Load skills (this task only) |
|---|---|---|---|---|---|
| T-COM-DOCS-V2 | `T-COM-DOCS-V2_reconcile_design_docs_to_v2.md` | done | — | author | — (author lane; reference only) |
| T-COM-CODE-CLEAN-A | `T-COM-CODE-CLEAN-A_router_atlas_legibility.md` | done | — | coder | comlab-python, comlab-verification-loop, comlab-code-review (+ codingskills passes) |
| T-COM-CODE-CLEAN-B | `T-COM-CODE-CLEAN-B_schemas_contract_legibility.md` | done | — | coder | comlab-python, comlab-verification-loop, comlab-code-review (+ codingskills passes) |
| T-COM-CODE-CLEAN-C | `T-COM-CODE-CLEAN-C_core_pipeline_legibility.md` | done | — | coder | comlab-python, comlab-verification-loop, comlab-code-review (+ codingskills passes) |
| T-COM-CODE-CLEAN-D | `T-COM-CODE-CLEAN-D_analytics_projection_legibility.md` | done | — | coder | comlab-python, comlab-verification-loop, comlab-code-review (+ codingskills passes) |
| T-COM-TESTS-GREEN | `T-COM-TESTS-GREEN_whole_tests_tree_green.md` | done | — | coder | comlab-python, comlab-verification-loop, comlab-code-review |
| T-COM-CODEPREP | `T-COM-CODEPREP_ast_legibility_audit_package.md` | done | CODE-CLEAN-A/B/C/D | coder | comlab-python, comlab-verification-loop, comlab-code-review, **4dlab-code-prep**, **comlab-vault-prep** |
| T-COM-TESTPREP | `T-COM-TESTPREP_ast_legibility_audit_tests.md` | done — folded into CODEPREP | TESTS-GREEN | coder | comlab-verification-loop, **4dlab-code-prep**, **comlab-vault-prep** |
| T-COM-WIKIPREP | `T-COM-WIKIPREP_explicit_relations_wiki.md` | done | — | author | comlab-verification-loop, **4dlab-wiki-prep**, **comlab-vault-prep** |
| T-COM-DOCPREP | `T-COM-DOCPREP_doc_prep_design_docs.md` | done | DOCS-V2 | author | comlab-verification-loop, **4dlab-doc-prep**, **comlab-vault-prep** |
| T-COM-GRAPH-AST | `T-COM-GRAPH-AST_graphify_code_and_tests.md` | done — 2026-06-28 (architect, owner-delegated; gate clean, both tiers GOOD) | CODEPREP, TESTPREP | coder/graph | **4dlab-graphify-run**, **eval-code-graph**, comlab-verification-loop (frozen-graph guard) |
| T-COM-GRAPH-LLM | `T-COM-GRAPH-LLM_prose_graphs_waived.md` | waived | WIKIPREP, DOCPREP | — | n/a — waived (lift → 4dlab-graphify-run + eval-wiki-graph/eval-doc-graph) |
| T-COM-PATHS-1 | `T-COM-PATHS-1_register_comlab_source_paths.md` | done — 2026-06-28 (LAB_SRC_PATHS comlab entry + provenance waiver branch; obd/dtc dry-runs byte-unchanged) | — | coder/vault | **4dlab-vault**, comlab-python |
| T-COM-VAULT | `T-COM-VAULT_build_comlab_vault.md` | done — 2026-06-28 (12 framed notes, health 91/91, graphs byte-unchanged, idempotent; SEMANTIC_CONTRACT homed in _vocabulary/) — **closes the COMLab vault pack** | T-COM-GRAPH-AST, T-COM-PATHS-1 | author/vault | **4dlab-vault**, **comlab-vault-prep**, comlab-verification-loop |

**Each task loads ONLY the skills on its row** (the task file's `Load skills:` line is authoritative — this
table is the at-a-glance map). The 3 mandatory COMLab skills (`comlab-python`, `comlab-verification-loop`,
`comlab-code-review`) gate the **coder-lane** tasks; author/graph/vault-lane tasks load the matching
pipeline skill + the COMLab companion only. `comlab-vault-prep` (on-demand, authored 2026-06-26) gates the
four Phase-2 prep tasks. **Do not load the registry trio** (`registry/docs/_registry_skills/`) — the
registry is out of this pack's scope.

## 4. Non-negotiables (carry from COMLab + Vault rules)

- **Python 3.14 ONLY** via the shared venv `/agent_workspace/.venv-wired` —
  `source /agent_workspace/.venv-wired/bin/activate` (or call `/agent_workspace/.venv-wired/bin/python`
  directly; never bare `python`/`python3`, the system default is 3.12). Coder inner loop after every edit
  (run from `labs/comlab/`): `ruff check .` → `pyright comlab/` → `python -m pytest -x -q`. No version
  mixing; purge stale `__pycache__` if a `.pyc` shadows an edit. (There is **no** `.sandbox-py` on Linux.)
- **graphify is a SANCTIONED step only inside `T-COM-GRAPH-AST`**, scoped to a specific package/dir,
  building the **new** tier dirs. It is **forbidden** as a side-effect of any other task and **never**
  re-extracts the frozen `graph/v1_baseline/`. The KG pre-step resolves to **SKIP** for every other task.
- **Fusion spine, built LAST.** COMLab consumes the four labs' **verdicts**
  (`schemas/ingestion.py::OrchestratorInboundRequest`), never raw sensors. Its vault notes' downstream
  consumers are **COMLab-internal** (analytics / fault-atlas routing) or **the app layer**
  (`apps/4DLabWired/` `from comlab import LabPipelineAggregator`; `apps/ui/`) — **never another lab**.
- **`consumers` is architect-named, never auto-derived from the graph.** Empty list = not ready → leave `plain:`.
- **Signal/noise at the edge:** every `CONSUMES`/`VERIFIES` line a prep skill appends must name a real,
  existing code path or test. Proposals (`wiki/13_proposals_register.md`; `comlab/config/proposals/` —
  `COMLab-DELTA`, `EP-*`) and default-off flag-gated capability stay labelled proposals — never promoted.
- **No cross-lab Python imports** (mirror types locally). **Numeric literals carry a wiki cite** (`# wiki: §…`).
  Reports in `.md` only; **archive, never delete**.
- **Folder convention:** `wiki/` = lab wiki only; vocabulary/contract → `docs/Vocabulary/`; design docs → `docs/`.
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/<id>.md`
  (open with the confirmed `## Plan`), flip the ledger row to `done`, then STOP. Coder lane runs the inner
  loop; the prep/graph/vault lanes are graph-/vault-tooling (no lab inner-loop) per each task's role note.

## 5. Follow-ups for the owner (not authored as pack tasks)

- **Registry vault pack (separate workstream).** `labs/comlab/registry/` is excluded here. Onboarding it
  to the vault is its own pipeline run (own `_registry_skills/`, own `vault-map.registry.yaml`), and is
  blocked on the **F1 registry-consolidation** decision (`global_fault_registry.json` ↔ REG-V2 shim,
  `wiki/12 §CONCEPT_PHASE0`) — an owner/GATE_DATA call, not a mechanical migration. Author after F1 lands.
- **Prose-graph lift.** If the owner confirms a Pass-3 LLM backend on the coder host, lift the
  `T-COM-GRAPH-LLM` waiver (build `v2_wiki`/`v2_docs`, change `required_graph_tiers` to all four in the
  `comlab` `LAB_SRC_PATHS` entry) — the symptomlab precedent. The Phase-2 wiki/doc prep already runs, so
  only the graphify + eval step is added.
- **Wiki scope spot-check (WIKIPREP).** `wiki/03_vehicle_dna_pruning.md:52` references an `SAI stuck on`
  enable (`ERR-LC-007`). GPF/LSPI/SAI are marked **out of scope** in `COMLab_PRD.md §`/`HLD §` (1990–2010
  Euro 1–5). Confirm the SAI line is an in-era residual (SAI was fitted on Euro 2–3 cars) and not a
  2010–2020 perk leak; if a leak, route a one-line wiki fix (architect out-of-band), not a code change.
- A COMLab-vault-pack pointer is **not** added to `/agent_workspace/CLAUDE.md` — this pack is a self-contained
  paste-doc started from this file, exactly like its GAS/DTC/VIN/DNA siblings in `Vault/tasks/`.
