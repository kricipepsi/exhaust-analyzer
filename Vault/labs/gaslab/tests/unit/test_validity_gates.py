"""Tests for gaslab.validity_gates — triangle gate and dilution screen."""

from __future__ import annotations

import pytest

from gaslab.contracts import GasReading, SampleValidity
from gaslab.validity_gates import dilution_gate, sample_validity, triangle_gate


# ---------------------------------------------------------------------------
# Triangle gate — GAS_WIKI §6.1
# ---------------------------------------------------------------------------


def test_triangle_valid_band() -> None:
    """14 ≤ CO+CO2+O2 ≤ 16 → VALID."""
    # Mid-band: sum = 0.3 + 14.8 + 0.2 = 15.3
    reading = GasReading(hc=20, co=0.3, co2=14.8, o2=0.2, nox=20)
    assert triangle_gate(reading) == SampleValidity.VALID


def test_triangle_external_o2_suspect() -> None:
    """16 < sum ≤ 18 → EXTERNAL_O2_SUSPECT."""
    # sum = 0.3 + 14.8 + 2.0 = 17.1
    reading = GasReading(hc=20, co=0.3, co2=14.8, o2=2.0, nox=20)
    assert triangle_gate(reading) == SampleValidity.EXTERNAL_O2_SUSPECT


@pytest.mark.parametrize(
    ("co", "co2", "o2", "label"),
    [
        (0.1, 3.0, 0.2, "sum_too_low"),  # sum = 3.3 < 14
        (0.1, 3.0, 10.5, "sum_still_low"),  # sum = 13.6 < 14
        (0.1, 14.0, 5.0, "sum_too_high"),  # sum = 19.1 > 18
    ],
)
def test_triangle_invalid(co: float, co2: float, o2: float, label: str) -> None:
    """sum < 14 or > 18 → INVALID."""
    reading = GasReading(hc=20, co=co, co2=co2, o2=o2, nox=20)
    assert triangle_gate(reading) == SampleValidity.INVALID, label


# ---------------------------------------------------------------------------
# Dilution screen — GAS_WIKI §6.2
# ---------------------------------------------------------------------------


def test_dilution_screen_floor() -> None:
    """CO+CO2 < 6 % → dilution gate returns False."""
    # sum = 0.3 + 14.8 = 15.1 > 6 → passes
    reading_good = GasReading(hc=20, co=0.3, co2=14.8, o2=0.2, nox=20)
    assert dilution_gate(reading_good) is True

    # sum = 0.1 + 4.0 = 4.1 < 6 → fails
    reading_bad = GasReading(hc=200, co=0.1, co2=4.0, o2=18.0, nox=10)
    assert dilution_gate(reading_bad) is False

    # sum = 6.0 exactly → fails (> 6, not >= 6)
    reading_edge = GasReading(hc=20, co=0.0, co2=6.0, o2=10.0, nox=20)
    assert dilution_gate(reading_edge) is False


# ---------------------------------------------------------------------------
# Combined sample_validity — GAS_WIKI §6.1 + §6.2
# ---------------------------------------------------------------------------


def test_sample_validity_triangle_wins() -> None:
    """Triangle INVALID takes priority — dilution not checked."""
    # sum = 0.1 + 3.0 + 0.2 = 3.3 < 14 → triangle INVALID
    reading = GasReading(hc=20, co=0.1, co2=3.0, o2=0.2, nox=20)
    assert sample_validity(reading) == SampleValidity.INVALID


def test_low_triangle_sum_with_high_hc_still_invalid() -> None:
    """Low triangle sum with non-normal HC remains INVALID at the gate."""
    # sum = 0.2 + 10.5 + 2.5 = 13.2 < 14; HC is not normal.
    reading = GasReading(hc=1500, co=0.2, co2=10.5, o2=2.5, nox=20)
    assert sample_validity(reading) == SampleValidity.INVALID


def test_sample_validity_dilution_fails() -> None:
    """Triangle VALID but dilution fails → INVALID."""
    # sum = 0.1 + 2.0 + 13.0 = 15.1 → triangle VALID
    # CO+CO2 = 2.1 < 6 → dilution fails
    reading = GasReading(hc=200, co=0.1, co2=2.0, o2=13.0, nox=10)
    assert triangle_gate(reading) == SampleValidity.VALID
    assert dilution_gate(reading) is False
    assert sample_validity(reading) == SampleValidity.INVALID


def test_sample_validity_all_green() -> None:
    """Both gates pass → VALID."""
    reading = GasReading(hc=20, co=0.3, co2=14.8, o2=0.2, nox=20)
    assert sample_validity(reading) == SampleValidity.VALID


def test_sample_validity_o2_suspect_passes_dilution() -> None:
    """Triangle EXTERNAL_O2_SUSPECT + dilution pass → EXTERNAL_O2_SUSPECT."""
    # sum = 0.3 + 14.8 + 2.0 = 17.1 → EXTERNAL_O2_SUSPECT
    # CO+CO2 = 15.1 > 6 → dilution passes
    reading = GasReading(hc=20, co=0.3, co2=14.8, o2=2.0, nox=20)
    assert triangle_gate(reading) == SampleValidity.EXTERNAL_O2_SUSPECT
    assert dilution_gate(reading) is True
    assert sample_validity(reading) == SampleValidity.EXTERNAL_O2_SUSPECT
