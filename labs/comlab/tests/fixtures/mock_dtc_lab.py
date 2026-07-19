"""Mock DTC Lab payload builders.

Match ``comlab.schemas.ingestion.DTCLabPayload``. All DTC strings here pass
the regex ``^[BCPU][0-3][0-9A-F]{3}$`` (DTC_REGEX per DTC_VOCABULARY §2.3).
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Shared minimal freeze-frame dict — valid for "no codes" scenarios
# ---------------------------------------------------------------------------

_MINIMAL_FREEZE_FRAME: dict = {
    "calculated_load_pct": 0.0,
    "engine_rpm": 0,
    "coolant_temp_c": 20.0,
    "short_term_ft1": 0.0,
    "long_term_ft1": 0.0,
    "manifold_pressure_kpa": 100.0,
    "vehicle_speed_kmh": 0,
    "ignition_advance_deg": 10.0,
    "intake_air_temp_c": 20.0,
    "maf_gps": 0.0,
    "throttle_pos_pct": 0.0,
    "fuel_system_status": "OL",
}


def no_codes() -> dict:
    """No active codes, MIL off, all fields at safe defaults."""
    return {
        "active_mil": False,
        "mil_flashing": False,
        "confirmed_dtcs": [],
        "pending_dtcs": [],
        "permanent_dtcs": [],
        "routing_tags": [],
        "mode_06_monitors": {},
        "historical_fault_context": "UNKNOWN",
        "freeze_frame": dict(_MINIMAL_FREEZE_FRAME),
    }


def full_confirmed() -> dict:
    """Full payload with confirmed misfire DTC, routing tags, and freeze-frame."""
    return {
        "active_mil": True,
        "mil_flashing": False,
        "confirmed_dtcs": ["P0302"],
        "pending_dtcs": [],
        "permanent_dtcs": [],
        "routing_tags": ["MISFIRE_HISTORY"],
        "mode_06_monitors": {},
        "historical_fault_context": "HISTORICAL_IDLE_FAULT",
        "freeze_frame": {
            "calculated_load_pct": 35.0,
            "engine_rpm": 780,
            "coolant_temp_c": 88.0,
            "short_term_ft1": -3.1,
            "long_term_ft1": 2.5,
            "manifold_pressure_kpa": 32.0,
            "vehicle_speed_kmh": 0,
            "ignition_advance_deg": 8.0,
            "intake_air_temp_c": 42.0,
            "maf_gps": 4.8,
            "throttle_pos_pct": 12.0,
            "fuel_system_status": "CL",
            "short_term_ft2": None,
            "long_term_ft2": None,
            "o2_voltage_b1s1": 0.45,
            "barometric_pressure_kpa": 101.3,
            "commanded_egr_pct": None,
            "run_time_since_start_sec": 340,
            "fuel_level_pct": 65.0,
        },
    }


def fuel_system_rich(code: str = "P0172") -> dict:
    """Active P0172 (fuel system too rich, bank 1) with MIL on."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = [code]
    payload["routing_tags"] = ["RICH_HISTORY"]
    payload["historical_fault_context"] = "HISTORICAL_LOAD_FAULT"
    return payload


def egr_flow_codes() -> dict:
    """Classic stuck-open EGR pair."""
    payload = no_codes()
    payload["confirmed_dtcs"] = ["P0401"]
    payload["routing_tags"] = ["EGR_HISTORY"]
    return payload


def cylinder_misfire(cylinder: int = 2) -> dict:
    """P030X misfire for the given cylinder, MIL on."""
    code = f"P030{cylinder}"
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = [code]
    payload["routing_tags"] = ["MISFIRE_HISTORY"]
    payload["historical_fault_context"] = "HISTORICAL_IDLE_FAULT"
    return payload


def malformed_dtc() -> dict:
    """Deliberately invalid DTC string — must trip schema validation."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["invalid_p0302"]
    return payload


# ---------------------------------------------------------------------------
# Registry-rule-specific builders — each sets freeze_frame fields that
# satisfy the OBD PID constraints in global_fault_registry.json.
# ---------------------------------------------------------------------------


def _ff(**overrides) -> dict:
    """Build a freeze_frame dict with safe defaults, overridden by kwargs."""
    base = dict(_MINIMAL_FREEZE_FRAME)
    # Map friendly names to freeze_frame keys for registry PID resolution
    key_map = {
        "shrtft1": "short_term_ft1",
        "longft1": "long_term_ft1",
        "map_kpa": "manifold_pressure_kpa",
        "ect_c": "coolant_temp_c",
        "o2_b1s2_v": "o2_voltage_b1s1",
        "calc_load_pct": "calculated_load_pct",
        "baro_kpa": "barometric_pressure_kpa",
    }
    for k, v in overrides.items():
        base[key_map.get(k, k)] = v
    return base


def p0172_rich_hpfp_leak() -> dict:
    """P0172 + MIL on + long_term_ft1=-25 → ERR-E3-F501 (rich_mixture)."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["P0172"]
    payload["routing_tags"] = ["RICH_HISTORY"]
    payload["freeze_frame"] = _ff(longft1=-25.0, map_kpa=35.0)
    return payload


def p0302_misfire_coil_arc() -> dict:
    """P0302 + MIL on + short_term_ft1=20 → ERR-E2-I104 (misfire)."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["P0302"]
    payload["routing_tags"] = ["MISFIRE_HISTORY"]
    payload["freeze_frame"] = _ff(shrtft1=20.0, map_kpa=35.0)
    return payload


def p0401_egr_stuck_open() -> dict:
    """P0401 + no MIL + baro=131.325 + map=90 → ERR-E1-M032 (lean_condition).

    manifold_vacuum_kpa = baro - map = 131.325 - 90 ≈ 41.3, inside [30, 50].
    """
    payload = no_codes()
    payload["confirmed_dtcs"] = ["P0401"]
    payload["routing_tags"] = ["EGR_HISTORY"]
    payload["freeze_frame"] = _ff(map_kpa=90.0, baro_kpa=131.325)
    return payload


def p0420_catalyst_below_threshold() -> dict:
    """P0420 + MIL on + o2_voltage_b1s1=0.7 → ERR-CF-001 (catalyst_failure)."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["P0420"]
    payload["routing_tags"] = ["CATALYST_HISTORY"]
    payload["freeze_frame"] = _ff(o2_b1s2_v=0.7, map_kpa=35.0)
    return payload


def p0171_exhaust_leak_manifold() -> dict:
    """P0171 + no MIL + long_term_ft1=15 → ERR-EL-001 (exhaust_leak)."""
    payload = no_codes()
    payload["confirmed_dtcs"] = ["P0171"]
    payload["routing_tags"] = ["LEAN_HISTORY"]
    payload["freeze_frame"] = _ff(longft1=15.0, map_kpa=35.0)
    return payload


def p0351_ignition_coil_driver() -> dict:
    """P0351 + MIL on + short_term_ft1=20 → ERR-IF-001 (ignition_fault)."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["P0351"]
    payload["routing_tags"] = ["MISFIRE_HISTORY"]
    payload["freeze_frame"] = _ff(shrtft1=20.0, map_kpa=35.0)
    return payload


def p0300_mechanical_wear() -> dict:
    """P0300 + MIL on → ERR-MW-001 (mechanical_wear)."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["P0300"]
    payload["routing_tags"] = ["MISFIRE_HISTORY"]
    payload["freeze_frame"] = _ff(map_kpa=35.0)
    return payload


def p0016_cam_timing_retard() -> dict:
    """P0016 + MIL on + manifold_pressure_kpa=25 → ERR-CT-001 (cam_timing)."""
    payload = no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = ["P0016"]
    payload["routing_tags"] = ["VVT_HISTORY"]
    payload["freeze_frame"] = _ff(map_kpa=25.0)
    return payload

