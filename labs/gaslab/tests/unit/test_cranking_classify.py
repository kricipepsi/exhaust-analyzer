"""T-COMA-3b: GASLab classifies a CRANKING sample without the running-engine validity gates.

Tags: NEW fails on the base (no CRANKING bucket); PIN passes there and after.  Source: GAS_WIKI §4.14.
"""

from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.ontology_loader import load_ontology
from gaslab.dna_view import GasLabDnaView
from gaslab.rule_engine import classify

AIR = GasReading(hc=0, co=0.0, co2=0.04, o2=20.9, nox=0)
DNA = GasLabDnaView(
    engine_displacement_liters=2.0, cylinder_count=4, number_of_banks=1, euro_emission_category="Euro 4",
    fuel_delivery_type="PORT", induction_type="NA", upstream_o2_type="WIDEBAND", has_catalyst=True,
    egr_equipped=False, confidence="HIGH",
)


def _crank(**gas: float) -> tuple[ChemicalSignature, SampleValidity]:
    reading = GasReading(**{"hc": 2000, "co": 0.2, "co2": 2.0, "o2": 18.0, "nox": 0, **gas})
    return classify(reading, DNA, EngineStateBucket.CRANKING, load_ontology())


@pytest.mark.parametrize(("gas", "expected"), [
    ({"co": 1.5, "co2": 1.0}, (ChemicalSignature.RICH_MISFIRE, SampleValidity.VALID)),
    ({"co": 1.49, "co2": 4.99}, (ChemicalSignature.LEAN_MISFIRE, SampleValidity.VALID)),
    ({"co": 0.0, "co2": 0.04, "hc": 0, "o2": 20.9}, (ChemicalSignature.LEAN_MISFIRE, SampleValidity.VALID)),
    ({"co": 0.5, "co2": 5.0}, (ChemicalSignature.INCOMPLETE_COMBUSTION, SampleValidity.VALID)),
    ({"co": 0.5, "co2": 7.99}, (ChemicalSignature.INCOMPLETE_COMBUSTION, SampleValidity.VALID)),
    ({"co": 4.0, "co2": 8.0, "o2": 2.0}, (ChemicalSignature.SAMPLE_INVALID, SampleValidity.INVALID)),
])
def test_cranking_branches(gas: dict, expected: tuple) -> None:
    """NEW: the four cranking branches and their boundaries (CO 1.5 %, CO2 5.0 % and 8.0 %)."""
    assert _crank(**gas) == expected


def test_air_at_idle_is_still_invalid() -> None:
    """PIN: the running-engine buckets keep the triangle gate; near-air at idle is SAMPLE_INVALID."""
    result = classify(AIR, DNA, EngineStateBucket.STABILIZED_IDLE, load_ontology())
    assert result == (ChemicalSignature.SAMPLE_INVALID, SampleValidity.INVALID)
