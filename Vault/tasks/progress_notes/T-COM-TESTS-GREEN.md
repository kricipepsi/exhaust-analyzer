## Plan

Task: `T-COM-TESTS-GREEN` — make the COMLab `tests/` tree pyright-clean without weakening runtime assertions.

Scope guard:
- Touch only `labs/comlab/tests/**/*.py`, this progress note, and the VAULT task/ledger status if gates pass.
- No production `comlab/` changes, no registry tests, no graphify.
- Preserve the 4 intentional phase-3 skips in `tests/unit/test_lab_pipeline_aggregator.py`.

Fix classes to audit:
- Missing required Pydantic constructor fields in test payload builders.
- Deliberate `None` negative-path constructor inputs that need typed casts or real minimal test doubles.
- Optional member access assertions that need explicit `is not None` guards.
- UUID/list variance mismatches in test fixtures.

VERIFICATION GATE — T-COM-TESTS-GREEN
=====================================
Phase 1 Syntax/import:  PASS — `python -m py_compile` succeeded for all five touched test modules.
Phase 2 Type check:     PASS — `/agent_workspace/.venv-wired/bin/pyright --pythonpath /agent_workspace/.venv-wired/bin/python tests/` returned 0 errors; `pyright ... comlab/` also returned OK.
Phase 3 Lint:           PASS — `/agent_workspace/.venv-wired/bin/ruff check tests/` returned OK.
Phase 4 pytest:         PASS — `/agent_workspace/.venv-wired/bin/python -m pytest -q` returned `509 passed, 4 skipped`; the 4 existing phase-3 skips remain skipped.
Phase 5 Wiki/orphan:    PASS — tests-only type fixes; no schema field, enum, production consumer, numeric threshold, or COMLab code path changed.
Phase 6 Diff review:    PASS — changed files are the five pyright-error test modules plus required VAULT progress/ledger metadata; no graphify/KG rebuild run.

comlab-python checklist items applied:
  1. Type hints — `routing_tags` helper type narrowed to `list[DTCRoutingTag]`; UUID fixture uses a `UUID` object.
  2. Docstrings — existing test docstrings preserved; no public production symbol introduced.
  3. No mutable defaults — checked; none introduced.
  4. No bare except — checked; none introduced.
  5. No magic numbers — no production numeric thresholds added; fixture defaults are unchanged behavior anchors.
  6. f-strings — none introduced.
  7. Pathlib — unchanged; no file I/O added.
  8. Context managers — existing registry-loader patches remain under `with`.
  9. `is None` — optional winners now use explicit non-None assertions before member access.
  10. Sorted imports — ruff clean.

Status: DONE — flipping VAULT ledger row to done.

CODE REVIEW — T-COM-TESTS-GREEN
===============================
1. Design rules:        PASS — tests-only changes; no cross-lab imports, raw-sensor derivation, schema surface, or signal/noise field added.
2. Scope compliance:    PASS — edits are limited to `labs/comlab/tests/**/*.py` plus required progress/ledger metadata.
3. Contracts:           PASS — production signatures, Pydantic models, enums, field defaults, and flag defaults unchanged.
4. Docstrings:          PASS — no new public production symbols; test names and docstrings still describe behavior.
5. Wiki provenance:     PASS — no new production numerics/enums; fixture values only satisfy existing schema requirements.
6. Immediate Checklist: PASS — py_compile, pyright tests, pyright comlab, ruff tests, targeted pytest, and full pytest all passed.
7. Test coverage:       PASS — assertions were preserved or strengthened with non-None guards; targeted touched tests passed (`137 passed`), full suite passed (`509 passed, 4 skipped`).
8. Structural craft:    PASS with notes — real constructor dependencies replaced `None` placeholders in registry-selection tests; optional result assertions are explicit without weakening verdict/family/score checks.

Verdict: CLEAN
Blockers: none
