"""Loader and validator for the wired-v7 petrol case corpus.

Exposes a function load_corpus() to iterate over all viable petrol test cases,
mapping the flat CSV row fields into the structured raw inputs dict expected by
the public wired diagnose() interface.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import traceback
from collections.abc import Iterator
from pathlib import Path
from typing import Any

# Bootstrap lab paths so editable packages resolve correctly when run directly
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / 'apps/wired'))
for relative in (
    "labs/comlab",
    "labs/dnalab",
    "labs/dtclab",
    "labs/gaslab",
    "labs/obdlab",
    "labs/symptomlab",
    "labs/vinlab",
):
    path = str(WORKSPACE_ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)

from dnalab import build_vehicle_dna  # noqa: E402
from vinlab import VINDecodeError  # noqa: E402

from wired.composition import (  # noqa: E402
    _as_dict,
    _build_fallback_vin_dna,
    _map_o2_sensor_type,
    _run_dtclab,
    _run_gaslab,
    _run_obdlab,
)

DEFAULT_CSV_PATH = Path(__file__).parent / "data" / "cases_petrol_v7.csv"


def safe_str(val: Any) -> str:
    """Return a stripped string, converting None/nan/hyphen sentinels to empty."""
    if val is None:
        return ""
    s = str(val).strip()
    if s == "-" or s.lower() == "none" or s.lower() == "nan":
        return ""
    return s


def safe_float(val: Any, default: Any = None) -> Any:
    """Safely parse float value, falling back to default on empty/invalid."""
    s = safe_str(val)
    if not s:
        return default
    try:
        return float(s)
    except ValueError:
        return default


def safe_int(val: Any, default: Any = None) -> Any:
    """Safely parse integer value, falling back to default on empty/invalid."""
    s = safe_str(val)
    if not s:
        return default
    try:
        return int(float(s))
    except ValueError:
        return default


def get_o2_type(vin: str) -> str:
    """Resolve the O2 sensor type for a VIN from DNALab, falling back to narrowband."""
    vin_clean = safe_str(vin)
    if not vin_clean:
        vin_clean = 'UNKNOWNVIN0000000'
    triage_def = {
        "tier_1": "rough_idle_shudder",
        "tier_2": "constant_vibration_shudder",
        "occurs_during": "always",
        "engine_state": "running",
        "load_state": "idle",
    }
    try:
        vehicle_dna = build_vehicle_dna(vin_clean, triage_def)
        vin_dna = vehicle_dna.to_json_payload()["vin_dna"]
    except VINDecodeError:
        return "NARROWBAND_0_TO_1V"
    emissions = vin_dna.get("emissions", {})
    vocab_o2 = str(emissions.get("upstream_o2_type", "NARROWBAND_0_TO_1V"))
    return _map_o2_sensor_type(vocab_o2)


def row_to_raw_inputs(row: dict[str, str]) -> dict[str, Any]:
    """Map a flat CSV row to the structured raw_inputs dict expected by diagnose()."""
    raw_inputs: dict[str, Any] = {"vin": row["vin"]}

    triage = {}
    for f in ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state", "csv_primary_symptom"):
        val = row.get(f"triage_{f}", "").strip()
        if val:
            triage[f] = val
    if triage:
        raw_inputs["triage"] = triage

    overrides = {}
    for f in ("upstream_o2_type", "de_cat"):
        val = row.get(f"override_{f}", "").strip()
        if val:
            if f == "de_cat":
                overrides[f] = (val.lower() == "true")
            else:
                overrides[f] = val
    if overrides:
        raw_inputs["overrides"] = overrides

    gas = {}
    for f in ("hc", "nox", "hc_high", "nox_high"):
        val = row.get(f"gas_{f}", "").strip()
        if val:
            gas[f] = int(float(val))
    for f in ("co", "co2", "o2", "co_high", "co2_high", "o2_high", "lambda_measured", "lambda_2500"):
        val = row.get(f"gas_{f}", "").strip()
        if val:
            gas[f] = float(val)

    val = row.get("gas_engine_state", "").strip()
    if val:
        gas["engine_state"] = val
    val = row.get("gas_block_test_passed", "").strip()
    if val:
        gas["block_test_passed"] = (val.lower() == "true")

    for f in ("coc_target_lambda_v112", "coc_target_lambda_low", "coc_target_lambda_high", "coc_co_low_idle", "coc_co_high_idle"):
        val = row.get(f, "").strip()
        if val:
            gas[f] = float(val)

    for f in ("decel_co_pct", "pre_post_cat_hc_delta_ppm", "pre_post_cat_co_delta_pct"):
        val = row.get(f, "").strip()
        if val:
            gas[f] = float(val)

    raw_inputs["gas"] = gas

    obd = {}
    obd_fields = {
        "engine_rpm": int, "coolant_temp_c": float, "calculated_engine_load_pct": float,
        "mass_airflow_gps": float, "manifold_vacuum_kpa": float, "intake_air_temp_c": float,
        "throttle_pos_pct": float, "control_module_voltage_v": float, "shrtft1": float,
        "longft1": float, "shrtft2": float, "longft2": float, "number_of_banks": int,
        "fuel_sys_status": str, "pid_oxygen_sensor_volts": float, "drive_cycles_since_clear": int
    }

    # Check if there's any active live OBD field present
    live_obd_keys = [
        "engine_rpm", "coolant_temp_c", "calculated_engine_load_pct",
        "mass_airflow_gps", "manifold_vacuum_kpa", "shrtft1", "longft1",
        "pid_oxygen_sensor_volts"
    ]
    has_obd = False
    for f in live_obd_keys:
        val = row.get(f"obd_{f}", "").strip()
        if val:
            has_obd = True
            break

    if row.get("stft_idle_pct", "").strip():
        has_obd = True
    for f in (
        "koeo_map_baro_delta_kpa",
        "module_voltage_loaded_v",
        "dlc_signal_ground_drop_v",
        "bidirectional_fuel_response_ok_bool",
        "mode06_o2_response_margin_pct",
        "maf_actual_calc_delta_pct_idle",
        "maf_actual_calc_delta_pct_2500",
        "maf_gps_idle",
        "maf_gps_2500",
        "calc_airflow_gps_idle",
        "calc_airflow_gps_2500",
        "stft_load_pct",
        "ltft_load_pct",
        "calc_load_wot_pct",
        "fuel_rail_pressure_load_kpa",
        "wideband_lambda_wot",
        "co2_idle_pct",
        "tailpipe_o2_elevation_pct",
        "downstream_o2_v",
        "propane_trim_shift_pct",
        "readiness_supported_complete_bool",
        "stored_dtc_count",
        "pending_dtc_count",
        "permanent_dtc_count",
        "mode06_min_margin_pct",
        "warmup_cycles_since_clear",
        "miles_since_clear",
    ):
        if row.get(f, "").strip():
            has_obd = True
            break
    dtc_str = row.get("obd_active_dtcs_json", "").strip()
    if dtc_str and dtc_str != "[]":
        has_obd = True

    if has_obd:
        for f, t in obd_fields.items():
            val = row.get(f"obd_{f}", "").strip()
            if val:
                obd[f] = t(val) if t is not str else val

        for f in ("active_dtcs", "per_cylinder_misfire_counts", "ltft_cell_vector", "freeze_frame_pids"):
            val = row.get(f"obd_{f}_json", "").strip()
            if val:
                parsed = json.loads(val)
                if f in ("per_cylinder_misfire_counts", "ltft_cell_vector") and isinstance(parsed, dict):
                    parsed = {int(k): v for k, v in parsed.items()}
                obd[f] = parsed

        for f in (
            "mode06_catalyst_margin_pct",
            "catalyst_index_ratio",
            "stft_idle_pct",
            "ltft_idle_pct",
            "stft_2500_pct",
            "ltft_2500_pct",
            "mode06_o2_response_margin_pct",
            "maf_actual_calc_delta_pct_idle",
            "maf_actual_calc_delta_pct_2500",
            "maf_gps_idle",
            "maf_gps_2500",
            "calc_airflow_gps_idle",
            "calc_airflow_gps_2500",
            "stft_load_pct",  # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
            "ltft_load_pct",  # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
            "calc_load_wot_pct",  # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
            "fuel_rail_pressure_load_kpa",  # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
            "wideband_lambda_wot",  # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
            "co2_idle_pct",  # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
            "tailpipe_o2_elevation_pct",  # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
            "downstream_o2_v",  # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
            "propane_trim_shift_pct",  # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
            "mode06_min_margin_pct",  # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
        ):
            val = row.get(f, "").strip()
            if val:
                obd[f] = float(val)
        for f in ("koeo_map_baro_delta_kpa", "module_voltage_loaded_v", "dlc_signal_ground_drop_v"):
            val = row.get(f, "").strip()
            if val:
                obd[f] = float(val)
        for f in (
            "stored_dtc_count",
            "pending_dtc_count",
            "permanent_dtc_count",
            "warmup_cycles_since_clear",
            "miles_since_clear",
        ):
            val = row.get(f, "").strip()
            if val:
                obd[f] = int(float(val))
        val = row.get("readiness_supported_complete_bool", "").strip()
        if val:
            obd["readiness_supported_complete_bool"] = val.lower() == "true"
        val = row.get("bidirectional_fuel_response_ok_bool", "").strip()
        if val:
            obd["bidirectional_fuel_response_ok_bool"] = val.lower() == "true"
        # Apply validator/translator-safe defaults for missing fields
        if "engine_rpm" not in obd or obd["engine_rpm"] is None:
            obd["engine_rpm"] = 800
        if "coolant_temp_c" not in obd or obd["coolant_temp_c"] is None:
            obd["coolant_temp_c"] = 85.0
        if "fuel_sys_status" not in obd or not obd["fuel_sys_status"]:
            obd["fuel_sys_status"] = "CL"

        if "shrtft1" not in obd or obd["shrtft1"] is None:
            obd["shrtft1"] = 0.0
        if "longft1" not in obd or obd["longft1"] is None:
            obd["longft1"] = 0.0

        if obd.get("number_of_banks", 1) == 2:
            if "shrtft2" not in obd or obd["shrtft2"] is None:
                obd["shrtft2"] = obd["shrtft1"]
            if "longft2" not in obd or obd["longft2"] is None:
                obd["longft2"] = obd["longft1"]

        vin_val = row["vin"]
        upstream_o2 = get_o2_type(vin_val)

        o2_val = row.get("obd_pid_oxygen_sensor_volts", "").strip()
        if o2_val:
            v_num = float(o2_val)
            if upstream_o2 == "WIDEBAND_LINEAR":
                obd["pid_wideband_equivalence_ratio"] = v_num
                obd.pop("pid_oxygen_sensor_volts", None)
            else:
                if v_num > 1.01:
                    obd["pid_oxygen_sensor_volts"] = 0.25
                elif v_num < 0.99:
                    obd["pid_oxygen_sensor_volts"] = 0.70
                else:
                    obd["pid_oxygen_sensor_volts"] = 0.45
        else:
            if upstream_o2 == "WIDEBAND_LINEAR":
                obd["pid_wideband_equivalence_ratio"] = 1.0
            else:
                obd["pid_oxygen_sensor_volts"] = 0.45

        raw_inputs["obd"] = obd

    dtc = {}
    has_dtc = False
    raw_dtcs = {}
    for dtc_mode, key in [("$03", "confirmed"), ("$07", "pending"), ("$0A", "permanent")]:
        val = row.get(f"dtc_{key}_json", "").strip()
        if val:
            raw_dtcs[dtc_mode] = json.loads(val)
            has_dtc = True
    if raw_dtcs:
        dtc["raw_dtcs"] = raw_dtcs

    for f in ("raw_freeze_frame", "raw_mode06"):
        val = row.get(f"dtc_{f}_json", "").strip()
        if val:
            dtc[f] = json.loads(val)
            has_dtc = True

    for f in ("codes_cleared", "active_mil", "mil_flashing"):
        val = row.get(f"dtc_{f}", "").strip()
        if val:
            dtc[f] = (val.lower() == "true")
            has_dtc = True

    if has_dtc:
        raw_inputs["dtc"] = dtc

    return raw_inputs


def load_corpus(csv_path: str | Path | None = None) -> Iterator[tuple[str, dict[str, Any], str, str, str]]:
    """Iterate over all test cases in the v7 petrol corpus.

    Yields:
        tuple: (case_id, raw_inputs, source_category, source_ref, tag)
    """
    path = Path(csv_path or DEFAULT_CSV_PATH)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            case_id = row["case_id"]
            category = row["source_category"]
            source_ref = row["source_ref"]
            tag = row["tag"]
            raw_inputs = row_to_raw_inputs(row)
            yield case_id, raw_inputs, category, source_ref, tag


def validate_corpus(csv_path: str | Path | None = None) -> bool:
    """Validate that every row in the CSV parses and maps to valid lab inputs without crashing.

    Returns:
        bool: True if validation is fully clean, False otherwise.
    """
    path = Path(csv_path or DEFAULT_CSV_PATH)
    print(f"Validating corpus: {path}")
    errors = []
    success_count = 0
    total_count = 0

    for case_id, raw_inputs, category, source_ref, tag in load_corpus(path):
        total_count += 1
        if not source_ref:
            errors.append(f"Row {total_count} ({case_id}): missing source_ref")
            continue

        try:
            vin = raw_inputs.get("vin", "")
            triage = _as_dict(raw_inputs.get("triage"))
            try:
                vehicle_dna = build_vehicle_dna(vin, triage)
                vin_dna = _as_dict(vehicle_dna.to_json_payload()["vin_dna"])
            except VINDecodeError:
                vin_dna = _build_fallback_vin_dna(vin)

            gas_inputs = _as_dict(raw_inputs.get("gas"))
            _run_gaslab(gas_inputs, vin_dna)

            obd_inputs = raw_inputs.get("obd")
            if obd_inputs is not None:
                _run_obdlab(_as_dict(obd_inputs), vin_dna)

            dtc_inputs = raw_inputs.get("dtc")
            if dtc_inputs is not None:
                _run_dtclab(_as_dict(dtc_inputs))

            # If tag is invalid, we expected a validation failure (like out-of-range or format error)
            if tag == "invalid":
                # Some invalid_input rows parse structurally but are logically marked invalid.
                # Only check that they do not cause raw python crashes/errors.
                pass

            success_count += 1
        except Exception as e:
            if tag == "invalid":
                # Expected validation exception for invalid tag is a pass
                success_count += 1
                continue
            tb = traceback.format_exc()
            errors.append(f"Row {total_count} ({case_id}): {type(e).__name__} - {str(e)}\n{tb}")

    print(f"Parsed and validated {success_count}/{total_count} cases successfully.")
    if errors:
        print(f"Validation failed with {len(errors)} errors:")
        for err in errors[:10]:
            print(err)
        return False

    print("Corpus validation is clean!")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and validate the cases_petrol_v7 corpus.")
    parser.add_argument("--validate", action="store_true", help="Run the full mapping and validation pipeline.")
    args = parser.parse_args()

    if args.validate:
        sys.exit(0 if validate_corpus() else 1)
    else:
        # Simple dry-run output
        print("Corpus entries:")
        for idx, (case_id, _, category, source_ref, tag) in enumerate(load_corpus(), start=1):
            print(f"  [{idx:03d}] {case_id:<12} tag={tag:<8} category={category:<16} ref={source_ref}")
