"""C5 auditor helper — mirrors the widget dict apps/ui/app.py:789-918 builds at click time.

`base_widgets()` returns exactly what app.py passes to build_diagnose_payload() when the
page is first loaded and the user clicks "Run Diagnostic Seam" without typing anything
(all four module boxes ticked, DNA/VIN on, no VIN, Tier-1 "—", every number_input None).
Probes override only the keys a user would change.

sys.path: apps/ui (what root app.py adds) + labs/comlab (gets past F-C4-1 / F-C1-5 so the
verdict path can be exercised; the KeyError/triage crashes happen before that import).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
for p in ("apps/ui", "labs/comlab", "apps/wired"):
    if str(ROOT / p) not in sys.path:
        sys.path.insert(0, str(ROOT / p))

import logging  # noqa: E402

logging.disable(logging.WARNING)

from ui_payload import build_diagnose_payload  # noqa: E402
from wired.composition import diagnose  # noqa: E402

ADV_NUM = [
    "mode06_catalyst_margin_pct", "catalyst_index_ratio", "stft_idle_pct", "ltft_idle_pct",
    "stft_2500_pct", "ltft_2500_pct", "decel_co_pct", "pre_post_cat_hc_delta_ppm",
    "pre_post_cat_co_delta_pct", "koeo_map_baro_delta_kpa", "module_voltage_loaded_v",
    "dlc_signal_ground_drop_v", "mode06_o2_response_margin_pct", "maf_actual_calc_delta_pct_idle",
    "maf_actual_calc_delta_pct_2500", "maf_gps_idle", "maf_gps_2500", "calc_airflow_gps_idle",
    "calc_airflow_gps_2500", "stft_load_pct", "ltft_load_pct", "calc_load_wot_pct",
    "fuel_rail_pressure_load_kpa", "wideband_lambda_wot", "co2_idle_pct",
    "tailpipe_o2_elevation_pct", "downstream_o2_v", "propane_trim_shift_pct", "stored_dtc_count",
    "pending_dtc_count", "permanent_dtc_count", "mode06_min_margin_pct",
    "warmup_cycles_since_clear", "miles_since_clear",
]

# A plausible warm, stoichiometric low-idle sample (lambda ~1.0)
GOOD_GAS = {"gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50}


def base_widgets(**over: Any) -> dict[str, Any]:
    w: dict[str, Any] = {
        "vin": "", "dna_module": True, "gas_module": True, "obd_module": True, "dtc_module": True,
        "use_decoded_dna": False, "vin_confidence": "NONE",
        # basic-mode defaults, app.py:341-351
        "active_number_of_banks": 1, "active_has_maf_sensor": False, "active_has_map_sensor": False,
        "active_upstream_o2_type": "NARROWBAND", "active_downstream_o2_present": False,
        "active_egr_equipped": False, "active_cylinder_count": 4,
        "active_induction_type": "NATURALLY_ASPIRATED",
        "triage_tier_1": "—", "triage_tier_2": "—", "triage_occurs_during": "Always",
        "triage_engine_state": "Running", "triage_free_text_notes": "",
        "symptom_misfire_cylinder": None,
        "override_upstream_o2_type": "Auto (VIN-decoded)", "override_de_cat": False,
        "gas_hc": None, "gas_co": None, "gas_co2": None, "gas_o2": None, "gas_nox": None,
        "gas_lambda_measured": None,
        "gas_hc_high": None, "gas_co_high": None, "gas_co2_high": None, "gas_o2_high": None,
        "gas_nox_high": None, "gas_lambda_2500": None,
        "gas_engine_state": "STABILIZED_IDLE", "gas_block_test_passed": False,
        "obd_engine_rpm": None, "obd_coolant_temp_c": None, "obd_calculated_engine_load_pct": None,
        "obd_shrtft1": None, "obd_longft1": None, "obd_shrtft2": None, "obd_longft2": None,
        "obd_mass_airflow_gps": None, "obd_manifold_vacuum_kpa": None, "obd_upstream_o2_val": None,
        "obd_downstream_o2_v": None, "obd_fuel_sys_status": "",
        "dtc_active_mil": False, "dtc_mil_flashing": False, "dtc_memory_status": "Normal",
        "dtc_confirmed": "", "dtc_pending": "", "dtc_permanent": "", "mode06_monitors": [],
        "ff_calculated_load_pct": None, "ff_engine_rpm": None, "ff_coolant_temp_c": None,
        "ff_short_term_ft1": None, "ff_long_term_ft1": None, "ff_manifold_pressure_kpa": None,
        "ff_vehicle_speed_kmh": None, "ff_ignition_advance_deg": None, "ff_intake_air_temp_c": None,
        "ff_maf_gps": None, "ff_throttle_pos_pct": None, "ff_fuel_system_status": "",
        "ff_add_extended": False, "ff_short_term_ft2": None, "ff_long_term_ft2": None,
        "ff_o2_voltage_b1s1": None, "ff_barometric_pressure_kpa": None, "ff_commanded_egr_pct": None,
        "ff_run_time_since_start_sec": None, "ff_fuel_level_pct": None,
        "bidirectional_fuel_response_ok_bool": "—", "readiness_supported_complete_bool": "—",
    }
    for k in ADV_NUM:
        w[k] = None
    w.update(over)
    return w


def decoded_widgets(vin: str, **over: Any) -> dict[str, Any]:
    """Widget dict when DNA/VIN is on, `vin` decodes and "Use this decoded DNA" stays ticked
    (app.py:312-339)."""
    import vinlab

    dna = vinlab.decode(vin)
    w = base_widgets(
        vin=vin, use_decoded_dna=True, vin_confidence=dna.confidence.value,
        active_number_of_banks=dna.number_of_banks,
        active_has_maf_sensor=dna.air_metering_architecture.has_maf_sensor,
        active_has_map_sensor=dna.air_metering_architecture.has_map_sensor,
        active_upstream_o2_type=dna.emissions.upstream_o2_type.value,
        active_downstream_o2_present=dna.emissions.downstream_o2_present,
        active_egr_equipped=dna.emissions.egr_equipped,
        active_cylinder_count=dna.cylinder_count,
        active_induction_type=dna.induction_type.value,
    )
    w.update(over)
    return w


def run(w: dict[str, Any]):
    """Return (payload, result_or_None, error_string_or_None) — error string is exactly what
    app.py:928 would print after 'Diagnostic calculation failed: '."""
    payload = build_diagnose_payload(w)
    try:
        return payload, diagnose(payload), None
    except Exception as e:  # app.py:927 catches Exception
        return payload, None, f"{type(e).__name__}: {e}"


def verdict_str(res) -> str:
    v = res.diagnostic_verdict
    return (f"{v.fault_code} {v.fault_family} conf={v.confidence_score:.2f} "
            f"abstained={v.abstained} horizon={res.execution_meta.resolved_horizon} "
            f"mode={res.execution_meta.degradation_mode}")
