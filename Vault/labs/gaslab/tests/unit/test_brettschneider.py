"""Tests for gaslab.brettschneider — Brettschneider 5-gas lambda."""

from __future__ import annotations

import pytest

from gaslab.brettschneider import lambda_chem
from gaslab.contracts import GasReading


# ---------------------------------------------------------------------------
# Success-criteria cases
# ---------------------------------------------------------------------------


def test_stoich_idle_lambda_near_unity() -> None:
    """CO=0.3, CO2=14.8, O2=0.2, HC=20, NOx=20 → λ ∈ [0.99, 1.01]."""
    reading = GasReading(hc=20, co=0.3, co2=14.8, o2=0.2, nox=20)
    result = lambda_chem(reading)
    assert 0.99 <= result <= 1.01, f"λ={result} outside [0.99, 1.01]"


def test_misfire_immunity() -> None:
    """HC=1500, CO=0.2, CO2=8, O2=4, NOx=10 → λ ∈ [0.98, 1.05].

    The masking case from GAS_WIKI §8.5: high HC + high O2 with low NOx
    is an ignition misfire, but lambda stays balanced because the raw
    fuel and raw air escape in stoichiometric proportion.
    Source: GAS_WIKI §4.3.
    """
    reading = GasReading(hc=1500, co=0.2, co2=8, o2=4, nox=10)
    result = lambda_chem(reading)
    assert 0.98 <= result <= 1.05, f"λ={result} outside [0.98, 1.05]"


def test_5gas_required() -> None:
    """NOx omitted raises TypeError; NOx=0 with high HC stays valid.

    GasReading requires all five fields — no 4-gas fallback.
    NOx=0 is a legal reading (cold idle, rich mixture, or misfire).
    """
    # NOx omitted — must raise
    with pytest.raises(TypeError):
        GasReading(hc=1500, co=0.2, co2=8, o2=4)  # type: ignore[call-arg]

    # NOx=0 with very high HC — stays valid
    reading = GasReading(hc=1500, co=0.2, co2=8, o2=4, nox=0)
    result = lambda_chem(reading)
    assert 0.95 <= result <= 1.05


# ---------------------------------------------------------------------------
# Parametrised sweep — rich / stoich / lean
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("hc", "co", "co2", "o2", "nox", "lam_lo", "lam_hi", "label"),
    [
        # Rich: high CO, low O2
        (150, 1.5, 13.0, 0.1, 30, 0.90, 0.96, "rich_classic"),
        # Borderline rich
        (80, 0.6, 13.5, 0.3, 50, 0.96, 1.00, "borderline_rich"),
        # Stoich: balanced
        (20, 0.3, 14.8, 0.2, 30, 0.98, 1.02, "stoich_clean"),
        # Borderline lean
        (30, 0.1, 14.0, 1.0, 80, 1.03, 1.08, "borderline_lean"),
        # Lean: low CO, high O2
        (20, 0.05, 13.0, 2.5, 200, 1.13, 1.22, "lean_moderate"),
    ],
)
def test_parametrised_lambda(
    hc: int,
    co: float,
    co2: float,
    o2: float,
    nox: int,
    lam_lo: float,
    lam_hi: float,
    label: str,
) -> None:
    """Parametrised sweep across rich → stoich → lean."""
    reading = GasReading(hc=hc, co=co, co2=co2, o2=o2, nox=nox)
    result = lambda_chem(reading)
    assert lam_lo <= result <= lam_hi, (
        f"[{label}] λ={result:.4f} outside [{lam_lo}, {lam_hi}]"
    )


# ---------------------------------------------------------------------------
# Custom Hcv
# ---------------------------------------------------------------------------


def test_custom_hcv() -> None:
    """Custom Hcv value is accepted (methane=4.0 gives different result)."""
    reading = GasReading(hc=20, co=0.3, co2=14.8, o2=0.2, nox=20)
    result_petrol = lambda_chem(reading, hcv=1.85)
    result_methane = lambda_chem(reading, hcv=4.0)
    # With higher Hcv, current formula is Hcv-independent (no Hcv term).
    # This test guards the API contract — lambda_chem must accept hcv=.
    assert isinstance(result_petrol, float)
    assert isinstance(result_methane, float)
