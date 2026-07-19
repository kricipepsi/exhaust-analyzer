# T-WTEST-4 — progress note

## Plan

Scope confirmation: I am taking `T-WTEST-4` only. This task adds `apps/wired/trace/run_traced_case.py`, records evidence in `apps/wired/test_tasks/progress_notes/T-WTEST-4.md`, and updates only the `T-WTEST-4` / unblocked `T-WTEST-5` rows in `apps/wired/test_tasks/TEST_PROGRESS.md`; I will run the MW-002 oil case through live `wired.diagnose()` with `WIRED_OTEL=1` and a locally registered OTLP `TracerProvider`, query Jaeger REST for service `4dlab-wired-harness`, verify the canonical `EXPECTED_SPANS` nesting and traced-vs-untraced verdict byte equality, then run `pytest apps/wired/tests/test_tracing.py -q`, compile/ruff/pyright on the touched Python file, and the wired outer gate. AGENTS.md risks are avoiding `ARCHIVE/` imports, `graphify`, `Vault/`, source/lab/COMLab edits, and retained span JSON/binary artifacts.

## Jaeger/profile proof

Command:

```text
cd /agent_workspace
. apps/wired/trace/setup_env_wired.sh; printf 'CHECK WIRED_OTEL=%s OTEL_TRACES_EXPORTER=%s OTEL_SERVICE_NAME=%s\n' "$WIRED_OTEL" "$OTEL_TRACES_EXPORTER" "$OTEL_SERVICE_NAME"
```

Output:

```text
--------------------------------------------------------
  4DLab wired Telemetry Profile Loaded
--------------------------------------------------------
  Service       : 4dlab-wired-harness
  OTLP endpoint : http://localhost:4317  (grpc)
  WIRED_OTEL    : 1
  PYTHONPATH    : /agent_workspace/apps/wired:/agent_workspace/labs/comlab:/agent_workspace/labs/dnalab:/agent_workspace/labs/dtclab:/agent_workspace/labs/gaslab:/agent_workspace/labs/obdlab:/agent_workspace/labs/symptomlab:/agent_workspace/labs/vinlab:/agent_workspace
  Jaeger        : ONLINE  (UI at http://localhost:16686)
  Commands      : python apps/wired/trace/sanity_emit_span.py | open http://localhost:16686
--------------------------------------------------------
CHECK WIRED_OTEL=1 OTEL_TRACES_EXPORTER=otlp OTEL_SERVICE_NAME=4dlab-wired-harness
```

## Traced MW-002 run

Command:

```text
cd /agent_workspace
. apps/wired/trace/setup_env_wired.sh; /agent_workspace/.venv-wired/bin/python apps/wired/trace/run_traced_case.py --case MW-002
```

Output tail:

```text
case=MW-002
service=4dlab-wired-harness
trace_id=e72961acd660e386ec9537bacc0fc4e9
wired_diagnose_span_id=6e0a714d487fb4af
verdict_json={"is_fault_detected":true,"fault_code":"MW-002","fault_name":"Worn valve stem seals: oil leaks past valve stem seals into combustion chamber under high vacuum (snap-throttle closed / deceleration). Produces WORN_VALVE_SEALS chemistry — transient HC plume, not steady-state elevation. Differentiated from ring wear (MW-001) by the transient/snap-throttle HC pattern vs steady elevated HC. v1 ERR-MW-004 reactivated (v1 was GAS_ONLY at 0.70). confidence_ceiling applied because this is the only WORN_VALVE_SEALS-gated rule in the competition group","fault_family":"mechanical_wear","display_headline":"Worn valve stem seals: oil leaks past valve stem seals into combustion chamber under high vacuum (snap-throttle closed / deceleration). Prod","confidence_score":0.95,"actionable_remediation":"See diagnostic verdict for next steps.","differential_siblings":[]}
verdict_byte_match=true
required_spans=comlab.process,lab.dnalab.build,lab.gaslab.process,wired.diagnose
nesting:
  wired.diagnose
    comlab.process parent=6e0a714d487fb4af
    lab.dnalab.build parent=6e0a714d487fb4af
    lab.gaslab.process parent=6e0a714d487fb4af
```

MW-002 has no `obd` or `dtc` block, so `lab.obdlab.translate` and `lab.dtclab.sanitize` are correctly absent for this fixture shape. The full six-name `EXPECTED_SPANS` set is covered by `apps/wired/tests/test_tracing.py::test_spans_emitted_when_enabled`, which uses an optional-lab fixture.

## Jaeger REST span proof

REST source: `GET http://localhost:16686/api/traces/e72961acd660e386ec9537bacc0fc4e9`.

```json
{
  "traceID": "e72961acd660e386ec9537bacc0fc4e9",
  "spans": [
    {"operationName": "comlab.process", "spanID": "37f2a0c3f72019ee", "parent": "6e0a714d487fb4af", "duration": 14603},
    {"operationName": "lab.dnalab.build", "spanID": "ef681ac8131a3647", "parent": "6e0a714d487fb4af", "duration": 447},
    {"operationName": "lab.gaslab.process", "spanID": "79de4cce96c5ef11", "parent": "6e0a714d487fb4af", "duration": 52303},
    {"operationName": "phase.prune", "spanID": "af0b454474aea3fe", "parent": "37f2a0c3f72019ee", "duration": 250},
    {"operationName": "phase.rank", "spanID": "9e55a78d730f48f3", "parent": "37f2a0c3f72019ee", "duration": 69},
    {"operationName": "wired.diagnose", "spanID": "6e0a714d487fb4af", "parent": null, "duration": 67801}
  ]
}
```

Nesting checked: `lab.dnalab.build`, `lab.gaslab.process`, and `comlab.process` are direct children of `wired.diagnose`; `phase.prune` and `phase.rank` are children of `comlab.process`.

## Verification commands

```text
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/trace/run_traced_case.py -> exit 0
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/trace/run_traced_case.py -> OK
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/trace/run_traced_case.py -> 0 errors, 0 warnings, 0 informations
cd /agent_workspace/apps/wired && /agent_workspace/.venv-wired/bin/python -m pyright . -> 0 errors, 0 warnings, 0 informations
```

Tracing tests were run from `/agent_workspace` with the sourced Jaeger profile variables explicitly removed so the test's own monkeypatch controls the environment:

```text
env -u WIRED_OTEL -u OTEL_TRACES_EXPORTER -u OTEL_EXPORTER_OTLP_ENDPOINT -u OTEL_EXPORTER_OTLP_PROTOCOL -u OTEL_SERVICE_NAME -u OTEL_RESOURCE_ATTRIBUTES /agent_workspace/.venv-wired/bin/python -m pytest apps/wired/tests/test_tracing.py -q
..                                                                       [100%]
pytest: 2 passed in 0.69s
```

Artifact check: `glob` found no `apps/wired/trace/**/*.json`, `apps/wired/trace/**/*.html`, or `apps/wired/trace/**/jaeger*` files. The native Jaeger process/binary remains outside the repo.

## VERIFICATION GATE — T-WTEST-4

```text
VERIFICATION GATE — T-WTEST-4
1. Compile : PASS  (apps/wired/trace/run_traced_case.py py_compile)
2. Lint    : PASS  (ruff check apps/wired/trace/run_traced_case.py -> OK)
3. Types   : PASS  (pyright apps/wired/trace/run_traced_case.py -> 0 errors; pyright apps/wired/. -> 0 errors)
4. Tests   : PASS  (run_traced_case.py --case MW-002 -> trace_id=e72961acd660e386ec9537bacc0fc4e9 and verdict_byte_match=true; env-clean pytest apps/wired/tests/test_tracing.py -q -> 2 passed)
5. Contract: PASS  (live Jaeger UI ONLINE; OTLP provider registered in apps/wired/trace/run_traced_case.py without ARCHIVE import; REST trace contains MW-002 fixture-eligible canonical spans nested under wired.diagnose; no wired/lab/COMLab source edits by this task)
6. Orphan  : N-A   (no domain field/fault/consumer mapping added; trace artifact consumer is [[T-WTEST-5]])
Result: CLEAN
```

## CODE REVIEW — T-WTEST-4

```text
CODE REVIEW — T-WTEST-4
Scope         : PASS  (changed only apps/wired/trace/run_traced_case.py, this progress note, and TEST_PROGRESS.md for the T-WTEST-4/T-WTEST-5 ledger rows)
Composition   : PASS  (no wired/lab/COMLab source edits; no diagnostic logic; no second-lab import changes; no deferred path; no graphify)
Consumers     : PASS  (N/A for domain fields; trace consumer is [[T-WTEST-5]])
Literals      : PASS  (no diagnostic/boundary numerics added; OTLP endpoint/service/default case are task-pinned trace configuration)
Docstrings    : PASS  (run_traced_case.py has module and public helper/main docstrings)
Craft (WARN)  : depth=thin local run harness only; deletion=no unused CLI args or retained artifacts; seam=provider bootstrap isolated under apps/wired/trace; interface=uses public wired.diagnose() via load_case fixture, plus Jaeger REST public API
Result: CLEAN
```
