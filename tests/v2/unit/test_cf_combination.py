"""Golden-output tests for combine_cf (MYCIN Certainty Factor combination).

Validates every boundary case from v2-cf-inference §4.
Tolerance: ±0.001 (floating-point rounding).
"""

from __future__ import annotations

import math

import pytest

from engine.v2.kg_engine import combine_cf

TOLERANCE: float = 0.001


@pytest.mark.parametrize(
    "weights,expected",
    [
        ([], 0.0),
        ([0.0], 0.0),
        ([1.0], 1.0),
        ([0.5], 0.5),
        ([0.5, 0.5], 0.75),
        ([0.3, 0.4], 0.58),
        ([0.5, -0.5], 0.0),
        ([0.8, 0.8], 0.96),
        ([0.5, 0.5, 0.5], 0.875),
        ([1.0, 1.0], 1.0),
    ],
)
def test_combine_cf_golden_output(weights: list[float], expected: float) -> None:
    """CF combination matches v2-cf-inference §4 golden output."""
    result = combine_cf(weights)
    assert math.isclose(result, expected, abs_tol=TOLERANCE), (
        f"combine_cf({weights!r}) = {result!r}, expected {expected!r}"
    )


def test_combine_cf_empty_returns_zero() -> None:
    """Empty list returns 0.0 — explicit boundary test."""
    assert combine_cf([]) == 0.0


def test_combine_cf_single_value_is_identity() -> None:
    """Single input returns itself unchanged."""
    assert combine_cf([0.42]) == 0.42
    assert combine_cf([-0.3]) == -0.3


def test_combine_cf_never_exceeds_one() -> None:
    """CF combination never exceeds 1.0 for positive inputs."""
    result = combine_cf([0.9, 0.9, 0.9])
    assert result <= 1.0


def test_combine_cf_two_positives_mycin_rule() -> None:
    """Verify the MYCIN formula: a + b·(1 − a) for two positives."""
    a, b = 0.3, 0.4
    expected = a + b * (1.0 - a)  # 0.3 + 0.4*0.7 = 0.58
    assert math.isclose(combine_cf([a, b]), expected, abs_tol=TOLERANCE)


def test_combine_cf_opposite_signs_cancels() -> None:
    """Opposite-sign CFs: (a+b) / (1 − min(|a|,|b|))."""
    a, b = 0.6, -0.4
    expected = (a + b) / (1.0 - min(abs(a), abs(b)))  # 0.2 / 0.6 ≈ 0.3333
    assert math.isclose(combine_cf([a, b]), expected, abs_tol=TOLERANCE)


def test_combine_cf_all_negative_stays_negative() -> None:
    """Two negatives combine symmetrically; result stays negative."""
    result = combine_cf([-0.3, -0.4])
    assert result < 0.0
    assert result >= -1.0


def test_combine_cf_denom_zero_clamps() -> None:
    """When denominator is zero (a=1, b=-1), result is 0.0."""
    result = combine_cf([1.0, -1.0])
    assert math.isclose(result, 0.0, abs_tol=TOLERANCE)
