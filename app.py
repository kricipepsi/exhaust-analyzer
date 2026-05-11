"""4D Petrol Diagnostic Engine V2 — Streamlit UI (flat reference layout).

Sidebar uses VIN as primary vehicle entry point. Main area has stacked
L1..L4 expanders. Results pane uses dx-card styling from the V1 reference.
All fields derive from DiagnosticInput (L17). Backward-chaining defaults OFF (R3).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from engine.v2.input_model import (  # noqa: E402
    DiagnosticInput,
    FreezeFrameRecord,
    GasRecord,
    OBDRecord,
    VehicleContext,
)
from engine.v2.pipeline import diagnose  # noqa: E402

# ── page config ──────────────────────────────────────────────────────────

st.set_page_config(
    page_title="4D Petrol Diagnostic Engine",
    page_icon="🔧",
    layout="wide",
)

# ── CSS (lifted from exhaust-analyzer-main/app.py) ───────────────────────

st.markdown(
    """
    <style>
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
    @media (max-width: 640px) {
        .dx-card { padding: 12px; }
        .dx-state-panel { padding: 14px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔧 4D Petrol Diagnostic Engine")
st.markdown(
    "Knowledge graph-based exhaust gas analysis. Enter a VIN or vehicle context "
    "on the left, fill gas readings in the centre, and run a diagnosis."
)

# ── session state init ──────────────────────────────────────────────────

_DEFAULTS: dict[str, Any] = {
    "result": None,
    "vin_input": "",
    "vin_dna": None,
    "brand": "",
    "model": "",
    "engine_code": "",
    "displacement_cc": 2000,
    "my": 2010,
    "vin_autofilled": False,
    "analyser_type": "5-gas",
    "backward_chaining": False,
    # L1 gas idle
    "l1_co": 0.0,
    "l1_co2": 0.0,
    "l1_hc": 0,
    "l1_o2": 0.0,
    "l1_nox": 0.0,
    "l1_lambda": 1.0,
    # L2 gas high
    "include_high_idle": False,
    "l2_co": 0.0,
    "l2_co2": 0.0,
    "l2_hc": 0,
    "l2_o2": 0.0,
    "l2_nox": 0.0,
    "l2_lambda": 1.0,
    # L3 OBD + DTCs
    "dtcs_text": "",
    "include_obd": False,
    "obd_stft_b1": 0.0,
    "obd_stft_b2": 0.0,
    "obd_ltft_b1": 0.0,
    "obd_ltft_b2": 0.0,
    "obd_map": 100.0,
    "obd_maf": 0.0,
    "obd_rpm": 0,
    "obd_ect": 90.0,
    "obd_iat": 25.0,
    "obd_fuel_status": "",
    "obd_o2v_b1": 0.0,
    "obd_o2v_b2": 0.0,
    "obd_lambda": 1.0,
    "obd_vvt": 0.0,
    "obd_fuel_pressure": 0.0,
    "obd_baro": 101.0,
    "obd_evap": 0.0,
    "obd_load": 0.0,
    "obd_tps": 0.0,
    # L4 freeze frame
    "include_ff": False,
    "ff_dtc_trigger": "",
    "ff_ect": 90.0,
    "ff_rpm": 0,
    "ff_load": 0.0,
    "ff_map": 100.0,
    "ff_maf": 0.0,
    "ff_stft_b1": 0.0,
    "ff_stft_b2": 0.0,
    "ff_ltft_b1": 0.0,
    "ff_ltft_b2": 0.0,
    "ff_speed": 0,
    "ff_iat": 25.0,
    "ff_fuel_status": "",
    "ff_o2v_b1": 0.0,
    "ff_o2v_b2": 0.0,
    "ff_baro": 101.0,
    "ff_tps": 0.0,
    "ff_evap": 0.0,
    "ff_runtime": 0,
}

for _key, _val in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val


# ── helpers ─────────────────────────────────────────────────────────────


def _any_nonzero(*values: float) -> bool:
    """True if any value is non-zero (used for L2 gas_high presence)."""
    return any(v != 0.0 for v in values) or any(v != 0 for v in values)


def _build_gas(prefix: str) -> GasRecord:
    """Build a GasRecord from session_state keys prefixed with l1_ or l2_."""
    is_5gas = st.session_state.analyser_type == "5-gas"
    return GasRecord(
        co_pct=float(st.session_state[f"{prefix}_co"]),
        co2_pct=float(st.session_state[f"{prefix}_co2"]),
        hc_ppm=float(st.session_state[f"{prefix}_hc"]),
        o2_pct=float(st.session_state[f"{prefix}_o2"]),
        nox_ppm=float(st.session_state[f"{prefix}_nox"]) if is_5gas else None,
        lambda_analyser=float(st.session_state[f"{prefix}_lambda"]) if is_5gas else None,
    )


def _build_obd() -> OBDRecord | None:
    """Build OBDRecord if include_obd is checked."""
    if not st.session_state.include_obd:
        return None
    s = st.session_state
    return OBDRecord(
        stft_b1=float(s.obd_stft_b1) if s.obd_stft_b1 else None,
        stft_b2=float(s.obd_stft_b2) if s.obd_stft_b2 else None,
        ltft_b1=float(s.obd_ltft_b1) if s.obd_ltft_b1 else None,
        ltft_b2=float(s.obd_ltft_b2) if s.obd_ltft_b2 else None,
        map_kpa=float(s.obd_map) if s.obd_map else None,
        maf_gs=float(s.obd_maf) if s.obd_maf else None,
        rpm=int(s.obd_rpm) if s.obd_rpm else None,
        ect_c=float(s.obd_ect) if s.obd_ect else None,
        iat_c=float(s.obd_iat) if s.obd_iat else None,
        fuel_status=str(s.obd_fuel_status) if s.obd_fuel_status else None,
        o2_voltage_b1=float(s.obd_o2v_b1) if s.obd_o2v_b1 else None,
        o2_voltage_b2=float(s.obd_o2v_b2) if s.obd_o2v_b2 else None,
        obd_lambda=float(s.obd_lambda) if s.obd_lambda else None,
        vvt_angle=float(s.obd_vvt) if s.obd_vvt else None,
        fuel_pressure_kpa=float(s.obd_fuel_pressure) if s.obd_fuel_pressure else None,
        baro_kpa=float(s.obd_baro) if s.obd_baro else None,
        evap_purge_pct=float(s.obd_evap) if s.obd_evap else None,
        load_pct=float(s.obd_load) if s.obd_load else None,
        tps_pct=float(s.obd_tps) if s.obd_tps else None,
    )


def _build_ff() -> FreezeFrameRecord | None:
    """Build FreezeFrameRecord if include_ff is checked."""
    if not st.session_state.include_ff:
        return None
    s = st.session_state
    return FreezeFrameRecord(
        dtc_trigger=str(s.ff_dtc_trigger) if s.ff_dtc_trigger else "",
        ect_c=float(s.ff_ect) if s.ff_ect else None,
        rpm=int(s.ff_rpm) if s.ff_rpm else None,
        load_pct=float(s.ff_load) if s.ff_load else None,
        map_kpa=float(s.ff_map) if s.ff_map else None,
        maf_gs=float(s.ff_maf) if s.ff_maf else None,
        stft_b1=float(s.ff_stft_b1) if s.ff_stft_b1 else None,
        stft_b2=float(s.ff_stft_b2) if s.ff_stft_b2 else None,
        ltft_b1=float(s.ff_ltft_b1) if s.ff_ltft_b1 else None,
        ltft_b2=float(s.ff_ltft_b2) if s.ff_ltft_b2 else None,
        speed_kph=int(s.ff_speed) if s.ff_speed else None,
        iat_c=float(s.ff_iat) if s.ff_iat else None,
        fuel_status=str(s.ff_fuel_status) if s.ff_fuel_status else None,
        o2_voltage_b1=float(s.ff_o2v_b1) if s.ff_o2v_b1 else None,
        o2_voltage_b2=float(s.ff_o2v_b2) if s.ff_o2v_b2 else None,
        baro_kpa=float(s.ff_baro) if s.ff_baro else None,
        tps_pct=float(s.ff_tps) if s.ff_tps else None,
        evap_purge_pct=float(s.ff_evap) if s.ff_evap else None,
        runtime_s=int(s.ff_runtime) if s.ff_runtime else None,
    )


def _build_diagnostic_input() -> DiagnosticInput:
    """Assemble DiagnosticInput from session-state values (L17 compliance)."""
    s = st.session_state
    vehicle = VehicleContext(
        brand=str(s.brand),
        model=str(s.model),
        engine_code=str(s.engine_code),
        displacement_cc=int(s.displacement_cc),
        my=int(s.my),
        vin=str(s.vin_input) if s.vin_input else None,
    )

    dtcs: list[str] = []
    if s.dtcs_text.strip():
        dtcs = [c.strip().upper() for c in s.dtcs_text.split() if c.strip()]

    gas_idle = _build_gas("l1")

    gas_high: GasRecord | None = None
    if s.include_high_idle and _any_nonzero(
        s.l2_co, s.l2_co2, s.l2_hc, s.l2_o2,
        s.l2_nox if s.analyser_type == "5-gas" else 0.0, s.l2_lambda,
    ):
        gas_high = _build_gas("l2")

    analyser_type: Any = s.analyser_type

    return DiagnosticInput(
        vehicle_context=vehicle,
        dtcs=dtcs,
        analyser_type=analyser_type,
        gas_idle=gas_idle,
        gas_high=gas_high,
        obd=_build_obd(),
        freeze_frame=_build_ff(),
    )


# ══════════════════════════════════════════════════════════════════════════
# Sidebar
# ══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.header("⚙️ Vehicle & Options")

    # ── VIN Lookup ──────────────────────────────────────────────────────
    with st.expander("🔍 VIN Lookup", expanded=True):
        vin_input = st.text_input(
            "VIN (17 chars)",
            key="vin_input",
            placeholder="e.g. WVWZZZ1KZAW123456",
        ).strip().upper()

        vin_dna = None
        if len(vin_input) == 17:
            try:
                from engine.v2.vin import resolve as vin_resolve
                vin_dna = vin_resolve(vin_input)
            except Exception:
                vin_dna = None

        if vin_dna and vin_dna.confidence == "high":
            st.success(
                f"✅ {vin_dna.make or ''} · {vin_dna.engine_code or ''} · "
                f"{vin_dna.displacement_l}L · {vin_dna.induction or ''}"
            )
        elif vin_dna and vin_dna.confidence == "partial":
            st.info(f"ℹ️ {vin_dna.make or 'Manufacturer'} identified — engine not decoded")
        elif vin_dna and vin_dna.confidence == "none":
            st.warning("⚠️ VIN not recognised — fill fields manually below.")
        elif len(vin_input) == 17:
            st.caption("Resolving...")

        if (
            st.button("Auto-fill from VIN", key="vin_autofill_btn")
            and vin_dna
            and vin_dna.confidence in ("high", "partial")
        ):
            if vin_dna.make:
                st.session_state.brand = vin_dna.make
            if vin_dna.engine_code:
                st.session_state.engine_code = vin_dna.engine_code
            if vin_dna.displacement_l is not None:
                st.session_state.displacement_cc = int(round(vin_dna.displacement_l * 1000))
            st.session_state.vin_autofilled = True
            st.rerun()

    # ── Vehicle Identification ──────────────────────────────────────────
    vin_success = bool(
        st.session_state.get("vin_autofilled")
        and st.session_state.vin_input
        and len(st.session_state.vin_input) == 17
    )
    with st.expander("🚗 Vehicle Identification", expanded=not vin_success):
        st.text_input("Brand", key="brand", placeholder="e.g. VOLKSWAGEN")
        if st.session_state.vin_autofilled and st.session_state.brand:
            st.caption("auto-filled from VIN")

        st.text_input("Model", key="model", placeholder="e.g. Golf")
        st.text_input("Engine Code", key="engine_code", placeholder="e.g. BSE")
        if st.session_state.vin_autofilled and st.session_state.engine_code:
            st.caption("auto-filled from VIN")

        st.number_input(
            "Displacement (cc)", min_value=0, max_value=10000,
            value=st.session_state.displacement_cc, step=100, key="displacement_cc",
        )
        if st.session_state.vin_autofilled and st.session_state.displacement_cc:
            st.caption("auto-filled from VIN")

        st.number_input(
            "Model Year", min_value=1990, max_value=2020,
            value=st.session_state.my, step=1, key="my",
        )

    # ── Analyser ────────────────────────────────────────────────────────
    with st.expander("🧪 Analyser", expanded=False):
        st.radio(
            "Analyser type",
            options=["5-gas", "4-gas"],
            horizontal=True,
            key="analyser_type",
            help="5-gas includes NOx; 4-gas suppresses NOx and analyser-lambda.",
        )

    # ── Diagnosis Options ──────────────────────────────────────────────
    with st.expander("⚙️ Diagnosis Options", expanded=False):
        st.checkbox(
            "Enable backward chaining",
            value=False,
            key="backward_chaining",
            help="When ON and evidence is insufficient, suggests next diagnostic steps.",
        )

    st.divider()

    # ── Probe Depth Check ───────────────────────────────────────────────
    st.markdown("**🔍 Probe Depth Check**")
    total_co_co2 = float(st.session_state.l1_co) + float(st.session_state.l1_co2)
    if total_co_co2 > 0 and total_co_co2 < 12.0:
        st.warning(
            f"⚠️ Total CO+CO₂ = {total_co_co2:.1f}% is low. "
            "Ensure probe is inserted 30 cm into tailpipe."
        )
    elif total_co_co2 > 0:
        st.success(f"✅ Total CO+CO₂ = {total_co_co2:.1f}% (adequate)")
    else:
        st.caption("Enter L1 CO and CO₂ to check probe depth.")


# ══════════════════════════════════════════════════════════════════════════
# Main area — stacked expanders
# ══════════════════════════════════════════════════════════════════════════

# ── L1: Low Idle Gas ────────────────────────────────────────────────────
with st.expander("📊 L1 — Low Idle Gas", expanded=True):
    is_5gas = st.session_state.analyser_type == "5-gas"
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("CO (%)", min_value=0.0, max_value=15.0, value=0.12,
                        step=0.01, format="%.2f", key="l1_co")
        st.number_input("CO₂ (%)", min_value=0.0, max_value=20.0, value=14.8,
                        step=0.1, format="%.1f", key="l1_co2")
    with c2:
        st.number_input("HC (ppm)", min_value=0, max_value=30000, value=25,
                        step=1, key="l1_hc")
        st.number_input("O₂ (%)", min_value=0.0, max_value=21.0, value=0.25,
                        step=0.01, format="%.2f", key="l1_o2")
    with c3:
        if is_5gas:
            st.number_input("NOx (ppm)", min_value=0, max_value=5000, value=0,
                            step=1, key="l1_nox")
            st.number_input("Lambda (analyser)", min_value=0.50, max_value=2.00,
                            value=1.00, step=0.01, format="%.2f", key="l1_lambda")
        else:
            st.caption("NOx — 4-gas (disabled)")
            st.caption("Lambda — 4-gas (disabled)")

# ── L2: High Idle Gas ───────────────────────────────────────────────────
with st.expander("📊 L2 — High Idle Gas (~2500 RPM)", expanded=False):
    st.checkbox("Include high-idle gas readings", key="include_high_idle")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("CO (%)", min_value=0.0, max_value=15.0, value=0.0,
                        step=0.01, format="%.2f", key="l2_co")
        st.number_input("CO₂ (%)", min_value=0.0, max_value=20.0, value=0.0,
                        step=0.1, format="%.1f", key="l2_co2")
    with c2:
        st.number_input("HC (ppm)", min_value=0, max_value=30000, value=0,
                        step=1, key="l2_hc")
        st.number_input("O₂ (%)", min_value=0.0, max_value=21.0, value=0.0,
                        step=0.01, format="%.2f", key="l2_o2")
    with c3:
        if is_5gas:
            st.number_input("NOx (ppm)", min_value=0, max_value=5000, value=0,
                            step=1, key="l2_nox")
            st.number_input("Lambda (analyser)", min_value=0.50, max_value=2.00,
                            value=1.00, step=0.01, format="%.2f", key="l2_lambda")
        else:
            st.caption("NOx — 4-gas (disabled)")
            st.caption("Lambda — 4-gas (disabled)")

# ── L3: Live PIDs + DTCs ────────────────────────────────────────────────
with st.expander("📈 L3 — Live PIDs + DTCs", expanded=False):
    st.text_area(
        "DTCs (space-separated, e.g. P0420 P0171)",
        key="dtcs_text",
        placeholder="P0420 P0171",
        height=68,
    )
    st.checkbox("Include OBD live data", key="include_obd")
    if st.session_state.include_obd:
        c1, c2, c3 = st.columns(3)
        s = st.session_state
        with c1:
            st.number_input("STFT B1 (%)", value=0.0, step=0.1, key="obd_stft_b1")
            st.number_input("STFT B2 (%)", value=0.0, step=0.1, key="obd_stft_b2")
            st.number_input("LTFT B1 (%)", value=0.0, step=0.1, key="obd_ltft_b1")
            st.number_input("LTFT B2 (%)", value=0.0, step=0.1, key="obd_ltft_b2")
            st.number_input("MAP (kPa)", value=100.0, step=1.0, key="obd_map")
            st.number_input("MAF (g/s)", value=0.0, step=0.1, key="obd_maf")
        with c2:
            st.number_input("RPM", value=0, step=100, key="obd_rpm")
            st.number_input("ECT (°C)", value=90.0, step=1.0, key="obd_ect")
            st.number_input("IAT (°C)", value=25.0, step=1.0, key="obd_iat")
            st.text_input("Fuel Status", key="obd_fuel_status", placeholder="CL")
            st.number_input("O₂ Voltage B1 (V)", value=0.0, step=0.01, key="obd_o2v_b1")
            st.number_input("O₂ Voltage B2 (V)", value=0.0, step=0.01, key="obd_o2v_b2")
        with c3:
            st.number_input("OBD Lambda", value=1.0, step=0.01, key="obd_lambda")
            st.number_input("VVT Angle (°)", value=0.0, step=0.1, key="obd_vvt")
            st.number_input("Fuel Pressure (kPa)", value=0.0, step=1.0, key="obd_fuel_pressure")
            st.number_input("Baro (kPa)", value=101.0, step=0.1, key="obd_baro")
            st.number_input("EVAP Purge (%)", value=0.0, step=0.1, key="obd_evap")
            st.number_input("Load (%)", value=0.0, step=0.1, key="obd_load")
            st.number_input("TPS (%)", value=0.0, step=0.1, key="obd_tps")

# ── L4: Freeze Frame ────────────────────────────────────────────────────
with st.expander("📟 L4 — Freeze Frame", expanded=False):
    st.checkbox("Include freeze frame data", key="include_ff")
    if st.session_state.include_ff:
        st.text_input("DTC Trigger", key="ff_dtc_trigger", placeholder="e.g. P0420")
        c1, c2, c3 = st.columns(3)
        s = st.session_state
        with c1:
            st.number_input("FF ECT (°C)", value=90.0, step=1.0, key="ff_ect")
            st.number_input("FF RPM", value=0, step=100, key="ff_rpm")
            st.number_input("FF Load (%)", value=0.0, step=0.1, key="ff_load")
            st.number_input("FF MAP (kPa)", value=100.0, step=1.0, key="ff_map")
            st.number_input("FF MAF (g/s)", value=0.0, step=0.1, key="ff_maf")
        with c2:
            st.number_input("FF STFT B1 (%)", value=0.0, step=0.1, key="ff_stft_b1")
            st.number_input("FF STFT B2 (%)", value=0.0, step=0.1, key="ff_stft_b2")
            st.number_input("FF LTFT B1 (%)", value=0.0, step=0.1, key="ff_ltft_b1")
            st.number_input("FF LTFT B2 (%)", value=0.0, step=0.1, key="ff_ltft_b2")
            st.number_input("FF Speed (kph)", value=0, step=1, key="ff_speed")
        with c3:
            st.number_input("FF IAT (°C)", value=25.0, step=1.0, key="ff_iat")
            st.text_input("FF Fuel Status", key="ff_fuel_status", placeholder="CL")
            st.number_input("FF O₂V B1 (V)", value=0.0, step=0.01, key="ff_o2v_b1")
            st.number_input("FF O₂V B2 (V)", value=0.0, step=0.01, key="ff_o2v_b2")
            st.number_input("FF Baro (kPa)", value=101.0, step=0.1, key="ff_baro")
            st.number_input("FF TPS (%)", value=0.0, step=0.1, key="ff_tps")
            st.number_input("FF EVAP (%)", value=0.0, step=0.1, key="ff_evap")
            st.number_input("FF Runtime (s)", value=0, step=1, key="ff_runtime")

# ── L5: Deferred ────────────────────────────────────────────────────────
with st.expander("📈 L5 — Live PIDs (deferred v2.1)", expanded=False):
    st.caption("Live PID streaming will be available in v2.1.")

# ── Run Diagnosis button ────────────────────────────────────────────────

st.markdown("---")
run_col1, run_col2 = st.columns([1, 4])
with run_col1:
    run_clicked = st.button("🔍 Run Diagnosis", type="primary", use_container_width=True)

if run_clicked:
    with st.spinner("Running diagnosis pipeline..."):
        try:
            diag_input = _build_diagnostic_input()
            result = diagnose(
                diag_input,
                backward_chaining=st.session_state.backward_chaining,
            )
            st.session_state.result = result
        except Exception as exc:
            st.error(f"Diagnosis failed: {exc}")
            st.session_state.result = None

# ══════════════════════════════════════════════════════════════════════════
# Results pane
# ══════════════════════════════════════════════════════════════════════════

result = st.session_state.get("result")
if result is None:
    st.info("Enter vehicle context and gas readings, then click **Run Diagnosis**.")
else:
    state = result.get("state", "invalid_input")
    primary = result.get("primary")
    alternatives = result.get("alternatives", [])
    warnings = result.get("validation_warnings", [])
    ceiling = result.get("confidence_ceiling", 0.0)
    perception_gap = result.get("perception_gap")
    next_steps = result.get("next_steps", [])
    cascading = result.get("cascading_consequences", [])

    st.markdown("---")
    st.header("📋 Diagnosis Result")

    # 1. State banner
    _state_colors = {
        "named_fault": ("#2e7d32", "#e8f5e9", "✅"),
        "insufficient_evidence": ("#e65100", "#fef7e0", "⚠️"),
        "invalid_input": ("#c62828", "#fce8e6", "🚫"),
    }
    sc = _state_colors.get(state, _state_colors["invalid_input"])
    state_label = state.replace("_", " ").title()
    st.markdown(
        f"""<div class="dx-state-panel"
        style="background:{sc[1]};border:1px solid {sc[0]};">
        <span style="color:{sc[0]};font-weight:600;font-size:1.1em;">
        {sc[2]} {state_label}</span>
        </div>""",
        unsafe_allow_html=True,
    )

    # 2. Validation warnings
    if warnings:
        with st.expander(f"⚠️ Validation Warnings ({len(warnings)})", expanded=bool(warnings)):
            for w in warnings:
                st.warning(f"**[{w.get('channel', '?')}]** {w.get('message', str(w))}")

    # 3. Metric tiles
    if primary:
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.metric("Confidence", f"{primary.get('confidence', 0):.1%}")
        with mc2:
            st.metric("Raw Score", f"{primary.get('raw_score', 0):.3f}")
        with mc3:
            st.metric("Confidence Ceiling", f"{ceiling:.2f}")
        with mc4:
            layers = primary.get("evidence_layers_used", [])
            st.metric("Layers Used", " → ".join(layers) if layers else "—")

    # 4. Primary diagnosis
    if primary and state == "named_fault":
        fault_id = primary.get("fault_id", "Unknown")
        st.markdown(f"<h2 style='color:{sc[0]};'>{fault_id}</h2>", unsafe_allow_html=True)

        symptom_chain = primary.get("symptom_chain", [])
        if symptom_chain:
            st.markdown("**Symptom Chain:** " + " → ".join(symptom_chain))

        root_cause = primary.get("root_cause")
        if root_cause:
            st.markdown(f"**Root Cause:** ★ {root_cause}")

        disc = primary.get("discriminator_tags", [])
        prom = primary.get("promotion_tags", [])
        if disc:
            st.markdown("**Discriminators:** " + ", ".join(disc))
        if prom:
            st.markdown("**Promotions:** " + ", ".join(prom))

    # 5. Differential diagnosis
    if alternatives:
        st.subheader("Differential Diagnosis")
        for idx, alt in enumerate(alternatives):
            css_class = "dx-card-top1" if idx == 0 else ("dx-card-top2" if idx < 3 else "")
            fault_name = alt.get("fault_id", "?")
            conf = alt.get("confidence", 0)
            st.markdown(
                f"""<div class="dx-card {css_class}">
                <strong>{fault_name}</strong>
                <span style="float:right;color:#5f6368;">{conf:.1%}</span>
                </div>""",
                unsafe_allow_html=True,
            )

    # 6. Plotly confidence gauge
    if primary:
        try:
            import plotly.graph_objects as go
            conf_val = primary.get("confidence", 0) * 100
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=conf_val,
                title={"text": "Confidence %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": sc[0]},
                    "steps": [
                        {"range": [0, 25], "color": "#f0f0f0"},
                        {"range": [25, 50], "color": "#ffe0b2"},
                        {"range": [50, 100], "color": "#c8e6c9"},
                    ],
                },
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.caption("Plotly not available — install plotly>=5.14 for confidence gauge.")

    # 7. Perception gap
    if perception_gap and perception_gap.get("fired"):
        st.info(
            f"🔍 **Perception Gap Detected:** {perception_gap.get('summary', '')} "
            f"(Δλ = {perception_gap.get('delta_lambda', 0):.3f})"
        )

    # 8. Next steps
    if next_steps:
        with st.expander("📋 Recommended Next Steps", expanded=True):
            for ns in next_steps:
                st.markdown(f"- **{ns.get('action', ns)}**: {ns.get('rationale', '')}")

    # 9. Cascading consequences
    if cascading:
        with st.expander("🔗 Cascading Consequences", expanded=False):
            for cc in cascading:
                st.markdown(f"- {cc}")

    # 10. Technical details
    with st.expander("🔧 Technical Details", expanded=False):
        st.json(result)

    # 11. Run again
    if st.button("🔄 Run Again", key="run_again_btn"):
        st.session_state.result = None
        st.session_state.vin_autofilled = False
        st.rerun()
