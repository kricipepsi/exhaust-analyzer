"""Validity gates — chemistry-level filters that run before fault evaluation.

Pure functions: same inputs → same outputs, no I/O, no globals.

Source: ``GAS_WIKI §6`` (Validity gates).
"""

from __future__ import annotations

from gaslab.contracts import GasReading, SampleValidity


def triangle_gate(reading: GasReading) -> SampleValidity:
    """Exhaust Gas Triangle gate — checks CO+CO₂+O₂ invariant.

    In a clean petrol burn the sum is 14–16 %, regardless of mixture.
    Values outside this band indicate sample dilution or probe failure.

    Source: ``GAS_WIKI §6.1``, ``GAS_VOCABULARY §5``.

    Returns:
        VALID, EXTERNAL_O2_SUSPECT, or INVALID.
        BORDERLINE (per GAS_VOCABULARY §5) is collapsed to VALID in v1.
    """
    volumetric_sum = reading.co + reading.co2 + reading.o2  # wiki: GAS_WIKI §6.1

    if volumetric_sum < 14.0:  # wiki: GAS_WIKI §6.1
        return SampleValidity.INVALID
    if volumetric_sum > 18.0:  # wiki: GAS_WIKI §6.1
        return SampleValidity.INVALID
    if volumetric_sum > 16.0:  # wiki: GAS_WIKI §6.1 — (16, 18]
        return SampleValidity.EXTERNAL_O2_SUSPECT
    return SampleValidity.VALID  # wiki: GAS_WIKI §6.1 — [14, 16]


def dilution_gate(reading: GasReading) -> bool:
    """Dilution screen — checks CO+CO₂ floor.

    An undiluted exhaust sample always satisfies CO+CO₂ > 6 %.
    Values ≤ 6 % indicate heavy dilution or missing combustion.

    Source: ``GAS_WIKI §6.2``.

    Returns:
        True if the sample passes the 6 % floor.
    """
    carbon_sum = reading.co + reading.co2  # wiki: GAS_WIKI §6.2
    return carbon_sum > 6.0  # wiki: GAS_WIKI §6.2


def sample_validity(reading: GasReading) -> SampleValidity:
    """Combined validity check — runs both gates and returns the worst verdict.

    The triangle gate runs first. If it reports INVALID, dilution is not checked
    (the sample is already halted). Otherwise, if dilution fails, the verdict
    is downgraded to INVALID.

    Source: ``GAS_WIKI §6.1``, ``GAS_WIKI §6.2``.
    """
    verdict = triangle_gate(reading)

    if verdict == SampleValidity.INVALID:
        return verdict

    if not dilution_gate(reading):
        return SampleValidity.INVALID

    return verdict
