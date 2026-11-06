"""T-AUD-20: a COLD_OPEN_LOOP_INVALID sample is rejected as SAMPLE_INVALID / INVALID (GAS_VOCABULARY §7).

Tags: NEW fails on the base (the cold bucket reaches bound matching); PIN passes there and after.
"""

from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.process import GasLabContext, process
from gaslab.rule_engine import classify

DNA = GasLabDnaView(
    engine_displacement_liters=2.0, cylinder_count=4, number_of_banks=1, euro_emission_category="Euro 4",
    fuel_delivery_type="PORT", induction_type="NA", upstream_o2_type="WIDEBAND", has_catalyst=True,
    egr_equipped=False, confidence="HIGH",
)
NORMAL = GasReading(hc=20, co=0.2, co2=15.0, o2=0.2, nox=50)
RICH = GasReading(hc=300, co=3.0, co2=12.5, o2=0.3, nox=50)
INVALID = (ChemicalSignature.SAMPLE_INVALID, SampleValidity.INVALID)


@pytest.mark.parametrize("reading", [NORMAL, RICH], ids=["normal", "rich"])
def test_new_cold_bucket_is_rejected(reading):
    assert classify(reading, DNA, EngineStateBucket.COLD_OPEN_LOOP_INVALID, load_ontology()) == INVALID


def test_new_cold_payload_is_sample_invalid():
    payload = process(NORMAL, GasLabContext(dna=DNA, engine_state=EngineStateBucket.COLD_OPEN_LOOP_INVALID))
    assert (payload.chemical_state, payload.sample_validity) == INVALID


def test_pin_warm_bucket_unchanged():
    assert classify(NORMAL, DNA, EngineStateBucket.STABILIZED_IDLE, load_ontology()) != INVALID
