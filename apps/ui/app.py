#!/usr/bin/env python3
"""4D Petrol Diagnostic Engine — Streamlit UI (V2)."""

import json
from pathlib import Path
import streamlit as st

from wired.composition import diagnose
from ui_payload import (
    build_diagnose_payload,
    TIER1_UI_TO_INTERNAL,
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
    UPSTREAM_O2_NARROWBAND_MIN, UPSTREAM_O2_NARROWBAND_MAX,
    UPSTREAM_O2_WIDEBAND_LAMBDA_MIN, UPSTREAM_O2_WIDEBAND_LAMBDA_MAX,
    UPSTREAM_O2_WIDEBAND_AFR_MIN, UPSTREAM_O2_WIDEBAND_AFR_MAX,
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

# Page configuration
st.set_page_config(
    page_title="4D Petrol Diagnostic Engine",
    page_icon="🔧",
    layout="wide"
)
# Initialize all telemetry variables to None or defaults to ensure they are always bound in scope for Pyright
gas_low_hc = None
gas_low_co = None
gas_low_co2 = None
gas_low_o2 = None
gas_low_nox = None
gas_low_lambda = None
gas_high_hc = None
gas_high_co = None
gas_high_co2 = None
gas_high_o2 = None
gas_high_nox = None
gas_high_lambda = None
obd_low_rpm = None
obd_low_ect = None
obd_low_load = None
obd_low_stft1 = None
obd_low_ltft1 = None
obd_low_stft2 = None
obd_low_ltft2 = None
obd_low_maf = None
obd_low_map = None
obd_low_o2_up = None
obd_low_o2_dn = None
obd_low_fss = ""
active_mil = False
mil_flashing = False
confirmed_dtcs = ""
pending_dtcs = ""
permanent_dtcs = ""
ff_load = None
ff_rpm = None
ff_ect = None
ff_stft_b1 = None
ff_ltft_b1 = None
ff_map = None
ff_speed = None
ff_ignition = None
ff_intake_air_temp_c = None
ff_maf = None
ff_throttle = None
ff_fss = ""
ff_add_extended = False
ff_stft_b2 = None
ff_long_term_ft2 = None
ff_o2_voltage_b1s1 = None
ff_barometric = None
ff_egr = None
ff_runtime = None
ff_fuel_level = None

adv_mode06_catalyst_margin_pct = None
adv_catalyst_index_ratio = None
adv_stft_idle_pct = None
adv_ltft_idle_pct = None
adv_stft_2500_pct = None
adv_ltft_2500_pct = None
adv_decel_co_pct = None
adv_pre_post_cat_hc_delta_ppm = None
adv_pre_post_cat_co_delta_pct = None
adv_koeo_map_baro_delta_kpa = None
adv_module_voltage_loaded_v = None
adv_dlc_signal_ground_drop_v = None
adv_bidirectional_fuel_response_ok_bool = "—"
adv_mode06_o2_response_margin_pct = None
adv_maf_actual_calc_delta_pct_idle = None
adv_maf_actual_calc_delta_pct_2500 = None
adv_maf_gps_idle = None
adv_maf_gps_2500 = None
adv_calc_airflow_gps_idle = None
adv_calc_airflow_gps_2500 = None
adv_stft_load_pct = None
adv_ltft_load_pct = None
adv_calc_load_wot_pct = None
adv_fuel_rail_pressure_load_kpa = None
adv_wideband_lambda_wot = None
adv_co2_idle_pct = None
adv_tailpipe_o2_elevation_pct = None
adv_downstream_o2_v = None
adv_propane_trim_shift_pct = None
adv_readiness_supported_complete_bool = "—"
adv_stored_dtc_count = None
adv_pending_dtc_count = None
adv_permanent_dtc_count = None
adv_mode06_min_margin_pct = None
adv_warmup_cycles_since_clear = None
adv_miles_since_clear = None

# Load Mode $06 dictionary for live component lookup
MODE06_DICT = {}
DICT_PATH = Path(__file__).parent.parent / "dtclab" / "dtclab" / "config" / "mode_06_hex_dictionary.json"
if DICT_PATH.exists():
    try:
        with open(DICT_PATH, "r", encoding="utf-8") as f:
            MODE06_DICT = json.load(f)
    except Exception:
        pass

# Custom CSS to force light inputs and cards styling (matches old UI)
st.markdown(
    """
    <style>
    /* Ensure all inputs have white background and visible border */
    .stApp input[type="number"],
    .stApp input[type="text"],
    .stApp textarea,
    .stApp select,
    .stApp .stTextInput input,
    .stApp .stNumberInput input,
    .stApp .stSelectbox input,
    .stApp .stTextInput > div > input,
    .stApp .stNumberInput > div > input,
    .stApp .stSelectbox > div > select {
        background-color: #ffffff !important;
        color: #31333F !important;
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        padding: 4px 8px !important;
    }

    /* Override dark mode completely */
    .stApp {
        background-color: #ffffff !important;
    }

    /* Diagnosis candidate cards */
    .dx-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        background: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .dx-card-top1 {
        border-left: 5px solid #1a73e8;
        background: #f8faff;
        box-shadow: 0 2px 6px rgba(26,115,232,0.12);
    }
    .dx-card-top2, .dx-card-top3 {
        border-left: 3px solid #9aa0a6;
        background: #fafafa;
    }
    .dx-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
    }
    .dx-fault-name {
        font-weight: 600;
        font-size: 1.05em;
        color: #202124;
    }
    .dx-fault-name-top1 {
        font-size: 1.25em;
        color: #1a73e8;
    }
    .dx-confidence {
        font-size: 0.9em;
        color: #5f6368;
        white-space: nowrap;
    }
    .dx-confidence-bar {
        height: 8px;
        border-radius: 4px;
        background: #e8eaed;
        margin: 8px 0;
        overflow: hidden;
    }
    .dx-confidence-bar-fill {
        height: 8px;
        border-radius: 4px;
        background: #1a73e8;
        transition: width 0.3s ease;
    }
    .dx-confidence-bar-fill-secondary {
        background: #9aa0a6;
    }
    .dx-badge {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75em;
        font-weight: 500;
        white-space: nowrap;
    }
    .dx-evidence {
        margin-top: 8px;
        font-size: 0.85em;
        color: #5f6368;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def _check_radio(options: list[str], state_key: str, default_index: int = 0, help_text: str | None = None, help_str: str | None = None) -> str:
    """Render a single-select radio button group as square checkboxes."""
    if state_key not in st.session_state:
        st.session_state[state_key] = options[default_index]
        for opt in options:
            st.session_state[f"{state_key}__{opt}"] = (opt == options[default_index])

    if help_text:
        st.caption(help_text)

    def _on_toggle(sk: str, opts: list[str], just_clicked: str) -> None:
        if st.session_state[f"{sk}__{just_clicked}"]:
            st.session_state[sk] = just_clicked
            for other in opts:
                if other != just_clicked:
                    st.session_state[f"{sk}__{other}"] = False
        else:
            st.session_state[f"{sk}__{just_clicked}"] = True

    for opt in options:
        st.checkbox(
            opt,
            key=f"{state_key}__{opt}",
            on_change=_on_toggle,
            args=(state_key, options, opt),
            help=help_str
        )
    return st.session_state[state_key]


# Initialize session state for repeating Mode $06 monitors
if "monitors" not in st.session_state:
    st.session_state.monitors = []

# Title
st.title("🔧 4D Petrol Diagnostic Engine")

# LEFT SIDEBAR
with st.sidebar:
    st.header("⚙️ Vehicle Context")

    # Modules selection block
    st.markdown("### 🧩 Modules in this diagnosis")
    st.caption(
        "Tick the data you'll enter today. Each ticked module opens its panel "
        "in the centre and sends that channel to the engine. Tick DNA/VIN to decode "
        "the car and auto-hide fields that don't apply; leave it off for a basic, "
        "show-all diagnosis."
    )
    gas_module = st.checkbox("GASLab", value=True, help=FIELD_HELP["gas_module"].get_tooltip())
    obd_module = st.checkbox("OBDLab", value=True, help=FIELD_HELP["obd_module"].get_tooltip())
    dtc_module = st.checkbox("DTCLab", value=True, help=FIELD_HELP["dtc_module"].get_tooltip())
    dna_module = st.checkbox("DNA / VIN", value=True, help=FIELD_HELP["dna_module"].get_tooltip())

    dna = None
    use_decoded_dna = False
    vin_input = ""

    # VIN Lookup expander
    if dna_module:
        with st.expander("🔍 VIN Lookup", expanded=True):
            vin_input = st.text_input(
                "VIN (17 characters)",
                key="vin_input",
                placeholder="e.g. WBA4W9C5ZLYYYYYYY",
                help=FIELD_HELP["vin"].get_tooltip()
            ).strip().upper()

            if len(vin_input) == 17:
                try:
                    import vinlab
                    dna = vinlab.decode(vin_input)
                    st.success(
                        f"Decoded: {dna.make} {dna.model_year or ''} "
                        f"{dna.engine_displacement_liters}L {dna.cylinder_count}cyl "
                        f"{dna.induction_type} {dna.fuel_delivery_type}"
                    )
                    use_decoded_dna = st.checkbox("✅ Use this decoded DNA", value=True, help=FIELD_HELP["use_decoded_dna"].get_tooltip())
                except Exception:
                    st.warning("VIN decode unavailable — using basic input mode.")
                    use_decoded_dna = False
            elif vin_input:
                st.warning("VIN must be exactly 17 characters.")

    # FALLBACK ATTR & GATES DETERMINATION
    if dna_module and use_decoded_dna and dna:
        active_number_of_banks = dna.number_of_banks
        active_has_maf_sensor = dna.air_metering_architecture.has_maf_sensor
        active_has_map_sensor = dna.air_metering_architecture.has_map_sensor
        active_upstream_o2_type = dna.emissions.upstream_o2_type.value
        active_downstream_o2_present = dna.emissions.downstream_o2_present
        active_egr_equipped = dna.emissions.egr_equipped
        active_cylinder_count = dna.cylinder_count
        active_induction_type = dna.induction_type.value
        active_has_catalyst = dna.emissions.has_catalyst
        vin_confidence = dna.confidence.value
    else:
        # Basic mode defaults per FieldMap §1.6
        active_number_of_banks = 1
        active_has_maf_sensor = False
        active_has_map_sensor = False
        active_upstream_o2_type = "NARROWBAND"
        active_downstream_o2_present = False
        active_egr_equipped = False
        active_cylinder_count = 4
        active_induction_type = "NATURALLY_ASPIRATED"
        active_has_catalyst = True
        vin_confidence = "NONE"

    # Hardware Overrides (HIGH confidence VIN decode only)
    o2_override = "Auto (VIN-decoded)"
    de_cat_override = False
    if dna_module and use_decoded_dna and dna and vin_confidence == "HIGH":
        with st.expander("🛠️ Hardware Overrides", expanded=False):
            st.caption(
                "Override VIN-decoded values when aftermarket hardware is fitted. "
                "Leave on 'Auto' to use the VIN-decoded value."
            )
            o2_override = st.selectbox(
                "Upstream O₂ type override",
                options=["Auto (VIN-decoded)", "Narrowband 0-1V (OEM)", "Wideband NB-Sim (Aftermarket)"],
                index=0,
                help=FIELD_HELP["override_upstream_o2_type"].get_tooltip()
            )
            de_cat_override = st.checkbox("De-catted vehicle", value=False, help=FIELD_HELP["override_de_cat"].get_tooltip())
            
            # Apply overrides to active visibility states
            if o2_override == "Narrowband 0-1V (OEM)":
                active_upstream_o2_type = "NARROWBAND"
            elif o2_override == "Wideband NB-Sim (Aftermarket)":
                active_upstream_o2_type = "WIDEBAND_NB_SIM"
            if de_cat_override:
                active_has_catalyst = False

    # Context expanders
    fuel_blend_val = _check_radio(["E0", "E5", "E10"], "fuel_blend", default_index=2, help_text="⛽ Fuel Blend", help_str=FIELD_HELP["fuel_blend"].get_tooltip())
    mileage_val = _check_radio(["Unknown", "Low", "Mid", "High"], "mileage", default_index=0, help_text="🛣️ Mileage", help_str=FIELD_HELP["mileage"].get_tooltip())
    dtc_mem_status = _check_radio(["Normal", "Recently cleared (<50 mi)"], "dtc_memory_status", default_index=0, help_text="🗒️ DTC Memory Status", help_str=FIELD_HELP["dtc_memory_status"].get_tooltip())

    # Symptom expander
    triage_tier_1 = "—"
    triage_tier_2 = "—"
    misfire_cyl = None
    triage_free_text_notes = ""
    triage_occurs_during = "Always"
    triage_engine_state = "Running"
    
    if dna_module:
        with st.expander("🩺 Primary Symptom", expanded=True):
            st.caption("Pick the main complaint, then the sub-filter.")
            triage_tier_1 = st.selectbox(
                "Primary symptom (Tier 1)",
                options=["—"] + list(TIER1_UI_TO_INTERNAL.keys()),
                index=0,
                help=FIELD_HELP["triage_tier_1"].get_tooltip()
            )
            
            if triage_tier_1 != "—":
                pad, body = st.columns([0.06, 0.94])
                with body:
                    # Filter Tier 2 options by Tier 1 selection
                    allowed_t2 = ["—"]
                    if triage_tier_1 == "🚫 Vehicle Won't Start":
                        allowed_t2 += ["No crank / silent", "Fast crank / whining", "Normal crank / zero RPM (prolonged crank)"]
                    elif triage_tier_1 == "🔧 Rough Idle / Shudder":
                        allowed_t2 += ["Constant shudder / vibration", "Surging / hunting idle", "Stalls on cold start"]
                    elif triage_tier_1 == "⬇️ Lack of Power / Hesitation":
                        allowed_t2 += ["Flat / sluggish always", "Hesitation at throttle tip-in", "Sudden jerk / stumble"]
                    elif triage_tier_1 == "⛽ Poor Economy / Fuel Odour":
                        allowed_t2 += ["Just poor MPG", "Strong fuel smell", "Knock / pinging under load"]
                    elif triage_tier_1 == "🛑 Engine Dies / Stalls":
                        allowed_t2 += ["When coasting to stop", "Intermittent / random cutout", "Backfire / loud pop"]
                    elif triage_tier_1 == "💨 Visible Exhaust Smoke":
                        allowed_t2 += ["Black smoke", "Blue / oily smell", "White / sweet smell"]
                    elif triage_tier_1 == "🛢️ Oil Consumption":
                        allowed_t2 += ["Blue smoke on cold start that clears", "Blue smoke under acceleration", "Oil loss without visible smoke"]
                    
                    triage_tier_2 = st.selectbox("Subfield filter (Tier 2)", options=allowed_t2, index=0, help=FIELD_HELP["triage_tier_2"].get_tooltip())
                    
                    # Rough Idle gets misfire slider
                    if triage_tier_1 == "🔧 Rough Idle / Shudder":
                        misfire_cyl = st.slider(
                            "Misfiring cylinder",
                            min_value=1,
                            max_value=active_cylinder_count,
                            value=1,
                            help=FIELD_HELP["symptom_misfire_cylinder"].get_tooltip()
                        )
            
            triage_occurs_during = _check_radio(["Always", "Cold only", "Hot only", "Intermittent"], "occurs_during", default_index=0, help_text="Occurs during", help_str=FIELD_HELP["triage_occurs_during"].get_tooltip())
            triage_engine_state = _check_radio(["Running", "Cranking", "Won't start"], "engine_state", default_index=0, help_text="Engine state", help_str=FIELD_HELP["triage_engine_state"].get_tooltip())
            triage_free_text_notes = st.text_area("Free-text notes", placeholder="Enter additional technician details...")


# CENTRAL LAYOUT — Central expanders
col_main, col_verdict = st.columns([0.65, 0.35])

with col_main:
    # 1. GASLab (Low Idle)
    if gas_module:
        with st.expander("📊 GASLab (Low Idle)", expanded=True):
            st.caption("Engine at V10 Low Idle RPM, fully warm (ECT ≥ 75 °C).")
            gc1, gc2, gc3 = st.columns(3)
            with gc1:
                gas_low_co = st.number_input("CO (%)", min_value=GAS_CO_MIN, max_value=GAS_CO_MAX, value=None, step=0.01, format="%.2f", key="gas_co", help=FIELD_HELP["gas_co"].get_tooltip())
                gas_low_o2 = st.number_input("O₂ (%)", min_value=GAS_O2_MIN, max_value=GAS_O2_MAX, value=None, step=0.01, format="%.2f", key="gas_o2", help=FIELD_HELP["gas_o2"].get_tooltip())
            with gc2:
                gas_low_co2 = st.number_input("CO₂ (%)", min_value=GAS_CO2_MIN, max_value=GAS_CO2_MAX, value=None, step=0.1, format="%.1f", key="gas_co2", help=FIELD_HELP["gas_co2"].get_tooltip())
                gas_low_nox = st.number_input("NOx (ppm)", min_value=GAS_NOX_MIN, max_value=GAS_NOX_MAX, value=None, step=1, key="gas_nox", help=FIELD_HELP["gas_nox"].get_tooltip())
            with gc3:
                gas_low_hc = st.number_input("HC (ppm)", min_value=GAS_HC_MIN, max_value=GAS_HC_MAX, value=None, step=1, key="gas_hc", help=FIELD_HELP["gas_hc"].get_tooltip())
                gas_low_lambda = st.number_input("Measured λ (analyser)", min_value=GAS_LAMBDA_MIN, max_value=GAS_LAMBDA_MAX, value=None, step=0.001, format="%.3f", key="gas_lambda", help=FIELD_HELP["gas_lambda_measured"].get_tooltip())

    # 2. GASLab (High Idle)
    if gas_module:
        with st.expander("📊 GASLab (High Idle)", expanded=False):
            st.caption("Engine held warm at V11 High Idle RPM.")
            ghc1, ghc2, ghc3 = st.columns(3)
            with ghc1:
                gas_high_co = st.number_input("CO (%)", min_value=GAS_CO_MIN, max_value=GAS_CO_MAX, value=None, step=0.01, format="%.2f", key="gas_co_high", help=FIELD_HELP["gas_co_high"].get_tooltip())
                gas_high_o2 = st.number_input("O₂ (%)", min_value=GAS_O2_MIN, max_value=GAS_O2_MAX, value=None, step=0.01, format="%.2f", key="gas_o2_high", help=FIELD_HELP["gas_o2_high"].get_tooltip())
            with ghc2:
                gas_high_co2 = st.number_input("CO₂ (%)", min_value=GAS_CO2_MIN, max_value=GAS_CO2_MAX, value=None, step=0.1, format="%.1f", key="gas_co2_high", help=FIELD_HELP["gas_co2_high"].get_tooltip())
                gas_high_nox = st.number_input("NOx (ppm)", min_value=GAS_NOX_MIN, max_value=GAS_NOX_MAX, value=None, step=1, key="gas_nox_high", help=FIELD_HELP["gas_nox_high"].get_tooltip())
            with ghc3:
                gas_high_hc = st.number_input("HC (ppm)", min_value=GAS_HC_MIN, max_value=GAS_HC_MAX, value=None, step=1, key="gas_hc_high", help=FIELD_HELP["gas_hc_high"].get_tooltip())
                gas_high_lambda = st.number_input("Measured λ (analyser)", min_value=GAS_LAMBDA_MIN, max_value=GAS_LAMBDA_MAX, value=None, step=0.001, format="%.3f", key="gas_lambda_high", help=FIELD_HELP["gas_lambda_2500"].get_tooltip())

    # 3. OBDLab (Low Idle)
    if obd_module:
        with st.expander("📡 OBDLab (Low Idle)", expanded=True):
            st.caption("Capture at V10 Low Idle RPM — stabilised, closed-loop, ECT ≥ 75 °C.")
            oc1, oc2, oc3, oc4 = st.columns(4)
            with oc1:
                obd_low_rpm = st.number_input("Engine RPM", min_value=OBD_RPM_MIN, max_value=OBD_RPM_MAX, value=None, step=50, key="obd_rpm", help=FIELD_HELP["obd_engine_rpm"].get_tooltip())
                obd_low_stft1 = st.number_input("STFT B1 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_stft1", help=FIELD_HELP["obd_shrtft1"].get_tooltip())
                
                # Bank 2 trims (gated by banks)
                if active_number_of_banks == 2:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        obd_low_stft2 = st.number_input("STFT B2 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_stft2", help=FIELD_HELP["obd_shrtft2"].get_tooltip())
                else:
                    obd_low_stft2 = None
                    
            with oc2:
                obd_low_ect = st.number_input("Coolant temp ECT (°C)", min_value=OBD_ECT_MIN, max_value=OBD_ECT_MAX, value=None, step=1.0, key="obd_ect", help=FIELD_HELP["obd_coolant_temp_c"].get_tooltip())
                obd_low_ltft1 = st.number_input("LTFT B1 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_ltft1", help=FIELD_HELP["obd_longft1"].get_tooltip())
                
                if active_number_of_banks == 2:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        obd_low_ltft2 = st.number_input("LTFT B2 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_ltft2", help=FIELD_HELP["obd_longft2"].get_tooltip())
                else:
                    obd_low_ltft2 = None
                    
            with oc3:
                obd_low_load = st.number_input("Calc load (%)", min_value=OBD_LOAD_MIN, max_value=OBD_LOAD_MAX, value=None, step=1.0, key="obd_load", help=FIELD_HELP["obd_calculated_engine_load_pct"].get_tooltip())
                
                # Gated MAF
                if active_has_maf_sensor:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        obd_low_maf = st.number_input("MAF (g/s)", min_value=OBD_MAF_MIN, max_value=OBD_MAF_MAX, value=None, step=0.1, key="obd_maf", help=FIELD_HELP["obd_mass_airflow_gps"].get_tooltip())
                else:
                    obd_low_maf = None
                    
                # Gated MAP
                if active_has_map_sensor:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        obd_low_map = st.number_input("MAP (kPa)", min_value=OBD_MAP_MIN, max_value=OBD_MAP_MAX, value=None, step=1.0, key="obd_map", help=FIELD_HELP["obd_manifold_vacuum_kpa"].get_tooltip())
                else:
                    obd_low_map = None
                    
            with oc4:
                # Upstream O2 polymorphic input
                obd_low_o2_up = None
                if active_upstream_o2_type != "NONE":
                    if active_upstream_o2_type in ("NARROWBAND", "WIDEBAND_NB_SIM"):
                        obd_low_o2_up = st.number_input("Upstream O₂ (V)", min_value=UPSTREAM_O2_NARROWBAND_MIN, max_value=UPSTREAM_O2_NARROWBAND_MAX, value=None, step=0.01, key="obd_o2_up", help=FIELD_HELP["obd_upstream_o2_val"].get_tooltip())
                    elif active_upstream_o2_type == "WIDEBAND_LAMBDA":
                        obd_low_o2_up = st.number_input("Upstream O₂ (λ)", min_value=UPSTREAM_O2_WIDEBAND_LAMBDA_MIN, max_value=UPSTREAM_O2_WIDEBAND_LAMBDA_MAX, value=None, step=0.001, format="%.3f", key="obd_o2_up", help=FIELD_HELP["obd_upstream_o2_val"].get_tooltip())
                    elif active_upstream_o2_type == "WIDEBAND_AFR":
                        obd_low_o2_up = st.number_input("Upstream O₂ (AFR)", min_value=UPSTREAM_O2_WIDEBAND_AFR_MIN, max_value=UPSTREAM_O2_WIDEBAND_AFR_MAX, value=None, step=0.1, format="%.1f", key="obd_o2_up", help=FIELD_HELP["obd_upstream_o2_val"].get_tooltip())
                
                # Gated downstream O2
                if active_downstream_o2_present:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        obd_low_o2_dn = st.number_input("Downstream O₂ S12 (V)", min_value=OBD_O2_DN_MIN, max_value=OBD_O2_DN_MAX, value=None, step=0.01, format="%.2f", key="obd_o2_dn", help=FIELD_HELP["obd_downstream_o2_v"].get_tooltip())
                else:
                    obd_low_o2_dn = None
                    
                obd_low_fss = st.selectbox("Fuel-sys status", options=["", "CL", "OL", "OL_DRIVE", "OL_FAULT"], index=0, key="obd_fss", help=FIELD_HELP["obd_fuel_sys_status"].get_tooltip())

    # 4. OBDLab (High Idle)
    if obd_module:
        with st.expander("📡 OBDLab (High Idle)", expanded=False):
            st.caption("Capture at U2 RPM (stationary noise test point) — ECT ≥ 75 °C.")
            ohc1, ohc2, ohc3, ohc4 = st.columns(4)
            with ohc1:
                st.number_input("Engine RPM", min_value=OBD_RPM_MIN, max_value=OBD_RPM_MAX, value=None, step=50, key="obd_rpm_high", help=FIELD_HELP["obd_engine_rpm"].get_tooltip())
                st.number_input("STFT B1 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_stft1_high", help=FIELD_HELP["obd_shrtft1"].get_tooltip())
                if active_number_of_banks == 2:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        st.number_input("STFT B2 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_stft2_high", help=FIELD_HELP["obd_shrtft2"].get_tooltip())
            with ohc2:
                st.number_input("Coolant temp ECT (°C)", min_value=OBD_ECT_MIN, max_value=OBD_ECT_MAX, value=None, step=1.0, key="obd_ect_high", help=FIELD_HELP["obd_coolant_temp_c"].get_tooltip())
                st.number_input("LTFT B1 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_ltft1_high", help=FIELD_HELP["obd_longft1"].get_tooltip())
                if active_number_of_banks == 2:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        st.number_input("LTFT B2 (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, step=1.0, key="obd_ltft2_high", help=FIELD_HELP["obd_longft2"].get_tooltip())
            with ohc3:
                st.number_input("Calc load (%)", min_value=OBD_LOAD_MIN, max_value=OBD_LOAD_MAX, value=None, step=1.0, key="obd_load_high", help=FIELD_HELP["obd_calculated_engine_load_pct"].get_tooltip())
                if active_has_maf_sensor:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        st.number_input("MAF (g/s)", min_value=OBD_MAF_MIN, max_value=OBD_MAF_MAX, value=None, step=0.1, key="obd_maf_high", help=FIELD_HELP["obd_mass_airflow_gps"].get_tooltip())
                if active_has_map_sensor:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        st.number_input("MAP (kPa)", min_value=OBD_MAP_MIN, max_value=OBD_MAP_MAX, value=None, step=1.0, key="obd_map_high", help=FIELD_HELP["obd_manifold_vacuum_kpa"].get_tooltip())
            with ohc4:
                if active_upstream_o2_type != "NONE":
                    if active_upstream_o2_type in ("NARROWBAND", "WIDEBAND_NB_SIM"):
                        st.number_input("Upstream O₂ (V)", min_value=UPSTREAM_O2_NARROWBAND_MIN, max_value=UPSTREAM_O2_NARROWBAND_MAX, value=None, step=0.01, key="obd_o2_up_high", help=FIELD_HELP["obd_upstream_o2_val"].get_tooltip())
                    elif active_upstream_o2_type == "WIDEBAND_LAMBDA":
                        st.number_input("Upstream O₂ (λ)", min_value=UPSTREAM_O2_WIDEBAND_LAMBDA_MIN, max_value=UPSTREAM_O2_WIDEBAND_LAMBDA_MAX, value=None, step=0.001, format="%.3f", key="obd_o2_up_high", help=FIELD_HELP["obd_upstream_o2_val"].get_tooltip())
                    elif active_upstream_o2_type == "WIDEBAND_AFR":
                        st.number_input("Upstream O₂ (AFR)", min_value=UPSTREAM_O2_WIDEBAND_AFR_MIN, max_value=UPSTREAM_O2_WIDEBAND_AFR_MAX, value=None, step=0.1, format="%.1f", key="obd_o2_up_high", help=FIELD_HELP["obd_upstream_o2_val"].get_tooltip())
                if active_downstream_o2_present:
                    pad, body = st.columns([0.06, 0.94])
                    with body:
                        st.number_input("Downstream O₂ S12 (V)", min_value=OBD_O2_DN_MIN, max_value=OBD_O2_DN_MAX, value=None, step=0.01, format="%.2f", key="obd_o2_dn_high", help=FIELD_HELP["obd_downstream_o2_v"].get_tooltip())
                st.selectbox("Fuel-sys status", options=["", "CL", "OL", "OL_DRIVE", "OL_FAULT"], index=0, key="obd_fss_high", help=FIELD_HELP["obd_fuel_sys_status"].get_tooltip())

    # 5. DTCLab (DTC)
    if dtc_module:
        with st.expander("📝 DTCLab (DTC)", expanded=True):
            st.caption("MIL indicators and scanner-reported diagnostic trouble codes.")
            dc1, dc2 = st.columns(2)
            with dc1:
                active_mil = st.checkbox("MIL illuminated (solid)", value=False, help=FIELD_HELP["dtc_active_mil"].get_tooltip())
            with dc2:
                mil_flashing = st.checkbox("MIL flashing (Class-A misfire)", value=False, help=FIELD_HELP["dtc_mil_flashing"].get_tooltip())
                
            confirmed_dtcs = st.text_input("Confirmed DTCs (Mode $03)", placeholder="e.g. P0171, P0420", help=FIELD_HELP["dtc_confirmed"].get_tooltip())
            pending_dtcs = st.text_input("Pending DTCs (Mode $07)", placeholder="e.g. P0300", help=FIELD_HELP["dtc_pending"].get_tooltip())
            permanent_dtcs = st.text_input("Permanent DTCs (Mode $0A)", placeholder="e.g. P0171", help=FIELD_HELP["dtc_permanent"].get_tooltip())

    # 6. DTCLab (FF)
    if dtc_module:
        with st.expander("📝 DTCLab (FF)", expanded=False):
            st.caption("Mode $02 Freeze Frame snapshot at fault confirmation.")
            
            # 12 Mandatory fields
            st.markdown("#### 12 Mandatory PIDs")
            fc1, fc2, fc3, fc4 = st.columns(4)
            with fc1:
                ff_load = st.number_input("Calc load (%)", min_value=FF_LOAD_MIN, max_value=FF_LOAD_MAX, value=None, step=1.0, key="ff_load", help=FIELD_HELP["ff_calculated_load_pct"].get_tooltip())
                ff_stft_b1 = st.number_input("STFT B1 (%)", min_value=FF_TRIM_MIN, max_value=FF_TRIM_MAX, value=None, step=0.1, key="ff_stft_b1", help=FIELD_HELP["ff_short_term_ft1"].get_tooltip())
                ff_intake_air_temp_c = st.number_input("Intake air temp IAT (°C)", min_value=FF_IAT_MIN, max_value=FF_IAT_MAX, value=None, step=1.0, key="ff_iat", help=FIELD_HELP["ff_intake_air_temp_c"].get_tooltip())
            with fc2:
                ff_rpm = st.number_input("Engine RPM", min_value=FF_RPM_MIN, max_value=FF_RPM_MAX, value=None, step=50, key="ff_rpm", help=FIELD_HELP["ff_engine_rpm"].get_tooltip())
                ff_ltft_b1 = st.number_input("LTFT B1 (%)", min_value=FF_TRIM_MIN, max_value=FF_TRIM_MAX, value=None, step=0.1, key="ff_ltft_b1", help=FIELD_HELP["ff_long_term_ft1"].get_tooltip())
                ff_maf = st.number_input("MAF (g/s)", min_value=FF_MAF_MIN, max_value=FF_MAF_MAX, value=None, step=0.1, key="ff_maf", help=FIELD_HELP["ff_maf_gps"].get_tooltip())
            with fc3:
                ff_ect = st.number_input("Coolant temp ECT (°C)", min_value=FF_ECT_MIN, max_value=FF_ECT_MAX, value=None, step=1.0, key="ff_ect", help=FIELD_HELP["ff_coolant_temp_c"].get_tooltip())
                ff_map = st.number_input("MAP (kPa)", min_value=FF_MAP_MIN, max_value=FF_MAP_MAX, value=None, step=1, key="ff_map", help=FIELD_HELP["ff_manifold_pressure_kpa"].get_tooltip())
                ff_throttle = st.number_input("Throttle (%)", min_value=FF_THROTTLE_MIN, max_value=FF_THROTTLE_MAX, value=None, step=1.0, key="ff_throttle", help=FIELD_HELP["ff_throttle_pos_pct"].get_tooltip())
            with fc4:
                ff_speed = st.number_input("Vehicle speed (km/h)", min_value=FF_SPEED_MIN, max_value=FF_SPEED_MAX, value=None, step=1, key="ff_speed", help=FIELD_HELP["ff_vehicle_speed_kmh"].get_tooltip())
                ff_ignition = st.number_input("Ignition advance (°BTDC)", min_value=FF_IGNITION_MIN, max_value=FF_IGNITION_MAX, value=None, step=0.5, key="ff_ignition", help=FIELD_HELP["ff_ignition_advance_deg"].get_tooltip())
                ff_fss = st.selectbox("Fuel-system status", options=["", "CL", "OL", "OL_DRIVE", "OL_FAULT"], index=0, key="ff_fss", help=FIELD_HELP["ff_fuel_system_status"].get_tooltip())

            # Extended fields toggle
            ff_add_extended = st.checkbox("Add extended freeze-frame PIDs", value=False, help=FIELD_HELP["ff_add_extended"].get_tooltip())
            if ff_add_extended:
                pad, body = st.columns([0.06, 0.94])
                with body:
                    st.markdown("#### Extended PIDs")
                    fe1, fe2, fe3 = st.columns(3)
                    with fe1:
                        if active_number_of_banks == 2:
                            ff_stft_b2 = st.number_input("STFT B2 (%)", min_value=FF_TRIM_MIN, max_value=FF_TRIM_MAX, value=None, step=0.1, key="ff_stft_b2", help=FIELD_HELP["ff_short_term_ft2"].get_tooltip())
                            ff_long_term_ft2 = st.number_input("LTFT B2 (%)", min_value=FF_TRIM_MIN, max_value=FF_TRIM_MAX, value=None, step=0.1, key="ff_ltft_b2", help=FIELD_HELP["ff_long_term_ft2"].get_tooltip())
                        else:
                            ff_stft_b2 = None
                            ff_long_term_ft2 = None
                            
                        if active_downstream_o2_present:
                            ff_o2_voltage_b1s1 = st.number_input("Upstream O₂ B1S1 (V)", min_value=FF_O2_V_B1S1_MIN, max_value=FF_O2_V_B1S1_MAX, value=None, step=0.001, format="%.3f", key="ff_o2_voltage_b1s1", help=FIELD_HELP["ff_o2_voltage_b1s1"].get_tooltip())
                        else:
                            ff_o2_voltage_b1s1 = None
                            
                    with fe2:
                        ff_barometric = st.number_input("Barometric pressure (kPa)", min_value=FF_MAP_MIN, max_value=FF_MAP_MAX, value=None, step=1, key="ff_baro", help=FIELD_HELP["ff_barometric_pressure_kpa"].get_tooltip())
                        if active_egr_equipped:
                            ff_egr = st.number_input("Commanded EGR (%)", min_value=FF_THROTTLE_MIN, max_value=FF_THROTTLE_MAX, value=None, step=0.1, key="ff_egr", help=FIELD_HELP["ff_commanded_egr_pct"].get_tooltip())
                        else:
                            ff_egr = None
                            
                    with fe3:
                        ff_runtime = st.number_input("Run time since start (s)", min_value=FF_RUNTIME_MIN, max_value=FF_RUNTIME_MAX, value=None, step=1, key="ff_runtime", help=FIELD_HELP["ff_run_time_since_start_sec"].get_tooltip())
                        ff_fuel_level = st.number_input("Fuel level (%)", min_value=FF_FUEL_LEVEL_MIN, max_value=FF_FUEL_LEVEL_MAX, value=None, step=0.1, key="ff_fuel_level", help=FIELD_HELP["ff_fuel_level_pct"].get_tooltip())
            else:
                ff_stft_b2 = None
                ff_long_term_ft2 = None
                ff_o2_voltage_b1s1 = None
                ff_barometric = None
                ff_egr = None
                ff_runtime = None
                ff_fuel_level = None

    # 7. DTCLab ($06)
    if dtc_module:
        with st.expander("📝 DTCLab ($06)", expanded=False):
            st.caption("Mode $06 on-board monitor results.")
            
            # Render repeating monitor rows
            for i, mon in enumerate(st.session_state.monitors):
                col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                with col1:
                    mon_id_val = st.text_input(f"Monitor ID #{i+1}", value=mon["monitor_id"], key=f"mon_id_{i}", help=FIELD_HELP["mode06_monitor_id"].get_tooltip())
                    mon_id = mon_id_val.strip().upper() if mon_id_val else ""
                    st.session_state.monitors[i]["monitor_id"] = mon_id
                    
                    # Component name lookup
                    mid_name = "UNKNOWN"
                    if mon_id.startswith("MID_") and "_TID_" in mon_id:
                        parts = mon_id.split("_")
                        if len(parts) >= 2:
                            mid_hex = parts[1]
                            mid_name = MODE06_DICT.get(mid_hex, {}).get("name", "UNKNOWN")
                    st.caption(f"Component: {mid_name}")
                    
                with col2:
                    st.selectbox(
                        f"Result state #{i+1}",
                        options=["Passed", "Pending/marginal", "Critical fail"],
                        index=0,
                        key=f"mon_state_{i}",
                        help=FIELD_HELP["mode06_result_state"].get_tooltip()
                    )
                with col3:
                    margin = st.number_input(f"Margin (%) #{i+1}", value=mon["margin_pct"], key=f"mon_margin_{i}", help=FIELD_HELP["mode06_margin_pct"].get_tooltip())
                    st.session_state.monitors[i]["margin_pct"] = margin
                with col4:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("🗑️", key=f"mon_del_{i}"):
                        st.session_state.monitors.pop(i)
                        st.rerun()
                        
            if st.button("➕ Add monitor"):
                st.session_state.monitors.append({"monitor_id": "", "margin_pct": None})
                st.rerun()

    # 8. Advanced / workshop signals
    if gas_module or obd_module:
        with st.expander("⚙️ Advanced / workshop signals", expanded=False):
            st.caption("The 36 workshop measurement signals (C2..C9 columns) for diagnostic calibration.")
            
            # C2: Rich/catalyst
            st.markdown("#### Rich/catalyst — C2")
            ac2_1, ac2_2, ac2_3 = st.columns(3)
            with ac2_1:
                adv_mode06_catalyst_margin_pct = st.number_input("mode06_catalyst_margin_pct (%)", min_value=ADV_CAT_MARGIN_MIN, max_value=ADV_CAT_MARGIN_MAX, value=None, key="adv_mode06_catalyst_margin_pct", help=FIELD_HELP["mode06_catalyst_margin_pct"].get_tooltip())
                adv_ltft_idle_pct = st.number_input("ltft_idle_pct (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, key="adv_ltft_idle_pct", help=FIELD_HELP["ltft_idle_pct"].get_tooltip())
                adv_pre_post_cat_hc_delta_ppm = st.number_input("pre_post_cat_hc_delta_ppm (ppm)", min_value=ADV_DELTA_HC_MIN, max_value=ADV_DELTA_HC_MAX, value=None, key="adv_pre_post_cat_hc_delta_ppm", help=FIELD_HELP["pre_post_cat_hc_delta_ppm"].get_tooltip())
            with ac2_2:
                adv_catalyst_index_ratio = st.number_input("catalyst_index_ratio", min_value=ADV_CAT_INDEX_MIN, max_value=ADV_CAT_INDEX_MAX, value=None, key="adv_catalyst_index_ratio", help=FIELD_HELP["catalyst_index_ratio"].get_tooltip())
                adv_stft_2500_pct = st.number_input("stft_2500_pct (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, key="adv_stft_2500_pct", help=FIELD_HELP["stft_2500_pct"].get_tooltip())
                adv_pre_post_cat_co_delta_pct = st.number_input("pre_post_cat_co_delta_pct (%)", min_value=ADV_DELTA_CO_MIN, max_value=ADV_DELTA_CO_MAX, value=None, key="adv_pre_post_cat_co_delta_pct", help=FIELD_HELP["pre_post_cat_co_delta_pct"].get_tooltip())
            with ac2_3:
                adv_stft_idle_pct = st.number_input("stft_idle_pct (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, key="adv_stft_idle_pct", help=FIELD_HELP["stft_idle_pct"].get_tooltip())
                adv_ltft_2500_pct = st.number_input("ltft_2500_pct (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, key="adv_ltft_2500_pct", help=FIELD_HELP["ltft_2500_pct"].get_tooltip())
                adv_decel_co_pct = st.number_input("decel_co_pct (%)", min_value=ADV_DECEL_CO_MIN, max_value=ADV_DECEL_CO_MAX, value=None, key="adv_decel_co_pct", help=FIELD_HELP["decel_co_pct"].get_tooltip())
                
            # C3: ECU electrical
            st.markdown("#### ECU electrical — C3")
            ac3_1, ac3_2 = st.columns(2)
            with ac3_1:
                adv_koeo_map_baro_delta_kpa = st.number_input("koeo_map_baro_delta_kpa (kPa)", min_value=ADV_MAP_BARO_MIN, max_value=ADV_MAP_BARO_MAX, value=None, key="adv_koeo_map_baro_delta_kpa", help=FIELD_HELP["koeo_map_baro_delta_kpa"].get_tooltip())
                adv_dlc_signal_ground_drop_v = st.number_input("dlc_signal_ground_drop_v (V)", min_value=ADV_GND_DROP_MIN, max_value=ADV_GND_DROP_MAX, value=None, key="adv_dlc_signal_ground_drop_v", help=FIELD_HELP["dlc_signal_ground_drop_v"].get_tooltip())
            with ac3_2:
                adv_module_voltage_loaded_v = st.number_input("module_voltage_loaded_v (V)", min_value=ADV_VOLTAGE_MIN, max_value=ADV_VOLTAGE_MAX, value=None, key="adv_module_voltage_loaded_v", help=FIELD_HELP["module_voltage_loaded_v"].get_tooltip())
                adv_bidirectional_fuel_response_ok_bool = st.selectbox("bidirectional_fuel_response_ok_bool", options=["—", "True", "False"], index=0, key="adv_bidirectional_fuel_response_ok_bool", help=FIELD_HELP["bidirectional_fuel_response_ok_bool"].get_tooltip())
                
            # C6: Sensor dynamics
            st.markdown("#### Sensor dynamics — C6")
            ac6_1, ac6_2, ac6_3 = st.columns(3)
            with ac6_1:
                adv_mode06_o2_response_margin_pct = st.number_input("mode06_o2_response_margin_pct (%)", min_value=ADV_O2_MARGIN_MIN, max_value=ADV_O2_MARGIN_MAX, value=None, key="adv_mode06_o2_response_margin_pct", help=FIELD_HELP["mode06_o2_response_margin_pct"].get_tooltip())
                adv_maf_gps_idle = st.number_input("maf_gps_idle (g/s)", min_value=ADV_MAF_GPS_MIN, max_value=ADV_MAF_GPS_MAX, value=None, key="adv_maf_gps_idle", help=FIELD_HELP["maf_gps_idle"].get_tooltip())
                adv_calc_airflow_gps_2500 = st.number_input("calc_airflow_gps_2500 (g/s)", min_value=ADV_MAF_GPS_MIN, max_value=ADV_MAF_GPS_MAX, value=None, key="adv_calc_airflow_gps_2500", help=FIELD_HELP["calc_airflow_gps_2500"].get_tooltip())
            with ac6_2:
                adv_maf_actual_calc_delta_pct_idle = st.number_input("maf_actual_calc_delta_pct_idle (%)", min_value=ADV_MAF_DELTA_MIN, max_value=ADV_MAF_DELTA_MAX, value=None, key="adv_maf_actual_calc_delta_pct_idle", help=FIELD_HELP["maf_actual_calc_delta_pct_idle"].get_tooltip())
                adv_maf_gps_2500 = st.number_input("maf_gps_2500 (g/s)", min_value=ADV_MAF_GPS_MIN, max_value=ADV_MAF_GPS_MAX, value=None, key="adv_maf_gps_2500", help=FIELD_HELP["maf_gps_2500"].get_tooltip())
            with ac6_3:
                adv_maf_actual_calc_delta_pct_2500 = st.number_input("maf_actual_calc_delta_pct_2500 (%)", min_value=ADV_MAF_DELTA_MIN, max_value=ADV_MAF_DELTA_MAX, value=None, key="adv_maf_actual_calc_delta_pct_2500", help=FIELD_HELP["maf_actual_calc_delta_pct_2500"].get_tooltip())
                adv_calc_airflow_gps_idle = st.number_input("calc_airflow_gps_idle (g/s)", min_value=ADV_MAF_GPS_MIN, max_value=ADV_MAF_GPS_MAX, value=None, key="adv_calc_airflow_gps_idle", help=FIELD_HELP["calc_airflow_gps_idle"].get_tooltip())
                
            # C5: Lean root-cause
            st.markdown("#### Lean root-cause — C5")
            ac5_1, ac5_2 = st.columns(2)
            with ac5_1:
                adv_stft_load_pct = st.number_input("stft_load_pct (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, key="adv_stft_load_pct", help=FIELD_HELP["stft_load_pct"].get_tooltip())
                adv_calc_load_wot_pct = st.number_input("calc_load_wot_pct (%)", min_value=OBD_LOAD_MIN, max_value=OBD_LOAD_MAX, value=None, key="adv_calc_load_wot_pct", help=FIELD_HELP["calc_load_wot_pct"].get_tooltip())
                adv_wideband_lambda_wot = st.number_input("wideband_lambda_wot (λ)", min_value=ADV_LAMBDA_WOT_MIN, max_value=ADV_LAMBDA_WOT_MAX, value=None, key="adv_wideband_lambda_wot", help=FIELD_HELP["wideband_lambda_wot"].get_tooltip())
            with ac5_2:
                adv_ltft_load_pct = st.number_input("ltft_load_pct (%)", min_value=OBD_TRIM_MIN, max_value=OBD_TRIM_MAX, value=None, key="adv_ltft_load_pct", help=FIELD_HELP["ltft_load_pct"].get_tooltip())
                adv_fuel_rail_pressure_load_kpa = st.number_input("fuel_rail_pressure_load_kpa (kPa)", min_value=ADV_PRESSURE_MIN, max_value=ADV_PRESSURE_MAX, value=None, key="adv_fuel_rail_pressure_load_kpa", help=FIELD_HELP["fuel_rail_pressure_load_kpa"].get_tooltip())
                
            # C4: Leak/dilution
            st.markdown("#### Leak/dilution — C4")
            ac4_1, ac4_2 = st.columns(2)
            with ac4_1:
                adv_co2_idle_pct = st.number_input("co2_idle_pct (%)", min_value=ADV_CO2_MIN, max_value=ADV_CO2_MAX, value=None, key="adv_co2_idle_pct", help=FIELD_HELP["co2_idle_pct"].get_tooltip())
                adv_downstream_o2_v = st.number_input("downstream_o2_v (V)", min_value=OBD_O2_DN_MIN, max_value=OBD_O2_DN_MAX, value=None, key="adv_downstream_o2_v", help=FIELD_HELP["downstream_o2_v"].get_tooltip())
            with ac4_2:
                adv_tailpipe_o2_elevation_pct = st.number_input("tailpipe_o2_elevation_pct (%)", min_value=ADV_O2_ELEV_MIN, max_value=ADV_O2_ELEV_MAX, value=None, key="adv_tailpipe_o2_elevation_pct", help=FIELD_HELP["tailpipe_o2_elevation_pct"].get_tooltip())
                adv_propane_trim_shift_pct = st.number_input("propane_trim_shift_pct (%)", min_value=ADV_MAF_DELTA_MIN, max_value=ADV_MAF_DELTA_MAX, value=None, key="adv_propane_trim_shift_pct", help=FIELD_HELP["propane_trim_shift_pct"].get_tooltip())
                
            # C9: Health confirm
            st.markdown("#### Health confirm — C9")
            ac9_1, ac9_2, ac9_3 = st.columns(3)
            with ac9_1:
                adv_readiness_supported_complete_bool = st.selectbox("readiness_supported_complete_bool", options=["—", "True", "False"], index=0, key="adv_readiness_supported_complete_bool", help=FIELD_HELP["readiness_supported_complete_bool"].get_tooltip())
                adv_permanent_dtc_count = st.number_input("permanent_dtc_count", min_value=ADV_DTC_COUNT_MIN, max_value=ADV_DTC_COUNT_MAX, value=None, step=1, key="adv_permanent_dtc_count", help=FIELD_HELP["permanent_dtc_count"].get_tooltip())
                adv_miles_since_clear = st.number_input("miles_since_clear", min_value=ADV_MILES_MIN, max_value=ADV_MILES_MAX, value=None, step=1, key="adv_miles_since_clear", help=FIELD_HELP["miles_since_clear"].get_tooltip())
            with ac9_2:
                adv_stored_dtc_count = st.number_input("stored_dtc_count", min_value=ADV_DTC_COUNT_MIN, max_value=ADV_DTC_COUNT_MAX, value=None, step=1, key="adv_stored_dtc_count", help=FIELD_HELP["stored_dtc_count"].get_tooltip())
                adv_mode06_min_margin_pct = st.number_input("mode06_min_margin_pct (%)", min_value=-100.0, max_value=100.0, value=None, key="adv_mode06_min_margin_pct", help=FIELD_HELP["mode06_min_margin_pct"].get_tooltip())
            with ac9_3:
                adv_pending_dtc_count = st.number_input("pending_dtc_count", min_value=ADV_DTC_COUNT_MIN, max_value=ADV_DTC_COUNT_MAX, value=None, step=1, key="adv_pending_dtc_count", help=FIELD_HELP["pending_dtc_count"].get_tooltip())
                adv_warmup_cycles_since_clear = st.number_input("warmup_cycles_since_clear", min_value=ADV_WARMUP_MIN, max_value=ADV_WARMUP_MAX, value=None, step=1, key="adv_warmup_cycles_since_clear", help=FIELD_HELP["warmup_cycles_since_clear"].get_tooltip())


# Trigger calculation
st.markdown("---")
if st.button("🔬 Run Diagnostic Seam", type="primary", use_container_width=True):
    # Assemble widgets dictionary
    widgets = {
        "vin": vin_input,
        "dna_module": dna_module,
        "gas_module": gas_module,
        "obd_module": obd_module,
        "dtc_module": dtc_module,
        "use_decoded_dna": use_decoded_dna if dna_module else False,
        "vin_confidence": vin_confidence,
        "active_number_of_banks": active_number_of_banks,
        "active_has_maf_sensor": active_has_maf_sensor,
        "active_has_map_sensor": active_has_map_sensor,
        "active_upstream_o2_type": active_upstream_o2_type,
        "active_downstream_o2_present": active_downstream_o2_present,
        "active_egr_equipped": active_egr_equipped,
        "active_cylinder_count": active_cylinder_count,
        "active_induction_type": active_induction_type,
        
        "triage_tier_1": triage_tier_1,
        "triage_tier_2": triage_tier_2,
        "triage_occurs_during": triage_occurs_during,
        "triage_engine_state": triage_engine_state,
        "triage_free_text_notes": triage_free_text_notes,
        "symptom_misfire_cylinder": misfire_cyl,
        
        "override_upstream_o2_type": o2_override,
        "override_de_cat": de_cat_override,
        
        # Gas low
        "gas_hc": gas_low_hc,
        "gas_co": gas_low_co,
        "gas_co2": gas_low_co2,
        "gas_o2": gas_low_o2,
        "gas_nox": gas_low_nox,
        "gas_lambda_measured": gas_low_lambda,
        
        # Gas high
        "gas_hc_high": gas_high_hc,
        "gas_co_high": gas_high_co,
        "gas_co2_high": gas_high_co2,
        "gas_o2_high": gas_high_o2,
        "gas_nox_high": gas_high_nox,
        "gas_lambda_2500": gas_high_lambda,
        "gas_engine_state": "STABILIZED_IDLE",
        "gas_block_test_passed": False,
        
        # OBD basic
        "obd_engine_rpm": obd_low_rpm,
        "obd_coolant_temp_c": obd_low_ect,
        "obd_calculated_engine_load_pct": obd_low_load,
        "obd_shrtft1": obd_low_stft1,
        "obd_longft1": obd_low_ltft1,
        "obd_shrtft2": obd_low_stft2,
        "obd_longft2": obd_low_ltft2,
        "obd_mass_airflow_gps": obd_low_maf,
        "obd_manifold_vacuum_kpa": obd_low_map,
        "obd_upstream_o2_val": obd_low_o2_up,
        "obd_downstream_o2_v": obd_low_o2_dn,
        "obd_fuel_sys_status": obd_low_fss,
        
        # DTC basic
        "dtc_active_mil": active_mil,
        "dtc_mil_flashing": mil_flashing,
        "dtc_memory_status": dtc_mem_status,
        "dtc_confirmed": confirmed_dtcs,
        "dtc_pending": pending_dtcs,
        "dtc_permanent": permanent_dtcs,
        "mode06_monitors": st.session_state.monitors,
        
        # FF PIDs
        "ff_calculated_load_pct": ff_load,
        "ff_engine_rpm": ff_rpm,
        "ff_coolant_temp_c": ff_ect,
        "ff_short_term_ft1": ff_stft_b1,
        "ff_long_term_ft1": ff_ltft_b1,
        "ff_manifold_pressure_kpa": ff_map,
        "ff_vehicle_speed_kmh": ff_speed,
        "ff_ignition_advance_deg": ff_ignition,
        "ff_intake_air_temp_c": ff_intake_air_temp_c,
        "ff_maf_gps": ff_maf,
        "ff_throttle_pos_pct": ff_throttle,
        "ff_fuel_system_status": ff_fss,
        
        # FF extended
        "ff_add_extended": ff_add_extended,
        "ff_short_term_ft2": ff_stft_b2,
        "ff_long_term_ft2": ff_long_term_ft2,
        "ff_o2_voltage_b1s1": ff_o2_voltage_b1s1,
        "ff_barometric_pressure_kpa": ff_barometric,
        "ff_commanded_egr_pct": ff_egr,
        "ff_run_time_since_start_sec": ff_runtime,
        "ff_fuel_level_pct": ff_fuel_level,
        
        # 36 columns / Advanced expander
        "mode06_catalyst_margin_pct": adv_mode06_catalyst_margin_pct,
        "catalyst_index_ratio": adv_catalyst_index_ratio,
        "stft_idle_pct": adv_stft_idle_pct,
        "ltft_idle_pct": adv_ltft_idle_pct,
        "stft_2500_pct": adv_stft_2500_pct,
        "ltft_2500_pct": adv_ltft_2500_pct,
        "decel_co_pct": adv_decel_co_pct,
        "pre_post_cat_hc_delta_ppm": adv_pre_post_cat_hc_delta_ppm,
        "pre_post_cat_co_delta_pct": adv_pre_post_cat_co_delta_pct,
        "koeo_map_baro_delta_kpa": adv_koeo_map_baro_delta_kpa,
        "module_voltage_loaded_v": adv_module_voltage_loaded_v,
        "dlc_signal_ground_drop_v": adv_dlc_signal_ground_drop_v,
        "bidirectional_fuel_response_ok_bool": adv_bidirectional_fuel_response_ok_bool,
        "mode06_o2_response_margin_pct": adv_mode06_o2_response_margin_pct,
        "maf_actual_calc_delta_pct_idle": adv_maf_actual_calc_delta_pct_idle,
        "maf_actual_calc_delta_pct_2500": adv_maf_actual_calc_delta_pct_2500,
        "maf_gps_idle": adv_maf_gps_idle,
        "maf_gps_2500": adv_maf_gps_2500,
        "calc_airflow_gps_idle": adv_calc_airflow_gps_idle,
        "calc_airflow_gps_2500": adv_calc_airflow_gps_2500,
        "stft_load_pct": adv_stft_load_pct,
        "ltft_load_pct": adv_ltft_load_pct,
        "calc_load_wot_pct": adv_calc_load_wot_pct,
        "fuel_rail_pressure_load_kpa": adv_fuel_rail_pressure_load_kpa,
        "wideband_lambda_wot": adv_wideband_lambda_wot,
        "co2_idle_pct": adv_co2_idle_pct,
        "tailpipe_o2_elevation_pct": adv_tailpipe_o2_elevation_pct,
        "downstream_o2_v": adv_downstream_o2_v,
        "propane_trim_shift_pct": adv_propane_trim_shift_pct,
        "readiness_supported_complete_bool": adv_readiness_supported_complete_bool,
        "stored_dtc_count": adv_stored_dtc_count,
        "pending_dtc_count": adv_pending_dtc_count,
        "permanent_dtc_count": adv_permanent_dtc_count,
        "mode06_min_margin_pct": adv_mode06_min_margin_pct,
        "warmup_cycles_since_clear": adv_warmup_cycles_since_clear,
        "miles_since_clear": adv_miles_since_clear,
    }

    raw_inputs = build_diagnose_payload(widgets)

    st.session_state.raw_payload = raw_inputs

    try:
        res = diagnose(raw_inputs)
        st.session_state.diagnose_result = res
    except Exception as e:
        st.error(f"❌ Diagnostic calculation failed: {e}")
        st.session_state.diagnose_result = None

# RIGHT VERDICT PANEL
with col_verdict:
    st.header("📋 Diagnostic Results")

    if "diagnose_result" in st.session_state and st.session_state.diagnose_result is not None:
        res = st.session_state.diagnose_result
        meta = res.execution_meta
        verdict = res.diagnostic_verdict
        enrichment = res.fault_enrichment
        analytics = res.performance_analytics

        # 1. Verification Meta info
        st.caption(f"Session ID: `{res.session_id}`")
        st.caption(f"Degradation Mode: **{meta.degradation_mode}**")
        st.caption(f"VIN Decode Confidence: **{meta.vin_confidence}**")

        # Confidence Rating display: band label + score format per contract §3
        # e.g., "HIGH_ASSURANCE" -> "High Assurance"
        band_label = str(meta.processing_confidence_rating).replace("_", " ").title()
        score_val = verdict.confidence_score
        
        st.markdown(f"**Confidence Rating:** `{band_label}` (Score: `{score_val:.2f}`)")

        # 2. ABSTAIN outcome rendering per contract §3.2
        if verdict.abstained:
            st.info("ℹ️ No single confident verdict — top candidates:")
            reason_str = "below floor" if verdict.abstain_reason == "floor" else "within margin"
            st.caption(f"Reason: candidates are {reason_str}")

            # Top candidate (Winner card styled neutrally)
            st.markdown(
                f"""
                <div class="dx-card dx-card-top2">
                    <div class="dx-card-header">
                        <span class="dx-fault-name">{verdict.fault_code} — {verdict.fault_name}</span>
                        <span class="dx-badge">{verdict.fault_family}</span>
                    </div>
                    <div class="dx-confidence-bar">
                        <div class="dx-confidence-bar-fill dx-confidence-bar-fill-secondary" style="width: {verdict.confidence_score * 100}%;"></div>
                    </div>
                    <div class="dx-confidence">Confidence Score: {verdict.confidence_score:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Differential siblings (the runners-up)
            for idx, sib in enumerate(verdict.differential_siblings[:2]):
                conf_text = f"{sib.confidence_score:.2f}" if sib.confidence_score is not None else "null"
                conf_pct = int((sib.confidence_score or 0.0) * 100)
                st.markdown(
                    f"""
                    <div class="dx-card dx-card-top3">
                        <div class="dx-card-header">
                            <span class="dx-fault-name">Candidate #{idx + 2}: {sib.fault_id} — {sib.fault_name}</span>
                            <span class="dx-badge">{sib.fault_family}</span>
                        </div>
                        <div class="dx-confidence-bar">
                            <div class="dx-confidence-bar-fill dx-confidence-bar-fill-secondary" style="width: {conf_pct}%;"></div>
                        </div>
                        <div class="dx-confidence">Confidence Score: {conf_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            # 3. Standard Verdict outcome rendering (Ranked top-3 differential)
            # Winner card styled with prominence (Blue border)
            st.markdown(
                f"""
                <div class="dx-card dx-card-top1">
                    <div class="dx-card-header">
                        <span class="dx-fault-name dx-fault-name-top1">{verdict.fault_code} — {verdict.fault_name}</span>
                        <span class="dx-badge">{verdict.fault_family}</span>
                    </div>
                    <div class="dx-confidence-bar">
                        <div class="dx-confidence-bar-fill" style="width: {verdict.confidence_score * 100}%;"></div>
                    </div>
                    <div class="dx-confidence">Confidence Score: {verdict.confidence_score:.2f}</div>
                    <div style="margin-top: 10px; font-weight: bold;">{verdict.display_headline}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Sibling differential candidates (first 2 distinct families)
            for idx, sib in enumerate(verdict.differential_siblings[:2]):
                conf_text = f"{sib.confidence_score:.2f}" if sib.confidence_score is not None else "null"
                conf_pct = int((sib.confidence_score or 0.0) * 100)
                st.markdown(
                    f"""
                    <div class="dx-card dx-card-top2">
                        <div class="dx-card-header">
                            <span class="dx-fault-name">Candidate #{idx + 2}: {sib.fault_id} — {sib.fault_name}</span>
                            <span class="dx-badge">{sib.fault_family}</span>
                        </div>
                        <div class="dx-confidence-bar">
                            <div class="dx-confidence-bar-fill dx-confidence-bar-fill-secondary" style="width: {conf_pct}%;"></div>
                        </div>
                        <div class="dx-confidence">Confidence Score: {conf_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Remediation information
            st.subheader("🔧 Actionable Remediation")
            st.write(verdict.actionable_remediation)

            # Knowledge graph enrichment details
            with st.expander("🔬 Knowledge Graph Enrichment", expanded=True):
                st.markdown(f"**Component Group:** `{enrichment.component_group}`")
                st.markdown(f"**Mechanical Failure Mode:** {enrichment.mechanical_failure_mode}")
                st.markdown("**UI Remediation Steps:**")
                for step in enrichment.ui_remediation_steps:
                    st.write(f"- {step}")

            # Performance analytics details
            with st.expander("📊 Performance & Perception Analytics", expanded=False):
                st.markdown(f"**Kinetic Power Loss:** `{analytics.kinetic_power_loss_pct:.1f} %`")
                st.markdown(f"**Catalyst Conversion Index:** `{analytics.catalyst_efficiency_index_pct:.1f} %`" if analytics.catalyst_efficiency_index_pct is not None else "**Catalyst Conversion Index:** `N/A`")
                st.markdown(f"**Lambda Perception Delta:** `{analytics.lambda_perception_delta:.3f}`")
                st.markdown(f"**O₂ Sensor Bias Verdict:** `{analytics.o2_sensor_bias_verdict or 'NONE'}`")
                st.markdown(f"**Severity Level:** `{analytics.severity_level}`")

        # Static Calibration Caveat Footer per contract §3.3
        st.markdown("---")
        st.caption(
            "⚠️ **Calibration Caveat:** Rankings are calibrated on research-grounded synthetic "
            "signal data until real measurements accumulate."
        )

    else:
        st.info("Enter vehicle telemetry and click 'Run Diagnostic Seam' to see diagnosis.")
