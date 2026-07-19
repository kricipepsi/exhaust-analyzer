"""Tests for the Streamlit UI payload mapping and E2E integration."""

from typing import Any

from wired.composition import diagnose
from ui_payload import build_diagnose_payload


def test_widget_to_payload_untouched_absent():
    """Verify that untouched widget values are completely absent from the payload."""
    widgets: dict[str, Any] = {
        "vin": "",
        "dna_module": False,
        "gas_module": False,
        "obd_module": False,
        "dtc_module": False,
    }
    payload = build_diagnose_payload(widgets)
    
    assert payload["vin"] == "UNKNOWNVIN0000000"
    assert "triage" not in payload
    assert "overrides" not in payload
    assert "gas" not in payload
    assert "obd" not in payload
    assert "dtc" not in payload


def test_widget_to_payload_roundtrip():
    """Verify that typed widget values correctly map and round-trip into the payload."""
    widgets: dict[str, Any] = {
        "vin": "WBA4W9C5ZLYYYYYYY",
        "dna_module": True,
        "gas_module": True,
        "obd_module": True,
        "dtc_module": True,
        
        # DNA/Triage
        "triage_tier_1": "🔧 Rough Idle / Shudder",
        "triage_tier_2": "Constant shudder / vibration",
        "triage_occurs_during": "Always",
        "triage_engine_state": "Running",
        "triage_free_text_notes": "Slight vibration",
        
        # Gas
        "gas_hc": 120,
        "gas_co": 0.5,
        "gas_co2": 14.5,
        "gas_o2": 0.4,
        "gas_nox": 30,
        "gas_lambda_measured": 1.01,
        
        # OBD basic
        "obd_engine_rpm": 850,
        "obd_coolant_temp_c": 90.0,
        "obd_calculated_engine_load_pct": 25.0,
        "obd_shrtft1": 2.5,
        "obd_longft1": 5.0,
        "active_number_of_banks": 1,
        "active_has_maf_sensor": True,
        "obd_mass_airflow_gps": 3.4,
        "active_has_map_sensor": False,
        
        # DTC
        "dtc_active_mil": True,
        "dtc_confirmed": "P0171",
        "dtc_pending": "P0300",
        "dtc_permanent": "",
        "mode06_monitors": [
            {"monitor_id": "MID_A2_TID_0B", "margin_pct": 25.0}
        ],
        
        # FF PIDs
        "ff_calculated_load_pct": 30.0,
        "ff_engine_rpm": 900,
        "ff_coolant_temp_c": 88.0,
        "ff_short_term_ft1": 1.2,
        "ff_long_term_ft1": 3.4,
        "ff_manifold_pressure_kpa": 45.0,
        "ff_vehicle_speed_kmh": 0,
        "ff_ignition_advance_deg": 12.0,
        "ff_intake_air_temp_c": 35.0,
        "ff_maf_gps": 3.8,
        "ff_throttle_pos_pct": 15.0,
        "ff_fuel_system_status": "CL",
    }
    
    payload = build_diagnose_payload(widgets)
    
    assert payload["vin"] == "WBA4W9C5ZLYYYYYYY"
    assert payload["triage"]["tier_1"] == "rough_idle_shudder"
    assert payload["triage"]["tier_2"] == "constant_vibration_shudder"
    assert payload["triage"]["occurs_during"] == "always"
    assert payload["triage"]["engine_state"] == "running"
    
    assert payload["gas"]["hc"] == 120
    assert payload["gas"]["co"] == 0.5
    assert payload["gas"]["co2"] == 14.5
    assert payload["gas"]["o2"] == 0.4
    assert payload["gas"]["nox"] == 30
    assert payload["gas"]["lambda_measured"] == 1.01
    
    assert payload["obd"]["engine_rpm"] == 850
    assert payload["obd"]["coolant_temp_c"] == 90.0
    assert payload["obd"]["shrtft1"] == 2.5
    assert payload["obd"]["longft1"] == 5.0
    assert payload["obd"]["mass_airflow_gps"] == 3.4
    assert "manifold_vacuum_kpa" not in payload["obd"]
    
    assert payload["dtc"]["active_mil"] is True
    assert payload["dtc"]["raw_dtcs"]["$03"] == ["P0171"]
    assert payload["dtc"]["raw_dtcs"]["$07"] == ["P0300"]
    assert "$0A" not in payload["dtc"]["raw_dtcs"]
    assert payload["dtc"]["raw_mode06"]["MID_A2_TID_0B"] == 25.0
    
    assert payload["dtc"]["raw_freeze_frame"]["calculated_load_pct"] == 30.0
    assert payload["dtc"]["raw_freeze_frame"]["engine_rpm"] == 900
    assert payload["dtc"]["raw_freeze_frame"]["fuel_system_status"] == "CL"


def test_e2e_mw002_fixture():
    """Verify that MW-002 fixture values mapped from UI return fault_code=MW-002."""
    widgets: dict[str, Any] = {
        "vin": "WBA4W9C5ZLYYYYYYY",
        "dna_module": True,
        "gas_module": True,
        "obd_module": False,
        "dtc_module": False,
        
        # Triage
        "triage_tier_1": "🔧 Rough Idle / Shudder",
        "triage_tier_2": "Constant shudder / vibration",
        "triage_occurs_during": "Always",
        "triage_engine_state": "Running",
        
        # Gas
        "gas_hc": 500,
        "gas_co": 0.9,
        "gas_co2": 13.0,
        "gas_o2": 0.2,
        "gas_nox": 50,
        "gas_hc_high": 30,
        "gas_co_high": 0.15,
        "gas_co2_high": 15.2,
        "gas_o2_high": 0.1,
        "gas_nox_high": 50,
        "gas_lambda_measured": 0.95,
        "gas_engine_state": "STABILIZED_IDLE",
    }
    
    raw_inputs = build_diagnose_payload(widgets)
    res = diagnose(raw_inputs)
    
    assert res.diagnostic_verdict.is_fault_detected is True
    assert res.diagnostic_verdict.fault_code == "MW-002"
    assert res.diagnostic_verdict.abstained is True


def test_e2e_abstain_case():
    """Verify that a perfect stoich case results in an abstained verdict."""
    widgets: dict[str, Any] = {
        "vin": "WBA4W9C5ZLYYYYYYY",
        "dna_module": True,
        "gas_module": True,
        "obd_module": False,
        "dtc_module": False,
        
        # Triage
        "triage_tier_1": "💨 Visible Exhaust Smoke",
        "triage_tier_2": "Black smoke",
        "triage_occurs_during": "Always",
        "triage_engine_state": "Running",
        # Gas - perfect stoichiometric readings
        "gas_hc": 12,
        "gas_co": 0.1,
        "gas_co2": 15.2,
        "gas_o2": 0.1,
        "gas_nox": 0,
        "gas_lambda_measured": 1.00,
        "gas_engine_state": "STABILIZED_IDLE",
    }
    
    raw_inputs = build_diagnose_payload(widgets)
    res = diagnose(raw_inputs)
    
    # Perfect stoich with no symptoms / no DTCs / no trims should abstain due to insufficient evidence
    assert res.diagnostic_verdict.abstained is True
    assert res.diagnostic_verdict.abstain_reason in ("floor", "margin")


def test_advanced_fields_mapping():
    """Verify that all 36 advanced workshop signals are correctly mapped to the payload."""
    widgets = {
        "vin": "WBA4W9C5ZLYYYYYYY",
        "dna_module": True,
        "gas_module": True,
        "obd_module": True,
        # Catalyst C2
        "mode06_catalyst_margin_pct": 12.5,
        "catalyst_index_ratio": 0.25,
        "stft_idle_pct": 2.0,
        "ltft_idle_pct": 4.5,
        "stft_2500_pct": 1.5,
        "ltft_2500_pct": 3.0,
        "pre_post_cat_hc_delta_ppm": 90.0,
        "pre_post_cat_co_delta_pct": 0.8,
        "decel_co_pct": 0.05,
        # ECU electrical C3
        "koeo_map_baro_delta_kpa": 1.2,
        "module_voltage_loaded_v": 13.8,
        "dlc_signal_ground_drop_v": 0.08,
        "bidirectional_fuel_response_ok_bool": "True",
        # Sensor dynamics C6
        "mode06_o2_response_margin_pct": 15.0,
        "maf_actual_calc_delta_pct_idle": 5.0,
        "maf_actual_calc_delta_pct_2500": 3.0,
        "maf_gps_idle": 2.8,
        "maf_gps_2500": 12.5,
        "calc_airflow_gps_idle": 2.7,
        "calc_airflow_gps_2500": 12.2,
        # Lean root-cause C5
        "stft_load_pct": -2.0,
        "ltft_load_pct": 8.0,
        "calc_load_wot_pct": 85.0,
        "fuel_rail_pressure_load_kpa": 400.0,
        "wideband_lambda_wot": 0.98,
        # Leak/dilution C4
        "co2_idle_pct": 14.8,
        "tailpipe_o2_elevation_pct": 0.3,
        "downstream_o2_v": 0.65,
        "propane_trim_shift_pct": 1.2,
        # Health confirm C9
        "readiness_supported_complete_bool": "False",
        "stored_dtc_count": 2,
        "pending_dtc_count": 1,
        "permanent_dtc_count": 0,
        "mode06_min_margin_pct": 18.5,
        "warmup_cycles_since_clear": 40,
        "miles_since_clear": 320,
    }

    payload = build_diagnose_payload(widgets)

    # Verify Gas delta fields
    assert payload["gas"]["pre_post_cat_hc_delta_ppm"] == 90.0
    assert payload["gas"]["pre_post_cat_co_delta_pct"] == 0.8
    assert payload["gas"]["decel_co_pct"] == 0.05

    # Verify OBD advanced fields
    obd = payload["obd"]
    assert obd["mode06_catalyst_margin_pct"] == 12.5
    assert obd["catalyst_index_ratio"] == 0.25
    assert obd["stft_idle_pct"] == 2.0
    assert obd["ltft_idle_pct"] == 4.5
    assert obd["stft_2500_pct"] == 1.5
    assert obd["ltft_2500_pct"] == 3.0

    assert obd["koeo_map_baro_delta_kpa"] == 1.2
    assert obd["module_voltage_loaded_v"] == 13.8
    assert obd["dlc_signal_ground_drop_v"] == 0.08
    assert obd["bidirectional_fuel_response_ok_bool"] is True

    assert obd["mode06_o2_response_margin_pct"] == 15.0
    assert obd["maf_actual_calc_delta_pct_idle"] == 5.0
    assert obd["maf_actual_calc_delta_pct_2500"] == 3.0
    assert obd["maf_gps_idle"] == 2.8
    assert obd["maf_gps_2500"] == 12.5
    assert obd["calc_airflow_gps_idle"] == 2.7
    assert obd["calc_airflow_gps_2500"] == 12.2

    assert obd["stft_load_pct"] == -2.0
    assert obd["ltft_load_pct"] == 8.0
    assert obd["calc_load_wot_pct"] == 85.0
    assert obd["fuel_rail_pressure_load_kpa"] == 400.0
    assert obd["wideband_lambda_wot"] == 0.98

    assert obd["co2_idle_pct"] == 14.8
    assert obd["tailpipe_o2_elevation_pct"] == 0.3
    assert obd["downstream_o2_v"] == 0.65
    assert obd["propane_trim_shift_pct"] == 1.2

    assert obd["readiness_supported_complete_bool"] is False
    assert obd["stored_dtc_count"] == 2.0
    assert obd["pending_dtc_count"] == 1.0
    assert obd["permanent_dtc_count"] == 0.0
    assert obd["mode06_min_margin_pct"] == 18.5
    assert obd["warmup_cycles_since_clear"] == 40.0
    assert obd["miles_since_clear"] == 320.0

    # Verify there are 36 fields mapped
    # 3 in gas + 31 in obd + 2 booleans (already in obd) = 3 in gas + 33 in obd = 36 total advanced columns
    advanced_gas_keys = {"pre_post_cat_hc_delta_ppm", "pre_post_cat_co_delta_pct", "decel_co_pct"}
    advanced_obd_keys = {
        "mode06_catalyst_margin_pct", "catalyst_index_ratio", "stft_idle_pct", "ltft_idle_pct", "stft_2500_pct", "ltft_2500_pct",
        "koeo_map_baro_delta_kpa", "module_voltage_loaded_v", "dlc_signal_ground_drop_v", "bidirectional_fuel_response_ok_bool",
        "mode06_o2_response_margin_pct", "maf_actual_calc_delta_pct_idle", "maf_actual_calc_delta_pct_2500",
        "maf_gps_idle", "maf_gps_2500", "calc_airflow_gps_idle", "calc_airflow_gps_2500",
        "stft_load_pct", "ltft_load_pct", "calc_load_wot_pct", "fuel_rail_pressure_load_kpa", "wideband_lambda_wot",
        "co2_idle_pct", "tailpipe_o2_elevation_pct", "downstream_o2_v", "propane_trim_shift_pct",
        "readiness_supported_complete_bool", "stored_dtc_count", "pending_dtc_count", "permanent_dtc_count",
        "mode06_min_margin_pct", "warmup_cycles_since_clear", "miles_since_clear"
    }
    assert len(advanced_gas_keys) == 3
    assert len(advanced_obd_keys) == 33
    
    mapped_gas = [k for k in advanced_gas_keys if k in payload["gas"]]
    mapped_obd = [k for k in advanced_obd_keys if k in payload["obd"]]
    assert len(mapped_gas) + len(mapped_obd) == 36



def test_field_help_coverage():
    """Verify that every widget key read by build_diagnose_payload is present in FIELD_HELP."""
    import ast
    from pathlib import Path
    from ui_payload import FIELD_HELP

    path = Path(__file__).parent.parent / "ui_payload.py"
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    keys = set()
    for node in ast.walk(tree):
        # Match widgets.get('key') or widgets.get('key', default)
        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Name) and
                node.func.value.id == "widgets" and
                node.func.attr == "get"
            ):
                if node.args and isinstance(node.args[0], ast.Constant):
                    keys.add(node.args[0].value)
        # Match widgets['key']
        elif isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name) and node.value.id == "widgets":
                if isinstance(node.slice, ast.Constant):
                    keys.add(node.slice.value)

    # Also explicitly add keys looped dynamically in dicts within ui_payload
    dynamic_keys = {
        "ff_short_term_ft2", "ff_long_term_ft2", "ff_o2_voltage_b1s1",
        "ff_barometric_pressure_kpa", "ff_commanded_egr_pct",
        "ff_run_time_since_start_sec", "ff_fuel_level_pct",
        "ff_calculated_load_pct", "ff_engine_rpm", "ff_coolant_temp_c",
        "ff_short_term_ft1", "ff_long_term_ft1", "ff_manifold_pressure_kpa",
        "ff_vehicle_speed_kmh", "ff_ignition_advance_deg",
        "ff_intake_air_temp_c", "ff_maf_gps", "ff_throttle_pos_pct",
        "dtc_confirmed", "dtc_pending", "dtc_permanent"
    }
    keys.update(dynamic_keys)

    for k in keys:
        assert k in FIELD_HELP, f"Key {k} is queried from widgets but missing from FIELD_HELP"


def test_field_help_numeric_bounds():
    """Verify that every numeric entry's min/max equals the shared range constants."""
    from ui_payload import (
        FIELD_HELP,
        GAS_CO_MIN, GAS_CO_MAX, GAS_CO2_MIN, GAS_CO2_MAX, GAS_HC_MIN, GAS_HC_MAX,
        GAS_O2_MIN, GAS_O2_MAX, GAS_NOX_MIN, GAS_NOX_MAX, GAS_LAMBDA_MIN, GAS_LAMBDA_MAX,
        OBD_RPM_MIN, OBD_RPM_MAX, OBD_ECT_MIN, OBD_ECT_MAX, OBD_LOAD_MIN, OBD_LOAD_MAX,
        OBD_TRIM_MIN, OBD_TRIM_MAX, OBD_MAF_MIN, OBD_MAF_MAX, OBD_MAP_MIN, OBD_MAP_MAX,
        OBD_O2_DN_MIN, OBD_O2_DN_MAX,
        FF_LOAD_MIN, FF_LOAD_MAX, FF_RPM_MIN, FF_RPM_MAX, FF_ECT_MIN, FF_ECT_MAX,
        FF_TRIM_MIN, FF_TRIM_MAX, FF_MAP_MIN, FF_MAP_MAX, FF_SPEED_MIN, FF_SPEED_MAX,
        FF_IGNITION_MIN, FF_IGNITION_MAX, FF_IAT_MIN, FF_IAT_MAX, FF_MAF_MIN, FF_MAF_MAX,
        FF_THROTTLE_MIN, FF_THROTTLE_MAX, FF_O2_V_B1S1_MIN, FF_O2_V_B1S1_MAX,
        FF_RUNTIME_MIN, FF_RUNTIME_MAX, FF_FUEL_LEVEL_MIN, FF_FUEL_LEVEL_MAX,
        ADV_CAT_MARGIN_MIN, ADV_CAT_MARGIN_MAX, ADV_CAT_INDEX_MIN, ADV_CAT_INDEX_MAX,
        ADV_DECEL_CO_MIN, ADV_DECEL_CO_MAX, ADV_DELTA_HC_MIN, ADV_DELTA_HC_MAX,
        ADV_DELTA_CO_MIN, ADV_DELTA_CO_MAX, ADV_MAP_BARO_MIN, ADV_MAP_BARO_MAX,
        ADV_VOLTAGE_MIN, ADV_VOLTAGE_MAX, ADV_GND_DROP_MIN, ADV_GND_DROP_MAX,
        ADV_O2_MARGIN_MIN, ADV_O2_MARGIN_MAX, ADV_MAF_DELTA_MIN, ADV_MAF_DELTA_MAX,
        ADV_MAF_GPS_MIN, ADV_MAF_GPS_MAX, ADV_PRESSURE_MIN, ADV_PRESSURE_MAX,
        ADV_LAMBDA_WOT_MIN, ADV_LAMBDA_WOT_MAX, ADV_CO2_MIN, ADV_CO2_MAX,
        ADV_O2_ELEV_MIN, ADV_O2_ELEV_MAX, ADV_DTC_COUNT_MIN, ADV_DTC_COUNT_MAX,
        ADV_WARMUP_MIN, ADV_WARMUP_MAX, ADV_MILES_MIN, ADV_MILES_MAX
    )

    # Gas low
    assert FIELD_HELP["gas_co"].min_val == GAS_CO_MIN
    assert FIELD_HELP["gas_co"].max_val == GAS_CO_MAX
    assert FIELD_HELP["gas_co2"].min_val == GAS_CO2_MIN
    assert FIELD_HELP["gas_co2"].max_val == GAS_CO2_MAX
    assert FIELD_HELP["gas_hc"].min_val == GAS_HC_MIN
    assert FIELD_HELP["gas_hc"].max_val == GAS_HC_MAX
    assert FIELD_HELP["gas_o2"].min_val == GAS_O2_MIN
    assert FIELD_HELP["gas_o2"].max_val == GAS_O2_MAX
    assert FIELD_HELP["gas_nox"].min_val == GAS_NOX_MIN
    assert FIELD_HELP["gas_nox"].max_val == GAS_NOX_MAX
    assert FIELD_HELP["gas_lambda_measured"].min_val == GAS_LAMBDA_MIN
    assert FIELD_HELP["gas_lambda_measured"].max_val == GAS_LAMBDA_MAX

    # Gas high
    assert FIELD_HELP["gas_co_high"].min_val == GAS_CO_MIN
    assert FIELD_HELP["gas_co_high"].max_val == GAS_CO_MAX
    assert FIELD_HELP["gas_co2_high"].min_val == GAS_CO2_MIN
    assert FIELD_HELP["gas_co2_high"].max_val == GAS_CO2_MAX
    assert FIELD_HELP["gas_hc_high"].min_val == GAS_HC_MIN
    assert FIELD_HELP["gas_hc_high"].max_val == GAS_HC_MAX
    assert FIELD_HELP["gas_o2_high"].min_val == GAS_O2_MIN
    assert FIELD_HELP["gas_o2_high"].max_val == GAS_O2_MAX
    assert FIELD_HELP["gas_nox_high"].min_val == GAS_NOX_MIN
    assert FIELD_HELP["gas_nox_high"].max_val == GAS_NOX_MAX
    assert FIELD_HELP["gas_lambda_2500"].min_val == GAS_LAMBDA_MIN
    assert FIELD_HELP["gas_lambda_2500"].max_val == GAS_LAMBDA_MAX

    # OBD low basic
    assert FIELD_HELP["obd_engine_rpm"].min_val == OBD_RPM_MIN
    assert FIELD_HELP["obd_engine_rpm"].max_val == OBD_RPM_MAX
    assert FIELD_HELP["obd_coolant_temp_c"].min_val == OBD_ECT_MIN
    assert FIELD_HELP["obd_coolant_temp_c"].max_val == OBD_ECT_MAX
    assert FIELD_HELP["obd_calculated_engine_load_pct"].min_val == OBD_LOAD_MIN
    assert FIELD_HELP["obd_calculated_engine_load_pct"].max_val == OBD_LOAD_MAX
    assert FIELD_HELP["obd_shrtft1"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["obd_shrtft1"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["obd_longft1"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["obd_longft1"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["obd_shrtft2"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["obd_shrtft2"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["obd_longft2"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["obd_longft2"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["obd_mass_airflow_gps"].min_val == OBD_MAF_MIN
    assert FIELD_HELP["obd_mass_airflow_gps"].max_val == OBD_MAF_MAX
    assert FIELD_HELP["obd_manifold_vacuum_kpa"].min_val == OBD_MAP_MIN
    assert FIELD_HELP["obd_manifold_vacuum_kpa"].max_val == OBD_MAP_MAX
    assert FIELD_HELP["obd_downstream_o2_v"].min_val == OBD_O2_DN_MIN
    assert FIELD_HELP["obd_downstream_o2_v"].max_val == OBD_O2_DN_MAX

    # FF mandatory
    assert FIELD_HELP["ff_calculated_load_pct"].min_val == FF_LOAD_MIN
    assert FIELD_HELP["ff_calculated_load_pct"].max_val == FF_LOAD_MAX
    assert FIELD_HELP["ff_engine_rpm"].min_val == FF_RPM_MIN
    assert FIELD_HELP["ff_engine_rpm"].max_val == FF_RPM_MAX
    assert FIELD_HELP["ff_coolant_temp_c"].min_val == FF_ECT_MIN
    assert FIELD_HELP["ff_coolant_temp_c"].max_val == FF_ECT_MAX
    assert FIELD_HELP["ff_short_term_ft1"].min_val == FF_TRIM_MIN
    assert FIELD_HELP["ff_short_term_ft1"].max_val == FF_TRIM_MAX
    assert FIELD_HELP["ff_long_term_ft1"].min_val == FF_TRIM_MIN
    assert FIELD_HELP["ff_long_term_ft1"].max_val == FF_TRIM_MAX
    assert FIELD_HELP["ff_manifold_pressure_kpa"].min_val == FF_MAP_MIN
    assert FIELD_HELP["ff_manifold_pressure_kpa"].max_val == FF_MAP_MAX
    assert FIELD_HELP["ff_vehicle_speed_kmh"].min_val == FF_SPEED_MIN
    assert FIELD_HELP["ff_vehicle_speed_kmh"].max_val == FF_SPEED_MAX
    assert FIELD_HELP["ff_ignition_advance_deg"].min_val == FF_IGNITION_MIN
    assert FIELD_HELP["ff_ignition_advance_deg"].max_val == FF_IGNITION_MAX
    assert FIELD_HELP["ff_intake_air_temp_c"].min_val == FF_IAT_MIN
    assert FIELD_HELP["ff_intake_air_temp_c"].max_val == FF_IAT_MAX
    assert FIELD_HELP["ff_maf_gps"].min_val == FF_MAF_MIN
    assert FIELD_HELP["ff_maf_gps"].max_val == FF_MAF_MAX
    assert FIELD_HELP["ff_throttle_pos_pct"].min_val == FF_THROTTLE_MIN
    assert FIELD_HELP["ff_throttle_pos_pct"].max_val == FF_THROTTLE_MAX

    # FF extended
    assert FIELD_HELP["ff_short_term_ft2"].min_val == FF_TRIM_MIN
    assert FIELD_HELP["ff_short_term_ft2"].max_val == FF_TRIM_MAX
    assert FIELD_HELP["ff_long_term_ft2"].min_val == FF_TRIM_MIN
    assert FIELD_HELP["ff_long_term_ft2"].max_val == FF_TRIM_MAX
    assert FIELD_HELP["ff_o2_voltage_b1s1"].min_val == FF_O2_V_B1S1_MIN
    assert FIELD_HELP["ff_o2_voltage_b1s1"].max_val == FF_O2_V_B1S1_MAX
    assert FIELD_HELP["ff_barometric_pressure_kpa"].min_val == FF_MAP_MIN
    assert FIELD_HELP["ff_barometric_pressure_kpa"].max_val == FF_MAP_MAX
    assert FIELD_HELP["ff_commanded_egr_pct"].min_val == FF_THROTTLE_MIN
    assert FIELD_HELP["ff_commanded_egr_pct"].max_val == FF_THROTTLE_MAX
    assert FIELD_HELP["ff_run_time_since_start_sec"].min_val == FF_RUNTIME_MIN
    assert FIELD_HELP["ff_run_time_since_start_sec"].max_val == FF_RUNTIME_MAX
    assert FIELD_HELP["ff_fuel_level_pct"].min_val == FF_FUEL_LEVEL_MIN
    assert FIELD_HELP["ff_fuel_level_pct"].max_val == FF_FUEL_LEVEL_MAX

    # Advanced workshop signals C2..C9
    assert FIELD_HELP["mode06_catalyst_margin_pct"].min_val == ADV_CAT_MARGIN_MIN
    assert FIELD_HELP["mode06_catalyst_margin_pct"].max_val == ADV_CAT_MARGIN_MAX
    assert FIELD_HELP["catalyst_index_ratio"].min_val == ADV_CAT_INDEX_MIN
    assert FIELD_HELP["catalyst_index_ratio"].max_val == ADV_CAT_INDEX_MAX
    assert FIELD_HELP["stft_idle_pct"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["stft_idle_pct"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["ltft_idle_pct"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["ltft_idle_pct"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["stft_2500_pct"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["stft_2500_pct"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["ltft_2500_pct"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["ltft_2500_pct"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["decel_co_pct"].min_val == ADV_DECEL_CO_MIN
    assert FIELD_HELP["decel_co_pct"].max_val == ADV_DECEL_CO_MAX
    assert FIELD_HELP["pre_post_cat_hc_delta_ppm"].min_val == ADV_DELTA_HC_MIN
    assert FIELD_HELP["pre_post_cat_hc_delta_ppm"].max_val == ADV_DELTA_HC_MAX
    assert FIELD_HELP["pre_post_cat_co_delta_pct"].min_val == ADV_DELTA_CO_MIN
    assert FIELD_HELP["pre_post_cat_co_delta_pct"].max_val == ADV_DELTA_CO_MAX
    assert FIELD_HELP["koeo_map_baro_delta_kpa"].min_val == ADV_MAP_BARO_MIN
    assert FIELD_HELP["koeo_map_baro_delta_kpa"].max_val == ADV_MAP_BARO_MAX
    assert FIELD_HELP["module_voltage_loaded_v"].min_val == ADV_VOLTAGE_MIN
    assert FIELD_HELP["module_voltage_loaded_v"].max_val == ADV_VOLTAGE_MAX
    assert FIELD_HELP["dlc_signal_ground_drop_v"].min_val == ADV_GND_DROP_MIN
    assert FIELD_HELP["dlc_signal_ground_drop_v"].max_val == ADV_GND_DROP_MAX
    assert FIELD_HELP["mode06_o2_response_margin_pct"].min_val == ADV_O2_MARGIN_MIN
    assert FIELD_HELP["mode06_o2_response_margin_pct"].max_val == ADV_O2_MARGIN_MAX
    assert FIELD_HELP["maf_actual_calc_delta_pct_idle"].min_val == ADV_MAF_DELTA_MIN
    assert FIELD_HELP["maf_actual_calc_delta_pct_2500"].min_val == ADV_MAF_DELTA_MIN
    assert FIELD_HELP["maf_actual_calc_delta_pct_idle"].max_val == ADV_MAF_DELTA_MAX
    assert FIELD_HELP["maf_actual_calc_delta_pct_2500"].max_val == ADV_MAF_DELTA_MAX
    assert FIELD_HELP["maf_gps_idle"].min_val == ADV_MAF_GPS_MIN
    assert FIELD_HELP["maf_gps_idle"].max_val == ADV_MAF_GPS_MAX
    assert FIELD_HELP["maf_gps_2500"].min_val == ADV_MAF_GPS_MIN
    assert FIELD_HELP["maf_gps_2500"].max_val == ADV_MAF_GPS_MAX
    assert FIELD_HELP["calc_airflow_gps_idle"].min_val == ADV_MAF_GPS_MIN
    assert FIELD_HELP["calc_airflow_gps_idle"].max_val == ADV_MAF_GPS_MAX
    assert FIELD_HELP["calc_airflow_gps_2500"].min_val == ADV_MAF_GPS_MIN
    assert FIELD_HELP["calc_airflow_gps_2500"].max_val == ADV_MAF_GPS_MAX
    assert FIELD_HELP["stft_load_pct"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["stft_load_pct"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["ltft_load_pct"].min_val == OBD_TRIM_MIN
    assert FIELD_HELP["ltft_load_pct"].max_val == OBD_TRIM_MAX
    assert FIELD_HELP["calc_load_wot_pct"].min_val == FF_LOAD_MIN
    assert FIELD_HELP["calc_load_wot_pct"].max_val == FF_LOAD_MAX
    assert FIELD_HELP["fuel_rail_pressure_load_kpa"].min_val == ADV_PRESSURE_MIN
    assert FIELD_HELP["fuel_rail_pressure_load_kpa"].max_val == ADV_PRESSURE_MAX
    assert FIELD_HELP["wideband_lambda_wot"].min_val == ADV_LAMBDA_WOT_MIN
    assert FIELD_HELP["wideband_lambda_wot"].max_val == ADV_LAMBDA_WOT_MAX
    assert FIELD_HELP["co2_idle_pct"].min_val == ADV_CO2_MIN
    assert FIELD_HELP["co2_idle_pct"].max_val == ADV_CO2_MAX
    assert FIELD_HELP["tailpipe_o2_elevation_pct"].min_val == ADV_O2_ELEV_MIN
    assert FIELD_HELP["tailpipe_o2_elevation_pct"].max_val == ADV_O2_ELEV_MAX
    assert FIELD_HELP["downstream_o2_v"].min_val == OBD_O2_DN_MIN
    assert FIELD_HELP["downstream_o2_v"].max_val == OBD_O2_DN_MAX
    assert FIELD_HELP["propane_trim_shift_pct"].min_val == ADV_MAF_DELTA_MIN
    assert FIELD_HELP["propane_trim_shift_pct"].max_val == ADV_MAF_DELTA_MAX
    assert FIELD_HELP["stored_dtc_count"].min_val == ADV_DTC_COUNT_MIN
    assert FIELD_HELP["stored_dtc_count"].max_val == ADV_DTC_COUNT_MAX
    assert FIELD_HELP["pending_dtc_count"].min_val == ADV_DTC_COUNT_MIN
    assert FIELD_HELP["pending_dtc_count"].max_val == ADV_DTC_COUNT_MAX
    assert FIELD_HELP["permanent_dtc_count"].min_val == ADV_DTC_COUNT_MIN
    assert FIELD_HELP["permanent_dtc_count"].max_val == ADV_DTC_COUNT_MAX
    assert FIELD_HELP["mode06_min_margin_pct"].min_val == -100.0
    assert FIELD_HELP["mode06_min_margin_pct"].max_val == 100.0
    assert FIELD_HELP["warmup_cycles_since_clear"].min_val == ADV_WARMUP_MIN
    assert FIELD_HELP["warmup_cycles_since_clear"].max_val == ADV_WARMUP_MAX
    assert FIELD_HELP["miles_since_clear"].min_val == ADV_MILES_MIN
    assert FIELD_HELP["miles_since_clear"].max_val == ADV_MILES_MAX


def test_field_help_tooltip_format():
    """Verify that every help string generated by FIELD_HELP is non-empty and formatted correctly."""
    from ui_payload import FIELD_HELP

    for key, fh in FIELD_HELP.items():
        tooltip = fh.get_tooltip()
        assert len(tooltip) > 0, f"Tooltip for {key} is empty"
        assert "Range:" in tooltip or "Options:" in tooltip, f"Tooltip for {key} lacks Range or Options: {tooltip}"

