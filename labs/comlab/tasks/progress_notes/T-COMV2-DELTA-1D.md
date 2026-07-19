# T-COMV2-DELTA-1D progress note

Status: done
Date: 2026-06-20

## Scope Confirm

Wire the completed delta engine into the v1 `use_v2_registry=False` router path
behind a default-off `enable_delta` flag. Compute the signature in `route()`,
consume it in `execute_triage_loop` Phase 5 with `max(static_score, confidence)`,
thread the flag through `LabPipelineAggregator`, and lock both single-point
inertness and trusted two-point activation. The v2 registry shim/default,
ExecutionMeta degradation mapping, corpus, and emitters remain unchanged.

## Changed Files

- `comlab/core/fault_atlas_router.py` — default-off flag, lazy delta computation
  in the v1 branch, and Phase 5 family-matched primary rank input.
- `comlab/core/lab_pipeline_aggregator.py` — `enable_delta=False` constructor
  flag threaded into `FaultAtlasRouter`.
- `tests/e2e/test_delta_router_wiring.py` — single-point byte-identity and
  two-point winner-promotion/event regression locks.
- `tasks/PROGRESS.md` — 1A–1D and epic rows closed.

## Verification Gate

- Python: `C:\Workspace\labs\dtclab\.venv` → 3.14.6.
- `ruff check .` — all checks passed.
- `pytest tests/unit/test_delta_engine.py -q` — 23 passed.
- `pytest tests/e2e/test_delta_router_wiring.py -q` — 2 passed.
- `pytest tests/e2e -q -k "single_point or regression or delta"` —
  2 passed, 42 deselected.
- `pytest tests/unit/test_fault_atlas_router.py tests/unit/test_symptom_prior.py
  tests/unit/test_router_spans.py -q` — 83 passed, 6 skipped (OpenTelemetry
  dependency absent; pre-existing).
- `pytest -q` — 370 passed, 12 skipped, 2 known-red:
  `test_fault_atlas_router_v2.py::{test_v1_when_explicit_false,
  test_v2_when_explicit_true}` fail because the separate `registry` package is
  absent from this checkout.
- `pyright tests/e2e/test_delta_router_wiring.py` with the 3.14 venv —
  0 errors. Repository-wide `pyright comlab/` remains at the pre-existing 12
  OpenTelemetry/registry-import and optional-access errors; no new delta error.

## Consumer-Read Gate

- `delta_signature = sanitized.get("delta_signature")` is inside
  `execute_triage_loop` Phase 5.
- The v1 branch guarded by `if self._use_v2_registry` falls through to lazy
  `DeltaEngine.compute_delta_signature(request)` and then calls
  `execute_triage_loop(sanitized)`.
- The Phase 5 consumer requires `present`, positive confidence, and a target
  family; it resolves each candidate through the KG and applies
  `max(score, confidence)` only to matching families.

## Code Review

- Default-off is preserved at both constructor layers.
- Three independent falsy paths leave scoring untouched: missing signature key,
  `present=False`, and `confidence==0.0`.
- The existing sort and threshold logic are unchanged.
- The activation fixture uses a static catalyst winner and mechanical-wear
  runner-up; trusted ΔHC evidence promotes mechanical wear from 0.75 to 0.92 and
  records `delta_signature_applied`.
- The single-point fixture supplies a fixed existing audit timestamp and proves
  the complete serialized outputs are identical with the flag on and off.
- No cross-lab import, graph rebuild, v2 shim change, registry-default change,
  or ExecutionMeta `SINGLE_POINT` exposure was introduced.

## Next

Stop. `T-COMV2-DELTA-2` remains the separate v2-registry activation follow-up.
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
