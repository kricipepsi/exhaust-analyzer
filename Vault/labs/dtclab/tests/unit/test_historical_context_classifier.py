"""Tests for historical_context_classifier per DTC_VOCABULARY.md §9."""

from __future__ import annotations

import pytest

from dtclab.core.historical_context_classifier import classify_historical_context
from dtclab.schemas.vocabulary import HistoricalFaultContext as HFC


# -- Priority-order structural tests (cold-start dominates) ------------------


def test_cold_start_transit_dominates_idle():
    """ECT < 60 must return COLD_START_TRANSIT_FAULT even when RPM/load match idle."""
    result = classify_historical_context(coolant_temp_c=40.0, engine_rpm=500, calculated_load_pct=10.0)
    assert result == HFC.COLD_START_TRANSIT_FAULT


def test_cold_start_transit_dominates_load():
    """ECT < 60 must return COLD_START_TRANSIT_FAULT even when RPM/load match load."""
    result = classify_historical_context(coolant_temp_c=55.0, engine_rpm=3000, calculated_load_pct=60.0)
    assert result == HFC.COLD_START_TRANSIT_FAULT


def test_cold_start_transit_any_rpm_load():
    """ECT < 60 always wins regardless of RPM/load values."""
    result = classify_historical_context(coolant_temp_c=0.0, engine_rpm=0, calculated_load_pct=0.0)
    assert result == HFC.COLD_START_TRANSIT_FAULT


# -- Historical idle fault --------------------------------------------------


@pytest.mark.parametrize(
    ("ect", "rpm", "load"),
    [
        (80.0, 750, 20.0),   # typical idle
        (90.0, 500, 10.0),   # low idle, low load
        (75.0, 999, 24.0),   # just inside both bounds
        (85.0, 100, 0.0),    # extreme low
    ],
)
def test_historical_idle_fault(ect, rpm, load):
    assert classify_historical_context(ect, rpm, load) == HFC.HISTORICAL_IDLE_FAULT


# -- Historical load fault --------------------------------------------------


@pytest.mark.parametrize(
    ("ect", "rpm", "load"),
    [
        (90.0, 3000, 60.0),   # typical load
        (85.0, 2500, 55.0),   # moderate load
        (80.0, 4000, 80.0),   # high load
        (95.0, 2001, 46.0),   # just inside both bounds
    ],
)
def test_historical_load_fault(ect, rpm, load):
    assert classify_historical_context(ect, rpm, load) == HFC.HISTORICAL_LOAD_FAULT


# -- Unknown ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("ect", "rpm", "load"),
    [
        (85.0, 1500, 35.0),   # mid-range — nothing matches
        (80.0, 1000, 20.0),   # RPM at idle boundary (1000 not < 1000)
        (80.0, 750, 25.0),    # load at idle boundary (25 not < 25)
        (90.0, 2000, 50.0),   # RPM at load boundary (2000 not > 2000)
        (90.0, 2500, 45.0),   # load at load boundary (45 not > 45)
        (75.0, 1000, 25.0),   # both at idle boundaries
        (75.0, 2000, 45.0),   # both at load boundaries
    ],
)
def test_unknown(ect, rpm, load):
    assert classify_historical_context(ect, rpm, load) == HFC.UNKNOWN


# -- ECT boundary -----------------------------------------------------------


def test_ect_exactly_60_is_not_cold_start():
    """Wiki says ECT < 60 (strict); ECT=60 is not cold start."""
    # RPM 750 / load 20 would be idle fault, so this should fall through to idle
    result = classify_historical_context(coolant_temp_c=60.0, engine_rpm=750, calculated_load_pct=20.0)
    assert result == HFC.HISTORICAL_IDLE_FAULT


def test_ect_below_60_is_cold_start():
    """ECT just below 60 is cold start."""
    result = classify_historical_context(coolant_temp_c=59.9, engine_rpm=3000, calculated_load_pct=60.0)
    assert result == HFC.COLD_START_TRANSIT_FAULT


# -- Idle part: only when load part doesn't match ---------------------------


def test_idle_rpm_only_not_enough():
    """RPM < 1000 alone is not enough; load must also be < 25."""
    result = classify_historical_context(coolant_temp_c=85.0, engine_rpm=500, calculated_load_pct=30.0)
    assert result == HFC.UNKNOWN


def test_idle_load_only_not_enough():
    """Load < 25 alone is not enough; RPM must also be < 1000."""
    result = classify_historical_context(coolant_temp_c=85.0, engine_rpm=1500, calculated_load_pct=10.0)
    assert result == HFC.UNKNOWN


# -- Load part: only when both parts match ----------------------------------


def test_load_rpm_only_not_enough():
    """RPM > 2000 alone is not enough; load must also be > 45."""
    result = classify_historical_context(coolant_temp_c=85.0, engine_rpm=3000, calculated_load_pct=30.0)
    assert result == HFC.UNKNOWN


def test_load_load_only_not_enough():
    """Load > 45 alone is not enough; RPM must also be > 2000."""
    result = classify_historical_context(coolant_temp_c=85.0, engine_rpm=1000, calculated_load_pct=50.0)
    assert result == HFC.UNKNOWN


# -- Cross-check: idle matches but load also matches → idle wins ------------


def test_idle_beats_load():
    """Idle is checked before load in priority order."""
    # RPM=500 < 1000 (idle match) AND RPM > 2000 is false, so load can't match.
    # This is structural — idle and load RPM ranges are disjoint.
    # The priority is: cold-start > idle > load > unknown.
    result = classify_historical_context(coolant_temp_c=85.0, engine_rpm=500, calculated_load_pct=10.0)
    assert result == HFC.HISTORICAL_IDLE_FAULT
