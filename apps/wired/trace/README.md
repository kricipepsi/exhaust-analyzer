# wired trace profile

Live trace tooling for `apps/wired`. This directory is the Linux/native counterpart to the archived Windows `_jaeger` scaffold; it does not import from `ARCHIVE/` and does not contain Jaeger binaries or trace JSON.

## Backend location

The Jaeger v2 linux/amd64 binary for `T-WTEST-3` is host-local and outside the repo:

```text
/home/m/jaeger/jaeger-2.19.0-linux-amd64/jaeger
```

Pinned artifact:

```text
version: v2.19.0
archive: /home/m/jaeger/jaeger-2.19.0-linux-amd64.tar.gz
sha256: 26c965b1ae08a7888ed60b2deba9d899859e033df0e05075ebbd06653013d72a
```

## Bring up Jaeger

From any shell:

```bash
/home/m/jaeger/jaeger-2.19.0-linux-amd64/jaeger
```

Expected endpoints:

- Jaeger UI and REST API: `http://localhost:16686/`
- OTLP gRPC ingest: `localhost:4317`
- OTLP HTTP ingest: `http://localhost:4318`

Stop it with `Ctrl-C` in the terminal running the binary. If it was started in the background, stop that process explicitly before starting another copy.

## Source the wired profile

Dot-source the profile so exported variables persist in the current shell:

```bash
source /agent_workspace/apps/wired/trace/setup_env_wired.sh
```

The profile exports:

```text
OTEL_SERVICE_NAME=4dlab-wired-harness
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_TRACES_EXPORTER=otlp
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=local,service.namespace=4dlab
WIRED_OTEL=1
PYTHONPATH=<apps/wired + seven lab paths + workspace root>
```

It intentionally does not export `USE_V2_REGISTRY`: no live `apps/wired` source consumer reads that variable in the current tree.

## Sanity span

After Jaeger is running and the profile is sourced:

```bash
/agent_workspace/.venv-wired/bin/python /agent_workspace/apps/wired/trace/sanity_emit_span.py
```

Then query:

```text
http://localhost:16686/api/traces?service=4dlab-wired-harness
```

A successful response contains an operation named `sanity_check_span` under service `4dlab-wired-harness`.
