"""Property tests for combine_cf — invariants that hold for any valid input.

Pins two load-bearing properties per v2-property-tests §1:
  - CF always ∈ [-1.0, 1.0] for any sequence of valid CF weights.
  - CF always ∈ [0.0, 1.0] for non-negative weights (the M4 domain).
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from engine.v2.kg_engine import combine_cf

# ── strategies ───────────────────────────────────────────────────────────────

_CF_ANY = st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False)

_CF_NON_NEG = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)


# ── properties ───────────────────────────────────────────────────────────────


@given(weights=st.lists(_CF_ANY, min_size=1, max_size=20))
@settings(max_examples=200)
def test_cf_bounded_general(weights: list[float]) -> None:
    """combine_cf result is always in [-1.0, 1.0] for any valid CF weights."""
    result = combine_cf(weights)
    assert -1.0 - 1e-9 <= result <= 1.0 + 1e-9, (
        f"combine_cf({weights!r}) = {result!r} is outside [-1.0, 1.0]"
    )


@given(weights=st.lists(_CF_NON_NEG, min_size=1, max_size=20))
@settings(max_examples=200)
def test_cf_bounded_non_negative(weights: list[float]) -> None:
    """combine_cf result is always in [0.0, 1.0] for non-negative weights."""
    result = combine_cf(weights)
    assert 0.0 - 1e-9 <= result <= 1.0 + 1e-9, (
        f"combine_cf({weights!r}) = {result!r} is outside [0.0, 1.0]"
    )


@given(weights=st.lists(_CF_ANY, min_size=1, max_size=20))
@settings(max_examples=200)
def test_cf_deterministic(weights: list[float]) -> None:
    """combine_cf is deterministic — same input always produces same output."""
    r1 = combine_cf(weights)
    r2 = combine_cf(weights)
    assert r1 == r2


@given(weights=st.lists(_CF_ANY, min_size=0, max_size=0))
def test_cf_empty_is_zero(weights: list[float]) -> None:
    """Empty list always returns 0.0 (property check on boundary)."""
    assert combine_cf(weights) == 0.0


@given(weight=st.just(1.0), extra=st.lists(_CF_NON_NEG, min_size=0, max_size=15))
@settings(max_examples=100)
def test_cf_one_saturates(weight: float, extra: list[float]) -> None:
    """If any weight is 1.0 (absolute certainty), the combined result is 1.0."""
    weights = [weight] + extra
    result = combine_cf(weights)
    assert result <= 1.0 + 1e-9
