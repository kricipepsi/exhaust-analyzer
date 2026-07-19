# WTEST5 Trace Report — wired oil case

**Task:** [[T-WTEST-5_trace_extract_and_report]]  
**Date:** 2026-06-30  
**Trace source:** Jaeger REST `http://localhost:16686/api/traces/934b526f078a04b65521aeee8669b581`  
**Raw dump:** `apps/wired/trace/runs/WTEST5_20260630/traces-raw.json` (local run artifact; do not commit)  
**Baseline anchor:** [[T-WTEST-1_full_suite_green_baseline]] — 1991 passed, 16 skipped, 0 failed/errors.  
**Trace invariance anchor:** [[T-WTEST-4_otel_run_spans_to_jaeger]] — traced MW-002 verdict bytes matched the untraced verdict.

## Extracted trace

| Field | Value |
|---|---|
| Service | `4dlab-wired-harness` |
| Case | `MW-002` |
| Trace ID | `934b526f078a04b65521aeee8669b581` |
| Root span | `wired.diagnose` |
| Total trace duration | `77.502 ms` |
| Span status summary | all extracted spans `OK` |
| Phase-of-failure readable | **yes** — the trace separates lab boundary spans from COMLab prune/rank spans; this case has no error phase. |

## Span tree

Durations are Jaeger microsecond durations converted to milliseconds.

```text
wired.diagnose  77.502 ms  OK  span=2774d6c5a039486b
├── lab.dnalab.build   0.484 ms  OK  span=0f4ab3706cf130c5
├── lab.gaslab.process 59.080 ms  OK  span=70001c8f66d98e02
└── comlab.process     17.390 ms  OK  span=ebcfea317a14baf2
    ├── phase.prune     0.368 ms  OK  span=8741133e0d236898
    └── phase.rank      0.197 ms  OK  span=93ef3540bde99da2
```

## Per-span detail

| Span | Parent | Duration | Status | Key attributes |
|---|---|---:|---|---|
| `wired.diagnose` | — | `77.502 ms` | `OK` | root composition span |
| `lab.dnalab.build` | `wired.diagnose` | `0.484 ms` | `OK` | VIN/DNA boundary ran |
| `lab.gaslab.process` | `wired.diagnose` | `59.080 ms` | `OK` | GASLab boundary ran |
| `comlab.process` | `wired.diagnose` | `17.390 ms` | `OK` | COMLab aggregation boundary ran |
| `phase.prune` | `comlab.process` | `0.368 ms` | `OK` | `router.candidates_in=73`, `router.candidates_out=14` |
| `phase.rank` | `comlab.process` | `0.197 ms` | `OK` | `router.candidates_in=14`, `router.candidates_out=1`, `router.winner_id=MW-002`, `router.winner_score=0.95`, `router.threshold_miss=false` |

## EXPECTED_SPANS check

`apps/wired/tests/test_tracing.py::EXPECTED_SPANS` defines six canonical spans:

| Expected span | Present in extracted MW-002 trace | Nesting result |
|---|---|---|
| `wired.diagnose` | yes | root |
| `lab.dnalab.build` | yes | child of `wired.diagnose` |
| `lab.gaslab.process` | yes | child of `wired.diagnose` |
| `lab.obdlab.translate` | not applicable to MW-002 | MW-002 fixture has no `obd` block; full optional-lab coverage is verified by `test_spans_emitted_when_enabled` |
| `lab.dtclab.sanitize` | not applicable to MW-002 | MW-002 fixture has no `dtc` block; full optional-lab coverage is verified by `test_spans_emitted_when_enabled` |
| `comlab.process` | yes | child of `wired.diagnose` |

Router child spans are nested under `comlab.process`: `phase.prune` and `phase.rank`.

## Findings

1. The extracted trace is readable offline: the raw JSON, service list, and operation list were written by `apps/wired/trace/extract_traces.py` to `apps/wired/trace/runs/WTEST5_20260630/`.
2. The oil-case phase split is visible: GASLab took `59.080 ms`, COMLab took `17.390 ms`, DNA took `0.484 ms`; router prune/rank sub-phases are visible under COMLab.
3. No span carried an error status. `phase.rank` selected `MW-002` at score `0.95` without a threshold miss.
4. This report does not run or import `ARCHIVE/_jaeger/analyse_failure_modes.py`; multi-case aggregation remains deferred to the future accuracy-harness pack.
