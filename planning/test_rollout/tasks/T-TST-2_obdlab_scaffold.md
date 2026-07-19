# T-TST-2 — Scaffold obdlab tests/ to the canonical template

**Status:** completed · **Blocked by:** T-TST-0 · **Pack:** `planning/test_rollout/`

## Goal

Lay the T-TST-0 template tree into `labs/obdlab/tests/` so the harness build
(T-TST-8) has a home. **Structure + stubs only** — no live CSV, no live generators
(those are blocked on the master relabel and the obdlab revive/quarantine decision).

## Context (disk state)

`labs/obdlab/tests/` exists with `unit/`, `integration/`, `regression/` and only
`__init__.py` files. Code is forked: `obdlab/schemas/{payload,dna_view,vocabulary}.py`,
`obdlab/core/*` (2060 LOC). README flags a pending **revive-vs-quarantine** scope
decision (>95% NO_FAULT on this corpus) — that gates the *harness*, not this scaffold.

## Success criteria

1. `labs/obdlab/tests/` matches the template: `conftest.py`, `fixtures/`
   (`descriptor.py` **stub** + `.gitkeep` for `obdlab_cases.csv`), `generative/`
   with stub files for the applicable generators (boundary, combinatorial, noise,
   overlap, fuzz — OBD is continuous), `test_cases.py` stub. Existing
   `unit/integration/regression/` retained.
2. `fixtures/descriptor.py` is a **typed stub** — signature + docstring naming the
   source (`obdlab/schemas` + OBD fault-box table) and a `NotImplementedError`
   body, so it imports clean but does not fake coverage.
3. Generative stub files `pytest`-collect as skipped (`pytest.mark.skip(reason=
   "blocked: T-TST-8 obdlab harness")`) — no false green.

## Out of scope

- Building the OBD descriptor / generators / CSV (T-TST-6, T-TST-8).
- The revive-vs-quarantine decision (separate OBDLab task).
- Touching `obdlab/` code or schemas.

## Signal/noise consumer

`labs/obdlab/tests/generative/` (future OBD forked suite). Until T-TST-8, the
stubs are explicitly skipped — they assert no coverage they don't have.

## Files to touch

- `labs/obdlab/tests/conftest.py`, `tests/fixtures/descriptor.py`,
  `tests/fixtures/.gitkeep`, `tests/generative/test_*.py` (stubs), `tests/test_cases.py` (stub)

## Verification

`pytest -q labs/obdlab` collects clean with the new stubs skipped (not failed);
`ruff`/`pyright` clean; no change to `pytest` pass count of existing obdlab tests.
