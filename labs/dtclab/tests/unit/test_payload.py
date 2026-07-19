"""Unit tests for DTCLabPayload Pydantic constraint enforcement.

Covers: valid round-trip, malformed DTCs on all three mode lists,
routing_tags type enforcement, mode_06_monitors key validation.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dtclab.schemas.mode06_result import Mode06MonitorResult
from dtclab.schemas.payload import DTCLabPayload
from dtclab.schemas.vocabulary import (
    DTCRoutingTag,
    FuelSystemStatus,
    HistoricalFaultContext,
    Mode06MonitorState,
)


# ------------------------------------------------------------------
# Shared fixtures
# ------------------------------------------------------------------


def _valid_freeze_frame() -> dict:
    """Minimal valid freeze-frame record (all 12 mandatory PIDs + defaults)."""
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
        "fuel_system_status": FuelSystemStatus.CL,
        "ff_open_loop_at_fault": False,
        "ff_load_high_at_low_rpm": False,
        "ff_ect_warmup": False,
        "ff_iat_ect_biased": False,
        "ff_timing_retard_severe": False,
        "ff_codes_cleared_invalidated": False,
    }


def _valid_payload_dict() -> dict:
    """Baseline valid payload dictionary matching DTCLabPayload schema."""
    return {
        "active_mil": True,
        "mil_flashing": False,
        "confirmed_dtcs": ["P0171"],
        "pending_dtcs": [],
        "permanent_dtcs": [],
        "routing_tags": [DTCRoutingTag.LEAN_HISTORY],
        "mode_06_monitors": {
            "MID_21_TID_81": Mode06MonitorResult(
                monitor_id="MID_21_TID_81",
                state=Mode06MonitorState.PASSED,
                margin_pct=45.0,
                target_component="Catalyst OSC B1",
            ),
        },
        "historical_fault_context": HistoricalFaultContext.HISTORICAL_IDLE_FAULT,
        "freeze_frame": _valid_freeze_frame(),
    }


# ------------------------------------------------------------------
# Round-trip
# ------------------------------------------------------------------


def test_valid_payload_round_trips():
    """A fully valid payload dict round-trips through model_validate."""
    payload = DTCLabPayload.model_validate(_valid_payload_dict())
    assert payload.active_mil is True
    assert payload.mil_flashing is False
    assert payload.confirmed_dtcs == ["P0171"]
    assert payload.routing_tags == [DTCRoutingTag.LEAN_HISTORY]


def test_payload_serializes_to_json():
    """DTCLabPayload serializes and deserializes cleanly."""
    payload = DTCLabPayload.model_validate(_valid_payload_dict())
    json_str = payload.model_dump_json()
    assert isinstance(json_str, str)
    reloaded = DTCLabPayload.model_validate_json(json_str)
    assert reloaded.active_mil == payload.active_mil
    assert reloaded.confirmed_dtcs == payload.confirmed_dtcs


def test_payload_with_multiple_dtcs_and_tags():
    """Round-trip with multiple DTCs across modes and several routing tags."""
    data = _valid_payload_dict()
    data["confirmed_dtcs"] = ["P0171", "P0420", "P0300"]
    data["pending_dtcs"] = ["P0174"]
    data["permanent_dtcs"] = ["P0455"]
    data["routing_tags"] = [
        DTCRoutingTag.LEAN_HISTORY,
        DTCRoutingTag.CATALYST_HISTORY,
        DTCRoutingTag.MISFIRE_HISTORY,
    ]
    payload = DTCLabPayload.model_validate(data)
    assert len(payload.confirmed_dtcs) == 3
    assert len(payload.pending_dtcs) == 1
    assert len(payload.permanent_dtcs) == 1
    assert len(payload.routing_tags) == 3


# ------------------------------------------------------------------
# DTC list constraint violations
# ------------------------------------------------------------------


def test_malformed_dtc_in_confirmed_raises():
    """A DTC string not matching DTC_REGEX in confirmed_dtcs raises
    ValidationError (ERR-CONTRACT-001)."""
    data = _valid_payload_dict()
    data["confirmed_dtcs"] = ["P0171", "XYZ99"]  # XYZ99 is invalid
    with pytest.raises(ValidationError) as exc_info:
        DTCLabPayload.model_validate(data)
    assert "XYZ99" in str(exc_info.value)


def test_malformed_dtc_in_pending_raises():
    """A malformed DTC in pending_dtcs is also caught."""
    data = _valid_payload_dict()
    data["pending_dtcs"] = ["P9999"]  # subgroup digit 9 is invalid
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


def test_malformed_dtc_in_permanent_raises():
    """A malformed DTC in permanent_dtcs is also caught."""
    data = _valid_payload_dict()
    data["permanent_dtcs"] = ["D0171"]  # D is invalid class
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


def test_bp_form_regex_is_rejected():
    """The BP-form character class B-D,P,U is rejected by the canonical regex.

    P0171 is valid for [BCPU] but D0171 and any B/P/U codes outside the
    canonical form are rejected.  'B0xxx' codes start with B, which IS in
    the canonical [BCPU] set, but the test ensures 'Z' class fails.
    """
    data = _valid_payload_dict()
    data["confirmed_dtcs"] = ["Z0171"]  # Z is not in [BCPU]
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


def test_lowercase_dtc_is_rejected():
    """Lowercase DTC codes do not match the canonical regex (case-sensitive)."""
    data = _valid_payload_dict()
    data["confirmed_dtcs"] = ["p0171"]
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


def test_dtc_too_short_is_rejected():
    """A 4-character DTC does not match the 5-character canonical form."""
    data = _valid_payload_dict()
    data["confirmed_dtcs"] = ["P017"]
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


# ------------------------------------------------------------------
# routing_tags type enforcement
# ------------------------------------------------------------------


def test_routing_tags_with_invalid_string_raises():
    """Passing a raw string not in DTCRoutingTag raises ValidationError
    carrying ERR-CONTRACT-002 (wiki §11)."""
    data = _valid_payload_dict()
    data["routing_tags"] = ["NOT_A_TAG"]
    with pytest.raises(ValidationError) as exc_info:
        DTCLabPayload.model_validate(data)
    assert "ERR-CONTRACT-002" in str(exc_info.value)


def test_routing_tags_with_mixed_valid_invalid_raises():
    """A mix of valid and invalid tags also fails with ERR-CONTRACT-002."""
    data = _valid_payload_dict()
    data["routing_tags"] = [DTCRoutingTag.LEAN_HISTORY, "BOGUS_TAG"]
    with pytest.raises(ValidationError) as exc_info:
        DTCLabPayload.model_validate(data)
    assert "ERR-CONTRACT-002" in str(exc_info.value)


def test_empty_routing_tags_is_valid():
    """An empty routing_tags list is allowed."""
    data = _valid_payload_dict()
    data["routing_tags"] = []
    payload = DTCLabPayload.model_validate(data)
    assert payload.routing_tags == []


# ------------------------------------------------------------------
# mode_06_monitors key validation
# ------------------------------------------------------------------


def test_mode06_monitor_key_wrong_format_raises():
    """A monitor key not matching MID_<HEX>_TID_<HEX> form raises
    ValidationError.

    Uses a raw dict to bypass Mode06MonitorResult's own field validation
    so we test DTCLabPayload's key-level validator specifically."""
    data = _valid_payload_dict()
    # Build the dict manually with a bad key — Mode06MonitorResult won't
    # accept bad_key as monitor_id, so we pass a raw sub-dict.
    data["mode_06_monitors"] = {
        "bad_key": {
            "monitor_id": "MID_21_TID_81",
            "state": "PASSED",
            "margin_pct": 50.0,
            "target_component": "Something",
        },
    }
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


def test_mode06_monitor_key_lowercase_hex_is_rejected():
    """Lowercase hex in a monitor key fails the canonical pattern."""
    data = _valid_payload_dict()
    data["mode_06_monitors"] = {
        "MID_21_TID_81": {
            "monitor_id": "MID_21_TID_81",
            "state": "PASSED",
            "margin_pct": 50.0,
            "target_component": "Catalyst",
        },
        "mid_a2_tid_0b": {
            "monitor_id": "MID_A2_TID_0B",
            "state": "CRITICAL_FAIL",
            "margin_pct": -5.0,
            "target_component": "Misfire Cyl 2",
        },
    }
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


def test_empty_mode06_monitors_is_valid():
    """An empty mode_06_monitors dict is allowed."""
    data = _valid_payload_dict()
    data["mode_06_monitors"] = {}
    payload = DTCLabPayload.model_validate(data)
    assert payload.mode_06_monitors == {}


# ------------------------------------------------------------------
# Missing required fields
# ------------------------------------------------------------------


def test_missing_required_field_raises():
    """Omitting active_mil raises a Pydantic validation error."""
    data = _valid_payload_dict()
    del data["active_mil"]
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)


def test_missing_freeze_frame_raises():
    """Omitting the freeze_frame field raises a validation error."""
    data = _valid_payload_dict()
    del data["freeze_frame"]
    with pytest.raises(ValidationError):
        DTCLabPayload.model_validate(data)
