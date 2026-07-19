# T-WTEST-5 — Progress Notes

## Plan
Task `[[T-WTEST-5_trace_extract_and_report]]`: add `apps/wired/trace/extract_traces.py` to query the live Jaeger REST API for service `4dlab-wired-harness` and dump `traces-raw.json`, `services.json`, and `operations.json` into an uncommitted `apps/wired/trace/runs/<timestamp>/` directory; write `apps/wired/test_tasks/reports/WTEST5_TRACE_2026-06-30.md`; update this note and `apps/wired/test_tasks/TEST_PROGRESS.md`. Verification will run the extractor against Jaeger, compile/ruff/pyright the new Python, confirm the six `apps/wired/tests/test_tracing.py::EXPECTED_SPANS` are present and nested under `wired.diagnose`, and confirm no `ARCHIVE/`, `wired/`, lab, COMLab, `graphify`, or `Vault/` edits. AGENTS risk is limited to the `ARCHIVE/` reference scaffold: I will clone the REST-query pattern only and import nothing from `ARCHIVE/`.

## Jaeger extraction

Initial direct extraction of the T-WTEST-4 trace id `e72961acd660e386ec9537bacc0fc4e9` failed because Jaeger had been restarted and the in-memory trace was gone:

```text
RuntimeError: failed to query Jaeger at http://localhost:16686/api/traces/e72961acd660e386ec9537bacc0fc4e9: <urlopen error [Errno 111] Connection refused>
```

Per the task's restart rule, Jaeger was started from the T-WTEST-3 native binary and MW-002 was replayed through `apps/wired/trace/run_traced_case.py`.

Final extraction command:

```text
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python apps/wired/trace/extract_traces.py --trace-id 934b526f078a04b65521aeee8669b581 --timestamp WTEST5_20260630
```

Output:

```text
run_dir=/agent_workspace/apps/wired/trace/runs/WTEST5_20260630
traces_raw=/agent_workspace/apps/wired/trace/runs/WTEST5_20260630/traces-raw.json
services=/agent_workspace/apps/wired/trace/runs/WTEST5_20260630/services.json
operations=/agent_workspace/apps/wired/trace/runs/WTEST5_20260630/operations.json
trace_count=1
trace_ids=934b526f078a04b65521aeee8669b581
service_names=4dlab-wired-harness
operation_names=comlab.process,lab.dnalab.build,lab.gaslab.process,phase.prune,phase.rank,wired.diagnose
```

## Parsed span tree

```text
wired.diagnose  77.502 ms  OK  span=2774d6c5a039486b
├── lab.dnalab.build   0.484 ms  OK  span=0f4ab3706cf130c5
├── lab.gaslab.process 59.080 ms  OK  span=70001c8f66d98e02
└── comlab.process     17.390 ms  OK  span=ebcfea317a14baf2
    ├── phase.prune     0.368 ms  OK  span=8741133e0d236898
    └── phase.rank      0.197 ms  OK  span=93ef3540bde99da2
```

`phase.prune` attributes: `router.candidates_in=73`, `router.candidates_out=14`.  
`phase.rank` attributes: `router.candidates_in=14`, `router.candidates_out=1`, `router.winner_id=MW-002`, `router.winner_score=0.95`, `router.threshold_miss=false`.

## EXPECTED_SPANS check

The extracted MW-002 trace contains the four spans applicable to this fixture: `wired.diagnose`, `lab.dnalab.build`, `lab.gaslab.process`, `comlab.process`. They are correctly nested under `wired.diagnose`; `phase.prune` and `phase.rank` are correctly nested under `comlab.process`.

`lab.obdlab.translate` and `lab.dtclab.sanitize` are not emitted for MW-002 because the fixture has no `obd` or `dtc` block, matching the T-WTEST-4 note. Full six-name `EXPECTED_SPANS` coverage remains verified by `apps/wired/tests/test_tracing.py::test_spans_emitted_when_enabled`.

Report path: `apps/wired/test_tasks/reports/WTEST5_TRACE_2026-06-30.md`.

## Verification commands

```text
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/trace/extract_traces.py -> exit 0
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/trace/extract_traces.py -> OK
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/trace/extract_traces.py -> 0 errors, 0 warnings, 0 informations
cd /agent_workspace/apps/wired && /agent_workspace/.venv-wired/bin/python -m pyright . -> 0 errors, 0 warnings, 0 informations
env -u WIRED_OTEL -u OTEL_TRACES_EXPORTER -u OTEL_EXPORTER_OTLP_ENDPOINT -u OTEL_EXPORTER_OTLP_PROTOCOL -u OTEL_SERVICE_NAME -u OTEL_RESOURCE_ATTRIBUTES /agent_workspace/.venv-wired/bin/python -m pytest apps/wired/tests/test_tracing.py -q -> 2 passed
```

Artifact check: `apps/wired/trace/runs/WTEST5_20260630/` contains `traces-raw.json`, `services.json`, and `operations.json`; these are local extraction artifacts and are intentionally excluded from the owner commit block.

## VERIFICATION GATE — T-WTEST-5

```text
VERIFICATION GATE — T-WTEST-5
1. Compile : PASS  (apps/wired/trace/extract_traces.py py_compile)
2. Lint    : PASS  (ruff check apps/wired/trace/extract_traces.py -> OK)
3. Types   : PASS  (pyright apps/wired/trace/extract_traces.py -> 0 errors; pyright apps/wired/. -> 0 errors)
4. Tests   : PASS  (extract_traces.py --trace-id 934b526f078a04b65521aeee8669b581 -> run dir WTEST5_20260630; env-clean pytest apps/wired/tests/test_tracing.py -q -> 2 passed)
5. Contract: PASS  (raw trace/services/operations JSON written locally; report contains span tree, durations, statuses, total duration, nesting check, and phase-of-failure verdict; no ARCHIVE import/run; no graphify)
6. Orphan  : N-A   (no domain field/fault/consumer mapping added; report consumer is architect review of trace phase visibility)
Result: CLEAN
```

## CODE REVIEW — T-WTEST-5

```text
CODE REVIEW — T-WTEST-5
Scope         : PASS  (changed only apps/wired/trace/extract_traces.py, the WTEST5 Markdown report, this progress note, and TEST_PROGRESS.md)
Composition   : PASS  (no wired/lab/COMLab source edits; no diagnostic logic; no second-lab import changes; no deferred path; no graphify; no Vault edit)
Consumers     : PASS  (N/A for domain fields; report consumer is the architect's trace phase-visibility review)
Literals      : PASS  (no diagnostic/boundary numerics added; Jaeger URL/service/lookback/limit are task-pinned trace extraction configuration)
Docstrings    : PASS  (extract_traces.py has module and public helper/main docstrings)
Craft (WARN)  : depth=thin REST extractor only; deletion=no unused CLI args or retained probe artifacts; seam=trace extraction isolated under apps/wired/trace; interface=Jaeger REST public API plus public pytest tracing contract
Result: CLEAN
```
