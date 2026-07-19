# T-WIRE-1 — progress note

## Plan
Stand up the `wired` package and its composition entry point `diagnose(raw_inputs) -> OrchestratorFinalUIOutput` in `apps/wired/wired/composition.py`. Touch and create `apps/wired/pyproject.toml`, `apps/wired/wired/__init__.py`, `apps/wired/wired/composition.py`, `apps/wired/wired/registry_guard.py`, and `apps/wired/tests/test_composition.py`. Verification runs py_compile, ruff, pyright from `apps/wired`, and `pytest -x -q apps/wired/tests/test_composition.py`. No workspace rules are at risk.

## VERIFICATION GATE

VERIFICATION GATE — T-WIRE-1
1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/wired/composition.py apps/wired/wired/registry_guard.py apps/wired/wired/__init__.py apps/wired/tests/test_composition.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/ruff check apps/wired/wired apps/wired/tests` -> OK)
3. Types   : PASS  (`cd apps/wired && /agent_workspace/.venv-wired/bin/pyright . --pythonpath /agent_workspace/.venv-wired/bin/python` -> OK, 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired/tests/test_composition.py` -> 2 passed)
5. Contract: PASS  (`from wired import diagnose` import smoke OK; `air_metering_strategy` forwarded; `composition.py` has no `deferred`; `registry_guard.py` pins 73; `assert_registry_ready()` OK)
6. Orphan  : PASS  (consumer greps confirmed live reads in `fault_atlas_router.py`, `perception_contradiction.py`, `lab_pipeline_aggregator.py`, `ecu_hardware_checker.py`, `power_loss_analytics.py`, and `registry/integration_shim.py`)
Result: CLEAN

## CODE REVIEW

CODE REVIEW — T-WIRE-1
Scope         : PASS  (`pyproject.toml`, `wired/__init__.py`, `wired/composition.py`, `wired/registry_guard.py`, `tests/test_composition.py`, this progress note, and ledger only)
Composition   : PASS  (all multi-lab imports live under `apps/wired`; no lab edits; no `ARCHIVE`/`v2`/`v6` import; no deferred path)
Consumers     : PASS  (every lab->COMLab mapped field carries a specific `# consumer:` comment)
Literals      : PASS  (boundary literals carry `# wiki:` or `# dossier:` comments; registry guard count cites `REGISTRY_PROGRESS.md`)
Docstrings    : PASS  (public entry point, mappers, guard, and helpers documented)
Craft (WARN)  : thin composition seam; no diagnostic scoring in `wired`; high-idle mapper test targets the mapper because COMLab request is internal, while `diagnose()` itself is exercised through the public signature.
Result: CLEAN
