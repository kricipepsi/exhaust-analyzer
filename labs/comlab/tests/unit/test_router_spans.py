"""Phase-span hierarchy tests for `FaultAtlasRouter.execute_triage_loop()` (T-W-JAEGER-3).

Three contract requirements from the task:

1. `test_router_emits_5_phase_hierarchy` — with an in-memory exporter, calling
   `execute_triage_loop()` against a fixed OrchestratorInboundRequest emits five
   child spans named `phase.prune`, `phase.obd_eval`, `phase.dtc_verify`,
   `phase.score`, `phase.rank` in that order, each child of
   `fault_atlas_router.execute_triage_loop`.

2. `test_rank_emits_rule_scored_events` — the rank span carries one
   `rule_scored` event per scored candidate, each with attributes `rule_id`,
   `score`, `matched_horizon`, `matched_chemistry`, `matched_obd`,
   `matched_dtc`.

3. `test_threshold_miss_tag` — using a fixture that produces a winner with
   score below `MIN_CONFIDENCE_THRESHOLD`, the rank span carries
   `router.threshold_miss=True` and `router.winner_id` equals the suppressed
   rule's `fault_id` (not `__NONE__`).

The exporter swap mirrors `test_composition_spans.py` — we patch
`comlab.observability._tracer._initialise_provider_once` to use
`SimpleSpanProcessor` + `InMemorySpanExporter` so we never need a live
Jaeger collector.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _spans_by_name(exporter: Any) -> dict[str, list[Any]]:
    """Group finished spans by name."""
    out: dict[str, list[Any]] = {}
    for span in exporter.get_finished_spans():
        out.setdefault(span.name, []).append(span)
    return out


# ---------------------------------------------------------------------------
# Singleton reset
# ---------------------------------------------------------------------------


@pytest.fixture
def _reset_tracer() -> Iterator[None]:
    """Reset the COMLab tracer singleton before and after each test."""
    from comlab.observability import _tracer
    _tracer._reset_for_tests()
    yield
    _tracer._reset_for_tests()


# ---------------------------------------------------------------------------
# Env-var fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def _otel_env_set(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set the env vars that turn on real tracing."""
    monkeypatch.setenv("OTEL_TRACES_EXPORTER", "otlp")
    monkeypatch.setenv("OTEL_SERVICE_NAME", "test-comlab-router-spans")


@pytest.fixture
def _threshold_relaxed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set MIN_CONFIDENCE_THRESHOLD to 0.0 so rules always pass the gate."""
    import comlab.core.fault_atlas_router as router_mod
    monkeypatch.setattr(router_mod, "MIN_CONFIDENCE_THRESHOLD", 0.0)


# ---------------------------------------------------------------------------
# In-memory exporter setup — mirrors test_composition_spans.py pattern
# ---------------------------------------------------------------------------


@pytest.fixture
def in_memory_exporter(
    _otel_env_set: None,
    _reset_tracer: Iterator[None],
    _threshold_relaxed: None,
    monkeypatch: pytest.MonkeyPatch,
) -> Any:
    """Patch the COMLab tracer init to use SimpleSpanProcessor + InMemorySpanExporter.

    Returns the exporter so tests can call `.get_finished_spans()`.
    """
    pytest.importorskip("opentelemetry")
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    from comlab.observability import _tracer

    exporter = InMemorySpanExporter()

    def _fake_init() -> bool:
        if _tracer._init_done:
            return _tracer._real_tracing_active
        _tracer._init_done = True
        current: Any = trace.get_tracer_provider()
        if type(current).__name__ == "ProxyTracerProvider":
            provider = TracerProvider(
                resource=Resource.create({"service.name": "test-router-spans"})
            )
            provider.add_span_processor(SimpleSpanProcessor(exporter))
            trace.set_tracer_provider(provider)
        elif hasattr(current, "add_span_processor"):
            current.add_span_processor(SimpleSpanProcessor(exporter))
        _tracer._real_tracing_active = True
        return True

    monkeypatch.setattr(_tracer, "_initialise_provider_once", _fake_init)

    return exporter


# ---------------------------------------------------------------------------
# Router fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def router(registry_path: Any) -> Any:
    """Module-scoped router — loaded once for all span tests."""
    from comlab.analytics.power_loss_analytics import PowerLossAnalytics
    from comlab.core.fault_atlas_kg import FaultAtlasKG
    from comlab.core.fault_atlas_router import FaultAtlasRouter

    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    return FaultAtlasRouter(str(registry_path), kg, analytics)


# ---------------------------------------------------------------------------
# Request builders
# ---------------------------------------------------------------------------


def _make_sanitized(
    chemical_state: str = "INCOMPLETE_OXIDATION",
    horizon: str = "HORIZON_LEGACY",
    confirmed_dtcs: list[str] | None = None,
    manifold_pressure_kpa: float = 65.0,
    barometric_pressure_kpa: float | None = 101.3,
) -> dict[str, Any]:
    """Build a minimal sanitized dict that routes to ERR-E1-M032 (EGR rule).

    The EGR stuck-open rule (ERR-E1-M032) targets HORIZON_LEGACY with
    INCOMPLETE_OXIDATION chemistry and requires manifold vacuum 30-50 kPa
    (vacuum = baro - manifold = 101.3 - 65.0 = 36.3 → in range).
    """
    from uuid import uuid4

    from comlab.schemas.ingestion import (
        DTCLabPayload,
        FreezeFrameRecord,
        GasLabPayload,
        OBDLiveDataPayload,
        OrchestratorInboundRequest,
        SessionMetadata,
    )
    from comlab.schemas.vocabulary import (
        DTCRoutingTag,
        EngineStateBucket,
        FuelSystemStatus,
        HistoricalFaultContext,
        NodeMAFStatus,
        NodeMAPStatus,
        O2FailureMode,
        SampleValidity,
        TrimAnalyticsGate,
        VEValidity,
        VinConfidence,
    )

    req = OrchestratorInboundRequest(
        metadata=SessionMetadata(
            session_id=uuid4(),
            vin_dna_string="1FA6P8CF0HXXXXXXX",
            resolved_horizon=horizon,
            cylinder_count=4,
            vin_confidence=VinConfidence.HIGH,
        ),
        gas_lab_output=GasLabPayload(
            chemical_state=chemical_state,
            gas_co=0.4,
            gas_hc=120,
            gas_co2=13.0,
            gas_o2=1.8,
            gas_nox=200,
            lambda_chem=1.04,
            sample_validity=SampleValidity.VALID,
        ),
        obd_live_data=OBDLiveDataPayload(
            engine_warmed=True,
            total_trim_correction_delta=0.0,
            normalized_obd_lambda=1.0,
            ve_pct=72.0,
            ve_validity=VEValidity.VALID,
            rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
            trim_analytics_gate=TrimAnalyticsGate.VALID,
            o2_failure_mode=O2FailureMode.STUCK_LEAN,
            maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
            map_status=NodeMAPStatus.REAL_SENSOR_FEED,
        ),
        dtc_lab_output=DTCLabPayload(
            active_mil=False,
            mil_flashing=False,
            confirmed_dtcs=confirmed_dtcs or ["P0401"],
            pending_dtcs=[],
            permanent_dtcs=[],
            routing_tags=[DTCRoutingTag.EGR_HISTORY],
            mode_06_monitors={},
            historical_fault_context=HistoricalFaultContext.UNKNOWN,
            freeze_frame=FreezeFrameRecord(
                calculated_load_pct=0.0,
                engine_rpm=0,
                coolant_temp_c=85.0,
                short_term_ft1=0.0,
                long_term_ft1=0.0,
                manifold_pressure_kpa=manifold_pressure_kpa,
                vehicle_speed_kmh=0,
                ignition_advance_deg=10.0,
                intake_air_temp_c=20.0,
                maf_gps=0.0,
                throttle_pos_pct=0.0,
                fuel_system_status=FuelSystemStatus.OL,
                o2_voltage_b1s1=None,
                barometric_pressure_kpa=barometric_pressure_kpa,
            ),
        ),
        symptom_dna={},
    )
    return {"request": req}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


_EXPECTED_PHASE_SPAN_NAMES = [
    "phase.prune",
    "phase.obd_eval",
    "phase.dtc_verify",
    "phase.score",
    "phase.rank",
]


def test_router_emits_5_phase_hierarchy(
    in_memory_exporter: Any,
    router: Any,
) -> None:
    """Running execute_triage_loop under tracing emits 5 child spans in order."""
    sanitized = _make_sanitized()
    verdict = router.execute_triage_loop(sanitized)
    assert verdict["winner"] is not None
    assert verdict["winner"].fault_id == "ERR-E1-M032"

    by_name = _spans_by_name(in_memory_exporter)
    span_names = set(by_name.keys())

    # Root span is present
    assert "fault_atlas_router.execute_triage_loop" in span_names, (
        f"Missing root span. Got: {sorted(span_names)}"
    )

    # All 5 phase spans are present
    for name in _EXPECTED_PHASE_SPAN_NAMES:
        assert name in span_names, (
            f"Missing phase span {name!r}. Got: {sorted(span_names)}"
        )

    # Parent-child: each phase span is a child of execute_triage_loop
    id_to_span: dict[int, Any] = {}
    for spans in by_name.values():
        for span in spans:
            id_to_span[span.context.span_id] = span

    root_spans = by_name["fault_atlas_router.execute_triage_loop"]
    assert len(root_spans) == 1
    root_id = root_spans[0].context.span_id

    for name in _EXPECTED_PHASE_SPAN_NAMES:
        for span in by_name[name]:
            assert span.parent is not None, (
                f"Phase span {name!r} has no parent"
            )
            assert span.parent.span_id == root_id, (
                f"Phase span {name!r} parent is not the root span"
            )

    # Phases appear in order (sorted by start_time)
    phase_order = [
        span.name for span in sorted(
            in_memory_exporter.get_finished_spans(),
            key=lambda s: s.start_time or 0,
        )
        if span.name in _EXPECTED_PHASE_SPAN_NAMES
    ]
    assert phase_order == _EXPECTED_PHASE_SPAN_NAMES, (
        f"Phase spans out of order: {phase_order}"
    )

    # Verify router.candidates_in/out on each phase span
    for name in _EXPECTED_PHASE_SPAN_NAMES:
        for span in by_name[name]:
            attrs = span.attributes or {}
            assert "router.candidates_in" in attrs, (
                f"Phase span {name!r} missing router.candidates_in"
            )
            assert "router.candidates_out" in attrs, (
                f"Phase span {name!r} missing router.candidates_out"
            )
            assert isinstance(attrs["router.candidates_in"], int)
            assert isinstance(attrs["router.candidates_out"], int)


def test_rank_emits_rule_scored_events(
    in_memory_exporter: Any,
    router: Any,
) -> None:
    """The rank span carries one rule_scored event per scored candidate."""
    sanitized = _make_sanitized()
    verdict = router.execute_triage_loop(sanitized)
    assert verdict["winner"] is not None

    by_name = _spans_by_name(in_memory_exporter)
    rank_spans = by_name.get("phase.rank", [])
    assert len(rank_spans) == 1, (
        f"Expected 1 rank span, got {len(rank_spans)}"
    )
    rank_span = rank_spans[0]

    events = rank_span.events or []
    scored_events = [e for e in events if e.name == "rule_scored"]
    assert len(scored_events) >= 1, (
        f"Expected ≥1 rule_scored events, got {len(scored_events)}"
    )

    for event in scored_events:
        attrs = event.attributes or {}
        assert "rule_id" in attrs, f"rule_scored event missing rule_id: {attrs}"
        assert attrs["rule_id"].startswith("ERR-"), (
            f"rule_id should start with ERR-: {attrs['rule_id']}"
        )
        assert "score" in attrs
        assert isinstance(attrs["score"], float)
        assert "matched_horizon" in attrs
        assert "matched_chemistry" in attrs
        assert "matched_obd" in attrs
        assert "matched_dtc" in attrs


def test_prune_emits_rule_pruned_events(
    in_memory_exporter: Any,
    router: Any,
) -> None:
    """The prune span carries rule_pruned events for rules dropped before scoring."""
    sanitized = _make_sanitized(chemical_state="STOICHIOMETRIC_BURN")
    router.execute_triage_loop(sanitized)

    by_name = _spans_by_name(in_memory_exporter)
    prune_spans = by_name.get("phase.prune", [])
    assert len(prune_spans) == 1, (
        f"Expected 1 prune span, got {len(prune_spans)}"
    )
    prune_span = prune_spans[0]

    events = prune_span.events or []
    pruned_events = [event for event in events if event.name == "rule_pruned"]
    assert pruned_events, "Expected at least one rule_pruned event"

    reasons = set()
    gating_keys = set()
    for event in pruned_events:
        attrs = event.attributes or {}
        assert "rule_id" in attrs, f"rule_pruned event missing rule_id: {attrs}"
        assert str(attrs["rule_id"]).startswith("ERR-")
        assert "prune_reason" in attrs
        assert "failed_gating_key" in attrs
        reasons.add(attrs["prune_reason"])
        gating_keys.add(attrs["failed_gating_key"])

    assert reasons <= {"horizon", "chemistry", "missing_evidence"}
    assert "chemistry" in reasons
    assert "gas_lab_state" in gating_keys


def test_threshold_miss_tag(
    in_memory_exporter: Any,
    router: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When winner score < MIN_CONFIDENCE_THRESHOLD, rank span tags threshold_miss."""
    # Force threshold high so all rules are suppressed
    import comlab.core.fault_atlas_router as router_mod
    monkeypatch.setattr(router_mod, "MIN_CONFIDENCE_THRESHOLD", 0.99)

    sanitized = _make_sanitized()
    verdict = router.execute_triage_loop(sanitized)

    # Verdict should have no winner (suppressed by threshold)
    assert verdict["winner"] is None, (
        f"Expected no winner with threshold=0.99, got {verdict['winner']}"
    )

    by_name = _spans_by_name(in_memory_exporter)
    rank_spans = by_name.get("phase.rank", [])
    assert len(rank_spans) == 1
    rank_span = rank_spans[0]

    attrs = rank_span.attributes or {}
    assert attrs.get("router.threshold_miss") is True, (
        f"Expected router.threshold_miss=True, got {attrs.get('router.threshold_miss')}"
    )
    # winner_id should be the suppressed rule's fault_id, not __NONE__
    winner_id = attrs.get("router.winner_id")
    assert winner_id is not None, "router.winner_id missing"
    assert winner_id != "__NONE__", (
        f"router.winner_id should be the suppressed rule, got {winner_id!r}"
    )
    assert winner_id.startswith("ERR-"), (
        f"router.winner_id should be a fault_id: {winner_id!r}"
    )
    # router.winner_score should be present and positive
    winner_score = attrs.get("router.winner_score")
    assert winner_score is not None
    assert winner_score > 0.0, (
        f"router.winner_score should be positive, got {winner_score}"
    )
    assert winner_score < 0.99, (
        f"router.winner_score should be below threshold, got {winner_score}"
    )


def test_v2_route_emits_rank_span_with_expected_rule_tags(
    in_memory_exporter: Any,
    registry_path: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The REG-V2 route mirrors scored rules into phase.rank diagnostics."""
    pytest.importorskip("opentelemetry")
    from opentelemetry import baggage, context

    from comlab.analytics.power_loss_analytics import PowerLossAnalytics
    from comlab.core.fault_atlas_kg import FaultAtlasKG
    from comlab.core.fault_atlas_router import FaultAtlasRouter

    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=True,
    )
    payload = {
        "gas_lab_output": {
            "chemical_state": "RICH_MIXTURE",
            "sample_validity": "VALID",
            "gas_co": 1.5,
            "gas_hc": 250,
            "gas_co2": 12.0,
            "gas_o2": 0.3,
            "gas_nox": 50,
        },
        "obd_live_data": {
            "normalized_obd_lambda": 0.94,
        },
        "dtc_lab_output": {
            "confirmed_dtcs": ["P0172"],
            "freeze_frame": {
                "short_term_ft1": -8.0,
                "long_term_ft1": -15.0,
                "manifold_pressure_kpa": 45.0,
                "engine_rpm": 800.0,
                "coolant_temp_c": 90.0,
                "maf_gps": 4.0,
                "o2_voltage_b1s1": 0.8,
                "fuel_pressure_kpa": 2500.0,
            },
        },
    }

    token = context.attach(
        baggage.set_baggage("harness.expected_family", "rich_mixture")
    )
    try:
        router.route(payload)
    finally:
        context.detach(token)

    by_name = _spans_by_name(in_memory_exporter)
    rank_spans = by_name.get("phase.rank", [])
    assert len(rank_spans) == 1
    rank_span = rank_spans[0]
    attrs = rank_span.attributes or {}
    assert attrs["router.expected_rule_present"] is True
    assert attrs["router.expected_rule_rank"] == 1
    assert attrs["router.winner_id"] != "__NONE__"

    scored_events = [
        event for event in (rank_span.events or []) if event.name == "rule_scored"
    ]
    assert scored_events
    first_attrs = scored_events[0].attributes or {}
    assert first_attrs["rule_id"]
    assert isinstance(first_attrs["score"], float)


def test_v2_route_emits_prune_span_with_rule_pruned_events(
    in_memory_exporter: Any,
    registry_path: Any,
) -> None:
    """FT-3. The REG-V2 route emits a phase.prune span replaying the shim's
    pre-scoring prune attributions as rule_pruned events, with the same keys the
    Jaeger analyser consumes (rule_id, prune_reason, failed_gating_key).
    """
    pytest.importorskip("opentelemetry")

    from comlab.analytics.power_loss_analytics import PowerLossAnalytics
    from comlab.core.fault_atlas_kg import FaultAtlasKG
    from comlab.core.fault_atlas_router import FaultAtlasRouter

    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=True,
    )
    # RICH_MIXTURE chemistry: rich rules fire; lean/misfire/etc. GATING rules
    # are pruned. Guarantees a non-empty prune bucket alongside a non-empty
    # scored set.
    payload = {
        "gas_lab_output": {
            "chemical_state": "RICH_MIXTURE",
            "sample_validity": "VALID",
            "gas_co": 1.5,
            "gas_hc": 250,
            "gas_co2": 12.0,
            "gas_o2": 0.3,
            "gas_nox": 50,
        },
        "obd_live_data": {"normalized_obd_lambda": 0.94},
        "dtc_lab_output": {
            "confirmed_dtcs": ["P0172"],
            "freeze_frame": {
                "short_term_ft1": -8.0,
                "long_term_ft1": -15.0,
                "manifold_pressure_kpa": 45.0,
                "engine_rpm": 800.0,
                "coolant_temp_c": 90.0,
                "maf_gps": 4.0,
                "o2_voltage_b1s1": 0.8,
                "fuel_pressure_kpa": 2500.0,
            },
        },
    }
    router.route(payload)

    by_name = _spans_by_name(in_memory_exporter)
    prune_spans = by_name.get("phase.prune", [])
    assert len(prune_spans) == 1, f"Expected 1 prune span, got {len(prune_spans)}"
    prune_span = prune_spans[0]

    # Prune is a sibling of rank under the v2 route (both present, prune first).
    attrs = prune_span.attributes or {}
    assert isinstance(attrs.get("router.candidates_in"), int)
    assert isinstance(attrs.get("router.candidates_out"), int)
    # candidates_in == total rules; out == scored survivors; in > out (some pruned).
    assert attrs["router.candidates_in"] > attrs["router.candidates_out"]

    pruned_events = [
        event for event in (prune_span.events or []) if event.name == "rule_pruned"
    ]
    assert pruned_events, "Expected at least one rule_pruned event on the v2 path"

    reasons = set()
    for event in pruned_events:
        ev_attrs = event.attributes or {}
        assert ev_attrs["rule_id"]
        assert "prune_reason" in ev_attrs
        assert "failed_gating_key" in ev_attrs
        reasons.add(ev_attrs["prune_reason"])
    # REG-V2 has no horizon gate — only the chemistry / missing_evidence vocab.
    assert reasons <= {"chemistry", "missing_evidence"}
