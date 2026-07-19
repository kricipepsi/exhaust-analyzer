---
node_type: task
task_id: T-GAS-TESTS-GREEN
status: pending
pack: VAULT
lab: gaslab
mode: strict coder lane
blocked_by: []
consumers:
- drift-guards.base — coverage view
- graph/v2_tests — AST test graph
tags:
- task
- vault
- gaslab
---


# T-GAS-TESTS-GREEN — Make the whole GASLab `tests/` tree green and meaningful

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** STRICT coder lane (inner loop after every edit)
**Origin:** pipeline guide §3·1B + AUDIT_2026-06-10 AUD-1/AUD-2 · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field.** The test corpus *is* the consumer being made
ready: the whole `tests/` tree becomes the `graph/v2_tests/` graph in T-GAS-GRAPH-AST, whose nodes
back the `drift_guards` frontmatter the vault build derives (`drift-guards.base` coverage view, plan
§4). A test that does not collect contributes no `VERIFIES` edge — so a red collection is a
silent hole in the eventual coverage map. No new fields; this task only makes the existing suite run.

### Role note (coder lane) ###

This is real GASLab test code under the lab inner loop: `ruff` → `pyright` → `pytest -x -q` after
every meaningful edit. graphify does **not** run here (GASLab START_HERE §0). No diagnostic-logic
change — wiring + tiering only.

### Goal ###

Phase-1B exit criterion for the test corpus: a default `pytest -x -q` from `labs/gaslab` collects
**and** passes the whole `tests/` tree (today it is **red at collection**, 4 errors), and the heavy
generative tests are tiered so they do not dominate the fast inner loop.

### Background (from the audit) ###

`tests/generative/{boundary,combinatorial,noise,overlap}.py` import `from harness... import ...`.
The `harness` package is real at `harness/harness/` but the gaslab lab has **no mechanism**
to put it on the import path (no `conftest.py`, no `pyproject` `pythonpath`, not pip-installed), so a
default `pytest` errors before a single test runs (AUD-1). With `PYTHONPATH` set, all four collect and
pass. The generative files are also slow (25–42 s/file, AUD-2).

### Success criteria ###

1. **Collection clean:** `pytest -q` from `labs/gaslab` collects every file under `tests/` with **0
   collection errors** (no `ModuleNotFoundError: harness`). Fix via the minimal mechanism — a
   `conftest.py` or a `[tool.pytest.ini_options] pythonpath` line in `pyproject.toml` — **decide
   one** and record why in the progress note.
2. **Core stays green:** the 207-pass core figure is preserved (`tests/unit`, `tests/test_cases.py`,
   `tests/fixtures`); no core regression.
3. **Generative green when run:** the four generative files pass when collected (they already do with
   `harness` on path); `test_fuzz.py` skip-stub left as-is.
4. **Slow-tier decision (AUD-2):** the heavy generative tests are marked so the fast loop can skip
   them (e.g. `@pytest.mark.slow` + `-m "not slow"` default, or a separate path) — **pick one**, wire
   it, and state it; the default `pytest -x -q` inner loop must stay fast.
5. Inner loop clean: `ruff` + `pyright` + `pytest -x -q` all green.

### Out of scope (route to "Unplanned follow-ups", do not touch) ###

- AUD-3/4/6 schema-orphan removals (`number_of_banks`, `engine_displacement_liters`,
  `fuel_delivery_type`, `wrong_valve_timing_rule` rename) — separate GASLab diagnostic tasks, not
  this pipeline task. Do **not** fold them in ("while I'm here" is banned).
- Any change to `harness/` itself — only the gaslab-side import wiring.
- The ledger one-line note (AUD-7) — owner/ledger pass.

### Files to touch ###

- `labs/gaslab/tests/conftest.py` **or** `labs/gaslab/pyproject.toml` (`[tool.pytest.ini_options]`) — one mechanism.
- `labs/gaslab/tests/generative/*.py` — only the `slow` marker, if that tiering is chosen.

### Verification (inner loop) ###

```bash
cd <repo>/labs/gaslab
ruff check . && pyright
pytest -q            # expect: 0 collection errors across the whole tests/ tree
pytest -x -q -m "not slow"   # fast inner-loop path stays fast and green
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-TESTS-GREEN.md` opens with the confirmed `## Plan` (which mechanism,
which slow-tier); the run session fills `VERIFICATION GATE` (collection 0 errors, core 207 green,
generative green, fast loop fast) + `CODE REVIEW`. Ledger row flips to `done` only when both are clean.
