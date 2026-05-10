"""Streamlit UI for the 4D Petrol Diagnostic Engine V2.

Stage 0-4 progressive disclosure.  All fields derive from DiagnosticInput (L17).
Backward-chaining checkbox defaults off (R3 opt-in).  Three result-state visual
treatments: named_fault (green), insufficient_evidence (amber), invalid_input (red).
PDF export via fpdf2.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import streamlit as st
from fpdf import FPDF

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

# Engine imports after path setup — required for repo-relative resolution.
from engine.v2.input_model import (  # noqa: E402
    DiagnosticInput,
    FreezeFrameRecord,
    GasRecord,
    OBDRecord,
    VehicleContext,
)
from engine.v2.pipeline import diagnose  # noqa: E402

logger = logging.getLogger(__name__)

# ── constants ──

MY_MIN: int = 1990   # source: v2-design-rules R6 era buckets
MY_MAX: int = 2020
DEFAULT_MY: int = 2005
DEFAULT_DISPLACEMENT: int = 2000

STATE_COLOR: dict[str, str] = {
    "named_fault": "#2e7d32",
    "insufficient_evidence": "#e65100",
    "invalid_input": "#c62828",
}
STATE_BG: dict[str, str] = {
    "named_fault": "#e8f5e9",
    "insufficient_evidence": "#fff3e0",
    "invalid_input": "#ffebee",
}
STATE_ICON: dict[str, str] = {
    "named_fault": ":white_check_mark:",
    "insufficient_evidence": ":warning:",
    "invalid_input": ":no_entry:",
}


# ── session state init ──

_KEYS: dict[str, Any] = {
    "stage": 0,
    "result": None,
    # Stage 0 — vehicle context
    "brand": "",
    "model": "",
    "engine_code": "",
    "displacement_cc": DEFAULT_DISPLACEMENT,
    "my": DEFAULT_MY,
    # Stage 1 — gas
    "analyser_type": "5-gas",
    "include_high_idle": False,
    "gas_idle_co": 0.0,
    "gas_idle_hc": 0,
    "gas_idle_co2": 0.0,
    "gas_idle_o2": 0.0,
    "gas_idle_nox": 0.0,
    "gas_idle_lambda": 1.0,
    "gas_high_co": 0.0,
    "gas_high_hc": 0,
    "gas_high_co2": 0.0,
    "gas_high_o2": 0.0,
    "gas_high_nox": 0.0,
    "gas_high_lambda": 1.0,
    # Stage 2 — digital
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
    # Stage 3
    "backward_chaining": False,
}

for _key, _val in _KEYS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val


# ── helpers ─────────────────────────────────────────────────────────────────


def _build_diagnostic_input() -> DiagnosticInput:
    """Assemble DiagnosticInput from session-state values (L17 compliance)."""
    vehicle = VehicleContext(
        brand=st.session_state.brand,
        model=st.session_state.model,
        engine_code=st.session_state.engine_code,
        displacement_cc=st.session_state.displacement_cc,
        my=st.session_state.my,
    )

    analyser_type: Any = st.session_state.analyser_type
    is_5gas = analyser_type == "5-gas"

    gas_idle = GasRecord(
        co_pct=st.session_state.gas_idle_co,
        hc_ppm=st.session_state.gas_idle_hc,
        co2_pct=st.session_state.gas_idle_co2,
        o2_pct=st.session_state.gas_idle_o2,
        nox_ppm=st.session_state.gas_idle_nox if is_5gas else None,
        lambda_analyser=st.session_state.gas_idle_lambda if is_5gas else None,
    )

    gas_high: GasRecord | None = None
    if st.session_state.include_high_idle:
        gas_high = GasRecord(
            co_pct=st.session_state.gas_high_co,
            hc_ppm=st.session_state.gas_high_hc,
            co2_pct=st.session_state.gas_high_co2,
            o2_pct=st.session_state.gas_high_o2,
            nox_ppm=st.session_state.gas_high_nox if is_5gas else None,
            lambda_analyser=st.session_state.gas_high_lambda if is_5gas else None,
        )

    obd: OBDRecord | None = None
    if st.session_state.include_obd:
        obd = OBDRecord(
            stft_b1=_none_if_zero_f(st.session_state.obd_stft_b1),
            stft_b2=_none_if_zero_f(st.session_state.obd_stft_b2),
            ltft_b1=_none_if_zero_f(st.session_state.obd_ltft_b1),
            ltft_b2=_none_if_zero_f(st.session_state.obd_ltft_b2),
            map_kpa=_none_if_zero_f(st.session_state.obd_map),
            maf_gs=_none_if_zero_f(st.session_state.obd_maf),
            rpm=_none_if_zero_i(st.session_state.obd_rpm),
            ect_c=_none_if_zero_f(st.session_state.obd_ect),
            iat_c=_none_if_zero_f(st.session_state.obd_iat),
            fuel_status=st.session_state.obd_fuel_status or None,
            o2_voltage_b1=_none_if_zero_f(st.session_state.obd_o2v_b1),
            o2_voltage_b2=_none_if_zero_f(st.session_state.obd_o2v_b2),
            obd_lambda=_none_if_zero_f(st.session_state.obd_lambda),
            vvt_angle=_none_if_zero_f(st.session_state.obd_vvt),
            fuel_pressure_kpa=_none_if_zero_f(
                st.session_state.obd_fuel_pressure),
            baro_kpa=_none_if_zero_f(st.session_state.obd_baro),
            evap_purge_pct=_none_if_zero_f(st.session_state.obd_evap),
            load_pct=_none_if_zero_f(st.session_state.obd_load),
            tps_pct=_none_if_zero_f(st.session_state.obd_tps),
        )

    ff: FreezeFrameRecord | None = None
    if st.session_state.include_ff:
        ff = FreezeFrameRecord(
            dtc_trigger=st.session_state.ff_dtc_trigger,
            ect_c=_none_if_zero_f(st.session_state.ff_ect),
            rpm=_none_if_zero_i(st.session_state.ff_rpm),
            load_pct=_none_if_zero_f(st.session_state.ff_load),
            map_kpa=_none_if_zero_f(st.session_state.ff_map),
            maf_gs=_none_if_zero_f(st.session_state.ff_maf),
            stft_b1=_none_if_zero_f(st.session_state.ff_stft_b1),
            stft_b2=_none_if_zero_f(st.session_state.ff_stft_b2),
            ltft_b1=_none_if_zero_f(st.session_state.ff_ltft_b1),
            ltft_b2=_none_if_zero_f(st.session_state.ff_ltft_b2),
            speed_kph=_none_if_zero_i(st.session_state.ff_speed),
            iat_c=_none_if_zero_f(st.session_state.ff_iat),
            fuel_status=st.session_state.ff_fuel_status or None,
            o2_voltage_b1=_none_if_zero_f(st.session_state.ff_o2v_b1),
            o2_voltage_b2=_none_if_zero_f(st.session_state.ff_o2v_b2),
            baro_kpa=_none_if_zero_f(st.session_state.ff_baro),
            tps_pct=_none_if_zero_f(st.session_state.ff_tps),
            evap_purge_pct=_none_if_zero_f(st.session_state.ff_evap),
            runtime_s=_none_if_zero_i(st.session_state.ff_runtime),
        )

    dtcs = _parse_dtcs(st.session_state.dtcs_text)

    return DiagnosticInput(
        vehicle_context=vehicle,
        dtcs=dtcs,
        analyser_type=analyser_type,
        gas_idle=gas_idle,
        gas_high=gas_high,
        obd=obd,
        freeze_frame=ff,
    )


def _none_if_zero_f(value: float) -> float | None:
    """Return None for zero float values so optional fields stay optional."""
    return value if value != 0.0 else None


def _none_if_zero_i(value: int) -> int | None:
    """Return None for zero int values so optional fields stay optional."""
    return value if value != 0 else None


def _parse_dtcs(text: str) -> list[str]:
    """Parse DTCs from comma- or whitespace-separated text."""
    if not text.strip():
        return []
    tokens = text.replace(",", " ").split()
    return [t.strip().upper() for t in tokens if t.strip()]


# ── PDF export ──────────────────────────────────────────────────────────────


def _pdf_cell(pdf: FPDF, text: str, **kw: Any) -> None:
    """Shorthand for pdf.cell with standard new-line options."""
    pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT", **kw)


def generate_pdf(result: dict) -> bytes:
    """Generate a PDF diagnostic report from the result dict (R9 shape).

    Returns:
        PDF file contents as bytes.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "4D Petrol Diagnostic Report", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    _pdf_cell(pdf, "Vehicle Context")
    pdf.set_font("Helvetica", "", 10)
    _pdf_cell(pdf, f"Brand: {st.session_state.brand}")
    _pdf_cell(pdf, f"Model: {st.session_state.model}")
    _pdf_cell(pdf, f"Engine Code: {st.session_state.engine_code}")
    _pdf_cell(pdf,
              f"Displacement: {st.session_state.displacement_cc} cc")
    _pdf_cell(pdf, f"Model Year: {st.session_state.my}")
    pdf.ln(4)

    state = result.get("state", "unknown")
    pdf.set_font("Helvetica", "B", 12)
    _pdf_cell(pdf, f"Result: {state}")
    pdf.set_font("Helvetica", "", 10)

    primary = result.get("primary")
    if primary is not None:
        fid = primary.get("fault_id", "N/A")
        conf = primary.get("confidence", 0)
        raw = primary.get("raw_score", 0)
        _pdf_cell(pdf, f"Primary Fault: {fid}")
        _pdf_cell(pdf, f"Confidence: {conf:.2f}")
        _pdf_cell(pdf, f"Raw Score: {raw:.4f}")
        root_cause = primary.get("root_cause")
        if root_cause is not None:
            _pdf_cell(pdf, f"Root Cause: {root_cause}")

    alternatives = result.get("alternatives", [])
    if alternatives:
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 10)
        _pdf_cell(pdf, "Alternatives:")
        pdf.set_font("Helvetica", "", 10)
        for alt in alternatives:
            alt_id = alt.get("fault_id", "N/A")
            alt_score = alt.get("raw_score", 0)
            _pdf_cell(pdf, f"- {alt_id} (score: {alt_score:.4f})")

    warnings = result.get("validation_warnings", [])
    if warnings:
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 10)
        _pdf_cell(pdf, "Validation Warnings:")
        pdf.set_font("Helvetica", "", 10)
        for w in warnings:
            cat = w.get("category", "?")
            msg = w.get("message", "")
            _pdf_cell(pdf, f"- [{cat}] {msg}")

    next_steps = result.get("next_steps", [])
    if next_steps:
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 10)
        _pdf_cell(pdf, "Recommended Next Steps:")
        pdf.set_font("Helvetica", "", 10)
        for ns in next_steps:
            evidence = ns.get("evidence", "unknown")
            lift = ns.get("expected_lift", 0.0)
            _pdf_cell(pdf,
                      f"- Gather {evidence} (expected lift: {lift:.2f})")

    return bytes(pdf.output())


# ── stage renderers ─────────────────────────────────────────────────────────


def _render_stage_0() -> None:
    """Stage 0 — Vehicle Context."""
    st.subheader("Stage 0: Vehicle Context")
    st.caption(
        "All fields required for VIN-free vehicle identification "
        "(vref.db lookup)."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Brand", key="brand", placeholder="e.g. BMW, Toyota")
        st.text_input("Model", key="model", placeholder="e.g. 325i, Camry")
        st.text_input(
            "Engine Code", key="engine_code",
            placeholder="e.g. M50B25, 2AZ-FE",
        )
    with col2:
        st.number_input(
            "Displacement (cc)", min_value=500, max_value=10000,
            step=100, key="displacement_cc",
        )
        st.number_input(
            "Model Year", min_value=MY_MIN, max_value=MY_MAX,
            step=1, key="my",
        )

    valid = all([
        st.session_state.brand,
        st.session_state.model,
        st.session_state.engine_code,
    ])
    st.button(
        "Next: Gas Data →", key="to_stage_1",
        disabled=not valid, on_click=_advance_stage,
    )


def _render_stage_1() -> None:
    """Stage 1 — Gas Data (idle + optional high-idle)."""
    st.subheader("Stage 1: Exhaust Gas Data")

    st.radio(
        "Analyser Type", options=["5-gas", "4-gas"],
        horizontal=True, key="analyser_type",
    )
    is_5gas = st.session_state.analyser_type == "5-gas"

    st.markdown("#### Idle Gas Reading")
    _render_gas_fields("gas_idle", is_5gas, required=True)

    st.markdown("#### High-Idle Gas Reading")
    st.checkbox(
        "Include high-idle gas reading (recommended for L2 evidence)",
        key="include_high_idle",
    )
    if st.session_state.include_high_idle:
        _render_gas_fields("gas_high", is_5gas, required=False)

    col_a, col_b = st.columns(2)
    with col_a:
        st.button(
            "← Back: Vehicle", key="to_stage_0",
            on_click=_retreat_stage,
        )
    with col_b:
        idle_ok = (
            st.session_state.gas_idle_co != 0.0
            or st.session_state.gas_idle_o2 != 0.0
        )
        st.button(
            "Next: Digital Data →", key="to_stage_2",
            disabled=not idle_ok, on_click=_advance_stage,
        )


def _render_gas_fields(prefix: str, is_5gas: bool, *, required: bool) -> None:
    """Render a gas-record field group bound to session-state keys."""
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input(
            "CO (%)", min_value=0.0, max_value=15.0,
            step=0.01, key=f"{prefix}_co",
        )
        st.number_input(
            "CO₂ (%)", min_value=0.0, max_value=20.0,
            step=0.1, key=f"{prefix}_co2",
        )
    with c2:
        st.number_input(
            "HC (ppm)", min_value=0, max_value=10000,
            step=1, key=f"{prefix}_hc",
        )
        st.number_input(
            "O₂ (%)", min_value=0.0, max_value=25.0,
            step=0.01, key=f"{prefix}_o2",
        )
    with c3:
        if is_5gas:
            st.number_input(
                "NOx (ppm)", min_value=0.0, max_value=5000.0,
                step=1.0, key=f"{prefix}_nox",
            )
            st.number_input(
                "Lambda (analyser)", min_value=0.5, max_value=2.0,
                step=0.001, key=f"{prefix}_lambda",
            )
        else:
            st.caption("NOx: N/A (4-gas)")
            st.caption("Lambda: N/A (4-gas)")


def _render_stage_2() -> None:
    """Stage 2 — Digital Data (DTCs + OBD + Freeze Frame)."""
    st.subheader("Stage 2: Digital Data")

    st.markdown("#### Diagnostic Trouble Codes (DTCs)")
    st.text_input(
        "DTCs (comma-separated)", key="dtcs_text",
        placeholder="e.g. P0171, P0174, P0300",
    )
    parsed = _parse_dtcs(st.session_state.dtcs_text)
    if parsed:
        st.caption(f"{len(parsed)} DTC(s): {' • '.join(parsed)}")

    st.markdown("#### OBD Live Data")
    st.checkbox("Include OBD live data (L3 evidence)", key="include_obd")
    if st.session_state.include_obd:
        _render_obd_fields()

    st.markdown("#### Freeze Frame Data")
    st.checkbox(
        "Include freeze frame data (L4 evidence)", key="include_ff",
    )
    if st.session_state.include_ff:
        _render_ff_fields()

    col_a, col_b = st.columns(2)
    with col_a:
        st.button(
            "← Back: Gas Data", key="to_stage_1b",
            on_click=_retreat_stage,
        )
    with col_b:
        st.button(
            "Next: Run Diagnosis →", key="to_stage_3",
            on_click=_advance_stage,
        )


def _render_obd_fields() -> None:
    """Render OBD live-data inputs."""
    with st.expander("OBD Live Data Fields", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(
                "STFT B1 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="obd_stft_b1",
            )
            st.number_input(
                "STFT B2 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="obd_stft_b2",
            )
            st.number_input(
                "LTFT B1 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="obd_ltft_b1",
            )
            st.number_input(
                "LTFT B2 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="obd_ltft_b2",
            )
            st.number_input(
                "MAP (kPa)", min_value=0.0, max_value=300.0,
                step=1.0, key="obd_map",
            )
            st.number_input(
                "MAF (g/s)", min_value=0.0, max_value=500.0,
                step=0.1, key="obd_maf",
            )
        with c2:
            st.number_input(
                "RPM", min_value=0, max_value=12000,
                step=50, key="obd_rpm",
            )
            st.number_input(
                "ECT (°C)", min_value=-40.0, max_value=150.0,
                step=0.5, key="obd_ect",
            )
            st.number_input(
                "IAT (°C)", min_value=-40.0, max_value=100.0,
                step=0.5, key="obd_iat",
            )
            st.text_input(
                "Fuel Status", key="obd_fuel_status",
                placeholder="e.g. CL, OL, OL_DRIVE, OL_FAULT",
            )
            st.number_input(
                "O₂ Voltage B1 (V)", min_value=0.0, max_value=1.5,
                step=0.01, key="obd_o2v_b1",
            )
            st.number_input(
                "O₂ Voltage B2 (V)", min_value=0.0, max_value=1.5,
                step=0.01, key="obd_o2v_b2",
            )
        with c3:
            st.number_input(
                "OBD Lambda", min_value=0.5, max_value=2.0,
                step=0.001, key="obd_lambda",
            )
            st.number_input(
                "VVT Angle (°)", min_value=-30.0, max_value=60.0,
                step=0.5, key="obd_vvt",
            )
            st.number_input(
                "Fuel Pressure (kPa)", min_value=0.0, max_value=1000.0,
                step=10.0, key="obd_fuel_pressure",
            )
            st.number_input(
                "Barometric (kPa)", min_value=50.0, max_value=110.0,
                step=0.1, key="obd_baro",
            )
            st.number_input(
                "EVAP Purge (%)", min_value=0.0, max_value=100.0,
                step=0.5, key="obd_evap",
            )
            st.number_input(
                "Engine Load (%)", min_value=0.0, max_value=100.0,
                step=0.5, key="obd_load",
            )
            st.number_input(
                "TPS (%)", min_value=0.0, max_value=100.0,
                step=0.5, key="obd_tps",
            )


def _render_ff_fields() -> None:
    """Render freeze frame data inputs."""
    with st.expander("Freeze Frame Data Fields", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input(
                "DTC Trigger", key="ff_dtc_trigger",
                placeholder="e.g. P0171",
            )
            st.number_input(
                "FF ECT (°C)", min_value=-40.0, max_value=150.0,
                step=0.5, key="ff_ect",
            )
            st.number_input(
                "FF RPM", min_value=0, max_value=12000,
                step=50, key="ff_rpm",
            )
            st.number_input(
                "FF Load (%)", min_value=0.0, max_value=100.0,
                step=0.5, key="ff_load",
            )
            st.number_input(
                "FF MAP (kPa)", min_value=0.0, max_value=300.0,
                step=1.0, key="ff_map",
            )
            st.number_input(
                "FF MAF (g/s)", min_value=0.0, max_value=500.0,
                step=0.1, key="ff_maf",
            )
        with c2:
            st.number_input(
                "FF STFT B1 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="ff_stft_b1",
            )
            st.number_input(
                "FF STFT B2 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="ff_stft_b2",
            )
            st.number_input(
                "FF LTFT B1 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="ff_ltft_b1",
            )
            st.number_input(
                "FF LTFT B2 (%)", min_value=-50.0, max_value=50.0,
                step=0.1, key="ff_ltft_b2",
            )
            st.number_input(
                "FF Speed (km/h)", min_value=0, max_value=300,
                step=1, key="ff_speed",
            )
            st.number_input(
                "FF IAT (°C)", min_value=-40.0, max_value=100.0,
                step=0.5, key="ff_iat",
            )
        with c3:
            st.text_input(
                "FF Fuel Status", key="ff_fuel_status",
                placeholder="e.g. CL, OL",
            )
            st.number_input(
                "FF O₂V B1 (V)", min_value=0.0, max_value=1.5,
                step=0.01, key="ff_o2v_b1",
            )
            st.number_input(
                "FF O₂V B2 (V)", min_value=0.0, max_value=1.5,
                step=0.01, key="ff_o2v_b2",
            )
            st.number_input(
                "FF Baro (kPa)", min_value=50.0, max_value=110.0,
                step=0.1, key="ff_baro",
            )
            st.number_input(
                "FF TPS (%)", min_value=0.0, max_value=100.0,
                step=0.5, key="ff_tps",
            )
            st.number_input(
                "FF EVAP (%)", min_value=0.0, max_value=100.0,
                step=0.5, key="ff_evap",
            )
            st.number_input(
                "FF Runtime (s)", min_value=0, max_value=3600,
                step=1, key="ff_runtime",
            )


def _render_stage_3() -> None:
    """Stage 3 — Backward chaining opt-in + diagnosis trigger."""
    st.subheader("Stage 3: Run Diagnosis")

    st.checkbox(
        "Enable backward chaining (suggest next evidence when insufficient)",
        value=False,
        key="backward_chaining",
        help=(
            "When enabled, next_steps[] will populate if the engine "
            "cannot reach a confident diagnosis (R3 opt-in)."
        ),
    )

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.button(
            "← Back: Digital Data", key="to_stage_2b",
            on_click=_retreat_stage,
        )
    with col_b:
        st.button(
            "Run Diagnosis", key="run_diagnosis",
            type="primary", on_click=_run_diagnosis,
        )


def _render_stage_4() -> None:
    """Stage 4 — Results display with 3-state visual treatment."""
    result: dict[str, Any] = st.session_state.result  # type: ignore[assignment]

    if result is None:
        st.warning("No result yet. Click 'Run Diagnosis' on Stage 3.")
        st.button(
            "← Back to Diagnosis", key="to_stage_3b",
            on_click=_retreat_stage,
        )
        return

    state: str = result.get("state", "unknown")
    color = STATE_COLOR.get(state, "#333333")
    bg = STATE_BG.get(state, "#f0f0f0")
    icon = STATE_ICON.get(state, ":grey_question:")

    # ── state banner ──
    st.markdown(
        f"<div style='background-color:{bg}; "
        f"border-left:6px solid {color}; "
        f"padding:16px 20px; border-radius:4px; margin-bottom:16px;'>"
        f"<h3 style='margin:0; color:{color};'>{icon} State: {state}</h3>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── validation warnings ──
    warnings: list[dict] = result.get("validation_warnings", [])
    if warnings:
        expanded = state == "invalid_input"
        with st.expander(
            f":warning: Validation Warnings ({len(warnings)})",
            expanded=expanded,
        ):
            for w in warnings:
                cat = w.get("category", "?")
                msg = w.get("message", "")
                ch = w.get("channel", "")
                st.warning(f"**[Cat {cat}]** {msg} — `{ch}`")

    # ── primary fault ──
    primary: dict | None = result.get("primary")
    if primary is not None:
        st.markdown("### Primary Diagnosis")

        col_a, col_b = st.columns([2, 1])
        with col_a:
            _render_fault_chain(primary, result)
        with col_b:
            _render_confidence_gauge(primary, result)

        # ── alternatives ──
        alternatives: list[dict] = result.get("alternatives", [])
        if alternatives:
            st.markdown("#### Alternative Candidates")
            alt_data = [
                {
                    "Rank": i + 1,
                    "Fault": a.get("fault_id", "?"),
                    "Raw Score": f"{a.get('raw_score', 0):.4f}",
                    "Confidence": f"{a.get('confidence', 0):.2f}",
                    "Tier Delta": f"{a.get('tier_delta', 0):.4f}",
                }
                for i, a in enumerate(alternatives)
            ]
            st.dataframe(
                alt_data, use_container_width=True, hide_index=True,
            )

    else:
        if state == "invalid_input":
            st.error(
                "All input channels were rejected by the Validation Layer. "
                "No diagnosis possible."
            )
        elif state == "insufficient_evidence":
            st.warning(
                "Insufficient evidence to reach a confident diagnosis."
            )

    # ── perception gap ──
    pg: dict | None = result.get("perception_gap")
    if pg is not None and pg.get("fired"):
        pg_type = pg.get("type", "?")
        pg_delta = pg.get("delta_lambda", 0)
        st.info(
            f":mag: **Perception Gap Detected** — "
            f"Type: `{pg_type}`, Delta Lambda: `{pg_delta:.3f}`"
        )

    # ── next steps ──
    next_steps: list[dict] = result.get("next_steps", [])
    if next_steps:
        st.markdown("#### :bulb: Recommended Next Steps")
        for ns in next_steps:
            evidence = ns.get("evidence", "unknown")
            lift = ns.get("expected_lift", 0.0)
            st.markdown(
                f"- Gather **{evidence}** "
                f"(expected score lift: +{lift:.2f})"
            )

    # ── cascading consequences ──
    cascading: list[str] = result.get("cascading_consequences", [])
    if cascading:
        st.markdown(
            "#### :cyclone: Cascading Consequences (Flood Control)"
        )
        for cc in cascading:
            st.markdown(f"- `{cc}`")

    # ── metadata ──
    st.markdown("---")
    st.caption(
        f"Confidence Ceiling: {result.get('confidence_ceiling', 0):.2f}"
    )
    evidence_used: list[str] = (
        primary.get("evidence_layers_used", []) if primary else []
    )
    st.caption(
        f"Evidence Layers Used: "
        f"{', '.join(evidence_used) if evidence_used else 'none'}"
    )

    # ── actions ──
    col_x, col_y, col_z = st.columns([1, 1, 2])
    with col_x:
        st.button(
            "← Back to Diagnosis", key="to_stage_3c",
            on_click=_retreat_stage,
        )
    with col_y:
        pdf_bytes = generate_pdf(result)
        st.download_button(
            label="Export PDF",
            data=pdf_bytes,
            file_name="4d_diagnostic_report.pdf",
            mime="application/pdf",
        )


def _render_fault_chain(primary: dict, result: dict) -> None:
    """Render symptom chain → fault → root cause for the primary diagnosis."""
    fault_id = primary.get("fault_id", "Unknown")
    symptom_chain: list[str] = primary.get("symptom_chain", [])
    root_cause = primary.get("root_cause")

    st.markdown(f"**Fault:** `{fault_id}`")

    if symptom_chain:
        chain_repr = "  →  ".join(f"`{s}`" for s in symptom_chain)
        st.markdown(f"**Symptom Chain:** {chain_repr}")
    else:
        st.caption("(symptom chain populated by forward reasoning)")

    if root_cause is not None:
        st.markdown(
            f"**Root Cause:** `{root_cause}` :star: (score ≥ 0.80)"
        )

    discrim = primary.get("discriminator_satisfied", True)
    promoted = primary.get("promoted_from_parent", False)
    tags = []
    if discrim:
        tags.append("discriminator ✓")
    if promoted:
        tags.append("promoted over parent")
    if tags:
        st.caption(" • ".join(tags))


def _render_confidence_gauge(primary: dict, result: dict) -> None:
    """Render a confidence gauge using Streamlit progress bar."""
    confidence: float = primary.get("confidence", 0.0)
    raw_score: float = primary.get("raw_score", 0.0)
    ceiling: float = result.get("confidence_ceiling", 1.0)

    st.markdown("**Confidence**")
    st.progress(min(confidence, 1.0), text=f"{confidence:.2f}")
    st.caption(f"raw_score: {raw_score:.4f}  |  ceiling: {ceiling:.2f}")


# ── navigation ──────────────────────────────────────────────────────────────


def _advance_stage() -> None:
    """Move to the next stage."""
    st.session_state.stage = min(st.session_state.stage + 1, 4)


def _retreat_stage() -> None:
    """Move to the previous stage."""
    st.session_state.stage = max(st.session_state.stage - 1, 0)


def _run_diagnosis() -> None:
    """Build DiagnosticInput from session state, run diagnose(), store result."""
    try:
        di = _build_diagnostic_input()
        result = diagnose(
            di, backward_chaining=st.session_state.backward_chaining,
        )
        st.session_state.result = result
        st.session_state.stage = 4
    except Exception:
        logger.exception("diagnosis_failed")
        st.error("Diagnosis failed. Check the console for details.")
        st.session_state.result = None


# ── main ────────────────────────────────────────────────────────────────────


def main() -> None:
    """Entry point — render current stage with progressive disclosure."""
    st.title("4D Petrol Diagnostic Engine V2")
    st.caption(
        "Petrol MY 1990–2020  |  Evidence Arbitrator Architecture  |  V2.0"
    )

    # ── progress stepper ──
    stage_labels = [
        "0: Vehicle", "1: Gas Data", "2: Digital",
        "3: Diagnose", "4: Results",
    ]
    current = st.session_state.stage
    step_cols = st.columns(5)
    for i, label in enumerate(stage_labels):
        with step_cols[i]:
            if i < current:
                st.success(label)
            elif i == current:
                st.info(label)
            else:
                st.markdown(f":gray[{label}]")

    st.markdown("---")

    # ── stage router ──
    if current == 0:
        _render_stage_0()
    elif current == 1:
        _render_stage_1()
    elif current == 2:
        _render_stage_2()
    elif current == 3:
        _render_stage_3()
    elif current == 4:
        _render_stage_4()


if __name__ == "__main__":
    main()
