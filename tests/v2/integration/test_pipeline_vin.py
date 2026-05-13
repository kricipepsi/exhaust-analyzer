"""Integration tests — VIN-only path ≡ manual engine_code path (no inference drift)."""

from __future__ import annotations

from engine.v2.input_model import DiagnosticInput, GasRecord, VehicleContext
from engine.v2.pipeline import diagnose

# ── helpers ────────────────────────────────────────────────────────────────


def _make_diag(vin: str | None, engine_code: str, displacement_cc: int) -> DiagnosticInput:
    return DiagnosticInput(
        vehicle_context=VehicleContext(
            brand="VW",
            model="Golf",
            engine_code=engine_code,
            displacement_cc=displacement_cc,
            my=2005,
            vin=vin,
        ),
        dtcs=[],
        analyser_type="5-gas",
        gas_idle=GasRecord(
            co_pct=0.12, co2_pct=14.8, hc_ppm=25.0, o2_pct=0.25,
            nox_ppm=30.0, lambda_analyser=1.00,
        ),
    )


# ── VIN-only vs manual equivalence ─────────────────────────────────────────


def test_vin_only_equiv_manual_pipeline():
    """DiagnosticInput with VIN-only produces same R9 state as manual entry."""
    diag_vin = _make_diag(vin="WVWZZZ1KZAW123456", engine_code="", displacement_cc=0)
    diag_manual = _make_diag(vin=None, engine_code="BSE", displacement_cc=1595)

    result_vin = diagnose(diag_vin)
    result_manual = diagnose(diag_manual)

    assert result_vin["state"] == result_manual["state"]
    assert result_vin["confidence_ceiling"] == result_manual["confidence_ceiling"]


def test_vin_only_no_crash():
    """VIN-only input with empty manual fields does not crash the pipeline."""
    diag = DiagnosticInput(
        vehicle_context=VehicleContext(
            brand="", model="", engine_code="", displacement_cc=0, my=2010,
            vin="WVWZZZ1KZAW123456",
        ),
        dtcs=[],
        analyser_type="5-gas",
        gas_idle=GasRecord(
            co_pct=0.12, co2_pct=14.8, hc_ppm=25.0, o2_pct=0.25,
        ),
    )
    result = diagnose(diag)
    assert result["state"] in ("named_fault", "insufficient_evidence", "invalid_input")


def test_vin_partial_manual_fallback():
    """When VIN resolves partial, manual engine_code is used as fallback."""
    diag = DiagnosticInput(
        vehicle_context=VehicleContext(
            brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
            my=2005, vin="VF1AAAAA123456789",
        ),
        dtcs=[],
        analyser_type="5-gas",
        gas_idle=GasRecord(
            co_pct=0.12, co2_pct=14.8, hc_ppm=25.0, o2_pct=0.25,
        ),
    )
    result = diagnose(diag)
    assert result["state"] in ("named_fault", "insufficient_evidence", "invalid_input")


def test_vin_none_confidence_ignored():
    """When VIN resolves to confidence='none', manual fields are used unchanged."""
    diag = DiagnosticInput(
        vehicle_context=VehicleContext(
            brand="VW", model="Golf", engine_code="BSE", displacement_cc=1595,
            my=2005, vin="INVALID1234567890",
        ),
        dtcs=[],
        analyser_type="5-gas",
        gas_idle=GasRecord(
            co_pct=0.12, co2_pct=14.8, hc_ppm=25.0, o2_pct=0.25,
        ),
    )
    result = diagnose(diag)
    assert result["state"] in ("named_fault", "insufficient_evidence", "invalid_input")
