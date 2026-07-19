# T-GAS-TESTS-GREEN - progress note

**Status:** `done` - **Pack:** VAULT (GASLab) - run session 2026-06-10
Task spec: `Vault/tasks/T-GAS-TESTS-GREEN_*.md` - Pack ledger: `Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`

## Plan

Scope confirmed: make the GASLab `tests/` corpus collectable and tiered for the
vault test graph consumer, without changing diagnostic logic or `harness/`.

Mechanism chosen: keep the lab-local `tests/conftest.py` import-path shim. It is
the minimal GASLab-side wiring, limits the harness path change to pytest
collection, and avoids packaging or cross-lab runtime imports.

Slow-tier chosen: mark the four heavy generative tests with `@pytest.mark.slow`
and set GASLab pytest `addopts = "-m 'not slow'"`. This keeps default
`pytest -x -q` fast while preserving an explicit `-m slow` path for the
generative corpus.

Files verified as task-owned:

- `labs/gaslab/tests/conftest.py`
- `labs/gaslab/pyproject.toml`
- `labs/gaslab/tests/generative/test_boundary.py`
- `labs/gaslab/tests/generative/test_combinatorial.py`
- `labs/gaslab/tests/generative/test_noise.py`
- `labs/gaslab/tests/generative/test_overlap.py`

## VERIFICATION GATE

All commands run from `labs/gaslab` with `py -3.14 -m ...`.

- `ruff check .` -> all checks passed.
- `pyright` -> 0 errors, 0 warnings, 0 informations.
- `pytest -q` -> 207 passed, 2 skipped, 4 deselected in 6.49s.
- `pytest -x -q -m "not slow"` -> 207 passed, 2 skipped, 4 deselected in 6.53s.
- `pytest -q tests/unit tests/test_cases.py tests/fixtures` -> 207 passed, 1 skipped in 6.61s.
- `pytest -q -m slow tests/generative/test_overlap.py` -> 1 passed in 0.92s.
- `pytest -q -m slow tests/generative/test_boundary.py` -> 1 passed in 31.29s.
- `pytest -q -m slow tests/generative/test_combinatorial.py` -> 1 passed in 51.00s.
- `pytest -q -m slow tests/generative/test_noise.py` -> 1 passed in 601.68s (0:10:01).

Collection is clean: default pytest imports the generative modules and deselects
the four slow tests with no `ModuleNotFoundError: harness`. Core remains at the
audited 207-pass figure. The heavy generative tests are green through the
explicit slow tier; `test_fuzz.py` remains the existing skip stub.

## CODE REVIEW

No diagnostic logic changed. The pytest wiring is lab-local and only mutates
`sys.path` during test collection. The slow marker is registered in
`pyproject.toml`, so marker use is not silent or warning-prone.

Review finding: the slow tier is intentionally not part of the default inner
loop because `test_noise.py` takes about 10 minutes by itself. That matches the
task's AUD-2 tiering goal and keeps the fast loop under 7 seconds on this run.

No graphify update was run: the task file explicitly forbids graphify as a
side-effect outside the sanctioned graph tasks.
