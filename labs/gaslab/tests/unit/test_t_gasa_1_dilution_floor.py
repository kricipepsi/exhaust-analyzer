"""T-GASA-1 (F-C2-1, HIGH): the low-triangle exhaust-leak route honours the GASWIKI-04 §4.2 dilution screen.

A sample with no combustion products (CO + CO2 <= 6 %) is diluted, not leak chemistry: it falls through to the
below-14 % triangle halt and is SAMPLE_INVALID / INVALID. Leak chemistry with real combustion stays EXHAUST_AIR_LEAK.
"""

from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.process import GasLabContext, process

DNA = GasLabDnaView(
    engine_displacement_liters=1.6, cylinder_count=4, number_of_banks=1, euro_emission_category="EURO_4",
    fuel_delivery_type="PORT_INJECTION", induction_type="NATURALLY_ASPIRATED", upstream_o2_type="NARROWBAND",
    has_catalyst=True, egr_equipped=False,
)


def _run(hc: float, co: float, co2: float, o2: float, nox: float):
    out = process(GasReading(hc=hc, co=co, co2=co2, o2=o2, nox=nox),
                  GasLabContext(DNA, EngineStateBucket.STABILIZED_IDLE))
    return out.chemical_state, out.sample_validity


@pytest.mark.parametrize(("reading", "label"), [
    ((0, 0.1, 0.0, 2.1, 0), "F-C2-1 probe: CO2 0 %, sum 2.2 %"),
    ((50, 0.3, 3.0, 10.5, 20), "sum 13.8 %, CO + CO2 3.3 %"),
    ((50, 0.3, 5.7, 7.0, 20), "CO + CO2 exactly 6.0 %: the screen is strict"),
])
def test_diluted_sample_is_invalid_not_a_leak(reading, label) -> None:
    assert _run(*reading) == (ChemicalSignature.SAMPLE_INVALID, SampleValidity.INVALID), label


def test_leak_chemistry_with_real_combustion_is_still_a_leak() -> None:
    """Sum 13.3 %, CO + CO2 10.3 %: the leak route still fires."""
    assert _run(50, 0.3, 10.0, 3.0, 20) == (ChemicalSignature.EXHAUST_AIR_LEAK, SampleValidity.EXTERNAL_O2_SUSPECT)
