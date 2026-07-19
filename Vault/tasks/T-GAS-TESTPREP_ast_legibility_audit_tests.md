---
node_type: task
task_id: T-GAS-TESTPREP
status: pending
pack: VAULT
lab: gaslab
mode: graph-tooling + coder lane
blocked_by:
- T-GAS-TESTS-GREEN
consumers:
- drift-guards.base — coverage view
- graph/v2_tests — AST test graph
tags:
- task
- vault
- gaslab
---

# T-GAS-TESTPREP — AST-legibility audit of the GASLab `tests/` tree (`4dlab-code-prep`)

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** GRAPH-TOOLING + coder lane
**Origin:** pipeline guide §4 (test-code prep, scoped to `tests/`) · **Blocked by:** T-GAS-TESTS-GREEN
**Consumer (signal/noise):** **Adds no schema field.** Readies the test corpus so `graph/v2_tests/`
(built in T-GAS-GRAPH-AST) carries clean `VERIFIES` / `drift_guards` edges — the exact edges the vault
build turns into `drift_guards` frontmatter for the `drift-guards.base` coverage view (plan §4). A test
whose target is not AST-legible yields a vague or missing edge, i.e. a hole in the coverage map.

### Role note ###

Same lane as T-GAS-CODEPREP: `4dlab-code-prep` **audits/reports**, never auto-rewrites; the coder
applies fixes under the inner loop. Scoped to `tests/` as its **own** run (the package run excludes
tests). No graphify, no `graph.json`.

### Why blocked by T-GAS-TESTS-GREEN ###

The whole `tests/` tree must **collect** before it can be audited — today the generative subtree fails
collection (AUD-1). Auditing a tree that doesn't import is meaningless. **This task may fold into
T-GAS-CODEPREP** if the test prep turns out light (guide §7.2 "≈0–1; may fold into CODEPREP"); if
folded, mark this row `void — folded into T-GAS-CODEPREP` rather than `done`.

### Scope ###

- `labs/gaslab/tests/` only — `unit/`, `test_cases.py`, `fixtures/`, `generative/`, `conftest.py`.

### Success criteria ###

1. `4dlab-code-prep` run scoped to `tests/`; report lists `file:line → rule → fix` for test-legibility
   (explicit imports, named test functions/fixtures that map to real schema/rules so they become
   `VERIFIES` edges, no `import *`).
2. Coder applies in-scope fixes; `pytest -q` still collects the whole tree with **0 errors** and core
   **207 green**; generative tests still pass when run.
3. Tests map to real schema/rules (these become the `VERIFIES` / `drift_guards` edges in v2_tests) —
   spot-confirm a sample test → the GASLab rule/field it guards.
4. No graphify run; no schema field touched.

### Out of scope ###

- Fixing test *logic* or adding coverage — prep is legibility only.
- The harness import wiring + slow-tiering — that was T-GAS-TESTS-GREEN.
- Running graphify (→ T-GAS-GRAPH-AST).

### Files to touch ###

- `labs/gaslab/tests/**/*.py` — only audit-reported legibility fixes.

### Verification ###

```bash
cd <repo>/labs/gaslab
pytest -q            # 0 collection errors across tests/
ruff check tests/ && pyright tests/
grep -rn 'import \*' tests/ && echo "FAIL star-import" || echo "OK"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-TESTPREP.md` opens with the confirmed `## Plan` (or the fold decision);
the run session fills `VERIFICATION GATE` + `CODE REVIEW`. Ledger row flips to `done` (or `void — folded`)
only when resolved.
