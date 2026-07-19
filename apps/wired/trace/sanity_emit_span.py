"""Emit one Jaeger sanity span for the wired tracing profile.

Run after sourcing ``setup_env_wired.sh`` so ``OTEL_*`` and ``WIRED_OTEL`` are set.
This is a live-tool clone of the archived sanity emitter pattern: it builds its
own ``TracerProvider`` and shuts it down after one span so the batch processor
flushes before the process exits.
"""

from __future__ import annotations

import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

SERVICE_NAME = "4dlab-wired-harness"
DEFAULT_OTLP_ENDPOINT = "http://localhost:4317"


def main() -> None:
    """Emit a single span and flush it to the configured OTLP collector."""
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", DEFAULT_OTLP_ENDPOINT)
    service = os.environ.get("OTEL_SERVICE_NAME", SERVICE_NAME)

    provider = TracerProvider(resource=Resource.create({"service.name": service}))
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
    )
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("wired.trace.sanity")

    with tracer.start_as_current_span("sanity_check_span"):
        pass

    provider.shutdown()
    print(f"OK: emitted 1 span to {endpoint} as service={service!r}")
    print("Query: http://localhost:16686/api/traces?service=4dlab-wired-harness")


if __name__ == "__main__":
    main()
