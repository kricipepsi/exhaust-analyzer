"""Idempotent, env-gated OpenTelemetry tracer for COMLab.

Mirror of `4DLabWired/_jaeger/_tracer.py` — same contract, same singleton guard,
same no-op fallback. COMLab ships its own copy so it does not import from
`4DLabWired/` (preserves the no-cross-lab-imports invariant).

Contract (see `_wired_skills/wired-jaeger-tracing/SKILL.md` §2):

- `get_tracer(name)` returns a real tracer iff `OTEL_TRACES_EXPORTER` is set
  and the `opentelemetry` SDK imports cleanly. Otherwise it returns a local
  no-op tracer whose `start_as_current_span(...)` context manager yields a
  no-op span (zero allocations on the call site).
- The underlying `TracerProvider` is registered **once** per process
  (idempotent — singleton guard). Multiple callers (composition, harness,
  this COMLab mirror) never double-register an exporter.
- A first-time exporter connection failure logs a single WARNING and falls
  back to no-op semantics for the remainder of the process — a missing
  collector never breaks a harness run.

Consumer: T-W-JAEGER-3 (COMLab FaultAtlasRouter phase spans + rule_scored events
+ threshold_miss tag).
"""

from __future__ import annotations

import logging
import os
import threading
from contextlib import contextmanager
from typing import Any, Iterator

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# No-op fallback — minimum span/tracer protocol surface
# ---------------------------------------------------------------------------


class _NoOpSpan:
    """No-op span implementing the subset of the OTel Span API used by COMLab.

    Every method is a no-op; `is_recording()` returns False so unit tests can
    distinguish the no-op path from a real recording span without importing
    the OTel SDK.
    """

    __slots__ = ()

    def set_attribute(self, key: str, value: Any) -> None:  # noqa: ARG002
        return None

    def set_status(self, status: Any, description: str | None = None) -> None:  # noqa: ARG002
        return None

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:  # noqa: ARG002
        return None

    def record_exception(self, exception: BaseException, attributes: dict[str, Any] | None = None) -> None:  # noqa: ARG002
        return None

    def is_recording(self) -> bool:
        return False

    def end(self) -> None:
        return None


class _NoOpTracer:
    """No-op tracer. `start_as_current_span` yields a `_NoOpSpan`."""

    __slots__ = ()

    @contextmanager
    def start_as_current_span(
        self,
        name: str,  # noqa: ARG002
        **kwargs: Any,  # noqa: ARG002
    ) -> Iterator[_NoOpSpan]:
        yield _NoOpSpan()


# ---------------------------------------------------------------------------
# Singleton guard — provider is initialised at most once per process
# ---------------------------------------------------------------------------

_init_lock = threading.Lock()
_init_done = False
_real_tracing_active = False  # True iff the OTel SDK is wired and exporter is live


def _initialise_provider_once() -> bool:
    """Initialise the global `TracerProvider` exactly once per process.

    Returns True iff real OTel tracing is active after the call (provider
    registered, exporter constructed). Returns False on any failure — the
    caller then falls back to the no-op tracer for the rest of the process.
    """
    global _init_done, _real_tracing_active
    with _init_lock:
        if _init_done:
            return _real_tracing_active
        _init_done = True  # do not retry on subsequent calls — fail soft, once.

        try:
            # Lazy imports — only required when real tracing is requested.
            from opentelemetry import trace
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
                OTLPSpanExporter,
            )
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError as exc:
            logger.warning(
                "OTEL_TRACES_EXPORTER is set but the opentelemetry SDK is not "
                "installed (%s). Install with: "
                'pip install -e ".[tracing]" --break-system-packages. '
                "Falling back to no-op tracing for this process.",
                exc,
            )
            return False

        endpoint = os.environ.get(
            "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
        )
        service = os.environ.get("OTEL_SERVICE_NAME", "4dlab-wired-harness")

        try:
            current = trace.get_tracer_provider()
            if type(current).__name__ == "ProxyTracerProvider":
                provider = TracerProvider(
                    resource=Resource.create({"service.name": service})
                )
                provider.add_span_processor(
                    BatchSpanProcessor(
                        OTLPSpanExporter(endpoint=endpoint, insecure=True)
                    )
                )
                trace.set_tracer_provider(provider)
            # else: an outer caller already set the provider — leave it.
        except Exception as exc:  # noqa: BLE001 — observability must never break callers
            logger.warning(
                "OTel TracerProvider initialisation failed (%s). "
                "Falling back to no-op tracing for this process.",
                exc,
            )
            return False

        _real_tracing_active = True
        return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_NOOP_TRACER = _NoOpTracer()


def get_tracer(name: str) -> Any:
    """Return a tracer for `name`.

    Real tracer iff `OTEL_TRACES_EXPORTER` is set AND the OTel SDK is
    importable AND the provider initialises cleanly. No-op tracer otherwise.

    Idempotent — the underlying `TracerProvider` is registered at most once
    per process across all callers.
    """
    if not os.environ.get("OTEL_TRACES_EXPORTER"):
        return _NOOP_TRACER

    if not _initialise_provider_once():
        return _NOOP_TRACER

    # Lazy import — only reached when real tracing is active.
    from opentelemetry import trace

    return trace.get_tracer(name)


def _reset_for_tests() -> None:
    """Reset the singleton guard. Test-only — never call from production code.

    Used by tests to exercise the env-unset and env-set paths in a single
    process. Does NOT tear down any registered OTel provider.
    """
    global _init_done, _real_tracing_active
    with _init_lock:
        _init_done = False
        _real_tracing_active = False
