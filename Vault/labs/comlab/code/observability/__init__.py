"""Observability package — OpenTelemetry tracer mirror for COMLab.

The public import path intentionally remains the `_tracer` module:
`from comlab.observability import _tracer` is used by tracer reset tests, while
production callers import `get_tracer` from `comlab.observability._tracer`.
"""
from . import _tracer as _tracer


__all__ = ["_tracer"]
