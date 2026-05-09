"""Standalone Brettschneider lambda pin tests.

source: v2-gas-chemistry §1 — Brettschneider formula with petrol constants.
source: core/bretschneider.py — V1 verified implementation.
"""

from __future__ import annotations

import math

import pytest

from engine.v2.gas_lab import _brettschneider
from engine.v2.input_model import GasRecord

# ── helpers ─────────────────────────────────────────────────────────────────


def _gas(
    co_pct: float = 0.0,
    hc_ppm: float = 0.0,
    co2_pct: float = 0.0,
    o2_pct: float = 0.0,
    nox_ppm: float | None = None,
) -> GasRecord:
    return GasRecord(
        co_pct=co_pct,
        hc_ppm=hc_ppm,
        co2_pct=co2_pct,
        o2_pct=o2_pct,
        nox_ppm=nox_ppm,
    )


# ── pin test ─────────────────────────────────────────────────────────────────
# source: v2-gas-chemistry §1 worked pin test
# HC=80ppm, CO=0.18%, CO2=14.6%, O2=1.8% → λ ≈ 1.080 (±0.002)


def test_brettschneider_pin_standard_reference():
    """Pin test from v2-gas-chemistry §1 — petrol reference values."""
    gas = _gas(co_pct=0.18, hc_ppm=80.0, co2_pct=14.6, o2_pct=1.8)
    result = _brettschneider(gas)
    assert 1.078 <= result <= 1.082, f"Expected λ ≈ 1.080 ± 0.002, got {result}"


# ── stoichiometric point ─────────────────────────────────────────────────────


def test_brettschneider_near_stoichiometric():
    """Near-perfect combustion should yield λ ≈ 1.0."""
    gas = _gas(co_pct=0.01, hc_ppm=10.0, co2_pct=14.7, o2_pct=0.5)
    result = _brettschneider(gas)
    assert 0.97 <= result <= 1.04, f"Expected λ ≈ 1.0, got {result}"


def test_brettschneider_rich_mixture():
    """High CO, low O2 → λ < 1.0 (rich)."""
    gas = _gas(co_pct=3.5, hc_ppm=200.0, co2_pct=12.0, o2_pct=0.2)
    result = _brettschneider(gas)
    assert result < 1.0, f"Expected rich (λ < 1.0), got {result}"


def test_brettschneider_lean_mixture():
    """Low CO, high O2 → λ > 1.0 (lean)."""
    gas = _gas(co_pct=0.02, hc_ppm=30.0, co2_pct=14.0, o2_pct=2.5)
    result = _brettschneider(gas)
    assert result > 1.0, f"Expected lean (λ > 1.0), got {result}"


# ── edge cases ───────────────────────────────────────────────────────────────


def test_brettschneider_zero_co2_guard():
    """CO2=0.0 must not divide-by-zero; internal guard clamps to 0.001."""
    gas = _gas(co_pct=0.1, hc_ppm=50.0, co2_pct=0.0, o2_pct=20.9)
    result = _brettschneider(gas)
    assert not math.isnan(result)
    assert not math.isinf(result)
    assert result > 0.0


def test_brettschneider_all_zeros():
    """All-zero input must not crash (denominator-zero guard).

    The internal zero-CO2 guard clamps CO2 to 0.001, producing λ = 1.0
    rather than a division-by-zero crash.
    """
    gas = _gas(co_pct=0.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=0.0)
    result = _brettschneider(gas)
    assert not math.isnan(result)
    assert not math.isinf(result)
    assert result == 1.0


# ── monotonicity ─────────────────────────────────────────────────────────────


def test_brettschneider_increasing_co_decreases_lambda():
    """Higher CO (richer) → lower lambda, monotonic."""
    base = _gas(co_pct=0.1, hc_ppm=80.0, co2_pct=14.5, o2_pct=1.0)
    richer = _gas(co_pct=2.0, hc_ppm=80.0, co2_pct=14.5, o2_pct=1.0)
    assert _brettschneider(richer) < _brettschneider(base)


def test_brettschneider_increasing_o2_increases_lambda():
    """Higher O2 (leaner) → higher lambda, monotonic."""
    base = _gas(co_pct=0.1, hc_ppm=80.0, co2_pct=14.5, o2_pct=0.5)
    leaner = _gas(co_pct=0.1, hc_ppm=80.0, co2_pct=14.5, o2_pct=3.0)
    assert _brettschneider(leaner) > _brettschneider(base)


# ── parametrized known values ────────────────────────────────────────────────
# source: v2-gas-chemistry §1 Brettschneider formula


@pytest.mark.parametrize(
    "co_pct, hc_ppm, co2_pct, o2_pct, expected_range",
    [
        # Standard pin from v2-gas-chemistry §1
        (0.18, 80.0, 14.6, 1.8, (1.078, 1.082)),
        # Typical idle — slightly rich
        (0.5, 100.0, 14.0, 1.0, (0.96, 1.04)),
        # Lean cruise
        (0.02, 20.0, 14.5, 2.0, (1.03, 1.10)),
        # Rich WOT
        (4.0, 300.0, 11.5, 0.3, (0.70, 0.90)),
    ],
)
def test_brettschneider_parametrized(co_pct, hc_ppm, co2_pct, o2_pct, expected_range):
    """Parametrized Brettschneider checks across operating conditions."""
    gas = _gas(co_pct=co_pct, hc_ppm=hc_ppm, co2_pct=co2_pct, o2_pct=o2_pct)
    result = _brettschneider(gas)
    lo, hi = expected_range
    assert lo <= result <= hi, f"Expected λ ∈ [{lo}, {hi}], got {result}"


# ── reproducibility ──────────────────────────────────────────────────────────


def test_brettschneider_deterministic():
    """Same input must produce identical output every call."""
    gas = _gas(co_pct=0.18, hc_ppm=80.0, co2_pct=14.6, o2_pct=1.8)
    results = [_brettschneider(gas) for _ in range(10)]
    assert all(r == results[0] for r in results)
