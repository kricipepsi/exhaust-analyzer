from __future__ import annotations

import copy

import pytest
from dtclab.schemas.dna_view import AirMeteringStrategy, ResolvedHorizon, VinConfidence

from wired import composition
from wired.composition import _build_dtc_dna_view, diagnose

_DNA = {
    "make": "PEUGEOT",
    "model_year": 2010,
    "euro_emission_category": "EURO_5",
    "air_metering_strategy": "MAF_ONLY",
    "resolved_horizon": "HORIZON_MODERN",
    "confidence": "HIGH",
    "emissions": {"has_catalyst": True, "egr_equipped": False},
}


def test_view_carries_confidence_and_equipment() -> None:
    view = _build_dtc_dna_view(_DNA)
    assert view is not None
    assert view.confidence == VinConfidence.HIGH
    assert view.emissions.has_catalyst is True
    assert view.emissions.egr_equipped is False
    assert view.model == ""


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("air_metering_strategy", "MAF_ONLY", AirMeteringStrategy.MAF),
        ("air_metering_strategy", "MAP_ONLY_SPEED_DENSITY", AirMeteringStrategy.MAP_SPEED_DENSITY),
        ("air_metering_strategy", "DUAL_MAF_MAP_CROSSCHECK", AirMeteringStrategy.HYBRID),
        ("resolved_horizon", "HORIZON_LEGACY", ResolvedHorizon.HORIZON_LEGACY),
        ("resolved_horizon", "HORIZON_ADAPTIVE", ResolvedHorizon.HORIZON_CLASSIC),
        ("resolved_horizon", "HORIZON_MODERN", ResolvedHorizon.HORIZON_MODERN),
    ],
)
def test_enum_mapping(field: str, value: str, expected: object) -> None:
    view = _build_dtc_dna_view(dict(_DNA, **{field: value}))
    assert view is not None
    assert getattr(view, field) == expected


@pytest.mark.parametrize(
    "change",
    [{"model_year": None}, {"air_metering_strategy": "X"}, {"resolved_horizon": "X"},
     {"emissions": {"has_catalyst": True}}],
)
def test_unknown_required_field_gives_no_view(change: dict) -> None:
    assert _build_dtc_dna_view(dict(_DNA, **change)) is None


_FF = {
    "calculated_load_pct": 30.0, "engine_rpm": 800, "coolant_temp_c": 90.0, "short_term_ft1": 2.0,
    "long_term_ft1": 3.0, "manifold_pressure_kpa": 35.0, "vehicle_speed_kmh": 0, "ignition_advance_deg": 10.0,
    "intake_air_temp_c": 30.0, "maf_gps": 3.0, "throttle_pos_pct": 15.0, "fuel_system_status": "CL",
}
_RAW = {
    "vin": "VF7SA5FR8AW511081",
    "triage": {"tier_1": "rough_idle_shudder", "tier_2": "constant_vibration_shudder",
               "occurs_during": "always", "engine_state": "running", "load_state": "idle"},
    "gas": {"co": 0.1, "co2": 14.5, "o2": 0.3, "hc": 50, "nox": 10, "engine_state": "STABILIZED_IDLE"},
    "dtc": {"raw_dtcs": {"$03": ["P0401"]}, "raw_freeze_frame": _FF},
}


def _spy_views(monkeypatch) -> list:
    seen: list = []
    real = composition._build_dtc_dna_view

    def spy(vin_dna):
        seen.append(real(vin_dna))
        return seen[-1]

    monkeypatch.setattr(composition, "_build_dtc_dna_view", spy)
    return seen


def test_high_egr_less_vehicle_drops_egr_history(monkeypatch) -> None:
    tags: list = []
    real_run = composition._run_dtclab

    def run(dtc_inputs, vin_dna):
        out = real_run(dtc_inputs, vin_dna)
        tags.extend(str(getattr(t, "value", t)) for t in out.routing_tags)
        return out

    monkeypatch.setattr(composition, "_run_dtclab", run)
    seen = _spy_views(monkeypatch)
    diagnose(copy.deepcopy(_RAW))
    assert seen[-1] is not None and seen[-1].confidence == VinConfidence.HIGH
    assert seen[-1].emissions.egr_equipped is False
    assert "EGR_HISTORY" not in tags


def test_de_cat_override_reaches_dtclab(monkeypatch) -> None:
    seen = _spy_views(monkeypatch)
    raw = copy.deepcopy(_RAW)
    raw["overrides"] = {"de_cat": True}
    diagnose(raw)
    assert seen[-1] is not None
    assert seen[-1].emissions.has_catalyst is False
