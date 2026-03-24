#!/usr/bin/env python3
"""Refine diagnostic logics and ordering to fix remaining failures."""

from pathlib import Path
import json

kb_path = Path('data/expanded_knowledge_base.json')
backup_path = kb_path.with_suffix('.json.bak_20260323_3')
import shutil
if not backup_path.exists():
    shutil.copy2(kb_path, backup_path)
    print(f"Backup: {backup_path}")

with open(kb_path, 'r') as f:
    kb = json.load(f)

matrix = kb.get('diagnostic_matrix', [])

# Helper: find case by case_id
def find_case(cid):
    for c in matrix:
        if c.get('case_id') == cid:
            return c
    return None

# 1. Catalyst: Ensure it requires high NOx AND poor CO2 AND moderate HC to avoid shadowing timing_adv
cat = find_case('catalyst_failure')
if cat:
    cat['logic'] = 'low_idle.nox > 1000 && low_idle.co2 < 13.0 && low_idle.hc > 50'
    cat['confidence_boosters'] = {'base_confidence': 0.85}
    cat['modular_addons'] = {'tier2_obd_dtc': ['P0420', 'P0430']}
    print("Updated catalyst_failure logic")

# 2. High NOx timing advance: tighten to require very clean burn and NOT high HC
timing = find_case('high_nox_timing_advance')
if timing:
    timing['logic'] = 'low_idle.nox > 500 && low_idle.co < 0.25 && low_idle.hc < 50 && 0.99 <= low_idle.lambda <= 1.03'
    timing['confidence_boosters'] = {'base_confidence': 0.75}
    print("Updated high_nox_timing_advance logic")

# 3. Cold Start Enrichment: use gas values only, ignore calculated_lambda
cold = find_case('cold_start_enrichment_fault')
if cold:
    cold['logic'] = 'low_idle.co > 3.0 && low_idle.hc > 20000 && low_idle.co2 < 5.0 && low_idle.lambda < 0.75'
    cold['confidence_boosters'] = {'base_confidence': 0.8}
    print("Updated cold_start_enrichment_fault logic")

# 4. Lean exhaust (pattern_002): define clearly: high lambda, high O2, low CO, low CO2, moderate HC
lean = find_case('pattern_002')
if lean:
    lean['name'] = 'lean_exhaust'
    lean['logic'] = 'low_idle.lambda > 1.05 && low_idle.o2 > 2.0 && low_idle.co < 0.4 && low_idle.co2 < 13.0 && low_idle.hc < 500'
    lean['confidence_boosters'] = {'base_confidence': 0.65}
    print("Updated pattern_002 (lean_exhaust) logic")

# 5. Fuel Delivery Problem (Lean): use fuel_delivery_lean or pattern_012. Ensure distinct by requiring higher NOx and positive trims
fuel_lean = find_case('fuel_delivery_lean')
if not fuel_lean:
    fuel_lean = find_case('pattern_012')
if fuel_lean:
    fuel_lean['name'] = 'Fuel Delivery Problem (Lean)'
    fuel_lean['logic'] = 'low_idle.lambda > 1.07 && low_idle.stft > 10 && low_idle.ltft > 8 && low_idle.nox > 100'
    fuel_lean['confidence_boosters'] = {'base_confidence': 0.7}
    fuel_lean['modular_addons'] = {'tier2_obd_dtc': ['P0171', 'P0174']}
    print("Updated fuel_delivery_lean logic")

# 6. Ignition Timing Issues: use timing_retard with low NOx and higher CO, moderate HC
timing_ret = find_case('timing_retard')
if timing_ret:
    timing_ret['name'] = 'Ignition Timing Issues'
    timing_ret['logic'] = 'low_idle.nox < 30 && low_idle.co > 0.8 && low_idle.co2 < 13.0 && 0.98 <= low_idle.lambda <= 1.02'
    timing_ret['confidence_boosters'] = {'base_confidence': 0.65}
    timing_ret['modular_addons'] = {'tier2_obd_dtc': ['P0016', 'P0017']}
    print("Updated timing_retard logic")

# 7. O2 Sensor Sluggish: lambda near 1, O2 stuck 0.4-0.6, CO moderate, exclude high NOx
o2_lazy = find_case('o2_sensor_lazy')
if o2_lazy:
    o2_lazy['name'] = 'O2 Sensor Sluggish or Failed'
    o2_lazy['logic'] = '0.96 <= low_idle.lambda <= 1.04 && low_idle.o2 > 0.4 && low_idle.o2 < 0.7 && low_idle.co > 0.3 && low_idle.nox < 200'
    o2_lazy['confidence_boosters'] = {'base_confidence': 0.6}
    o2_lazy['modular_addons'] = {'tier2_obd_dtc': ['P0131', 'P0132', 'P0133', 'P0134']}
    print("Updated o2_sensor_lazy logic")

# 8. Exhaust Leak: high O2, false lean, but lambda > measured? Not available. Use high O2 and CO2 low
exh_leak = find_case('exhaust_leak_false_lean')
if exh_leak:
    exh_leak['name'] = 'Exhaust Leak'
    exh_leak['logic'] = 'low_idle.o2 > 3.0 && low_idle.lambda > 1.05 && low_idle.co < 0.5 && low_idle.co2 < 12.0 && low_idle.nox < 100'
    exh_leak['confidence_boosters'] = {'base_confidence': 0.6}
    print("Updated exhaust_leak_false_lean logic")

# 9. Engine Misfire: high HC and high O2, but exclude very high CO (which suggests rich) and moderate NOx
misfire = find_case('ignition_misfire_high_hc_o2')
if misfire:
    misfire['name'] = 'Engine Misfire'
    misfire['logic'] = 'low_idle.hc > 1500 && low_idle.o2 > 1.5 && low_idle.co < 1.0 && low_idle.co2 > 5.0 && low_idle.nox < 200'
    misfire['confidence_boosters'] = {'base_confidence': 0.85}
    misfire['modular_addons'] = {'tier2_obd_dtc': ['P0300', 'P0301', 'P0302', 'P0303', 'P0304', 'P0305', 'P0306']}
    print("Updated ignition_misfire_high_hc_o2 logic")

# 10. System Running Rich: lambda low, high CO, low O2, HC not extremely high (unless misfire)
rich = find_case('P_005')
if rich:
    rich['name'] = 'System Running Rich'
    rich['logic'] = 'low_idle.lambda < 0.92 && low_idle.co > 2.0 && low_idle.o2 < 0.2 && low_idle.hc < 2000 && low_idle.nox < 100'
    rich['confidence_boosters'] = {'base_confidence': 0.7}
    rich['modular_addons'] = {'tier2_obd_dtc': ['P0172']}
    print("Updated P_005 (System Running Rich) logic")

# Also rename pattern_001 to System Running Rich and keep it as backup (same logic, different priority)
p001 = find_case('pattern_001')
if p001:
    p001['name'] = 'System Running Rich'
    p001['logic'] = 'low_idle.lambda < 0.95 && low_idle.co > 1.0 && low_idle.o2 < 0.3 && low_idle.hc < 3000'
    p001['confidence_boosters'] = {'base_confidence': 0.65}
    print("Updated pattern_001 logic")

# 11. MAF Under-Reading: lambda high, positive trims, low MAF (but we don't have MAF in base context; need to rely on DTC or tier4? Since base_context doesn't include tier4, we can't use MAF in logic. Instead, rely on lambda + trims + maybe NOx)
maf = find_case('mass_airflow_underreport')
if maf:
    maf['name'] = 'MAF Sensor Under-Reading'
    maf['logic'] = 'low_idle.lambda > 1.06 && low_idle.stft > 15 && low_idle.ltft > 10 && low_idle.nox > 120'
    maf['confidence_boosters'] = {'base_confidence': 0.65}
    maf['modular_addons'] = {'tier2_obd_dtc': ['P0101', 'P0102']}
    print("Updated mass_airflow_underreport logic")

# Save
with open(kb_path, 'w') as f:
    json.dump(kb, f, indent=2)

print("Knowledge base refinement complete.")
