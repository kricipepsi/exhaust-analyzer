# T-TST-1 — Align gaslab tests/ to the canonical template

**Status:** completed · **Blocked by:** T-TST-0 · **Pack:** `planning/test_rollout/`

## Goal

Reconcile gaslab's **existing** `tests/` to the T-TST-0 template so it matches the
shape every other lab will use. GASLab is the pilot; its generative harness build
already lives in the `T-TH` series — this task does **not** rebuild it, only
re-lays the folder and wires the shared-engine import.

## Context (disk state)

`labs/gaslab/tests/` already has `fixtures/`, `unit/`, and ~15 `test_*.py` at the
top level (`test_rule_engine.py`, `test_resolution.py`, `test_validators.py`, …).
The generative engine is at `harness/harness/` with gaslab as pilot
consumer (`HARNESS_PROGRESS.md`).

## Success criteria

1. gaslab `tests/` matches the template: top-level `test_*.py` that are unit tests
   move under `unit/`; a `generative/` dir exists with the gaslab generative suite
   referenced from the engine (boundary/combinatorial/noise/overlap/fuzz).
2. `fixtures/descriptor.py` is the single GASLab `ModuleDescriptor` source (built
   from `gaslab/contracts.py` + the `ChemicalSignature` box table), imported by the
   generative suite — no descriptor duplicated inside `harness/`.
3. The stale ontology reference is fixed: any test pointing at
   `GASLab/gaslab/data/gas_lab_ontology.yaml` (v1 archive) repoints to
   `labs/gaslab/gaslab/data/gas_lab_ontology.yaml` (loose-end #2, migration map §4).
4. `pytest -q` collects and passes at the same count as before the move (no test
   lost or silently skipped by the relayout).

## Out of scope

- Rebuilding/extending the GASLab generative harness (that is `T-TH-10/11/14`).
- Deriving `gaslab_cases.csv` from master (that is the T-TH series + T-TST-6 model).
- Any non-gaslab lab.

## Signal/noise consumer

`labs/gaslab/tests/generative/` (the GASLab forked suite) — already the named
pilot consumer of the engine.

## Files to touch

- `labs/gaslab/tests/` (relayout only: move unit tests under `unit/`, add
  `generative/`, consolidate `descriptor.py` under `fixtures/`)
- fix the one stale `gas_lab_ontology.yaml` path in the offending test

## Verification

`pytest -q` before/after collection counts match; `ruff`/`pyright` clean; grep
confirms no remaining `GASLab/gaslab/data` path in `labs/gaslab/`.
