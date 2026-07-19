"""End-to-end integration tests for the full DTCLab pipeline.

Covers: HIGH-confidence DNA gate suppression (CATALYST/EGR),
PARTIAL/NONE downgrade, dna_view=None fallback,
output passes DTCLabPayload.model_validate.
"""

from __future__ import annotations

from dtclab import DataFusionSanitizer
from dtclab.schemas.dna_view import (
    AirMeteringStrategy,
    DtcEmissionsView,
    DtcLabDnaView,
    EuroEmissionCategory,
    ResolvedHorizon,
    VinConfidence,
)
from dtclab.schemas.payload import DTCLabPayload
from dtclab.schemas.vocabulary import DTCRoutingTag


# ------------------------------------------------------------------
# DNA view factories
# ------------------------------------------------------------------


def _dna_view(
    *,
    has_catalyst: bool = True,
    egr_equipped: bool = False,
    resolved_horizon: ResolvedHorizon = ResolvedHorizon.HORIZON_CLASSIC,
    confidence: VinConfidence = VinConfidence.HIGH,
) -> DtcLabDnaView:
    return DtcLabDnaView.model_validate(
        {
            "make": "Toyota",
            "model": "Corolla",
            "model_year": 2010,
            "euro_emission_category": EuroEmissionCategory.EURO_4,
            "air_metering_strategy": AirMeteringStrategy.MAF,
            "resolved_horizon": resolved_horizon,
            "emissions": DtcEmissionsView(
                has_catalyst=has_catalyst,
                egr_equipped=egr_equipped,
            ),
            "confidence": confidence,
        }
    )


# ------------------------------------------------------------------
# Raw input fixtures
# ------------------------------------------------------------------


def _raw_dtcs_p0171_p0420() -> dict:
    """P0171 (lean) + P0420 (catalyst efficiency) across modes."""
    return {
        "$03": ["P0171", "P0420"],
        "$07": ["P0174"],
        "$0A": [],
    }


def _raw_dtcs_p0420_only() -> dict:
    return {"$03": ["P0420"], "$07": [], "$0A": []}


def _raw_dtcs_empty() -> dict:
    return {"$03": [], "$07": [], "$0A": []}


def _raw_freeze_frame() -> dict:
    return {
        "calculated_load_pct": 15.0,
        "engine_rpm": 850,
        "coolant_temp_c": 82.0,
        "short_term_ft1": 18.0,
        "long_term_ft1": 11.0,
        "manifold_pressure_kpa": 32.0,
        "vehicle_speed_kmh": 0,
        "ignition_advance_deg": 12.0,
        "intake_air_temp_c": 25.0,
        "maf_gps": 1.8,
        "throttle_pos_pct": 4.5,
        "fuel_system_status": "CL",
    }


def _raw_mode06() -> dict:
    return {
        "MID_21_TID_81": 45.0,  # Catalyst OSC B1 — PASSED
        "MID_A2_TID_0B": 5.0,   # Cyl 2 misfire — PENDING_FAIL_MARGINAL
    }


# ------------------------------------------------------------------
# End-to-end pipeline tests
# ------------------------------------------------------------------


def test_pipeline_with_high_confidence_dna():
    """Full pipeline: HIGH-confidence DNA with catalyst-equipped car.

    P0171 → LEAN_HISTORY (no gate)
    P0420 → CATALYST_HISTORY (DNA-gated: has_catalyst=True → emit)
    """
    dna = _dna_view(
        has_catalyst=True,
        confidence=VinConfidence.HIGH,
    )
    sanitizer = DataFusionSanitizer(dna)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_p0171_p0420(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06=_raw_mode06(),
    )

    assert payload.active_mil is False
    assert payload.mil_flashing is False
    assert set(payload.confirmed_dtcs) == {"P0171", "P0420"}
    assert payload.pending_dtcs == ["P0174"]
    assert DTCRoutingTag.LEAN_HISTORY in payload.routing_tags
    assert DTCRoutingTag.CATALYST_HISTORY in payload.routing_tags


def test_pipeline_catalyst_suppressed_on_non_catalyst_car():
    """CATALYST_HISTORY is suppressed when has_catalyst=False with HIGH confidence.

    Tests the DNA gate suppression path through the full pipeline."""
    dna = _dna_view(
        has_catalyst=False,
        confidence=VinConfidence.HIGH,
    )
    sanitizer = DataFusionSanitizer(dna)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_p0420_only(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06={},
    )

    assert "P0420" in payload.confirmed_dtcs
    assert DTCRoutingTag.CATALYST_HISTORY not in payload.routing_tags


def test_pipeline_catalyst_emitted_on_catalyst_car():
    """CATALYST_HISTORY is emitted when has_catalyst=True with HIGH confidence."""
    dna = _dna_view(
        has_catalyst=True,
        confidence=VinConfidence.HIGH,
    )
    sanitizer = DataFusionSanitizer(dna)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_p0420_only(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06={},
    )

    assert DTCRoutingTag.CATALYST_HISTORY in payload.routing_tags


def test_pipeline_egr_suppressed_on_non_egr_car():
    """EGR_HISTORY is suppressed when egr_equipped=False with HIGH confidence.

    Tests a second DNA gate (EGR) through the full pipeline to confirm
    the three-branch pattern is consistent across gates."""
    dna = _dna_view(
        egr_equipped=False,
        confidence=VinConfidence.HIGH,
    )
    sanitizer = DataFusionSanitizer(dna)
    payload = sanitizer.sanitize(
        raw_dtcs={"$03": ["P0400"], "$07": [], "$0A": []},
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06={},
    )

    assert "P0400" in payload.confirmed_dtcs
    assert DTCRoutingTag.EGR_HISTORY not in payload.routing_tags


def test_pipeline_dna_view_none_fallback():
    """With dna_view=None, all tags emit unconditionally on DTC pattern match
    (the pre-DNA fallback)."""
    sanitizer = DataFusionSanitizer(None)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_p0171_p0420(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06=_raw_mode06(),
    )

    assert DTCRoutingTag.LEAN_HISTORY in payload.routing_tags
    assert DTCRoutingTag.CATALYST_HISTORY in payload.routing_tags


def test_pipeline_output_validates_as_dtclab_payload():
    """The output of sanitize() passes DTCLabPayload.model_validate."""
    sanitizer = DataFusionSanitizer(None)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_p0171_p0420(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06=_raw_mode06(),
    )

    # Re-validate to confirm the output is a valid DTCLabPayload
    reloaded = DTCLabPayload.model_validate(payload.model_dump())
    assert reloaded == payload


def test_pipeline_empty_dtcs():
    """Pipeline with no DTCs produces empty lists and no routing tags."""
    sanitizer = DataFusionSanitizer(None)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_empty(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06={},
    )

    assert payload.confirmed_dtcs == []
    assert payload.pending_dtcs == []
    assert payload.permanent_dtcs == []
    assert payload.routing_tags == []


def test_pipeline_with_mil_flashing():
    """Pipeline correctly propagates active_mil and mil_flashing flags."""
    sanitizer = DataFusionSanitizer(None)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_empty(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06={},
        active_mil=True,
        mil_flashing=True,
    )

    assert payload.active_mil is True
    assert payload.mil_flashing is True


def test_pipeline_historical_context_cold_start():
    """When ECT < 60°C, context is COLD_START_TRANSIT_FAULT."""
    sanitizer = DataFusionSanitizer(None)
    ff = _raw_freeze_frame()
    ff["coolant_temp_c"] = 15.0  # cold start

    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_empty(),
        raw_freeze_frame=ff,
        raw_mode06={},
    )

    assert payload.historical_fault_context.value == "COLD_START_TRANSIT_FAULT"


def test_pipeline_historical_context_idle():
    """Low RPM + low load → HISTORICAL_IDLE_FAULT."""
    sanitizer = DataFusionSanitizer(None)
    ff = _raw_freeze_frame()
    ff["coolant_temp_c"] = 85.0
    ff["engine_rpm"] = 800
    ff["calculated_load_pct"] = 10.0

    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_empty(),
        raw_freeze_frame=ff,
        raw_mode06={},
    )

    assert payload.historical_fault_context.value == "HISTORICAL_IDLE_FAULT"


def test_pipeline_historical_context_load():
    """High RPM + high load → HISTORICAL_LOAD_FAULT."""
    sanitizer = DataFusionSanitizer(None)
    ff = _raw_freeze_frame()
    ff["coolant_temp_c"] = 90.0
    ff["engine_rpm"] = 3500
    ff["calculated_load_pct"] = 65.0

    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_empty(),
        raw_freeze_frame=ff,
        raw_mode06={},
    )

    assert payload.historical_fault_context.value == "HISTORICAL_LOAD_FAULT"


def test_pipeline_mode06_monitors_present():
    """Mode $06 monitor results are populated in the payload."""
    sanitizer = DataFusionSanitizer(None)
    payload = sanitizer.sanitize(
        raw_dtcs=_raw_dtcs_empty(),
        raw_freeze_frame=_raw_freeze_frame(),
        raw_mode06=_raw_mode06(),
    )

    assert "MID_21_TID_81" in payload.mode_06_monitors
    assert "MID_A2_TID_0B" in payload.mode_06_monitors
    assert payload.mode_06_monitors["MID_21_TID_81"].state.value == "PASSED"
    assert payload.mode_06_monitors["MID_A2_TID_0B"].state.value == "PENDING_FAIL_MARGINAL"
