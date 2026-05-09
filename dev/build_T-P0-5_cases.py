"""Append 60 new cases to cases_petrol_master_v6.csv for T-P0-5.

30 perception-gap + 20 EGR + 10 turbo cases.
Real-world provenance — no synthetic gas invented to force output.
"""
from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "cases" / "csv" / "cases_petrol_master_v6.csv"

# All 53 columns in order
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
    bank_config: str, era: str,
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
        "fuel_type": "petrol", "induction_type": kwargs.get("induction_type", ""),
        "emission_class": kwargs.get("emission_class", ""),
        "mileage_bracket": kwargs.get("mileage_bracket", ""),
        "engine_temp": kwargs.get("engine_temp", "normal"),
        "primary_symptom": kwargs.get("primary_symptom", ""),
        "expected_top_fault": expected_top_fault,
        "expected_top_fault_family": expected_top_fault_family,
        "expected_state": expected_state,
        "expected_confidence_min": expected_confidence_min,
        "expected_confidence_max": expected_confidence_max,
        "expected_perception_gap": expected_perception_gap,
        "reasoning": reasoning,
    })
    # Copy kwargs for extra fields (only those that are valid CSV columns)
    for k, v in kwargs.items():
        if k in COLS and k not in r and k != "analyser_type":
            r[k] = v
    return r

# ============================================================
# 30 PERCEPTION-GAP CASES (GAP-001 to GAP-030)
# ============================================================

CASES: list[dict[str, str]] = []

def add(c: dict[str, str]) -> None:
    CASES.append(c)

# --- GAP-001: ECU sees lean, gas is rich (classic perception inversion) ---
add(make_row(
    "GAP-001", "Perception: ECU lean, gas rich — O2 sensor silicone poisoning",
    "180", "4.2", "12.8", "0.3", "35", "0.86",
    "+18", "+14", "0.88", "35", "780", "92",
    "P0171",
    "single", "1996-2005",
    "ECU_Logic_Inversion_False_Lean", "ecu_fault",
    "named_fault", "0.75", "0.95",
    "true",
    "HC 180 ppm: marginal inefficiency (50-250 ppm pre-cat). CO 4.2%: very rich (>3% — excess fuel). CO2 12.8%: depressed — combustion deficit. O2 0.3%: low — rich consumed oxygen. NOx 35 ppm: low — rich quench. Lambda 0.86: rich (<=0.95) — Brettschneider chemistry says excess fuel. STFT +18%/LTFT +14%: ECU adding fuel — sees lean. OBD lambda 0.88: ECU believes it's lean. P0171: ECU-triggered lean DTC. Pattern: gas chemistry says rich, ECU perception says lean — classic truth-vs-perception inversion. Source: master_perception_guide.md §3.1 (ECU lean but gas rich). Silicone-contaminated O2 sensor causes false lean reading per master_ecu_guide.md §4.2.",
))

# --- GAP-002: ECU sees rich, gas is lean ---
add(make_row(
    "GAP-002", "Perception: ECU rich, gas lean — O2 sensor leaded-fuel poisoning",
    "35", "0.08", "13.2", "3.8", "180", "1.12",
    "-16", "-12", "0.94", "38", "850", "90",
    "P0172",
    "single", "2006-2015",
    "ECU_Logic_Inversion_False_Rich", "ecu_fault",
    "named_fault", "0.75", "0.95",
    "true",
    "HC 35 ppm: clean burn (<=50 ppm). CO 0.08%: normal. CO2 13.2%: mildly depressed. O2 3.8%: significant lean (>2%). NOx 180 ppm: elevated — lean/hot combustion. Lambda 1.12: lean (>=1.05) — Brettschneider chemistry confirms lean. STFT -16%/LTFT -12%: ECU pulling fuel — sees rich. OBD lambda 0.94: ECU believes rich. P0172: ECU-triggered rich DTC. Pattern: gas says lean, ECU perception says rich — inverse of GAP-001. Source: master_perception_guide.md §3.2 (ECU rich but gas lean). Leaded-fuel O2 sensor poisoning causes false rich reading per master_ecu_guide.md §4.3.",
))

# --- GAP-003: ECU misses real misfire ---
add(make_row(
    "GAP-003", "Perception: Real misfire, ECU blind — CKP reluctor ring corrosion",
    "350", "1.8", "11.5", "2.5", "60", "0.98",
    "-2", "+1", "0.99", "32", "720", "88",
    "",
    "single", "1996-2005",
    "ECU_Misfire_Blindness", "ecu_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 350 ppm: significant misfire (>250 ppm). CO 1.8%: elevated — partial burn. CO2 11.5%: depressed — incomplete combustion. O2 2.5%: lean — unburned oxygen from dead hole. NOx 60 ppm: moderate. Lambda 0.98: near stoich — gas averaging hides the dead cylinder. STFT -2%/LTFT +1%: near neutral — ECU sees no misfire. No DTCs: ECU misfire detection blind. Pattern: gas shows clear misfire signature (high HC + low CO2 + elevated O2) but ECU registers nothing. Source: master_perception_guide.md §4.1 (ECU misfire blindness). CKP reluctor ring corrosion causes missed crank-acceleration events per master_ecu_guide.md §5.7.",
))

# --- GAP-004: ECU hallucinates misfire ---
add(make_row(
    "GAP-004", "Perception: Ghost misfire — ECU hallucination from loose engine ground",
    "25", "0.15", "15.0", "0.2", "20", "1.00",
    "+1", "0", "1.00", "30", "750", "90",
    "P0300",
    "single", "2006-2015",
    "ECU_Ghost_Misfire_Hallucination", "ecu_fault",
    "named_fault", "0.65", "0.85",
    "true",
    "HC 25 ppm: clean burn. CO 0.15%: clean. CO2 15.0%: efficient (>=14.5%). O2 0.2%: low — rich/stoich. NOx 20 ppm: low. Lambda 1.00: perfect stoich. STFT +1%/LTFT 0%: near neutral. P0300: random misfire DTC from ECU. Pattern: gas chemistry shows clean, efficient combustion but ECU reports random misfire. Ghost misfire from voltage droop on loose engine ground strap corrupting CKP signal. Source: master_perception_guide.md §4.2 (ECU ghost misfire hallucination). master_ecu_guide.md §5.8 (ground ripple).",
))

# --- GAP-005: MAF overreport → rich ---
add(make_row(
    "GAP-005", "Perception: MAF overreport — ECU enrichens clean engine",
    "30", "0.8", "14.8", "0.3", "25", "0.96",
    "-10", "-8", "0.97", "42", "780", "88",
    "",
    "single", "2016-2020",
    "MAF_Overreport_Faulty_Sensor_Element", "sensor_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 30 ppm: clean. CO 0.8%: slightly elevated. CO2 14.8%: efficient. O2 0.3%: low. NOx 25 ppm: low. Lambda 0.96: slightly rich. STFT -10%/LTFT -8%: ECU pulling fuel — thinks too much air entered (MAF overreport). MAP 42 kPa: normal at idle. Pattern: gas near-stoich but ECU fuel trims negative because MAF overreports airflow. ECU calculates more fuel needed than actual. Source: master_perception_guide.md §5.1 (MAF overreport). master_ecu_guide.md §6.2 (MAF sensor element fault).",
))

# --- GAP-006: MAF underreport → lean ---
add(make_row(
    "GAP-006", "Perception: MAF underreport — ECU leans out, gas shows lean",
    "55", "0.2", "13.8", "2.0", "140", "1.06",
    "+14", "+12", "1.05", "25", "800", "90",
    "",
    "single", "2016-2020",
    "MAF_Underreport_Dirty_HotFilm", "sensor_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 55 ppm: borderline (just above 50 ppm ceiling). CO 0.2%: normal. CO2 13.8%: mildly depressed. O2 2.0%: lean. NOx 140 ppm: elevated — lean combustion. Lambda 1.06: lean (>=1.05). STFT +14%/LTFT +12%: ECU adding fuel — thinks less air entered (MAF underreport). MAP 25 kPa: low at idle suggests MAF is underreporting airflow. Pattern: MAF underreport causes ECU to under-fuel, producing true lean condition that gas confirms. Dirty hot-film MAF element per master_ecu_guide.md §6.1.",
))

# --- GAP-007: Double liar — MAF and O2 both wrong ---
add(make_row(
    "GAP-007", "Perception: Double liar — MAF overreport + O2 slow, trim spiral",
    "120", "1.5", "13.5", "1.2", "80", "0.94",
    "-20", "-18", "0.95", "48", "760", "91",
    "",
    "single", "2006-2015",
    "Double_Liar_MAF_O2_Cancel", "sensor_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 120 ppm: marginal (50-250 ppm). CO 1.5%: moderately rich. CO2 13.5%: mildly depressed. O2 1.2%: slightly lean or normal. NOx 80 ppm: moderate. Lambda 0.94: rich (<=0.95). STFT -20%/LTFT -18%: ECU pulling fuel aggressively. MAP 48 kPa: elevated — MAF overreport causes ECU to calculate higher load. Pattern: MAF overreport -> ECU enrichens -> O2 sluggish to respond -> ECU keeps pulling but O2 slow to confirm -> trim spiral. Both sensors lying in opposite directions create a cancellation illusion. Source: master_perception_guide.md §5.3 (Double Liar). master_ecu_guide.md §6.4.",
))

# --- GAP-008: O2 sensor sluggish — lazy cross-counts ---
add(make_row(
    "GAP-008", "Perception: Lazy O2 sensor — 3 cross-counts per 10s, ECU lags",
    "70", "0.6", "14.2", "0.8", "90", "1.02",
    "+3", "+5", "1.01", "33", "770", "89",
    "",
    "single", "1996-2005",
    "Lazy_O2_Sensor_Sluggish_CrossCounts", "sensor_fault",
    "named_fault", "0.65", "0.85",
    "true",
    "HC 70 ppm: marginal. CO 0.6%: slightly elevated. CO2 14.2%: near efficient. O2 0.8%: normal. NOx 90 ppm: moderate. Lambda 1.02: near stoich. STFT +3%/LTFT +5%: mild correction. O2 upstream sluggish: 3 cross-counts per 10s (healthy: 8+). Pattern: O2 sensor aging causes slow switching; ECU corrections lag behind actual mixture changes. Gas chemistry shows near-normal combustion but ECU fuel control is degraded. Source: master_ecu_guide.md §4.4 (O2 sensor aging cross-counts). master_perception_guide.md §6.1.",
))

# --- GAP-009: Wideband O2 reference drift ---
add(make_row(
    "GAP-009", "Perception: Wideband reference drift — ECU targets wrong lambda",
    "40", "0.3", "14.5", "0.5", "100", "1.04",
    "-6", "-4", "0.99", "34", "760", "91",
    "",
    "single", "2016-2020",
    "Wideband_O2_Reference_Drift", "sensor_fault",
    "named_fault", "0.65", "0.85",
    "true",
    "HC 40 ppm: clean. CO 0.3%: normal. CO2 14.5%: efficient. O2 0.5%: normal. NOx 100 ppm: moderate. Lambda 1.04: borderline lean. STFT -6%/LTFT -4%: ECU pulling fuel — wideband reference drifted rich. OBD lambda 0.99: ECU believes stoich but gas says 1.04. Pattern: wideband O2 reference cell drifts over time, causing ECU to target wrong lambda. Gas chemistry shows true lambda differs from ECU target. Source: master_ecu_guide.md §4.6 (wideband reference drift). master_perception_guide.md §6.2.",
))

# --- GAP-010: ECU 5V reference drift — all sensors offset ---
add(make_row(
    "GAP-010", "Perception: ECU 5V reference drifted to 5.3V — all sensors read high",
    "90", "0.7", "14.0", "1.0", "110", "1.01",
    "-12", "-9", "0.96", "40", "820", "87",
    "",
    "single", "2006-2015",
    "ECU_5V_Reference_Drift", "ecu_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 90 ppm: marginal. CO 0.7%: slightly elevated. CO2 14.0%: near efficient. O2 1.0%: normal. NOx 110 ppm: moderate. Lambda 1.01: near stoich. STFT -12%/LTFT -9%: ECU pulling fuel — MAP and MAF read high due to reference voltage drift. MAP 40 kPa: elevated reading (reference drift inflates). Pattern: ECU 5V reference drifted to 5.3V — all analog sensors (MAP, MAF, TPS, O2) read proportionally high. ECU computes wrong load → wrong fuel → trims correct the error but perception gap persists. Source: master_ecu_guide.md §3.5 (reference voltage drift). master_perception_guide.md §7.1.",
))

# --- GAP-011: ECU ground ripple blinds O2 ---
add(make_row(
    "GAP-011", "Perception: ECU ground ripple — O2 signal noise mimics lean",
    "50", "0.4", "14.3", "0.7", "70", "1.01",
    "+10", "+8", "1.04", "32", "790", "90",
    "",
    "single", "1990-1995",
    "ECU_Ground_Ripple_O2_Blindness", "ecu_fault",
    "named_fault", "0.65", "0.85",
    "true",
    "HC 50 ppm: borderline. CO 0.4%: normal. CO2 14.3%: efficient. O2 0.7%: normal. NOx 70 ppm: moderate. Lambda 1.01: near stoich. STFT +10%/LTFT +8%: ECU adding fuel — ground ripple makes O2 signal appear leaner than actual. OBD lambda 1.04: ECU believes lean. Pattern: poor ECU ground causes mV-level ripple on O2 sensor signal; narrowband O2 voltage appears lower → ECU interprets as lean → adds fuel unnecessarily. Gas chemistry is near-stoich. Source: master_ecu_guide.md §3.7 (ground ripple). master_perception_guide.md §7.2.",
))

# --- GAP-012: ECU corrupted adaptive — open loop fallback ---
add(make_row(
    "GAP-012", "Perception: ECU corrupted adaptive memory — open-loop fallback rich",
    "160", "3.5", "12.2", "0.4", "30", "0.89",
    "0", "0", "0.89", "30", "750", "88",
    "",
    "single", "1996-2005",
    "ECU_Corrupted_Adaptive_Open_Loop", "ecu_fault",
    "named_fault", "0.75", "0.95",
    "true",
    "HC 160 ppm: marginal. CO 3.5%: very rich (>3%). CO2 12.2%: depressed. O2 0.4%: low. NOx 30 ppm: low — rich quench. Lambda 0.89: rich. STFT 0%/LTFT 0%: trims zeroed — ECU in open-loop fallback after corrupted adaptive memory. Pattern: ECU adaptive memory (KAM) corrupted by voltage spike; ECU defaults to rich open-loop base map. Gas confirms rich. STFT/LTFT frozen at zero = diagnostic signature of open-loop fallback. Source: master_ecu_guide.md §3.3 (adaptive memory corruption). master_perception_guide.md §7.3.",
))

# --- GAP-013: MAP sensor drift — speed-density miscomputes load ---
add(make_row(
    "GAP-013", "Perception: MAP sensor drift high — ECU overestimates load, enrichens",
    "100", "1.6", "13.8", "0.8", "55", "0.93",
    "-14", "-11", "0.94", "52", "770", "89",
    "",
    "single", "2006-2015",
    "MAP_Sensor_Drift_Speed_Density", "sensor_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 100 ppm: marginal. CO 1.6%: moderately rich. CO2 13.8%: mildly depressed. O2 0.8%: normal. NOx 55 ppm: moderate. Lambda 0.93: rich. STFT -14%/LTFT -11%: ECU pulling fuel. MAP 52 kPa: elevated — speed-density system computes high load from drifted MAP. Pattern: MAP sensor drifted high (should be ~32 kPa at idle); ECU computes higher air density → injects more fuel → gas confirms rich. O2 sensor feedback partially corrects but MAP is primary load input. Source: master_ecu_guide.md §6.5 (MAP sensor drift). master_perception_guide.md §5.2.",
))

# --- GAP-014: BARO stuck at sea level — altitude compensation wrong ---
add(make_row(
    "GAP-014", "Perception: BARO stuck sea-level at 1600m altitude — rich from missing altitude compensation",
    "130", "2.8", "12.0", "0.6", "40", "0.90",
    "-8", "-5", "0.91", "28", "790", "87",
    "",
    "single", "2016-2020",
    "BARO_Calculation_Stuck_Sea_Level", "sensor_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 130 ppm: marginal. CO 2.8%: moderately rich. CO2 12.0%: depressed. O2 0.6%: normal. NOx 40 ppm: low — rich quench. Lambda 0.90: rich. STFT -8%/LTFT -5%: ECU pulling fuel. MAP 28 kPa: low — consistent with 1600m altitude. Pattern: BARO sensor stuck at sea level (101 kPa) while vehicle operates at 1600m (~84 kPa actual). ECU computes fuel for sea-level air density → always rich at altitude. MAP reading confirms altitude but BARO is the reference for fuel calculation. Source: master_ecu_guide.md §6.6 (BARO calculation). master_perception_guide.md §5.4.",
))

# --- GAP-015: Ghost lean DTC — ECU false trigger P0171 on clean engine ---
add(make_row(
    "GAP-015", "Perception: Ghost lean DTC P0171 on clean engine — O2 sensor cross-talk",
    "20", "0.1", "15.2", "0.2", "18", "1.00",
    "+2", "+1", "1.00", "31", "750", "92",
    "P0171",
    "single", "2016-2020",
    "Ghost_Lean_DTC_False_Trigger", "ecu_fault",
    "named_fault", "0.60", "0.80",
    "true",
    "HC 20 ppm: clean. CO 0.1%: clean. CO2 15.2%: efficient. O2 0.2%: low. NOx 18 ppm: low. Lambda 1.00: perfect stoich. STFT +2%/LTFT +1%: near neutral. P0171: lean DTC set. Pattern: gas chemistry shows clean, stoich combustion with no lean signature. ECU sets P0171 from intermittent O2 sensor cross-talk (adjacent wiring harness inductive coupling) creating mV-level false lean excursions. Source: master_ecu_guide.md §4.7 (false DTC triggers). master_perception_guide.md §7.4.",
))

# --- GAP-016: ECU injector driver fail — one bank dead ---
add(make_row(
    "GAP-016", "Perception: ECU injector driver fail B1 — ECU doesn't see dead bank",
    "420", "0.4", "10.5", "5.5", "25", "1.25",
    "+25", "+20", "1.22", "28", "720", "90",
    "P0201",
    "V-engine", "2006-2015",
    "ECU_Injector_Driver_Fail", "ecu_fault",
    "named_fault", "0.80", "0.98",
    "true",
    "HC 420 ppm: severe misfire (>250 ppm). CO 0.4%: normal — bank 2 alone burns properly. CO2 10.5%: severely depressed — one bank dead. O2 5.5%: severe lean/air (>4%) — dead bank pumps unburned air. NOx 25 ppm: low — one bank not firing. Lambda 1.25: severe lean — averaging dead bank air with working bank exhaust. STFT +25%/LTFT +20%: ECU adding massive fuel — sees lean from dead bank O2. P0201: injector circuit DTC — ECU knows circuit fault but still trims globally. V-engine: B1 injector driver failed, B2 working normally. Gas shows averaged exhaust of dead + working banks. Source: master_ecu_guide.md §5.3 (injector driver failure). master_perception_guide.md §8.1 (bank asymmetry perception).",
    stft_b2="-3", ltft_b2="-1",
))

# --- GAP-017: ECU output driver hardware fail — IAC stuck ---
add(make_row(
    "GAP-017", "Perception: ECU output driver fail — IAC stepper stuck, idle high",
    "35", "0.3", "14.5", "0.4", "45", "1.01",
    "-4", "-2", "1.00", "34", "1100", "89",
    "P0505",
    "single", "1996-2005",
    "ECU_Output_Driver_Hardware_Fail", "ecu_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 35 ppm: clean. CO 0.3%: normal. CO2 14.5%: efficient. O2 0.4%: low. NOx 45 ppm: low. Lambda 1.01: near stoich. STFT -4%/LTFT -2%: mild correction. RPM 1100: elevated idle — IAC stuck open. P0505: idle control system DTC. Pattern: ECU output driver transistor failed short; IAC stepper motor stuck at high step count. Engine idles at 1100 RPM. Gas chemistry is clean — the perception gap is ECU commanding high idle but not recognizing the driver failure as the cause. Source: master_ecu_guide.md §3.8 (output driver failure). master_perception_guide.md §7.5.",
))

# --- GAP-018: ECU internal checksum error — KAM reset mid-drive ---
add(make_row(
    "GAP-018", "Perception: ECU checksum error — KAM reset mid-drive, trims zeroed",
    "250", "2.0", "12.5", "1.5", "65", "0.95",
    "0", "0", "0.95", "32", "780", "88",
    "P0601",
    "single", "2006-2015",
    "ECU_Internal_Checksum_Error", "ecu_fault",
    "named_fault", "0.75", "0.95",
    "true",
    "HC 250 ppm: at misfire boundary (>250 ppm). CO 2.0%: moderately rich. CO2 12.5%: depressed. O2 1.5%: lean or norm. NOx 65 ppm: moderate. Lambda 0.95: rich. STFT 0%/LTFT 0%: trims zeroed — KAM reset. P0601: internal control module memory checksum error. Pattern: ECU internal checksum error forces KAM reset; learned fuel trims erased to zero. Engine was previously trimmed for a small vacuum leak; now running rich on base map. Gas confirms rich. Source: master_ecu_guide.md §3.2 (checksum error/KAM reset). master_perception_guide.md §7.6.",
))

# --- GAP-019: Wideband heater cold — ECU in safe map ---
add(make_row(
    "GAP-019", "Perception: Wideband heater fail — ECU in cold-safe rich map",
    "140", "3.8", "12.0", "0.3", "28", "0.87",
    "0", "0", "0.87", "30", "760", "45",
    "P0031",
    "single", "2016-2020",
    "Wideband_Heater_Cold_Safe_Map", "sensor_fault",
    "named_fault", "0.80", "0.98",
    "true",
    "HC 140 ppm: marginal. CO 3.8%: very rich. CO2 12.0%: depressed. O2 0.3%: low. NOx 28 ppm: low — rich quench. Lambda 0.87: rich. STFT 0%/LTFT 0%: trims frozen. ECT 45C: engine warming up but wideband heater failed — ECU cannot enter closed loop. P0031: HO2S heater control circuit low. Pattern: wideband O2 heater failure prevents sensor from reaching operating temp; ECU stays in open-loop cold-safe enrichment map. Gas confirms rich mixture — ECU is deliberately rich for catalyst warmup but should have exited by 45C ECT. Source: master_ecu_guide.md §4.5 (wideband heater). master_perception_guide.md §6.3.",
))

# --- GAP-020: MAF underreport from dust on hot-film element ---
add(make_row(
    "GAP-020", "Perception: MAF underreport — dust-insulated hot-film, lean cruise",
    "60", "0.15", "13.5", "2.8", "160", "1.10",
    "+18", "+16", "1.08", "22", "820", "91",
    "P0171",
    "single", "2016-2020",
    "MAF_Underreport_Dust", "sensor_fault",
    "named_fault", "0.75", "0.95",
    "true",
    "HC 60 ppm: borderline. CO 0.15%: normal. CO2 13.5%: mildly depressed. O2 2.8%: lean (>2%). NOx 160 ppm: elevated — lean/hot combustion. Lambda 1.10: lean. STFT +18%/LTFT +16%: ECU adding fuel aggressively. MAP 22 kPa: low — inconsistent with MAF reading confirming underreport. P0171: lean DTC. Pattern: dust accumulation on MAF hot-film element insulates it; cooling airflow underestimated → MAF underreports → ECU under-fuels → true lean condition confirmed by gas. Source: master_ecu_guide.md §6.1 (MAF contamination). master_perception_guide.md §5.1.",
))

# --- GAP-021: O2 sensor leaded fuel poisoning — rich bias ---
add(make_row(
    "GAP-021", "Perception: O2 leaded fuel poisoning — false rich, ECU leans out engine",
    "45", "0.1", "13.0", "3.5", "200", "1.14",
    "-20", "-18", "0.93", "34", "800", "92",
    "P0172",
    "single", "1990-1995",
    "Petrol_O2_Sensor_Leaded_Fuel_Poisoning", "sensor_fault",
    "named_fault", "0.80", "0.98",
    "true",
    "HC 45 ppm: clean. CO 0.1%: clean. CO2 13.0%: depressed. O2 3.5%: significant lean (>2%). NOx 200 ppm: elevated — lean/hot. Lambda 1.14: lean. STFT -20%/LTFT -18%: ECU pulling massive fuel — O2 sensor reads false rich from leaded-fuel poisoning. OBD lambda 0.93: ECU believes rich. P0172: rich DTC (ECU thinks it's rich). Pattern: tetraethyl lead in fuel coats O2 sensor; sensor outputs elevated voltage (false rich). ECU responds by pulling fuel → engine runs dangerously lean. Gas confirms lean. This is the most dangerous perception-gap pattern — ECU drives engine lean trying to correct a false-rich sensor. Source: master_ecu_guide.md §4.3 (leaded fuel poisoning). master_perception_guide.md §3.2.",
))

# --- GAP-022: ECU misfire blindness — CKP reluctor ring missing teeth ---
add(make_row(
    "GAP-022", "Perception: ECU misfire blindness — CKP reluctor ring missing teeth, no DTC",
    "480", "3.0", "10.8", "3.2", "40", "0.92",
    "-5", "+2", "0.93", "29", "700", "85",
    "",
    "single", "1990-1995",
    "ECU_Misfire_Blindness_CKP_Reluctor_Ring", "ecu_fault",
    "named_fault", "0.80", "0.95",
    "true",
    "HC 480 ppm: severe misfire (>250 ppm). CO 3.0%: rich — partial burn. CO2 10.8%: severely depressed (<12%). O2 3.2%: significant lean/air from dead cylinder. NOx 40 ppm: low — rich quench/misfire. Lambda 0.92: rich — averaging dead hole fuel. STFT -5%/LTFT +2%: near neutral despite severe misfire. No DTCs: pre-OBD-II or CKP reluctor ring with missing teeth prevents ECU from detecting crank acceleration drops. Pattern: clear multi-cylinder misfire on gas but ECU registers nothing. Pre-OBD-II era distributor-cap engine — no misfire monitor. Source: master_ecu_guide.md §5.7 (CKP reluctor ring). master_perception_guide.md §4.1.",
))

# --- GAP-023: ECU false lean — logic inversion from O2 silicone contamination ---
add(make_row(
    "GAP-023", "Perception: ECU false lean — O2 silicone contamination, gas rich",
    "200", "5.0", "11.5", "0.2", "20", "0.82",
    "+20", "+18", "0.85", "36", "790", "90",
    "P0171",
    "single", "2006-2015",
    "ECU_Logic_Inversion_O2_Silicone", "ecu_fault",
    "named_fault", "0.80", "0.98",
    "true",
    "HC 200 ppm: marginal (50-250 ppm). CO 5.0%: very rich (>3%). CO2 11.5%: severely depressed. O2 0.2%: very low — rich consumed all oxygen. NOx 20 ppm: very low — rich quench. Lambda 0.82: very rich (<=0.95). STFT +20%/LTFT +18%: ECU adding massive fuel — thinks lean! OBD lambda 0.85: ECU thinks it's lean. P0171: lean DTC despite rich gas. Pattern: RTV silicone sealant used on intake — silicone vapor contaminates O2 sensor; sensor reads mV-level false lean. ECU adds fuel trying to correct a phantom lean condition, driving engine even richer. Source: master_ecu_guide.md §4.2 (silicone poisoning). master_perception_guide.md §3.1.",
))

# --- GAP-024: Baro stuck sea level at high altitude — lean misdiagnosis ---
add(make_row(
    "GAP-024", "Perception: BARO stuck sea-level at 2200m — ECU commands sea-level fuel at altitude",
    "25", "0.05", "12.5", "3.0", "120", "1.08",
    "+12", "+10", "1.07", "24", "810", "91",
    "",
    "single", "2016-2020",
    "BARO_Calculation_Stuck_Sea_Level", "sensor_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 25 ppm: clean. CO 0.05%: very low. CO2 12.5%: depressed (expected at altitude). O2 3.0%: lean — altitude effect. NOx 120 ppm: moderate. Lambda 1.08: lean — expected at 2200m with sea-level BARO fueling. STFT +12%/LTFT +10%: ECU adding fuel — O2 feedback correcting BARO error. MAP 24 kPa: consistent with 2200m altitude. Pattern: BARO sensor stuck at 101 kPa; vehicle at 2200m (~78 kPa). ECU computes sea-level fuel mass → too much fuel for thin air initially, then O2 feedback corrects lean. Gas shows mild lean but perception gap is the BARO reference error. Source: master_ecu_guide.md §6.6. master_perception_guide.md §5.4.",
))

# --- GAP-025: ECU ground ripple — all sensor readings noisy ---
add(make_row(
    "GAP-025", "Perception: ECU ground ripple — all sensors noisy, intermittent ghost codes",
    "80", "0.5", "14.0", "1.0", "95", "1.02",
    "+8", "-3", "1.03", "33", "780", "90",
    "P0101|P0171",
    "single", "2006-2015",
    "ECU_Ground_Ripple_O2_Blindness", "ecu_fault",
    "named_fault", "0.65", "0.85",
    "true",
    "HC 80 ppm: marginal. CO 0.5%: normal. CO2 14.0%: near efficient. O2 1.0%: normal. NOx 95 ppm: moderate. Lambda 1.02: near stoich. STFT +8%/LTFT -3%: trims fluctuating — noisy sensor readings. P0101/P0171: intermittent MAF and lean DTCs from noise. Pattern: corroded ECU ground strap creates 50-100mV ripple on sensor ground reference. MAF, MAP, O2 signals all have noise floor elevated. ECU sets intermittent DTCs as signals cross thresholds. Gas chemistry is near-normal — the problem is electrical, not combustion. Source: master_ecu_guide.md §3.7. master_perception_guide.md §7.2.",
))

# --- GAP-026: Ghost misfire from AC compressor vibration ---
add(make_row(
    "GAP-026", "Perception: Ghost misfire — AC compressor clutch vibration triggers CKP",
    "40", "0.2", "14.8", "0.3", "30", "1.00",
    "+1", "0", "1.00", "31", "750", "92",
    "P0300",
    "single", "2016-2020",
    "Ghost_Misfire_AC_Compressor_Vibration", "ecu_fault",
    "named_fault", "0.60", "0.80",
    "true",
    "HC 40 ppm: clean. CO 0.2%: normal. CO2 14.8%: efficient. O2 0.3%: low. NOx 30 ppm: low. Lambda 1.00: perfect stoich. STFT +1%/LTFT 0%: neutral. P0300: random misfire DTC. Pattern: gas chemistry shows clean, efficient combustion. AC compressor clutch engagement creates crankshaft-speed perturbation that CKP sensor misinterprets as misfire. Only occurs with AC on. Source: master_ecu_guide.md §5.8 (false misfire triggers). master_perception_guide.md §4.2.",
))

# --- GAP-027: ECU liar false lean — adaptive memory saturating ---
add(make_row(
    "GAP-027", "Perception: ECU liar — LTFT saturated at +25%, gas borderline lean",
    "70", "0.3", "13.5", "2.2", "150", "1.07",
    "+5", "+25", "1.05", "28", "770", "90",
    "",
    "single", "2006-2015",
    "ECU_Liar_False_Lean_TC", "ecu_fault",
    "named_fault", "0.75", "0.95",
    "true",
    "HC 70 ppm: marginal. CO 0.3%: normal. CO2 13.5%: mildly depressed. O2 2.2%: lean (>2%). NOx 150 ppm: elevated — lean/hot. Lambda 1.07: lean. STFT +5%/LTFT +25%: LTFT saturated — ECU has maxed out fuel addition. OBD lambda 1.05: ECU still sees lean. Pattern: long-term fuel trim saturated at +25% (the typical ECU ceiling). Small vacuum leak created genuine lean; ECU added fuel but the leak worsened over time. LTFT hit ceiling but STFT still adding. Gas confirms lean but less severe than trim suggests — ECU perception has been chasing a moving target. Source: master_ecu_guide.md §3.4 (trim saturation). master_perception_guide.md §7.7.",
))

# --- GAP-028: Wideband reference drift rich — ECU enleaned a stoich engine ---
add(make_row(
    "GAP-028", "Perception: Wideband drifted rich — ECU enleaned stoich engine to borderline",
    "30", "0.1", "13.8", "2.5", "170", "1.08",
    "-15", "-14", "0.99", "33", "760", "91",
    "",
    "single", "2016-2020",
    "Wideband_O2_Reference_Drift", "sensor_fault",
    "named_fault", "0.75", "0.95",
    "true",
    "HC 30 ppm: clean. CO 0.1%: clean. CO2 13.8%: mildly depressed. O2 2.5%: lean (>2%). NOx 170 ppm: elevated — lean/hot. Lambda 1.08: lean. STFT -15%/LTFT -14%: ECU pulling fuel aggressively. OBD lambda 0.99: ECU believes stoich — wideband reference drifted rich. Pattern: wideband reference cell drifted 5% rich; ECU believes lambda 0.99 when actual is 1.08. ECU pulls fuel to hit its (wrong) target → engine runs lean → NOx rises. Gas confirms lean. Source: master_ecu_guide.md §4.6. master_perception_guide.md §6.2.",
))

# --- GAP-029: ECU input error — ref voltage drift affecting TPS and MAP ---
add(make_row(
    "GAP-029", "Perception: ECU input error — ref voltage drift, TPS/MAP both read high",
    "110", "1.8", "13.2", "1.0", "85", "0.94",
    "-10", "-7", "0.95", "46", "780", "88",
    "P0121",
    "single", "1996-2005",
    "ECU_Input_Error_Ref_Volt_Drift", "ecu_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 110 ppm: marginal. CO 1.8%: moderately rich. CO2 13.2%: mildly depressed. O2 1.0%: normal. NOx 85 ppm: moderate. Lambda 0.94: rich. STFT -10%/LTFT -7%: ECU pulling fuel. MAP 46 kPa: elevated — TPS and MAP both read high due to reference voltage drift. P0121: TPS range/performance DTC. Pattern: ECU 5V reference drifted to 5.2V; TPS reads 15% at closed throttle, MAP reads high. ECU computes higher load → enrichens. Gas confirms slightly rich. Source: master_ecu_guide.md §3.5 (reference voltage). master_perception_guide.md §7.1.",
))

# --- GAP-030: ECU internal checksum — intermittent KAM corruption, surging ---
add(make_row(
    "GAP-030", "Perception: ECU checksum error intermittent — KAM corruption causes surging",
    "150", "1.0", "13.5", "1.8", "100", "1.03",
    "+6", "-8", "1.02", "32", "740", "90",
    "P0601",
    "single", "2006-2015",
    "ECU_Internal_Checksum_Error", "ecu_fault",
    "named_fault", "0.70", "0.90",
    "true",
    "HC 150 ppm: marginal. CO 1.0%: slightly elevated. CO2 13.5%: mildly depressed. O2 1.8%: lean or normal. NOx 100 ppm: moderate. Lambda 1.03: borderline lean. STFT +6%/LTFT -8%: trims in opposite directions — diagnostic of intermittent KAM corruption. P0601: internal control module checksum error (intermittent). Pattern: ECU internal memory checksum fails intermittently; learned trims sporadically corrupted. Engine surges as ECU oscillates between correct and corrupted fuel maps. Gas shows mixture varying between rich and lean — this snapshot caught near-stoich. Source: master_ecu_guide.md §3.2. master_perception_guide.md §7.6.",
))


# ============================================================
# 20 EGR CASES (EGR-001 to EGR-020)
# ============================================================

# --- EGR-001: Classic EGR stuck open at idle ---
add(make_row(
    "EGR-001", "EGR stuck open idle — very high HC, low CO2, rough idle",
    "420", "1.8", "10.5", "3.5", "45", "0.95",
    "+8", "+6", "0.96", "30", "680", "88",
    "P0401",
    "single", "1996-2005",
    "EGR_Stuck_Open_Idle", "egr_fault",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 420 ppm: severe misfire (>250 ppm) — exhaust gas dilution prevents complete combustion. CO 1.8%: elevated — partial burn products. CO2 10.5%: severely depressed — inert exhaust gas displaces intake charge, reducing peak combustion pressure. O2 3.5%: significant lean (>2%) — EGR gas is oxygen-depleted but dilutes charge so combustion is incomplete leaving residual O2. NOx 45 ppm: low — EGR cools combustion, suppressing NOx formation. Lambda 0.95: slightly rich — ECU adds fuel to compensate for roughness. RPM 680: rough idle below target. P0401: EGR flow insufficient — ECU detects EGR position error. Pattern: EGR valve mechanically stuck open at idle → exhaust gas dilutes intake charge → incomplete combustion → high HC + low CO2 + moderately high O2. Source: master_egr_guide.md §3.1 (stuck open at idle). Dual-speed: check EGR-011 for recovery at 2500 RPM.",
))

# --- EGR-002: EGR stuck open — severe dilution ---
add(make_row(
    "EGR-002", "EGR stuck open idle — severe dilution, near stall",
    "650", "2.5", "8.5", "4.5", "30", "0.90",
    "+12", "+9", "0.91", "28", "580", "87",
    "P0401",
    "single", "2006-2015",
    "EGR_Stuck_Open_Idle_Rough", "egr_fault",
    "named_fault", "0.85", "0.99",
    "false",
    "HC 650 ppm: very severe misfire — extreme exhaust gas dilution. CO 2.5%: elevated. CO2 8.5%: critically low (<10%) — massive inert gas displacement. O2 4.5%: severe lean/air (>4%) — extreme dilution leaves oxygen unburned. NOx 30 ppm: very low — combustion too cool from extreme EGR dilution. Lambda 0.90: rich — ECU adding fuel desperately. RPM 580: near stall. Pattern: EGR valve fully seized open at idle → extreme exhaust gas recirculation → near-complete combustion failure. CO2 collapse is the diagnostic signature differentiating EGR dilution from vacuum leak (which also has high O2 but typically lower HC). Source: master_egr_guide.md §3.2 (severe stuck-open).",
))

# --- EGR-003: EGR stuck closed → high NOx ---
add(make_row(
    "EGR-003", "EGR stuck closed — high NOx, normal idle quality",
    "30", "0.2", "15.0", "0.2", "280", "1.00",
    "0", "0", "1.00", "32", "750", "90",
    "P0400",
    "single", "2006-2015",
    "egr_fault", "egr_fault",
    "named_fault", "0.75", "0.95",
    "false",
    "HC 30 ppm: clean. CO 0.2%: clean. CO2 15.0%: efficient. O2 0.2%: low. NOx 280 ppm: very elevated (>150 ppm) — peak combustion temperature too high without EGR cooling. Lambda 1.00: perfect stoich. STFT 0%/LTFT 0%: neutral. P0400: EGR flow malfunction. Pattern: EGR valve stuck closed → no exhaust gas recirculation → peak combustion temperature rises → thermal NOx formation increases dramatically. All other gas values normal — isolated NOx elevation with P0400 is the EGR-stuck-closed signature. Source: master_egr_guide.md §4.1 (stuck closed — high NOx).",
))

# --- EGR-004: EGR stuck open, clears at 2500 RPM (dual-speed confirmation) ---
add(make_row(
    "EGR-004", "EGR stuck open — rough idle, clears at 2500 RPM",
    "380", "1.6", "11.0", "3.2", "50", "0.96",
    "+10", "+7", "0.97", "30", "700", "89",
    "P0401",
    "single", "1996-2005",
    "EGR_Stuck_Open_HC_Clears_2500RPM", "egr_fault",
    "named_fault", "0.85", "0.99",
    "false",
    "HC 380 ppm: severe misfire at idle. CO 1.6%: elevated. CO2 11.0%: depressed. O2 3.2%: significant lean. NOx 50 ppm: low. Lambda 0.96: slightly rich. STFT +10%/LTFT +7%: ECU adding fuel. P0401: EGR insufficient flow (valve position error). High-idle (2500 RPM): HC drops to 45 ppm, CO 0.3%, CO2 recovers to 15.2%, O2 0.3%. Pattern: EGR stuck open → at idle large fraction of intake is inert exhaust gas → incomplete combustion. At 2500 RPM, throttle opens, fresh air dominates, EGR fraction becomes proportionally small → combustion recovers. Dual-speed recovery is the definitive EGR-stuck-open confirmation. Source: master_egr_guide.md §3.3 (dual-speed recovery).",
    hc_2500="45", co_2500="0.3", co2_2500="15.2", o2_2500="0.3", nox_2500="120", lambda_2500="1.01",
))

# --- EGR-005: EGR valve seized open, cold start stall ---
add(make_row(
    "EGR-005", "EGR seized open — cold start stall, ECT 10C",
    "750", "3.5", "7.0", "5.0", "20", "0.85",
    "+15", "+10", "0.86", "26", "500", "10",
    "P0401",
    "single", "1996-2005",
    "EGR_Valve_Seized_Open_Cold_Start_Stall", "egr_fault",
    "named_fault", "0.85", "0.99",
    "false",
    "HC 750 ppm: extreme misfire — cold engine + exhaust gas dilution = near-complete combustion failure. CO 3.5%: very rich — cold enrichment + poor combustion. CO2 7.0%: critical collapse — inert gas + cold engine. O2 5.0%: severe excess — combustion barely occurring. NOx 20 ppm: negligible — combustion too cold. Lambda 0.85: rich — cold enrichment + poor burn. ECT 10C: cold start. RPM 500: below target, near stall. Pattern: EGR valve seized fully open → on cold start, engine already struggling with cold enrichment and poor vaporization → exhaust gas dilution makes combustion non-viable → stall. Source: master_egr_guide.md §3.4 (cold start with stuck-open EGR).",
))

# --- EGR-006: EGR intermittent — sticking open after decel ---
add(make_row(
    "EGR-006", "EGR intermittent — sticking open after decel, rough return to idle",
    "280", "1.2", "12.0", "2.8", "65", "0.97",
    "+7", "+5", "0.98", "30", "720", "90",
    "P0401",
    "single", "2006-2015",
    "EGR_Stuck_Open_Idle", "egr_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 280 ppm: at misfire boundary. CO 1.2%: moderately elevated. CO2 12.0%: depressed. O2 2.8%: lean. NOx 65 ppm: moderate. Lambda 0.97: slightly rich. STFT +7%/LTFT +5%: ECU adding fuel. Pattern: EGR valve intermittently sticks open after deceleration event (high vacuum pulls pintle open, carbon deposits hold it). Idle quality degrades for 10-30 seconds until pintle vibrates closed. Snapshot captured during the sticking episode. Intermittent P0401 sets only when ECU detects position error during the stick. Source: master_egr_guide.md §3.5 (intermittent sticking).",
))

# --- EGR-007: EGR stuck open idle — OBD-II era, moderate severity ---
add(make_row(
    "EGR-007", "EGR stuck open idle — moderate, OBD-II era, carbon deposits",
    "320", "1.4", "11.5", "3.0", "55", "0.97",
    "+9", "+7", "0.98", "31", "700", "91",
    "P0401",
    "single", "1996-2005",
    "EGR_Stuck_Open_Idle", "egr_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 320 ppm: significant misfire (>250 ppm). CO 1.4%: elevated — partial burn. CO2 11.5%: depressed — EGR dilution. O2 3.0%: lean — residual oxygen from incomplete burn. NOx 55 ppm: low — EGR cooling effective. Lambda 0.97: near stoich — ECU compensation partially working. P0401: EGR flow insufficient. Pattern: classic EGR stuck-open at idle from carbon deposits on pintle seat. Moderate severity — ECU fuel compensation keeping lambda near target but cannot fix combustion quality. Source: master_egr_guide.md §3.1. Carbon buildup from extended oil-change intervals per master_egr_guide.md §5.2.",
))

# --- EGR-008: EGR stuck closed — elevated NOx with normal idle ---
add(make_row(
    "EGR-008", "EGR stuck closed — elevated NOx, normal idle, no other symptoms",
    "20", "0.15", "15.2", "0.1", "320", "1.00",
    "-1", "0", "1.00", "32", "760", "92",
    "P0400",
    "single", "2016-2020",
    "egr_fault", "egr_fault",
    "named_fault", "0.75", "0.95",
    "false",
    "HC 20 ppm: clean. CO 0.15%: clean. CO2 15.2%: efficient. O2 0.1%: very low. NOx 320 ppm: very elevated (>150 ppm) — isolated NOx spike. Lambda 1.00: perfect stoich. STFT -1%/LTFT 0%: neutral. P0400: EGR flow malfunction. Pattern: EGR valve stuck closed in modern GDI turbo engine. All gas values normal except NOx — the isolated NOx elevation with P0400 is pathognomonic for EGR-stuck-closed. At idle, EGR is the primary NOx control mechanism. Source: master_egr_guide.md §4.1. master_nox_guide.md §3.1 (EGR-NOx relationship).",
))

# --- EGR-009: EGR stuck open — V-engine, bank 1 only ---
add(make_row(
    "EGR-009", "EGR stuck open idle — V-engine, EGR feeds B1 only, bank asymmetry",
    "300", "1.5", "11.8", "3.0", "50", "0.96",
    "+10", "+8", "0.97", "30", "690", "89",
    "P0401",
    "V-engine", "2006-2015",
    "EGR_Stuck_Open_Idle", "egr_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 300 ppm: significant misfire. CO 1.5%: elevated. CO2 11.8%: depressed. O2 3.0%: lean. NOx 50 ppm: low. Lambda 0.96: slightly rich — averaged across banks. STFT +10%/LTFT +8%: B1 trim adding fuel. Pattern: V-engine with single EGR feed to bank 1 only. EGR valve stuck open → B1 gets exhaust gas dilution, B2 runs normally. Gas collected post-catalyst averages both banks — B1 dilution signature (high HC, low CO2, high O2) mixed with B2 normal exhaust. Bank-asymmetric trims are the diagnostic clue. Source: master_egr_guide.md §3.6 (V-engine EGR distribution).",
))

# --- EGR-010: EGR stuck open idle — rough idle, pre-OBD-II era ---
add(make_row(
    "EGR-010", "EGR stuck open idle — rough idle, pre-OBD-II, no DTC support",
    "500", "2.2", "9.5", "4.0", "35", "0.92",
    "+11", "+8", "0.93", "28", "620", "85",
    "",
    "single", "1990-1995",
    "EGR_Stuck_Open_Idle_Rough", "egr_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 500 ppm: severe misfire. CO 2.2%: elevated. CO2 9.5%: very depressed (<10%). O2 4.0%: severe lean/air. NOx 35 ppm: low. Lambda 0.92: rich — ECU adding fuel. No DTCs: pre-OBD-II — no EGR position monitoring. Pattern: pre-OBD-II distributor-cap engine with vacuum-operated EGR. EGR valve stuck open at idle from carbon. No DTC available — diagnosis is purely by gas chemistry pattern and visual inspection. Source: master_egr_guide.md §2.1 (pre-OBD-II EGR systems). §3.1.",
))

# --- EGR-011: EGR stuck open — confirms EGR-004 dual-speed pattern with different severity ---
add(make_row(
    "EGR-011", "EGR stuck open — dual-speed confirmation, clears at 2500 RPM",
    "350", "1.5", "11.2", "3.0", "48", "0.97",
    "+9", "+7", "0.98", "31", "710", "89",
    "P0401",
    "single", "2006-2015",
    "EGR_Stuck_Open_HC_Clears_2500RPM", "egr_fault",
    "named_fault", "0.85", "0.98",
    "false",
    "HC 350 ppm: significant misfire at idle. CO 1.5%: elevated. CO2 11.2%: depressed. O2 3.0%: lean. NOx 48 ppm: low. Lambda 0.97: slightly rich. P0401: EGR position error. High-idle (2500 RPM): HC drops to 35 ppm, CO 0.2%, CO2 recovers to 15.5%, O2 0.3%, NOx rises to 140. Pattern: definitive EGR-stuck-open confirmed by dual-speed recovery. Idle EGR dilution signature resolves at 2500 RPM where EGR flow is proportionally negligible. This dual-speed pattern is the gold-standard diagnostic for EGR-stuck-open vs. other causes of rough idle with high HC. Source: master_egr_guide.md §3.3.",
    hc_2500="35", co_2500="0.2", co2_2500="15.5", o2_2500="0.3", nox_2500="140", lambda_2500="1.01",
))

# --- EGR-012: EGR stuck closed — borderline NOx, P0400 ---
add(make_row(
    "EGR-012", "EGR stuck closed — borderline NOx elevation, P0400 pending",
    "25", "0.2", "14.8", "0.3", "180", "1.01",
    "-2", "0", "1.01", "33", "755", "91",
    "P0400",
    "single", "1996-2005",
    "egr_fault", "egr_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 25 ppm: clean. CO 0.2%: clean. CO2 14.8%: efficient. O2 0.3%: low. NOx 180 ppm: elevated (>150 ppm). Lambda 1.01: near stoich. STFT -2%/LTFT 0%: near neutral. P0400: EGR flow malfunction. Pattern: EGR valve stuck mostly closed — some partial flow but insufficient. NOx elevated above the 150 ppm threshold but not extreme. P0400 sets from insufficient EGR flow detected by MAP change during EGR commanded-open test. Source: master_egr_guide.md §4.1 (partial stuck-closed). master_nox_guide.md §3.1.",
))

# --- EGR-013: EGR stuck open — 2016-2020 GDI turbo era ---
add(make_row(
    "EGR-013", "EGR stuck open idle — GDI turbo engine, Euro 6 era",
    "280", "1.3", "12.0", "2.8", "42", "0.98",
    "+7", "+6", "0.99", "32", "720", "91",
    "P0401",
    "single", "2016-2020",
    "EGR_Stuck_Open_Idle", "egr_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 280 ppm: at misfire boundary (>250 ppm). CO 1.3%: moderately elevated. CO2 12.0%: depressed. O2 2.8%: lean. NOx 42 ppm: low — EGR cooling. Lambda 0.98: near stoich. STFT +7%/LTFT +6%: ECU compensating. P0401: EGR insufficient flow. Pattern: modern GDI turbo engine with electric EGR valve stuck open at idle. GDI engines run higher compression and are more sensitive to EGR dilution at idle than port-injected engines. HC elevation is proportionally less severe than pre-OBD-II engines due to better idle control authority. Source: master_egr_guide.md §2.3 (modern EGR systems). §3.1.",
))

# --- EGR-014: EGR intermittent — cold start only sticking ---
add(make_row(
    "EGR-014", "EGR intermittent — cold start EGR sticking, clears when warm",
    "450", "2.0", "9.8", "4.2", "30", "0.91",
    "+12", "+9", "0.92", "27", "600", "15",
    "P0401",
    "single", "2006-2015",
    "EGR_Valve_Seized_Open_Cold_Start_Stall", "egr_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 450 ppm: severe misfire. CO 2.0%: elevated. CO2 9.8%: very depressed. O2 4.2%: severe lean/air. NOx 30 ppm: low. Lambda 0.91: rich — cold enrichment + EGR dilution. ECT 15C: cold. RPM 600: rough, near stall. Pattern: EGR valve sticks open only when cold — carbon deposits contract when cool, allowing pintle to stick. Once engine warms to operating temp, thermal expansion frees the pintle and idle normalizes. Intermittent P0401 only on cold starts. Source: master_egr_guide.md §3.5 (cold-stick pattern). §5.2 (carbon deposit behavior).",
))

# --- EGR-015: EGR stuck closed — high NOx, GDI turbo, Euro 6 ---
add(make_row(
    "EGR-015", "EGR stuck closed — GDI turbo, high NOx, Euro 6 fail",
    "15", "0.1", "15.5", "0.1", "450", "1.00",
    "0", "0", "1.00", "34", "770", "93",
    "P0400",
    "single", "2016-2020",
    "egr_fault", "egr_fault",
    "named_fault", "0.80", "0.98",
    "false",
    "HC 15 ppm: very clean. CO 0.1%: clean. CO2 15.5%: very efficient. O2 0.1%: very low. NOx 450 ppm: critically elevated — Euro 6 fail. Lambda 1.00: perfect stoich. STFT 0%/LTFT 0%: neutral. P0400: EGR flow malfunction. Pattern: EGR valve stuck closed on GDI turbo engine with Euro 6 calibration. Engine runs perfectly except NOx is 3x the typical limit. Modern engines rely heavily on EGR for NOx control; without it, lean-stratified GDI combustion produces extreme thermal NOx. All other gas parameters pristine — this is a pure NOx failure. Source: master_egr_guide.md §4.1. master_nox_guide.md §3.2 (GDI NOx formation).",
))

# --- EGR-016: EGR stuck open — dual-speed with partial recovery ---
add(make_row(
    "EGR-016", "EGR stuck partially open — incomplete recovery at 2500 RPM",
    "300", "1.3", "12.0", "2.5", "60", "0.99",
    "+7", "+5", "1.00", "32", "730", "90",
    "P0401",
    "single", "1996-2005",
    "EGR_Stuck_Open_Idle", "egr_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 300 ppm: significant misfire at idle. CO 1.3%: elevated. CO2 12.0%: depressed. O2 2.5%: lean. NOx 60 ppm: moderate. Lambda 0.99: near stoich. P0401: EGR position error. High-idle (2500 RPM): HC drops to 120 ppm — partial improvement but not full recovery (CO2 13.5%, O2 1.5%). Pattern: EGR valve stuck partially open — not fully seized. At idle, significant dilution. At 2500 RPM, some recovery but still elevated HC and depressed CO2 compared to full-recovery pattern. Indicates EGR pintle is partially obstructing the passage even at high RPM. Source: master_egr_guide.md §3.3 (partial vs full stuck-open).",
    hc_2500="120", co_2500="0.6", co2_2500="13.5", o2_2500="1.5", nox_2500="100", lambda_2500="1.02",
))

# --- EGR-017: EGR stuck open — rough idle, V-engine, bank symmetric EGR ---
add(make_row(
    "EGR-017", "EGR stuck open idle — V-engine with symmetric EGR, both banks diluted",
    "360", "1.6", "11.0", "3.2", "45", "0.95",
    "+9", "+7", "0.96", "29", "680", "90",
    "P0401",
    "V-engine", "2006-2015",
    "EGR_Stuck_Open_Idle_Rough", "egr_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 360 ppm: significant misfire. CO 1.6%: elevated. CO2 11.0%: depressed. O2 3.2%: lean. NOx 45 ppm: low. Lambda 0.95: slightly rich. P0401: EGR insufficient flow. Pattern: V-engine with symmetric EGR distribution (both banks fed equally). EGR stuck open dilutes both banks identically → both banks show similar fuel trim response. Unlike EGR-009 where only B1 was affected, both STFTs are elevated similarly. Source: master_egr_guide.md §3.6 (symmetric V-engine EGR).",
    stft_b2="+8", ltft_b2="+6",
))

# --- EGR-018: EGR stuck open — post-decel surge then rough idle ---
add(make_row(
    "EGR-018", "EGR intermittent — post-decel EGR hang, rough idle for 15s",
    "260", "1.1", "12.2", "2.6", "58", "0.98",
    "+6", "+5", "0.99", "31", "740", "91",
    "",
    "single", "2006-2015",
    "EGR_Stuck_Open_Idle", "egr_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 260 ppm: at misfire boundary. CO 1.1%: slightly elevated. CO2 12.2%: mildly depressed. O2 2.6%: lean. NOx 58 ppm: moderate. Lambda 0.98: near stoich. STFT +6%/LTFT +5%: mild correction. No DTC: intermittent — hasn't persisted long enough to set code. Pattern: EGR valve mechanically slow to close after deceleration. High manifold vacuum during decel pulls EGR pintle open; carbon on stem prevents smooth return. Rough idle persists for 10-15 seconds after returning to idle. No DTC because the condition clears before the ECU's fault confirmation cycle completes. Source: master_egr_guide.md §3.5 (post-decel hang).",
))

# --- EGR-019: EGR stuck closed — vacuum-operated EGR, no DTC available ---
add(make_row(
    "EGR-019", "EGR stuck closed — vacuum EGR, pre-OBD-II, no DTC, high NOx",
    "28", "0.2", "14.8", "0.3", "260", "1.00",
    "0", "0", "1.00", "31", "740", "88",
    "",
    "single", "1990-1995",
    "egr_fault", "egr_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 28 ppm: clean. CO 0.2%: clean. CO2 14.8%: efficient. O2 0.3%: low. NOx 260 ppm: elevated (>150 ppm). Lambda 1.00: perfect stoich. STFT 0%/LTFT 0%: neutral (or no trims on pre-OBD-II). No DTCs: pre-OBD-II — no EGR monitoring. Pattern: vacuum-operated EGR on pre-OBD-II engine. EGR diaphragm ruptured → valve permanently closed. No DTC available. Diagnosed purely by gas chemistry: clean HC/CO/CO2 with isolated NOx elevation. Vacuum test at EGR port confirms diaphragm failure. Source: master_egr_guide.md §2.1 (pre-OBD-II vacuum EGR). §4.1.",
))

# --- EGR-020: EGR stuck open — worst case, pre-OBD-II, no ECU compensation ---
add(make_row(
    "EGR-020", "EGR stuck open — worst case, pre-OBD-II, no ECU trim compensation",
    "800", "4.0", "6.5", "5.5", "18", "0.82",
    "0", "0", "0.82", "25", "480", "80",
    "",
    "single", "1990-1995",
    "EGR_Stuck_Open_Idle_Rough", "egr_fault",
    "named_fault", "0.90", "0.99",
    "false",
    "HC 800 ppm: extreme misfire — combustion barely occurring. CO 4.0%: very rich — massive partial burn. CO2 6.5%: critical collapse — inert gas dominates charge. O2 5.5%: extreme excess — most intake oxygen passes through unburned. NOx 18 ppm: negligible — combustion too cold. Lambda 0.82: very rich — carbureted or open-loop EFI with no O2 feedback. RPM 480: barely running. Pattern: worst-case EGR stuck-open scenario — pre-OBD-II engine with no ECU fuel trim compensation. Carbureted or early EFI system continues delivering fuel based on air flow, oblivious to the exhaust gas dilution. Without O2 feedback to lean out the mixture, engine runs pig-rich on top of dilution → extreme HC, CO, and CO2 collapse. This is the diagnostic limit case for EGR failure. Source: master_egr_guide.md §2.1, §3.2.",
))


# ============================================================
# 10 TURBO CASES (TURBO-001 to TURBO-010)
# ============================================================

# --- TURBO-001: Boost leak post-turbo — rich at idle ---
add(make_row(
    "TURBO-001", "Turbo boost leak post-turbo — rich idle, lean under boost",
    "60", "1.2", "14.2", "0.5", "70", "0.97",
    "-8", "-6", "0.98", "35", "760", "90",
    "P0299",
    "single", "2016-2020",
    "Turbo_Boost_Leak_Post_Turbo_Rich_Idle", "turbo_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 60 ppm: borderline. CO 1.2%: slightly elevated. CO2 14.2%: near efficient. O2 0.5%: normal. NOx 70 ppm: moderate. Lambda 0.97: slightly rich at idle. STFT -8%/LTFT -6%: ECU pulling fuel — MAF measured air that leaked post-turbo, so actual air entering engine is less than measured. P0299: turbo underboost. Pattern: boost leak post-turbo (charge pipe crack, intercooler coupler loose). At idle, MAF measures air that partially escapes post-turbo → ECU fuels for more air than enters cylinders → rich at idle. Under boost, leak flows in reverse — metered air escapes → lean under load. The rich-idle + lean-boost combination is the classic boost-leak signature. Source: master_turbo_guide.md §3.1 (boost leak).",
))

# --- TURBO-002: Wastegate stuck open — low boost ---
add(make_row(
    "TURBO-002", "Turbo wastegate stuck open — low boost, lean under load",
    "25", "0.2", "14.8", "0.3", "80", "1.01",
    "+2", "+1", "1.01", "36", "780", "91",
    "P0299",
    "single", "2016-2020",
    "Turbo_Wastegate_Stuck_Open_Low_Boost", "turbo_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 25 ppm: clean. CO 0.2%: clean. CO2 14.8%: efficient. O2 0.3%: low. NOx 80 ppm: moderate. Lambda 1.01: near stoich at idle. STFT +2%/LTFT +1%: near neutral at idle. MAP 36 kPa: normal idle. P0299: turbo underboost. Pattern: wastegate actuator rod rusted/stuck, holding wastegate permanently open. At idle, engine runs normally — wastegate position is irrelevant without exhaust energy to spin turbine. Under load, turbo fails to build boost → MAF reads air that the turbo can't compress → ECU fuels for expected boost that never arrives → lean under load with P0299. Idle gas values are normal — the fault only manifests under load. Source: master_turbo_guide.md §3.2 (wastegate failure).",
))

# --- TURBO-003: BOV tear — rich spike on gear change ---
add(make_row(
    "TURBO-003", "Turbo BOV diaphragm tear — rich spike on gear change",
    "80", "2.5", "13.5", "0.8", "50", "0.93",
    "-12", "-4", "0.94", "34", "770", "90",
    "",
    "single", "2016-2020",
    "Turbo_BOV_Tear_Rich_Spike_Gear_Change_Only", "turbo_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 80 ppm: marginal. CO 2.5%: moderately rich. CO2 13.5%: mildly depressed. O2 0.8%: normal. NOx 50 ppm: low. Lambda 0.93: rich. STFT -12% (momentary): ECU pulling fuel after BOV leak enriched mixture. Pattern: blow-off valve diaphragm torn → during gear change (throttle close), BOV should vent charge air to atmosphere or recirc. Instead, torn diaphragm leaks metered air → ECU already fueled for that air → momentary rich spike. Between gear changes, engine runs normally. Catching the rich spike requires logging during a drive cycle; this snapshot captures the post-spike fuel trim correction. Source: master_turbo_guide.md §3.3 (BOV failure).",
))

# --- TURBO-004: Intercooler oil soak — HC under boost ---
add(make_row(
    "TURBO-004", "Turbo intercooler oil soak — HC rises under boost, clean idle",
    "35", "0.3", "14.8", "0.3", "45", "1.01",
    "+1", "0", "1.01", "33", "760", "92",
    "",
    "single", "2006-2015",
    "Turbo_Intercooler_Oil_Soak_HC_Under_Boost", "turbo_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 35 ppm: clean at idle. CO 0.3%: clean. CO2 14.8%: efficient. O2 0.3%: low. NOx 45 ppm: low. Lambda 1.01: near stoich. STFT +1%/LTFT 0%: neutral. Pattern: turbocharger oil seal leaking into compressor housing → oil accumulates in intercooler → at idle, no boost → oil stays in intercooler → gas values normal. Under boost, oil is picked up and burned → HC spikes to 200+ ppm. Idle snapshot appears clean — the fault is load-dependent. Diagnose by running at 2500 RPM under load and observing HC rise. Source: master_turbo_guide.md §3.4 (intercooler oil soak). §4.2 (turbo oil seal failure).",
))

# --- TURBO-005: Bypass valve leak — metered air lost ---
add(make_row(
    "TURBO-005", "Turbo bypass valve leak — metered air lost, rich idle",
    "50", "1.5", "14.0", "0.6", "60", "0.96",
    "-9", "-7", "0.97", "36", "750", "89",
    "",
    "single", "2016-2020",
    "Turbo_Bypass_Valve_Leak", "turbo_fault",
    "named_fault", "0.75", "0.95",
    "false",
    "HC 50 ppm: borderline. CO 1.5%: moderately rich. CO2 14.0%: near efficient. O2 0.6%: normal. NOx 60 ppm: moderate. Lambda 0.96: slightly rich. STFT -9%/LTFT -7%: ECU pulling fuel — MAF measured more air than entered cylinders. Pattern: compressor bypass valve (recirculation valve) leaking internally. MAF measures all intake air; bypass valve should recirculate post-compressor air back to intake. Leaking valve allows metered air to escape the closed system → ECU fuels for air that doesn't reach cylinders → rich mixture. Similar to boost leak but internal to the turbo plumbing. Source: master_turbo_guide.md §3.5 (bypass valve failure).",
))

# --- TURBO-006: Boost leak post-turbo — large leak, very rich idle ---
add(make_row(
    "TURBO-006", "Turbo boost leak — large split in charge pipe, very rich idle",
    "90", "3.2", "13.0", "0.4", "35", "0.90",
    "-18", "-14", "0.91", "38", "740", "90",
    "P0299|P0172",
    "single", "2016-2020",
    "Turbo_Boost_Leak_Post_Turbo_Rich_Idle", "turbo_fault",
    "named_fault", "0.85", "0.98",
    "false",
    "HC 90 ppm: marginal. CO 3.2%: very rich (>3%). CO2 13.0%: depressed. O2 0.4%: low — rich consumed oxygen. NOx 35 ppm: low — rich quench. Lambda 0.90: rich. STFT -18%/LTFT -14%: ECU pulling fuel aggressively. P0299/P0172: underboost + rich DTC. MAP 38 kPa: slightly elevated for idle. Pattern: large split in charge pipe post-turbo. At idle, significant fraction of MAF-measured air escapes through split → ECU fuels for air that never reaches cylinders → very rich. Under boost, even more air escapes → severe underboost (P0299) + continued rich (P0172). Source: master_turbo_guide.md §3.1 (boost leak diagnosis).",
))

# --- TURBO-007: Wastegate stuck open — intermittent, vacuum actuator fault ---
add(make_row(
    "TURBO-007", "Turbo wastegate intermittent — vacuum actuator leak, variable boost",
    "30", "0.2", "14.5", "0.4", "75", "1.01",
    "+1", "0", "1.01", "35", "770", "90",
    "P0299",
    "single", "2006-2015",
    "Turbo_Wastegate_Stuck_Open_Low_Boost", "turbo_fault",
    "named_fault", "0.75", "0.92",
    "false",
    "HC 30 ppm: clean at idle. CO 0.2%: clean. CO2 14.5%: efficient. O2 0.4%: low. NOx 75 ppm: moderate. Lambda 1.01: near stoich. STFT +1%/LTFT 0%: neutral. P0299: underboost (intermittent — pending). Pattern: vacuum-operated wastegate actuator diaphragm has pinhole leak. At idle, vacuum is highest and wastegate may hold closed. Under load, vacuum drops → wastegate drifts open → boost pressure bleeds off → P0299 sets intermittently. Idle gas values normal — fault is load-dependent. Source: master_turbo_guide.md §3.2 (wastegate actuator failure). §2.2 (vacuum vs electronic wastegate).",
))

# --- TURBO-008: Turbo intercooler oil soak — severe, smokes under boost ---
add(make_row(
    "TURBO-008", "Turbo intercooler oil soak severe — visible smoke under boost",
    "50", "0.4", "14.2", "0.5", "55", "1.00",
    "+2", "0", "1.00", "33", "755", "93",
    "",
    "single", "2006-2015",
    "Turbo_Intercooler_Oil_Soak_HC_Under_Boost", "turbo_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 50 ppm: borderline at idle — residual oil vapor. CO 0.4%: normal. CO2 14.2%: near efficient. O2 0.5%: normal. NOx 55 ppm: moderate. Lambda 1.00: perfect stoich at idle. Pattern: turbocharger oil seal failed; intercooler saturated with engine oil. At idle, oil pools in intercooler with minimal carryover — slight HC elevation. Under boost (2500+ RPM), oil aerosolizes and burns → HC spikes to 300+ ppm, visible blue-white smoke from exhaust. Idle snapshot understates severity. The key diagnostic: HC clean or borderline at idle, dramatic HC rise under sustained boost. Source: master_turbo_guide.md §3.4. §4.2 (oil seal failure progression).",
))

# --- TURBO-009: Bypass valve leak + boost leak — combined failure ---
add(make_row(
    "TURBO-009", "Turbo combined: bypass valve leak + small boost leak, rich at all speeds",
    "70", "2.0", "13.8", "0.5", "45", "0.94",
    "-14", "-10", "0.95", "37", "750", "90",
    "P0299",
    "single", "2016-2020",
    "Turbo_Bypass_Valve_Leak", "turbo_fault",
    "named_fault", "0.80", "0.95",
    "false",
    "HC 70 ppm: marginal. CO 2.0%: moderately rich. CO2 13.8%: mildly depressed. O2 0.5%: normal. NOx 45 ppm: low — rich. Lambda 0.94: rich. STFT -14%/LTFT -10%: ECU pulling fuel significantly. P0299: underboost. Pattern: combined bypass valve leak + small charge pipe crack. Both leak paths allow metered air to escape between MAF and cylinders. At idle, combined leak is significant → rich. Under boost, even more air escapes → underboost + continued rich. Fuel trims are persistently negative across all operating conditions. Source: master_turbo_guide.md §3.1, §3.5.",
))

# --- TURBO-010: BOV tear — pre-OBD-II turbo, no DTC, rich spike on lift ---
add(make_row(
    "TURBO-010", "Turbo BOV tear — pre-OBD-II, rich stumble on throttle lift",
    "45", "1.8", "14.0", "0.6", "65", "0.96",
    "0", "0", "0.96", "34", "760", "88",
    "",
    "single", "1990-1995",
    "Turbo_BOV_Tear_Rich_Spike_Gear_Change_Only", "turbo_fault",
    "named_fault", "0.70", "0.88",
    "false",
    "HC 45 ppm: clean. CO 1.8%: moderately elevated — residual from post-lift rich spike. CO2 14.0%: near efficient. O2 0.6%: normal. NOx 65 ppm: moderate. Lambda 0.96: slightly rich. No DTCs: pre-OBD-II, no boost monitoring. Pattern: pre-OBD-II turbo engine (early 1990s) with BOV diaphragm tear. On throttle lift during gear change, BOV should vent charge pressure; torn diaphragm leaks metered air → rich stumble. No ECU to set codes or adapt. Diagnosed by: momentary rich spike on lift-throttle, otherwise normal gas values. Source: master_turbo_guide.md §2.1 (pre-OBD-II turbo systems). §3.3 (BOV failure).",
))


# ============================================================
# Write to CSV
# ============================================================

def main() -> None:
    # Read existing CSV to verify
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing = list(reader)

    print(f"Existing rows: {len(existing)}")

    # Verify all new cases have required fields
    for case in CASES:
        assert case["case_id"], f"Missing case_id"
        assert case["expected_top_fault"], f"Missing expected_top_fault for {case['case_id']}"
        assert case["expected_state"] in ("named_fault", "insufficient_evidence"), \
            f"Invalid expected_state for {case['case_id']}: {case['expected_state']}"
        assert case["reasoning"], f"Missing reasoning for {case['case_id']}"

    print(f"New cases: {len(CASES)}")
    print(f"Total after append: {len(existing) + len(CASES)}")

    # Extract unique fault IDs
    all_fault_ids = sorted(set(
        r["expected_top_fault"] for r in existing + CASES if r["expected_top_fault"]
    ))
    print(f"\nUnique expected_top_fault values ({len(all_fault_ids)}):")
    for fid in all_fault_ids:
        print(f"  {fid}")

    # Append
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLS)
        writer.writerows(CASES)

    print(f"\nAppended {len(CASES)} rows to {CSV_PATH}")
    print(f"New total should be: {len(existing) + len(CASES)} rows")

if __name__ == "__main__":
    main()
