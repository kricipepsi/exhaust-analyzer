"""T-COMA-18 (F-C1-6): RM-004 (precondition "gdi_equipped: true") applies only on a GDI decode or the MODERN era."""
from __future__ import annotations

import copy
import logging
from typing import Any

import pytest
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from registry import integration_shim as shim

logging.disable(logging.CRITICAL)


def _request(chem: str, horizon: str, fuel: str | None = None) -> OrchestratorInboundRequest:
    meta: dict[str, Any] = {
        "session_id": "6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60", "vin_dna_string": "WVWZZZ1JZ3W000001",
        "resolved_horizon": horizon, "cylinder_count": 4, "vin_confidence": "HIGH",
    }
    if fuel is not None:
        meta["fuel_delivery_type"] = fuel
    ff = {
        "calculated_load_pct": 25.0, "engine_rpm": 800, "coolant_temp_c": 90.0,
        "short_term_ft1": 0.0, "long_term_ft1": 0.0, "manifold_pressure_kpa": 35.0,
        "vehicle_speed_kmh": 0, "ignition_advance_deg": 10.0,
        "intake_air_temp_c": 30.0, "maf_gps": 3.0, "throttle_pos_pct": 12.0, "fuel_system_status": "CL",
    }
    raw = {
        "metadata": meta,
        "gas_lab_output": {
            "chemical_state": chem, "gas_co": 0.3, "gas_hc": 80, "gas_co2": 14.8, "gas_o2": 0.4,
            "gas_nox": 50, "lambda_chem": 1.0, "sample_validity": "VALID",
        },
        "obd_live_data": None,
        "dtc_lab_output": {
            "active_mil": False, "mil_flashing": False, "confirmed_dtcs": [], "routing_tags": [],
            "historical_fault_context": "UNKNOWN", "freeze_frame": ff,
        },
        "symptom_dna": {"environmental_conditions": {"engine_state": "running", "occurs_during": "always"}},
    }
    return OrchestratorInboundRequest.model_validate(copy.deepcopy(raw))


def _ids(chem: str, horizon: str, fuel: str | None = None) -> list[str]:
    v = LabPipelineAggregator().process(_request(chem, horizon, fuel)).diagnostic_verdict
    return [v.fault_code] + [s.fault_id for s in v.differential_siblings]


@pytest.mark.parametrize("horizon, fuel, offered", [
    ("HORIZON_LEGACY", None, False),
    ("HORIZON_ADAPTIVE", None, False),
    ("HORIZON_LEGACY", "PORT_INJECTION", False),
    ("HORIZON_MODERN", None, True),
    ("HORIZON_MODERN", "PORT_INJECTION", True),
    ("HORIZON_LEGACY", "GDI", True),
])
def test_rm004_offered_only_on_gdi_or_modern(horizon: str, fuel: str | None, offered: bool) -> None:
    assert ("RM-004" in _ids("RICH_MIXTURE", horizon, fuel)) is offered


def test_gdi_chemistry_on_legacy_car_is_not_rm004() -> None:
    assert "RM-004" not in _ids("GDI_HPFP_INTERNAL_SEAL_LEAK", "HORIZON_LEGACY")


def test_pruned_rule_is_reported_as_hardware_gate() -> None:
    rule = next(r for r in shim.RegistryV2Router().rules if r.rule_id == "RM-004")
    payload = {"horizon_ctx": "HORIZON_LEGACY", "metadata": {"fuel_delivery_type": None}}
    assert shim._hardware_gate(rule, payload) is True
    other = next(r for r in shim.RegistryV2Router().rules if r.rule_id == "RM-001")
    assert shim._hardware_gate(other, payload) is False
    assert shim._hardware_gate(rule, {"metadata": {}}) is False  # no era sent: unknown, not pruned


def test_router_records_the_hardware_gate_prune() -> None:
    payload = {"horizon_ctx": "HORIZON_LEGACY", "metadata": {"fuel_delivery_type": None}}
    _out, diagnostics = shim.RegistryV2Router().route_case_with_diagnostics(payload)
    gated = [p for p in diagnostics["pruned_rules"] if p["rule_id"] == "RM-004"]
    assert gated == [{"rule_id": "RM-004", "prune_reason": "hardware_gate",
                      "failed_gating_key": "precondition:gdi_equipped"}]
    assert "RM-004" not in [r["rule_id"] for r in diagnostics["scored_rules"]]


def test_wired_metadata_carries_fuel_delivery_type() -> None:
    from wired.composition import _build_metadata

    meta = _build_metadata({"vin": "WVWZZZ1JZ3W000001", "resolved_horizon": "HORIZON_LEGACY",
                            "fuel_delivery_type": "GDI", "confidence": "HIGH"})
    assert str(meta.fuel_delivery_type) == "GDI"
