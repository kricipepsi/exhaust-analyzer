"""Unit tests for VehicleContext.vin — backward compat, VIN+manual coexistence."""

from __future__ import annotations

import pytest

from engine.v2.input_model import VehicleContext


def test_vehicle_context_backward_compat_no_vin():
    """VehicleContext without vin works as before (backward compatible)."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595, my=2005
    )
    assert ctx.vin is None
    assert ctx.engine_code == "BSE"
    assert ctx.displacement_cc == 1595


def test_vehicle_context_with_vin():
    """VehicleContext with an explicit VIN field."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="WVWZZZ1KZAW123456"
    )
    assert ctx.vin == "WVWZZZ1KZAW123456"


def test_vehicle_context_vin_none_explicit():
    """VehicleContext with vin=None is equivalent to omitting it."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin=None
    )
    assert ctx.vin is None


def test_vehicle_context_vin_manual_coexistence():
    """VIN and manual fields coexist — manual is not overwritten by the field."""
    ctx = VehicleContext(
        brand="BMW", model="3er", engine_code="N46B20", displacement_cc=1995,
        my=2008, vin="WBA8E9C50GK647890"
    )
    assert ctx.vin == "WBA8E9C50GK647890"
    assert ctx.engine_code == "N46B20"  # manual value preserved in dataclass
    assert ctx.displacement_cc == 1995


def test_vehicle_context_slots_behavior():
    """VehicleContext uses __slots__ via slots=True."""
    ctx = VehicleContext(
        brand="TEST", model="X", engine_code="Y", displacement_cc=1000, my=2000
    )
    with pytest.raises(AttributeError):
        ctx.non_existent_field = 42
