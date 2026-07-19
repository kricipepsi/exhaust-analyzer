---
node_type: task
task_id: T-DNAV-TESTPREP
status: pending
pack: VAULT
lab: dnalab
mode: graph-tooling + coder lane
blocked_by:
- T-DNAV-TESTS-GREEN
consumers:
- graph/v2_tests — AST test graph
- drift-guards.base — coverage view
tags:
- task
- vault
- dnalab
---

# T-DNAV-TESTPREP — AST-legibility audit of the DNALab test suite (`4dlab-code-prep`, scoped to `tests/`)

**Status:** `pending` · **Pack:** VAULT (DNALab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes under inner loop)
**Origin:** pipeline guide §3·1B + §4 (test prep) · **Blocked by:** T-DNAV-TESTS-GREEN (done — `T-DNA-TH-1`)
**Consumer (signal/noise):** **Adds no schema field.** Produces a `file:line → rule → fix` audit report so
the `graph/v2_tests/` graph (built in `T-DNAV-GRAPH-AST`) has accurate test-node labels and clean
`VERIFIES` / `drift_guards` edges. That test graph's consumer is the `drift-guards.base` view — every
`implements` target must have ≥1 guarding test or be marked untested.

### Role note ###

Same as CODEPREP: `4dlab-code-prep` **probes and reports**, never auto-rewrites and never runs graphify.
The coder applies fixes under the inner loop. **This run may fold into `T-DNAV-CODEPREP`** if it returns
zero violations (mirror `T-DTC-TESTPREP`); note the fold in the progress note and the ledger.

### Scope ###

- **Tests only:** `labs/dnalab/tests/` — 4 modules under `tests/unit/` (`test_assembly.py` [11 tests, the
  `T-DNA-TH-1` isolation cases via monkeypatched fakes], `test_assembly_integration.py` [1 test —
  `test_real_pipeline_smoke`, real sibling-lab pipeline], `test_models.py` [10], `test_vehicledna_roundtrip.py`
  [5]); plus `conftest.py` and `fixtures/`.
- **Excludes** the production package (`dnalab/` → `T-DNAV-CODEPREP`).

### What the audit checks for the test corpus ###

Test names map to the real symbol/rule under test (so `VERIFIES` edges are accurate — e.g.
`test_schema_version_constant`/`test_from_json_payload_rejects_wrong_schema_version` → `SCHEMA_VERSION` +
`VehicleDNA.from_json_payload`; `test_happy_path_composes_vehicle_dna_from_fakes` → `build_vehicle_dna`);
explicit named imports of the symbols exercised; no `from x import *`. The `T-DNA-TH-1` isolation
builders (`make_vin_dna` / `make_symptom_dna`) and the monkeypatched fakes should be importable from
`conftest.py`/`fixtures/` and explicitly named, not constructed inline per test. The
`test_real_pipeline_smoke` integration case reads as a distinct (non-isolated) verifier — its env-gated
skip must not be mistaken for a missing edge.

### Success criteria ###

1. `4dlab-code-prep` run scoped to `labs/dnalab/tests/`; report lists every violation as
   `file:line → rule → fix`, zero false positives spot-checked.
2. Any in-scope fixes applied; `pytest -x -q` stays green (~27 tests; `test_real_pipeline_smoke` skip
   expected when siblings absent); counts preserved.
3. Report confirms no `import *` in tests; each `test_*` maps to a real schema/rule it asserts.
4. No production-code edit; no graphify; no schema change. If zero violations, record the fold into
   CODEPREP.

### Out of scope ###

- The production package (→ `T-DNAV-CODEPREP`) · running graphify (→ `T-DNAV-GRAPH-AST`).
- Adding new test coverage — the isolation harness (`T-DNA-TH-1`) already closed the assembly gaps.

### Files to touch ###

- `labs/dnalab/tests/**/*.py` — only the audit-reported legibility fixes.
- The audit report appended to the progress note.

### Verification ###

```bash
cd <repo>/labs/dnalab
ruff check tests/ && pyright tests/ && pytest -x -q
grep -rn 'import \*' tests/ && echo "FAIL star-import" || echo "OK no star-import"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DNAV-TESTPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / fixes applied or zero-violation fold / `pytest` green / counts
preserved) + `CODE REVIEW` (violations found vs fixed, fold decision). Ledger row → `done` only when both
are clean.
