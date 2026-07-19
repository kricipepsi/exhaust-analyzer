# T-COMTST-1 — COMLab harness descriptor + upstream-verdict cases fixture

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4 (COMLab, LAST). **Type:** test-suite harness infra (no `comlab/` source change).
**Pack:** `T-COMTST-*` — the COMLab lab-local test harness that the emitter labs already have (obd/dtc/gas: `descriptor.py` + `<lab>_cases.csv` + `test_cases.py` + `regression/`). Closes the reserved **`T-TST-10` "comlab harness"** placeholder referenced in the skipped generative stubs.
**Drill:** `START_HERE.md` → `ROADMAP.md` → `AGENTS.md` (five rules) → **this file**, then post the scope-confirm before any code.

> **One-line scope:** replace the `build_comlab_descriptor()` `NotImplementedError` stub with a real **categorical** `ModuleDescriptor` (no continuous FaultBox geometry) and add a hand-authored `tests/fixtures/comlab_cases.csv` whose rows are **assembled upstream-lab verdicts** (gas/obd/dtc payloads + metadata) — plus a `row → OrchestratorInboundRequest` builder. This is the data + descriptor layer only; the characterization net that consumes it is **T-COMTST-2**.

---

## ⚠ Read first — why COMLab's harness is shaped differently from obd/dtc/gas

The emitter labs project the **raw-sensor master corpus** (`apps/wired/harness/data/cases_petrol_master_v6.csv`) directly, because each consumes raw PIDs/gas/DTC cells. **COMLab does not.** Its sole entry point — `comlab/core/lab_pipeline_aggregator.py::LabPipelineAggregator.process()` — ingests the **four upstream labs' already-computed verdicts** validated against `comlab/schemas/ingestion.py::OrchestratorInboundRequest` (`gas_lab_output`, `obd_live_data`, `dtc_lab_output`, `symptom_dna`, `metadata`). Two consequences, both load-bearing for this pack:

1. **There is no `project_comlab_cases.py`.** A master-row → COMLab projection would require running the three upstream labs first — that is exactly the **wired full-chain integration gate** at `apps/wired/harness/` (`T-TH-12`). Per `TESTSUITE_MIGRATION_MAP.md` §5 and the `descriptor.py` stub note, COMLab's lab-local layer **must not duplicate that gate**. So COMLab's fixture is **assembled upstream verdicts**, authored from the existing mock builders, not a master projection.
2. **The descriptor is categorical.** `boxes={}` (like `labs/dtclab/tests/fixtures/descriptor.py`) — COMLab discriminates over enum verdict states (degradation mode, chemical state, routing tags, horizon), not continuous ranges. The boundary/noise generators do not apply; the combinatorial/fuzz axes are categorical (**T-COMTST-3**).

### Goal ###

Produce the COMLab `ModuleDescriptor` and the case-table fixture that the rest of the pack consumes. `build_comlab_descriptor()` returns a real descriptor (categorical `FieldRange`s over the upstream-verdict enums, `boxes={}`, with `build_args`/`entry_point`/`extract_expected`/`diff` wired to assemble and run `LabPipelineAggregator`). `tests/fixtures/comlab_cases.csv` holds ~20–30 hand-authored rows of assembled upstream verdicts spanning the degradation modes and the populated `FaultFamilyLit` families. Proof it's done: `.sandbox-py/bin/python3.14 -c "from tests.fixtures.descriptor import build_comlab_descriptor as b; d=b(); print(d.name, len(d.fields), len(d.boxes))"` prints `COMLab <n> 0` without raising, and the CSV loads with the declared row count.

### Success criteria ###

- `tests/fixtures/descriptor.py::build_comlab_descriptor()` returns a `ModuleDescriptor` (no longer raises `NotImplementedError`); `d.boxes == {}`; every `FieldRange` is categorical (`enum_values` set, no `min_`/`max_`).
- A new `tests/fixtures/comlab_cases.csv` exists with a header + N data rows (N pinned in the file's `gt_source` note), one column group per upstream payload + `metadata`, and **empty** `expected_*` columns (characterization — populated only if/when an accuracy harness lands behind F1/Gate-Data, out of scope here).
- `descriptor.build_args(row)` assembles a valid `OrchestratorInboundRequest` from a CSV row (reusing the mock-builder field shapes), and `descriptor.entry_point(...)` runs `LabPipelineAggregator(...).process()` returning an `OrchestratorFinalUIOutput` for at least the healthy-baseline row.
- Inner loop clean on every edited file: `ruff check .` → `pyright comlab/ tests/` → `pytest -x -q` (the existing suite stays green; no test consumes the new CSV yet — that is T-COMTST-2).

### Context ###

The emitter-lab template to mirror is `labs/dtclab/tests/fixtures/descriptor.py` (categorical lab, `boxes={}`, the `build_args`/`entry_point`/`extract_expected`/`diff` quartet) and `labs/dtclab/tests/test_cases.py` (next task's consumer). The assembled-request shape is already proven in `labs/comlab/tests/e2e/test_pipeline_round_trip.py::_make_request` (lines 29–50) — copy that assembly into `build_args`. Upstream payload field shapes come from the existing builders: `tests/fixtures/mock_gas_lab.py`, `mock_obd_lab.py`, `mock_dtc_lab.py`. The verdict enums to enumerate as `FieldRange`s are in `comlab/schemas/response.py` (`HorizonLit` line 25, `DegradationLit` line 26, `ConfidenceLit` line 27, `FaultFamilyLit` line 34) and `comlab/schemas/vocabulary.py`. Taxonomy/family truth: `wiki/05_fault_taxonomy.md`, `wiki/06_fault_atlas_families.md`; degradation/ingest gate: `wiki/02_lab_input_contract.md`, `wiki/07_pipeline_stages.md`. **READ-NARROW:** read the cited `_make_request` helper and the `response.py` literal blocks by line range — do not whole-read the wiki.

CSV row authoring: cover, at minimum, one row per populated `FaultFamilyLit` family that COMLab can actually emit from upstream verdicts (`lean_condition`, `rich_mixture`, `misfire`, `sensor_fault`, `ecu_fault`, `catalyst_failure`, `exhaust_leak`, `ignition_fault`, `mechanical_wear`, `cam_timing`, `non_starter`, `no_fault`), plus the three `DegradationLit` modes (`FULL_FUSION`, `GAS_DOMINANT`, `FATAL_INCOMPLETE`) and an `invalid_input` row. Reuse the named mock scenarios where one exists (e.g. `mock_gas_lab.healthy_baseline`, `ignition_misfire_heavy_hc`, `catalyst_overwhelmed`, `exhaust_air_leak`, `wrong_valve_timing`).

### Consumer (signal/noise) ###

- **Consumer:** the COMLab characterization net `tests/test_cases.py::test_csv_cases_comlab` (**added in T-COMTST-1's successor T-COMTST-2, same pack**) and the generative layer (T-COMTST-3), which read `build_comlab_descriptor()` + `comlab_cases.csv`.
- **Code path:** `descriptor.build_args` → `descriptor.entry_point` → `LabPipelineAggregator.process()`. This is test-only infra: **no new field/enum/fault is added to any `comlab/` schema or the KG/registry.** `N/A — no new production field/enum/fault.` (The CSV's empty `expected_*` columns are placeholders, not a schema widening.)

### Deliverables ###

1. `labs/comlab/tests/fixtures/descriptor.py` — replace the stub body with a real categorical `build_comlab_descriptor()` (+ the `build_args`/`entry_point`/`extract_expected`/`diff` helpers).
2. `labs/comlab/tests/fixtures/comlab_cases.csv` — CREATE; ~20–30 assembled-verdict rows, empty `expected_*`, `gt_source` documenting authoring provenance + pinned row count.

### Files to touch ###

- `labs/comlab/tests/fixtures/descriptor.py` (MODIFY — remove `NotImplementedError`)
- `labs/comlab/tests/fixtures/comlab_cases.csv` (CREATE)

### Out of scope ###

Do **not** add `tests/test_cases.py` (that is T-COMTST-2), touch the generative stubs (T-COMTST-3), or add `tests/regression/` (T-COMTST-4). Do **not** author a `scripts/project_comlab_cases.py` — COMLab has no master-row projection (see "Read first"). Do **not** populate the `expected_*` columns or add any accuracy/scoring logic — that is a separate harness gated on Phase-0 **F1** (registry consolidation) and **GATE_DATA** per `wiki/12_corpus_eval_discipline.md` §F1/§GATE_DATA; not this pack. Do **not** modify any `comlab/` source, the registry, or the KG. Surgical-change rule: every changed line traces to a Deliverable above; adjacent improvements go to PROGRESS.md "Unplanned follow-ups". **GRAPH GUARDRAIL:** do not run `graphify` / rebuild any graph.

### Verification ###

```bash
cd labs/comlab
# Python 3.14 ONLY — no 3.10/3.12/3.13 mixing. Pin every python/pytest call to the repo sandbox interpreter:
PY=../../.sandbox-py/bin/python3.14
"$PY" --version                          # must print Python 3.14.x — stop if not
ruff check tests/fixtures/descriptor.py
pyright tests/fixtures/descriptor.py     # pyrightconfig must pin pythonVersion 3.14
# descriptor builds and is categorical:
"$PY" -c "from tests.fixtures.descriptor import build_comlab_descriptor as b; d=b(); assert d.boxes=={}; print(d.name, len(d.fields), 'boxes', len(d.boxes))"
# fixture loads with the declared row count:
"$PY" -c "import csv; rows=list(csv.DictReader(open('tests/fixtures/comlab_cases.csv'))); print('rows', len(rows))"
# existing suite stays green:
"$PY" -m pytest -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-COMTST-1`: Status=done, Files changed=2, Verification="descriptor categorical (boxes=0) + comlab_cases.csv N rows load; existing suite green"
