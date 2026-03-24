#!/usr/bin/env python3
"""
Petrol Diagnostic Dashboard - Streamlit UI
4D Diagnostic System with Bretschneider Formula
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import core module
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

import streamlit as st
import plotly.graph_objects as go
import json

# Import core modules
from core.bretschneider import calculate_lambda
from core.catalyst import catalyst_efficiency
from core.validator import validate_gas_data, check_probe_placement
from core.matrix import match_case
from core.reporter import generate_report

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
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("🔧 4D Petrol Diagnostic Engine")
st.markdown(
    "Bretschneider-based exhaust gas analysis with theoretical lambda calculation. "
    "Enter low-idle 5-gas measurements to diagnose engine faults."
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    fuel_label = st.selectbox(
        "Fuel Type",
        options=[
            'E0 - Pure Petrol (0% ethanol)',
            'E5 - Petrol (5% ethanol)',
            'E10 - Standard Petrol (10% ethanol)',
            'E85 - Flex-Fuel (85% ethanol)',
        ],
        index=2,
        help="Select petrol fuel type. This affects Bretschneider stoichiometric constants (Hcv, Ocv, AFR)."
    )
    fuel_type = fuel_label.split(' ')[0].lower()
    cold_engine = st.checkbox(
        "Cold Engine (SAI active)",
        value=False,
        help="Check if engine is cold (<60°C). Secondary Air Injection may affect O2 readings."
    )
    st.divider()
    st.markdown("**Note:** O2 thresholds are relaxed when cold engine is checked.")
    
    # Sponsored ad space – placeholder (AdSense integration pending)
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; margin: 10px 0;">
            <small style="color: #666; font-style: italic;">Sponsored</small>
        </div>
        """,
        unsafe_allow_html=True
    )

# Load knowledge base (cached)
@st.cache_resource
def load_knowledge_base():
    kb_path = Path(__file__).parent / "data" / "expanded_knowledge_base.json"
    with open(kb_path, 'r') as f:
        return json.load(f)

try:
    kb = load_knowledge_base()
except Exception as e:
    st.error(f"Failed to load knowledge base: {e}")
    st.stop()

# Main input form
st.header("📊 Low Idle Gas Measurements")

# Use an expander for the 5-gas inputs to get a clean framed look, matching high idle style
with st.expander("📊 Low Idle Gas Measurements", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        co = st.number_input("CO (%)", min_value=0.0, max_value=10.0, value=0.12, step=0.01, format="%.2f", key="low_co")
        co2 = st.number_input("CO₂ (%)", min_value=0.0, max_value=20.0, value=14.8, step=0.1, format="%.1f", key="low_co2")
        hc = st.number_input("HC (ppm)", min_value=0, max_value=20000, value=25, step=1, key="low_hc")
    with col2:
        o2 = st.number_input("O₂ (%)", min_value=0.0, max_value=20.0, value=0.25, step=0.01, format="%.2f", key="low_o2")
        lambda_sensor = st.number_input("Lambda (sensor)", min_value=0.5, max_value=2.0, value=1.00, step=0.01, format="%.2f", key="low_lambda")
        nox = st.number_input("NOx (ppm)", min_value=0, max_value=5000, value=0, step=1, key="low_nox")
    with col3:
        st.markdown("**Probe Depth Check**")
        total_gas = co + co2
        if total_gas < 12.0:
            st.warning(f"⚠️ Total CO+CO₂ = {total_gas:.1f}% is low. Ensure probe is inserted 30cm into tailpipe.")
        else:
            st.success(f"✅ Total CO+CO₂ = {total_gas:.1f}% (adequate)")

        st.markdown("**Validation**")
        valid, msg = validate_gas_data({
            'co': co, 'co2': co2, 'hc': hc, 'o2': o2, 'lambda': lambda_sensor, 'nox': nox
        })
        if valid:
            st.success(msg)
        else:
            st.error(msg)

# High Idle Gas Measurements (collapsible)
with st.expander("📊 High Idle Gas Measurements (~2500 RPM)", expanded=False):
    st.markdown("Enter gas readings at elevated RPM for differential diagnosis (e.g. vacuum leak detection).")
    hi_col1, hi_col2 = st.columns(2)
    with hi_col1:
        hi_co = st.number_input("CO (%) [High Idle]", min_value=0.0, max_value=10.0, value=0.12, step=0.01, format="%.2f", key="hi_co")
        hi_co2 = st.number_input("CO₂ (%) [High Idle]", min_value=0.0, max_value=20.0, value=14.8, step=0.1, format="%.1f", key="hi_co2")
        hi_hc = st.number_input("HC (ppm) [High Idle]", min_value=0, max_value=20000, value=25, step=1, key="hi_hc")
    with hi_col2:
        hi_o2 = st.number_input("O₂ (%) [High Idle]", min_value=0.0, max_value=20.0, value=0.25, step=0.01, format="%.2f", key="hi_o2")
        hi_lambda = st.number_input("Lambda [High Idle]", min_value=0.5, max_value=2.0, value=1.00, step=0.01, format="%.2f", key="hi_lambda")
        hi_nox = st.number_input("NOx (ppm) [High Idle]", min_value=0, max_value=5000, value=0, step=1, key="hi_nox")
    use_high_idle = st.checkbox("Use high idle data for diagnosis", value=True)

# Tier 3: OBD DTC and Freeze Frame Data
with st.expander("📟 OBD DTC and Freeze Frame Data", expanded=False):
    st.markdown("Enter diagnostic trouble codes and freeze frame snapshot if available.")
    dtc_input = st.text_area("DTC Codes (comma or space separated)", placeholder="P0171, P0420, P0300", key="tier3_dtc")
    
    st.markdown("---")
    st.markdown("**Freeze Frame Parameters**")
    ff_col1, ff_col2, ff_col3 = st.columns(3)
    with ff_col1:
        ff_rpm = st.number_input("Engine RPM", min_value=0, max_value=8000, value=0, step=1, key="ff_rpm")
        ff_speed = st.number_input("Vehicle Speed (km/h)", min_value=0, max_value=300, value=0, step=1, key="ff_speed")
        ff_coolant = st.number_input("Coolant Temp (°C)", min_value=-40, max_value=200, value=0, step=1, key="ff_coolant")
        ff_iat = st.number_input("Intake Air Temp (°C)", min_value=-40, max_value=100, value=0, step=1, key="ff_iat")
    with ff_col2:
        ff_map = st.number_input("MAP (kPa)", min_value=0.0, max_value=200.0, value=0.0, step=0.1, key="ff_map")
        ff_throttle = st.number_input("Throttle Position (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="ff_throttle")
        ff_stft = st.number_input("Short-Term Fuel Trim (%)", min_value=-25.0, max_value=25.0, value=0.0, step=0.1, key="ff_stft")
        ff_ltft = st.number_input("Long-Term Fuel Trim (%)", min_value=-25.0, max_value=25.0, value=0.0, step=0.1, key="ff_ltft")
    with ff_col3:
        ff_o2_b1s1 = st.number_input("O2 B1S1 (V)", min_value=0.0, max_value=1.5, value=0.0, step=0.01, key="ff_o2_b1s1")
        ff_o2_b1s2 = st.number_input("O2 B1S2 (V)", min_value=0.0, max_value=1.5, value=0.0, step=0.01, key="ff_o2_b1s2")
        ff_maf = st.number_input("MAF (g/s)", min_value=0.0, max_value=500.0, value=0.0, step=0.1, key="ff_maf")
        ff_timing = st.number_input("Timing Advance (°BTDC)", min_value=-20.0, max_value=60.0, value=0.0, step=0.1, key="ff_timing")
        ff_lambda = st.number_input("Lambda", min_value=0.5, max_value=2.0, value=1.0, step=0.01, key="ff_lambda")
        ff_cat_temp = st.number_input("Catalyst Temp (°C)", min_value=0, max_value=1200, value=0, step=1, key="ff_cat_temp")

# Tier 4: Live PID Data at Low Idle
with st.expander("📈 Live PID Data (Low Idle)", expanded=False):
    st.markdown("Enter live PID readings at low idle (~750-900 RPM).")
    low_pid_col1, low_pid_col2 = st.columns(2)
    with low_pid_col1:
        low_pid_rpm = st.number_input("Engine RPM", min_value=0, max_value=8000, value=0, step=1, key="low_pid_rpm")
        low_pid_stft = st.number_input("STFT (%)", min_value=-25.0, max_value=25.0, value=0.0, step=0.1, key="low_pid_stft")
        low_pid_ltft = st.number_input("LTFT (%)", min_value=-25.0, max_value=25.0, value=0.0, step=0.1, key="low_pid_ltft")
        low_pid_lambda = st.number_input("Upstream Lambda", min_value=0.5, max_value=2.0, value=1.0, step=0.01, key="low_pid_lambda")
        low_pid_downstream_lambda = st.number_input("Downstream Lambda", min_value=0.5, max_value=2.0, value=1.0, step=0.01, key="low_pid_downstream_lambda")
    with low_pid_col2:
        low_pid_maf = st.number_input("MAF (g/s)", min_value=0.0, max_value=500.0, value=0.0, step=0.1, key="low_pid_maf")
        low_pid_map = st.number_input("MAP (kPa)", min_value=0.0, max_value=200.0, value=0.0, step=0.1, key="low_pid_map")
        low_pid_throttle = st.number_input("Throttle Position (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="low_pid_throttle")

# Tier 5: Live PID Data at High Idle
with st.expander("📈 Live PID Data (High Idle)", expanded=False):
    st.markdown("Enter live PID readings at high idle (~2500-3500 RPM).")
    high_pid_col1, high_pid_col2 = st.columns(2)
    with high_pid_col1:
        high_pid_rpm = st.number_input("Engine RPM", min_value=0, max_value=8000, value=0, step=1, key="high_pid_rpm")
        high_pid_stft = st.number_input("STFT (%)", min_value=-25.0, max_value=25.0, value=0.0, step=0.1, key="high_pid_stft")
        high_pid_ltft = st.number_input("LTFT (%)", min_value=-25.0, max_value=25.0, value=0.0, step=0.1, key="high_pid_ltft")
        high_pid_lambda = st.number_input("Upstream Lambda", min_value=0.5, max_value=2.0, value=1.0, step=0.01, key="high_pid_lambda")
        high_pid_downstream_lambda = st.number_input("Downstream Lambda", min_value=0.5, max_value=2.0, value=1.0, step=0.01, key="high_pid_downstream_lambda")
    with high_pid_col2:
        high_pid_maf = st.number_input("MAF (g/s)", min_value=0.0, max_value=500.0, value=0.0, step=0.1, key="high_pid_maf")
        high_pid_map = st.number_input("MAP (kPa)", min_value=0.0, max_value=200.0, value=0.0, step=0.1, key="high_pid_map")
        high_pid_throttle = st.number_input("Throttle Position (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key="high_pid_throttle")

# Run diagnosis button
if st.button("🔍 Run Diagnosis", type="primary", use_container_width=True):
    # Prepare input dict
    low_idle = {
        'lambda': lambda_sensor,
        'co': co,
        'co2': co2,
        'hc': hc,
        'o2': o2,
        'nox': nox
    }

    # Step 1: Validate (shown above but re-check)
    valid, msg = validate_gas_data(low_idle)
    if not valid:
        st.error(f"Input Error: {msg}")
        st.stop()

    # Step 2: Probe placement warning
    probe_warning = check_probe_placement(co, co2)
    if probe_warning:
        st.warning(probe_warning['message'])

    # Step 3: Bretschneider lambda
    calc_result = calculate_lambda(co, co2, hc, o2, fuel_type)
    calc_lambda = calc_result['lambda']
    afr = calc_result['afr']
    stoich = calc_result['stoich']

    # Step 4: Catalyst efficiency
    cat_eff, cat_status = catalyst_efficiency(low_idle, config=kb.get('catalyst_config'))

    # Step 5: Match case
    high_idle = None
    if use_high_idle:
        high_idle = {
            'co': hi_co, 'co2': hi_co2, 'hc': hi_hc,
            'o2': hi_o2, 'lambda': hi_lambda, 'nox': hi_nox
        }
    
    # Collect additional tier data
    dtc_codes_list = [c.strip() for c in dtc_input.replace(',', ' ').split() if c.strip()]
    freeze_frame_dict = {
        'rpm': ff_rpm,
        'speed': ff_speed,
        'coolant_temp': ff_coolant,
        'iat': ff_iat,
        'map': ff_map,
        'throttle': ff_throttle,
        'stft': ff_stft,
        'ltft': ff_ltft,
        'o2_b1s1': ff_o2_b1s1,
        'o2_b1s2': ff_o2_b1s2,
        'maf': ff_maf,
        'timing': ff_timing,
        'lambda': ff_lambda,
        'cat_temp': ff_cat_temp
    }
    tier4_low_dict = {
        '0C': low_pid_rpm,
        '06': low_pid_stft,
        '07': low_pid_ltft,
        '44': low_pid_lambda,
        'downstream_lambda': low_pid_downstream_lambda,
        '10': low_pid_maf,
        '0B': low_pid_map,
        '11': low_pid_throttle
    }
    tier4_high_dict = {
        '0C': high_pid_rpm,
        '06': high_pid_stft,
        '07': high_pid_ltft,
        '44': high_pid_lambda,
        'downstream_lambda': high_pid_downstream_lambda,
        '10': high_pid_maf,
        '0B': high_pid_map,
        '11': high_pid_throttle
    }
    
    matched_case = match_case(
        low_idle=low_idle,
        calculated_lambda=calc_lambda,
        measured_lambda=lambda_sensor,
        knowledge_base=kb,
        high_idle=high_idle,
        dtc_codes=dtc_codes_list,
        freeze_frame=freeze_frame_dict,
        tier4_low=tier4_low_dict,
        tier4_high=tier4_high_dict
    )

    # Step 6: Generate report
    report = generate_report(
        low_idle=low_idle,
        measured_lambda=lambda_sensor,
        calculated_lambda=calc_lambda,
        cat_eff=cat_eff,
        cat_status=cat_status,
        matched_case=matched_case,
        knowledge_base=kb
    )

    # Display results
    st.header("📋 Diagnostic Results")

    # Key metrics
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("Calculated λ", f"{calc_lambda:.3f}")
    with col_b:
        st.metric("Measured λ", f"{lambda_sensor:.3f}")
    with col_c:
        delta = abs(lambda_sensor - calc_lambda)
        st.metric("Lambda Δ", f"{delta:.3f}")
    with col_d:
        st.metric("AFR", f"{afr:.1f}:1 (stoich {stoich})")

    # Catalyst gauge
    st.subheader("🛢️ Catalyst Efficiency")
    fig_cat = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cat_eff,
        title={'text': f"Efficiency - {cat_status}"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 85], 'color': "orange"},
                {'range': [85, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': cat_eff
            }
        }
    ))
    st.plotly_chart(fig_cat, use_container_width=True)

    # Overall health
    st.subheader("❤️ Overall Health")
    health = report['overall_health']
    health_color = "green" if health >= 80 else "orange" if health >= 60 else "red"
    st.markdown(
        f"<h1 style='text-align: center; color: {health_color};'>{health}/100</h1>",
        unsafe_allow_html=True
    )

    # Verdict and action
    st.subheader("📝 Assessment")
    st.info(f"**{report['assessment']}**")
    st.write(report['verdict'])
    st.success(f"**Recommended Action:** {report['action']}")

    # NOx info
    if nox > 0:
        st.markdown(f"**NOx:** {nox} ppm")
    if report.get('nox_warning'):
        st.warning(f"⚠️ {report['nox_warning']}")

    # Debug expander
    with st.expander("🔬 Technical Details"):
        st.json({
            "calculated_lambda": calc_lambda,
            "measured_lambda": lambda_sensor,
            "lambda_delta": delta,
            "fuel_type": fuel_type,
            "matched_case_id": matched_case['case_id'],
            "base_health": matched_case.get('health_score'),
            "final_health": health,
            "catalyst": {"efficiency": cat_eff, "status": cat_status}
        })

    # Holy Grail Graph (simulated)
    st.subheader("📈 Holy Grail - Lambda vs RPM")
    # Simulate some data points (in real app, would come from history)
    import pandas as pd
    rpm = list(range(800, 3500, 200))
    # Simulate measured lambda with some variation; calculated would be smoother
    measured = [lambda_sensor + (0.01 if r < 2000 else -0.02) for r in rpm]
    calculated = [calc_lambda] * len(rpm)

    df = pd.DataFrame({'RPM': rpm, 'Measured Lambda': measured, 'Calculated Lambda': calculated})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['RPM'], y=df['Measured Lambda'], mode='lines+markers', name='Measured'))
    fig.add_trace(go.Scatter(x=df['RPM'], y=df['Calculated Lambda'], mode='lines', name='Calculated'))
    # Add stoich zone
    fig.add_hrect(y0=0.98, y1=1.02, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Stoich Zone")
    fig.update_layout(
        xaxis_title="RPM",
        yaxis_title="Lambda",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Built with Bretschneider formula | 4D Diagnostic System | krici pepsi")

