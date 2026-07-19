"""Isolation tests for vinlab.overlay.stress_rpm."""

from __future__ import annotations

from vinlab.models import Horizon
from vinlab.overlay.stress_rpm import stress_idle_rpm


def test_euro1_naturally_aspirated_uses_legacy_baseline(make_stress_profile) -> None:
    profile = make_stress_profile(euro="EURO_1", horizon=Horizon.LEGACY)

    result = stress_idle_rpm(**profile)

    assert result == 3000  # characterization: stress_rpm table source comments.


def test_euro2_small_naturally_aspirated_uses_small_displacement_target(make_stress_profile) -> None:
    profile = make_stress_profile(euro="EURO_2", displacement=1.8)

    result = stress_idle_rpm(**profile)

    assert result == 3500  # characterization: stress_rpm table source comments.


def test_euro4_large_naturally_aspirated_uses_large_displacement_target(make_stress_profile) -> None:
    profile = make_stress_profile(euro="EURO_4", displacement=2.0)

    result = stress_idle_rpm(**profile)

    assert result == 4000  # characterization: stress_rpm table source comments.


def test_euro5_turbo_uses_boost_target(make_stress_profile) -> None:
    profile = make_stress_profile(euro="EURO_5", induction="TURBOCHARGED")

    result = stress_idle_rpm(**profile)

    assert result == 4000  # characterization: stress_rpm table source comments.


def test_euro6_gdi_uses_high_pressure_fuel_target(make_stress_profile) -> None:
    profile = make_stress_profile(euro="EURO_6", fuel_delivery="GDI")

    result = stress_idle_rpm(**profile)

    assert result == 4500  # characterization: stress_rpm table source comments.


def test_unrecognised_euro_falls_back_to_horizon(make_stress_profile) -> None:
    modern_profile = make_stress_profile(euro="EURO_UNKNOWN", horizon=Horizon.MODERN)

    result = stress_idle_rpm(**modern_profile)

    assert result == 4000  # characterization: horizon fallback branch.
