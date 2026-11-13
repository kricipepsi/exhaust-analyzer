"""T-GASA-2 (F-C2-2, HIGH): the collision rule keeps the triangle gate's validity.

GASWIKI-04 §4.1: a CO + CO2 + O2 sum in [14, 16] is VALID. The collision rule (GASWIKI §8.5) names the chemistry; it
does not re-label the sample. A sum in (16, 18] stays EXTERNAL_O2_SUSPECT, as the gate already says.
"""

from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.rule_engine import classify

DNA = GasLabDnaView(
    engine_displacement_liters=1.6, cylinder_count=4, number_of_banks=1, euro_emission_category="EURO_4",
    fuel_delivery_type="PORT_INJECTION", induction_type="NATURALLY_ASPIRATED", upstream_o2_type="NARROWBAND",
    has_catalyst=True, egr_equipped=False,
)


@pytest.fixture(scope="module")
def ontology() -> dict:
    return load_ontology()


@pytest.mark.parametrize(("hc", "co", "co2", "o2", "chem", "validity"), [
    (400, 1.0, 11.5, 2.5, ChemicalSignature.RICH_MISFIRE, SampleValidity.VALID),  # the F-C2-2 probe: sum 15.0
    (300, 2.0, 10.0, 4.0, ChemicalSignature.RICH_MISFIRE, SampleValidity.VALID),  # sum 16.0, the band's edge
])
def test_collision_inside_the_valid_band_stays_valid(ontology, hc, co, co2, o2, chem, validity) -> None:
    reading = GasReading(hc=hc, co=co, co2=co2, o2=o2, nox=80)
    assert classify(reading, DNA, EngineStateBucket.STABILIZED_IDLE, ontology) == (chem, validity)


def test_collision_above_the_band_stays_suspect(ontology) -> None:
    """Sum 17.0 %: the gate's EXTERNAL_O2_SUSPECT is kept."""
    reading = GasReading(hc=100, co=2.0, co2=8.0, o2=7.0, nox=30)
    assert classify(reading, DNA, EngineStateBucket.STABILIZED_IDLE, ontology) == (
        ChemicalSignature.EXHAUST_AIR_LEAK, SampleValidity.EXTERNAL_O2_SUSPECT)
