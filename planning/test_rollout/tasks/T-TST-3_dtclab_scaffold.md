# T-TST-3 — Scaffold dtclab tests/ to the canonical template

**Status:** completed · **Blocked by:** T-TST-0 · **Pack:** `planning/test_rollout/`

## Goal

Lay the T-TST-0 template tree into `labs/dtclab/tests/`. **Structure + stubs only.**
DTCLab is **discrete** — the template here omits the continuous generators.

## Context (disk state)

`labs/dtclab/tests/` exists with `unit/integration/regression/` (only `__init__.py`).
Code forked: `dtclab/schemas/{freeze_frame,mode06_result,payload,dna_view,vocabulary}.py`,
`dtclab/core/*` (1582 LOC). README flags the `T-FX-13` hex-regex contract gap — that
gates the *harness* (T-TST-9), not this scaffold.

## Success criteria

1. `labs/dtclab/tests/` matches the template **minus** the continuous generators:
   `conftest.py`, `fixtures/` (`descriptor.py` stub + `.gitkeep`), `generative/`
   with **only** `test_combinatorial.py` and `test_fuzz.py` stubs, `test_cases.py`
   stub. No `test_boundary.py` / `test_noise.py` / `test_overlap.py` (ε-boundary
   and Gaussian noise do not apply to discrete DTC codes — see ledger matrix).
2. `descriptor.py` stub names its source (`dtclab/schemas` + DTC rule/family table)
   and raises `NotImplementedError`.
3. Generative stubs collect as skipped (`reason="blocked: T-TST-9 dtclab harness"`).

## Out of scope

- DTC descriptor/generators/CSV (T-TST-7, T-TST-9). The `T-FX-13` gap. `dtclab/` code.

## Signal/noise consumer

`labs/dtclab/tests/generative/` (future DTC forked suite); stubs skipped until T-TST-9.

## Files to touch

- `labs/dtclab/tests/conftest.py`, `tests/fixtures/descriptor.py`,
  `tests/fixtures/.gitkeep`, `tests/generative/{test_combinatorial,test_fuzz}.py`
  (stubs), `tests/test_cases.py` (stub)

## Verification

`pytest -q labs/dtclab` collects clean (new stubs skipped); `ruff`/`pyright` clean;
existing dtclab pass count unchanged; confirm the three continuous-generator files
are absent (not empty — absent).
