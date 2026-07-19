#!/usr/bin/env python3
"""4D Petrol Diagnostic Engine — Streamlit UI (V4 5-layer KG)."""

import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import json

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from engine import (
    KnowledgeGraph, calculate_lambda, FUEL_UI_TO_ENGINE, FUEL_STOICH_AFR,
    DiagnosticInput, GasRecord, OBDRecord, DTCSet, FreezeFrameRecord,
    VehicleContext,
)
from engine.layered import diagnose_layered
from engine.validators import classify_o2_upstream, validate_input

# Build fault-id → human-readable label map from schema
_NODES_YAML_PATH = Path(__file__).parent / "schema" / "nodes.yaml"
NODE_LABELS: dict[str, str] = {}
try:
    import yaml as _yaml
    with open(_NODES_YAML_PATH, "r", encoding="utf-8") as _f:
        _nodes_data = _yaml.safe_load(_f)
    for _node in _nodes_data.get("nodes", []):
        _nid = _node.get("id")
        if _nid:
            NODE_LABELS[_nid] = _node.get("name", _nid)
except Exception:
    pass

# AdSense site verification meta tag (injected into <head>)
st.markdown(
    '<meta name="google-adsense-account" content="ca-pub-4889634886203423">',
    unsafe_allow_html=True
)

# Page config
st.set_page_config(
    page_title="4D Petrol Diagnostic Engine",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS to force light inputs
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

    /* ── T11: Diagnosis candidate cards ── */
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
    .dx-evidence li {
        margin-bottom: 2px;
    }
    .dx-evidence-summary {
        cursor: pointer;
        color: #1a73e8;
        font-size: 0.85em;
        font-weight: 500;
    }
    .dx-state-panel {
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 12px;
    }
    .dx-state-insufficient {
        background: #fef7e0;
        border: 1px solid #f9d849;
    }
    .dx-state-invalid {
        background: #fce8e6;
        border: 1px solid #ea4335;
    }
    .dx-state-title {
        font-weight: 600;
        font-size: 1.1em;
        margin-bottom: 6px;
    }
    .dx-state-symptoms {
        font-size: 0.85em;
        color: #5f6368;
        margin-top: 8px;
    }
    .dx-fallback-list {
        font-size: 0.85em;
        margin-top: 8px;
    }

    /* Mobile: stack cards tighter */
    @media (max-width: 640px) {
        .dx-card { padding: 12px; }
        .dx-fault-name-top1 { font-size: 1.1em; }
        .dx-card-header { flex-direction: column; align-items: flex-start; }
        .dx-state-panel { padding: 14px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔧 4D Petrol Diagnostic Engine")
st.markdown(
    "Knowledge graph-based exhaust gas analysis. Configure vehicle context "
    "on the left, enter gas readings and OBD data in the centre"
)

# ---------------------------------------------------------------------------
# Sidebar — Vehicle Context (7 selectors)
# ---------------------------------------------------------------------------
EMISSION_PROFILE_UI_TO_INTERNAL = {
    "Stock OEM (Euro 4-6)": "euro4",
    "Legacy (Pre-Euro 4)": "pre_euro4",
    "Aftermarket Cat (Euro 4-6)": "aftermarket_euro4",
    "De-cat / Modified": "decat",
}
FUEL_UI_LABEL_TO_KEY = {
    "E0 - Pure Petrol (0% ethanol)": "e0",
    "E5 - Petrol (5% ethanol)": "e5",
    "E10 - Standard Petrol (10% ethanol)": "e10",
}
DTC_MEMORY_UI_TO_INTERNAL = {
    "Normal (Codes Persistent)": False,
    "Recently Cleared (<50 miles)": True,
}
ENGINE_TEMP_UI_TO_INTERNAL = {
    "Hot (>60°C)": "hot",
    "Cold (<60°C, SAI may be active)": "cold",
}


def _check_radio(options, state_key, default_index=0, help_text=None):
    """Single-select rendered as a vertical list of square checkboxes
    (st.checkbox). Click a box to select that option; previously-selected
    box auto-unchecks. Forces selection always non-empty.

    Native Streamlit widgets only — no new CSS, preserves Hard Constraint #1.
    Returns the currently-selected option string.
    """
    # initialise the group's state on first render
    if state_key not in st.session_state:
        st.session_state[state_key] = options[default_index]
        for i, opt in enumerate(options):
            st.session_state[f"{state_key}__{opt}"] = (i == default_index)

    if help_text:
        st.caption(help_text)

    def _on_toggle(sk, opts, just_clicked):
        # Streamlit fires this after the user changes one checkbox.
        if st.session_state[f"{sk}__{just_clicked}"]:
            # newly checked → make it the selection, uncheck the rest
            st.session_state[sk] = just_clicked
            for other in opts:
                if other != just_clicked:
                    st.session_state[f"{sk}__{other}"] = False
        else:
            # user unchecked the active selection → re-check it
            st.session_state[f"{sk}__{just_clicked}"] = True

    for opt in options:
        st.checkbox(
            opt,
            key=f"{state_key}__{opt}",
            on_change=_on_toggle,
            args=(state_key, options, opt),
        )

    return st.session_state[state_key]


with st.sidebar:
    st.header("⚙️ Vehicle Context")

    # ── VIN Lookup (Sub-task 1) ──────────────────────────────────────────
    with st.expander("🔍 VIN Lookup", expanded=False):
        vin_input = st.text_input("VIN (17 characters)", key="vin_input",
                                   placeholder="e.g. WVWZZZ1JZ3W386752").strip().upper()
        _dna = None
        if len(vin_input) == 17:
            try:
                from engine.vin import resolve as _vin_resolve
                _dna = _vin_resolve(vin_input)
            except Exception as _e:
                st.caption(f"⚠ VIN lookup error: {_e}")

        if _dna:
            if _dna.confidence == 'high':
                _yr = (f"{_dna.year_range[0]}–{_dna.year_range[1]}"
                       if getattr(_dna, 'year_range', None) else str(_dna.year or ''))
                _dl = f"{_dna.displacement_l}L" if _dna.displacement_l else ""
                st.success(f"✅ {_yr} {_dna.make or ''} · {_dna.engine_code or ''} · {_dl} "
                           f"{_dna.induction or ''} {_dna.injection or ''} · "
                           f"{_dna.o2_arch or ''}")
                if st.button("Auto-fill from VIN", key="vin_autofill"):
                    if _dna.induction in ("turbo", "super", "twincharged"):
                        _ind_map = {"turbo": "Turbocharged", "super": "Supercharged",
                                    "twincharged": "Turbocharged"}
                        st.session_state["sel_induction"] = _ind_map.get(_dna.induction, "NA")
                    else:
                        st.session_state["sel_induction"] = "NA (naturally aspirated)"
                    if _dna.fuel_type:
                        _fuel_map = {"petrol": "E5 - Petrol (5% ethanol)"}
                        _fl = _fuel_map.get(_dna.fuel_type)
                        if _fl:
                            st.session_state["sel_fuel"] = _fl
                    # Push brand + displacement so VehicleContext receives them and
                    # the COC vref_lookup can fire (engine/layered.py:78-91).
                    if _dna.make:
                        st.session_state["vin_brand"] = _dna.make
                    if _dna.displacement_l:
                        st.session_state["vin_displacement_cc"] = int(round(_dna.displacement_l * 1000))
                    if _dna.engine_code:
                        st.session_state["vin_engine_code"] = _dna.engine_code

            elif _dna.confidence == 'partial':
                st.info(f"ℹ️ {_dna.make or 'Manufacturer'} identified — engine not decoded")
                try:
                    from engine.vin import _load_dna as _vdna
                    from engine.vin.engine_dna import EngineDNA as _ED
                    _rows = _vdna()
                    _mfr_rows = [r for r in _rows.values()
                                 if (r.get('manufacturer','') or '').lower()
                                 == (_dna.make or '').lower()
                                 and r.get('induction')]
                    if _mfr_rows:
                        _opts = {r['engine_code']: f"{r['engine_code']} — "
                                                   f"{r.get('displacement_l','?')}L "
                                                   f"{r.get('induction','')}"
                                 for r in sorted(_mfr_rows, key=lambda r: r['engine_code'])}
                        _sel = st.selectbox("Select engine code", list(_opts.keys()),
                                            format_func=lambda k: _opts[k],
                                            key="vin_engine_sel")
                        if _sel:
                            _dna = _ED.from_dna_row(_rows[_sel], source='manual')
                except Exception:
                    pass
            else:
                st.warning("VIN not recognised — fill fields manually below.")

    with st.expander("🔧 Induction Type", expanded=False):
        induction_label = _check_radio(
            options=["NA (naturally aspirated)", "Turbocharged", "Supercharged"],
            state_key="sel_induction",
            default_index=0,
            help_text="Turbocharged/Supercharged activates boost-related fault paths "
                      "(turbo seal, bypass valve, intercooler). Auto-filled if VIN decoded.",
        )
    INDUCTION_UI_TO_INTERNAL = {
        "NA (naturally aspirated)": "na",
        "Turbocharged": "turbo",
        "Supercharged": "super",
    }
    induction_val = INDUCTION_UI_TO_INTERNAL[induction_label]

    with st.expander("Emissions Profile", expanded=False):
        emission_profile_label = _check_radio(
            options=list(EMISSION_PROFILE_UI_TO_INTERNAL.keys()),
            state_key="sel_emission_profile",
            default_index=0,
            help_text=("Stock OEM = factory catalyst within manufacturer specs. "
                       "Legacy = pre-Euro-4 (cat may be tired). "
                       "Aftermarket = replacement catalyst with reduced efficiency. "
                       "De-cat = catalyst removed/gutted."),
        )
    emission_class_internal = EMISSION_PROFILE_UI_TO_INTERNAL[emission_profile_label]

    with st.expander("Fuel Type", expanded=False):
        fuel_label = _check_radio(
            options=list(FUEL_UI_LABEL_TO_KEY.keys()),
            state_key="sel_fuel",
            default_index=2,
            help_text="Affects Brettschneider stoichiometric constants (Hcv, Ocv, AFR).",
        )
    fuel_ui_key = FUEL_UI_LABEL_TO_KEY[fuel_label]
    fuel_engine = FUEL_UI_TO_ENGINE.get(fuel_ui_key, "petrol")
    fuel_stoich = FUEL_STOICH_AFR.get(fuel_ui_key, 14.7)

    # ── Engine Temperature (before DTC per sidebar order) ────────────────────
    with st.expander("🌡️ Engine Temperature", expanded=False):
        temp_label = _check_radio(
            options=list(ENGINE_TEMP_UI_TO_INTERNAL.keys()),
            state_key="sel_engine_temp",
            default_index=0,
            help_text="Cold start relaxes O₂ thresholds and dampens lean-condition priors.",
        )
    engine_temp_val = ENGINE_TEMP_UI_TO_INTERNAL[temp_label]

    # ── Mileage bracket (user input — KG uses low/mid/high on wear nodes) ────
    MILEAGE_UI_TO_INTERNAL = {
        "Unknown": None,
        "Low (< 80,000 km)": "low",
        "Mid (80,000 – 150,000 km)": "mid",
        "High (> 150,000 km)": "high",
    }
    with st.expander("🛣️ Mileage", expanded=False):
        mileage_label = _check_radio(
            options=list(MILEAGE_UI_TO_INTERNAL.keys()),
            state_key="sel_mileage",
            default_index=0,
            help_text="Affects wear-related fault priors (rings, valve seals, "
                      "timing chain stretch, turbo seal).",
        )
    mileage_bracket_val = MILEAGE_UI_TO_INTERNAL[mileage_label]

    with st.expander("🗒️ DTC Memory Status", expanded=False):
        dtc_memory_label = _check_radio(
            options=list(DTC_MEMORY_UI_TO_INTERNAL.keys()),
            state_key="sel_dtc_memory",
            default_index=0,
            help_text=("Recently Cleared inhibits trim-derived symptoms because "
                       "the ECU hasn't relearned fuel adaptation yet."),
        )
    codes_cleared_val = DTC_MEMORY_UI_TO_INTERNAL[dtc_memory_label]

    # ── Primary Symptom (required) ────────────────────────────────────────
    with st.expander("🩺 Primary Symptom", expanded=True):
        _PRIMARY_SYMPTOM_UI_TO_INTERNAL = {
            "Select primary symptom...": None,
            "Check Engine Light (no drivability symptom)": "cel",
            "Rough Idle": "rough_idle",
            "Hesitation / Stumble": "hesitation",
            "Power Loss": "power_loss",
            "Hard Start — Cold Engine": "hard_start_cold",
            "Hard Start — Hot Engine": "hard_start_hot",
            "Non-Starter / Crank No-Start": "non_starter",
            "Black Smoke": "black_smoke",
            "Blue Smoke (oil burning)": "blue_smoke",
            "White Smoke (coolant)": "white_smoke",
            "Fuel Smell": "fuel_smell",
            "Knocking / Pinging": "knocking",
            "Stalling": "stalling",
            "Backfire": "backfire",
            "Other": None,
        }
        primary_symptom_label = st.selectbox(
            "Primary symptom (required)",
            options=list(_PRIMARY_SYMPTOM_UI_TO_INTERNAL.keys()),
            index=0,
            key="primary_symptom_sel",
            help="Routes the diagnosis to the correct fault family. Required for accurate results.",
        )
        primary_symptom_val = _PRIMARY_SYMPTOM_UI_TO_INTERNAL[primary_symptom_label]

        st.caption("Free-text notes (optional, shown in report only):")
        driver_notes = st.text_area(
            "Notes",
            key="driver_notes",
            placeholder="Any additional observations...",
            label_visibility="collapsed",
        )

    st.divider()

    # Probe Depth Check + Validation (driven by L1 inputs)
    low_co_val = st.session_state.get("low_co", 0.0)
    low_co2_val = st.session_state.get("low_co2", 0.0)
    st.markdown("**Probe Depth Check**")
    total_gas = low_co_val + low_co2_val
    if total_gas < 12.0:
        st.warning(
            f"⚠️ Total CO+CO₂ = {total_gas:.1f}% is low. "
            "Ensure probe is inserted 30 cm into tailpipe."
        )
    else:
        st.success(f"✅ Total CO+CO₂ = {total_gas:.1f}% (adequate)")

    st.markdown("**Validation**")
    _v_gases = {
        "co": low_co_val,
        "co2": low_co2_val,
        "hc": st.session_state.get("low_hc", 0),
        "o2": st.session_state.get("low_o2", 0.0),
        "lambda": st.session_state.get("low_lambda", 1.0),
        "nox": st.session_state.get("low_nox", 0),
    }
    v_err = validate_input(_v_gases)
    if v_err:
        st.error(v_err)
    else:
        st.info("Inputs within physical bounds.")

# ---------------------------------------------------------------------------
# Main area — 5 stacked expanders L1..L5 (aligned with PRD-4D-Petrol-Diagnostic-Engine.md)
# ---------------------------------------------------------------------------

# L1 — Low Idle Gas
with st.expander("📊 L1 — Low Idle Gas", expanded=True):
    l1_c1, l1_c2 = st.columns(2)
    with l1_c1:
        co = st.number_input("CO (%)", min_value=0.0, max_value=10.0,
                             value=0.12, step=0.01, format="%.2f", key="low_co")
        co2 = st.number_input("CO₂ (%)", min_value=0.0, max_value=20.0,
                              value=14.8, step=0.1, format="%.1f", key="low_co2")
        hc = st.number_input("HC (ppm)", min_value=0, max_value=20000,
                             value=25, step=1, key="low_hc")
    with l1_c2:
        o2 = st.number_input("O₂ (%)", min_value=0.0, max_value=20.0,
                             value=0.25, step=0.01, format="%.2f", key="low_o2")
        lambda_sensor = st.number_input(
            "Lambda (sensor)", min_value=0.5, max_value=2.0,
            value=1.00, step=0.01, format="%.2f", key="low_lambda",
            help=("Wideband lambda from the analyser. Compare to the "
                  "Brettschneider-calculated λ to detect sensor bias."),
        )
        nox = st.number_input(
            "NOx (ppm)", min_value=0, max_value=5000, value=0, step=1,
            key="low_nox",
            help=("NOx >100 ppm at idle suggests EGR/combustion temperature "
                  "issues; <50 ppm with lean λ flags ECU/sensor inversion."),
        )

# L2 — High Idle Gas
with st.expander("📊 L2 — High Idle Gas (~2500 RPM)", expanded=False):
    # ── COC high-idle target caption ────────────────────────────────────────
    _coc_rpm = None
    _coc_lam = None
    _vin_brand = st.session_state.get("vin_brand")
    _vin_displ = st.session_state.get("vin_displacement_cc")
    if _vin_brand and _vin_displ:
        try:
            from engine.vehicle_reference import lookup as _vref_lookup
            _coc_ref = _vref_lookup(_vin_brand, "petrol", _vin_displ)
            if _coc_ref:
                _coc_rpm = _coc_ref.ref_high_idle_rpm
                _coc_lam = _coc_ref.ref_high_idle_lambda
        except Exception:
            pass
    if _coc_rpm and _coc_lam is not None:
        st.caption(
            f"Hold engine at **{_coc_rpm} RPM** "
            f"(target λ ≈ **{_coc_lam:.3f}**, COC reference)"
        )
    elif _coc_rpm:
        st.caption(
            f"Hold engine at **{_coc_rpm} RPM** (COC reference)"
        )
    l2_c1, l2_c2 = st.columns(2)
    with l2_c1:
        hi_co = st.number_input("CO (%)", min_value=0.0, max_value=10.0,
                                value=0.0, step=0.01, format="%.2f", key="hi_co")
        hi_co2 = st.number_input("CO₂ (%)", min_value=0.0, max_value=20.0,
                                 value=0.0, step=0.1, format="%.1f", key="hi_co2")
        hi_hc = st.number_input("HC (ppm)", min_value=0, max_value=20000,
                                value=0, step=1, key="hi_hc")
    with l2_c2:
        hi_o2 = st.number_input("O₂ (%)", min_value=0.0, max_value=20.0,
                                value=0.0, step=0.01, format="%.2f", key="hi_o2")
        hi_lambda = st.number_input("Lambda (sensor)", min_value=0.0, max_value=2.0,
                                    value=0.0, step=0.01, format="%.2f", key="hi_lambda")
        hi_nox = st.number_input("NOx (ppm)", min_value=0, max_value=5000,
                                 value=0, step=1, key="hi_nox")

# L3 — Live PIDs (Low Idle) + DTCs
with st.expander("📈 L3 — Live PIDs (Low Idle) + DTCs", expanded=False):
    l3_c1, l3_c2 = st.columns(2)
    with l3_c1:
        l3_rpm = st.number_input("Engine RPM", min_value=0, max_value=8000,
                                 value=0, step=1, key="l3_rpm")
        l3_load = st.number_input("Calc Load (%)", min_value=0.0, max_value=100.0,
                                  value=0.0, step=0.1, key="l3_load")
        l3_stft_b1 = st.number_input(
            "STFT B1 (%)", min_value=-25.0, max_value=25.0,
            value=0.0, step=0.1, key="l3_stft_b1",
            help="Short-term fuel trim, bank 1.",
        )
        l3_ltft_b1 = st.number_input(
            "LTFT B1 (%)", min_value=-25.0, max_value=25.0,
            value=0.0, step=0.1, key="l3_ltft_b1",
            help="Long-term fuel trim, bank 1.",
        )
        l3_stft_b2 = st.number_input(
            "STFT B2 (%)", min_value=-25.0, max_value=25.0,
            value=0.0, step=0.1, key="l3_stft_b2",
            help="Bank 2 only on V engines. Leave 0 on inline-4/6.",
        )
        l3_ltft_b2 = st.number_input(
            "LTFT B2 (%)", min_value=-25.0, max_value=25.0,
            value=0.0, step=0.1, key="l3_ltft_b2",
            help="Bank 2 only on V engines. Leave 0 on inline-4/6.",
        )
    with l3_c2:
        l3_o2_up = st.number_input(
            "Upstream O₂ S11 (smart)", min_value=0.0, max_value=2.0,
            value=0.45, step=0.01, format="%.2f", key="l3_o2_up",
            help=("Auto-classified as narrowband voltage (<1V) or wideband "
                  "lambda (~1.0). Compared with Brettschneider λ for sanity."),
        )
        # Live caption — use L1-derived calculated lambda
        try:
            _calc_lam_l1 = calculate_lambda(
                co=co, co2=co2, hc_ppm=hc, o2=o2, nox_ppm=nox,
                fuel_type=fuel_engine,
            )
            _cls = classify_o2_upstream(l3_o2_up, _calc_lam_l1)
            if _cls is not None:
                st.caption(f"🔍 Auto-detected: {_cls.get('type', 'unknown')}")
        except Exception:
            pass
        l3_o2_dn = st.number_input(
            "Downstream O₂ S12 (V)", min_value=0.0, max_value=1.5,
            value=0.0, step=0.01, format="%.2f", key="l3_o2_dn",
            help=("Post-cat narrowband. Active 0.3-0.7 V with P0420 = cat "
                  "inefficient; steady 0.7-0.8 V = healthy cat."),
        )
        l3_maf = st.number_input("MAF (g/s)", min_value=0.0, max_value=500.0,
                                 value=0.0, step=0.1, key="l3_maf")
        l3_map = st.number_input("MAP (kPa)", min_value=0.0, max_value=200.0,
                                 value=0.0, step=0.1, key="l3_map")
        l3_ect = st.number_input("ECT (°C)", min_value=-40, max_value=200,
                                 value=0, step=1, key="l3_ect")

    st.divider()
    dtc_input = st.text_area(
        "DTC Codes (comma or space separated)",
        placeholder="P0171, P0420, P0300", key="l3_dtc",
    )

# L5 — Live PIDs (High Idle, Coming in v1.1)
with st.expander("📈 L5 — Live PIDs (High Idle, 2500-3500 RPM, Coming in v1.1)", expanded=False):
    l4_c1, l4_c2 = st.columns(2)
    with l4_c1:
        l4_rpm_hi = st.number_input("Engine RPM", min_value=0, max_value=8000,
                                    value=0, step=1, key="l4_rpm")
        l4_load_hi = st.number_input("Calc Load (%)", min_value=0.0, max_value=100.0,
                                     value=0.0, step=0.1, key="l4_load")
        l4_stft_b1_hi = st.number_input("STFT B1 (%)", min_value=-25.0, max_value=25.0,
                                        value=0.0, step=0.1, key="l4_stft_b1",
                                        help="Short-term fuel trim, bank 1.")
        l4_ltft_b1_hi = st.number_input("LTFT B1 (%)", min_value=-25.0, max_value=25.0,
                                        value=0.0, step=0.1, key="l4_ltft_b1",
                                        help="Long-term fuel trim, bank 1.")
        l4_stft_b2_hi = st.number_input("STFT B2 (%)", min_value=-25.0, max_value=25.0,
                                        value=0.0, step=0.1, key="l4_stft_b2",
                                        help="V-engine only.")
        l4_ltft_b2_hi = st.number_input("LTFT B2 (%)", min_value=-25.0, max_value=25.0,
                                        value=0.0, step=0.1, key="l4_ltft_b2",
                                        help="V-engine only.")
    with l4_c2:
        l4_o2_up_hi = st.number_input(
            "Upstream O₂ S11 (smart)", min_value=0.0, max_value=2.0,
            value=0.45, step=0.01, format="%.2f", key="l4_o2_up",
            help="Same smart classification as L3.",
        )
        l4_o2_dn_hi = st.number_input(
            "Downstream O₂ S12 (V)", min_value=0.0, max_value=1.5,
            value=0.0, step=0.01, format="%.2f", key="l4_o2_dn",
            help="Active sweep at high RPM with P0420 = aged catalyst.",
        )
        l4_maf_hi = st.number_input("MAF (g/s)", min_value=0.0, max_value=500.0,
                                    value=0.0, step=0.1, key="l4_maf")
        l4_map_hi = st.number_input("MAP (kPa)", min_value=0.0, max_value=200.0,
                                    value=0.0, step=0.1, key="l4_map")
        l4_ect_hi = st.number_input("ECT (°C)", min_value=-40, max_value=200,
                                    value=0, step=1, key="l4_ect")

# L4 — Freeze Frame (Coming in v1.1)
with st.expander("📟 L4 — Freeze Frame (Coming in v1.1)", expanded=False):
    st.markdown("**Freeze Frame Snapshot (15 priority PIDs)**")
    ff_c1, ff_c2, ff_c3, ff_c4 = st.columns(4)
    with ff_c1:
        st.markdown("**Fuel Status**")
        ff_fuel_status = _check_radio(
            options=["CL", "OL", "OL_DRIVE", "OL_FAULT", "CL_FAULT"],
            state_key="ff_fuel_status_sel",
            default_index=0,
        )
        ff_calc_load = st.number_input("Calc Load (%)", min_value=0.0, max_value=100.0,
                                       value=0.0, step=0.1, key="ff_calc_load")
        ff_ect = st.number_input("ECT (°C)", min_value=-40, max_value=200,
                                 value=0, step=1, key="ff_ect")
        ff_iat = st.number_input("IAT (°C)", min_value=-40, max_value=100,
                                 value=0, step=1, key="ff_iat")
        ff_baro = st.number_input(
            "Barometric Pressure (kPa)", min_value=0.0, max_value=120.0,
            value=0.0, step=0.1, key="ff_baro",
            help="<92 kPa hints at altitude effects on fuel mixture.",
        )
    with ff_c2:
        ff_rpm = st.number_input("Engine RPM", min_value=0, max_value=8000,
                                 value=0, step=1, key="ff_rpm")
        ff_speed = st.number_input("Vehicle Speed (km/h)", min_value=0, max_value=300,
                                   value=0, step=1, key="ff_speed")
        ff_map = st.number_input("MAP (kPa)", min_value=0.0, max_value=200.0,
                                 value=0.0, step=0.1, key="ff_map")
        ff_maf = st.number_input("MAF (g/s)", min_value=0.0, max_value=500.0,
                                 value=0.0, step=0.1, key="ff_maf")
        ff_throttle = st.number_input("Throttle (%)", min_value=0.0, max_value=100.0,
                                      value=0.0, step=0.1, key="ff_throttle")
    with ff_c3:
        ff_stft_b1 = st.number_input("STFT B1 (%)", min_value=-25.0, max_value=25.0,
                                     value=0.0, step=0.1, key="ff_stft_b1",
                                     help="Short-term fuel trim, bank 1.")
        ff_ltft_b1 = st.number_input("LTFT B1 (%)", min_value=-25.0, max_value=25.0,
                                     value=0.0, step=0.1, key="ff_ltft_b1",
                                     help="Long-term fuel trim, bank 1.")
        ff_stft_b2 = st.number_input(
            "STFT B2 (%)", min_value=-25.0, max_value=25.0,
            value=0.0, step=0.1, key="ff_stft_b2",
            help="V engines only. Bank-divergent trims hint at one-side faults.",
        )
        ff_ltft_b2 = st.number_input(
            "LTFT B2 (%)", min_value=-25.0, max_value=25.0,
            value=0.0, step=0.1, key="ff_ltft_b2",
            help="V engines only. Compare with B1 for asymmetry.",
        )
    with ff_c4:
        ff_o2_up = st.number_input(
            "Upstream O₂ S11 (smart)", min_value=0.0, max_value=2.0,
            value=0.45, step=0.01, format="%.2f", key="ff_o2_up",
            help="Smart-classified as narrowband or wideband.",
        )
        ff_o2_dn = st.number_input(
            "Downstream O₂ S12 (V)", min_value=0.0, max_value=1.5,
            value=0.0, step=0.01, format="%.2f", key="ff_o2_dn",
            help="Cross-checks L3/L4 downstream signal.",
        )
        ff_ignition = st.number_input(
            "Ignition Advance (°BTDC)", min_value=-20.0, max_value=60.0,
            value=0.0, step=0.1, key="ff_ignition",
            help="Severe retard (>10° below expected) suggests knock-protection.",
        )

    with st.expander("Advanced FF (optional)"):
        ff_fuel_rail = st.number_input(
            "Fuel Rail Pressure (kPa)", min_value=0.0, max_value=20000.0,
            value=0.0, step=1.0, key="ff_fuel_rail",
        )
        ff_egr = st.number_input(
            "Commanded EGR (%)", min_value=0.0, max_value=100.0,
            value=0.0, step=0.1, key="ff_egr",
        )

# ---------------------------------------------------------------------------
# Run Diagnosis
# ---------------------------------------------------------------------------

def _any_nonzero(*values) -> bool:
    """True if any value carries user-entered data (non-zero, non-None, non-empty)."""
    for v in values:
        if v is not None and v != 0 and v != "":
            return True
    return False


if st.button("🔍 Run Diagnosis", type="primary", use_container_width=True):
    gases = GasRecord(co=co, co2=co2, hc=hc, o2=o2, nox=nox,
                       lambda_sensor=lambda_sensor)

    # L2 — High-idle gas: present if any field is non-zero
    _has_high = _any_nonzero(hi_co, hi_co2, hi_hc, hi_o2, hi_lambda, hi_nox)
    gases_high = GasRecord(
        co=hi_co, co2=hi_co2, hc=hi_hc, o2=hi_o2,
        nox=hi_nox, lambda_sensor=hi_lambda,
    ) if _has_high else GasRecord()

    # O2 upstream sentinel — 0.45 is the default (untouched)
    _O2_UP_DEFAULT = 0.45
    _l3_o2_up = l3_o2_up if l3_o2_up != _O2_UP_DEFAULT else None
    _l4_o2_up = l4_o2_up_hi if l4_o2_up_hi != _O2_UP_DEFAULT else None
    _ff_o2_up = ff_o2_up if ff_o2_up != _O2_UP_DEFAULT else None

    # L3 — Low-idle OBD + DTCs
    if _any_nonzero(l3_stft_b1, l3_ltft_b1, l3_stft_b2, l3_ltft_b2,
                    l3_o2_dn, l3_rpm, l3_load, l3_maf, l3_map, l3_ect) \
       or _l3_o2_up is not None:
        obd_low = OBDRecord(
            stft_b1=l3_stft_b1, ltft_b1=l3_ltft_b1,
            stft_b2=l3_stft_b2, ltft_b2=l3_ltft_b2,
            o2_upstream=_l3_o2_up, o2_downstream=l3_o2_dn,
            rpm=l3_rpm, calc_load=l3_load,
            maf=l3_maf, map=l3_map, ect=l3_ect,
        )
    else:
        obd_low = OBDRecord()

    # L5 — High-idle OBD (Live PIDs, deferred v1.1)
    if _any_nonzero(l4_stft_b1_hi, l4_ltft_b1_hi, l4_stft_b2_hi, l4_ltft_b2_hi,
                    l4_o2_dn_hi) or _l4_o2_up is not None:
        obd_high = OBDRecord(
            stft_b1=l4_stft_b1_hi, ltft_b1=l4_ltft_b1_hi,
            stft_b2=l4_stft_b2_hi, ltft_b2=l4_ltft_b2_hi,
            o2_upstream=_l4_o2_up, o2_downstream=l4_o2_dn_hi,
        )
    else:
        obd_high = OBDRecord()

    # DTCs
    dtc_list = [c.strip().upper() for c in dtc_input.replace(",", " ").split() if c.strip()]
    dtcs = DTCSet(codes=dtc_list)

    # L4 — Freeze Frame (deferred v1.1)
    if _any_nonzero(ff_calc_load, ff_ect, ff_iat, ff_rpm, ff_speed,
                    ff_map, ff_maf, ff_throttle, ff_stft_b1, ff_ltft_b1,
                    ff_stft_b2, ff_ltft_b2, ff_o2_dn, ff_ignition,
                    ff_baro, ff_fuel_rail, ff_egr) \
       or ff_fuel_status != "CL" or _ff_o2_up is not None:
        freeze_frame = FreezeFrameRecord(
            fuel_status=ff_fuel_status,
            calc_load=ff_calc_load, ect=ff_ect, iat=ff_iat,
            rpm=ff_rpm, speed=ff_speed,
            map=ff_map, maf=ff_maf,
            throttle=ff_throttle,
            stft_b1=ff_stft_b1, ltft_b1=ff_ltft_b1,
            stft_b2=ff_stft_b2, ltft_b2=ff_ltft_b2,
            o2_upstream=_ff_o2_up, o2_downstream=ff_o2_dn,
            ignition_advance=ff_ignition,
            barometric_pressure=ff_baro,
            fuel_rail_pressure=ff_fuel_rail,
            commanded_egr=ff_egr,
        )
    else:
        freeze_frame = FreezeFrameRecord()

    context = VehicleContext(
        fuel_type=fuel_engine,
        emission_class=emission_class_internal,
        codes_cleared=codes_cleared_val,
        engine_temp=engine_temp_val,
        induction_type=induction_val,
        primary_symptom=primary_symptom_val,
        mileage_bracket=mileage_bracket_val,
        vehicle_brand=st.session_state.get("vin_brand"),
        displacement_cc=st.session_state.get("vin_displacement_cc"),
        _emission_class_pinned=(emission_class_internal != "euro4"),
    )

    payload = DiagnosticInput(
        gases=gases,
        gases_high=gases_high,
        obd_low=obd_low,
        obd_high=obd_high,
        dtcs=dtcs,
        freeze_frame=freeze_frame,
        context=context,
    )

    try:
        result = diagnose_layered(payload)
    except Exception as exc:
        st.error(f"❌ Diagnostic engine failed: {exc}")
        with st.expander("🔬 Technical Details"):
            import traceback as _tb
            st.code(_tb.format_exc())
            st.json({
                "fuel_engine": fuel_engine,
                "context": {
                    "emission_class": context.emission_class,
                    "fuel_type": context.fuel_type,
                    "codes_cleared": context.codes_cleared,
                    "engine_temp": context.engine_temp,
                    "induction_type": context.induction_type,
                    "primary_symptom": context.primary_symptom,
                },
                "payload_channels": {
                    "gases": payload.gases.is_present(),
                    "gases_high": payload.gases_high.is_present(),
                    "obd_low": payload.obd_low.is_present(),
                    "obd_high": payload.obd_high.is_present(),
                    "dtcs": payload.dtcs.is_present(),
                    "freeze_frame": payload.freeze_frame.is_present(),
                },
            })
        st.stop()

    if result.get("state") == "invalid_input":
        st.error(f"Input Error: {result['validation_error']}")
        fallback = result.get("fallback_top_3")
        if fallback:
            st.markdown(
                '<div class="dx-state-panel dx-state-invalid">'
                '<div class="dx-state-title">'
                'Fallback candidates (from remaining valid channels)'
                '</div><div class="dx-fallback-list">',
                unsafe_allow_html=True,
            )
            for fb in fallback:
                fid = fb.get("fault", "unknown")
                fconf = float(fb.get("confidence", 0.0))
                label = NODE_LABELS.get(fid, fid.replace("_", " ").title())
                st.caption(f"• {label} — {fconf:.1%}")
            st.markdown('</div></div>', unsafe_allow_html=True)
        st.stop()

    # Audit fix #2 (lambda guard): validate engine-returned lambda before use.
    _raw_lam = result.get("lambda_calculated", 1.0)
    try:
        calc_lambda_val = float(_raw_lam)
        if calc_lambda_val != calc_lambda_val or calc_lambda_val in (
                float("inf"), float("-inf")):
            calc_lambda_val = 1.0
    except (TypeError, ValueError):
        calc_lambda_val = 1.0
    delta = abs(lambda_sensor - calc_lambda_val)

    st.header("📋 Diagnostic Results")

    # ── M1.5 Thermal Gate (soft warning, ported from v2 §6.7) ────────────────
    # Cold-engine chemistry is unreliable: cold-start enrichment, inactive
    # catalyst, and choke-mode trims create false-positive symptoms. We do
    # NOT block diagnosis (v1 keeps optional channels), only flag reliability.
    if freeze_frame.ect is not None and freeze_frame.ect < 75:
        st.warning(
            f"⚠️ Engine not fully warm (FF ECT = {freeze_frame.ect}°C). "
            "Cold-start enrichment and an inactive catalyst can produce "
            "false rich/lean symptoms. For best accuracy, warm the engine "
            "to ≥ 75°C and re-test."
        )

    # ── Vehicle Reference Panel ─────────────────────────────────────────────
    _vref_data = result.get("vehicle_ref")
    if _vref_data:
        _euro = _vref_data.get("vref_euro_norm", "").upper()
        _ec   = _vref_data.get("vref_emission_class", "")
        _n    = _vref_data.get("vref_sample_count", 0)
        _q    = _vref_data.get("vref_match_quality", "")
        _co_r = _vref_data.get("vref_ref_co")
        _hc_r = _vref_data.get("vref_ref_hc")
        _nox_r = _vref_data.get("vref_ref_nox")
        _co2_r = _vref_data.get("vref_ref_co2")
        _co_t = _vref_data.get("vref_co_threshold")
        _hc_t = _vref_data.get("vref_hc_threshold")
        _nox_t = _vref_data.get("vref_nox_threshold")
        with st.expander(
            f"📂 COC Reference: {_vref_data.get('vref_brand','')} · {_euro} · {_n:,} records ({_q} match)",
            expanded=False,
        ):
            rc1, rc2, rc3, rc4 = st.columns(4)
            with rc1:
                st.metric("Ref CO", f"{_co_r}%" if _co_r else "—",
                          help="COC certified CO at idle")
                st.metric("Threshold CO (3×)", f"{_co_t}%" if _co_t else "—")
            with rc2:
                st.metric("Ref HC", f"{_hc_r} ppm" if _hc_r else "—")
                st.metric("Threshold HC (3×)", f"{_hc_t} ppm" if _hc_t else "—")
            with rc3:
                st.metric("Ref NOx", f"{_nox_r} ppm" if _nox_r else "—")
                st.metric("Threshold NOx (3×)", f"{_nox_t} ppm" if _nox_t else "—")
            with rc4:
                st.metric("Ref CO₂", f"{_co2_r} g/km" if _co2_r else "—")
                st.metric("Euro norm", _euro or "—")
            st.caption(
                "Reference values are medians of manufacturer COC (Certificate of Conformity) "
                "figures from Slovenian vehicle registration data. Thresholds = 3× the COC reference."
            )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Calculated λ", f"{calc_lambda_val:.3f}")
    with m2:
        st.metric("Measured λ", f"{lambda_sensor:.3f}")
    with m3:
        st.metric("Lambda Δ", f"{delta:.3f}")
    with m4:
        st.metric("AFR (stoich)", f"{fuel_stoich:.1f}:1")

    # ── High-idle lambda deviation from COC target ──────────────────────────
    _hi_lam_measured = gases_high.lambda_sensor if gases_high.is_present() else None
    _hi_lam_target = _vref_data.get("vref_ref_high_idle_lambda") if _vref_data else None
    if (_hi_lam_measured is not None and _hi_lam_measured > 0
            and _hi_lam_target is not None):
        _lam_dev = abs(_hi_lam_measured - _hi_lam_target)
        if _lam_dev > 0.02:
            st.caption(
                f"Measured high-idle λ deviates from COC target by "
                f"{_lam_dev:.3f} — possible timing/VVT or sensor bias."
            )

    top_fault = result.get("top_fault", "unknown")
    confidence = float(result.get("confidence", 0.0))
    repair = result.get("repair", "")
    priority = int(result.get("priority", 0) or 0)
    layers = result.get("evidence_layers_used", [])

    severity_color = "red" if confidence >= 0.5 else "orange" if confidence >= 0.25 else "green"
    st.markdown(
        f"<h2 style='color:{severity_color};'>🛠️ {top_fault.replace('_', ' ').title()}</h2>",
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Priority", priority if priority else "—")
    with s2:
        st.metric("Confidence", f"{confidence:.0%}")
    with s3:
        st.metric("Layers used", " → ".join(layers) if layers else "L1")

    # Pass D — confidence scaler message
    channels_present = result.get("channels_present", 0)
    if channels_present < 6:
        st.info(
            f"Diagnosis based on {channels_present} of 6 channels "
            f"— confidence adjusted accordingly."
        )

    if repair:
        st.success(f"**Recommended Action:** {repair}")

    # ── Output-state rendering (PRD Feat 8, HLD §7.5.3) ──────────────────
    st.subheader("🔬 Differential Diagnosis")
    top_candidates = result.get("top_candidates", [])
    active_symptoms = result.get("active_symptoms", [])

    if top_candidates:
        # ── named_fault: render top-K candidate cards ─────────────────
        for c in top_candidates:
            rank = int(c.get("rank", 1))
            fault_id = c.get("fault", "unknown")
            confidence = float(c.get("confidence", 0.0))
            promoted = bool(c.get("promoted", False))
            evidence = c.get("evidence", [])

            label = NODE_LABELS.get(fault_id, fault_id.replace("_", " ").title())

            card_class = (
                "dx-card-top1" if rank == 1
                else "dx-card-top2" if rank == 2
                else "dx-card-top3" if rank == 3
                else ""
            )
            name_class = "dx-fault-name-top1" if rank == 1 else ""
            bar_fill_class = "" if rank == 1 else "dx-confidence-bar-fill-secondary"
            badge_html = (
                '<span class="dx-badge">&#x2B06; Promoted &mdash; '
                'specific over generic</span>'
                if promoted else ""
            )

            evidence_html = ""
            if evidence:
                items = "".join(
                    f"<li>{e.replace('_', ' ').title()}</li>" for e in evidence
                )
                evidence_html = (
                    f'<details><summary class="dx-evidence-summary">'
                    f'Why this fault?</summary>'
                    f'<ul class="dx-evidence">{items}</ul></details>'
                )

            conf_pct = min(confidence * 100.0, 100.0)

            card_html = (
                f'<div class="dx-card {card_class}">'
                f'<div class="dx-card-header">'
                f'<span class="dx-fault-name {name_class}">{label}</span>'
                f'<span class="dx-confidence">{conf_pct:.1f}% confidence</span>'
                f'{badge_html}'
                f'</div>'
                f'<div class="dx-confidence-bar">'
                f'<div class="dx-confidence-bar-fill {bar_fill_class}" '
                f'style="width:{conf_pct:.1f}%;"></div>'
                f'</div>'
                f'{evidence_html}'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

    elif result.get("state") == "insufficient_evidence":
        # ── insufficient_evidence: "we need more data" panel ──────────
        st.markdown(
            '<div class="dx-state-panel dx-state-insufficient">'
            '<div class="dx-state-title">'
            '&#x1F50D; We Need More Data'
            '</div>'
            '<p>The available evidence is too thin to narrow the diagnosis '
            'to a single fault with confidence. Try entering data from '
            'more stages (L2 high-idle gas, L3 DTCs, or L4 freeze frame).</p>',
            unsafe_allow_html=True,
        )
        if active_symptoms:
            st.markdown(
                '<div class="dx-state-symptoms">'
                '<strong>Most active symptoms detected:</strong></div>',
                unsafe_allow_html=True,
            )
            for sym in active_symptoms[:10]:
                sym_label = sym.replace("_", " ").title()
                st.caption(f"• {sym_label}")
        st.markdown('</div>', unsafe_allow_html=True)

    elif result.get("state") == "invalid_input":
        # ── invalid_input (defensive — normally caught by early exit) ─
        st.error("&#x26A0;&#xFE0F; Input Issue &mdash; Please Re-check")
        reasons = result.get("warnings", [result.get("validation_error", "")])
        for reason in reasons:
            if reason:
                st.warning(reason)
        fallback = result.get("fallback_top_3")
        if fallback:
            st.markdown(
                '<div class="dx-state-panel dx-state-invalid">'
                '<div class="dx-state-title">'
                'Fallback candidates (from remaining valid channels)'
                '</div><div class="dx-fallback-list">',
                unsafe_allow_html=True,
            )
            for fb in fallback:
                fid = fb.get("fault", "unknown")
                fconf = float(fb.get("confidence", 0.0))
                flabel = NODE_LABELS.get(fid, fid.replace("_", " ").title())
                st.caption(f"• {flabel} — {fconf:.1%}")
            st.markdown('</div></div>', unsafe_allow_html=True)

    else:
        # No candidates and unrecognised state — fallback to all_probs
        probs = result.get("all_probs", {})
        top_n = list(probs.items())[:5]
        if top_n:
            df_diff = pd.DataFrame(
                [{"Fault": k.replace("_", " ").title(), "Probability": f"{v:.1%}"}
                 for k, v in top_n]
            )
            st.table(df_diff)

    # Confidence gauge
    st.subheader("📊 Top-fault Confidence")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        title={"text": top_fault.replace("_", " ").title()},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 25], "color": "lightgray"},
                {"range": [25, 50], "color": "orange"},
                {"range": [50, 100], "color": "green"},
            ],
        },
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Layered Confidence Trajectory
    trajectory = result.get("layer_trajectory", [])
    if trajectory:
        st.subheader("📈 Layered Confidence Trajectory")
        traj_x = [t[0] for t in trajectory]
        traj_y = [float(t[1].get("confidence", 0.0)) * 100 for t in trajectory]
        traj_top = [t[1].get("top_fault", "") for t in trajectory]
        fig_traj = go.Figure()
        fig_traj.add_trace(go.Scatter(
            x=traj_x, y=traj_y, mode="lines+markers",
            text=traj_top, hovertemplate="%{x}: %{y:.1f}%% — %{text}",
            name="Top-fault confidence",
        ))
        fig_traj.update_layout(
            xaxis_title="Layer",
            yaxis_title="Confidence (%)",
            yaxis=dict(range=[0, 100]),
        )
        st.plotly_chart(fig_traj, use_container_width=True)

    with st.expander("🔬 Technical Details"):
        st.json({
            "top_fault": top_fault,
            "confidence": confidence,
            "evidence_layers_used": layers,
            "active_symptoms": result.get("active_symptoms", []),
            "lambda_calculated": calc_lambda_val,
            "lambda_measured": lambda_sensor,
            "lambda_delta": delta,
            "fuel_engine": fuel_engine,
            "context": {
                "emission_class": context.emission_class,
                "fuel_type": context.fuel_type,
                "codes_cleared": context.codes_cleared,
                "engine_temp": context.engine_temp,
                "mileage_bracket": context.mileage_bracket,
                "oil_consumption": context.oil_consumption,
                "ignition_age": context.ignition_age,
                "induction_type": context.induction_type,
                "altitude_band": context.altitude_band,
                "primary_symptom": context.primary_symptom,
                "driver_symptoms": context.driver_symptoms,
            },
            "warnings": result.get("warnings", []),
        })

    # Holy Grail — Lambda vs RPM
    st.subheader("📈 Holy Grail — Lambda vs RPM")
    rpm = list(range(800, 3500, 200))
    measured = [lambda_sensor + (0.01 if r < 2000 else -0.02) for r in rpm]
    calculated = [calc_lambda_val] * len(rpm)
    df = pd.DataFrame({"RPM": rpm, "Measured Lambda": measured,
                       "Calculated Lambda": calculated})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["RPM"], y=df["Measured Lambda"],
                             mode="lines+markers", name="Measured"))
    fig.add_trace(go.Scatter(x=df["RPM"], y=df["Calculated Lambda"],
                             mode="lines", name="Calculated"))
    fig.add_hrect(y0=0.98, y1=1.02, line_width=0, fillcolor="green",
                  opacity=0.1, annotation_text="Stoich Zone")
    fig.update_layout(xaxis_title="RPM", yaxis_title="Lambda",
                      hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Built with Bretschneider formula | 4D Diagnostic System | krici pepsi")
