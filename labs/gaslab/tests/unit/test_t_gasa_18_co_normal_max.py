"""T-GASA-18 (T-GASA-F45): the CO normal-with-cat maximum is the legal idle limit, 0.3 %.

Source: T-GASA-17 verdicts W0185 and W1303 CONTRADICTED; MOT inspection manual 8.2.1
(labs/gaslab/audit_tasks/wikiaudit/sources/S001.md): "CO up to 0.3% at idle (450rpm to 1,500rpm)".
Live consumers: the collision tier (rule_engine) and the TIMING_OVER_ADVANCED "others near normal" guard (resolution).
"""
from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.resolution import apply_differentiators
from gaslab.rule_engine import classify


@pytest.fixture(scope="module")
def ontology() -> dict:
    return load_ontology()


def _dna() -> GasLabDnaView:
    return GasLabDnaView(
        engine_displacement_liters=2.0, cylinder_count=4, number_of_banks=1, euro_emission_category="Euro 4",
        fuel_delivery_type="PORT", induction_type="NA", upstream_o2_type="WIDEBAND", has_catalyst=True,
        egr_equipped=False, confidence="HIGH",
    )


def test_ontology_values_are_the_legal_idle_limit(ontology: dict) -> None:
    assert ontology["faults"]["NORMAL_OPERATION"]["signature"]["co"]["max"] == 0.3
    assert ontology["reasoning_grammar"]["collision_rule"]["co_tier_max"] == 0.3


def test_collision_fires_above_co_0_3_with_cat(ontology: dict) -> None:
    """CO 0.4 % with O2 > 2 % is the CO/O2 collision for a cat car (0.4 > 0.3; it was below the old 0.45)."""
    reading = GasReading(hc=300, co=0.4, co2=10.0, o2=4.0, nox=80)
    chem, _ = classify(reading, _dna(), EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.RICH_MISFIRE


@pytest.mark.parametrize(("co_high", "toa"), [(0.25, True), (0.40, False)])
def test_timing_over_advanced_needs_co_near_normal_at_2500(ontology: dict, co_high: float, toa: bool) -> None:
    idle = GasReading(hc=180, co=0.2, co2=12.5, o2=1.0, nox=40)
    high = GasReading(hc=60, co=co_high, co2=14.0, o2=0.6, nox=1500)
    out = apply_differentiators([], idle, _dna(), ontology, EngineStateBucket.STABILIZED_IDLE, high)
    assert ("TIMING_OVER_ADVANCED" in out) is toa, out
