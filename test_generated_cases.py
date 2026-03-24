#!/usr/bin/env python3
import csv, random
from core.matrix import match_case
from core.bretschneider import calculate_lambda
from core.validator import validate_gas_data
import json

with open('data/expanded_knowledge_base.json') as f:
    kb = json.load(f)

# load a few cases from generator (we'll use generator functions directly)
from generate_aligned_100 import gen_catalyst, gen_vacuum_leak, gen_exhaust_leak, gen_healthy, gen_timing_advance, gen_misfire, gen_cold_start, gen_fuel_lean, gen_rich_running, gen_o2_lazy, gen_timing_retard, gen_maf_under

gens = {
    'Catalytic Converter Efficiency Failure': gen_catalyst,
    'Exhaust Leak (False Lean)': gen_exhaust_leak,
    'Intake Vacuum Leak': gen_vacuum_leak,
    'Healthy Engine': gen_healthy,
    'Excessively Advanced Timing': gen_timing_advance,
    'Engine Misfire': gen_misfire,
    'Cold Start Enrichment': gen_cold_start,
    'Fuel Delivery Problem (Lean)': gen_fuel_lean,
    'System Running Rich': gen_rich_running,
    'O2 Sensor Sluggish or Failed': gen_o2_lazy,
    'Ignition Timing Issues (Retard)': gen_timing_retard,
    'MAF Sensor Under-Reading': gen_maf_under
}

# Test one of each
for exp, gen in gens.items():
    case = gen()
    low_idle = {
        'lambda': float(case['OBD_Lambda']),
        'co': float(case['CO_Pct']),
        'co2': float(case['CO2_Pct']),
        'hc': int(case['HC_PPM']),
        'o2': float(case['O2_Pct']),
        'nox': int(float(case['NOx_PPM']))
    }
    valid, _ = validate_gas_data(low_idle)
    if not valid:
        print(f"{exp}: invalid")
        continue
    fuel_type = case['Fuel'].lower() if case['Fuel'].lower() in ['e0','e5','e10','e85'] else 'e10'
    calc = calculate_lambda(co=low_idle['co'], co2=low_idle['co2'], hc_ppm=low_idle['hc'], o2=low_idle['o2'], fuel_type=fuel_type)
    calc_lambda = calc['lambda']
    dtc_list = [case['OBD_DTC']] if case['OBD_DTC'] != 'None' else []
    tier4_low = {'0C':0, '06': float(case['OBD_STFT']), '07': float(case['OBD_LTFT']), '44': float(case['OBD_Lambda']), '10':0, '0B':0, '11':0}
    matched = match_case(low_idle, calc_lambda, low_idle['lambda'], kb, None, dtc_list, None, tier4_low, None)
    actual = matched.get('name','')
    match = (actual == exp)
    print(f"{exp}: got '{actual}' -> {'OK' if match else 'FAIL'}")
