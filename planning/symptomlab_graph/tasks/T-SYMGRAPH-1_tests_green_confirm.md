# T-SYMGRAPH-1 — Confirm `tests/` green and assertion-meaningful

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE · **Blocked by:** —

### Goal ###

Confirm `labs/symptomlab/tests/` runs green under the inner loop and that each unit test
**asserts a real `validator.py`/`models.py` rule** (not a bare construct/import smoke), so
that when the test corpus is graphed (T-SYMGRAPH-4) it produces meaningful `VERIFIES` edges
rather than dead nodes. Proof of done: `pytest` green and a one-line note per
`tests/unit/test_*.py` naming the rule it asserts.

### Success criteria ###

- `cd labs/symptomlab && pytest` exits 0 (all tests pass).
- `ruff check labs/symptomlab/tests` and `pyright labs/symptomlab/tests` clean.
- Every module in `labs/symptomlab/tests/unit/` has ≥ 1 assertion tied to a named
  validator/model rule (recorded in the progress note). Any pure-smoke test is either
  given a real assertion or logged as a known stub with a reason.

### Context ###

The test corpus becomes its own graph tier (`v2_tests`). The pipeline guide §1B requires
tests be "green and meaningful" before that tier is built — the assertions are what become
the graph's `VERIFIES` / `drift_guards` edges. Code-clean on the production package is
already DONE (owner), so this task touches **test files only**. Scope to read:
`labs/symptomlab/tests/` (`unit/`, `fixtures/`, `conftest.py`) — all small, whole-read OK.
Do **not** whole-read the production package; if a test references a rule, `grep -n` the
target in `labs/symptomlab/symptomlab/validator.py` and read ~40 lines.

### Consumer (signal/noise) ###

N/A — no new field/enum/fault. This task changes only test assertions, not schema.
(The downstream graph consumer of the *tests tier* is the future vault frontmatter
derivation; not in scope here.)

### Deliverables ###

1. `labs/symptomlab/tests/unit/*.py` — assertions added/tightened only where a test was
   pure-smoke (no behavioural change to production code).
2. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-1.md` — `## Plan` + the
   per-module rule map + verification headline.

### Files to touch ###

- `labs/symptomlab/tests/unit/*.py` (MODIFY — only if a test lacks a real assertion)
- progress note (CREATE)

### Out of scope ###

No edits to `labs/symptomlab/symptomlab/` (production code is clean — owner). No new test
modules, no new features, no fixture redesign beyond what a missing assertion needs. **GRAPH
GUARDRAIL:** do not run `graphify` or touch any `graph/` dir — this is not a KG-lane task.
**Fold rule:** if the suite is already green and every test is meaningful, record that and
note in the progress hook that execution may fold into T-SYMGRAPH-2 (don't burn a session on
a no-op).

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\symptomlab
ruff check tests
pyright tests
pytest -q
```

All steps must pass (exit 0). Paste the `pytest` summary line into the progress note.

### Progress hook ###

PROGRESS `T-SYMGRAPH-1`: Status=done, Files changed=<count>, Verification="pytest green; N unit modules mapped to rules".
