# T-COMTST-2 — COMLab CSV characterization net (test_cases.py)

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4 (COMLab, LAST). **Type:** test-suite harness infra (no `comlab/` source change).
**Pack:** `T-COMTST-*`. **Blocked by:** T-COMTST-1 (descriptor + `comlab_cases.csv`).
**Drill:** `START_HERE.md` → `ROADMAP.md` → `AGENTS.md` (five rules) → **this file**, then post the scope-confirm before any code.

> **One-line scope:** add `labs/comlab/tests/test_cases.py` — a parametrized **characterization net** (one pytest case per `comlab_cases.csv` row) that assembles the inbound request, runs `LabPipelineAggregator.process()`, and asserts **no crash + schema-valid `OrchestratorFinalUIOutput` + fail-closed on invalid input**, recording the observed verdict (`top_fault` / `fault_family` / `degradation_mode` / `confidence`). Expected columns are empty, so this is a regression net, **not** a correctness/accuracy gate.

---

### Goal ###

Mirror `labs/dtclab/tests/test_cases.py` for COMLab: a `pytest_generate_tests` hook parametrizes over every row of `tests/fixtures/comlab_cases.csv`, and `test_csv_cases_comlab(row)` builds the request via the T-COMTST-1 descriptor's `build_args`, runs the aggregator, and asserts the outcome is either a schema-valid `OrchestratorFinalUIOutput` **or** a clean fail-closed (validation error / `FATAL_INCOMPLETE`) — never an unhandled exception. Observed verdict fields are `print`-recorded for audit. Proof it's done: `pytest tests/test_cases.py -q` collects N cases (N = the row count pinned in T-COMTST-1) and all pass.

### Success criteria ###

- `tests/test_cases.py::test_csv_cases_comlab` exists and is parametrized one-per-CSV-row (ids derived from `case_id` + family), collecting exactly the T-COMTST-1 row count.
- Each case asserts: no unhandled exception; if a verdict is produced it `isinstance`-checks as `OrchestratorFinalUIOutput` with the contract fields present and correctly typed (`degradation_mode ∈ DegradationLit`, `confidence ∈ ConfidenceLit`, `fault_family ∈ FaultFamilyLit` or `no_fault`); invalid/short rows are **fail-closed** (caught validation error or `FATAL_INCOMPLETE`), not a crash.
- The row count assertion in the loader matches T-COMTST-1's CSV exactly (a mismatch fails loudly — prevents silent fixture drift).
- Inner loop clean: `ruff check tests/test_cases.py` → `pyright tests/test_cases.py` → `pytest tests/test_cases.py -q` all pass; the rest of the suite stays green.

### Context ###

Template: `labs/dtclab/tests/test_cases.py` (the `_load_csv_rows` / `pytest_generate_tests` / `_make_row_id` / `test_csv_cases_*` structure, including the `assert len(rows) == <N>` drift guard and the characterization-net docstring). Adapt the body to COMLab: assemble the request with `build_comlab_descriptor().build_args(row)` (T-COMTST-1) and run `entry_point`, rather than dtclab's `run_sanitize`. The fail-closed helper pattern is COMLab's three `DegradationLit` terminal states — reuse `comlab/schemas/response.py` `DegradationLit` (line 26) and the e2e assertion style in `tests/e2e/test_pipeline_round_trip.py`. **READ-NARROW:** read the dtclab template and the `response.py` literal lines by range; do not whole-read the wiki.

This is explicitly a **characterization** net (`gt_method=characterization`): the `expected_*` columns are empty by T-COMTST-1's design, so the test records observed behaviour and locks against crashes/schema breakage — it does **not** assert the verdict is *correct*. Correctness scoring is the separate accuracy harness gated on Phase-0 **F1**/**GATE_DATA** (`wiki/12_corpus_eval_discipline.md`), not this task.

### Consumer (signal/noise) ###

`N/A — no new field/enum/fault.` Test-only; consumes the T-COMTST-1 descriptor + CSV and the existing `OrchestratorFinalUIOutput` contract. Adds no production schema surface.

### Deliverables ###

1. `labs/comlab/tests/test_cases.py` — CREATE; parametrized characterization net over `comlab_cases.csv`.

### Files to touch ###

- `labs/comlab/tests/test_cases.py` (CREATE)

### Out of scope ###

Do **not** populate `expected_*` or add any pass/fail accuracy scoring (F1/GATE_DATA-gated, separate pack). Do **not** touch the generative stubs (T-COMTST-3) or `tests/regression/` (T-COMTST-4). Do **not** modify the descriptor or CSV from T-COMTST-1 except to fix a genuine defect found while wiring (record any such fix in PROGRESS.md "Unplanned follow-ups" if it widens scope). No `comlab/` source, registry, or KG changes. Surgical-change rule applies. **GRAPH GUARDRAIL:** no `graphify` / graph rebuild.

### Verification ###

```bash
cd labs/comlab
# Python 3.14 ONLY — no 3.10/3.12/3.13 mixing. Pin every python/pytest call to the repo sandbox interpreter:
PY=../../.sandbox-py/bin/python3.14
"$PY" --version                          # must print Python 3.14.x — stop if not
ruff check tests/test_cases.py
pyright tests/test_cases.py              # pyrightconfig must pin pythonVersion 3.14
# collects one case per CSV row and all pass:
"$PY" -m pytest tests/test_cases.py -q
# drift guard: row count assertion fires if the CSV count changed:
"$PY" -m pytest tests/test_cases.py -q -k "cases" | tail -3
# whole suite still green:
"$PY" -m pytest -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-COMTST-2`: Status=done, Files changed=1, Verification="test_cases.py characterization net — N cases collected, all green; suite green"
