"""Extract wired OpenTelemetry traces from Jaeger REST into a local run folder."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

JAEGER_BASE_URL = "http://localhost:16686"
SERVICE_NAME = "4dlab-wired-harness"
LOOKBACK = "15m"
LIMIT = 600
TRACE_ROOT = Path(__file__).resolve().parent
RUNS_DIR = TRACE_ROOT / "runs"


def _timestamp() -> str:
    """Return the UTC timestamp used for one extraction run directory."""
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S")


def _normalise_base_url(base_url: str) -> str:
    """Return a Jaeger base URL without a trailing slash."""
    return base_url.rstrip("/")


def _build_url(
    *,
    base_url: str,
    service: str,
    lookback: str,
    limit: int,
    trace_id: str | None,
) -> str:
    """Build the Jaeger REST URL for a direct trace or service query."""
    root = _normalise_base_url(base_url)
    if trace_id:
        quoted_trace_id = urllib.parse.quote(trace_id, safe="")
        return f"{root}/api/traces/{quoted_trace_id}"

    query = urllib.parse.urlencode(
        {
            "service": service,
            "lookback": lookback,
            "limit": str(limit),
        }
    )
    return f"{root}/api/traces?{query}"


def _read_json_url(url: str) -> Any:
    """Read and decode one Jaeger JSON response."""
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"failed to query Jaeger at {url}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Jaeger returned invalid JSON at {url}: {exc}") from exc


def _extract_trace_list(payload: Any) -> list[dict[str, Any]]:
    """Return the Jaeger ``data`` trace list from supported response shapes."""
    if isinstance(payload, list):
        return cast(list[dict[str, Any]], payload)
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return cast(list[dict[str, Any]], data)
        if isinstance(data, dict):
            return [cast(dict[str, Any], data)]
    raise RuntimeError(f"unexpected Jaeger response shape: {type(payload).__name__}")


def query_jaeger(
    *,
    base_url: str = JAEGER_BASE_URL,
    service: str = SERVICE_NAME,
    lookback: str = LOOKBACK,
    limit: int = LIMIT,
    trace_id: str | None = None,
) -> list[dict[str, Any]]:
    """Query Jaeger REST and return trace payloads."""
    url = _build_url(
        base_url=base_url,
        service=service,
        lookback=lookback,
        limit=limit,
        trace_id=trace_id,
    )
    return _extract_trace_list(_read_json_url(url))


def _trace_sort_key(trace: Mapping[str, Any]) -> int:
    """Return the newest span start timestamp for stable trace ordering."""
    spans = trace.get("spans", [])
    if not isinstance(spans, list):
        return 0
    starts = [int(span.get("startTime", 0)) for span in spans if isinstance(span, Mapping)]
    return max(starts, default=0)


def _extract_services_ops(traces: Sequence[Mapping[str, Any]]) -> tuple[list[str], list[str]]:
    """Return sorted Jaeger service names and operation names from traces."""
    services: set[str] = set()
    operations: set[str] = set()
    for trace in traces:
        processes = trace.get("processes", {})
        if isinstance(processes, Mapping):
            for process in processes.values():
                if isinstance(process, Mapping):
                    service = process.get("serviceName")
                    if service:
                        services.add(str(service))

        spans = trace.get("spans", [])
        if isinstance(spans, list):
            for span in spans:
                if isinstance(span, Mapping):
                    operation = span.get("operationName")
                    if operation:
                        operations.add(str(operation))
    return sorted(services), sorted(operations)


def _write_json(path: Path, payload: Any) -> None:
    """Write deterministic UTF-8 JSON."""
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_run_artifacts(
    traces: Sequence[dict[str, Any]],
    *,
    run_dir: Path,
) -> tuple[Path, Path, Path]:
    """Write raw traces plus service and operation indexes into ``run_dir``."""
    run_dir.mkdir(parents=True, exist_ok=True)
    sorted_traces = sorted(traces, key=_trace_sort_key, reverse=True)
    services, operations = _extract_services_ops(sorted_traces)

    raw_path = run_dir / "traces-raw.json"
    services_path = run_dir / "services.json"
    operations_path = run_dir / "operations.json"
    _write_json(raw_path, sorted_traces)
    _write_json(services_path, services)
    _write_json(operations_path, operations)
    return raw_path, services_path, operations_path


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Parse command-line arguments for one extraction run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace-id", help="Specific Jaeger trace id to extract.")
    parser.add_argument(
        "--service",
        default=os.getenv("OTEL_SERVICE_NAME", SERVICE_NAME),
        help=f"Jaeger service name. Default: {SERVICE_NAME}.",
    )
    parser.add_argument(
        "--jaeger-base",
        default=JAEGER_BASE_URL,
        help=f"Jaeger base URL. Default: {JAEGER_BASE_URL}.",
    )
    parser.add_argument(
        "--lookback",
        default=LOOKBACK,
        help=f"Jaeger service-query lookback window. Default: {LOOKBACK}.",
    )
    parser.add_argument(
        "--limit",
        default=LIMIT,
        type=int,
        help=f"Jaeger service-query trace limit. Default: {LIMIT}.",
    )
    parser.add_argument(
        "--timestamp",
        default=_timestamp(),
        help="Run directory timestamp. Defaults to current UTC time.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Extract Jaeger traces and print the emitted artifact paths."""
    args = _parse_args(argv)
    run_dir = RUNS_DIR / str(args.timestamp)
    traces = query_jaeger(
        base_url=str(args.jaeger_base),
        service=str(args.service),
        lookback=str(args.lookback),
        limit=int(args.limit),
        trace_id=args.trace_id,
    )
    if not traces:
        raise RuntimeError(
            f"Jaeger returned no traces for service={args.service!r} trace_id={args.trace_id!r}"
        )

    raw_path, services_path, operations_path = write_run_artifacts(traces, run_dir=run_dir)
    trace_ids = [str(trace.get("traceID", "<missing>")) for trace in traces]
    services, operations = _extract_services_ops(traces)

    print(f"run_dir={run_dir}")
    print(f"traces_raw={raw_path}")
    print(f"services={services_path}")
    print(f"operations={operations_path}")
    print(f"trace_count={len(traces)}")
    print(f"trace_ids={','.join(trace_ids)}")
    print(f"service_names={','.join(services)}")
    print(f"operation_names={','.join(operations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
