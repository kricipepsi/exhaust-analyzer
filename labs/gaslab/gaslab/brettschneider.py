"""Brettschneider 5-gas lambda — chemistry-only, pure function.

Source: ``GAS_VOCABULARY §6`` (Lambda from chemistry — formal definition).
"""

from __future__ import annotations

from gaslab.contracts import HC_FACTOR, GasReading


def lambda_chem(reading: GasReading, hcv: float | None = None) -> float:
    """Brettschneider 5-gas lambda from tailpipe chemistry.

    The carbon-balance denominator weights HC by ``HC_FACTOR`` to convert ppm
    to an effective volume-percent that preserves the misfire-immunity property
    described in ``GAS_WIKI §4.3``: raw fuel and raw air escaping a misfiring
    cylinder remain in stoichiometric proportion, so λ ≈ 1.000 even with high
    HC and high O₂.

    Args:
        reading: Five raw analyser inputs (hc ppm, co/co2/o2 vol%, nox ppm).
        hcv: Hydrogen-to-carbon atomic ratio. Reserved for future use;
            currently unused (HC weighting is captured by HC_FACTOR).

    Returns:
        Dimensionless lambda.  ``λ < 1`` → rich; ``λ > 1`` → lean.

    Source: ``GAS_VOCABULARY §6``.
    """
    co = reading.co
    co2 = reading.co2
    o2 = reading.o2
    hc_ppm = reading.hc
    nox_ppm = reading.nox

    # vocab: GAS_VOCABULARY §6 — carbon-balance λ
    # HC_FACTOR converts ppm HC to effective vol% in the carbon-balance
    # denominator; tuned to satisfy misfire-immunity (§4.3 wiki).
    hc_equiv = hc_ppm * HC_FACTOR  # vocab: GAS_VOCABULARY §6
    carbon_sum = co2 + co + hc_equiv  # vocab: GAS_VOCABULARY §6

    if carbon_sum == 0:
        # Degenerate / all-zero sample (atmospheric air, probe not in tailpipe).
        # Return a safe sentinel; classify() independently flags SAMPLE_INVALID.
        return 1.0

    lambda_4gas = (co2 + co / 2.0 + o2) / carbon_sum  # vocab: GAS_VOCABULARY §6

    # 5-gas NOx correction
    # vocab: GAS_VOCABULARY §6 — λ_5gas = λ_4gas + (NOx_ppm / 1e6) × 0.5 / vol_frac
    volumetric_sum = co + co2 + o2  # vocab: GAS_VOCABULARY §2 — volumetric_sum
    if volumetric_sum > 0:
        vol_frac = volumetric_sum / 100.0  # vocab: GAS_VOCABULARY §6
        nox_correction = (nox_ppm / 1_000_000.0) * 0.5 / vol_frac  # vocab: GAS_VOCABULARY §6
    else:
        nox_correction = 0.0

    return lambda_4gas + nox_correction
