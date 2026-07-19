---
node_type: task
task_id: T-VIN-TESTPREP
status: done
pack: VAULT
lab: vinlab
mode: graph-tooling + coder lane
blocked_by:
- T-VIN-TESTS-GREEN
consumers:
- graph/v2_tests — AST test graph
- drift-guards.base — coverage view
tags:
- task
- vault
- vinlab
---

# T-VIN-TESTPREP — AST-legibility audit of the VINLab test suite (`4dlab-code-prep`, scoped to `tests/`)

**Status:** `done` · **Pack:** VAULT (VINLab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes under inner loop)
**Origin:** pipeline guide §3·1B + §4 (test prep) · **Blocked by:** T-VIN-TESTS-GREEN (done — `T-DNA-TH-2`)
**Consumer (signal/noise):** **Adds no schema field.** Produces a `file:line → rule → fix` audit report so
the `graph/v2_tests/` graph (built in `T-VIN-GRAPH-AST`) has accurate test-node labels and clean
`VERIFIES` / `drift_guards` edges. That test graph's consumer is the `drift-guards.base` view — every
`implements` target must have ≥1 guarding test or be marked untested.

### Role note ###

Same as CODEPREP: `4dlab-code-prep` **probes and reports**, never auto-rewrites and never runs graphify.
The coder applies fixes under the inner loop. **This run may fold into `T-VIN-CODEPREP`** if it returns
zero violations (mirror `T-DTC-TESTPREP`); note the fold in the progress note and the ledger.

### Scope ###

- **Tests only:** `labs/vinlab/tests/` — 15 `test_*.py` under `tests/unit/` (`test_decoder`, `test_models`,
  `test_air_metering`, `test_cylinder_heuristic`, `test_horizon`, `test_stress_rpm`, `test_switches`,
  `test_build`, `test_contract_conformance`, `test_csv_suite`, `test_decode_isolation`,
  `test_patch_regression`, `test_standalone`, `test_vindna_from_json`, `test_vindna_roundtrip`), plus
  `conftest.py` and `fixtures/`.
- **Excludes** the production package (`vinlab/` → `T-VIN-CODEPREP`).

### What the audit checks for the test corpus ###

Test names map to the real symbol/rule under test (so `VERIFIES` edges are accurate); explicit named
imports of the symbols exercised; no `from x import *`; the per-module isolation tests added by
`T-DNA-TH-2` (`test_horizon`, `test_stress_rpm`, `test_switches`, `test_decode_isolation`) read as direct
verifiers of their overlay modules. The mini-fixture `data_dir` builder (`make_mini_data_dir`) should be
importable and explicitly named, not constructed inline per test.

### Success criteria ###

1. `4dlab-code-prep` run scoped to `labs/vinlab/tests/`; report lists every violation as
   `file:line → rule → fix`, zero false positives spot-checked.
2. Any in-scope fixes applied; `pytest -x -q` stays green (173 vin tests, no skips); counts preserved.
3. Report confirms no `import *` in tests; each `test_*` maps to a real schema/rule it asserts.
4. No production-code edit; no graphify; no schema change. If zero violations, record the fold into
   CODEPREP.

### Out of scope ###

- The production package (→ `T-VIN-CODEPREP`) · running graphify (→ `T-VIN-GRAPH-AST`).
- Adding new test coverage — the isolation harness (`T-DNA-TH-2`) already closed the per-module gaps.

### Files to touch ###

- `labs/vinlab/tests/**/*.py` — only the audit-reported legibility fixes.
- The audit report appended to the progress note.

### Verification ###

```bash
cd <repo>/labs/vinlab
ruff check tests/ && pyright tests/ && pytest -x -q
grep -rn 'import \*' tests/ && echo "FAIL star-import" || echo "OK no star-import"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VIN-TESTPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / fixes applied or zero-violation fold / `pytest` green / counts
preserved) + `CODE REVIEW` (violations found vs fixed, fold decision). Ledger row → `done` only when both
are clean.
