"""Env-gated OpenTelemetry span helpers for wired."""

from __future__ import annotations

import importlib
import importlib.util
import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

TRACE_ENV_VAR = "WIRED_OTEL"
_TRUTHY = {"1", "true", "yes", "on"}


def is_tracing_enabled() -> bool:
    """Return whether wired OpenTelemetry spans should be emitted."""
    return os.getenv(TRACE_ENV_VAR, "").strip().lower() in _TRUTHY


def is_opentelemetry_sdk_available() -> bool:
    """Return whether tests can install an in-memory OpenTelemetry exporter."""
    return (
        importlib.util.find_spec("opentelemetry.sdk.trace") is not None
        and importlib.util.find_spec("opentelemetry.sdk.trace.export") is not None
    )


@contextmanager
def span(name: str) -> Iterator[Any]:
    """Yield an active OpenTelemetry span when enabled, otherwise a no-op."""
    if not is_tracing_enabled():
        yield None
        return

    if importlib.util.find_spec("opentelemetry.trace") is None:
        yield None
        return

    trace_module = importlib.import_module("opentelemetry.trace")
    with trace_module.get_tracer("wired").start_as_current_span(name) as active_span:
        yield active_span
