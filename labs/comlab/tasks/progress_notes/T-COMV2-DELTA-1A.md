# T-COMV2-DELTA-1A progress note

Status: done
Date: 2026-06-20

## Scope Confirm

Inert input surface for the cross-lab two-point delta — `SINGLE_POINT` degradation
mode, widened `DegradationLit`, optional `SecondOperatingPointFrame` on the request,
and the `COMLab-DELTA` proposal registration. Default-`None` everywhere; nothing reads
these yet (engine is 1B/1C, consumer is 1D). Schema/vocab landed in session 1; this
session completed the outstanding step 4 (`entries.yaml`).

## Changed Files (this slice)

- `labs/comlab/comlab/schemas/vocabulary.py` — `DegradationMode.SINGLE_POINT` (`:569`) *(session 1)*
- `labs/comlab/comlab/schemas/response.py` — `DegradationLit` widened to `SINGLE_POINT` (`:26`) *(session 1)*
- `labs/comlab/comlab/schemas/ingestion.py` — `SecondOperatingPointFrame` (`:370`) +
  `OrchestratorInboundRequest.second_operating_point` (`:463`) *(session 1)*
- `labs/comlab/comlab/config/proposals/entries.yaml` — `COMLab-DELTA` entry appended *(this session)*

## Verification Gate

- `ruff check .` — All checks passed.
- `pyright comlab/` — no new errors (pre-existing opentelemetry / `fault_atlas_router.py`
  Optional-access / `registry`-import debt only; nothing in the touched schema files).
- `pytest -q` — 368 passed, 12 skipped, 2 failed. The 2 failures are the known-red
  baseline `tests/unit/test_fault_atlas_router_v2.py::{test_v1_when_explicit_false,
  test_v2_when_explicit_true}` → `ModuleNotFoundError: No module named 'registry'`
  (the `registry` module is absent from this checkout; documented in the DELTA pickup
  note as NOT ours). All existing JSON fixtures validate unchanged → byte-identity holds
  (default `None`, last-field position).
- YAML parse + entry check: `COMLab-DELTA` present exactly once, `status: proposed`,
  `field.path = OrchestratorInboundRequest.second_operating_point`, consumer names
  `execute_triage_loop` (Reader: T-COMV2-DELTA-1D). 19 total proposal entries.
- Greps:
  - `grep -nI SINGLE_POINT comlab/schemas/` → present in both `vocabulary.py` and `response.py`.
  - `grep -nI second_operating_point comlab/schemas/ingestion.py` → field present, default `None`.
  - `grep -nI COMLab-DELTA comlab/config/proposals/entries.yaml` → present.

## Code Review

- Proposal entry mirrors the existing entry shape (id/family/consumer/status/owning_ledger/
  source/description/field) used by `COMLab-A`..`COMLab-G`; the YAML-shape tests
  (`-k "proposal or entries or kg_registry_consistency"`) pass (8 tests).
- Anti-orphan is a Stage-4-close gate, not per-task; registering `COMLab-DELTA` now keeps
  the field proposal-bounded from the moment it exists. `entries.yaml` is registry-only and
  does not gate behaviour, so registering before the 1D consumer lands is harmless.
- No router/engine change in this slice (out of scope — 1B/1C/1D).

## Next

`T-COMV2-DELTA-1B` / `1C` — engine + unit tests (completed in the same session; see those notes).
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
