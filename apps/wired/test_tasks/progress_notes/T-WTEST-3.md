# T-WTEST-3 — progress note

## Plan

Scope confirmation: I am taking `T-WTEST-3` only. This task adds local tracing support under `apps/wired/trace/` and records evidence in `apps/wired/test_tasks/progress_notes/T-WTEST-3.md` plus the ledger row in `apps/wired/test_tasks/TEST_PROGRESS.md`; I will fetch a native linux/amd64 Jaeger v2 binary outside the repo under `~/jaeger/`, create `apps/wired/trace/setup_env_wired.sh`, `apps/wired/trace/sanity_emit_span.py`, and `apps/wired/trace/README.md`, then run UI/OTLP health checks, dot-source the profile, run the sanity emitter, query Jaeger REST for service `4dlab-wired-harness`, and run compile/ruff/pyright over touched Python/shell-facing files as applicable. AGENTS.md risk is avoiding `ARCHIVE/` imports, `graphify`, `Vault/`, and any `wired/`, lab, or COMLab source edit; this task adds no domain field/fault, and its named consumer is [[T-WTEST-4]].

## Jaeger binary

Downloaded outside the repo:

```text
archive=/home/m/jaeger/jaeger-2.19.0-linux-amd64.tar.gz
binary=/home/m/jaeger/jaeger-2.19.0-linux-amd64/jaeger
sha256=26c965b1ae08a7888ed60b2deba9d899859e033df0e05075ebbd06653013d72a
```

Version check:

```text
/home/m/jaeger/jaeger-2.19.0-linux-amd64/jaeger version
2026/06/30 12:00:14 application version: git-commit=48f1e46121d1c428a6c989d08e7d69df4bccae82, git-version=v2.19.0, build-date=2026-06-03T13:17:07Z
{"gitCommit":"48f1e46121d1c428a6c989d08e7d69df4bccae82","gitVersion":"v2.19.0","buildDate":"2026-06-03T13:17:07Z"}
```

Launch command used:

```text
/home/m/jaeger/jaeger-2.19.0-linux-amd64/jaeger
```

## Backend health checks

```text
UI: http://localhost:16686/ -> 200
OTLP gRPC: 127.0.0.1:4317 -> open
```

## Env profile proof

Command:

```text
cd /agent_workspace
. apps/wired/trace/setup_env_wired.sh; printf 'CHECK OTEL_SERVICE_NAME=%s WIRED_OTEL=%s OTEL_TRACES_EXPORTER=%s\n' "$OTEL_SERVICE_NAME" "$WIRED_OTEL" "$OTEL_TRACES_EXPORTER"
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
CHECK OTEL_SERVICE_NAME=4dlab-wired-harness WIRED_OTEL=1 OTEL_TRACES_EXPORTER=otlp
```

`USE_V2_REGISTRY` was not exported. `grep` found no live `apps/wired/wired` or `apps/wired/tests` consumer; the only hit was the `T-WTEST-3` task prompt asking for this check.

## Sanity span proof

Command:

```text
cd /agent_workspace
. apps/wired/trace/setup_env_wired.sh; /agent_workspace/.venv-wired/bin/python apps/wired/trace/sanity_emit_span.py
```

Output:

```text
OK: emitted 1 span to http://localhost:4317 as service='4dlab-wired-harness'
Query: http://localhost:16686/api/traces?service=4dlab-wired-harness
```

REST API proof:

```json
{
  "data": [
    {
      "traceID": "506e1253b7cd4c8508a059f0729c2b2a",
      "spans": [
        {
          "operationName": "sanity_check_span",
          "references": [],
          "tags": [
            {"key": "otel.scope.name", "type": "string", "value": "wired.trace.sanity"},
            {"key": "span.kind", "type": "string", "value": "internal"}
          ]
        }
      ],
      "processes": {
        "p1": {
          "serviceName": "4dlab-wired-harness",
          "tags": [
            {"key": "deployment.environment", "type": "string", "value": "local"},
            {"key": "service.namespace", "type": "string", "value": "4dlab"},
            {"key": "telemetry.sdk.language", "type": "string", "value": "python"}
          ]
        }
      }
    }
  ],
  "errors": null
}
```

## Verification commands

```text
bash -n apps/wired/trace/setup_env_wired.sh -> exit 0
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/trace/sanity_emit_span.py -> exit 0
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/trace/sanity_emit_span.py -> OK
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/trace/sanity_emit_span.py -> 0 errors, 0 warnings, 0 informations
cd /agent_workspace/apps/wired && /agent_workspace/.venv-wired/bin/python -m pyright . -> 0 errors, 0 warnings, 0 informations
```

## Artifact check

`glob` found no `apps/wired/trace/**/*.json`, `apps/wired/trace/**/*.html`, or `apps/wired/trace/**/jaeger*` files. The Jaeger binary and release archive remain outside the repo under `/home/m/jaeger/`.

## VERIFICATION GATE — T-WTEST-3

```text
VERIFICATION GATE — T-WTEST-3
1. Compile : PASS  (apps/wired/trace/sanity_emit_span.py py_compile; apps/wired/trace/setup_env_wired.sh bash -n)
2. Lint    : PASS  (ruff check apps/wired/trace/sanity_emit_span.py -> OK)
3. Types   : PASS  (pyright apps/wired/trace/sanity_emit_span.py -> 0 errors; pyright apps/wired/. -> 0 errors)
4. Tests   : PASS  (Jaeger UI 200; OTLP gRPC 4317 open; profile banner ONLINE; sanity_emit_span.py -> OK; REST query returned operationName=sanity_check_span for service=4dlab-wired-harness)
5. Contract: PASS  (v2.19.0 linux/amd64 binary outside repo; sha256 pinned; setup_env_wired.sh exports OTEL_* plus WIRED_OTEL=1 and Linux PYTHONPATH; README contains bring-up/teardown; USE_V2_REGISTRY dropped because no live apps/wired consumer reads it)
6. Orphan  : N-A   (no domain field/fault/consumer mapping added; named consumer is [[T-WTEST-4]])
Result: CLEAN
```

## CODE REVIEW — T-WTEST-3

```text
CODE REVIEW — T-WTEST-3
Scope         : PASS  (changed only apps/wired/trace/setup_env_wired.sh, apps/wired/trace/sanity_emit_span.py, apps/wired/trace/README.md, this progress note, and TEST_PROGRESS.md)
Composition   : PASS  (no wired/lab/COMLab source edits; no diagnostic logic; no second-lab import changes; no deferred path; no graphify)
Consumers     : PASS  (N/A for domain fields; trace profile consumer is [[T-WTEST-4]])
Literals      : PASS  (no diagnostic/boundary numerics added; Jaeger ports/service/env values are task-pinned trace configuration)
Docstrings    : PASS  (sanity_emit_span.py has module and public main() docstrings)
Craft (WARN)  : depth=thin local tooling only; deletion=no unused profile/env exports, USE_V2_REGISTRY intentionally omitted; seam=trace tooling isolated under apps/wired/trace; interface=sanity proof uses public OTLP/Jaeger REST path, not private internals
Result: CLEAN
```
