# T-COMTST-3 — COMLab generative layer (combinatorial + fuzz over categorical axes)

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4 (COMLab, LAST). **Type:** test-suite harness infra (no `comlab/` source change).
**Pack:** `T-COMTST-*`. **Blocked by:** T-COMTST-1 (descriptor). **Independent of** T-COMTST-2/4.
**Drill:** `START_HERE.md` → `ROADMAP.md` → `AGENTS.md` (five rules) → **this file**, then post the scope-confirm before any code.

> **One-line scope:** replace the two skipped generative stubs (`tests/generative/test_combinatorial.py`, `test_fuzz.py`, both currently `@pytest.mark.skip(reason="blocked: T-TST-10 comlab harness")`) with real generators over COMLab's **categorical** verdict axes, asserting **fail-closed / no-crash** for every generated combination. Remove the `T-TST-10` skip markers. This closes the reserved `T-TST-10` placeholder.

---

### ⚠ Read first — categorical axes, and do not duplicate the wired gate

COMLab's descriptor is categorical (`boxes={}`, T-COMTST-1). The shared boundary/noise generators (`harness/harness/generators/boundary.py`, `noise.py`) target continuous `FaultBox` geometry and **do not apply** here — do not import or adapt them. The COMLab generative axes are the verdict enums: `DegradationLit` × `chemical_state` × `routing_tags` × `HorizonLit` (+ a small invalid/sentinel set for fuzz). The descriptor stub's own note stands: the **full-pipeline correctness** end-to-end gate is `apps/wired/harness/` (`T-TH-12`); this layer only asserts COMLab **never crashes and always fails closed** across the categorical product — it does not assert verdict correctness.

### Goal ###

Turn the two generative stubs into real tests. `test_combinatorial_comlab` enumerates the Cartesian product of the categorical axes (capped to a sane bound, e.g. a representative subset per axis) and asserts each assembled request runs through `LabPipelineAggregator.process()` to either a schema-valid `OrchestratorFinalUIOutput` or a clean fail-closed terminal — never an unhandled exception. `test_fuzz_comlab` feeds malformed/sentinel/out-of-range payloads (missing keys, `±127`/`999` sentinels, wrong enum strings, empty upstream blocks) and asserts the ingestion gate **fail-closes** (validation error or `FATAL_INCOMPLETE`) rather than raising. Proof it's done: both tests run (no `skip`) and pass; `grep -rn "T-TST-10" tests/` returns nothing.

### Success criteria ###

- `tests/generative/test_combinatorial.py::test_combinatorial_comlab` and `tests/generative/test_fuzz.py::test_fuzz_comlab` are **un-skipped** (no `@pytest.mark.skip`) and pass.
- Combinatorial: enumerates the categorical axes via `build_comlab_descriptor().fields` (T-COMTST-1) and asserts no-crash + fail-closed-or-valid for every generated case; the case count is bounded and printed.
- Fuzz: a fixed set of malformed/sentinel inputs each fail-close (caught `ValidationError` or `degradation_mode == "FATAL_INCOMPLETE"`); no unhandled exception escapes `process()`.
- No `T-TST-10` reference remains anywhere under `labs/comlab/tests/` (`grep -rn "T-TST-10" labs/comlab/tests/` is empty).
- Inner loop clean: `ruff check tests/generative/` → `pyright tests/generative/` → `pytest tests/generative/ -q`; whole suite stays green.

### Context ###

Stub locations and current bodies: `labs/comlab/tests/generative/test_combinatorial.py` and `test_fuzz.py` (each ~9 lines, a single skipped no-op). The categorical-lab generative reference is `labs/dtclab/tests/generative/test_combinatorial.py` and `test_fuzz.py` (dtclab is `boxes={}` too — its generators enumerate routing exemplars, not FaultBoxes; mirror that approach). Axis sources: `comlab/schemas/response.py::DegradationLit` (line 26), `HorizonLit` (line 25); `comlab/schemas/vocabulary.py` chemical-state + routing-tag enums; assembly via the T-COMTST-1 `build_args`. Sentinel values for fuzz: `±127`, `999` (the ambiguous sentinels named in `wiki/12_corpus_eval_discipline.md` §CONCEPT_CEILING) and the O₂-enum / DTC-regex gaps named in `wiki/12` §M3. **READ-NARROW:** read the dtclab generative templates and the enum literal lines by range only.

### Consumer (signal/noise) ###

`N/A — no new field/enum/fault.` Test-only; enumerates existing enums and the existing ingestion contract. No production schema surface added.

### Deliverables ###

1. `labs/comlab/tests/generative/test_combinatorial.py` — MODIFY; real categorical combinatorial generator, skip removed.
2. `labs/comlab/tests/generative/test_fuzz.py` — MODIFY; real malformed/sentinel fuzz, skip removed.

### Files to touch ###

- `labs/comlab/tests/generative/test_combinatorial.py` (MODIFY)
- `labs/comlab/tests/generative/test_fuzz.py` (MODIFY)

### Out of scope ###

Do **not** import or adapt the continuous boundary/noise generators (`harness/harness/generators/boundary.py`, `noise.py`) — categorical lab. Do **not** assert verdict **correctness** (no expected-output checks) — that is the wired gate (`T-TH-12`) and the F1/GATE_DATA accuracy harness, both separate. Do **not** add new generative files beyond the two existing stubs, touch `test_cases.py` (T-COMTST-2) or `regression/` (T-COMTST-4), or modify any `comlab/` source. Surgical-change rule applies. **GRAPH GUARDRAIL:** no `graphify` / graph rebuild.

### Verification ###

```bash
cd labs/comlab
# Python 3.14 ONLY — no 3.10/3.12/3.13 mixing. Pin every python/pytest call to the repo sandbox interpreter:
PY=../../.sandbox-py/bin/python3.14
"$PY" --version                          # must print Python 3.14.x — stop if not
ruff check tests/generative/
pyright tests/generative/                # pyrightconfig must pin pythonVersion 3.14
# both generative tests run (not skipped) and pass:
"$PY" -m pytest tests/generative/ -q -rs
# the T-TST-10 reservation is fully closed:
grep -rn "T-TST-10" tests/ ; test $? -ne 0 && echo "OK: no T-TST-10 left"
# whole suite still green:
"$PY" -m pytest -x -q
```

All steps must pass; the `-rs` flag must show **no skipped** generative tests.

### Progress hook ###

PROGRESS.md `T-COMTST-3`: Status=done, Files changed=2, Verification="generative combinatorial+fuzz un-skipped and green; T-TST-10 reservation closed"
