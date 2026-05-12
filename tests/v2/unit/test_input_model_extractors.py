"""Tests for signal extraction helpers in engine.v2.input_model."""

from __future__ import annotations

import pytest

from engine.v2.input_model import (
    FreezeFrameRecord,
    OBDRecord,
    extract_ect,
    extract_fuel_status,
    extract_rpm,
)

# ── fixtures ─────────────────────────────────────────────────────────────────


def _obd(ect=90.0, rpm=800, fuel_status="CL"):
    return OBDRecord(ect_c=ect, rpm=rpm, fuel_status=fuel_status)


def _ff(ect=20.0, rpm=0, fuel_status="OL"):
    return FreezeFrameRecord(ect_c=ect, rpm=rpm, fuel_status=fuel_status)


# ── extract_ect ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "obd,ff,expected",
    [
        (_obd(ect=90.0), _ff(ect=20.0), 90.0),
        (None, _ff(ect=50.0), 50.0),
        (None, None, None),
    ],
)
def test_extract_ect(obd, ff, expected):
    assert extract_ect(obd, ff) == expected


# ── extract_rpm ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "obd,ff,expected",
    [
        (_obd(rpm=2500), _ff(rpm=800), 2500),
        (None, _ff(rpm=1200), 1200),
        (None, None, None),
    ],
)
def test_extract_rpm(obd, ff, expected):
    assert extract_rpm(obd, ff) == expected


# ── extract_fuel_status ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "obd,ff,expected",
    [
        (_obd(fuel_status="CL"), _ff(fuel_status="OL_DRIVE"), "CL"),
        (None, _ff(fuel_status="OL_FAULT"), "OL_FAULT"),
        (None, None, None),
    ],
)
def test_extract_fuel_status(obd, ff, expected):
    assert extract_fuel_status(obd, ff) == expected
