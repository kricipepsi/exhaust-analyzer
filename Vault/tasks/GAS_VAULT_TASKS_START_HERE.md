# GASLab → Vault — PIPELINE PACK · START HERE

Read this first, every session, before any other action in the GAS vault pack.

**Pack:** VAULT (GASLab tier) · **Lab:** `labs/gaslab` · **Authored:** 2026-06-10 (architect)
**Pipeline spec:** `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`
**Vault plan:** `Vault/VAULT_IMPLEMENTATION_PLAN.md`
**Driving skill:** `_skills/graph/4dlab-vault/`

> **One rule above all (signal/noise):** nothing — no schema field, no graph edge, no vault
> frontmatter key — ships unless a **named, existing consumer** reads it on a real code path.
> "Future use" is not a consumer. A note with an empty `consumers` list is not ready to ship.

---

## 0. GASLab-specific paths — DO NOT copy OBDLab's paths blindly

The pipeline guide and `build_lab_vault.py` were written against **OBDLab**, whose wiki lives at
`research/chunks/` and whose graph is at `graphify-out/graph.json`. **GASLab is laid out
differently** — this is the single biggest trap in this pack:

| Corpus | Pipeline/OBD path (WRONG for GAS) | **GASLab actual path** |
|---|---|---|
| wiki | `labs/<lab>/research/chunks/` | **`labs/gaslab/wiki/`** (12 chunk files + `00_index.md` + `CHANGE_v2.1_timing_taxonomy.md`) |
| graph | `labs/<lab>/graphify-out/graph.json` (single) | **four-tier** `labs/gaslab/graph/v2_code|v2_tests|v2_wiki|v2_docs/` (to be built; today only `graph/v2_current/` + `graph/v1_baseline/`) |
| docs | `labs/<lab>/docs/` | same — `labs/gaslab/docs/` (6 design docs + `GAS_VOCABULARY.md` + `audits/`) ✓ |
| code | `labs/<lab>/<lab>/` | same — `labs/gaslab/gaslab/` ✓ |
| tests | `labs/<lab>/tests/` | same — `labs/gaslab/tests/` ✓ |

`build_lab_vault.py` lines 195/197/237 hardcode `research/chunks` + `graphify-out/graph.json`, so
its eligibility check would **fail outright on GAS**. **T-GAS-PATHS-1** parametrizes those per-lab
source paths and is a hard blocker on **T-GAS-VAULT**. Wherever a task names a wiki path, it is
`labs/gaslab/wiki/` — never `research/chunks/`.

## 1. Scope trims applied to this pack (owner direction 2026-06-10)

- **Code-clean / code-review is DONE.** The codingskills code audit ran — see
  `labs/gaslab/docs/audits/AUDIT_2026-06-10_gaslab_state.md` (ruff/pyright clean, 207 core tests
  green, isolation honoured). So **no `T-GAS-CODE-CLEAN`** is authored. The audit's open items
  (AUD-1..7) are referenced where they touch a pipeline corpus (notably AUD-1 → T-GAS-TESTS-GREEN).
- **Code-prep STAYS.** `4dlab-code-prep` is the AST-legibility audit for graphify — a different
  step from the code review — so `T-GAS-CODEPREP` / `T-GAS-TESTPREP` remain in the pack.
- **Graph review SKIPPED for now.** The Pass-3 LLM cross-check tier (the OBDLab
  `T-VAULT-DOCGRAPH-2 / WIKIGRAPH-1 / CODEGRAPH-1` equivalents) is **not authored**. Phase-3 tasks
  still run the cheap, no-token, no-re-extraction **health-check** (`eval-*-graph --health-only`)
  inline — that is build verification, not the gated cross-check.

## 2. The chain (run in dependency order — one task per session)

```
PHASE 1  T-GAS-TESTS-GREEN   whole tests/ tree green+meaningful (fix AUD-1 harness wiring)   coder
         T-GAS-DOCS-V2       reconcile ADR+BDD to v2.1 baseline; confirm design-doc parity   author
              │
PHASE 2  T-GAS-CODEPREP      4dlab-code-prep on labs/gaslab/gaslab/        ← (none)          coder
         T-GAS-TESTPREP      4dlab-code-prep on labs/gaslab/tests/         ← TESTS-GREEN     coder
         T-GAS-WIKIPREP      4dlab-wiki-prep on labs/gaslab/wiki/          ← (wiki current)  author
         T-GAS-DOCPREP       4dlab-doc-prep on the 6 design docs           ← DOCS-V2         author
              │
PHASE 3  T-GAS-GRAPH-AST     graphify code+tests → graph/v2_code, v2_tests ← CODEPREP+TESTPREP
         T-GAS-GRAPH-LLM     waived by owner direction; Phase-2 wiki/doc prep is sufficient
              │
PHASE 4  T-GAS-PATHS-1       parametrize build_lab_vault.py per-lab paths  ← (none)          coder
         T-GAS-VAULT         vault-map.gaslab.yaml + dry-run + build + bases ← AST graphs + PATHS-1
```

The four corpora are independent until they converge at the vault, so within a phase the sessions
run in any order. **PATHS-1 has no corpus dependency** and can run any time before VAULT.

## 3. Pack ledger (source of truth — the next task is the first `pending` row whose Blocked-by are all `done`)

| ID | Task file | Status | Blocked by | Lane | Notes |
|---|---|---|---|---|---|
| T-GAS-TESTS-GREEN | `T-GAS-TESTS-GREEN_whole_tests_tree_green.md` | done | — | coder | fix AUD-1 harness import wiring; AUD-2 slow-tier decision |
| T-GAS-DOCS-V2 | `T-GAS-DOCS-V2_reconcile_adr_bdd_to_v2.md` | done | — | author | ADR/BDD remain doc version 1.0 by owner direction; baseline/content reconciled to GASLab v2.1; HLD/DLD/LLD/PRD parity confirmed |
| T-GAS-CODEPREP | `T-GAS-CODEPREP_ast_legibility_audit_package.md` | done | — | coder | 4dlab-code-prep probe→audit→report on `gaslab/` |
| T-GAS-TESTPREP | `T-GAS-TESTPREP_ast_legibility_audit_tests.md` | void — folded into T-GAS-CODEPREP | T-GAS-TESTS-GREEN | coder | zero edits needed (tree already clean); spot-confirm table in progress note |
| T-GAS-WIKIPREP | `T-GAS-WIKIPREP_explicit_relations_wiki.md` | done | — | author | 248 relation lines, 14/14 chunks, zero orphans, proposals labelled |
| T-GAS-DOCPREP | `T-GAS-DOCPREP_doc_prep_design_docs.md` | done | T-GAS-DOCS-V2 | author | 4dlab-doc-prep on the 6 v2 docs; 71 chunks, 18 tables, 236 relations |
| T-GAS-GRAPH-AST | `T-GAS-GRAPH-AST_graphify_code_and_tests.md` | done | T-GAS-CODEPREP, T-GAS-TESTPREP | coder | v2_code/v2_tests built; health GOOD, 0 dangling/isolated |
| T-GAS-GRAPH-LLM | `T-GAS-GRAPH-LLM_graphify_wiki_and_docs.md` | void — owner waived Pass-3 | T-GAS-WIKIPREP, T-GAS-DOCPREP | coder | 2026-06-11 direction: second-pass wiki/doc prep is sufficient; no token-spending LLM run |
| T-GAS-PATHS-1 | `T-GAS-PATHS-1_parametrize_build_source_paths.md` | done | — | coder | per-lab wiki/ + four-tier graph source; fix guide OBD paths |
| T-GAS-VAULT | `T-GAS-VAULT_build_gaslab_vault.md` | done | T-GAS-GRAPH-AST, T-GAS-PATHS-1 | author | vault-map.gaslab.yaml + dry-run + build + bases; prose graphs waived |

## 4. Non-negotiables (carry from GASLab + Vault rules)

- **graphify is a SANCTIONED step only inside T-GAS-GRAPH-AST / T-GAS-GRAPH-LLM**, scoped to a
  specific package/dir, building the **new** tier dirs. It is **still forbidden** as a side-effect
  of any other task, and never re-extracts the frozen `graph/v2_current/` (GASLab START_HERE §0).
- **`consumers` is architect-named, never auto-derived from the graph.** Empty list = not ready.
- **No cross-lab Python imports**; every numeric literal in `gaslab/` carries its wiki cite.
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/<id>.md`,
  flip the ledger row to `done`, then STOP. Coder lane runs the inner loop after every edit; the
  prep/graph/vault lanes are graph-tooling (no lab inner-loop) per each task's role note.

## 5. Follow-ups for the owner (not authored as pack tasks)

- Add a GASLab-vault-pack row to the bootstrap table in `4DLab/CLAUDE.md` pointing here.
- The pipeline guide's OBD-hardcoded wiki/graph paths (§2, §6, §9) are addressed mechanically by
  **T-GAS-PATHS-1**; consider a one-line edit there marking those paths as `<lab>`-parametric.
