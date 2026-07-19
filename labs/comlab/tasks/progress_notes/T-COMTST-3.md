# T-COMTST-3 progress note

Status: done
Date: 2026-06-21

## Plan / Scope Confirm

Replace only the two COMLab generative stubs with bounded categorical coverage
and fixed malformed-input fuzz. Derive axes from the existing descriptor, build
validated inbound requests through its `build_args`, run the production entry
point, and assert schema-valid output or clean validation/fatal failure. Do not
use continuous `FaultBox` generators, assert verdict accuracy, or modify
production source, fixtures, registry, wiki, or graph artifacts.

## Changed Files

- `tests/generative/test_combinatorial.py` — bounded categorical product over
  degradation scenarios, representative chemistry and routing values, and all
  horizons.
- `tests/generative/test_fuzz.py` — fixed missing-key, empty-block, sentinel,
  invalid-enum, and malformed-DTC cases.
- `tasks/PROGRESS.md` — T-COMTST-3 row closed.
- `tasks/progress_notes/T-COMTST-3.md` — verification and review record.

## Verification Gate

- Native adapted interpreter: Python 3.14.6; pydantic 2.13.4; pytest 9.1.1.
- `ruff check tests/generative/` — clean.
- `pyright --pythonpath .venv-comlab/Scripts/python.exe tests/generative/` —
  0 errors.
- `pytest tests/generative/ -q -rs -s` — 12 passed, no skips.
- Combinatorial report — 192 cases: 192 schema-valid outputs and 0 validation
  failures; axes are degradation 4 × representative chemistry 4 ×
  representative routing 4 × horizon 3.
- Fuzz report — 11 malformed/sentinel cases rejected by Pydantic validation.
- `rg -n "T-TST-10" tests` — no matches.
- `ruff check .` — clean.
- `pyright --pythonpath .venv-comlab/Scripts/python.exe comlab/` — 0 errors.
- `pytest -x -q` — 423 passed, 4 skipped.

## Code Review

- Both original skip decorators and no-op bodies are removed.
- Axis values come from `build_comlab_descriptor().fields`; chemistry and
  routing use a deterministic evenly spaced cap while all degradation and
  horizon values participate.
- The descriptor assembles each base request, then the production inbound
  Pydantic contract revalidates each categorical mutation before processing.
- Generated valid requests must return `OrchestratorFinalUIOutput`; unexpected
  runtime exceptions are not caught and therefore fail the suite.
- Fuzz mutations cover missing required structures, empty upstream blocks,
  the wiki's −127/999 sentinels, wrong sample/O2/routing enums, and an invalid
  DTC regex value.
- Fuzz catches only `ValidationError`; if a future schema accepts a malformed
  payload, the production result must explicitly be `FATAL_INCOMPLETE`.
- No expected fault, family, confidence, or accuracy assertion was added.
- No shared continuous boundary/noise generator, cross-lab import, production
  source change, new field, enum, fault, consumer, or graph operation exists.
