"""Isolation tests for vinlab.overlay.switches."""

from __future__ import annotations

from vinlab.models import UpstreamO2Type
from vinlab.overlay.switches import derive_upstream_o2_type


def test_wideband_hint_wins_over_year_rule(make_switch_profile) -> None:
    profile = make_switch_profile(year=1999, o2_type_hint="WB")

    result = derive_upstream_o2_type(**profile)

    assert result == UpstreamO2Type.WIDEBAND_AFR


def test_narrowband_hint_wins_over_year_rule(make_switch_profile) -> None:
    profile = make_switch_profile(year=2010, o2_type_hint="NB")

    result = derive_upstream_o2_type(**profile)

    assert result == UpstreamO2Type.NARROWBAND


def test_post_2001_injected_petrol_defaults_to_wideband(make_switch_profile) -> None:
    profile = make_switch_profile(year=2001, fuel_delivery="PORT_INJECTION")

    result = derive_upstream_o2_type(**profile)

    assert result == UpstreamO2Type.WIDEBAND_AFR


def test_carburetor_defaults_to_narrowband(make_switch_profile) -> None:
    profile = make_switch_profile(year=2001, fuel_delivery="CARBURETOR")

    result = derive_upstream_o2_type(**profile)

    assert result == UpstreamO2Type.NARROWBAND
