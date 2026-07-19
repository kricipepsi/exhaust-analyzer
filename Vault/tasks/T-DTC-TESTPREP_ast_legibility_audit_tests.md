---
node_type: task
task_id: T-DTC-TESTPREP
status: pending
pack: VAULT
lab: dtclab
mode: graph-tooling + coder lane
blocked_by:
- T-DTC-TESTS-GREEN
consumers:
- drift-guards.base — coverage view
- graph/v2_tests — AST test graph
tags:
- task
- vault
- dtclab
---

# T-DTC-TESTPREP — AST-legibility audit of the DTCLab test tree (`4dlab-code-prep`)

**Status:** `pending` · **Pack:** VAULT (DTCLab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes)
**Origin:** pipeline guide §4 (test-code prep) · **Blocked by:** T-DTC-TESTS-GREEN
**Consumer (signal/noise):** **Adds no schema field.** Makes `labs/dtclab/tests/` AST-legible so the
`graph/v2_tests/` graph (built in `T-DTC-GRAPH-AST`) forms accurate `VERIFIES` edges to package symbols.
Those edges are read by the vault's `drift-guards.base`. No new fields — structural audit of test code.

### Role note ###

Same as CODEPREP: `4dlab-code-prep` **probes then reports**; it does **not** auto-rewrite. The coder
applies fixes under the inner loop. Scoped to `tests/` only (the production package is `T-DTC-CODEPREP`).
The skill never writes `graph.json` and never runs graphify.

### Scope ###

- `labs/dtclab/tests/` only — `unit/`, `integration/`, `regression/`, `generative/`, `fixtures/`,
  `conftest.py`, `test_cases.py`, `scripts/`. 16 test files.
- **Excludes** the production package (`dtclab/`, → `T-DTC-CODEPREP`).

### Legibility levers for the test corpus ###

Explicit imports of the symbols under test (so `VERIFIES` edges resolve to real nodes); descriptive test
names that name the rule/threshold guarded; fixtures with typed return values where practical; no
`import *`. The goal is that each test's graph node clearly points at the package symbol it guards.

### Fold-in note ###

If the test tree is already clean (likely after `T-DTC-TESTS-GREEN`), this run needs **zero edits**:
record a spot-confirm table in the progress note and the ledger may mark this row "folded into
`T-DTC-CODEPREP`" (mirroring GASLab's `T-GAS-TESTPREP`). Do not invent edits to justify the task.

### Success criteria ###

1. `4dlab-code-prep` run scoped to `tests/`; report lists any violation as `file:line → rule → fix`.
2. Coder applies in-scope fixes (if any); `pytest -x -q` stays green; `ruff`/`pyright` on `tests/` clean.
3. Report confirms test↔symbol references are explicit enough for `VERIFIES` edge formation.
4. No behaviour change; no graphify run; no production-code edit.

### Out of scope ###

- Production package (→ `T-DTC-CODEPREP`) · running graphify (→ `T-DTC-GRAPH-AST`).
- Making vacuous tests green by weakening them — that is a TESTS-GREEN concern, already done.

### Files to touch ###

- `labs/dtclab/tests/**` — only audit-reported legibility fixes.
- The audit report appended to the progress note.

### Verification ###

```bash
cd <repo>/labs/dtclab
pytest -x -q
ruff check tests/ && pyright tests/
grep -rn 'import \*' tests/ && echo "FAIL star-import" || echo "OK no star-import"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-TESTPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / fixes or zero-edit spot-confirm / `pytest` green) + `CODE REVIEW`
(VERIFIES-edge readiness). Ledger row → `done` (or "folded into CODEPREP") only when the block is clean.
