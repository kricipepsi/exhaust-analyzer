"""UI payload builder — T-SHIP-UI-2.

Maps flat Streamlit widget values to the structured raw_inputs dict
expected by wired.diagnose().
"""

from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Shared range constants for numeric inputs
# ---------------------------------------------------------------------------
GAS_CO_MIN = 0.0
GAS_CO_MAX = 15.0
GAS_CO2_MIN = 0.0
GAS_CO2_MAX = 22.0
GAS_HC_MIN = 0
GAS_HC_MAX = 20000
GAS_O2_MIN = 0.0
GAS_O2_MAX = 22.0
GAS_NOX_MIN = 0
GAS_NOX_MAX = 5000
GAS_LAMBDA_MIN = 0.500
GAS_LAMBDA_MAX = 2.000

OBD_RPM_MIN = 0
OBD_RPM_MAX = 8000
OBD_ECT_MIN = -40.0
OBD_ECT_MAX = 140.0
OBD_LOAD_MIN = 0.0
OBD_LOAD_MAX = 100.0
OBD_TRIM_MIN = -127.0
OBD_TRIM_MAX = 127.0
OBD_MAF_MIN = 0.0
OBD_MAF_MAX = 655.35
OBD_MAP_MIN = 0.0
OBD_MAP_MAX = 255.0
OBD_O2_DN_MIN = 0.0
OBD_O2_DN_MAX = 1.5

FF_LOAD_MIN = 0.0
FF_LOAD_MAX = 100.0
FF_RPM_MIN = 0
FF_RPM_MAX = 16383
FF_ECT_MIN = -40.0
FF_ECT_MAX = 215.0
FF_TRIM_MIN = -100.0
FF_TRIM_MAX = 99.22
FF_MAP_MIN = 0
FF_MAP_MAX = 255
FF_SPEED_MIN = 0
FF_SPEED_MAX = 255
FF_IGNITION_MIN = -64.0
FF_IGNITION_MAX = 63.5
FF_IAT_MIN = -40.0
FF_IAT_MAX = 215.0
FF_MAF_MIN = 0.0
FF_MAF_MAX = 655.35
FF_THROTTLE_MIN = 0.0
FF_THROTTLE_MAX = 100.0
FF_O2_V_B1S1_MIN = 0.000
FF_O2_V_B1S1_MAX = 1.275
FF_RUNTIME_MIN = 0
FF_RUNTIME_MAX = 65535
FF_FUEL_LEVEL_MIN = 0.0
FF_FUEL_LEVEL_MAX = 100.0

UPSTREAM_O2_NARROWBAND_MIN = 0.0
UPSTREAM_O2_NARROWBAND_MAX = 1.0
UPSTREAM_O2_WIDEBAND_LAMBDA_MIN = 0.7
UPSTREAM_O2_WIDEBAND_LAMBDA_MAX = 1.3
UPSTREAM_O2_WIDEBAND_AFR_MIN = 10.0
UPSTREAM_O2_WIDEBAND_AFR_MAX = 20.0

ADV_CAT_MARGIN_MIN = -1000.0
ADV_CAT_MARGIN_MAX = 100.0
ADV_CAT_INDEX_MIN = 0.0
ADV_CAT_INDEX_MAX = 2.0
ADV_DECEL_CO_MIN = 0.0
ADV_DECEL_CO_MAX = 25.0
ADV_DELTA_HC_MIN = 0
ADV_DELTA_HC_MAX = 20000
ADV_DELTA_CO_MIN = 0.0
ADV_DELTA_CO_MAX = 15.0
ADV_MAP_BARO_MIN = 0.0
ADV_MAP_BARO_MAX = 50.0
ADV_VOLTAGE_MIN = 0.0
ADV_VOLTAGE_MAX = 18.0
ADV_GND_DROP_MIN = 0.0
ADV_GND_DROP_MAX = 5.0
ADV_O2_MARGIN_MIN = 0.0
ADV_O2_MARGIN_MAX = 100.0
ADV_MAF_DELTA_MIN = -100.0
ADV_MAF_DELTA_MAX = 100.0
ADV_MAF_GPS_MIN = 0.0
ADV_MAF_GPS_MAX = 500.0
ADV_PRESSURE_MIN = 0.0
ADV_PRESSURE_MAX = 250000.0
ADV_LAMBDA_WOT_MIN = 0.0
ADV_LAMBDA_WOT_MAX = 3.0
ADV_CO2_MIN = 0.0
ADV_CO2_MAX = 22.0
ADV_O2_ELEV_MIN = 0.0
ADV_O2_ELEV_MAX = 22.0
ADV_DTC_COUNT_MIN = 0
ADV_DTC_COUNT_MAX = 100
ADV_WARMUP_MIN = 0
ADV_WARMUP_MAX = 255
ADV_MILES_MIN = 0
ADV_MILES_MAX = 65535

@dataclass
class FieldHelp:
    explanation: str
    min_val: float | int | None = None
    max_val: float | int | None = None
    unit: str = ""
    options: list[str] | None = None

    def get_tooltip(self) -> str:
        if self.options is not None:
            opts_str = ", ".join(str(o) for o in self.options)
            return f"{self.explanation}\nOptions: {opts_str}"
        else:
            range_str = f"{self.min_val}–{self.max_val}"
            if self.unit:
                range_str += f" {self.unit}"
            return f"{self.explanation}\nRange: {range_str}"

FIELD_HELP: dict[str, FieldHelp] = {
    # Sidebar control fields
    "vin": FieldHelp(
        explanation="Technician-entered 17-character VIN used to decode vehicle engine, equipment, and calibration priors.",
        min_val=17,
        max_val=17,
        unit="characters"
    ),
    "gas_module": FieldHelp(
        explanation="Enables tailpipe exhaust gas analyzer measurement inputs.",
        options=["Checked", "Unchecked"]
    ),
    "obd_module": FieldHelp(
        explanation="Enables live on-board diagnostic parameter inputs.",
        options=["Checked", "Unchecked"]
    ),
    "dtc_module": FieldHelp(
        explanation="Enables diagnostic trouble code and freeze frame inputs.",
        options=["Checked", "Unchecked"]
    ),
    "dna_module": FieldHelp(
        explanation="Enables vehicle identification number decoding for hardware layout gating.",
        options=["Checked", "Unchecked"]
    ),
    "use_decoded_dna": FieldHelp(
        explanation="Locks the decoded vehicle specification for active field gating.",
        options=["Checked", "Unchecked"]
    ),
    "override_upstream_o2_type": FieldHelp(
        explanation="Overrides the decoded upstream oxygen sensor type for aftermarket setups.",
        options=["Auto (VIN-decoded)", "Narrowband 0-1V (OEM)", "Wideband NB-Sim (Aftermarket)"]
    ),
    "override_de_cat": FieldHelp(
        explanation="Flags the vehicle as having its catalytic converter physically removed.",
        options=["Checked", "Unchecked"]
    ),
    "fuel_blend": FieldHelp(
        explanation="Selects the fuel ethanol blend ratio to adjust Stoichiometric chemistry calculations.",
        options=["E0", "E5", "E10"]
    ),
    "mileage": FieldHelp(
        explanation="Categorizes odometer age to adjust fault priors and wear weights.",
        options=["Unknown", "Low", "Mid", "High"]
    ),
    "dtc_memory_status": FieldHelp(
        explanation="Indicates if DTC memory was cleared recently, gating monitor readiness evaluation.",
        options=["Normal", "Recently cleared (<50 mi)"]
    ),
    "triage_tier_1": FieldHelp(
        explanation="The primary customer concern or diagnostic starting point.",
        options=["🚫 Vehicle Won't Start", "🔧 Rough Idle / Shudder", "⬇️ Lack of Power / Hesitation", "⛽ Poor Economy / Fuel Odour", "🛑 Engine Dies / Stalls", "💨 Visible Exhaust Smoke", "🛢️ Oil Consumption"]
    ),
    "triage_tier_2": FieldHelp(
        explanation="The sub-filter or specific category of the primary concern.",
        options=["Specific category of concern depending on Tier 1"]
    ),
    "triage_occurs_during": FieldHelp(
        explanation="Environmental conditions under which the symptom occurs.",
        options=["Always", "Cold only", "Hot only", "Intermittent"]
    ),
    "triage_engine_state": FieldHelp(
        explanation="The engine operating state when the symptom is observed.",
        options=["Running", "Cranking", "Won't start"]
    ),
    "symptom_misfire_cylinder": FieldHelp(
        explanation="The specific engine cylinder identified as misfiring.",
        min_val=1,
        max_val=4, # Baseline limit, dynamic cap applies in UI
        unit="cylinder"
    ),
    # Low Idle Gas
    "gas_co": FieldHelp(
        explanation="Tailpipe carbon monoxide concentration used for combustion efficiency analysis.",
        min_val=GAS_CO_MIN,
        max_val=GAS_CO_MAX,
        unit="%"
    ),
    "gas_co2": FieldHelp(
        explanation="Tailpipe carbon dioxide concentration used to verify probe depth and combustion efficiency.",
        min_val=GAS_CO2_MIN,
        max_val=GAS_CO2_MAX,
        unit="%"
    ),
    "gas_hc": FieldHelp(
        explanation="Tailpipe unburned hydrocarbon concentration indicating incomplete combustion or misfires.",
        min_val=GAS_HC_MIN,
        max_val=GAS_HC_MAX,
        unit="ppm"
    ),
    "gas_o2": FieldHelp(
        explanation="Tailpipe oxygen concentration indicating lean mixtures, dilution, or exhaust leaks.",
        min_val=GAS_O2_MIN,
        max_val=GAS_O2_MAX,
        unit="%"
    ),
    "gas_nox": FieldHelp(
        explanation="Tailpipe nitrogen oxides concentration indicating high combustion temperatures or catalyst failure.",
        min_val=GAS_NOX_MIN,
        max_val=GAS_NOX_MAX,
        unit="ppm"
    ),
    "gas_lambda_measured": FieldHelp(
        explanation="Measured lambda from gas analyzer, used as a feedback source when OBD is unavailable.",
        min_val=GAS_LAMBDA_MIN,
        max_val=GAS_LAMBDA_MAX,
        unit=""
    ),
    # High Idle Gas
    "gas_co_high": FieldHelp(
        explanation="High-idle tailpipe carbon monoxide concentration used to verify catalyst function under load.",
        min_val=GAS_CO_MIN,
        max_val=GAS_CO_MAX,
        unit="%"
    ),
    "gas_co2_high": FieldHelp(
        explanation="High-idle tailpipe carbon dioxide concentration used to verify catalyst function under load.",
        min_val=GAS_CO2_MIN,
        max_val=GAS_CO2_MAX,
        unit="%"
    ),
    "gas_hc_high": FieldHelp(
        explanation="High-idle tailpipe unburned hydrocarbon concentration indicating incomplete combustion under load.",
        min_val=GAS_HC_MIN,
        max_val=GAS_HC_MAX,
        unit="ppm"
    ),
    "gas_o2_high": FieldHelp(
        explanation="High-idle tailpipe oxygen concentration indicating combustion status or exhaust leaks under load.",
        min_val=GAS_O2_MIN,
        max_val=GAS_O2_MAX,
        unit="%"
    ),
    "gas_nox_high": FieldHelp(
        explanation="High-idle tailpipe nitrogen oxides concentration indicating catalyst function under load.",
        min_val=GAS_NOX_MIN,
        max_val=GAS_NOX_MAX,
        unit="ppm"
    ),
    "gas_lambda_2500": FieldHelp(
        explanation="High-idle measured lambda from gas analyzer, used to verify fuel control under load.",
        min_val=GAS_LAMBDA_MIN,
        max_val=GAS_LAMBDA_MAX,
        unit=""
    ),
    "gas_engine_state": FieldHelp(
        explanation="Exhaust gas analyzer target engine speed state.",
        options=["STABILIZED_IDLE", "HIGH_IDLE"]
    ),
    "gas_block_test_passed": FieldHelp(
        explanation="Indicates if tailpipe exhaust backpressure test was completed successfully.",
        options=["Checked", "Unchecked"]
    ),
    # OBD basic fields
    "obd_engine_rpm": FieldHelp(
        explanation="Engine speed reported by the ECU, used to identify current diagnostic operating regime.",
        min_val=OBD_RPM_MIN,
        max_val=OBD_RPM_MAX,
        unit="RPM"
    ),
    "obd_coolant_temp_c": FieldHelp(
        explanation="Engine coolant temperature used to verify the engine is fully warmed up.",
        min_val=OBD_ECT_MIN,
        max_val=OBD_ECT_MAX,
        unit="°C"
    ),
    "obd_calculated_engine_load_pct": FieldHelp(
        explanation="Calculated engine load indicating current engine torque demand.",
        min_val=OBD_LOAD_MIN,
        max_val=OBD_LOAD_MAX,
        unit="%"
    ),
    "obd_shrtft1": FieldHelp(
        explanation="Short-term fuel trim for cylinder bank 1 representing immediate fuel feedback correction.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "obd_longft1": FieldHelp(
        explanation="Long-term fuel trim for cylinder bank 1 representing learned fuel feedback correction.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "obd_shrtft2": FieldHelp(
        explanation="Short-term fuel trim for cylinder bank 2 representing immediate fuel feedback correction.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "obd_longft2": FieldHelp(
        explanation="Long-term fuel trim for cylinder bank 2 representing learned fuel feedback correction.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "obd_mass_airflow_gps": FieldHelp(
        explanation="Mass airflow sensor reading indicating total air mass entering the engine.",
        min_val=OBD_MAF_MIN,
        max_val=OBD_MAF_MAX,
        unit="g/s"
    ),
    "obd_manifold_vacuum_kpa": FieldHelp(
        explanation="Manifold absolute pressure sensor reading indicating intake manifold pressure.",
        min_val=OBD_MAP_MIN,
        max_val=OBD_MAP_MAX,
        unit="kPa"
    ),
    "obd_upstream_o2_val": FieldHelp(
        explanation="Upstream oxygen sensor reading. Units and ranges vary depending on the decoded sensor type.",
        min_val=0.0,
        max_val=20.0,
        unit=""
    ),
    "obd_downstream_o2_v": FieldHelp(
        explanation="Downstream sensor S12 voltage indicating post-catalyst oxygen levels and sensor bias.",
        min_val=OBD_O2_DN_MIN,
        max_val=OBD_O2_DN_MAX,
        unit="V"
    ),
    "obd_fuel_sys_status": FieldHelp(
        explanation="Fuel system loop status reported by the PCM.",
        options=["CL", "OL", "OL_DRIVE", "OL_FAULT"]
    ),
    # DTC basic fields
    "dtc_active_mil": FieldHelp(
        explanation="ECU command status for the Malfunction Indicator Lamp.",
        options=["Checked", "Unchecked"]
    ),
    "dtc_mil_flashing": FieldHelp(
        explanation="MIL flashing indicating active, catalyst-damaging misfires.",
        options=["Checked", "Unchecked"]
    ),
    "dtc_confirmed": FieldHelp(
        explanation="Confirmed Diagnostic Trouble Codes stored in scanner Mode $03.",
        options=["List of 5-character alphanumeric fault codes"]
    ),
    "dtc_pending": FieldHelp(
        explanation="Pending Diagnostic Trouble Codes stored in scanner Mode $07.",
        options=["List of 5-character alphanumeric fault codes"]
    ),
    "dtc_permanent": FieldHelp(
        explanation="Permanent Diagnostic Trouble Codes stored in scanner Mode $0A.",
        options=["List of 5-character alphanumeric fault codes"]
    ),
    "mode06_monitors": FieldHelp(
        explanation="Mode $06 on-board monitor diagnostic test results.",
        options=["List of monitor dicts"]
    ),
    "mode06_monitor_id": FieldHelp(
        explanation="The standardized hex identifier for the monitor (MID) and test (TID).",
        options=["MID_XX_TID_YY hex format"]
    ),
    "mode06_result_state": FieldHelp(
        explanation="The test status reported by the scanner.",
        options=["Passed", "Pending/marginal", "Critical fail"]
    ),
    "mode06_margin_pct": FieldHelp(
        explanation="The margin remaining before the test limit is exceeded.",
        min_val=-100.0,
        max_val=100.0,
        unit="%"
    ),
    # FF fields
    "ff_calculated_load_pct": FieldHelp(
        explanation="Calculated engine load percentage stored at the time of the fault.",
        min_val=FF_LOAD_MIN,
        max_val=FF_LOAD_MAX,
        unit="%"
    ),
    "ff_engine_rpm": FieldHelp(
        explanation="Engine speed stored at the time of the fault.",
        min_val=FF_RPM_MIN,
        max_val=FF_RPM_MAX,
        unit="RPM"
    ),
    "ff_coolant_temp_c": FieldHelp(
        explanation="Engine coolant temperature stored at the time of the fault.",
        min_val=FF_ECT_MIN,
        max_val=FF_ECT_MAX,
        unit="°C"
    ),
    "ff_short_term_ft1": FieldHelp(
        explanation="Short-term fuel trim for bank 1 stored at the time of the fault.",
        min_val=FF_TRIM_MIN,
        max_val=FF_TRIM_MAX,
        unit="%"
    ),
    "ff_long_term_ft1": FieldHelp(
        explanation="Long-term fuel trim for bank 1 stored at the time of the fault.",
        min_val=FF_TRIM_MIN,
        max_val=FF_TRIM_MAX,
        unit="%"
    ),
    "ff_manifold_pressure_kpa": FieldHelp(
        explanation="Manifold absolute pressure stored at the time of the fault.",
        min_val=FF_MAP_MIN,
        max_val=FF_MAP_MAX,
        unit="kPa"
    ),
    "ff_vehicle_speed_kmh": FieldHelp(
        explanation="Vehicle speed stored at the time of the fault.",
        min_val=FF_SPEED_MIN,
        max_val=FF_SPEED_MAX,
        unit="km/h"
    ),
    "ff_ignition_advance_deg": FieldHelp(
        explanation="Ignition timing advance stored at the time of the fault.",
        min_val=FF_IGNITION_MIN,
        max_val=FF_IGNITION_MAX,
        unit="°BTDC"
    ),
    "ff_intake_air_temp_c": FieldHelp(
        explanation="Intake air temperature stored at the time of the fault.",
        min_val=FF_IAT_MIN,
        max_val=FF_IAT_MAX,
        unit="°C"
    ),
    "ff_maf_gps": FieldHelp(
        explanation="Mass airflow sensor reading stored at the time of the fault.",
        min_val=FF_MAF_MIN,
        max_val=FF_MAF_MAX,
        unit="g/s"
    ),
    "ff_throttle_pos_pct": FieldHelp(
        explanation="Absolute throttle position stored at the time of the fault.",
        min_val=FF_THROTTLE_MIN,
        max_val=FF_THROTTLE_MAX,
        unit="%"
    ),
    "ff_fuel_system_status": FieldHelp(
        explanation="Fuel system status loop state stored at the time of the fault.",
        options=["CL", "OL", "OL_DRIVE", "OL_FAULT"]
    ),
    "ff_add_extended": FieldHelp(
        explanation="Enables entry of optional extended freeze-frame parameters.",
        options=["Checked", "Unchecked"]
    ),
    "ff_short_term_ft2": FieldHelp(
        explanation="Short-term fuel trim for bank 2 stored at the time of the fault.",
        min_val=FF_TRIM_MIN,
        max_val=FF_TRIM_MAX,
        unit="%"
    ),
    "ff_long_term_ft2": FieldHelp(
        explanation="Long-term fuel trim for bank 2 stored at the time of the fault.",
        min_val=FF_TRIM_MIN,
        max_val=FF_TRIM_MAX,
        unit="%"
    ),
    "ff_o2_voltage_b1s1": FieldHelp(
        explanation="Upstream oxygen sensor voltage stored at the time of the fault.",
        min_val=FF_O2_V_B1S1_MIN,
        max_val=FF_O2_V_B1S1_MAX,
        unit="V"
    ),
    "ff_barometric_pressure_kpa": FieldHelp(
        explanation="Barometric pressure stored at the time of the fault.",
        min_val=FF_MAP_MIN,
        max_val=FF_MAP_MAX,
        unit="kPa"
    ),
    "ff_commanded_egr_pct": FieldHelp(
        explanation="Commanded EGR valve duty cycle stored at the time of the fault.",
        min_val=FF_THROTTLE_MIN,
        max_val=FF_THROTTLE_MAX,
        unit="%"
    ),
    "ff_run_time_since_start_sec": FieldHelp(
        explanation="Engine run time since start stored at the time of the fault.",
        min_val=FF_RUNTIME_MIN,
        max_val=FF_RUNTIME_MAX,
        unit="s"
    ),
    "ff_fuel_level_pct": FieldHelp(
        explanation="Fuel tank level percentage stored at the time of the fault.",
        min_val=FF_FUEL_LEVEL_MIN,
        max_val=FF_FUEL_LEVEL_MAX,
        unit="%"
    ),
    # Advanced workshop signals C2..C9
    "mode06_catalyst_margin_pct": FieldHelp(
        explanation="Mode $06 catalyst monitor pass margin percentage.",
        min_val=ADV_CAT_MARGIN_MIN,
        max_val=ADV_CAT_MARGIN_MAX,
        unit="%"
    ),
    "catalyst_index_ratio": FieldHelp(
        explanation="Mode $06 catalyst switch ratio between upstream and downstream oxygen sensors.",
        min_val=ADV_CAT_INDEX_MIN,
        max_val=ADV_CAT_INDEX_MAX,
        unit=""
    ),
    "stft_idle_pct": FieldHelp(
        explanation="Short-term fuel trim deviation at idle used to identify fuel delivery skew.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "ltft_idle_pct": FieldHelp(
        explanation="Long-term fuel trim deviation at idle used to identify fuel delivery skew.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "stft_2500_pct": FieldHelp(
        explanation="Short-term fuel trim deviation at 2500 RPM used to identify fuel delivery skew.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "ltft_2500_pct": FieldHelp(
        explanation="Long-term fuel trim deviation at 2500 RPM used to identify fuel delivery skew.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "decel_co_pct": FieldHelp(
        explanation="Tailpipe carbon monoxide concentration during deceleration fuel cut-off.",
        min_val=ADV_DECEL_CO_MIN,
        max_val=ADV_DECEL_CO_MAX,
        unit="%"
    ),
    "pre_post_cat_hc_delta_ppm": FieldHelp(
        explanation="Difference between pre-catalyst and post-catalyst hydrocarbon concentrations.",
        min_val=ADV_DELTA_HC_MIN,
        max_val=ADV_DELTA_HC_MAX,
        unit="ppm"
    ),
    "pre_post_cat_co_delta_pct": FieldHelp(
        explanation="Difference between pre-catalyst and post-catalyst carbon monoxide concentrations.",
        min_val=ADV_DELTA_CO_MIN,
        max_val=ADV_DELTA_CO_MAX,
        unit="%"
    ),
    "koeo_map_baro_delta_kpa": FieldHelp(
        explanation="Absolute difference between MAP and barometric pressure at key-on engine-off.",
        min_val=ADV_MAP_BARO_MIN,
        max_val=ADV_MAP_BARO_MAX,
        unit="kPa"
    ),
    "module_voltage_loaded_v": FieldHelp(
        explanation="ECU operating voltage under load used to verify supply circuit integrity.",
        min_val=ADV_VOLTAGE_MIN,
        max_val=ADV_VOLTAGE_MAX,
        unit="V"
    ),
    "dlc_signal_ground_drop_v": FieldHelp(
        explanation="Voltage drop on the diagnostic link connector signal ground wire.",
        min_val=ADV_GND_DROP_MIN,
        max_val=ADV_GND_DROP_MAX,
        unit="V"
    ),
    "bidirectional_fuel_response_ok_bool": FieldHelp(
        explanation="Indicates if fuel system commands elicit the expected oxygen sensor response.",
        options=["—", "True", "False"]
    ),
    "mode06_o2_response_margin_pct": FieldHelp(
        explanation="Mode $06 oxygen sensor response rate monitor margin percentage.",
        min_val=ADV_O2_MARGIN_MIN,
        max_val=ADV_O2_MARGIN_MAX,
        unit="%"
    ),
    "maf_actual_calc_delta_pct_idle": FieldHelp(
        explanation="Percentage difference between measured and calculated mass airflow at idle.",
        min_val=ADV_MAF_DELTA_MIN,
        max_val=ADV_MAF_DELTA_MAX,
        unit="%"
    ),
    "maf_actual_calc_delta_pct_2500": FieldHelp(
        explanation="Percentage difference between measured and calculated mass airflow at 2500 RPM.",
        min_val=ADV_MAF_DELTA_MIN,
        max_val=ADV_MAF_DELTA_MAX,
        unit="%"
    ),
    "maf_gps_idle": FieldHelp(
        explanation="Measured mass airflow rate at idle operating point.",
        min_val=ADV_MAF_GPS_MIN,
        max_val=ADV_MAF_GPS_MAX,
        unit="g/s"
    ),
    "maf_gps_2500": FieldHelp(
        explanation="Measured mass airflow rate at 2500 RPM operating point.",
        min_val=ADV_MAF_GPS_MIN,
        max_val=ADV_MAF_GPS_MAX,
        unit="g/s"
    ),
    "calc_airflow_gps_idle": FieldHelp(
        explanation="Calculated/modeled mass airflow rate at idle operating point.",
        min_val=ADV_MAF_GPS_MIN,
        max_val=ADV_MAF_GPS_MAX,
        unit="g/s"
    ),
    "calc_airflow_gps_2500": FieldHelp(
        explanation="Calculated/modeled mass airflow rate at 2500 RPM operating point.",
        min_val=ADV_MAF_GPS_MIN,
        max_val=ADV_MAF_GPS_MAX,
        unit="g/s"
    ),
    "stft_load_pct": FieldHelp(
        explanation="Short-term fuel trim deviation under engine load.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "ltft_load_pct": FieldHelp(
        explanation="Long-term fuel trim deviation under engine load.",
        min_val=OBD_TRIM_MIN,
        max_val=OBD_TRIM_MAX,
        unit="%"
    ),
    "calc_load_wot_pct": FieldHelp(
        explanation="Calculated engine load under wide-open throttle conditions.",
        min_val=FF_LOAD_MIN,
        max_val=FF_LOAD_MAX,
        unit="%"
    ),
    "fuel_rail_pressure_load_kpa": FieldHelp(
        explanation="Fuel rail pressure under engine load, port or direct injection.",
        min_val=ADV_PRESSURE_MIN,
        max_val=ADV_PRESSURE_MAX,
        unit="kPa"
    ),
    "wideband_lambda_wot": FieldHelp(
        explanation="Measured wideband lambda under wide-open throttle conditions.",
        min_val=ADV_LAMBDA_WOT_MIN,
        max_val=ADV_LAMBDA_WOT_MAX,
        unit=""
    ),
    "co2_idle_pct": FieldHelp(
        explanation="Tailpipe carbon dioxide concentration at idle used to verify lean mixtures.",
        min_val=ADV_CO2_MIN,
        max_val=ADV_CO2_MAX,
        unit="%"
    ),
    "tailpipe_o2_elevation_pct": FieldHelp(
        explanation="Elevated tailpipe oxygen concentration at idle indicating dilution.",
        min_val=ADV_O2_ELEV_MIN,
        max_val=ADV_O2_ELEV_MAX,
        unit="%"
    ),
    "downstream_o2_v": FieldHelp(
        explanation="Downstream oxygen sensor voltage used to detect sensor bias.",
        min_val=OBD_O2_DN_MIN,
        max_val=OBD_O2_DN_MAX,
        unit="V"
    ),
    "propane_trim_shift_pct": FieldHelp(
        explanation="Fuel trim shift percentage observed during propane enrichment test.",
        min_val=ADV_MAF_DELTA_MIN,
        max_val=ADV_MAF_DELTA_MAX,
        unit="%"
    ),
    "readiness_supported_complete_bool": FieldHelp(
        explanation="Indicates if all non-continuous emission monitors report complete.",
        options=["—", "True", "False"]
    ),
    "stored_dtc_count": FieldHelp(
        explanation="Count of stored diagnostic trouble codes in ECU memory.",
        min_val=ADV_DTC_COUNT_MIN,
        max_val=ADV_DTC_COUNT_MAX,
        unit="codes"
    ),
    "pending_dtc_count": FieldHelp(
        explanation="Count of pending diagnostic trouble codes in ECU memory.",
        min_val=ADV_DTC_COUNT_MIN,
        max_val=ADV_DTC_COUNT_MAX,
        unit="codes"
    ),
    "permanent_dtc_count": FieldHelp(
        explanation="Count of permanent diagnostic trouble codes in ECU memory.",
        min_val=ADV_DTC_COUNT_MIN,
        max_val=ADV_DTC_COUNT_MAX,
        unit="codes"
    ),
    "mode06_min_margin_pct": FieldHelp(
        explanation="Minimum pass margin among all monitored Mode $06 tests.",
        min_val=-100.0,
        max_val=100.0,
        unit="%"
    ),
    "warmup_cycles_since_clear": FieldHelp(
        explanation="Number of engine warm-up cycles since DTC memory was cleared.",
        min_val=ADV_WARMUP_MIN,
        max_val=ADV_WARMUP_MAX,
        unit="cycles"
    ),
    "miles_since_clear": FieldHelp(
        explanation="Vehicle distance traveled since DTC memory was cleared.",
        min_val=ADV_MILES_MIN,
        max_val=ADV_MILES_MAX,
        unit="miles"
    ),

    # Non-widget internal logic control flags accessed from widgets dictionary
    "active_number_of_banks": FieldHelp(
        explanation="Number of active engine cylinder banks decoded from VIN.",
        options=["1", "2"]
    ),
    "active_has_maf_sensor": FieldHelp(
        explanation="Indicates if a Mass Airflow sensor is present in the decoded architecture.",
        options=["True", "False"]
    ),
    "active_has_map_sensor": FieldHelp(
        explanation="Indicates if a Manifold Absolute Pressure sensor is present in the decoded architecture.",
        options=["True", "False"]
    ),
    "active_upstream_o2_type": FieldHelp(
        explanation="Decoded oxygen sensor type for the upstream position.",
        options=["NARROWBAND", "WIDEBAND_AFR", "WIDEBAND_LAMBDA", "WIDEBAND_NB_SIM", "NONE"]
    ),
    "active_downstream_o2_present": FieldHelp(
        explanation="Indicates if a downstream oxygen sensor is present in the decoded architecture.",
        options=["True", "False"]
    ),
    "active_cylinder_count": FieldHelp(
        explanation="Decoded engine cylinder count.",
        min_val=1,
        max_val=12,
        unit="cylinders"
    ),
    "active_egr_equipped": FieldHelp(
        explanation="Indicates if an EGR system is present in the decoded architecture.",
        options=["True", "False"]
    ),
    "active_induction_type": FieldHelp(
        explanation="Decoded engine induction system type.",
        options=["NA", "TURBO", "SUPER"]
    ),
    "vin_confidence": FieldHelp(
        explanation="Decoding confidence tier of the supplied VIN.",
        options=["HIGH", "PARTIAL", "NONE"]
    ),
}



# Human to internal symptom mapping (18 catalog combinations + oil_consumption)
TIER1_UI_TO_INTERNAL = {
    "🚫 Vehicle Won't Start": "vehicle_starting_issues",
    "🔧 Rough Idle / Shudder": "rough_idle_shudder",
    "⬇️ Lack of Power / Hesitation": "lack_of_power_hesitation",
    "⛽ Poor Economy / Fuel Odour": "poor_economy_fuel_odor_sound",
    "🛑 Engine Dies / Stalls": "engine_dies_or_stalls",
    "💨 Visible Exhaust Smoke": "visible_exhaust_smoke",
    "🛢️ Oil Consumption": "oil_consumption",
}

TIER2_UI_TO_INTERNAL = {
    # vehicle_starting_issues
    "No crank / silent": "no_crank_silent",
    "Fast crank / whining": "fast_crank_whining",
    "Normal crank / zero RPM (prolonged crank)": "prolonged_crank_hard_start",
    # rough_idle_shudder
    "Constant shudder / vibration": "constant_vibration_shudder",
    "Surging / hunting idle": "surging_hunting_idle",
    "Stalls on cold start": "stalls_on_cold_start",
    # lack_of_power_hesitation
    "Flat / sluggish always": "flat_sluggish_always",
    "Hesitation at throttle tip-in": "hesitation_throttle_tip_in",
    "Sudden jerk / stumble": "sudden_jerk_stumble",
    # poor_economy_fuel_odor_sound
    "Just poor MPG": "just_poor_mpg",
    "Strong fuel smell": "strong_fuel_smell",
    "Knock / pinging under load": "knock_pinging_under_load",
    # engine_dies_or_stalls
    "When coasting to stop": "when_coasting_to_stop",
    "Intermittent / random cutout": "intermittent_random_cutout",
    "Backfire / loud pop": "backfire_loud_pop",
    # visible_exhaust_smoke
    "Black smoke": "black_smoke",
    "Blue / oily smell": "blue_oily_smell",
    "White / sweet smell": "white_sweet_smell",
    # oil_consumption
    "Blue smoke on cold start that clears": "blue_smoke_on_cold_start_clears",
    "Blue smoke under acceleration": "blue_smoke_under_acceleration",
    "Oil loss without visible smoke": "oil_loss_no_visible_smoke",
}

OCCURS_UI_TO_INTERNAL = {
    "Always": "always",
    "Cold only": "cold_only",
    "Hot only": "hot_only",
    "Intermittent": "intermittent",
}

ENGINE_STATE_UI_TO_INTERNAL = {
    "Running": "running",
    "Cranking": "cranking",
    "Won't start": "will_not_start",
}


def build_diagnose_payload(widgets: dict[str, Any]) -> dict[str, Any]:
    """Assemble UI widget states into the structured dict for wired.diagnose().

    Untouched widgets (None or empty) are omitted from the payload so
    downstream logic/producers can abstain on absence.
    """
    raw_inputs: dict[str, Any] = {}
    num_banks = int(widgets.get("active_number_of_banks") or 1)

    # 1. VIN
    # Always present in raw_inputs per composition.py, defaults to fallback
    vin = str(widgets.get("vin") or "").strip().upper()
    raw_inputs["vin"] = vin if vin else "UNKNOWNVIN0000000"

    # 2. Triage
    triage = {}
    if widgets.get("dna_module"):
        t1_ui = widgets.get("triage_tier_1")
        t2_ui = widgets.get("triage_tier_2")
        
        t1_internal = TIER1_UI_TO_INTERNAL.get(t1_ui) if isinstance(t1_ui, str) else None
        t2_internal = TIER2_UI_TO_INTERNAL.get(t2_ui) if isinstance(t2_ui, str) else None
        
        if t1_internal:
            triage["tier_1"] = t1_internal
        if t2_internal:
            triage["tier_2"] = t2_internal
            
        occurs_ui = widgets.get("triage_occurs_during")
        occurs_internal = OCCURS_UI_TO_INTERNAL.get(occurs_ui) if isinstance(occurs_ui, str) else None
        if occurs_internal:
            triage["occurs_during"] = occurs_internal
            
        eng_ui = widgets.get("triage_engine_state")
        eng_internal = ENGINE_STATE_UI_TO_INTERNAL.get(eng_ui) if isinstance(eng_ui, str) else None
        if eng_internal:
            triage["engine_state"] = eng_internal
            
        # load_state is always "idle" for stationary diagnostics
        triage["load_state"] = "idle"
        
        # Misfire primary symptom can carry the custom recovery/provenance tag
        if t1_internal == "rough_idle_shudder" and t2_internal == "constant_vibration_shudder":
            triage["csv_primary_symptom"] = "blue_smoke_on_cold_start_clears"
            
    if triage:
        raw_inputs["triage"] = triage

    # 3. Overrides
    overrides = {}
    if widgets.get("dna_module") and widgets.get("use_decoded_dna") and widgets.get("vin_confidence") == "HIGH":
        o2_override = widgets.get("override_upstream_o2_type")
        if o2_override == "Narrowband 0-1V (OEM)":
            overrides["upstream_o2_type"] = "NARROWBAND"
        elif o2_override == "Wideband NB-Sim (Aftermarket)":
            overrides["upstream_o2_type"] = "WIDEBAND_NB_SIM"
            
        if widgets.get("override_de_cat"):
            overrides["de_cat"] = True
            
    if overrides:
        raw_inputs["overrides"] = overrides

    # 4. Gas
    gas = {}
    if widgets.get("gas_module"):
        # Low idle
        for field in ("hc", "nox"):
            val = widgets.get(f"gas_{field}")
            if val is not None and str(val).strip() != "":
                gas[field] = int(val)
        for field in ("co", "co2", "o2", "lambda_measured"):
            val = widgets.get(f"gas_{field}")
            if val is not None and str(val).strip() != "":
                gas[field] = float(val)
                
        # High idle
        for field in ("hc_high", "nox_high"):
            val = widgets.get(f"gas_{field}")
            if val is not None and str(val).strip() != "":
                gas[field] = int(val)
        for field in ("co_high", "co2_high", "o2_high", "lambda_2500"):
            val = widgets.get(f"gas_{field}")
            if val is not None and str(val).strip() != "":
                gas[field] = float(val)
                
        # Non-numeric gas status
        if widgets.get("gas_engine_state"):
            gas["engine_state"] = str(widgets.get("gas_engine_state"))
        if widgets.get("gas_block_test_passed"):
            gas["block_test_passed"] = True
            
        # Advanced C2/C4 delta fields
        for field in ("decel_co_pct", "pre_post_cat_hc_delta_ppm", "pre_post_cat_co_delta_pct"):
            val = widgets.get(field)
            if val is not None and str(val).strip() != "":
                gas[field] = float(val)
                
    if gas:
        raw_inputs["gas"] = gas

    # 5. OBD
    obd = {}
    if widgets.get("obd_module"):
        # Basic fields
        for field in ("coolant_temp_c", "calculated_engine_load_pct", "shrtft1", "longft1"):
            val = widgets.get(f"obd_{field}")
            if val is not None and str(val).strip() != "":
                obd[field] = float(val)
                
        val_rpm = widgets.get("obd_engine_rpm")
        if val_rpm is not None and str(val_rpm).strip() != "":
            obd["engine_rpm"] = int(val_rpm)
            
        # Bank config (nominally derived, but required for translator bounds/contracts)
        num_banks = int(widgets.get("active_number_of_banks") or 1)
        obd["number_of_banks"] = num_banks
        
        if num_banks == 2:
            for field in ("shrtft2", "longft2"):
                val = widgets.get(f"obd_{field}")
                if val is not None and str(val).strip() != "":
                    obd[field] = float(val)
        else:
            obd["shrtft2"] = None
            obd["longft2"] = None
            
        # Gated air sensors
        if widgets.get("active_has_maf_sensor"):
            val = widgets.get("obd_mass_airflow_gps")
            if val is not None and str(val).strip() != "":
                obd["mass_airflow_gps"] = float(val)
        if widgets.get("active_has_map_sensor"):
            val = widgets.get("obd_manifold_vacuum_kpa")
            if val is not None and str(val).strip() != "":
                obd["manifold_vacuum_kpa"] = float(val)
                
        # Polymorphic Upstream O2
        o2_type = widgets.get("active_upstream_o2_type", "NARROWBAND")
        if o2_type != "NONE":
            val_o2 = widgets.get("obd_upstream_o2_val")
            if val_o2 is not None and str(val_o2).strip() != "":
                # WIDEBAND_LINEAR maps to pid_wideband_equivalence_ratio;
                # Narrowband maps to pid_oxygen_sensor_volts
                if o2_type in ("NARROWBAND", "WIDEBAND_NB_SIM"):
                    obd["pid_oxygen_sensor_volts"] = float(val_o2)
                elif o2_type in ("WIDEBAND_LAMBDA", "WIDEBAND_AFR"):
                    obd["pid_wideband_equivalence_ratio"] = float(val_o2)
                    
        # Downstream O2 present
        if widgets.get("active_downstream_o2_present"):
            val_ds = widgets.get("obd_downstream_o2_v")
            if val_ds is not None and str(val_ds).strip() != "":
                obd["downstream_o2_v"] = float(val_ds)
                
        # Fuel System Status
        fss = widgets.get("obd_fuel_sys_status")
        if fss:
            obd["fuel_sys_status"] = str(fss)
            
        # Symptom Misfire cylinder counts (slider to single-cylinder dict)
        t1_ui = widgets.get("triage_tier_1")
        if widgets.get("dna_module") and t1_ui == "🔧 Rough Idle / Shudder":
            misfire_cyl = widgets.get("symptom_misfire_cylinder")
            if misfire_cyl:
                # set Nth cylinder to 40 misfires, others to 0 up to active cylinder count
                cyl_count = int(widgets.get("active_cylinder_count") or 4)
                counts = {}
                for c in range(1, cyl_count + 1):
                    counts[c] = 40 if c == int(misfire_cyl) else 0
                obd["per_cylinder_misfire_counts"] = counts

        # Advanced C2..C9 columns (ferried straight to obd)
        for field in (
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
            "koeo_map_baro_delta_kpa",
            "module_voltage_loaded_v",
            "dlc_signal_ground_drop_v",
            "stft_load_pct",
            "ltft_load_pct",
            "calc_load_wot_pct",
            "fuel_rail_pressure_load_kpa",
            "wideband_lambda_wot",
            "co2_idle_pct",
            "tailpipe_o2_elevation_pct",
            "propane_trim_shift_pct",
            "downstream_o2_v",
            "stored_dtc_count",
            "pending_dtc_count",
            "permanent_dtc_count",
            "mode06_min_margin_pct",
            "warmup_cycles_since_clear",
            "miles_since_clear",
        ):
            val = widgets.get(field)
            if val is not None and str(val).strip() != "":
                obd[field] = float(val)
                
        # Advanced booleans (selectbox maps to boolean/None)
        for field in ("bidirectional_fuel_response_ok_bool", "readiness_supported_complete_bool"):
            val_bool = widgets.get(field)
            if val_bool == "True":
                obd[field] = True
            elif val_bool == "False":
                obd[field] = False
                
    if obd:
        raw_inputs["obd"] = obd

    # 6. DTC
    dtc = {}
    if widgets.get("dtc_module"):
        # MIL checkboxes
        if widgets.get("dtc_active_mil"):
            dtc["active_mil"] = True
        if widgets.get("dtc_mil_flashing"):
            dtc["mil_flashing"] = True
            
        # DTC memory status
        dtc_mem_status = widgets.get("dtc_memory_status")
        if dtc_mem_status == "Recently cleared (<50 mi)":
            dtc["codes_cleared"] = True
        else:
            dtc["codes_cleared"] = False
            
        # raw_dtcs mapping
        raw_dtcs = {}
        for mode, key in [("$03", "dtc_confirmed"), ("$07", "dtc_pending"), ("$0A", "dtc_permanent")]:
            val_str = str(widgets.get(key) or "").strip()
            if val_str:
                # split by commas or spaces, filter non-empty
                parts = [p.strip().upper() for p in val_str.replace(",", " ").split() if p.strip()]
                if parts:
                    raw_dtcs[mode] = parts
        if raw_dtcs:
            dtc["raw_dtcs"] = raw_dtcs
            
        # raw_mode06 mapping (repeating rows margin)
        # widgets["mode06_monitors"] is expected to be a list of dicts: [{"monitor_id": ..., "margin_pct": ...}]
        raw_mode06 = {}
        for mon in widgets.get("mode06_monitors", []):
            mid = str(mon.get("monitor_id") or "").strip().upper()
            margin = mon.get("margin_pct")
            if mid and margin is not None:
                try:
                    raw_mode06[mid] = float(margin)
                except ValueError:
                    pass
        if raw_mode06:
            dtc["raw_mode06"] = raw_mode06
            
        # raw_freeze_frame (12 mandatory + 7 optional)
        raw_ff = {}
        ff_active = False
        
        # Mandatory PIDs
        ff_fields = {
            "ff_calculated_load_pct": ("calculated_load_pct", float),
            "ff_engine_rpm": ("engine_rpm", int),
            "ff_coolant_temp_c": ("coolant_temp_c", float),
            "ff_short_term_ft1": ("short_term_ft1", float),
            "ff_long_term_ft1": ("long_term_ft1", float),
            "ff_manifold_pressure_kpa": ("manifold_pressure_kpa", float),
            "ff_vehicle_speed_kmh": ("vehicle_speed_kmh", int),
            "ff_ignition_advance_deg": ("ignition_advance_deg", float),
            "ff_intake_air_temp_c": ("intake_air_temp_c", float),
            "ff_maf_gps": ("maf_gps", float),
            "ff_throttle_pos_pct": ("throttle_pos_pct", float),
        }
        for w_key, (ff_key, coerce_fn) in ff_fields.items():
            val = widgets.get(w_key)
            if val is not None and str(val).strip() != "":
                raw_ff[ff_key] = coerce_fn(val)
                ff_active = True
                
        # Loop status
        ff_fss = widgets.get("ff_fuel_system_status")
        if ff_fss:
            raw_ff["fuel_system_status"] = str(ff_fss)
            ff_active = True
            
        # Optional / extended PIDs (if "Add extended freeze-frame PIDs" is ticked)
        if widgets.get("ff_add_extended"):
            ext_fields = {
                "ff_short_term_ft2": ("short_term_ft2", float),
                "ff_long_term_ft2": ("long_term_ft2", float),
                "ff_o2_voltage_b1s1": ("o2_voltage_b1s1", float),
                "ff_barometric_pressure_kpa": ("barometric_pressure_kpa", float),
                "ff_commanded_egr_pct": ("commanded_egr_pct", float),
                "ff_run_time_since_start_sec": ("run_time_since_start_sec", int),
                "ff_fuel_level_pct": ("fuel_level_pct", float),
            }
            for w_key, (ff_key, coerce_fn) in ext_fields.items():
                # check DNA limits
                show_field = True
                if ff_key in ("short_term_ft2", "long_term_ft2") and num_banks != 2:
                    show_field = False
                if ff_key == "o2_voltage_b1s1" and not widgets.get("active_downstream_o2_present"):
                    show_field = False
                if ff_key == "commanded_egr_pct" and not widgets.get("active_egr_equipped"):
                    show_field = False
                    
                if show_field:
                    val = widgets.get(w_key)
                    if val is not None and str(val).strip() != "":
                        raw_ff[ff_key] = coerce_fn(val)
                        ff_active = True
                        
        if ff_active:
            dtc["raw_freeze_frame"] = raw_ff
            
    if dtc:
        raw_inputs["dtc"] = dtc

    return raw_inputs
