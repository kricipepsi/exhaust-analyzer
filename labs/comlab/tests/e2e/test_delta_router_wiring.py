"""End-to-end locks for the default-off delta router consumer."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest

import comlab.core.fault_atlas_router as router_module
import registry.integration_shim as registry_shim
from comlab.core.fault_atlas_router import RegistryRow
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import (
    OrchestratorInboundRequest,
    SecondOperatingPointFrame,
)
from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    EngineStateBucket,
    InductionType,
    SampleValidity,
)
from tests.fixtures import mock_dtc_lab, mock_obd_lab


def _request(*, with_second_point: bool) -> OrchestratorInboundRequest:
    payload = {
        "metadata": {
            "session_id": str(uuid4()),
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": "HORIZON_MODERN",
            "cylinder_count": 4,
        },
        "gas_lab_output": {
            "chemical_state": "NORMAL_OPERATION",
            "gas_co": 0.1,
            "gas_hc": 15,  # wiki: delta-relations/07 — worn-rings low point
            "gas_co2": 14.5,
            "gas_o2": 0.3,
            "gas_nox": 10,
            "lambda_chem": 1.0,
            "sample_validity": "VALID",
        },
        "obd_live_data": mock_obd_lab.warm_idle_baseline(),
        "dtc_lab_output": mock_dtc_lab.no_codes(),
        "symptom_dna": {},
        "user_input_echo_audit": {
            "submitted_at": datetime(2026, 6, 20, tzinfo=timezone.utc),
            "groups": [],
        },
    }
    if with_second_point:
        payload["second_operating_point"] = {
            "rpm_state_bucket": "REGULATORY_HIGH_IDLE",
            "engine_rpm": 2500,  # wiki: delta-relations/07 — Δgas high-idle band
            "gas_hc": 180,  # wiki: delta-relations/07 — worn-rings elevated point
            "gas_co": 0.1,
            "gas_co2": 14.0,
            "gas_o2": 0.3,
            "gas_nox": 10,
            "lambda_chem": 1.0,
            "sample_validity": "VALID",
            "rpm_stable": True,
            "air_metering_strategy": "MAF_ONLY",
            "induction_type": "NATURALLY_ASPIRATED",
        }
    return OrchestratorInboundRequest.model_validate(payload)


def _controlled_registry() -> list[RegistryRow]:
    """Static winner first; delta-target mechanical-wear rule second."""
    common = {
        "target_horizons": ["HORIZON_MODERN"],
        "preconditions": {},
        "cross_domain_matrix": {
            "gas_lab_state": "NORMAL_OPERATION",
            "obd_live_pids": {},
            "dtc_lab_status": {
                "active_mil": False,
                "p_code_match": [],
                "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY",
            },
        },
    }
    return [
        RegistryRow.model_validate({
            **common,
            "fault_id": "ERR-CF-001",
            "fault_name": "catalyst_efficiency_below_threshold",
            "confidence_scoring": {
                "base_weight": 0.85,
                "bonus_on_dtc_match": 0.0,
            },
        }),
        RegistryRow.model_validate({
            **common,
            "fault_id": "ERR-MW-001",
            "fault_name": "head_gasket_fire_ring_failure",
            "confidence_scoring": {
                "base_weight": 0.75,
                "bonus_on_dtc_match": 0.0,
            },
        }),
    ]


def _aggregator(*, enable_delta: bool) -> LabPipelineAggregator:
    agg = LabPipelineAggregator(
        use_v2_registry=False,
        enable_delta=enable_delta,
    )
    agg._router.registry = _controlled_registry()
    return agg


def _v2_aggregator(*, enable_delta_v2: bool) -> LabPipelineAggregator:
    return LabPipelineAggregator(
        use_v2_registry=True,
        enable_delta_v2=enable_delta_v2,
    )


def _v2_stub_output(*, rule_id: str, family: str, score: float) -> dict:
    return {
        "session_id": "00000000-0000-4000-8000-000000000002",
        "execution_meta": {
            "resolved_horizon": "HORIZON_MODERN",
            "degradation_mode": "FULL_FUSION",
            "processing_confidence_rating": "HIGH_ASSURANCE",
            "vin_confidence": "HIGH",
            "lab_routing_directive": {
                "suppress_gaslab": False,
                "suppress_obd_live_pids": False,
                "suppress_mode06_ui": False,
                "cold_start_mode": False,
                "reasons": [],
            },
        },
        "diagnostic_verdict": {
            "is_fault_detected": True,
            "fault_code": rule_id,
            "fault_name": rule_id,
            "fault_family": family,
            "display_headline": rule_id,
            "confidence_score": score,
            "actionable_remediation": "test",
            "differential_siblings": [],
        },
        "performance_analytics": {
            "kinetic_power_loss_pct": 0.0,
            "catalyst_efficiency_index_pct": None,
            "lambda_perception_delta": 0.0,
            "o2_sensor_bias_verdict": None,
            "severity_level": "WARNING_DEGRADED_PERFORMANCE",
        },
        "fault_enrichment": {
            "component_group": "engine",
            "impacted_subsystems": [],
            "mechanical_failure_mode": rule_id,
            "ui_remediation_steps": ["test"],
            "editor_severity_hint": None,
        },
        "user_input_echo_audit": {
            "submitted_at": "2026-06-20T00:00:00Z",
            "groups": [],
        },
    }


def _patch_v2_registry(
    monkeypatch: pytest.MonkeyPatch,
    scored_rules: list[dict] | None = None,
) -> list[str]:
    rendered: list[str] = []
    rules = scored_rules or [
        {
            "rule_id": "CF-001",
            "fault_family": "catalyst_failure",
            "score": 0.85,
        },
        {
            "rule_id": "MW-001",
            "fault_family": "mechanical_wear",
            "score": 0.75,
        },
    ]
    top = rules[0]

    def route_stub(_payload: dict) -> tuple[dict, dict]:
        return (
            _v2_stub_output(
                rule_id=str(top["rule_id"]),
                family=str(top["fault_family"]),
                score=float(top["score"]),
            ),
            {
                "scored_rules": [dict(rule) for rule in rules],
                "pruned_rules": [],
                "winner_rule_id": str(top["rule_id"]),
            },
        )

    def render_stub(
        _payload: dict,
        rule_id: str,
        score: float,
    ) -> dict:
        rendered.append(rule_id)
        family = next(
            str(rule["fault_family"])
            for rule in rules
            if rule["rule_id"] == rule_id
        )
        return _v2_stub_output(rule_id=rule_id, family=family, score=score)

    monkeypatch.setattr(registry_shim, "route_case_with_diagnostics", route_stub)
    monkeypatch.setattr(registry_shim, "render_ranked_rule", render_stub)
    return rendered


class _RecordingSpan:
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def __enter__(self) -> _RecordingSpan:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def is_recording(self) -> bool:
        return True

    def set_attribute(self, _name: str, _value: object) -> None:
        return None

    def add_event(
        self,
        name: str,
        _attributes: dict[str, object] | None = None,
    ) -> None:
        self._events.append(name)


class _RecordingTracer:
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def start_as_current_span(self, _name: str) -> _RecordingSpan:
        return _RecordingSpan(self._events)


@pytest.mark.e2e
def test_delta_single_point_regression() -> None:
    """Flag-on remains byte-identical when no second frame exists."""
    request = _request(with_second_point=False)

    disabled = _aggregator(enable_delta=False).process(request)
    enabled = _aggregator(enable_delta=True).process(request)

    assert enabled.model_dump(mode="json") == disabled.model_dump(mode="json")


@pytest.mark.e2e
def test_delta_two_point_activation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Trusted two-point evidence promotes the matching runner-up family."""
    events: list[str] = []
    monkeypatch.setattr(
        router_module,
        "get_tracer",
        lambda _name: _RecordingTracer(events),
    )
    request = _request(with_second_point=True)

    disabled = _aggregator(enable_delta=False).process(request)
    enabled = _aggregator(enable_delta=True).process(request)

    assert disabled.diagnostic_verdict.fault_code == "ERR-CF-001"
    assert enabled.diagnostic_verdict.fault_code == "ERR-MW-001"
    assert enabled.diagnostic_verdict.fault_family == "mechanical_wear"
    assert enabled.diagnostic_verdict.confidence_score == pytest.approx(0.92)
    assert "delta_signature_applied" in events


@pytest.mark.e2e
def test_delta_v2_flag_off_regression(monkeypatch: pytest.MonkeyPatch) -> None:
    """The v2 production-default path is unchanged while its own flag is off."""
    rendered = _patch_v2_registry(monkeypatch)
    request = _request(with_second_point=True)

    output = _v2_aggregator(enable_delta_v2=False).process(request)

    assert output.diagnostic_verdict.fault_code == "CF-001"
    assert output.diagnostic_verdict.confidence_score == pytest.approx(0.85)
    assert rendered == []


@pytest.mark.e2e
def test_delta_parity_v1_and_v2(monkeypatch: pytest.MonkeyPatch) -> None:
    """Both rank paths apply the same trusted two-point family promotion."""
    rendered = _patch_v2_registry(monkeypatch)
    request = _request(with_second_point=True)

    v1 = _aggregator(enable_delta=True).process(request)
    v2 = _v2_aggregator(enable_delta_v2=True).process(request)

    assert v1.diagnostic_verdict.fault_family == "mechanical_wear"
    assert v2.diagnostic_verdict.fault_family == v1.diagnostic_verdict.fault_family
    assert v2.diagnostic_verdict.confidence_score == pytest.approx(
        v1.diagnostic_verdict.confidence_score
    )
    assert rendered == ["MW-001"]


@pytest.mark.e2e
def test_delta_v2_single_point_abstains(monkeypatch: pytest.MonkeyPatch) -> None:
    """No second frame leaves the v2 scored_rules order untouched."""
    rendered = _patch_v2_registry(monkeypatch)
    request = _request(with_second_point=False)

    output = _v2_aggregator(enable_delta_v2=True).process(request)

    assert output.diagnostic_verdict.fault_code == "CF-001"
    assert output.diagnostic_verdict.confidence_score == pytest.approx(0.85)
    assert rendered == []


@pytest.mark.e2e
def test_delta_v2_band_mismatch_abstains(monkeypatch: pytest.MonkeyPatch) -> None:
    """A second frame in neither allowed band cannot move v2 scored_rules."""
    rendered = _patch_v2_registry(monkeypatch)
    request = _request(with_second_point=False).model_copy(update={
        "second_operating_point": SecondOperatingPointFrame(
            rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
            engine_rpm=750,
            gas_hc=180,
            gas_co=0.1,
            gas_co2=14.0,
            gas_o2=0.3,
            gas_nox=10,
            lambda_chem=1.0,
            sample_validity=SampleValidity.VALID,
            rpm_stable=True,
            air_metering_strategy=AirMeteringStrategy.MAF_ONLY,
            induction_type=InductionType.NATURALLY_ASPIRATED,
        )
    })

    output = _v2_aggregator(enable_delta_v2=True).process(request)

    assert output.diagnostic_verdict.fault_code == "CF-001"
    assert rendered == []


@pytest.mark.e2e
def test_delta_v2_architecture_null_and_inversion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Speed-density nulls ΔTrim; forced induction promotes the inverted family."""
    rules = [
        {"rule_id": "VL-001", "fault_family": "vacuum_leak", "score": 0.85},
        {"rule_id": "LC-001", "fault_family": "lean_condition", "score": 0.75},
    ]
    rendered = _patch_v2_registry(monkeypatch, rules)
    base = _request(with_second_point=False)
    assert base.obd_live_data is not None
    obd = base.obd_live_data.model_copy(update={
        "total_trim_correction_delta": 20.0,
    })
    speed_density = base.model_copy(update={
        "obd_live_data": obd,
        "second_operating_point": SecondOperatingPointFrame(
            rpm_state_bucket=EngineStateBucket.STRESS_IDLE,
            engine_rpm=4000,
            total_trim_correction_delta=2.0,
            sample_validity=SampleValidity.VALID,
            rpm_stable=True,
            air_metering_strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY,
            induction_type=InductionType.NATURALLY_ASPIRATED,
        ),
    })

    nulled = _v2_aggregator(enable_delta_v2=True).process(speed_density)

    assert nulled.diagnostic_verdict.fault_code == "VL-001"
    assert rendered == []

    forced = base.model_copy(update={
        "second_operating_point": SecondOperatingPointFrame(
            rpm_state_bucket=EngineStateBucket.STRESS_IDLE,
            engine_rpm=4000,
            total_trim_correction_delta=-20.0,
            sample_validity=SampleValidity.VALID,
            rpm_stable=True,
            air_metering_strategy=AirMeteringStrategy.MAF_ONLY,
            induction_type=InductionType.TURBOCHARGED,
        ),
    })
    inverted = _v2_aggregator(enable_delta_v2=True).process(forced)

    assert inverted.diagnostic_verdict.fault_code == "LC-001"
    assert inverted.diagnostic_verdict.fault_family == "lean_condition"
    assert inverted.diagnostic_verdict.confidence_score == pytest.approx(0.92)
    assert rendered == ["LC-001"]
