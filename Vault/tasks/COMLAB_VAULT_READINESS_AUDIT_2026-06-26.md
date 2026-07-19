# COMLab → Vault — Final Readiness Audit

**Date:** 2026-06-26 · **Author:** architect (Cowork) · **Lab:** `labs/comlab`
**Against:** `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md` (Phase-0 gate + Phase-1 quality bars)
**Pack authored:** `Vault/tasks/COM_VAULT_TASKS_START_HERE.md` (+ 14 task files)

## Verdict

COMLab **passes** the Phase-0 readiness gate and the Phase-1 quality bars. There are **no blocking
gaps** — the only outstanding work is the migration pipeline itself (graph tiers, the vault path entry,
the build), which is exactly what the authored pack covers. COMLab is a **full fresh-lab pipeline run**
(≈12 sessions), like the GAS/DTC/VIN/DNA packs — not the trimmed OBDLab docs-only case — because no graph
tiers exist yet. One Phase-1 row (`DOCS-V2`) ships `done`; one (`TESTS-GREEN`) is genuine work.

## Phase-0 readiness gate — PASS (all four corpora present and finished)

| Corpus | Path | State |
|---|---|---|
| code | `labs/comlab/comlab/` | 21 modules, ~6,200 LOC (`core/`, `schemas/`, `analytics/`, `observability/`, `projection.py`) |
| tests | `labs/comlab/tests/` | unit / e2e / integration / generative / regression + fixtures |
| wiki | `labs/comlab/wiki/` | 15 chunks `00_index.md … 14_sources_appendices.md`, current (edited through 2026-06-21) |
| docs | `labs/comlab/docs/` | 6 design-doc peers (HLD/DLD/LLD/BDD/PRD + 11 ADR records) + `Vocabulary/` + `CROSS_LAB_DEPENDENCIES.md` + `ARCHIVE/` |

## Phase-1 quality bars — PASS

- **ruff** — clean on `comlab/` and `tests/` (`All checks passed!`).
- **pyright `comlab/`** — **0 errors** (run with the sandbox 3.14 interpreter via `--pythonpath`; the 13
  "import could not be resolved" errors seen without it are a resolver artifact, not real type errors).
- **pytest** — **509 passed, 4 skipped** (the 4 skips are intentional phase-3 reservations in
  `tests/unit/test_lab_pipeline_aggregator.py`).
- **pyright `tests/`** — **19 real errors** (missing ctor args, `None` fixtures, Optional member access,
  a UUID/list-variance mismatch). Runtime-green but not type-clean — resolved by `T-COM-TESTS-GREEN`.
- **DOCS-V2** — already done: HLD/DLD/LLD/PRD headed "v2.0 — as-built, reconciled to the shipped package";
  BDD v1.0 baselined to v2 code; the `adr/` index has 11 Accepted records (all 2026-06-21).
- **Scope hygiene** — petrol 1990–2010 Euro 1–5 holds; GPF/LSPI/SAI are explicitly marked out of scope in
  `COMLab_PRD.md`/`HLD`. One residual to confirm at WIKIPREP: `wiki/03_vehicle_dna_pruning.md:52` references
  an `SAI stuck on` (`ERR-LC-007`) enable — likely an in-era residual (SAI was fitted on Euro 2–3), not a
  2010–2020 perk leak. Flagged, not a blocker.

## Outstanding (the migration itself — covered by the pack)

- **Graphs:** only `graph/v1_baseline/` exists (frozen). No `v2_code`/`v2_tests` → built by `T-COM-GRAPH-AST`.
- **Vault path entry:** `build_lab_vault.py` `LAB_SRC_PATHS` has **no `comlab` entry** → it falls through to
  OBD's `research/chunks` default and aborts → fixed by `T-COM-PATHS-1`.
- **Vault presence:** COMLab is absent from `Vault/labs/` and `Vault/System-Map.md` → built by `T-COM-VAULT`.

## Scope decisions (owner-confirmed 2026-06-26)

- **Prose graphs TRIMMED (waived, liftable).** Viability assessment: the LLM Pass-3 is *technically proven*
  (OBDLab + symptomlab built `v2_wiki`/`v2_docs`) but *operationally gated* on an LLM backend/API key on the
  coder host — an unverified external dependency — and costs tokens. The last four labs all waived it
  because Phase-2 prep already makes relations explicit and the vault injects architect-named frontmatter
  regardless. So `T-COM-GRAPH-LLM` is authored as a **waived, liftable** row documenting the exact lift
  condition (confirmed backend), mirroring the symptomlab lift precedent. `T-COM-GRAPH-AST` still runs the
  free Part-A health-check.
- **Registry EXCLUDED.** `labs/comlab/registry/` is a separate package with its own 3-skill bundle and
  ledger, and its F1 consolidation is an open owner-gated decision. It gets its own vault pack later
  (see follow-ups). This pack migrates `comlab/comlab/` + tests/wiki/docs only.
- **Custom on-demand skill authored.** Per the per-task-minimal-skills directive + the coding-bootstrap
  ≥3-task trigger, `comlab-vault-prep` was authored (gates the 4 Phase-2 prep tasks) and registered in
  `_comlab_skills/_INDEX.md`. Every task file carries a precise minimal `Load skills:` line; the START_HERE
  §3 ledger is the at-a-glance per-task skill map.

## The authored pack (run in dependency order; one task per session)

```
Phase 1  CODE-CLEAN-A (router/atlas) · -B (schemas) · -C (core pipeline) · -D (analytics/projection)   coder
         TESTS-GREEN (resolve 19 pyright errors; keep 509+4)                                            coder
         DOCS-V2  ← DONE                                                                                 author
Phase 2  CODEPREP · TESTPREP (4dlab-code-prep) · WIKIPREP (4dlab-wiki-prep) · DOCPREP (4dlab-doc-prep)   coder/author
Phase 3  GRAPH-AST (v2_code + v2_tests; Part-A health-check) · GRAPH-LLM = WAIVED                        coder
Phase 4  PATHS-1 (LAB_SRC_PATHS comlab entry) · VAULT (vault-map.comlab.yaml + build + bases)            coder/author
```

Per-task skill loadout (the coder loads only its row): coder-lane tasks load the 3 mandatory COMLab skills
(`comlab-python`, `comlab-verification-loop`, `comlab-code-review`); the 4 prep tasks add the matching
`4dlab-*-prep` + `comlab-vault-prep`; GRAPH-AST loads `4dlab-graphify-run` + `eval-code-graph`; PATHS-1 and
VAULT load `4dlab-vault` (+ `comlab-vault-prep` for VAULT). The registry trio is **not** loaded.

## Follow-ups for the owner (recorded, not authored as pack tasks)

1. **Registry vault pack** — separate workstream, blocked on the F1 registry-consolidation decision.
2. **Prose-graph lift** — if a Pass-3 backend is confirmed on the host, lift `T-COM-GRAPH-LLM` (build
   `v2_wiki`/`v2_docs`, widen the `comlab` `required_graph_tiers` to all four) — the symptomlab precedent.
3. **Wiki SAI residual** — confirm `wiki/03:52` is an in-era residual during WIKIPREP; a one-line architect
   wiki fix if it is a 2010–2020 leak (not a code change).
