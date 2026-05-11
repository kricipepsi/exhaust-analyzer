"""Unit tests for VL category 12 — VIN format + ISO 3779 checksum validation."""

from __future__ import annotations

import pytest

from engine.v2.input_model import (
    DiagnosticInput,
    ValidationWarning,
    VehicleContext,
)
from engine.v2.validation import validate


@pytest.fixture
def ctx_base() -> VehicleContext:
    return VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595, my=2005
    )


@pytest.fixture
def input_base(ctx_base: VehicleContext) -> DiagnosticInput:
    return DiagnosticInput(
        vehicle_context=ctx_base, dtcs=[], analyser_type="5-gas",
    )


# ── no VIN (optional field) ───────────────────────────────────────────────


def test_no_vin_produces_no_warning(input_base: DiagnosticInput) -> None:
    """When vin is None, no cat 12 warning is emitted."""
    result = validate(input_base)
    cat12_warnings = [w for w in result.warnings if w.category == 12]
    assert cat12_warnings == []


def test_empty_vin_produces_no_warning(ctx_base: VehicleContext) -> None:
    """When vin is empty string, cat 12 is skipped."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="",
    )
    diag = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    result = validate(diag)
    cat12_warnings = [w for w in result.warnings if w.category == 12]
    assert cat12_warnings == []


# ── format failures ───────────────────────────────────────────────────────


def test_vin_too_short(ctx_base: VehicleContext) -> None:
    """VIN shorter than 17 chars → cat 12 warning."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="WVWZZZ1K",
    )
    diag = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    result = validate(diag)
    cat12 = [w for w in result.warnings if w.category == 12]
    assert len(cat12) == 1
    assert "format" in cat12[0].message.lower()


def test_vin_invalid_characters(ctx_base: VehicleContext) -> None:
    """VIN with I, O, Q → cat 12 warning."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="IVWZZZ1KZOW12345Q",
    )
    diag = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    result = validate(diag)
    cat12 = [w for w in result.warnings if w.category == 12]
    assert len(cat12) == 1


# ── EU VIN: non-numeric at position 9 skips checksum ──────────────────────


def test_eu_vin_with_z_at_position_9_passes_silently(ctx_base: VehicleContext) -> None:
    """EU manufacturers place Z at position 9 to opt out of ISO 3779
    checksum. Cat 12 must accept this silently — no warning emitted."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="WVWZZZ1KZAW123456",
    )
    diag = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    result = validate(diag)
    cat12 = [w for w in result.warnings if w.category == 12]
    assert cat12 == []


# ── valid checksum (numeric at position 9) ─────────────────────────────────


def test_vin_with_valid_checksum_passes(ctx_base: VehicleContext) -> None:
    """A VIN with correct ISO 3779 check digit produces no cat 12 warning."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="1G8ZH5287VZ285065",
    )
    diag = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    result = validate(diag)
    cat12 = [w for w in result.warnings if w.category == 12]
    assert cat12 == []


# ── bad checksum (numeric at position 9) ───────────────────────────────────


def test_vin_bad_checksum_numeric_position_9(ctx_base: VehicleContext) -> None:
    """VIN with a numeric at position 9 still has its checksum validated.
    Wrong check digit → cat 12 warning."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="WVWZZZ1K0AW123456",
    )
    diag = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    result = validate(diag)
    cat12 = [w for w in result.warnings if w.category == 12]
    assert len(cat12) == 1
    assert "checksum" in cat12[0].message.lower()


# ── vehicle_context channel survives VIN rejection ────────────────────────


def test_vehicle_context_survives_vin_rejection(ctx_base: VehicleContext) -> None:
    """When VIN is rejected, the rest of vehicle_context is unaffected."""
    ctx = VehicleContext(
        brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
        my=2005, vin="BADVIN1234567890",
    )
    diag = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    result = validate(diag)
    # vehicle_context channel is not in invalid_channels
    assert "vehicle_context" not in result.invalid_channels
    # but a cat 12 warning was emitted
    cat12 = [w for w in result.warnings if w.category == 12]
    assert len(cat12) >= 1
    # gas_idle is not rejected by this
    assert "gas_idle" not in result.invalid_channels
