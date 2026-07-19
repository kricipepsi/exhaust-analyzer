"""Public entry point for GASLab.

The ``process`` function is the single public surface of GASLab. It converts
five technician-entered analyser readings plus a slim DNA view into a canonical
``GasLabPayload`` (chemical state) for COMLab. See ``GAS_WIKI §2.1`` for the
contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from gaslab.brettschneider import lambda_chem
from gaslab.contracts import EngineStateBucket, GasLabPayload, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.rule_engine import classify


@dataclass(frozen=True)
class GasLabContext:
    """Engine-state + DNA-view bundle consumed by ``process()``.

    Source: ``GAS_WIKI §2.1``.
    """

    dna: GasLabDnaView
    engine_state: EngineStateBucket
    lambda_measured: float | None = None  # wiki: GAS_VOCABULARY §2/§6 — optional technician-entered analyser λ;
                                          # consumer: COMLab perception-contradiction detector (T-FX-7 no-OBD path)
    block_test_passed: bool = False  # wiki: GAS_WIKI §8.7 — chemical block test for combustion gases in coolant
    reading_high: GasReading | None = None  # wiki: GAS_WIKI §8.9 — optional high-idle (2500 RPM) reading (T-GV2-4)
    fuel_trim: float | None = None  # vocab: GAS_VOCABULARY §10.8 — short-term fuel trim context input (T-GV2-12)


def process(reading: GasReading, context: GasLabContext) -> GasLabPayload:
    """Run the 5-gas diagnostic pipeline.  Source: ``GAS_WIKI §2.1``."""
    ontology = load_ontology()
    chem_state, validity = classify(
        reading, context.dna, context.engine_state, ontology,
        block_test_passed=context.block_test_passed,
        reading_high=context.reading_high,
        fuel_trim=context.fuel_trim,
    )
    lambda_val = lambda_chem(reading)
    # Clamp to Pydantic bounds; classify() already gates via chemical_state +
    # sample_validity.  Extreme lambda values (non-starters, ambient-air samples)
    # are a chemical reality but must stay within the payload contract.
    # consumer: COMLab perception-contradiction detector (gated by sample_validity)
    lambda_val = min(max(lambda_val, 0.5), 2.5)

    high_idle_hc = None
    high_idle_co = None
    high_idle_co2 = None
    high_idle_o2 = None
    high_idle_nox = None
    high_idle_lambda = None

    if context.reading_high is not None:
        high_idle_hc = context.reading_high.hc
        high_idle_co = context.reading_high.co
        high_idle_co2 = context.reading_high.co2
        high_idle_o2 = context.reading_high.o2
        high_idle_nox = context.reading_high.nox
        high_idle_lambda = lambda_chem(context.reading_high)
        high_idle_lambda = min(max(high_idle_lambda, 0.5), 2.5)

    return GasLabPayload(
        chemical_state=chem_state,
        gas_co=reading.co,
        gas_hc=reading.hc,
        gas_co2=reading.co2,
        gas_o2=reading.o2,
        gas_nox=reading.nox,
        lambda_chem=lambda_val,
        sample_validity=validity,
        lambda_measured=context.lambda_measured,  # T-FX-7: pass-through to COMLab boundary
        high_idle_hc=high_idle_hc,
        high_idle_co=high_idle_co,
        high_idle_co2=high_idle_co2,
        high_idle_o2=high_idle_o2,
        high_idle_nox=high_idle_nox,
        high_idle_lambda=high_idle_lambda,
    )
