## Plan

Task: `T-COM-CODE-CLEAN-C` — codingskills audit + AST-legibility pass for the non-router COMLab core pipeline.

Target files:
- `labs/comlab/comlab/core/lab_pipeline_aggregator.py`
- `labs/comlab/comlab/core/perception_contradiction.py`
- `labs/comlab/comlab/core/horizon_context_injector.py`
- `labs/comlab/comlab/core/symptom_router.py`
- `labs/comlab/comlab/core/ecu_hardware_checker.py`

Skills/passes loaded:
- `comlab-python`
- `comlab-verification-loop`
- `comlab-code-review`
- `improve-codebase-architecture`
- `uncle-bob-craft`
- `code-simplifier`
- `code-review-excellence`
- `pythonskill`

Scope guard:
- No behavior change.
- No schema field or enum additions.
- No graphify / graph rebuild.
- No cross-lab Python imports.
- Only scoped legibility fixes in the non-router core pipeline files, plus this progress note and VAULT ledger update if gates pass.

AST-legibility checks:
- No `import *` in scoped files.
- Public surface stated or explicitly recorded.
- Public signatures typed and public classes/functions documented.
- Non-obvious fusion gates have `# WHY:` rationale where needed.
- Numeric literals in changed core code have named constants and `# wiki:` provenance.
- `enable_delta` / `enable_fatal_gates` remain default-off.

VERIFICATION GATE — T-COM-CODE-CLEAN-C
======================================
Phase 1 Syntax/import:  PASS — `python -m py_compile` succeeded for all five scoped core files.
Phase 2 Type check:     PASS — `/agent_workspace/.venv-wired/bin/pyright --pythonpath /agent_workspace/.venv-wired/bin/python comlab/` returned OK.
Phase 3 Lint:           PASS — `/agent_workspace/.venv-wired/bin/ruff check .` returned OK.
Phase 4 pytest:         PASS — `/agent_workspace/.venv-wired/bin/python -m pytest -x -q` returned `509 passed, 4 skipped`.
Phase 5 Wiki/orphan:    PASS — no schema fields, enum values, or consumer fields added; new numeric constants carry inline `# wiki:` or `lld:` provenance; `search` found no star imports, cross-lab imports, banned v6 enum names, bare `except:`, `print(`, or `== None`/`!= None` in scoped files.
Phase 6 Diff review:    PASS — scoped source files only plus required progress/ledger metadata; no graphify/KG rebuild run; no behavior path changed.

comlab-python checklist items applied:
  1. Type hints — `AggregatorAbort.__init__`, routing-directive seams, and `route_symptom` annotations tightened.
  2. Docstrings — public dataclass/class/function docstrings audited; `PerceptionContradictionResult.qualifiers` documented.
  3. No mutable defaults — checked; no mutable defaults introduced.
  4. No bare except — checked by search; none in scoped files.
  5. No magic numbers — edited numerics named and cited (`lambda_tolerance`, rich-DTC gates, response truncation limits, override stubs, warmed-gate copy).
  6. f-strings — only used for the existing warmed-gate remediation string.
  7. Pathlib — `HorizonContextInjector` now uses `Path.open()`.
  8. Context managers — mask YAML load remains under `with`.
  9. `is None` — checked by search; no `== None` / `!= None`.
  10. Sorted imports — ruff clean.

Status: DONE — flipping VAULT ledger row to done.

CODE REVIEW — T-COM-CODE-CLEAN-C
================================
1. Design rules:        PASS — no cross-lab imports, no raw-sensor/DTC/chemistry re-derivation added, no signal/noise surface added.
2. Scope compliance:    PASS — source edits are limited to the five non-router core files; required progress/ledger metadata only outside source scope.
3. Contracts:           PASS — no schema, enum, Pydantic field, public behavior, or flag default changed; module export surfaces are explicit.
4. Docstrings:          PASS — public symbols remain documented; perception result qualifier wording fixed.
5. Wiki provenance:     PASS — new numeric constants carry `# wiki:` or `lld:` source comments.
6. Immediate Checklist: PASS — no mutable defaults, bare excepts, prints, `None` equality, star imports, cross-lab imports, or banned v6 enum names found.
7. Test coverage:       PASS — full COMLab pytest passed with expected `509 passed, 4 skipped`; changes are annotation/comment/constant-extraction legibility only.
8. Structural craft:    PASS with notes — seams are now explicit via `__all__`, typed routing directives, named thresholds, and `# WHY:` gate comments. `_build_execution_meta(...)` extraction remains a possible future duplication cleanup, but not required for this no-behavior audit.

Verdict: CLEAN
Blockers: none
