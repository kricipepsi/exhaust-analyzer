# T-COMV2-DELTA-2 progress note

Status: done
Date: 2026-06-21

## Scope Confirm

Activate the existing typed `delta_signature` on the production-default v2
registry path only. Add an independent default-off `enable_delta_v2` constructor
gate, reuse `DeltaEngine.compute_delta_signature` for architecture/validity/band
policy, share the family score-promotion rule with v1, re-rank `scored_rules`,
and render a changed winner through the canonical registry translator. Register
`COMLab-DELTA-V2`; do not change delta math/schema/bands, registry defaults,
emitters, corpus, or graphs.

## Changed Files

- `comlab/analytics/delta_engine.py` — shared `apply_rank_score` policy used by
  both v1 and v2 rank consumers.
- `comlab/core/fault_atlas_router.py` — independent v2 flag, live
  `delta_signature` computation/read, `scored_rules` promotion, and winner
  re-render.
- `comlab/core/lab_pipeline_aggregator.py` — threads `enable_delta_v2=False`.
- `registry/integration_shim.py` — canonical `render_ranked_rule` public seam.
- `comlab/config/proposals/entries.yaml` — proposal `COMLab-DELTA-V2`.
- Focused unit/e2e/registry tests — parity, flag-off, single-point,
  band-mismatch, architecture null/inversion, and renderer locks.
- `docs/CROSS_LAB_DEPENDENCIES.md` — DEP-14 consumer live on both paths.
- `tasks/PROGRESS.md` — task closed.

## Verification Gate

- Interpreter: native `.venv-comlab`, Python 3.14.6; pydantic 2.13.4,
  pytest 9.1.1.
- `python -m ruff check .` — all checks passed.
- `python -m pyright --pythonpath .venv-comlab\Scripts\python.exe comlab\ registry\`
  — 0 errors, 0 warnings.
- Focused delta/v2/proposal/shim suite — 68 passed.
- `python -m pytest tests\ -q` — 387 passed, 6 skipped, 0 failed.
- `python -m pytest registry\tests\ -q` — 471 passed, 0 failed.
- Consumer read: `FaultAtlasRouter.route` computes `delta_signature` when
  `_enable_delta_v2`, reads it through `DeltaEngine.apply_rank_score` while
  iterating v2 `scored_rules`, then sorts and renders the promoted top rule.
- Production-default reachability: `LabPipelineAggregator` resolves
  `USE_V2_REGISTRY` with default `"1"` and constructs `FaultAtlasRouter` with
  `use_v2_registry=True`.

## Code Review

- The v1 and v2 consumers share both computation policy and the exact
  `max(static_score, signature.confidence)` family-promotion helper.
- The v2 activation flag is independent from DELTA-1's `enable_delta`; both
  remain default-off.
- Flag-off does not compute or read the delta and does not invoke post-rank
  rendering.
- Missing second frame, confidence-zero abstain, band mismatch, and
  speed-density trim nulling leave the original v2 winner untouched.
- Forced-induction sign inversion is computed before rank promotion and routes
  the inverted positive-trim family rather than a naturally aspirated leak.
- A changed winner is rendered by the registry's existing translator, avoiding
  duplicated fault-name/headline/enrichment assembly in COMLab.
- No cross-lab import, graph operation, registry-default change, corpus rebuild,
  emitter change, or new numeric policy was introduced.

## Remaining Gate

Gate-1 remains open: live diagnostic value requires real two-point capture and
emitter population. This does not block the completed default-off path wiring.
