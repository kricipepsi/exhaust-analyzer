"""Isolation tests for vinlab.overlay.horizon."""

from __future__ import annotations

import pytest

from vinlab.models import Horizon
from vinlab.overlay.horizon import _year_to_horizon, euro_to_horizon


@pytest.mark.parametrize(
    ("euro", "expected"),
    [
        ("EURO_1", Horizon.LEGACY),
        ("EURO_2", Horizon.LEGACY),
        ("EURO_3", Horizon.ADAPTIVE),
        ("EURO_4", Horizon.ADAPTIVE),
        ("EURO_5", Horizon.MODERN),
        ("EURO_6", Horizon.MODERN),
        ("EURO_7", Horizon.MODERN),
    ],
)
def test_euro_to_horizon_matches_contract(euro: str, expected: Horizon) -> None:
    """All EuroEmissionCategory values map per SEMANTIC_CONTRACT.md section 6.4."""
    assert euro_to_horizon(euro) == expected


def test_euro_to_horizon_rejects_unknown_category() -> None:
    with pytest.raises(ValueError, match="EURO_UNKNOWN"):
        euro_to_horizon("EURO_UNKNOWN")


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (1990, Horizon.LEGACY),
        (2000, Horizon.LEGACY),
        (2001, Horizon.ADAPTIVE),
        (2010, Horizon.ADAPTIVE),
        (2011, Horizon.MODERN),
        (2020, Horizon.MODERN),
    ],
)
def test_year_to_horizon_matches_vinlookup_bands(year: int, expected: Horizon) -> None:
    """Year bands follow VINlookup.md's 1990-2000, 2001-2010, 2011+ split."""
    assert _year_to_horizon(year) == expected
