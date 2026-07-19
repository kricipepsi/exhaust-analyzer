"""Tests for TrimVectorAggregator per OBDLab_KG_Wiki.md §12."""

import pytest

from obdlab.core.exceptions import PIDValidationError
from obdlab.core.trim_vector_aggregator import TrimVectorAggregator

# ==================================================================
# 1-bank case
# ==================================================================

def test_one_bank_aggregation():
    """shrtft1 + longft1 with number_of_banks == 1 returns (bank1, None, None)."""
    pids = {"shrtft1": -10.0, "longft1": -25.0, "number_of_banks": 1}
    bank1, bank2, delta = TrimVectorAggregator.aggregate(pids)
    assert bank1 == -35.0
    assert bank2 is None
    assert delta is None


# ==================================================================
# 2-bank case
# ==================================================================

def test_two_bank_aggregation():
    """All four trim fields summed per-bank when number_of_banks == 2."""
    pids = {
        "shrtft1": -10.0, "longft1": -25.0,
        "shrtft2": 5.0, "longft2": -10.0,
        "number_of_banks": 2,
    }
    bank1, bank2, delta = TrimVectorAggregator.aggregate(pids)
    assert bank1 == -35.0  # wiki: §12.1 — shrtft1 + longft1
    assert bank2 == -5.0   # wiki: §12.1 — shrtft2 + longft2
    assert delta == -30.0   # bank1 (-35.0) - bank2 (-5.0)


# ==================================================================
# null-bank-2 respected (1-bank engine with None bank-2 fields)
# ==================================================================

def test_bank2_none_ignored_when_banks_1():
    """Bank-2 None fields are ignored when number_of_banks == 1."""
    pids = {"shrtft1": 8.5, "longft1": 3.2, "number_of_banks": 1}
    bank1, bank2, delta = TrimVectorAggregator.aggregate(pids)
    assert bank1 == 11.7
    assert bank2 is None
    assert delta is None


# ==================================================================
# number_of_banks == 2 with null bank-2 raises
# ==================================================================

def test_banks_2_with_null_shrtft2_raises():
    """number_of_banks == 2 but shrtft2 is None raises PIDValidationError."""
    pids = {"shrtft1": -10.0, "longft1": -25.0, "number_of_banks": 2, "shrtft2": None, "longft2": -10.0}
    with pytest.raises(PIDValidationError, match="shrtft2"):
        TrimVectorAggregator.aggregate(pids)


def test_banks_2_with_null_longft2_raises():
    """number_of_banks == 2 but longft2 is None raises PIDValidationError."""
    pids = {"shrtft1": -10.0, "longft1": -25.0, "number_of_banks": 2, "shrtft2": 5.0, "longft2": None}
    with pytest.raises(PIDValidationError, match="longft2"):
        TrimVectorAggregator.aggregate(pids)


# ==================================================================
# Missing required bank-1 fields
# ==================================================================

def test_missing_shrtft1_raises():
    """Missing shrtft1 raises PIDValidationError."""
    pids = {"longft1": -25.0, "number_of_banks": 1}
    with pytest.raises(PIDValidationError, match="shrtft1"):
        TrimVectorAggregator.aggregate(pids)


def test_missing_longft1_raises():
    """Missing longft1 raises PIDValidationError."""
    pids = {"shrtft1": -10.0, "number_of_banks": 1}
    with pytest.raises(PIDValidationError, match="longft1"):
        TrimVectorAggregator.aggregate(pids)
