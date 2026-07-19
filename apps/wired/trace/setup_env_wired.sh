# 4DLab wired — local OpenTelemetry profile for native Jaeger v2.
# Usage: source /agent_workspace/apps/wired/trace/setup_env_wired.sh
# Jaeger UI/REST: http://localhost:16686
# OTLP gRPC ingest: localhost:4317
# OTLP HTTP ingest: http://localhost:4318

if [ -n "${BASH_SOURCE:-}" ]; then
  _wired_trace_profile="${BASH_SOURCE[0]}"
else
  _wired_trace_profile="$0"
fi
_wired_trace_dir="$(cd "$(dirname "$_wired_trace_profile")" && pwd)"
_wired_root="$(cd "$_wired_trace_dir/.." && pwd)"
_workspace_root="$(cd "$_wired_trace_dir/../../.." && pwd)"

export OTEL_SERVICE_NAME="4dlab-wired-harness"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
export OTEL_TRACES_EXPORTER="otlp"
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=local,service.namespace=4dlab"
export WIRED_OTEL="1"

export PYTHONPATH="$_wired_root:$_workspace_root/labs/comlab:$_workspace_root/labs/dnalab:$_workspace_root/labs/dtclab:$_workspace_root/labs/gaslab:$_workspace_root/labs/obdlab:$_workspace_root/labs/symptomlab:$_workspace_root/labs/vinlab:$_workspace_root"

_wired_jaeger_status="OFFLINE"
if command -v curl >/dev/null 2>&1; then
  if curl --silent --fail --max-time 2 http://localhost:16686/ >/dev/null 2>&1; then
    _wired_jaeger_status="ONLINE"
  fi
else
  if (echo >/dev/tcp/127.0.0.1/16686) >/dev/null 2>&1; then
    _wired_jaeger_status="ONLINE"
  fi
fi

printf '%s\n' '--------------------------------------------------------'
printf '%s\n' '  4DLab wired Telemetry Profile Loaded'
printf '%s\n' '--------------------------------------------------------'
printf '  Service       : %s\n' "$OTEL_SERVICE_NAME"
printf '  OTLP endpoint : %s  (%s)\n' "$OTEL_EXPORTER_OTLP_ENDPOINT" "$OTEL_EXPORTER_OTLP_PROTOCOL"
printf '  WIRED_OTEL    : %s\n' "$WIRED_OTEL"
printf '  PYTHONPATH    : %s\n' "$PYTHONPATH"
printf '  Jaeger        : %s  (UI at http://localhost:16686)\n' "$_wired_jaeger_status"
printf '  Commands      : python apps/wired/trace/sanity_emit_span.py | open http://localhost:16686\n'
printf '%s\n' '--------------------------------------------------------'

unset _wired_trace_profile _wired_trace_dir _wired_root _workspace_root _wired_jaeger_status
