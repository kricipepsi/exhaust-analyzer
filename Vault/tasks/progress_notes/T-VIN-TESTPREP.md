# T-VIN-TESTPREP - progress note

**Status:** `done` - test audit/fix complete; ledger row closed.
Task spec: `Vault/tasks/T-VIN-TESTPREP_*.md` - Pack ledger: `Vault/tasks/VIN_VAULT_TASKS_START_HERE.md`

## Plan

Scope: `labs/vinlab/tests/**/*.py` only; production package, wiki/docs, graph dirs, and schema fields excluded.
Consumer is the future AST test graph `graph/v2_tests`, feeding the `drift-guards.base` coverage view through
clean test-node labels and explicit `VERIFIES` / guard edges. No graphify build/update/extraction in this task.

## 4dlab-code-ingest: vinlab/tests / audit report

Pre-check:
- `python -m ruff check tests`: passed.
- `python -m pyright tests`: passed, `0 errors`.
- `python -m pytest -x -q`: passed, `177 passed, 11 skipped`.
- Skip investigation found two in-repo path issues that hid real checked-in tests/fixtures.

Machine-checkable audit:

| file:line | rule | found | fix |
|---|---|---|---|
| `tests/unit/test_models.py:149` | C/I | dynamic `__import__("inspect")` hid the `inspect` dependency from static import extraction | added explicit `import inspect`; changed call to `inspect.getsource(m)` |
| `tests/unit/test_build.py:11` | verifier path | build artifact tests resolved package data under `tests/vinlab/data` | changed to `Path(__file__).parents[2] / "vinlab" / "data"` |
| `tests/unit/test_vindna_roundtrip.py:10` | fixture path | roundtrip parametrization looked under `tests/unit/fixtures`, producing an empty parameter set | changed to `Path(__file__).parents[1] / "fixtures" / "vindna_pre_refactor"` |

Rule summary:
- I: no star imports found in `tests/`.
- A: package marker files are test package markers only; no public test API export surface required.
- T: test functions/fixtures are not public package signatures; pyright reports `0 errors`.
- C: fixed the dynamic `__import__` call. The remaining `getattr(dna, dna_field)` in
  `tests/unit/test_csv_suite.py:205` is intentional table-driven field comparison against
  `COC_DB_COLUMNS`; it is reviewed and left unchanged.
- S: test symbols are statically named; AST scan found 19 Python files, 15 `test_*.py` modules,
  170 `test_*` functions, and 9 fixtures.
- Test-map spot check: `test_horizon`, `test_stress_rpm`, `test_switches`, and `test_decode_isolation`
  import and exercise their target overlay/decoder-isolation symbols directly.

## VERIFICATION GATE

- Audit scoped to `labs/vinlab/tests/`; one in-scope legibility fix applied.
- False skips removed:
  - `python -m pytest -q tests/unit/test_build.py -rs`: passed, `6 passed`.
  - `python -m pytest -q tests/unit/test_vindna_roundtrip.py -rs`: passed, `5 passed`.
- `python -m ruff check tests`: passed.
- `python -m pyright tests`: passed, `0 errors`.
- `python -m pytest -x -q`: passed, `188 passed, 4 skipped`.
- Star import check: `OK no star-import`.
- Production code untouched; graph directories untouched; no schema changes.

Gate status: clean for the test-scoped task.

## CODE REVIEW

Code changes are test-only: `test_no_pfi_in_codebase()` now imports `inspect` explicitly instead of calling
`__import__("inspect")`, and two path constants now resolve checked-in package data / roundtrip fixtures from
the actual test module location. This preserves production behavior and makes the dependency/fixture edges
visible to AST extraction.

Review result: no production-code edits, no coverage additions, and no graph build. The future `v2_tests` graph
should retain direct verifier labels for the overlay isolation tests and no star-import ambiguity.
