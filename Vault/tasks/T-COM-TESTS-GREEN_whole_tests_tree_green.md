---
node_type: task
task_id: T-COM-TESTS-GREEN
status: done
pack: VAULT
lab: comlab
mode: coder lane
blocked_by: []
consumers:
- drift-guards.base — coverage view
- graph/v2_tests — AST test graph
tags:
- task
- vault
- comlab
---

# T-COM-TESTS-GREEN — whole `tests/` tree green AND type-clean + meaningful

**Status:** `done` · **Pack:** VAULT (COMLab) · **Mode:** coder lane (inner loop after every edit)
**Origin:** pipeline guide §3·1B (tests green + meaningful before they become the `v2_tests` graph)
**Blocked by:** — · **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`.
**Consumer (signal/noise):** **Adds no schema field.** The test tree becomes `graph/v2_tests/` (built in
`T-COM-GRAPH-AST`); its `VERIFIES`/`drift_guards` edges are read by `drift-guards.base`. Type-clean,
behaviour-asserting tests make those edges trustworthy.

### The gap (verified 2026-06-26) ###

`pytest` is **runtime-green** — `509 passed, 4 skipped` (the 4 skips are intentional phase-3 reservations in
`tests/unit/test_lab_pipeline_aggregator.py`, lines ~17/24/32/42 — leave them skipped). **But
`pyright tests/` reports 19 real type errors** that the standard COMLab inner loop (which checks
`pyright comlab/` only) never surfaced. Representative classes:

- Missing constructor args — `…calculated_engine_load_pct`, `freeze_frame_engine_rpm` (e.g.
  `test_fault_atlas_router.py:162`, `test_symptom_prior.py:109`, `test_tag_discriminator.py:112`).
- `None` passed where a model is required — `FaultAtlasRouter(kg=None, analytics=None)`
  (`test_fault_atlas_router_registry_select.py:19/30/40/52`).
- Optional member access — `"fault_id" is not a known attribute of "None"` (`test_tag_discriminator.py`,
  `test_symptom_prior.py:343`).
- A `str` passed to a `UUID4` `session_id` (`test_power_loss_analytics.py:78`); a list-variance mismatch
  on `routing_tags` (`test_tag_discriminator.py:120`).

### Goal ###

Resolve the 19 `pyright tests/` errors **without changing what each test asserts** — add the missing
required args/fixtures, type the `None` placeholders (use real minimal models or `cast`/`# type: ignore`
only where a deliberate negative-path input is being exercised, with a one-line WHY), fix the UUID/list
types. Tests must stay behaviour-asserting (not assertion-free no-crash shims).

### Success criteria ###

1. `"$PY" -m pyright --pythonpath "$PY" tests/` → **0 errors** (`$PY=../../.sandbox-py/bin/python3.14`).
2. `"$PY" -m pytest -q` → **509 passed, 4 skipped** (or more passed if a previously-skipped negative path is
   now typed) — **no test deleted or weakened to pass pyright**; the 4 phase-3 skips remain skipped.
3. `ruff check tests/` clean; `pyright comlab/` still clean (no production code changed for this).
4. Spot-check: each touched test still asserts real behaviour (a verdict/family/score), not just no-crash.

### Out of scope ###

- Production `comlab/` changes (this is a tests-only task) · adding new test cases (→ the `T-COMTST-*`
  harness pack, already `done`) · `registry/tests/` · graphify. **GRAPH GUARDRAIL:** no graphify.
- Surgical-change rule: every edit traces to a pyright fix; do not refactor tests beyond that.

### Files to touch ###

- `labs/comlab/tests/**/*.py` — only the type-fix edits.

### Verification ###

```bash
cd <repo>/labs/comlab && PY=../../.sandbox-py/bin/python3.14
"$PY" -m pyright --pythonpath "$PY" tests/      # expect 0 errors
"$PY" -m pytest -q                              # expect 509 passed, 4 skipped
ruff check tests/ && "$PY" -m pyright --pythonpath "$PY" comlab/   # both clean
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-TESTS-GREEN.md` opens with the confirmed `## Plan` (the 19 errors grouped
by fix-class); the run session fills `VERIFICATION GATE` (pyright tests/ 0 / pytest 509+4 / ruff clean /
no weakened assertions) + `CODE REVIEW` (errors fixed vs how, no assertion loss). Ledger row → `done` only
when both blocks are clean.
