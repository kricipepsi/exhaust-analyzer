# DTCLab → Vault — PIPELINE PACK · START HERE

Read this first, every session, before any other action in the DTC vault pack.

**Pack:** VAULT (DTCLab tier) · **Lab:** `labs/dtclab` · **Authored:** 2026-06-11 (architect)
**Pipeline spec:** `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`
**Vault plan:** `Vault/VAULT_IMPLEMENTATION_PLAN.md`
**Driving skill:** `_skills/graph/4dlab-vault/`
**Template pack:** GASLab (`GAS_VAULT_TASKS_START_HERE.md`) — DTCLab mirrors its decisions.

> **One rule above all (signal/noise):** nothing — no schema field, no graph edge, no vault
> frontmatter key — ships unless a **named, existing consumer** reads it on a real code path.
> "Future use" is not a consumer. A note with an empty `consumers` list is not ready to ship.

---

## 0. DTCLab-specific paths — DO NOT copy OBDLab's paths blindly

DTCLab shares GASLab's layout (wiki at `wiki/`, not `research/chunks/`), so the same path trap
applies. `build_lab_vault.py` defaults to OBDLab's layout for any **unregistered** lab:

| Corpus | OBD default (WRONG for DTC) | **DTCLab actual path** |
|---|---|---|
| code | `labs/<lab>/<lab>/` | `labs/dtclab/dtclab/` ✓ (core/, schemas/, config/, `family_map.py`, `ranking.py`) |
| tests | `labs/<lab>/tests/` | `labs/dtclab/tests/` ✓ (16 test files: unit/integration/regression/generative) |
| wiki | `labs/<lab>/research/chunks/` | **`labs/dtclab/wiki/`** (13 chunk files: `00_INDEX.md` + `01`–`12`) |
| docs | `labs/<lab>/docs/` | `labs/dtclab/docs/` ✓ — **6 design docs** (HLD/DLD/LLD/ADR/BDD/PRD) + `DTC_VOCABULARY.md` |
| graph | `labs/<lab>/graphify-out/graph.json` (single) | **four-tier** `labs/dtclab/graph/v2_code|v2_tests/` (to be built; today only `graph/v2_current/` + `graph/v1_baseline/` exist — **frozen**) |

`build_lab_vault.py` has **no `dtclab` entry** in `LAB_SRC_PATHS` (only `obdlab`, `gaslab`), so a DTC
build would fall through to OBD's `research/chunks` default and abort. **T-DTC-PATHS-1** adds the
one-entry override (mirroring the `gaslab` entry) and is a hard blocker on **T-DTC-VAULT**.

**Frozen canonical graphs:** `graph/v2_current/` and `graph/v1_baseline/` are the existing single
graphs. They are **canonical — never re-extracted.** Phase-3 builds the **new** `v2_code` / `v2_tests`
tier dirs only and leaves the frozen dirs byte-unchanged.

## 1. Scope trims applied to this pack (owner direction 2026-06-11)

- **"Skip graph testing" → mirror GASLab.** The Pass-3 LLM prose graphs (`v2_wiki`, `v2_docs`) are
  **waived**, and the graph-review cross-check tier (the OBDLab `T-VAULT-DOCGRAPH-2 / WIKIGRAPH-1 /
  CODEGRAPH-1` equivalents) is **not authored**. Phase-3 still runs the cheap, no-token, no-re-extraction
  **health-check** (`eval-*-graph` Part-A only) inline as build verification. The vault copies wiki/docs
  as raw `.md` + injected frontmatter (no prose graph), exactly as GASLab's tier was built.
- **DOCS-V2 is DONE (this session).** The six design docs were reconciled to the shipped `dtclab/`
  code on 2026-06-11 (HLD/DLD/LLD/PRD rewritten to v2.0; ADR + BDD authored; `DTC_VOCABULARY.md`
  surgically fixed: 18-tag enum, SAI removed). So `T-DTC-DOCS-V2` ships `done`; it unblocks DOCPREP.
- **Code-clean is NOT done (full fresh-lab pack).** Unlike GASLab, DTCLab has **no** `docs/audits/`
  code audit. So `T-DTC-CODE-CLEAN` and `T-DTC-TESTS-GREEN` are authored as real Phase-1 work. This is
  the full ≈10–12-session path (guide §7.3), not GASLab's trimmed path.
- **Stale-comment fix split out.** The 2026-06-11 docs reconciliation surfaced two stale
  enum-count docstrings in shipped code (see `T-DTC-COMMENT-FIX`). It is a tiny standalone coder task
  feeding clean labels into CODEPREP; it is **not** bundled into the diff of any other task.

## 2. The chain (run in dependency order — one task per session)

```
PHASE 1  T-DTC-CODE-CLEAN     codingskills audit + AST-legible on dtclab/dtclab/   coder
         T-DTC-COMMENT-FIX    fix 2 stale enum-count docstrings (18 vs 17/19)      coder
         T-DTC-TESTS-GREEN    whole tests/ tree green + meaningful                  coder
         T-DTC-DOCS-V2        reconcile 6 design docs to v2  ← DONE 2026-06-11      author
              │
PHASE 2  T-DTC-CODEPREP       4dlab-code-prep on labs/dtclab/dtclab/  ← CODE-CLEAN, COMMENT-FIX   coder
         T-DTC-TESTPREP       4dlab-code-prep on labs/dtclab/tests/   ← TESTS-GREEN                coder
         T-DTC-WIKIPREP       4dlab-wiki-prep on labs/dtclab/wiki/    ← (wiki current)             author
         T-DTC-DOCPREP        4dlab-doc-prep on the 6 design docs     ← DOCS-V2                     author
              │
PHASE 3  T-DTC-GRAPH-AST      graphify code+tests → graph/v2_code, v2_tests ← CODEPREP+TESTPREP    coder
         (T-DTC-GRAPH-LLM     waived — "skip graph testing"; prose graphs not built, mirror GAS)
              │
PHASE 4  T-DTC-PATHS-1        add dtclab entry to LAB_SRC_PATHS (wiki/, code+tests tiers)  ← (none) coder
         T-DTC-VAULT          vault-map.dtclab.yaml + dry-run + build + bases ← GRAPH-AST + PATHS-1 author
```

The four corpora are independent until they converge at the vault, so within a phase the sessions run
in any order. **PATHS-1 and COMMENT-FIX have no corpus dependency** and can run any time before their
dependents (VAULT / CODEPREP respectively).

## 3. Pack ledger (source of truth — the next task is the first `pending` row whose Blocked-by are all `done`)

| ID | Task file | Status | Blocked by | Lane | Notes |
|---|---|---|---|---|---|
| T-DTC-DOCS-V2 | `T-DTC-DOCS-V2_reconcile_design_docs_to_v2.md` | done | — | author | 2026-06-11: HLD/DLD/LLD/PRD → v2.0; ADR+BDD authored; vocab fixed (18-tag, SAI removed). Reconciled to shipped code. |
| T-DTC-CODE-CLEAN | `T-DTC-CODE-CLEAN_codingskills_audit_package.md` | done | — | coder | 2026-06-11: 1 fix (inline import → module level); ruff clean, pyright 0 on dtclab/, 576 tests green; audit record created |
| T-DTC-COMMENT-FIX | `T-DTC-COMMENT-FIX_enum_count_docstrings.md` | done | — | coder | fix stale `17-value`/`19-value` docstrings → 18 in `vocabulary.py` + `family_map.py` |
| T-DTC-TESTS-GREEN | `T-DTC-TESTS-GREEN_whole_tests_tree_green.md` | done | — | coder | 2026-06-11: resolved 3 pyright errors in tests; 576 tests green; type check clean |
| T-DTC-CODEPREP | `T-DTC-CODEPREP_ast_legibility_audit_package.md` | done | T-DTC-CODE-CLEAN, T-DTC-COMMENT-FIX | coder | 2026-06-11: 4dlab-code-prep probe + audit; added explicit `__all__` to ranking, family_map, and sanitizer; ruff & pyright clean, all tests green |
| T-DTC-TESTPREP | `T-DTC-TESTPREP_ast_legibility_audit_tests.md` | done | T-DTC-TESTS-GREEN | coder | 2026-06-11: 4dlab-code-prep run scoped to tests/ returned zero violations. Folded into CODEPREP. |
| T-DTC-WIKIPREP | `T-DTC-WIKIPREP_explicit_relations_wiki.md` | done | — | author | 2026-06-11: 4dlab-wiki-prep run over 13 chunks completed, 160 relation lines, proposals kept as proposals |
| T-DTC-DOCPREP | `T-DTC-DOCPREP_doc_prep_design_docs.md` | done | T-DTC-DOCS-V2 | author | 2026-06-11: 4dlab-doc-prep completed; 75 chunks written, 21 tables converted, 220 relation lines, zero orphans |
| T-DTC-GRAPH-AST | `T-DTC-GRAPH-AST_graphify_code_and_tests.md` | done | T-DTC-CODEPREP, T-DTC-TESTPREP | coder | build `v2_code`/`v2_tests`; health-check Part-A only; never touch `v2_current`/`v1_baseline` |
| T-DTC-GRAPH-LLM | — (no file) | waived | T-DTC-WIKIPREP, T-DTC-DOCPREP | — | "skip graph testing": prose Pass-3 graphs not built; Phase-2 wiki/doc prep is sufficient |
| T-DTC-PATHS-1 | `T-DTC-PATHS-1_register_dtclab_source_paths.md` | done | — | coder | 2026-06-11: registered dtclab entry in LAB_SRC_PATHS mirroring gaslab; dry-runs verified. |
| T-DTC-VAULT | `T-DTC-VAULT_build_dtclab_vault.md` | done | T-DTC-GRAPH-AST, T-DTC-PATHS-1 | author | vault-map.dtclab.yaml + dry-run + build + bases; `_vocabulary/DTC_VOCABULARY.md`; prose graphs waived |


## 4. Non-negotiables (carry from DTCLab + Vault rules)

- **graphify is a SANCTIONED step only inside T-DTC-GRAPH-AST**, scoped to a specific package/dir,
  building the **new** tier dirs. It is **still forbidden** as a side-effect of any other task, and
  never re-extracts the frozen `graph/v2_current/` or `graph/v1_baseline/`.
- **`consumers` is architect-named, never auto-derived from the graph.** Empty list = not ready.
- **No cross-lab Python imports** (audited in `test_dna_view.py`); DTCLab mirrors the DNA-view types
  it needs locally.
- **Signal/noise at the edge:** every `CONSUMES`/`VERIFIES` line a prep skill appends must name a real,
  existing code path or test. Proposals (`EP-DTC-NOSTART-1`, the `wiki/11_proposals_register.md` slate)
  stay labelled proposals — never promoted to live.
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/<id>.md`, flip
  the ledger row to `done`, then STOP. Coder lane runs the inner loop (`ruff`→`pyright`→`pytest -x -q`)
  after every edit; the prep/graph/vault lanes are graph-tooling (no lab inner-loop) per each task's role note.

## 5. Follow-ups for the owner (not authored as pack tasks)

- **GPF out-of-era reconciliation.** `wiki/11_proposals_register.md §11.4` proposes dropping GPF /
  hex-tailed codes (P244A/P2459) as outside the 1990–2010 Euro 1–5 scope, but shipped code still routes
  them (5 DNA-gated entries include 2 GPF). This is a behavioural/scope decision, not a doc or comment
  fix — it needs its own task spec with the COMLab consumer impact named. Recorded in `PRD_DTCLab.md §8`
  and `HLD_DTCLab.md §10`; **not** in this pack's diff.
- A DTCLab-vault-pack row has been added to the bootstrap table in `4DLab/CLAUDE.md` pointing here.
