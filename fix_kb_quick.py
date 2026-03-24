#!/usr/bin/env python3
import json
from pathlib import Path
import shutil

kb_path = Path('data/expanded_knowledge_base.json')
backup_path = kb_path.with_suffix('.json.bak_20260323_2')
if not backup_path.exists():
    shutil.copy2(kb_path, backup_path)
    print(f"Backup: {backup_path}")

with open(kb_path, 'r') as f:
    kb = json.load(f)

matrix = kb.get('diagnostic_matrix', [])

rename_map = {
    'P_001': 'Intake Vacuum Leak',
    'P_002': 'Catalytic Converter Efficiency Failure',
    'P_003': 'Exhaust Dilution (False Lean)',
    'P_004': 'Ignition Misfire',
    'P_005': 'System Running Rich',
    'high_nox_lean_egr': 'High NOx + Lean Idle (EGR/Cooling Failure)',
    'high_nox_timing_advance': 'Excessively Advanced Timing',
    'vacuum_leak_differential_high_idle': 'Intake Vacuum Leak',
    'P_100': 'Healthy Engine',
    'catalyst_failure': 'Catalytic Converter Efficiency Failure',
    'cold_start_enrichment_fault': 'Cold Start Enrichment',
    'pattern_001': 'System Running Rich',
    'pattern_002': 'lean_exhaust',
    'pattern_003': 'Ignition Misfire',
    'pattern_007': 'Excessively Advanced Timing',
    'pattern_010': 'Intake Vacuum Leak',
    'pattern_012': 'Fuel Delivery Problem (Lean)',
    'pattern_029': 'MAF Sensor Under-Reading',
    'pattern_048': 'O2 Sensor Sluggish or Failed',
    'pattern_049': 'Engine Misfire',
    'pattern_050': 'Exhaust Leak',
    'pattern_042': 'Fuel Delivery Problem (Lean)',
    'fuel_delivery_lean': 'Fuel Delivery Problem (Lean)',
    'mass_airflow_underreport': 'MAF Sensor Under-Reading',
    'o2_sensor_lazy': 'O2 Sensor Sluggish or Failed',
    'ignition_misfire_high_hc_o2': 'Engine Misfire',
    'exhaust_leak_false_lean': 'Exhaust Leak',
    'vacuum_leak_differential': 'Intake Vacuum Leak',
    'cold_start_over_enrichment': 'Cold Start Enrichment',
    'timing_retard': 'Ignition Timing Issues',
}

# Apply renames
for case in matrix:
    cid = case.get('case_id')
    if cid in rename_map:
        case['name'] = rename_map[cid]

desired_order_prefixes = [
    'catalyst_failure',
    'high_nox_timing_advance',
    'high_nox_lean_egr',
    'ignition_misfire_high_hc_o2',
    'cold_start_enrichment_fault',
    'P_004',
    'P_003',
    'vacuum_leak_differential_high_idle',
    'P_001',
    'pattern_010',
    'vacuum_leak_differential',
    'fuel_delivery_lean',
    'pattern_012',
    'timing_retard',
    'pattern_006',
    'pattern_002',
    'pattern_001',
    'mass_airflow_underreport',
    'o2_sensor_lazy',
    'exhaust_leak_false_lean',
    'P_005'
]

def sort_key(case):
    cid = case.get('case_id', '')
    try:
        idx = desired_order_prefixes.index(cid)
        return (0, idx)
    except ValueError:
        return (1, 0)

new_matrix = sorted(matrix, key=sort_key)
kb['diagnostic_matrix'] = new_matrix

with open(kb_path, 'w') as f:
    json.dump(kb, f, indent=2)

print(f"Updated KB: {len(new_matrix)} cases (renamed + reordered)")
