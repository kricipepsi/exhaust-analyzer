# T-COMV2-DELTA-1B progress note

Status: done
Date: 2026-06-20

## Scope Confirm

Standalone `comlab/analytics/delta_engine.py` — typed output models, the
`compute_delta_signature` entry point, the architecture gate, the validity gate, and
the single-point sentinel. Gate order = architecture → validity → (profiles). Profile
bodies are the 1C concern; this slice is the gate/sentinel families and their tests.
Module is NOT wired into the router (1D). Engine code landed in session 1; this session
authored the unit tests for the 1B families.

## Changed Files

- `labs/comlab/comlab/analytics/delta_engine.py` — engine module *(session 1; verified)*
- `labs/comlab/tests/unit/test_delta_engine.py` — NEW; 1B gate/sentinel families *(this session)*

## Verification Gate

- `pytest tests/unit/test_delta_engine.py -q` — 23 passed (1B + 1C families combined).
  1B-specific families green:
  - **Sentinel:** `test_sentinel_no_second_frame` → `present=False`, `SINGLE_POINT`, conf 0.0.
  - **Architecture (delta-relations/06):** MAP-only → `trim_nulled`;
    turbo/supercharger → `trim_inverted` (parametrized); both-`None` → permissive;
    unknown-architecture confidence cap → 0.70.
  - **Validity (delta-relations/08):** elevated dilution (CO+CO₂ ≤ 6), vsum < 14,
    rpm-unstable, low-frame `sample_validity=INVALID` → each `present=True`, conf 0.0.
- `ruff check .` — All checks passed.
- `pyright tests/unit/test_delta_engine.py` — 0 errors. `pyright comlab/` — no new errors
  in `delta_engine.py` (pre-existing debt unchanged).
- `pytest -q` — 368 passed, 12 skipped, 2 known-red (`registry` module absent — not ours).
- **Not-wired gate:** `grep -rnI compute_delta_signature comlab/core/` → empty (engine is
  standalone; wiring is 1D).

## Code Review

- Engine mirrors `PowerLossAnalytics`: static methods, pure math, pydantic I/O, every
  numeric band a `# wiki:`-cited class attr.
- Byte-identity contract verified by the sentinel test: absent frame → `present=False`,
  conf 0.0, so a wired Phase 5 (1D) would fall back to the static signature unchanged.
- Untrusted/nulled paths all return conf 0.0 — confirmed by the validity + speed-density
  tests, so an invalid second reading never perturbs the static rank.
- Architecture gate runs BEFORE any profile (the mandatory order from delta-relations/06)
  — exercised by the MAP-only-null and turbo-invert tests.

## Next

`T-COMV2-DELTA-1C` — profile bodies + profile/abstain tests (same session; see that note).
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
