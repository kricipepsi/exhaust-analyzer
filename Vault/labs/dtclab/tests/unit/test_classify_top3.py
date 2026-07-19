"""Tests for classify_top3 — DTCLab Phase 2 top-3 emission.

Verifies: ≤3 output, confidences in [0,1], clamp is unit-interval only,
family dedup keeps max, families are canonical, deterministic tie-break,
no sum-1 normalisation, empty on no evidence.
"""

from __future__ import annotations

import pytest
from dtclab.family_map import CANONICAL_FAMILIES
from dtclab.ranking import classify_top3
from dtclab.schemas.payload import DTCLabPayload, FreezeFrameRecord
from dtclab.schemas.vocabulary import (
    DTCRoutingTag,
    FuelSystemStatus,
    HistoricalFaultContext,
)


def _freeze_frame() -> FreezeFrameRecord:
    return FreezeFrameRecord(
        coolant_temp_c=85.0,
        calculated_load_pct=30.0,
        engine_rpm=800,
        vehicle_speed_kmh=0,
        short_term_ft1=0.0,
        long_term_ft1=0.0,
        manifold_pressure_kpa=100.0,
        maf_gps=5.0,
        ignition_advance_deg=10.0,
        throttle_pos_pct=15.0,
        intake_air_temp_c=25.0,
        fuel_system_status=FuelSystemStatus.CL,
    )


def _empty_payload() -> DTCLabPayload:
    return DTCLabPayload(
        active_mil=False,
        mil_flashing=False,
        confirmed_dtcs=[],
        pending_dtcs=[],
        permanent_dtcs=[],
        routing_tags=[],
        mode_06_monitors={},
        historical_fault_context=HistoricalFaultContext.UNKNOWN,
        freeze_frame=_freeze_frame(),
    )


def _payload_with_tags(*tags: str) -> DTCLabPayload:
    return DTCLabPayload(
        active_mil=False,
        mil_flashing=False,
        confirmed_dtcs=[],
        pending_dtcs=[],
        permanent_dtcs=[],
        routing_tags=[DTCRoutingTag(t) for t in tags],
        mode_06_monitors={},
        historical_fault_context=HistoricalFaultContext.UNKNOWN,
        freeze_frame=_freeze_frame(),
    )


def _payload_with_dtcs(dtcs: list[str], *, state: str = "confirmed") -> DTCLabPayload:
    p = _empty_payload()
    if state == "confirmed":
        p = p.model_copy(update={"confirmed_dtcs": dtcs})
    elif state == "pending":
        p = p.model_copy(update={"pending_dtcs": dtcs})
    elif state == "permanent":
        p = p.model_copy(update={"permanent_dtcs": dtcs})
    return p


# =============================================================================
# Test: returns at most three
# =============================================================================


def test_returns_at_most_three():
    """classify_top3 must return at most 3 candidates."""
    payload = _payload_with_tags(
        "LEAN_HISTORY",
        "RICH_HISTORY",
        "MISFIRE_HISTORY",
        "O2_HISTORY",
        "VVT_HISTORY",
        "ECU_INTERNAL_HISTORY",
        "KNOCK_HISTORY",
        "INJECTOR_HISTORY",
    )
    result = classify_top3(payload)
    assert len(result) <= 3

    payload2 = _payload_with_tags("LEAN_HISTORY", "MISFIRE_HISTORY")
    result2 = classify_top3(payload2)
    assert len(result2) == 2

    result3 = classify_top3(_empty_payload())
    assert result3 == []


# =============================================================================
# Test: confidences in [0,1]
# =============================================================================


def test_confidences_in_unit_interval():
    """Every confidence must be in [0.0, 1.0]."""
    payload = _payload_with_tags("LEAN_HISTORY", "MISFIRE_HISTORY", "RICH_HISTORY")
    result = classify_top3(payload)
    assert len(result) > 0
    for _family, conf in result:
        assert 0.0 <= conf <= 1.0, f"{_family} confidence {conf} not in [0,1]"


# =============================================================================
# Test: clamp is unit-interval only (no family-keyed or tier-keyed constant)
# =============================================================================


def test_clamp_is_unit_interval_only():
    """Clamp is min(max(x,0),1) — no family-keyed or tier-keyed constant."""
    # A confirmed DTC sets raw_confidence = 1.0 × dna_factor.
    # With no DNA view, dna_factor for LEAN_HISTORY (ungated) = 1.0 → raw=1.0.
    # classify_top3 must emit exactly 1.0, not something lower.
    payload = _payload_with_dtcs(["P0171"], state="confirmed")
    payload = payload.model_copy(update={
        "routing_tags": [DTCRoutingTag.LEAN_HISTORY]
    })
    result = classify_top3(payload)
    assert len(result) == 1
    family, conf = result[0]
    assert family == "lean_condition"
    assert conf == 1.0  # no family-specific downscaling

    # With no evidence, confidence is 0.0 (mode06_passed baseline × dna_factor)
    payload2 = _payload_with_tags("LEAN_HISTORY")
    result2 = classify_top3(payload2)
    assert len(result2) == 1
    assert result2[0][1] == 0.0


# =============================================================================
# Test: family dedup keeps max
# =============================================================================


def test_family_dedup_keeps_max():
    """No duplicate families in output; first occurrence carries max confidence."""
    payload = _payload_with_tags("LEAN_HISTORY", "MISFIRE_HISTORY")
    result = classify_top3(payload)
    result_families = [f for f, _ in result]
    assert len(result) == len(set(result_families)), (
        "classify_top3 produced duplicate families"
    )

    # With distinct confidence, dedup preserves the max (first in sorted order)
    payload2 = _payload_with_dtcs(["P0171"], state="confirmed")
    payload2 = payload2.model_copy(update={
        "routing_tags": [DTCRoutingTag.LEAN_HISTORY, DTCRoutingTag.MISFIRE_HISTORY]
    })
    result2 = classify_top3(payload2)
    # lean_condition = 1.0, misfire = 0.0 → lean first, no duplicate families
    families2 = [f for f, _ in result2]
    assert "lean_condition" in families2
    assert "misfire" in families2
    assert len(families2) == len(set(families2))


# =============================================================================
# Test: families are canonical
# =============================================================================


def test_families_are_canonical():
    """Every emitted family must be in CANONICAL_FAMILIES; never a tag string or POA."""
    payload = _payload_with_tags(
        "LEAN_HISTORY", "MISFIRE_HISTORY", "RICH_HISTORY",
        "O2_HISTORY", "CATALYST_HISTORY",
    )
    result = classify_top3(payload)
    for family, _conf in result:
        assert family in CANONICAL_FAMILIES, (
            f"family {family!r} not in CANONICAL_FAMILIES"
        )
        try:
            DTCRoutingTag(family)
            pytest.fail(f"Raw DTCRoutingTag value {family!r} leaked into families")
        except ValueError:
            pass

    # POA_HISTORY must never appear
    payload_poa = _payload_with_tags("POA_HISTORY")
    result_poa = classify_top3(payload_poa)
    poa_families = {f for f, _ in result_poa}
    assert "POA_HISTORY" not in poa_families
    assert len(result_poa) == 0


# =============================================================================
# Test: tie-break deterministic
# =============================================================================


def test_tie_break_deterministic():
    """Ties break by (-confidence, family) — exact ordering on equal confidence."""
    # With routing tags only (no DTC evidence), all families get
    # mode06_passed weight (0.0) × dna_factor = 0.0.
    payload = _payload_with_tags("LEAN_HISTORY", "MISFIRE_HISTORY", "RICH_HISTORY")
    result = classify_top3(payload)

    # With equal confidence, families sort alphabetically
    families = [f for f, _ in result]
    assert families == sorted(families), (
        f"tie-break failed: {families} != {sorted(families)}"
    )

    # With distinct confidences — highest first
    payload2 = _payload_with_dtcs(["P0171"], state="confirmed")
    payload2 = payload2.model_copy(update={
        "routing_tags": [DTCRoutingTag.LEAN_HISTORY, DTCRoutingTag.MISFIRE_HISTORY]
    })
    result2 = classify_top3(payload2)
    assert result2[0][0] == "lean_condition"
    assert result2[0][1] > result2[1][1]


# =============================================================================
# Test: does not normalise to 1
# =============================================================================


def test_does_not_normalise_to_one():
    """Confidences are NOT rescaled to sum 1 (Bayesian combine() does fusion)."""
    payload = _payload_with_dtcs(["P0171", "P0300"], state="confirmed")
    payload = payload.model_copy(update={
        "routing_tags": [DTCRoutingTag.LEAN_HISTORY, DTCRoutingTag.MISFIRE_HISTORY]
    })
    result = classify_top3(payload)
    assert len(result) >= 2

    total = sum(conf for _, conf in result)
    assert total > 1.0 or len(result) == 1, (
        f"confidences sum to {total} — appears normalised to 1 (DESIGN §4 forbids this)"
    )


# =============================================================================
# Test: empty when no evidence
# =============================================================================


def test_empty_when_no_evidence():
    """A payload with no routing-relevant DTCs/monitors emits []."""
    result = classify_top3(_empty_payload())
    assert result == []

    # Context-only tags produce no candidates
    payload_ctx = _payload_with_tags("EGR_HISTORY", "EVAP_HISTORY", "THERMAL_HISTORY")
    result_ctx = classify_top3(payload_ctx)
    assert result_ctx == []
