"""Append 59 new cases to cases_petrol_master_v6.csv for T-P0-6.
15 freeze-frame-driven + 15 cold-start/non-starter + 10 era-specific +
10 dual-bank + 9 remaining to reach exactly 400 cases.
Real-world provenance — no synthetic gas invented to force output.
"""
from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "cases" / "csv" / "cases_petrol_master_v6.csv"
COLS = [
    "case_id", "description",
    "hc", "co", "co2", "o2", "nox", "lambda_analyser",
    "stft_b1", "ltft_b1", "stft_b2", "ltft_b2", "obd_lambda",
    "o2_upstream_classification", "o2_downstream_voltage",
    "map", "maf", "rpm", "ect", "vehicle_speed", "fuel_pressure",
    "dtcs",
    "ff_ect", "ff_rpm", "ff_load", "ff_map", "ff_stft_b1", "ff_ltft_b1", "ff_dtcs",
    "engine_temp", "primary_symptom", "fuel_type", "induction_type",
    "altitude_band", "emission_class", "mileage_bracket",
    "oil_consumption", "ignition_age",
    "bank_config",
    "expected_top_fault", "expected_top_fault_family",
    "expected_state", "expected_confidence_min", "expected_confidence_max",
    "expected_demotion_note_contains", "expected_perception_gap",
    "reasoning",
    "hc_2500", "co_2500", "co2_2500", "o2_2500", "nox_2500", "lambda_2500",
]
def empty() -> dict[str, str]:
    return {c: "" for c in COLS}
def make_row(
    case_id: str, description: str,
    hc: str, co: str, co2: str, o2: str, nox: str, lambda_analyser: str,
    stft_b1: str, ltft_b1: str,
    obd_lambda: str,
    map_val: str, rpm: str, ect: str,
    dtcs: str,
    bank_config: str,
    expected_top_fault: str, expected_top_fault_family: str,
    expected_state: str, expected_confidence_min: str, expected_confidence_max: str,
    expected_perception_gap: str,
    reasoning: str,
    **kwargs
) -> dict[str, str]:
    r = empty()
    r.update({
        "case_id": case_id, "description": description,
        "hc": hc, "co": co, "co2": co2, "o2": o2, "nox": nox,
        "lambda_analyser": lambda_analyser,
        "stft_b1": stft_b1, "ltft_b1": ltft_b1,
        "obd_lambda": obd_lambda,
        "map": map_val, "rpm": rpm, "ect": ect,
        "dtcs": dtcs,
        "bank_config": bank_config,
        "fuel_type": "petrol",
        "engine_temp": kwargs.get("engine_temp", "normal"),
        "primary_symptom": kwargs.get("primary_symptom", ""),
        "induction_type": kwargs.get("induction_type", ""),
        "emission_class": kwargs.get("emission_class", ""),
        "mileage_bracket": kwargs.get("mileage_bracket", ""),
        "expected_top_fault": expected_top_fault,
        "expected_top_fault_family": expected_top_fault_family,
        "expected_state": expected_state,
        "expected_confidence_min": expected_confidence_min,
        "expected_confidence_max": expected_confidence_max,
        "expected_perception_gap": expected_perception_gap,
        "reasoning": reasoning,
    })
    for k, v in kwargs.items():
        if k in COLS:
            r[k] = v
    return r
CASES: list[dict[str, str]] = []
def add(c: dict[str, str]) -> None:
    CASES.append(c)
# ============================================================
# 15 FREEZE-FRAME-DRIVEN CASES (FF-001 to FF-015)
# ============================================================
# --- FF-001: P0301 + FF idle/low load — misfire at idle confirmed by FF ---
add(make_row(
    "FF-001", "FF: P0301 cyl 1 misfire — FF confirms idle, low CLV, stationary",
    "320", "1.2", "12.5", "2.2", "75", "0.98",
    "+5", "+3", "0.99", "30", "720", "88",
    "P0301",
    "single",
    "Misfire_Cylinder_1", "ignition_fault",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 320 ppm: significant misfire (>250 ppm). CO 1.2%: elevated — partial burn. CO2 12.5%: depressed — incomplete combustion. O2 2.2%: lean — unburned oxygen from dead cylinder. NOx 75 ppm: moderate. Lambda 0.98: near stoich — gas averaging hides dead hole. FF: ECT 88C (warm), RPM 720 (idle), CLV 22%% (idle), vehicle speed 0 (stationary). FF confirms misfire set at warm idle — reproducible in bay without road test. Source: master_freeze_frame_guide.md §3, §5, §6. master_ignition_guide.md §4 (single-cylinder misfire).",
    ff_ect="88", ff_rpm="720", ff_load="22", ff_map="30", ff_stft_b1="+5", ff_ltft_b1="+3", ff_dtcs="P0301",
))
# --- FF-002: P0420 + FF low ECT — catalyst monitor outside enable window ---
add(make_row(
    "FF-002", "FF: P0420 + FF ECT 45C — catalyst monitor invalid, cold set",
    "80", "0.5", "14.0", "0.6", "90", "1.01",
    "-2", "0", "1.01", "31", "740", "89",
    "P0420",
    "single",
    "Catalyst_Efficiency_Below_Threshold_P0420", "catalyst_fault",
    "named_fault", "0.55", "0.75",
    "false",
    "HC 80 ppm: marginal. CO 0.5%%: normal. CO2 14.0%%: near efficient. O2 0.6%%: normal. NOx 90 ppm: moderate. Lambda 1.01: near stoich. FF: ECT 45C, RPM 740, CLV 24%%, vehicle speed 0. P0420 set with FF ECT 45C — below the 70C enable threshold. Per master_freeze_frame_guide.md §4 and master_catalyst_guide.md §3, catalyst monitor requires ECT >= 70C. This DTC set outside enable window — flag dtc_set_outside_enable_window, demote catalyst-failure candidate. Source: master_freeze_frame_guide.md §4 (ECT gate). master_catalyst_guide.md §3 (monitor enable criteria).",
    ff_ect="45", ff_rpm="740", ff_load="24", ff_map="31", ff_stft_b1="-2", ff_ltft_b1="0", ff_dtcs="P0420",
))
# --- FF-003: P0171 + FF CLV 72% — lean under load, valid FF ---
add(make_row(
    "FF-003", "FF: P0171 + FF CLV 72%% load — lean under acceleration, valid",
    "40", "0.1", "13.5", "3.2", "180", "1.10",
    "+20", "+18", "1.09", "58", "3200", "92",
    "P0171",
    "single",
    "Mechanical_Lean_Vacuum_Leak", "lean_condition",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 40 ppm: clean. CO 0.1%%: clean. CO2 13.5%%: mildly depressed. O2 3.2%%: significant lean (>2%%). NOx 180 ppm: elevated — lean/hot combustion. Lambda 1.10: lean. STFT +20%%/LTFT +18%%: ECU adding fuel — classic lean correction. P0171: system too lean B1. FF: CLV 72%% (heavy load per master_freeze_frame_guide.md §3), RPM 3200, MAP 58 kPa. FF confirms lean condition set under moderate load — consistent with vacuum leak unmasked at higher airflow. Source: master_freeze_frame_guide.md §3 (CLV at 72%%. Heavy acceleration). master_fuel_trim_guide.md §4 (lean trim diagnosis).",
    ff_ect="92", ff_rpm="3200", ff_load="72", ff_map="58", ff_stft_b1="+20", ff_ltft_b1="+18", ff_dtcs="P0171",
))
# --- FF-004: P0300 + FF OL — misfire during open loop, fuel trim invalid ---
add(make_row(
    "FF-004", "FF: P0300 + FF fuel status OL — misfire in open loop, trim invalid",
    "450", "3.5", "10.0", "2.5", "30", "0.88",
    "+3", "+5", "0.89", "28", "690", "25",
    "P0300",
    "single",
    "Misfire_Random_Multiple_Cold_Start", "ignition_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 450 ppm: severe misfire. CO 3.5%%: very rich — cold enrichment + misfire. CO2 10.0%%: severely depressed. O2 2.5%%: lean — unburned oxygen. NOx 30 ppm: low — cold + rich quench. Lambda 0.88: rich — cold enrichment. FF: ECT 25C (cold), fuel status OL (open loop per master_freeze_frame_guide.md §7). Fuel trim values in FF are frozen/meaningless during OL — per master_cold_start_guide.md §1, STFT/LTFT are not active in open loop. Misfire during cold open-loop warm-up: suppress fuel-trim-based candidates, pursue ignition/cold-start path. Source: master_freeze_frame_guide.md §7 (fuel system status OL). master_cold_start_guide.md §1, §4.",
    ff_ect="25", ff_rpm="690", ff_load="28", ff_map="28", ff_stft_b1="+3", ff_ltft_b1="+5", ff_dtcs="P0300",
    engine_temp="cold",
))
# --- FF-005: P0172 + FF CL normal — valid rich DTC at cruise ---
add(make_row(
    "FF-005", "FF: P0172 + FF CL cruise — valid rich DTC, closed loop confirmed",
    "150", "3.8", "12.2", "0.3", "28", "0.87",
    "-18", "-15", "0.88", "38", "760", "91",
    "P0172",
    "single",
    "Mechanical_Rich_Leaking_Injector", "rich_mixture",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 150 ppm: marginal. CO 3.8%%: very rich (>3%%). CO2 12.2%%: depressed. O2 0.3%%: low — rich consumed oxygen. NOx 28 ppm: low — rich quench. Lambda 0.87: rich. STFT -18%%/LTFT -15%%: ECU pulling fuel. P0172: system too rich B1. FF: ECT 91C (warm), fuel status CL (closed loop — valid), CLV 38%% (light cruise), RPM 760. FF confirms DTC set in closed loop at normal operating temp — fuel trim DTC is valid per master_freeze_frame_guide.md §7. Rich condition confirmed by gas chemistry + ECU pulling fuel. Source: master_freeze_frame_guide.md §7 (CL validity). master_fuel_trim_guide.md §5 (rich trim diagnosis).",
    ff_ect="91", ff_rpm="760", ff_load="38", ff_map="38", ff_stft_b1="-18", ff_ltft_b1="-15", ff_dtcs="P0172",
))
# --- FF-006: P0420 + FF normal conditions — valid catalyst fault ---
add(make_row(
    "FF-006", "FF: P0420 + FF warm/cruise — valid catalyst monitor conditions",
    "55", "0.4", "14.2", "0.5", "95", "1.01",
    "-3", "+1", "1.01", "34", "2400", "93",
    "P0420",
    "single",
    "Catalyst_Efficiency_Below_Threshold_P0420", "catalyst_fault",
    "named_fault", "0.75", "0.95",
    "false",
    "HC 55 ppm: borderline. CO 0.4%%: normal. CO2 14.2%%: near efficient. O2 0.5%%: normal. NOx 95 ppm: moderate. Lambda 1.01: near stoich. P0420: catalyst system efficiency below threshold B1. FF: ECT 93C (fully warm), RPM 2400 (cruise), CLV 45%% (light-moderate cruise), vehicle speed 85 km/h. FF conditions meet catalyst monitor enable criteria: ECT >= 70C, RPM steady at cruise, closed loop. Unlike FF-002 where ECT was 45C, this P0420 set under valid test conditions → pursue catalyst degradation path. Source: master_freeze_frame_guide.md §4 (ECT >= 70C gate), §5 (RPM at cruise). master_catalyst_guide.md §3 (monitor enable).",
    ff_ect="93", ff_rpm="2400", ff_load="45", ff_map="48", ff_stft_b1="-3", ff_ltft_b1="+1", ff_dtcs="P0420",
))
# --- FF-007: P0302 + FF — cylinder 2 specific misfire with FF context ---
add(make_row(
    "FF-007", "FF: P0302 cyl 2 misfire — FF high CLV, under load misfire",
    "280", "1.0", "12.8", "2.0", "85", "0.99",
    "+4", "+2", "1.00", "32", "2900", "90",
    "P0302",
    "single",
    "Misfire_Cylinder_2", "ignition_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 280 ppm: at misfire boundary (>250 ppm). CO 1.0%%: slightly elevated. CO2 12.8%%: mildly depressed. O2 2.0%%: lean — dead cylinder pumps unburned air. NOx 85 ppm: moderate. Lambda 0.99: near stoich — averaging. P0302: cylinder 2 misfire detected. FF: CLV 65%% (moderate-heavy load), RPM 2900, ECT 90C. FF confirms misfire under load — points to ignition coil breakdown under cylinder pressure (as opposed to FF-001 idle-only misfire). Source: master_freeze_frame_guide.md §3 (CLV 65%% = moderate-heavy load). master_ignition_guide.md §4 (load-dependent misfire).",
    ff_ect="90", ff_rpm="2900", ff_load="65", ff_map="55", ff_stft_b1="+4", ff_ltft_b1="+2", ff_dtcs="P0302",
))
# --- FF-008: P0171 + FF high STFT — severe lean, trims maxed ---
add(make_row(
    "FF-008", "FF: P0171 + FF STFT +25%% — maxed lean trim, severe vacuum leak",
    "35", "0.05", "12.5", "4.5", "220", "1.18",
    "+25", "+25", "1.16", "26", "820", "91",
    "P0171",
    "single",
    "Mechanical_Lean_Vacuum_Leak_Severe", "lean_condition",
    "named_fault", "0.85", "0.99",
    "false",
    "HC 35 ppm: clean. CO 0.05%%: very low. CO2 12.5%%: depressed. O2 4.5%%: severe lean (>4%%). NOx 220 ppm: elevated — lean/hot. Lambda 1.18: severe lean. STFT +25%%/LTFT +25%%: both trims saturated at ECU ceiling. P0171: system too lean. FF: STFT +25%% — trim saturated, confirming severe lean at fault time. MAP 26 kPa: low — consistent with intake manifold vacuum leak downstream of throttle. Pattern: large vacuum leak (brake booster hose disconnected, intake manifold gasket split) — FF trim data confirms condition present at DTC set. Source: master_freeze_frame_guide.md §2.1 (STFT in FF). master_fuel_trim_guide.md §4 (saturated lean trim). master_air_induction_guide.md §3 (vacuum leak diagnosis).",
    ff_ect="91", ff_rpm="820", ff_load="24", ff_map="26", ff_stft_b1="+25", ff_ltft_b1="+25", ff_dtcs="P0171",
))
# --- FF-009: Fuel trim DTC + FF OL-DRIVE — invalid DTC ---
add(make_row(
    "FF-009", "FF: P0172 + FF OL-DRIVE — rich DTC invalid, power enrichment active",
    "120", "2.5", "13.0", "0.8", "55", "0.93",
    "-5", "+1", "0.94", "65", "4200", "92",
    "P0172",
    "single",
    "Fuel_Trim_DTC_Invalid_OL_Drive", "fuel_fault",
    "named_fault", "0.45", "0.65",
    "false",
    "HC 120 ppm: marginal. CO 2.5%%: moderately rich. CO2 13.0%%: mildly depressed. O2 0.8%%: normal. NOx 55 ppm: moderate. Lambda 0.93: rich. STFT -5%%/LTFT +1%%: mild correction. P0172: system too rich. FF: fuel status OL-DRIVE (open loop due to driving conditions), CLV 85%% (near-WOT), RPM 4200. Per master_freeze_frame_guide.md §7 and master_cold_start_guide.md §5.2, OL-DRIVE indicates power enrichment at high load — commanded rich is normal, not a fault. Fuel trim DTC set during OL-DRIVE is not valid — demote rich-mixture candidates. Source: master_freeze_frame_guide.md §7 (OL-DRIVE gate). master_cold_start_guide.md §5.2 (WOT enrichment).",
    ff_ect="92", ff_rpm="4200", ff_load="85", ff_map="95", ff_stft_b1="-5", ff_ltft_b1="+1", ff_dtcs="P0172",
))
# --- FF-010: P0303 + FF hot ECT — misfire when hot, coil thermal failure ---
add(make_row(
    "FF-010", "FF: P0303 + FF ECT 105C — misfire hot, coil thermal breakdown",
    "380", "1.5", "11.8", "2.8", "60", "0.96",
    "+6", "+4", "0.97", "30", "730", "105",
    "P0303",
    "single",
    "Misfire_Cylinder_3_Coil_Thermal", "ignition_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 380 ppm: significant misfire (>250 ppm). CO 1.5%%: elevated. CO2 11.8%%: depressed. O2 2.8%%: lean — dead cylinder air. NOx 60 ppm: moderate. Lambda 0.96: slightly rich. P0303: cylinder 3 misfire. FF: ECT 105C (hot — above normal 100C threshold per master_freeze_frame_guide.md §4). RPM 730 (idle), CLV 21%%. FF confirms misfire at abnormally high engine temperature — points to ignition coil thermal breakdown. Coil primary winding resistance increases with temperature until spark energy insufficient for combustion. Source: master_freeze_frame_guide.md §4 (ECT > 100C = unusually hot). master_ignition_guide.md §3 (coil thermal failure).",
    ff_ect="105", ff_rpm="730", ff_load="21", ff_map="30", ff_stft_b1="+6", ff_ltft_b1="+4", ff_dtcs="P0303",
))
# --- FF-011: P0441 + FF idle — EVAP purge fault at idle ---
add(make_row(
    "FF-011", "FF: P0441 + FF idle — EVAP incorrect purge flow, idle conditions",
    "45", "0.3", "14.5", "0.4", "65", "1.01",
    "-1", "0", "1.01", "30", "750", "90",
    "P0441",
    "single",
    "EVAP_Purge_Flow_Incorrect", "fuel_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 45 ppm: clean. CO 0.3%%: normal. CO2 14.5%%: efficient. O2 0.4%%: low. NOx 65 ppm: moderate. Lambda 1.01: near stoich. STFT -1%%/LTFT 0%%: near neutral. P0441: EVAP purge flow incorrect. FF: ECT 90C, RPM 750 (idle), CLV 20%% (idle), vehicle speed 0. Gas values near-normal at idle — EVAP fault may not manifest in gas signature at idle. FF confirms fault set at idle; EVAP purge test runs at idle after warm restart. Source: master_freeze_frame_guide.md §3 (CLV at idle). master_obd_guide.md §5 (EVAP monitor).",
    ff_ect="90", ff_rpm="750", ff_load="20", ff_map="30", ff_stft_b1="-1", ff_ltft_b1="0", ff_dtcs="P0441",
))
# --- FF-012: P0135 + FF cold ECT — O2 heater circuit, cold start ---
add(make_row(
    "FF-012", "FF: P0135 + FF ECT 8C — O2 heater circuit, cold start set",
    "250", "1.8", "11.5", "1.5", "35", "0.94",
    "0", "0", "0.94", "30", "780", "25",
    "P0135",
    "single",
    "O2_Sensor_Heater_Circuit_B1S1", "sensor_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 250 ppm: at misfire boundary — cold start enrichment. CO 1.8%%: elevated — cold enrichment. CO2 11.5%%: depressed — cold engine incomplete combustion. O2 1.5%%: normal. NOx 35 ppm: low — cold. Lambda 0.94: rich — cold enrichment. P0135: O2 sensor heater circuit malfunction B1S1. FF: ECT 8C (very cold), fuel status OL, CLV 28%%. FF confirms DTC set during cold start when O2 heater should be active. Per master_freeze_frame_guide.md §4 and master_cold_start_guide.md §1-2, cold start gas signature is normal enrichment — do not pursue rich-mixture faults. Source: master_freeze_frame_guide.md §4 (cold ECT gate). master_o2_sensor_guide.md §3 (heater circuit).",
    ff_ect="8", ff_rpm="780", ff_load="28", ff_map="30", ff_stft_b1="0", ff_ltft_b1="0", ff_dtcs="P0135",
    engine_temp="cold",
))
# --- FF-013: P0401 + FF low CLV — EGR insufficient flow, idle conditions ---
add(make_row(
    "FF-013", "FF: P0401 + FF idle — EGR insufficient flow at idle test",
    "30", "0.2", "14.8", "0.3", "240", "1.01",
    "-1", "0", "1.01", "31", "750", "91",
    "P0401",
    "single",
    "egr_fault", "egr_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 30 ppm: clean. CO 0.2%%: clean. CO2 14.8%%: efficient. O2 0.3%%: low. NOx 240 ppm: elevated (>150 ppm) — EGR not cooling combustion. Lambda 1.01: near stoich. STFT -1%%/LTFT 0%%: near neutral. P0401: EGR flow insufficient. FF: ECT 91C, RPM 750 (idle), CLV 20%%. FF confirms EGR flow test ran at warm idle — standard EGR monitor test conditions. Isolated NOx elevation with P0401 is the EGR-stuck-closed signature. Source: master_freeze_frame_guide.md §3 (CLV at idle). master_egr_guide.md §4.1 (stuck closed — high NOx).",
    ff_ect="91", ff_rpm="750", ff_load="20", ff_map="31", ff_stft_b1="-1", ff_ltft_b1="0", ff_dtcs="P0401",
))
# --- FF-014: P0304 + FF high RPM — misfire at speed ---
add(make_row(
    "FF-014", "FF: P0304 + FF RPM 3800 — cyl 4 misfire at highway speed",
    "220", "0.8", "13.0", "1.8", "100", "1.02",
    "+3", "+1", "1.03", "48", "3800", "92",
    "P0304",
    "single",
    "Misfire_Cylinder_4", "ignition_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 220 ppm: below misfire boundary at speed (HC diluted by higher airflow). CO 0.8%%: slightly elevated. CO2 13.0%%: mildly depressed. O2 1.8%%: lean — residual from misfire. NOx 100 ppm: moderate. Lambda 1.02: near stoich. P0304: cylinder 4 misfire. FF: RPM 3800, CLV 58%% (moderate load at cruise), vehicle speed 110 km/h. FF confirms misfire at highway speed — not reproducible at idle. Points to high-RPM ignition breakdown (spark plug gap eroded, coil weak at high dwell) or injector clogging at high duty cycle. Source: master_freeze_frame_guide.md §5 (RPM at fault). master_ignition_guide.md §4 (high-RPM misfire).",
    ff_ect="92", ff_rpm="3800", ff_load="58", ff_map="62", ff_stft_b1="+3", ff_ltft_b1="+1", ff_dtcs="P0304",
))
# --- FF-015: P0171 + FF bank 1 only — one-bank lean, intake gasket B1 ---
add(make_row(
    "FF-015", "FF: P0171 B1 only + FF B1 trim +20%% — single bank lean, intake gasket",
    "55", "0.2", "13.5", "2.5", "160", "1.08",
    "+20", "+17", "1.07", "27", "770", "91",
    "P0171",
    "V-engine",
    "Bank_Asymmetric_Lean_B1_Intake_Gasket", "lean_condition",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 55 ppm: borderline. CO 0.2%%: normal. CO2 13.5%%: mildly depressed. O2 2.5%%: lean. NOx 160 ppm: elevated — lean/hot. Lambda 1.08: lean. STFT B1 +20%%/LTFT B1 +17%%: B1 only lean correction. P0171: system too lean B1 only (no P0174 for B2). FF: B1 STFT +20%%, B2 STFT -2%%. Bank-asymmetric trims confirm the lean condition is isolated to bank 1. Intake manifold gasket leak at B1 runner. Source: master_freeze_frame_guide.md §2.1 (STFT B1/B2 in FF). master_fuel_trim_guide.md §4 (bank-asymmetric lean).",
    ff_ect="91", ff_rpm="770", ff_load="22", ff_map="27", ff_stft_b1="+20", ff_ltft_b1="+17", ff_dtcs="P0171",
    stft_b2="-2", ltft_b2="0",
))
# ============================================================
# 15 COLD-START / NON-STARTER CASES (CS-001 to CS-015)
# ============================================================
# --- CS-001: Normal cold start — enrichment signature, no fault ---
add(make_row(
    "CS-001", "Cold start normal — ECT 5C, enrichment signature, no fault",
    "450", "2.5", "9.5", "0.5", "25", "0.88",
    "0", "0", "0.88", "38", "1100", "5",
    "",
    "single",
    "no_fault", "no_fault",
    "insufficient_evidence", "0.0", "0.35",
    "false",
    "HC 450 ppm: elevated — normal for cold start (up to 400-600 ppm per master_cold_start_guide.md §4). CO 2.5%%: elevated — cold enrichment (up to 1.5-3.0%% normal per §4). CO2 9.5%%: depressed — incomplete cold combustion (8-12%% normal per §4). O2 0.5%%: low — enrichment consumes oxygen (<1%% normal per §4). NOx 25 ppm: low — cold combustion temperature. Lambda 0.88: rich — commanded cold enrichment (0.85-0.95 normal per §4). STFT 0%%/LTFT 0%%: trims frozen in open loop. RPM 1100: elevated cold fast-idle. ECT 5C: cold start. Pattern: this is a perfectly normal cold-start gas signature. The enrichment is ECU-commanded for cold operation. Without the cold-start gate, this would be misdiagnosed as a rich-running fault. Source: master_cold_start_guide.md §2 (cold enrichment physics), §4 (normal cold gas signatures).",
    engine_temp="cold",
))
# --- CS-002: Cold start — ECT 15C, borderline warm-up ---
add(make_row(
    "CS-002", "Cold start — ECT 15C, transition zone, enrichment decaying",
    "280", "1.5", "11.0", "0.8", "40", "0.93",
    "+2", "+5", "0.94", "35", "1050", "15",
    "",
    "single",
    "no_fault", "no_fault",
    "insufficient_evidence", "0.0", "0.35",
    "false",
    "HC 280 ppm: at misfire boundary — cold start elevation resolving. CO 1.5%%: elevated — enrichment decaying. CO2 11.0%%: depressed — still below warm threshold. O2 0.8%%: low — enrichment consuming oxygen. NOx 40 ppm: low — still cool. Lambda 0.93: rich — enrichment still active. STFT +2%%/LTFT +5%%: trims beginning to activate as O2 sensor warms. ECT 15C: cool, transition zone. Pattern: engine in transition from cold open-loop to closed-loop warmup. Per master_cold_start_guide.md §3-4, ECT 15C is in the transition zone — enrichment should be decaying, O2 sensor approaching readiness. This snapshot is normal for the warm-up phase. Source: master_cold_start_guide.md §3 (closed-loop transition), §4.",
    engine_temp="cold",
))
# --- CS-003: Cold start + small vacuum leak — masked by enrichment ---
add(make_row(
    "CS-003", "Cold start + masked vacuum leak — enrichment hides lean, will appear warm",
    "350", "1.8", "10.5", "1.2", "35", "0.91",
    "+5", "+10", "0.92", "28", "1080", "10",
    "",
    "single",
    "Mechanical_Lean_Vacuum_Leak_Masked_Cold", "lean_condition",
    "named_fault", "0.55", "0.75",
    "false",
    "HC 350 ppm: elevated — cold start + early misfire from lean. CO 1.8%%: elevated — enrichment partially compensates for vacuum leak. CO2 10.5%%: depressed — cold + lean combustion deficit. O2 1.2%%: normal/slightly lean — vacuum leak adds air but cold enrichment masks it. NOx 35 ppm: low — cold. Lambda 0.91: rich — cold enrichment overpowers small vacuum leak at idle. LTFT +10%%: elevated — ECU has been adding fuel historically (learned from warm operation). Pattern: small vacuum leak masked by cold enrichment. At cold start, enrichment compensates → gas looks normal-rich for cold. When engine warms, enrichment decays → lean condition emerges → P0171 sets after warmup. LTFT +10%% is the clue. Source: master_cold_start_guide.md §4 (masking effect). master_fuel_trim_guide.md §4.",
    engine_temp="cold",
))
# --- CS-004: Cold start — ECT 35C, enrichment just ended ---
add(make_row(
    "CS-004", "Cold start — ECT 35C, enrichment ending, O2 active, borderline rich",
    "120", "0.9", "13.5", "1.0", "70", "0.98",
    "-3", "-1", "0.99", "33", "980", "35",
    "",
    "single",
    "no_fault", "no_fault",
    "insufficient_evidence", "0.0", "0.30",
    "false",
    "HC 120 ppm: marginal — cold start residual clearing. CO 0.9%%: slightly elevated — enrichment nearly decayed. CO2 13.5%%: mildly depressed — combustion efficiency improving. O2 1.0%%: normal. NOx 70 ppm: moderate — combustion warming. Lambda 0.98: near stoich — enrichment almost fully decayed. STFT -3%%/LTFT -1%%: trims active — O2 sensor online. ECT 35C: approaching closed-loop enable threshold (20-40C per master_cold_start_guide.md §3). Pattern: engine nearing end of cold-start enrichment phase. Gas values converging toward warm-normal. This is a normal warm-up snapshot. Source: master_cold_start_guide.md §3 (closed-loop transition thresholds).",
    engine_temp="transition",
))
# --- CS-005: Cold start rich — leaking injector, cold enrichment amplifies ---
add(make_row(
    "CS-005", "Cold start + leaking injector — enrichment amplifies existing rich fault",
    "550", "5.5", "8.5", "0.2", "15", "0.78",
    "-15", "-10", "0.79", "36", "1050", "8",
    "P0172",
    "single",
    "Mechanical_Rich_Leaking_Injector", "rich_mixture",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 550 ppm: above cold normal (400-600 ceiling) — excess fuel from injector leak. CO 5.5%%: above cold normal (3.0%% ceiling) — injector leak adds fuel on top of enrichment. CO2 8.5%%: critically low — extreme rich combustion deficit. O2 0.2%%: critically low — fuel consumed all available oxygen. NOx 15 ppm: negligible — extreme rich quench. Lambda 0.78: critically rich — beyond cold enrichment range (0.85-0.95). STFT -15%%/LTFT -10%%: ECU pulling fuel — even in open loop, corrections are leaning. P0172: rich DTC. Pattern: cold enrichment amplifies a pre-existing leaking-injector rich fault. The lambda 0.78 is below the cold-start enrichment floor of 0.85 — enrichment alone cannot explain this. Combined cold enrichment + injector leak = extreme rich. Source: master_cold_start_guide.md §4 (cold enrichment upper bounds). master_fuel_system_guide.md §3 (leaking injector).",
    engine_temp="cold",
))
# --- CS-006: Non-starter — no fuel, CKP failure ---
add(make_row(
    "CS-006", "Non-starter: no fuel — CKP failure, no injection, cranking gas",
    "5", "0.02", "0.5", "20.5", "2", "5.00",
    "0", "0", "0.00", "15", "200", "10",
    "P0335",
    "single",
    "CKP_Sensor_Failure_No_Start", "ignition_fault",
    "named_fault", "0.90", "0.99",
    "false",
    "HC 5 ppm: near zero — no fuel reaching cylinders (master_non_starter_guide.md §2: No fuel fingerprint). CO 0.02%%: near zero — no combustion. CO2 0.5%%: near zero — no combustion products. O2 20.5%%: near-ambient (20.9%%) — engine pumping pure air. Lambda 5.00: infinite — no fuel. RPM 200: cranking speed normal. MAP 15 kPa: cranking vacuum (electronic vacuum gauge test). P0335: CKP sensor circuit. Pattern: classic no-fuel cranking fingerprint — HC ~ 0 + O2 ~ 20.9%% + lambda -> inf. CKP failure disables both injection AND ignition simultaneously (master_non_starter_guide.md §5). RPM PID = 200 confirms CKP reporting but ECU has disabled injection (not a 0-RPM CKP failure). Source: master_non_starter_guide.md §2 (no fuel fingerprint), §5 (CKP failure mode).",
    engine_temp="cold",
))
# --- CS-007: Non-starter — flooded, no spark ---
add(make_row(
    "CS-007", "Non-starter: flooded — no spark, injectors firing, raw fuel exits",
    "6000", "6.0", "4.0", "5.0", "10", "0.55",
    "0", "0", "0.55", "25", "180", "12",
    "",
    "single",
    "Ignition_Coil_Failure_No_Spark", "ignition_fault",
    "named_fault", "0.90", "0.99",
    "false",
    "HC 6000 ppm: extreme — raw fuel exiting cylinders unburned (master_non_starter_guide.md §2: Flooded fingerprint). CO 6.0%%: very high — partial burn of excess fuel during cranking. CO2 4.0%%: very low — minimal combustion. O2 5.0%%: moderate — some oxygen displaced by fuel vapor but not consumed. Lambda 0.55: extremely rich — massive excess fuel. RPM 180: cranking speed. Pattern: classic flooded/no-spark cranking fingerprint — HC very high + CO high + O2 moderate + lambda very rich. Injectors are delivering fuel, ignition is absent → raw fuel exits. Smell test: strong fuel odor at oil filler cap. Spark test: no spark on any cylinder. Source: master_non_starter_guide.md §2 (flooded fingerprint), §4 (sequential test). master_ignition_guide.md §2 (no-spark diagnosis).",
    engine_temp="cold",
))
# --- CS-008: Non-starter — no compression, timing belt ---
add(make_row(
    "CS-008", "Non-starter: no compression — broken timing belt, cranking gas",
    "300", "0.3", "1.5", "17.0", "5", "1.05",
    "0", "0", "1.05", "10", "350", "15",
    "",
    "single",
    "Mechanical_No_Compression_Timing_Belt", "mechanical_fault",
    "named_fault", "0.90", "0.99",
    "false",
    "HC 300 ppm: moderate — residual fuel vapor from intake, no compression to burn it. CO 0.3%%: low — minimal combustion. CO2 1.5%%: very low — no compression, no combustion pressure. O2 17.0%%: high (15-19%% range) — air enters but doesn't compress/burn per master_non_starter_guide.md §2. Lambda 1.05: near balanced — unburned mixture ratio preserved. RPM 350: too fast — low compression allows starter to spin engine faster (cranking RPM test, master_non_starter_guide.md §3: >350 RPM = low compression). Pattern: classic no-compression cranking fingerprint — HC low-to-moderate + CO low + CO2 very low + O2 high + lambda ~ 1.0. Fast cranking RPM confirms low compression. Timing belt broken → valves not moving → no compression on any cylinder. Source: master_non_starter_guide.md §2 (no compression fingerprint), §3 (fast cranking RPM test). master_mechanical_guide.md §1 (compression test).",
    engine_temp="cold",
))
# --- CS-009: Non-starter — no spark, all coils failed ---
add(make_row(
    "CS-009", "Non-starter: no spark — all coils dead, raw fuel + air exit",
    "2500", "0.8", "3.5", "12.0", "8", "0.98",
    "0", "0", "0.98", "18", "190", "14",
    "P0351",
    "single",
    "Ignition_Coil_All_Failure_No_Spark", "ignition_fault",
    "named_fault", "0.90", "0.99",
    "false",
    "HC 2500 ppm: very high — fuel enters but doesn't ignite (master_non_starter_guide.md §2: No spark fingerprint). CO 0.8%%: low — minimal partial burn. CO2 3.5%%: very low — no combustion. O2 12.0%%: high (10-18%% range) — fuel and air both exit unreacted. Lambda 0.98: near balanced — unburned mixture exits in roughly the ratio it entered. P0351: ignition coil A primary/secondary circuit. Pattern: no-spark cranking fingerprint — HC very high (>1000 ppm) + CO low + O2 high + lambda ~ 1.0. Unlike flooded (CS-007), CO is low because there's no partial burn — fuel and air exit chemically unreacted. All coils failed simultaneously (ECU ignition output stage failure). Source: master_non_starter_guide.md §2 (no spark fingerprint). master_ignition_guide.md §2 (ignition output stage).",
    engine_temp="cold",
))
# --- CS-010: Non-starter — immobiliser fuel-cut ---
add(make_row(
    "CS-010", "Non-starter: immobiliser active — cranks, no fuel injector pulse",
    "3", "0.01", "0.3", "20.8", "1", "6.00",
    "0", "0", "0.00", "14", "210", "18",
    "",
    "single",
    "Immobiliser_Active_Fuel_Cut", "ecu_fault",
    "named_fault", "0.85", "0.98",
    "false",
    "HC 3 ppm: near zero — no fuel (master_non_starter_guide.md §2: No fuel fingerprint). CO 0.01%%: near zero. CO2 0.3%%: near zero. O2 20.8%%: near-ambient — pumping pure air. Lambda 6.00: infinite — no fuel. RPM 210: cranking normal. No DTCs: immobiliser typically sets manufacturer-specific codes, not generic P-codes. Pattern: identical to CS-006 no-fuel fingerprint, but CKP is functional (RPM 210). The discriminator: no DTCs + security light flashing + no injector pulse (noid light test). Per master_non_starter_guide.md §6, immobiliser may permit cranking but cut injector pulse. Rule out immobiliser before pursuing mechanical/fuel-system candidates. Source: master_non_starter_guide.md §6 (immobiliser gate).",
    engine_temp="cold",
))
# --- CS-011: Cold start — enrichment normal, ECT -5C, extreme cold ---
add(make_row(
    "CS-011", "Cold start extreme — ECT -5C, maximum enrichment, sub-zero start",
    "580", "3.2", "8.0", "0.3", "15", "0.83",
    "0", "0", "0.83", "40", "1200", "-5",
    "",
    "single",
    "no_fault", "no_fault",
    "insufficient_evidence", "0.0", "0.35",
    "false",
    "HC 580 ppm: upper end of cold normal (400-600 ppm ceiling per master_cold_start_guide.md §4). CO 3.2%%: slightly above typical cold ceiling (3.0%% at extreme cold). CO2 8.0%%: depressed — extreme cold combustion inefficiency. O2 0.3%%: very low — maximum enrichment. NOx 15 ppm: negligible — extremely cold combustion. Lambda 0.83: rich — maximum cold enrichment (typical floor 0.85 at very low ambient per §2). STFT 0%%/LTFT 0%%: open loop, trims frozen. RPM 1200: maximum cold fast-idle. ECT -5C: sub-zero cold start. Pattern: extreme cold start at sub-zero ambient. Gas values are at the edge of normal cold enrichment. Per §4, ECT < 0C may push lambda below the 0.85 floor — still normal for the conditions. Must re-test when ECT >= 70C. Source: master_cold_start_guide.md §2 (cold enrichment physics), §4 (cold start normal ranges).",
    engine_temp="cold",
))
# --- CS-012: Cold start — P0115 ECT sensor stuck hot, ECU under-enrichens ---
add(make_row(
    "CS-012", "Cold start + P0115 — ECT sensor stuck at 85C, ECU under-enrichens cold engine",
    "200", "0.6", "12.0", "1.5", "50", "0.99",
    "+8", "+12", "1.00", "32", "850", "5",
    "P0115",
    "single",
    "ECT_Sensor_Stuck_Hot_Cold_Start", "sensor_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 200 ppm: elevated — cold engine with insufficient enrichment. CO 0.6%%: low for cold start — ECU not commanding enough fuel. CO2 12.0%%: better than typical cold — leaner burn. O2 1.5%%: higher than typical cold — excess air from lean mixture. NOx 50 ppm: higher than typical cold — leaner/hotter burn than cold normal. Lambda 0.99: near stoich — ECU targeting stoich because ECT sensor reports 85C (warm). STFT +8%%/LTFT +12%%: ECU adding fuel — O2 feedback correcting the lean from missing enrichment. P0115: ECT sensor circuit malfunction. Pattern: ECT sensor failed stuck at 85C → ECU believes engine is warm → commands stoich mixture → no cold enrichment. Engine actually at 5C — should be at lambda 0.85-0.95. O2 feedback partially corrects but cannot fully compensate for missing cold enrichment map. Source: master_cold_start_guide.md §1 (open loop fuel maps), §3 (ECT sensor role). master_ecu_guide.md §5.1 (ECT sensor failure).",
    engine_temp="cold",
))
# --- CS-013: Non-starter — normal cranking, will start ---
add(make_row(
    "CS-013", "Non-starter: normal cranking — will start with patience, no fault",
    "500", "1.0", "10.0", "8.0", "20", "0.95",
    "0", "0", "0.95", "22", "220", "12",
    "",
    "single",
    "no_fault", "no_fault",
    "insufficient_evidence", "0.0", "0.35",
    "false",
    "HC 500 ppm: normal cranking range (200-800 ppm per master_non_starter_guide.md §2). CO 1.0%%: normal cranking range (0.5-1.5%%). CO2 10.0%%: normal cranking range (8-12%%). O2 8.0%%: normal cranking range (5-12%%). Lambda 0.95: normal cranking range (0.9-1.1). RPM 220: normal cranking speed (150-300 RPM). Pattern: normal cranking gas fingerprint — engine has compression + fuel + spark, all three present. Will fire if cranked long enough. This is the baseline healthy-cranking signature. Per master_non_starter_guide.md §2: 'Normal cranking (will start with patience)'. Source: master_non_starter_guide.md §2 (normal cranking fingerprint).",
    engine_temp="cold",
))
# --- CS-014: Cold start + P0505 — IAC stuck, high idle cold ---
add(make_row(
    "CS-014", "Cold start + P0505 — IAC stuck, idle 1500 RPM cold, lean cold",
    "150", "0.4", "12.5", "2.0", "80", "1.04",
    "+12", "+10", "1.03", "32", "1500", "8",
    "P0505",
    "single",
    "IAC_Stuck_High_Idle_Cold", "mechanical_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 150 ppm: lower than expected for cold — extra air dilutes HC concentration. CO 0.4%%: low — extra air leans mixture. CO2 12.5%%: depressed — lean combustion. O2 2.0%%: lean — excess air from IAC stuck open. NOx 80 ppm: elevated for cold — lean/hotter combustion despite cold ECT. Lambda 1.04: lean — IAC stuck open adds unmetered air (or ECU targets high idle with lean mixture). STFT +12%%/LTFT +10%%: ECU adding fuel to correct lean. P0505: idle control system malfunction. RPM 1500: high — IAC stuck at high step count. ECT 8C: cold start. Pattern: IAC valve stuck open → high idle → excess air → lean mixture. Cold enrichment partially offsets but cannot fully compensate for the excess air. Source: master_cold_start_guide.md §4. master_air_induction_guide.md §4 (IAC failure).",
    engine_temp="cold",
))
# --- CS-015: Non-starter — CKP 0 RPM, no crank signal ---
add(make_row(
    "CS-015", "Non-starter: CKP 0 RPM — no crank signal, injection + ignition disabled",
    "2", "0.01", "0.2", "20.9", "1", "10.00",
    "0", "0", "0.00", "10", "0", "20",
    "P0335",
    "single",
    "CKP_Sensor_No_Signal_Zero_RPM", "ignition_fault",
    "named_fault", "0.95", "0.99",
    "false",
    "HC 2 ppm: near zero — no fuel AND no spark. CO 0.01%%: near zero. CO2 0.2%%: near zero. O2 20.9%%: ambient — pure air pumped through with no combustion. Lambda 10.00: infinite — zero fuel. RPM 0: no RPM signal — CKP not reporting. P0335: CKP sensor circuit. Pattern: the single most common non-starter root cause per master_non_starter_guide.md §5. CKP sensor open/shorted → no RPM signal → ECU disables BOTH injection AND ignition simultaneously. 0 RPM during cranking is the definitive diagnostic sign — differentiates from CS-006 where CKP reports RPM but ECU cuts injection for another reason. Source: master_non_starter_guide.md §3 (0 RPM = CKP failure), §5 (CKP failure mode specifics).",
    engine_temp="cold",
))
# ============================================================
# 10 ERA-SPECIFIC CASES (ERA-001 to ERA-010)
# ============================================================
# --- ERA-001: Pre-OBD-II 1992 — distributor cap carbon tracking ---
add(make_row(
    "ERA-001", "Era 1992: distributor cap carbon tracking — cross-fire, high HC, no DTCs",
    "420", "2.0", "11.0", "2.8", "55", "0.94",
    "0", "0", "0.94", "28", "700", "88",
    "",
    "single",
    "Distributor_Cap_Carbon_Tracking_Crossfire", "ignition_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 420 ppm: significant misfire — cross-fire sends spark to wrong cylinder. CO 2.0%%: elevated — partial burn from mis-timed ignition. CO2 11.0%%: depressed — combustion inefficiency. O2 2.8%%: lean — unburned oxygen from misfired cylinders. NOx 55 ppm: moderate. Lambda 0.94: slightly rich — partial burn products. No DTCs: pre-OBD-II (1992) — no misfire monitor, no DTC support. Era 1990-1995: distributor-cap ignition. Pattern: carbon tracking inside distributor cap creates conductive path between terminals → spark jumps to wrong cylinder → cross-fire misfire. Diagnosed by visual inspection of cap (carbon tracks visible) and gas chemistry pattern. Source: v2-design-rules §7 (era bucket 1990-1995 — pre-OBD-II, distributor cap). master_ignition_guide.md §5 (distributor diagnosis).",
))
# --- ERA-002: Pre-OBD-II 1994 — carbureted, rich at idle ---
add(make_row(
    "ERA-002", "Era 1994: carbureted rich idle — choke stuck closed, high CO",
    "300", "5.0", "10.0", "0.4", "20", "0.82",
    "0", "0", "0.82", "30", "720", "85",
    "",
    "single",
    "Carburetor_Choke_Stuck_Closed_Rich", "fuel_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 300 ppm: elevated — rich misfire. CO 5.0%%: very rich — choke stuck closed, excess fuel. CO2 10.0%%: depressed — rich combustion deficit. O2 0.4%%: low — rich consumed oxygen. NOx 20 ppm: very low — rich quench. Lambda 0.82: very rich. No DTCs: pre-OBD-II carbureted engine — no ECU, no codes. Era 1990-1995: carbureted vehicles still common in early 1990s. Pattern: automatic choke mechanism stuck closed → engine runs on cold-start mixture permanently → rich at all operating temps. Diagnosed by: choke plate visually closed when warm, gas confirms rich. Source: v2-design-rules §7 (era bucket 1990-1995 — pre-OBD-II). master_fuel_system_guide.md §2 (carburetor diagnosis).",
))
# --- ERA-003: OBD-II 1998 — P0420 + rear O2 high voltage, classic catalyst ---
add(make_row(
    "ERA-003", "Era 1998: P0420 + downstream O2 tracking upstream — dead catalyst",
    "45", "0.3", "14.5", "0.4", "100", "1.01",
    "-3", "+1", "1.01", "32", "750", "91",
    "P0420",
    "single",
    "Catalyst_Efficiency_Below_Threshold_P0420", "catalyst_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 45 ppm: clean — pre-cat normal. CO 0.3%%: clean. CO2 14.5%%: efficient. O2 0.4%%: low. NOx 100 ppm: moderate. Lambda 1.01: near stoich. P0420: catalyst efficiency below threshold. Era 1996-2005: OBD-II, P0xxx DTC families present. Pattern: downstream O2 sensor voltage mirrors upstream — catalyst has no oxygen storage capacity → dead catalyst. Gas values at tailpipe may appear normal because the engine runs correctly; the catalyst simply isn't converting. The P0420 + O2 sensor tracking pattern is the diagnosis. Source: v2-design-rules §7 (era bucket 1996-2005 — OBD-II, P0xxx families). master_catalyst_guide.md §3 (catalyst monitor), §4 (O2 tracking pattern).",
))
# --- ERA-004: OBD-II 2002 — EVAP large leak, P0455 ---
add(make_row(
    "ERA-004", "Era 2002: P0455 EVAP large leak — loose fuel cap, no gas symptoms",
    "25", "0.15", "15.0", "0.2", "30", "1.00",
    "-1", "0", "1.00", "31", "750", "92",
    "P0455",
    "single",
    "EVAP_Large_Leak_Loose_Fuel_Cap", "fuel_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 25 ppm: clean. CO 0.15%%: clean. CO2 15.0%%: efficient. O2 0.2%%: low. NOx 30 ppm: low. Lambda 1.00: perfect stoich. P0455: EVAP large leak detected. Era 1996-2005: OBD-II with full EVAP monitor. Pattern: loose/missing fuel cap → EVAP system cannot hold vacuum → P0455 sets. Gas values are completely normal — EVAP leaks do not affect combustion. This case tests that the engine does NOT incorrectly route EVAP DTCs to mixture faults. Source: v2-design-rules §7 (era bucket 1996-2005). master_obd_guide.md §5 (EVAP monitor). master_fuel_system_guide.md §5 (EVAP system).",
))
# --- ERA-005: CAN-bus 2008 — VVT solenoid stuck, P0011 ---
add(make_row(
    "ERA-005", "Era 2008: VVT solenoid stuck advanced — rough idle, P0011",
    "250", "0.8", "13.0", "1.8", "90", "1.02",
    "+6", "+4", "1.03", "32", "720", "91",
    "P0011",
    "single",
    "VVT_Solenoid_Stuck_Advanced", "mechanical_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 250 ppm: at misfire boundary — cam timing off at idle. CO 0.8%%: slightly elevated. CO2 13.0%%: mildly depressed. O2 1.8%%: lean — incomplete burn from wrong cam timing. NOx 90 ppm: moderate. Lambda 1.02: near stoich. P0011: camshaft position A — timing over-advanced B1. Era 2006-2015: CAN-bus era, VVT common. Pattern: VVT solenoid stuck in advanced position → intake cam advanced at idle → valve overlap excessive → rough idle with elevated HC. VVT introduced widely in this era; pre-2006 engines would not have this fault mode. Source: v2-design-rules §7 (era bucket 2006-2015 — CAN-bus, VVT). master_mechanical_guide.md §3 (VVT diagnosis).",
))
# --- ERA-006: CAN-bus 2012 — GDI high-pressure fuel pump, P0087 ---
add(make_row(
    "ERA-006", "Era 2012: GDI HPFP failure — P0087, lean under load",
    "40", "0.1", "13.0", "3.0", "170", "1.10",
    "+18", "+15", "1.09", "30", "780", "92",
    "P0087",
    "single",
    "GDI_HPFP_Low_Pressure_Lean", "fuel_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 40 ppm: clean. CO 0.1%%: clean. CO2 13.0%%: mildly depressed. O2 3.0%%: lean (>2%%). NOx 170 ppm: elevated — lean/hot GDI combustion. Lambda 1.10: lean. STFT +18%%/LTFT +15%%: ECU adding fuel — compensating for low fuel pressure. P0087: fuel rail/system pressure too low. Era 2006-2015: GDI emerging. Pattern: GDI high-pressure fuel pump failing → rail pressure drops → lean mixture. GDI engines run stratified lean under light load but this is homogeneous-mode lean from pressure deficit. Source: v2-design-rules §7 (era bucket 2006-2015 — GDI emerging). master_fuel_system_guide.md §4 (GDI fuel system).",
))
# --- ERA-007: Modern 2018 — GPF-equipped, P2463 ---
add(make_row(
    "ERA-007", "Era 2018: GPF soot load excessive — P2463, no gas symptoms",
    "20", "0.1", "15.5", "0.1", "25", "1.00",
    "0", "0", "1.00", "31", "740", "93",
    "P2463",
    "single",
    "GPF_Soot_Load_Excessive", "exhaust_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 20 ppm: very clean. CO 0.1%%: clean. CO2 15.5%%: very efficient. O2 0.1%%: very low. NOx 25 ppm: low. Lambda 1.00: perfect stoich. P2463: particulate filter — soot accumulation (GPF on petrol GDI). Era 2016-2020: Euro 6, GPF fitted to GDI engines. Pattern: gasoline particulate filter (GPF) reaching soot load limit — triggers regeneration request. Gas values completely normal — GPF loading does not affect combustion gas signature at idle. This case tests that the engine routes GPF DTCs correctly and does not confuse them with mixture or catalyst faults. Source: v2-design-rules §7 (era bucket 2016-2020 — Euro 6, GPF). master_exhaust_guide.md §5 (GPF diagnosis).",
))
# --- ERA-008: Modern 2019 — wideband O2, P2626 ---
add(make_row(
    "ERA-008", "Era 2019: wideband O2 pumping cell open — P2626, ECU open-loop fallback",
    "100", "1.2", "13.8", "0.8", "80", "0.97",
    "-6", "-3", "0.97", "32", "760", "91",
    "P2626",
    "single",
    "Wideband_O2_Pumping_Cell_Open", "sensor_fault",
    "named_fault", "0.75", "0.95",
    "false",
    "HC 100 ppm: marginal. CO 1.2%%: slightly elevated. CO2 13.8%%: mildly depressed. O2 0.8%%: normal. NOx 80 ppm: moderate. Lambda 0.97: slightly rich. STFT -6%%/LTFT -3%%: mild correction — ECU using last-known trims. P2626: O2 sensor pumping current trim circuit/open B1S1. Era 2016-2020: wideband O2 sensors standard on modern engines. Pattern: wideband O2 sensor pumping cell circuit open → ECU loses primary lambda feedback → falls back to modeled fuel with last-known trims. Mixture drifts slightly rich. Without the wideband-specific DTC knowledge, this could be confused with a mild rich-running fault. Source: v2-design-rules §7 (era bucket 2016-2020). master_o2_sensor_guide.md §4 (wideband diagnosis). master_ecu_guide.md §4.5.",
))
# --- ERA-009: Pre-OBD-II 1991 — no catalytic converter ---
add(make_row(
    "ERA-009", "Era 1991: no catalyst — high HC+CO, pre-cat era, normal for vehicle",
    "350", "3.5", "11.0", "1.5", "60", "0.92",
    "0", "0", "0.92", "30", "760", "88",
    "",
    "single",
    "no_fault", "no_fault",
    "insufficient_evidence", "0.0", "0.30",
    "false",
    "HC 350 ppm: elevated — typical pre-cat engine (no catalyst to oxidize HC). CO 3.5%%: elevated — typical pre-cat carbureted or early EFI. CO2 11.0%%: typical pre-cat. O2 1.5%%: typical pre-cat. NOx 60 ppm: moderate. Lambda 0.92: slightly rich — typical pre-cat tune. No DTCs: pre-OBD-II, no catalyst monitoring. Era 1990-1995: pre-catalyst era — many early 1990s vehicles had no catalytic converter or a basic oxidation catalyst only. Pattern: gas values that would indicate a dead catalyst on a modern vehicle are normal for a pre-cat vehicle. The era mask (R6) must prevent the engine from applying catalyst-efficiency fault logic to pre-cat-era vehicles. Source: v2-design-rules §7 (era bucket 1990-1995 — pre-OBD-II). R6 (era-aware KG). master_catalyst_guide.md §2 (catalyst history).",
))
# --- ERA-010: OBD-II 2004 — CAN-bus transition era, P0606 ---
add(make_row(
    "ERA-010", "Era 2004: ECU processor fault P0606 — CAN-bus transition era",
    "180", "1.5", "12.8", "1.5", "70", "0.96",
    "-4", "-2", "0.97", "30", "740", "88",
    "P0606",
    "single",
    "ECU_Internal_Processor_Fault", "ecu_fault",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 180 ppm: marginal. CO 1.5%%: moderately elevated. CO2 12.8%%: depressed. O2 1.5%%: lean/normal. NOx 70 ppm: moderate. Lambda 0.96: slightly rich. P0606: ECM/PCM processor fault. Era 1996-2005: late OBD-II, early CAN-bus transition. Pattern: ECU internal processor fault → erratic fuel control → mixture oscillates between rich and lean. P0606 is a critical ECU-internal fault — the engine should demote all sensor-based candidates and flag ECU-internal as primary. This era represents the transition from standalone ECUs to CAN-networked modules. Source: v2-design-rules §7 (era bucket 1996-2005 — OBD-II pre-CAN). master_ecu_guide.md §3.1 (processor fault).",
))
# ============================================================
# 10 DUAL-BANK CASES (DB-001 to DB-010)
# ============================================================
# --- DB-001: V-engine, B1 lean B2 normal — intake gasket B1 ---
add(make_row(
    "DB-001", "Dual-bank: B1 lean +25%%/B2 normal — intake gasket leak B1 only",
    "50", "0.15", "13.2", "3.0", "170", "1.09",
    "+25", "+22", "1.08", "26", "760", "91",
    "P0171",
    "V-engine",
    "Bank_Asymmetric_Lean_B1_Intake_Gasket", "lean_condition",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 50 ppm: borderline. CO 0.15%%: clean. CO2 13.2%%: mildly depressed — averaged across banks. O2 3.0%%: lean — B1 lean dominates post-catalyst average. NOx 170 ppm: elevated — B1 lean/hot combustion. Lambda 1.09: lean — averaged. STFT B1 +25%%/LTFT B1 +22%%: B1 severely lean. STFT B2 -2%%/LTFT B2 +1%%: B2 near neutral. P0171: B1 lean only (no P0174). V-engine bank_config: bank-asymmetric trims are the diagnosis. Pattern: intake manifold gasket leak at B1 runner → air enters B1 only → B1 runs lean → B1 trims maxed. B2 runs normally. Post-catalyst gas averages both banks. Source: master_fuel_trim_guide.md §4 (bank-asymmetric diagnosis). master_air_induction_guide.md §3 (intake gasket leak).",
    stft_b2="-2", ltft_b2="+1",
))
# --- DB-002: V-engine, B2 rich B1 normal — leaking injector B2 ---
add(make_row(
    "DB-002", "Dual-bank: B2 rich -20%%/B1 normal — leaking injector B2 only",
    "140", "2.5", "13.0", "0.6", "45", "0.93",
    "+2", "+1", "0.99", "34", "760", "92",
    "P0175",
    "V-engine",
    "Bank_Asymmetric_Rich_B2_Leaking_Injector", "rich_mixture",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 140 ppm: marginal — B2 rich contribution. CO 2.5%%: moderately rich — B2 excess fuel. CO2 13.0%%: mildly depressed — averaged across banks. O2 0.6%%: normal — B1 normal dilutes B2 rich. NOx 45 ppm: low — B2 rich quench. Lambda 0.93: rich — averaged. STFT B2 -20%%/LTFT B2 -18%%: B2 pulling fuel. STFT B1 +2%%/LTFT B1 +1%%: B1 near neutral. P0175: B2 too rich. V-engine: B2 leaking injector → excess fuel B2 only. Post-catalyst average is less rich than B2 alone because B1 exhaust dilutes it. Bank-asymmetric trims + single-bank DTC is the diagnosis. Source: master_fuel_trim_guide.md §5 (bank-asymmetric rich). master_fuel_system_guide.md §3 (leaking injector).",
    stft_b2="-20", ltft_b2="-18",
))
# --- DB-003: V-engine, both banks lean — global vacuum leak ---
add(make_row(
    "DB-003", "Dual-bank: B1 +18%%/B2 +15%% both lean — global vacuum leak",
    "35", "0.1", "13.0", "3.5", "200", "1.12",
    "+18", "+16", "1.11", "25", "780", "92",
    "P0171|P0174",
    "V-engine",
    "Mechanical_Lean_Vacuum_Leak_Global", "lean_condition",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 35 ppm: clean. CO 0.1%%: clean. CO2 13.0%%: depressed. O2 3.5%%: significant lean. NOx 200 ppm: elevated — lean/hot. Lambda 1.12: lean. STFT B1 +18%%/LTFT B1 +16%%, STFT B2 +15%%/LTFT B2 +14%%: both banks lean. P0171/P0174: both banks lean. MAP 25 kPa: low — vacuum leak. Pattern: global vacuum leak (brake booster hose, PCV hose disconnected) affects both banks equally. Both banks show similar lean trims + both P0171 and P0174 set. Unlike DB-001 (B1 only), the symmetry points to a common cause upstream of the intake split. Source: master_fuel_trim_guide.md §4 (global lean). master_air_induction_guide.md §3.",
    stft_b2="+15", ltft_b2="+14",
))
# --- DB-004: V-engine, B1 misfire B2 normal — coil failure B1 ---
add(make_row(
    "DB-004", "Dual-bank: B1 misfire P0300/B2 normal — coil pack B1 failed",
    "350", "1.5", "11.5", "2.8", "55", "0.96",
    "+8", "+5", "0.97", "28", "710", "90",
    "P0300",
    "V-engine",
    "Bank_Asymmetric_Misfire_B1_Coil_Pack", "ignition_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 350 ppm: significant misfire — B1 cylinders dead. CO 1.5%%: elevated — B1 partial burn. CO2 11.5%%: depressed — B1 incomplete combustion. O2 2.8%%: lean — B1 dead cylinders pump unburned air. NOx 55 ppm: moderate. Lambda 0.96: slightly rich — averaged. STFT B1 +8%%/B1 LTFT +5%%: B1 adding fuel (O2 sensor sees lean from dead cylinders). STFT B2 -1%%/LTFT B2 0%%: B2 normal. P0300: random misfire — B1 coil pack failure kills entire bank. Pattern: complete B1 coil pack failure → all B1 cylinders misfire. O2 sensor on B1 sees lean (unburned oxygen) → ECU adds fuel to B1 → trims positive despite rich raw exhaust. V-engine bank-asymmetric misfire — B2 runs normally. Source: master_ignition_guide.md §4 (coil pack failure). master_fuel_trim_guide.md §4 (false lean from misfire).",
    stft_b2="-1", ltft_b2="0",
))
# --- DB-005: V-engine, B1 rich B2 rich — FPR vacuum hose off ---
add(make_row(
    "DB-005", "Dual-bank: B1 -15%%/B2 -14%% both rich — FPR vacuum hose disconnected",
    "160", "3.2", "12.5", "0.3", "30", "0.88",
    "-15", "-13", "0.89", "40", "770", "91",
    "P0172|P0175",
    "V-engine",
    "Fuel_Pressure_Regulator_Vacuum_Hose_Off", "fuel_fault",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 160 ppm: marginal. CO 3.2%%: very rich. CO2 12.5%%: depressed. O2 0.3%%: low. NOx 30 ppm: low — rich quench. Lambda 0.88: rich. STFT B1 -15%%/LTFT B1 -13%%, STFT B2 -14%%/LTFT B2 -12%%: both banks pulling fuel. P0172/P0175: both banks rich. MAP 40 kPa: elevated — FPR vacuum reference lost → fuel pressure runs at atmospheric reference (higher). Pattern: fuel pressure regulator vacuum hose disconnected → FPR references atmosphere instead of manifold vacuum → fuel pressure higher than intended → both banks rich. Symmetric rich trims on both banks is the key differentiator from DB-002 (single-bank rich). Source: master_fuel_system_guide.md §3 (FPR diagnosis). master_fuel_trim_guide.md §5 (symmetric rich).",
    stft_b2="-14", ltft_b2="-12",
))
# --- DB-006: V-engine, B1 cat dead B2 cat good — P0430 only ---
add(make_row(
    "DB-006", "Dual-bank: P0430 B2 only — B2 catalyst dead, B1 cat OK",
    "60", "0.5", "14.0", "0.5", "110", "1.02",
    "-2", "0", "1.02", "33", "760", "93",
    "P0430",
    "V-engine",
    "Catalyst_Efficiency_Below_Threshold_B2", "catalyst_fault",
    "named_fault", "0.75", "0.95",
    "false",
    "HC 60 ppm: borderline. CO 0.5%%: normal. CO2 14.0%%: near efficient. O2 0.5%%: normal. NOx 110 ppm: moderate. Lambda 1.02: near stoich. P0430: catalyst system efficiency below threshold B2. No P0420 (B1 cat OK). V-engine: post-catalyst gas is averaged — B1 good cat masks B2 dead cat in tailpipe gas. Only the DTC reveals the bank asymmetry. Bank-specific catalyst DTCs are the diagnosis — gas values at tailpipe may appear deceptively normal. Source: master_catalyst_guide.md §3 (bank-specific monitor), §4 (post-cat averaging in V-engines).",
    stft_b2="-2", ltft_b2="0",
))
# --- DB-007: V-engine, B1 O2 dead B2 normal — false lean B1 ---
add(make_row(
    "DB-007", "Dual-bank: B1 O2 dead lean +25%%/B2 normal — false lean B1 only",
    "45", "0.2", "14.5", "0.4", "65", "1.01",
    "+25", "+25", "1.15", "31", "760", "92",
    "P0171",
    "V-engine",
    "O2_Sensor_Dead_Lean_B1_False", "sensor_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 45 ppm: clean. CO 0.2%%: clean. CO2 14.5%%: efficient. O2 0.4%%: low. NOx 65 ppm: moderate. Lambda 1.01: near stoich. STFT B1 +25%%/LTFT B1 +25%%: B1 trims saturated adding fuel — O2 sensor falsely reporting lean. OBD lambda 1.15: B1 O2 reads lean. STFT B2 -1%%/LTFT B2 0%%: B2 neutral. P0171: B1 lean only. Pattern: B1 upstream O2 sensor failed reading permanently lean (0 mV output). ECU adds fuel to B1 trying to correct false lean → B1 runs rich but O2 still reports lean → trims saturate. B2 runs normally. Gas chemistry from tailpipe (averaged) may appear near-normal because B2 dilutes B1's excess fuel. Source: master_o2_sensor_guide.md §3 (dead lean sensor). master_fuel_trim_guide.md §4 (false lean from sensor).",
    stft_b2="-1", ltft_b2="0",
))
# --- DB-008: V-engine, both banks symmetric — normal V8 warm idle ---
add(make_row(
    "DB-008", "Dual-bank: V8 normal — both banks symmetric, clean idle",
    "25", "0.2", "15.0", "0.2", "30", "1.00",
    "-1", "+1", "1.00", "32", "680", "93",
    "",
    "V-engine",
    "no_fault", "no_fault",
    "insufficient_evidence", "0.0", "0.35",
    "false",
    "HC 25 ppm: clean. CO 0.2%%: clean. CO2 15.0%%: efficient. O2 0.2%%: low. NOx 30 ppm: low. Lambda 1.00: perfect stoich. STFT B1 -1%%/LTFT B1 +1%%, STFT B2 0%%/LTFT B2 +1%%: both banks near neutral — symmetric, healthy. No DTCs. V-engine: normal V8 warm idle. Both banks running symmetrically with near-identical fuel trims. This is the baseline healthy V-engine case for the dual-bank test set. Source: master_fuel_trim_guide.md §3 (normal trim ranges).",
    stft_b2="0", ltft_b2="+1",
))
# --- DB-009: V-engine, B1 injector clogged B2 normal — lean B1 ---
add(make_row(
    "DB-009", "Dual-bank: B1 injectors partially clogged — lean B1, B2 compensates",
    "70", "0.3", "13.5", "2.2", "150", "1.06",
    "+20", "+18", "1.05", "27", "750", "91",
    "P0171",
    "V-engine",
    "Bank_Asymmetric_Lean_B1_Clogged_Injectors", "fuel_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 70 ppm: marginal. CO 0.3%%: normal — B2 normal masks B1 lean. CO2 13.5%%: mildly depressed — averaging. O2 2.2%%: lean — B1 lean contributes excess air. NOx 150 ppm: elevated — B1 lean/hot. Lambda 1.06: lean — averaged. STFT B1 +20%%/LTFT B1 +18%%: B1 lean correction. STFT B2 -3%%/LTFT B2 -2%%: B2 slightly rich — ECU enriching B2 to maintain overall lambda target. P0171: B1 lean. Pattern: B1 injectors partially clogged → B1 runs lean → ECU adds fuel to B1 (trims positive). To maintain global lambda target, ECU may slightly enrich B2 (trims slightly negative). Bank-asymmetric trims + opposite-sign corrections are the diagnosis. Source: master_fuel_system_guide.md §3 (clogged injectors). master_fuel_trim_guide.md §4 (cross-bank compensation).",
    stft_b2="-3", ltft_b2="-2",
))
# --- DB-010: V-engine, B1 exhaust leak before O2 — false lean B1 ---
add(make_row(
    "DB-010", "Dual-bank: B1 exhaust leak pre-O2 — false lean, ECU enrichens B1",
    "55", "0.8", "14.0", "0.6", "60", "0.98",
    "+15", "+13", "1.05", "31", "770", "92",
    "P0171",
    "V-engine",
    "Exhaust_Leak_Pre_O2_B1_False_Lean", "exhaust_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 55 ppm: borderline. CO 0.8%%: slightly elevated — ECU enrichened B1. CO2 14.0%%: near efficient. O2 0.6%%: normal. NOx 60 ppm: moderate. Lambda 0.98: slightly rich — ECU over-fueled B1. STFT B1 +15%%/LTFT B1 +13%%: B1 adding fuel. OBD lambda B1 1.05: ECU sees lean (exhaust leak dilutes O2 reading). STFT B2 -2%%/LTFT B2 0%%: B2 normal. P0171: B1 lean. Pattern: B1 exhaust manifold gasket leak before upstream O2 sensor → during exhaust pulse gaps, ambient air enters and dilutes exhaust → O2 sensor reads lean → ECU adds fuel to B1 → B1 runs rich but O2 still reports lean. B2 exhaust intact → B2 trims normal. The tailpipe average is near-normal but B1 is actually rich. Source: master_o2_sensor_guide.md §3 (exhaust leak pre-O2). master_exhaust_guide.md §3 (exhaust leak diagnosis).",
    stft_b2="-2", ltft_b2="0",
))
# ============================================================
# 9 REMAINING CASES (MIX-001 to MIX-009) — reach 400
# ============================================================
# Fill gaps: fuel system, ignition, mechanical, sensor, exhaust,
# catalyst, air induction fault families not fully covered above.
# --- MIX-001: Fuel pump weak — lean under load, normal idle ---
add(make_row(
    "MIX-001", "Fuel pump weak — normal idle, lean under load, P0171 pending",
    "30", "0.2", "14.8", "0.3", "45", "1.01",
    "+5", "+10", "1.00", "32", "760", "91",
    "P0171",
    "single",
    "Fuel_Pump_Weak_Lean_Under_Load", "fuel_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 30 ppm: clean. CO 0.2%%: clean. CO2 14.8%%: efficient. O2 0.3%%: low. NOx 45 ppm: low. Lambda 1.01: near stoich at idle. STFT +5%%/LTFT +10%%: LTFT trending lean — learned correction from load conditions. P0171: pending lean DTC. Pattern: fuel pump wearing — delivers adequate volume at idle (low demand) but pressure drops under load. LTFT +10%% reflects learned correction from load-rich episodes. Idle snapshot appears near-normal — the fault is load-dependent. Diagnose with fuel pressure test under load. Source: master_fuel_system_guide.md §2 (fuel pump diagnosis). master_fuel_trim_guide.md §4 (LTFT trending).",
))
# --- MIX-002: Spark plug gap eroded — high-RPM misfire ---
add(make_row(
    "MIX-002", "Spark plug gap eroded — high-RPM misfire, idle borderline",
    "100", "0.6", "14.0", "0.8", "80", "1.01",
    "+2", "+1", "1.01", "30", "750", "89",
    "",
    "single",
    "Spark_Plug_Gap_Eroded_High_RPM_Misfire", "ignition_fault",
    "named_fault", "0.65", "0.85",
    "false",
    "HC 100 ppm: marginal (pre-misfire). CO 0.6%%: slightly elevated. CO2 14.0%%: near efficient. O2 0.8%%: normal. NOx 80 ppm: moderate. Lambda 1.01: near stoich. No DTCs: misfire below detection threshold at idle. Pattern: spark plug electrodes worn → gap exceeds spec → spark voltage required exceeds coil output at high cylinder pressure (high RPM/load). At idle, cylinder pressure is low → spark jumps gap → normal combustion. At high RPM, misfire emerges. Idle gas borderline but not diagnostic — need high-RPM gas or cylinder balance test. Source: master_ignition_guide.md §2 (spark plug wear), §4 (load-dependent misfire).",
))
# --- MIX-003: Oxygen sensor bias — rich-shifted, mild correction ---
add(make_row(
    "MIX-003", "O2 sensor rich-shifted — ECU leans engine, borderline lean",
    "35", "0.1", "13.8", "2.0", "145", "1.06",
    "-10", "-8", "0.97", "31", "755", "91",
    "",
    "single",
    "O2_Sensor_Rich_Bias_Aging_Shift", "sensor_fault",
    "named_fault", "0.65", "0.85",
    "false",
    "HC 35 ppm: clean. CO 0.1%%: clean. CO2 13.8%%: mildly depressed. O2 2.0%%: lean — ECU pulled fuel based on false-rich O2. NOx 145 ppm: elevated — lean/hot combustion. Lambda 1.06: lean. STFT -10%%/LTFT -8%%: ECU pulling fuel — O2 sensor reads rich-shifted. OBD lambda 0.97: ECU believes slightly rich → pulls fuel → actual lambda drifts lean. Pattern: aging O2 sensor with rich voltage shift → sensor reports slightly rich → ECU pulls fuel → engine runs slightly lean → NOx rises. Gas chemistry reveals the lean truth. Source: master_o2_sensor_guide.md §3 (sensor aging bias). master_fuel_trim_guide.md §5 (false rich correction).",
))
# --- MIX-004: PCV valve stuck open — internal vacuum leak ---
add(make_row(
    "MIX-004", "PCV valve stuck open — internal vacuum leak, lean idle",
    "45", "0.15", "13.5", "2.8", "165", "1.09",
    "+16", "+14", "1.08", "26", "770", "92",
    "",
    "single",
    "PCV_Valve_Stuck_Open_Vacuum_Leak", "mechanical_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 45 ppm: clean. CO 0.15%%: clean. CO2 13.5%%: mildly depressed. O2 2.8%%: lean (>2%%). NOx 165 ppm: elevated — lean/hot. Lambda 1.09: lean. STFT +16%%/LTFT +14%%: ECU adding fuel. MAP 26 kPa: low — vacuum leak signature. Pattern: PCV valve stuck open → unmetered air enters intake through crankcase → lean mixture. Unlike external vacuum leak (brake booster), PCV leak draws crankcase vapors → oil vapor may cause slight HC elevation over time. Diagnose by pinching PCV hose — idle should drop and smooth if PCV is the leak source. Source: master_air_induction_guide.md §3 (vacuum leak sources). master_mechanical_guide.md §2 (PCV system).",
))
# --- MIX-005: MAF contaminated — underreport, lean with P0171 ---
add(make_row(
    "MIX-005", "MAF contaminated — underreport, lean mixture + P0171",
    "50", "0.15", "13.2", "3.0", "175", "1.11",
    "+18", "+16", "1.10", "23", "790", "90",
    "P0171",
    "single",
    "MAF_Underreport_Dirty_HotFilm", "sensor_fault",
    "named_fault", "0.75", "0.95",
    "false",
    "HC 50 ppm: borderline. CO 0.15%%: clean. CO2 13.2%%: mildly depressed. O2 3.0%%: lean (>2%%). NOx 175 ppm: elevated — lean/hot. Lambda 1.11: lean. STFT +18%%/LTFT +16%%: ECU adding fuel — MAF underreporting airflow. MAP 23 kPa: low reading confirms actual airflow is higher than MAF reports. P0171: lean DTC. Pattern: MAF hot-film element contaminated with oil/dust from aftermarket air filter → thermal insulation → cooling airflow underestimated → MAF underreports → ECU under-fuels → true lean condition confirmed by gas. Source: master_ecu_guide.md §6.1 (MAF contamination). master_air_induction_guide.md §5 (MAF diagnosis).",
))
# --- MIX-006: Exhaust leak at manifold — false lean O2, ECU enrichens ---
add(make_row(
    "MIX-006", "Exhaust manifold leak — pre-O2, false lean, ECU enrichens",
    "60", "1.0", "14.2", "0.5", "55", "0.97",
    "+12", "+10", "1.04", "32", "760", "91",
    "",
    "single",
    "Exhaust_Manifold_Leak_Pre_O2_False_Lean", "exhaust_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 60 ppm: borderline. CO 1.0%%: slightly elevated — ECU enrichened. CO2 14.2%%: near efficient. O2 0.5%%: normal. NOx 55 ppm: moderate. Lambda 0.97: slightly rich — ECU added fuel based on false lean. STFT +12%%/LTFT +10%%: ECU adding fuel — O2 sensor sees exhaust diluted by manifold leak air → reads lean → ECU enrichens. OBD lambda 1.04: ECU believes lean. Pattern: exhaust manifold gasket leak between head and upstream O2 sensor → during negative exhaust pulses, ambient air enters → O2 sensor reads lean → ECU adds fuel → engine runs slightly rich. The gas analyser at tailpipe shows the true slightly-rich mixture. Source: master_exhaust_guide.md §3 (exhaust leak effects). master_o2_sensor_guide.md §3 (pre-O2 leak).",
))
# --- MIX-007: Catalytic converter melted — high backpressure ---
add(make_row(
    "MIX-007", "Catalytic converter melted — high backpressure, power loss, rich idle",
    "220", "2.8", "12.0", "0.8", "40", "0.91",
    "-12", "-8", "0.92", "45", "720", "92",
    "P0420",
    "single",
    "Catalytic_Converter_Melted_Backpressure", "catalyst_fault",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 220 ppm: approaching misfire — elevated backpressure. CO 2.8%%: moderately rich — restricted exhaust. CO2 12.0%%: depressed — restricted flow reduces volumetric efficiency. O2 0.8%%: normal. NOx 40 ppm: low — rich + backpressure. Lambda 0.91: rich. STFT -12%%/LTFT -8%%: ECU pulling fuel. MAP 45 kPa: elevated for idle — exhaust backpressure increases manifold pressure. P0420: catalyst efficiency. Pattern: catalytic converter substrate melted (from prolonged rich operation or misfire) → exhaust flow restricted → increased backpressure → MAP elevated at idle → combustion efficiency drops → rich shift. Elevated idle MAP + P0420 + rich gas is the melted-cat signature. Source: master_catalyst_guide.md §5 (melted substrate), §6 (backpressure test). master_exhaust_guide.md §4 (restricted exhaust).",
))
# --- MIX-008: IAT sensor stuck cold — ECU enrichens, rich at warm ---
add(make_row(
    "MIX-008", "IAT sensor stuck at -30C — ECU enrichens for dense air, rich warm",
    "180", "3.0", "12.5", "0.4", "30", "0.89",
    "-14", "-11", "0.90", "34", "760", "92",
    "P0113",
    "single",
    "IAT_Sensor_Stuck_Cold_Enrichens", "sensor_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 180 ppm: marginal. CO 3.0%%: very rich — ECU computing fuel for -30C air density. CO2 12.5%%: depressed — rich combustion deficit. O2 0.4%%: low — rich consumed oxygen. NOx 30 ppm: low — rich quench. Lambda 0.89: rich. STFT -14%%/LTFT -11%%: ECU pulling fuel — O2 feedback correcting rich mixture. P0113: IAT sensor circuit high input (open circuit → reads -30C default). Pattern: IAT sensor circuit open → ECU defaults to -30C reading → calculates fuel for very dense cold air → drastically over-fuels for actual 25C ambient → engine runs rich. O2 feedback partially corrects but cannot fully compensate for gross IAT error. Source: master_ecu_guide.md §5.2 (IAT sensor failure). master_air_induction_guide.md §5 (IAT role in load calculation).",
))
# --- MIX-009: Ignition timing retarded — knock sensor false, low power ---
add(make_row(
    "MIX-009", "Ignition timing retarded — false knock sensor, low power, hot exhaust",
    "70", "0.5", "13.5", "1.2", "130", "1.03",
    "+4", "+2", "1.04", "31", "740", "93",
    "P0325",
    "single",
    "Knock_Sensor_False_Retard_Timing", "ignition_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 70 ppm: marginal — incomplete burn from retarded timing. CO 0.5%%: normal. CO2 13.5%%: mildly depressed — late combustion reduces efficiency. O2 1.2%%: normal. NOx 130 ppm: elevated — late combustion raises exhaust gas temperature → thermal NOx formation. Lambda 1.03: borderline lean — late burn leaves residual oxygen. P0325: knock sensor 1 circuit malfunction. Pattern: knock sensor falsely reporting knock → ECU retards ignition timing → combustion occurs later in the power stroke → less work extracted → higher exhaust temperature → elevated NOx. Gas values show the secondary effects of timing retard: mild HC elevation, NOx elevation, slight efficiency loss (CO2 depression). Source: master_ignition_guide.md §3 (knock sensor), §6 (timing retard effects). master_nox_guide.md §2 (thermal NOx from timing).",
))
# ============================================================
# Write to CSV
# ============================================================
def main() -> None:
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing = list(reader)
    print(f"Existing rows: {len(existing)}")
    for case in CASES:
        assert case["case_id"], "Missing case_id"
        assert case["expected_top_fault"], f"Missing expected_top_fault for {case['case_id']}"
        assert case["expected_state"] in ("named_fault", "insufficient_evidence"), \
            f"Invalid expected_state for {case['case_id']}: {case['expected_state']}"
        assert case["reasoning"], f"Missing reasoning for {case['case_id']}"
    print(f"New cases: {len(CASES)}")
    print(f"Total after append: {len(existing) + len(CASES)}")
    # Verify case ID uniqueness
    existing_ids = {r["case_id"] for r in existing}
    new_ids = {c["case_id"] for c in CASES}
    overlap = existing_ids & new_ids
    if overlap:
        print(f"ERROR: Duplicate case IDs: {overlap}")
        return
    print("Case ID uniqueness: PASS")
    # Distribution check
    ff_count = sum(1 for c in CASES if c["case_id"].startswith("FF-"))
    cs_count = sum(1 for c in CASES if c["case_id"].startswith("CS-"))
    era_count = sum(1 for c in CASES if c["case_id"].startswith("ERA-"))
    db_count = sum(1 for c in CASES if c["case_id"].startswith("DB-"))
    mix_count = sum(1 for c in CASES if c["case_id"].startswith("MIX-"))
    print(f"\nDistribution: FF={ff_count}, CS={cs_count}, ERA={era_count}, DB={db_count}, MIX={mix_count}")
    # Petrol-only check
    for case in CASES:
        combined = (case["description"] + case["reasoning"]).lower()
        for token in ["diesel", "lpg", "cng", "e85", "hybrid"]:
            assert token not in combined, f"PETROL-ONLY VIOLATION: {token} in {case['case_id']}"
    print("Petrol-only check: PASS")
    # Append
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLS)
        writer.writerows(CASES)
    print(f"\nAppended {len(CASES)} rows to {CSV_PATH}")
    total = len(existing) + len(CASES)
    print(f"New total: {total} data rows + 1 header = {total + 1} lines")
    print(f"Target: 400 data rows (401 lines) — {'MATCH' if total == 400 else 'OFF BY ' + str(total - 400)}")
if __name__ == "__main__":
    main()
