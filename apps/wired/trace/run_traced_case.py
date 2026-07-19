"""Run one wired oil case with live OTLP export into Jaeger.

This is a Linux/native clone of the archived Jaeger harness pattern. It registers
an OTLP ``TracerProvider`` in-process, enables ``WIRED_OTEL``, runs the public
``wired.diagnose()`` path, flushes spans, and queries Jaeger REST for the emitted
``wired.diagnose`` trace so the next task can extract it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any, cast

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from wired import diagnose
from wired.run_case import load_case
from wired.tracing import TRACE_ENV_VAR

SERVICE_NAME = "4dlab-wired-harness"
DEFAULT_CASE_ID = "MW-002"
DEFAULT_OTLP_ENDPOINT = "http://localhost:4317"
DEFAULT_JAEGER_API = "http://localhost:16686/api/traces"
_REQUIRED_BASE_SPANS = frozenset(
    {"wired.diagnose", "lab.dnalab.build", "lab.gaslab.process", "comlab.process"}
)
_OPTIONAL_SPANS_BY_INPUT = {
    "obd": "lab.obdlab.translate",
    "dtc": "lab.dtclab.sanitize",
}


def _verdict_bytes(raw_inputs: Mapping[str, Any]) -> bytes:
    """Return stable verdict JSON bytes for one ``diagnose()`` call."""
    verdict_json = diagnose(deepcopy(dict(raw_inputs))).diagnostic_verdict.model_dump_json()
    return verdict_json.encode("utf-8")


def _install_provider(endpoint: str, service: str) -> TracerProvider:
    """Register one OTLP provider for this short-lived process."""
    provider = TracerProvider(resource=Resource.create({"service.name": service}))
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
    )
    trace.set_tracer_provider(provider)
    return provider


def _required_spans(raw_inputs: Mapping[str, Any]) -> frozenset[str]:
    """Return the canonical span names expected for this fixture shape."""
    spans = set(_REQUIRED_BASE_SPANS)
    for input_key, span_name in _OPTIONAL_SPANS_BY_INPUT.items():
        if raw_inputs.get(input_key) is not None:
            spans.add(span_name)
    return frozenset(spans)


def _query_recent_traces(api_url: str, service: str) -> list[dict[str, Any]]:
    """Fetch recent traces for ``service`` from Jaeger REST."""
    query = urllib.parse.urlencode({"service": service, "lookback": "15m", "limit": "50"})
    with urllib.request.urlopen(f"{api_url}?{query}", timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return cast(list[dict[str, Any]], payload.get("data", []))


def _span_names(trace_payload: Mapping[str, Any]) -> set[str]:
    """Return operation names from one Jaeger trace payload."""
    spans = cast(list[Mapping[str, Any]], trace_payload.get("spans", []))
    return {str(span.get("operationName")) for span in spans}


def _find_trace(
    traces: Sequence[dict[str, Any]],
    *,
    required_spans: frozenset[str],
) -> dict[str, Any]:
    """Return the newest trace containing this run's required span set."""
    candidates: list[dict[str, Any]] = []
    for trace_payload in traces:
        spans = cast(list[Mapping[str, Any]], trace_payload.get("spans", []))
        if not spans:
            continue
        if required_spans <= _span_names(trace_payload):
            candidates.append(trace_payload)

    if not candidates:
        names_by_trace = [sorted(_span_names(trace_payload)) for trace_payload in traces[:5]]
        raise RuntimeError(
            "no recent Jaeger trace contained required spans "
            f"{sorted(required_spans)}; recent traces={names_by_trace}"
        )
    return max(
        candidates,
        key=lambda trace_payload: max(
            int(span.get("startTime", 0))
            for span in cast(list[Mapping[str, Any]], trace_payload.get("spans", []))
        ),
    )


def _parent_span_id(span_payload: Mapping[str, Any]) -> str | None:
    """Return the first parent span id from a Jaeger span payload."""
    references = cast(list[Mapping[str, Any]], span_payload.get("references", []))
    for reference in references:
        parent_span_id = reference.get("spanID")
        if parent_span_id is not None:
            return str(parent_span_id)
    return None


def _nested_children(trace_payload: Mapping[str, Any], required_spans: frozenset[str]) -> dict[str, str]:
    """Return required child span -> parent span mapping, validating nesting."""
    spans = cast(list[Mapping[str, Any]], trace_payload.get("spans", []))
    by_name = {str(span.get("operationName")): span for span in spans}
    diagnose_span = by_name.get("wired.diagnose")
    if diagnose_span is None:
        raise RuntimeError("trace is missing wired.diagnose")
    diagnose_span_id = str(diagnose_span.get("spanID"))

    parents: dict[str, str] = {}
    for span_name in sorted(required_spans - {"wired.diagnose"}):
        span_payload = by_name.get(span_name)
        if span_payload is None:
            raise RuntimeError(f"trace is missing {span_name}")
        parent_span_id = _parent_span_id(span_payload)
        parents[span_name] = parent_span_id or "<none>"
        if parent_span_id != diagnose_span_id:
            raise RuntimeError(
                f"{span_name} parent {parent_span_id!r} != wired.diagnose {diagnose_span_id!r}"
            )
    return parents


def main(argv: Sequence[str] | None = None) -> int:
    """Run one case, flush spans, and print Jaeger cross-reference evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default=DEFAULT_CASE_ID, help="Oil case ID to run.")
    parser.add_argument("--otlp-endpoint", default=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", DEFAULT_OTLP_ENDPOINT))
    parser.add_argument("--jaeger-api", default=DEFAULT_JAEGER_API)
    parser.add_argument("--service", default=os.getenv("OTEL_SERVICE_NAME", SERVICE_NAME))
    args = parser.parse_args(argv)

    raw_inputs = load_case(args.case)
    required_spans = _required_spans(raw_inputs)

    provider = _install_provider(args.otlp_endpoint, args.service)
    previous_gate = os.environ.pop(TRACE_ENV_VAR, None)
    untraced_verdict = _verdict_bytes(raw_inputs)

    os.environ[TRACE_ENV_VAR] = "1"
    traced_verdict = _verdict_bytes(raw_inputs)
    provider.shutdown()

    if previous_gate is None:
        os.environ.pop(TRACE_ENV_VAR, None)
    else:
        os.environ[TRACE_ENV_VAR] = previous_gate

    if traced_verdict != untraced_verdict:
        raise RuntimeError("traced verdict JSON differs from untraced verdict JSON")

    traces = _query_recent_traces(args.jaeger_api, args.service)
    trace_payload = _find_trace(traces, required_spans=required_spans)
    parents = _nested_children(trace_payload, required_spans)
    spans = cast(list[Mapping[str, Any]], trace_payload.get("spans", []))
    by_name = {str(span.get("operationName")): span for span in spans}
    diagnose_span = by_name["wired.diagnose"]

    print(f"case={args.case}")
    print(f"service={args.service}")
    print(f"trace_id={trace_payload.get('traceID')}")
    print(f"wired_diagnose_span_id={diagnose_span.get('spanID')}")
    print(f"verdict_json={traced_verdict.decode('utf-8')}")
    print("verdict_byte_match=true")
    print(f"required_spans={','.join(sorted(required_spans))}")
    print("nesting:")
    print("  wired.diagnose")
    for span_name in sorted(required_spans - {"wired.diagnose"}):
        print(f"    {span_name} parent={parents[span_name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
