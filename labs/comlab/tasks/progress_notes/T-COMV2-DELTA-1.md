# T-COMV2-DELTA-1 epic progress note

Status: done
Date: 2026-06-20

## Plan / Scope Confirm

This is the **umbrella epic** (split into 1A–1D); the per-slice scope confirms live in
`progress_notes/T-COMV2-DELTA-1{A,B,C,D}.md`. Epic-level confirm:

- **Field:** `delta_signature` — a typed cross-lab two-point delta computed by a new stateless
  COMLab analytics module (`analytics/delta_engine.py`) from an optional `second_operating_point`
  frame on the request.
- **Guard:** default-off constructor flag `enable_delta=False` (mirrors `use_v2_registry`).
  Absent frame / flag-off / untrusted ⇒ **byte-identical single-point path**.
- **Signal/noise consumer:** `fault_atlas_router.execute_triage_loop` **Phase 5** — `delta_signature`
  becomes a primary rank term via `score = max(score, confidence)` on the KG-family match; the static
  signature stays the fallback. Proposal-bounded as `COMLab-DELTA`; consumer ships in the same change.
- **Bands (locked):** ΔTrim @ `STRESS_IDLE`, Δgas/ΔO₂ @ `REGULATORY_HIGH_IDLE`; **ABSTAIN on band
  mismatch**. Fixtures derived from `delta-relations/01–08`, each `# wiki:`-cited.
- **Files:** `schemas/{vocabulary,response,ingestion}.py` · `analytics/delta_engine.py` ·
  `core/{fault_atlas_router,lab_pipeline_aggregator}.py` · `config/proposals/entries.yaml` ·
  `tests/unit/test_delta_engine.py` + `tests/e2e/` · `docs/CROSS_LAB_DEPENDENCIES.md` (DEP-14) · `PROGRESS.md`.

## Verification Gate

All four linear slices are complete:

- 1A schema/proposal foundations.
- 1B architecture, validity, and single-point gates.
- 1C per-signal profiles with locked bands and mismatch abstention.
- 1D default-off v1 router consumer, aggregator flag, and e2e locks.

Final baseline: Ruff clean; 23 delta-engine tests pass; 2 delta-router e2e tests
pass; full suite 370 passed, 12 skipped, with only the two documented missing
`registry` failures.

## Code Review

The proposal field now has its named live consumer in
`fault_atlas_router.execute_triage_loop` Phase 5 on the
`use_v2_registry=False` path. Single-point behavior is regression-locked
identical, while trusted two-point evidence uses `max(static, delta confidence)`
to promote the KG-matching family. The feature remains default-off and
proposal-bounded.

Live diagnostic value is still gated on two-point capture/emission. Production
v2-registry activation remains `T-COMV2-DELTA-2`.
---

## LEDGER RECONCILIATION — 2026-06-21 (architect, Cowork)

**Stale-ledger guard cleared.** Earlier snapshots in this note (and the sibling
DELTA-1/1A/1B/1C/1D notes) recorded **2 failing tests**. Those were the **known-red
`registry`-package import failures** captured on 2026-06-20, when the `registry`
package was broken — they were never failures in COMLab delta code.

They were resolved downstream by:
- **`T-REG-REVIVE-1`** (done 2026-06-21) — revived `labs/comlab/registry/`; registry **470 passed**.
- **`T-COMV2-DELTA-2`** (done 2026-06-21) — COMLab **387 passed** + registry **471 passed**; ruff/pyright clean.

**Re-verified 2026-06-21** with the pinned interpreter (`../../.sandbox-py/bin/python3.14`, 3.14.5):
- `pytest -q` → **417 passed, 10 skipped, 0 failed** (10 skips = opentelemetry-not-installed router spans + 1 phase-3 legacy stub).
- `pytest registry/tests/ -q` → **471 passed, 0 failed**.

These rows are correctly `done`; the "2 failed" text above is a historical snapshot,
not a live regression. `T-COMTST-4` (the next `pending` row) is unblocked.
