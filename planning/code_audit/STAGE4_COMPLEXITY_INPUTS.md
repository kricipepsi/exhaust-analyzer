# Stage-4 complexity & clone inputs (from T-PYSCN-1)
**Source:** `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md` · **Status:** deferred inputs — **NOT runnable tasks** · **Authored by:** architect (Cowork), 2026-06-29.

Real maintainability findings that are **deliberately not fix tasks now**: the code they touch is reworked at
**ROADMAP Stage 4** (COMLab + registry, done last). Refactoring before the boundary contracts freeze tunes a
moving target (same logic as D-V2-9 / D-V2-6). Pinned here so they surface when that rework starts.

## COMLab — `fault_atlas_router` complexity (do during the COMLab ranking-spine rework)
Worst complexity in the repo, all in the prune→rank spine:
- `labs/comlab/comlab/core/fault_atlas_router.py:917` `execute_triage_loop` — cyclomatic **144**, cognitive **785**.
- `:1884` `route` — cyclomatic 31, cognitive 119.
- `:825` `_prune_candidates` — 12 / cog 46 · `:765` `evaluate_operator` — 13.
Fold decomposition of `execute_triage_loop`/`route` into the COMLab architecture decision (additive vs
learned/Bayesian ranker, ROADMAP stage 4) — not a standalone refactor against the current spine.

## VINLab — core decode-path duplication (do when VINLab is reconciled for the COMLab prior)
Production clones concentrate in two on-path files (the rest are `tools/` ETL, acceptable as-is):
- `labs/vinlab/vinlab/overlay/cylinder_heuristic.py` + `labs/vinlab/vinlab/decoder.py` — repeated blocks;
  `decoder.py` also carries complexity (`decode_vin_payload` 14, `_apply_vref_techmask` 11).
Consolidate when VINLab is reconciled for the Stage-4 COMLab prior, not before (cleaning against a
pre-reconcile shape is wasted — cf. `labs/dnalab/README.md` "whole-repo green gate" discipline).

## Explicitly NOT actioned
- **VINLab `tools/*`** high-complexity ETL `main()`s (TecDoc enrichers, `build_vref_db`): one-shot
  build/maintenance scripts off the live diagnostic path. Accepted as-is.
- **GASLab** `resolution.apply_differentiators` (cc 53) / `rule_engine._definitive_match` (cc 21): on-path
  but in a **done/green** lab, consumed only via JSON at wiring (D-V2-9: wired imports `gaslab.process`,
  not internals). A pure complexity-score refactor here is speculative work on green code — no named
  consumer, regression risk. Deferred unless a wiring/comprehension need names it.
- **Dead code: 0. Dependency cycles: 0. Lab isolation: intact** (DNALab→vinlab/symptomlab is the
  documented one-way assembler exception, `labs/dnalab/wiki/12_assembly_contract.md`).

## deptry sweep — 2026-06-29 (the last coverage gap, now closed)
Ran `uvx deptry .` per lab (read-only). Verdict: **no real unused dependencies; nothing to remove.**
Most output is config-level false positives, not code debt:
- **pyyaml -> yaml naming (all 7 labs):** deptry reports `pyyaml` "unused" + `yaml` "missing" because the
  install name differs from the import name. `pyyaml` IS used. Do NOT remove it; if deptry is adopted, add
  `[tool.deptry.package_module_name_map]` `pyyaml = ["yaml"]`.
- **dev tools (`pytest`/`ruff`/`pyright`/`pytest-cov`):** flagged "unused" because they are run, not imported.
  Expected; configure deptry's dev-extra handling.
- **dnalab -> `symptomlab`/`vinlab`:** the documented one-way assembler import (undeclared because labs share
  one venv). Expected, not a finding.

Genuine items — both fold into the Stage-4 buckets above; neither blocks wiring:
- **COMLab:** `opentelemetry` imported in `comlab/observability/_tracer.py` + `core/fault_atlas_router.py:147`
  but undeclared. Likely a guarded/optional tracing import — declare it as an optional dep (or confirm the
  guard) during the COMLab rework.
- **VINLab:** `tools/*` ETL scripts import undeclared `mysql`/`pyngrok`/`requests`; plus a
  `labs/vinlab/temp/_check_*.py` scratch-script dir that should not ship in the package (archive per rule 5).
  Handle in the Stage-4 VINLab reconcile alongside the tools complexity/clones.
