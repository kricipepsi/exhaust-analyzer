---
node_type: task
task_id: T-COM-TESTPREP
status: done — folded into CODEPREP
pack: VAULT
lab: comlab
mode: graph-tooling + coder lane
blocked_by:
- T-COM-TESTS-GREEN
consumers:
- drift-guards.base — coverage view
- graph/v2_tests — AST test graph
tags:
- task
- vault
- comlab
---

# T-COM-TESTPREP — AST-legibility audit of the COMLab test tree (`4dlab-code-prep`, scoped to `tests/`)

**Status:** `done — folded into CODEPREP` · **Pack:** VAULT (COMLab) · **Mode:** GRAPH-TOOLING + coder lane
**Origin:** pipeline guide §4 (test-corpus prep) · **Blocked by:** T-COM-TESTS-GREEN
**Load skills:** `comlab-verification-loop`, **`4dlab-code-prep`**, **`comlab-vault-prep`**.
**Consumer (signal/noise):** **Adds no schema field.** Makes the test tree AST-legible so `graph/v2_tests/`
(built in `T-COM-GRAPH-AST`) has clean `VERIFIES`/`drift_guards` edges, read by `drift-guards.base`.

### Role note + fold option ###

Same audit-not-rewrite shape as `T-COM-CODEPREP`, scoped to `tests/`. `4dlab-code-prep` reports
`file:line → rule → fix`; the coder applies under the inner loop. **This run may fold into `T-COM-CODEPREP`**
(the DTC precedent returned zero test-tree violations) — if so, record it as folded in the note and ledger
rather than forcing a separate session. It never writes `graph.json` / runs graphify.

### Scope ###

- `labs/comlab/tests/` — `unit/`, `e2e/`, `integration/`, `generative/`, `regression/`, `fixtures/`,
  `conftest.py`, `test_cases.py`. **Excludes** `comlab/` package (→ `T-COM-CODEPREP`) and `registry/tests/`.
- Precondition: `T-COM-TESTS-GREEN` made `pyright tests/` clean — so the audit operates on type-clean tests.

### What the audit checks ###

Explicit named imports (no `import *` in test modules); fixtures and helpers named so graphify maps each
`test_*` to the symbol it `VERIFIES`; no cross-lab import sneaking into a fixture (the mocks
`tests/fixtures/mock_{gas,obd,dtc}_lab.py` mirror lab types **locally** — confirm they do not
`from gaslab import …`); test module/function names are descriptive node labels.

### Success criteria ###

1. `4dlab-code-prep probe → audit → report` run scoped to `labs/comlab/tests/`; violations listed as
   `file:line → rule → fix`; `registry/tests/` excluded.
2. Coder applies in-scope fixes (or report is clean → fold into CODEPREP); `"$PY" -m pytest -q` still
   509 passed / 4 skipped; `pyright tests/` still 0 errors; `ruff check tests/` clean.
3. Report confirms no `import *` in tests; no cross-lab import in fixtures; meaningful test names.
4. No behaviour change; no graphify run.

### Out of scope ###

- `comlab/` package (→ `T-COM-CODEPREP`) · `registry/tests/` (out of pack) · graphify · weakening any
  assertion. **GRAPH GUARDRAIL:** no graphify / graph rebuild.

### Files to touch ###

- `labs/comlab/tests/**/*.py` — only audit-reported legibility fixes (likely none).

### Verification ###

```bash
cd <repo>/labs/comlab && PY=../../.sandbox-py/bin/python3.14
grep -rn 'import \*' tests/ && echo "FAIL star-import" || echo "OK"
grep -rn 'from gaslab\|from obdlab\|from dtclab\|from dnalab' tests/fixtures/ && echo "FAIL cross-lab in fixtures" || echo "OK isolated"
"$PY" -m pytest -q   # 509 passed, 4 skipped
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-TESTPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean or folded / pytest 509+4 / fixtures isolated) + `CODE REVIEW` (violations
vs fixed). Ledger row → `done` (or `done — folded into CODEPREP`) only when the block is clean.
