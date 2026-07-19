# T-SYMGRAPH-3 — `4dlab-code-prep` audit + apply on `tests/`

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE
**Blocked by:** T-SYMGRAPH-1 (tests must be green + meaningful first)

### Goal ###

Run `4dlab-code-prep` **scoped to `labs/symptomlab/tests/`** (same `probe`→`audit`→`report`),
then apply the listed fixes, so the test package graphs cleanly into `v2_tests`
(T-SYMGRAPH-4). Proof of done: tests-scoped report clean, and `pytest` still green.

### Success criteria ###

- `4dlab-code-prep` report on `labs/symptomlab/tests/`: 0 outstanding AST-legibility
  violations (justify any exception).
- `ruff check labs/symptomlab/tests` + `pyright labs/symptomlab/tests` clean.
- `cd labs/symptomlab && pytest` still green.

### Context ###

Tests are `.py`, so they form their own Pass-1 AST graph tier (`v2_tests`). The same
AST-legibility levers apply (explicit imports, type hints on helpers/fixtures, named
fixtures over opaque tuples) so the extractor produces clean test→rule edges. This is the
**test-corpus run** that T-SYMGRAPH-2's production run deliberately excluded — do not
re-prep the production package here. Scope: `labs/symptomlab/tests/` (`unit/`, `fixtures/`,
`conftest.py`) — small, whole-read OK.

**Load skills:** `_skills\graph\4dlab-code-prep\SKILL.md` (the same skill, `tests/` scope).

### Consumer (signal/noise) ###

N/A — no new field/enum/fault; test-only legibility fixes.

### Deliverables ###

1. `labs/symptomlab/tests/**` — only the report's listed fixes.
2. The tests-scoped `4dlab-code-prep` report artefact.
3. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-3.md` — `## Plan` + report
   summary + before/after count.

### Files to touch ###

- `labs/symptomlab/tests/unit/*.py` (MODIFY — as report dictates)
- `labs/symptomlab/tests/conftest.py` / `fixtures/*` (MODIFY only if flagged)
- progress note (CREATE)

### Out of scope ###

Production package `labs/symptomlab/symptomlab/` (done in T-SYMGRAPH-2). No new assertions
or test logic (that was T-SYMGRAPH-1) — legibility fixes only. **GRAPH GUARDRAIL:** no
`graphify`, no `graph/` edits — not a KG-lane task. **Fold rule:** the test package is light
(`unit/` + `fixtures/` + `conftest.py`); if T-SYMGRAPH-2 is run in the same session and budget
allows, this may fold in as a second scoped prep pass — record that decision in the note.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2
# run 4dlab-code-prep probe/audit/report with scope = labs/symptomlab/tests
ruff check labs/symptomlab/tests
pyright labs/symptomlab/tests
cd labs/symptomlab && pytest -q
```

All steps pass; attach the report, confirm 0 outstanding violations.

### Progress hook ###

PROGRESS `T-SYMGRAPH-3`: Status=done, Files changed=<count>, Verification="tests code-prep 0 violations; pytest green".
