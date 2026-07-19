"""T-P8-7: Verify EXHAUST_AIR_LEAK collision-rule HC discriminator.

wiki: GAS_WIKI §7.7 — EXHAUST_AIR_LEAK requires HC Normal.
vocab: GAS_VOCABULARY §10.1 — normal_borderline.max = 100.
"""

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.rule_engine import classify


@pytest.fixture(scope="module")
def ontology() -> dict:
    return load_ontology()


def _dna(**overrides: object) -> GasLabDnaView:
    defaults: dict[str, object] = dict(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="PORT",
        induction_type="NA",
        upstream_o2_type="WIDEBAND",
        has_catalyst=True,
        egr_equipped=False,
        confidence="HIGH",
    )
    defaults.update(overrides)
    return GasLabDnaView(**defaults)  # type: ignore[arg-type]


def _reading(**overrides: object) -> GasReading:
    defaults: dict[str, object] = dict(
        hc=15, co=0.2, co2=15.0, o2=0.2, nox=50,
    )
    defaults.update(overrides)
    return GasReading(**defaults)  # type: ignore[arg-type]


def _classify(reading, dna=None, ontology_=None):
    if dna is None:
        dna = _dna()
    if ontology_ is None:
        ontology_ = load_ontology()
    return classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology_)


def test_exhaust_leak_normal_hc_routes_to_exhaust_air_leak(ontology):
    """HC Normal (<=100) + collision pattern + triangle > 16 -> EXHAUST_AIR_LEAK."""
    reading = _reading(co=2.0, hc=50, co2=9.0, o2=6.0, nox=30)
    result, validity = _classify(reading, ontology_=ontology)
    assert result == ChemicalSignature.EXHAUST_AIR_LEAK
    assert validity == SampleValidity.EXTERNAL_O2_SUSPECT


def test_high_hc_collision_routes_to_rich_misfire_not_exhaust_leak(ontology):
    """HC > 100 + collision pattern + triangle > 16 -> RICH_MISFIRE, not EXHAUST_AIR_LEAK."""
    reading = _reading(co=2.0, hc=650, co2=8.0, o2=7.0, nox=80)
    result, validity = _classify(reading, ontology_=ontology)
    assert result == ChemicalSignature.RICH_MISFIRE
    assert validity == SampleValidity.EXTERNAL_O2_SUSPECT


def test_high_hc_collision_triangle_normal_routes_to_rich_misfire(ontology):
    """HC > 100 + collision + triangle <= 16 -> RICH_MISFIRE (unchanged path)."""
    reading = _reading(co=1.0, hc=650, co2=12.0, o2=3.0, nox=80)
    result, validity = _classify(reading, ontology_=ontology)
    # triangle = 1.0 + 12.0 + 3.0 = 16.0 -> <= 16 -> RICH_MISFIRE
    assert result == ChemicalSignature.RICH_MISFIRE
    assert validity == SampleValidity.EXTERNAL_O2_SUSPECT


def test_hc_at_boundary_100_routes_to_exhaust_air_leak(ontology):
    """HC exactly at Normal ceiling (100) -> still EXHAUST_AIR_LEAK."""
    reading = _reading(co=2.0, hc=100, co2=8.0, o2=7.0, nox=30)
    result, validity = _classify(reading, ontology_=ontology)
    assert result == ChemicalSignature.EXHAUST_AIR_LEAK


def test_hc_101_routes_to_rich_misfire(ontology):
    """HC just above Normal ceiling (101) -> RICH_MISFIRE."""
    reading = _reading(co=2.0, hc=101, co2=8.0, o2=7.0, nox=30)
    result, validity = _classify(reading, ontology_=ontology)
    assert result == ChemicalSignature.RICH_MISFIRE
