from __future__ import annotations

import importlib
from copy import deepcopy
from typing import Any

from wired import diagnose
from wired.run_case import load_case
from wired.tracing import TRACE_ENV_VAR, is_opentelemetry_sdk_available

EXPECTED_SPANS = {
    "wired.diagnose",
    "lab.dnalab.build",
    "lab.gaslab.process",
    "lab.obdlab.translate",
    "lab.dtclab.sanitize",
    "comlab.process",
}


def _obd_inputs() -> dict[str, Any]:
    """Return a warm one-bank OBD sample that exercises the optional OBD lab call."""
    return {
        "engine_rpm": 800,
        "coolant_temp_c": 92.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 30.0,
        "intake_air_temp_c": 35.0,
        "shrtft1": -3.0,
        "longft1": -5.0,
        "number_of_banks": 1,
        "fuel_sys_status": "Closed_Loop",
        "pid_oxygen_sensor_volts": 0.45,
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }


def _raw_inputs_with_optional_labs() -> dict[str, Any]:
    """Return one fixture shaped to execute DNA, GAS, OBD, DTC, and COMLab spans."""
    raw_inputs = deepcopy(load_case("MW-003"))
    raw_inputs["obd"] = _obd_inputs()
    return raw_inputs


def _install_in_memory_exporter(monkeypatch: Any) -> Any:
    """Install an in-memory OpenTelemetry exporter for one test process."""
    if not is_opentelemetry_sdk_available():
        pytest_module = importlib.import_module("pytest")
        pytest_module.skip("opentelemetry-sdk is not installed in .venv-wired")

    trace_module = importlib.import_module("opentelemetry.trace")
    sdk_trace_module = importlib.import_module("opentelemetry.sdk.trace")
    sdk_export_module = importlib.import_module("opentelemetry.sdk.trace.export")
    in_memory_module = importlib.import_module(
        "opentelemetry.sdk.trace.export.in_memory_span_exporter"
    )

    monkeypatch.setattr(trace_module, "_TRACER_PROVIDER", None, raising=False)
    provider_once = getattr(trace_module, "_TRACER_PROVIDER_SET_ONCE", None)
    if provider_once is not None:
        monkeypatch.setattr(provider_once, "_done", False, raising=False)

    exporter = in_memory_module.InMemorySpanExporter()
    provider = sdk_trace_module.TracerProvider()
    provider.add_span_processor(sdk_export_module.SimpleSpanProcessor(exporter))
    trace_module.set_tracer_provider(provider)
    return exporter


def test_verdict_identical_traced_vs_untraced(monkeypatch: Any) -> None:
    """Tracing is observability only: it does not change the returned verdict bytes."""
    raw_inputs = load_case("MW-002")

    monkeypatch.delenv(TRACE_ENV_VAR, raising=False)
    untraced = diagnose(deepcopy(raw_inputs)).diagnostic_verdict.model_dump_json()

    monkeypatch.setenv(TRACE_ENV_VAR, "1")
    traced = diagnose(deepcopy(raw_inputs)).diagnostic_verdict.model_dump_json()

    assert traced == untraced


def test_spans_emitted_when_enabled(monkeypatch: Any) -> None:
    """WIRED_OTEL gates all spans: unset emits none, set emits the wired span tree."""
    exporter = _install_in_memory_exporter(monkeypatch)

    monkeypatch.delenv(TRACE_ENV_VAR, raising=False)
    diagnose(_raw_inputs_with_optional_labs())
    assert not exporter.get_finished_spans()

    monkeypatch.setenv(TRACE_ENV_VAR, "1")
    diagnose(_raw_inputs_with_optional_labs())

    emitted_names = {finished_span.name for finished_span in exporter.get_finished_spans()}
    assert EXPECTED_SPANS <= emitted_names
