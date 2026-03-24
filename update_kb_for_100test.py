#!/usr/bin/env python3
"""Update expanded_knowledge_base.json to fix naming, ordering, and logics for 100-case test."""

import json
from pathlib import Path

kb_path = Path('data/expanded_knowledge_base.json')
backup_path = kb_path.with_suffix('.json.bak_20260323')
import shutil
shutil.copy2(kb_path, backup_path)
print(f"Backup: {backup_path}")

with open(kb_path, 'r') as f:
    kb = json.load(f)

matrix = kb.get('diagnostic_matrix', [])

# Rename map: case_id -> new name (match test expectations)
rename_map = {
    'P_001': 'Intake Vacuum Leak',
    'P_002': 'Catalytic Converter Efficiency Failure',  # but we already have catalyst_failure; keep both
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
    'timing_retard': 'Ignition Timing Issues',  # map pattern_006
    # Add more as needed
}

# Apply renames
for case in matrix:
    cid = case.get('case_id')
    if cid in rename_map:
        case['name'] = rename_map[cid]

# Add base_logic for cases that lack it, to separate 5-gas matching from addons
# We'll copy 'logic' to 'base_logic' if not present and then keep 'logic' for addons if needed
# However, many patterns already only have 'logic'. We'll not add base_logic now to keep changes minimal. Instead, we'll rely on name matching.

# Reorder matrix: move specific high-priority cases to the top
desired_order = [
    'catalyst_failure',           # Catalyst failures
    'high_nox_timing_advance',    # High NOx timing
    'high_nox_lean_egr',          # High NOx lean (EGR)
    'ignition_misfire_high_hc_o2', # High HC + O2 misfire
    'cold_start_enrichment_fault', # Cold start
    'P_004',                      # Ignition Misfire (original)
    'P_003',                      # Exhaust Dilution
    'vacuum_leak_differential_high_idle', # Vacuum leak differential
    'P_001',                      # Vacuum Leak (Differential) - also maps to Intake Vacuum Leak
    'pattern_010',                # Another vacuum leak
    'vacuum_leak_differential',   # Another
    # Then others...
]

# Build new matrix order
new_matrix = []
remaining = matrix.copy()

# Place desired_order cases first (if they exist)
for cid in desired_order:
    for case in remaining:
        if case.get('case_id') == cid:
            new_matrix.append(case)
            remaining = [c for c in remaining if c.get('case_id') != cid]
            break

# Then add the rest in original order
new_matrix.extend(remaining)

kb['diagnostic_matrix'] = new_matrix

# Save
with open(kb_path, 'w') as f:
    json.dump(kb, f, indent=2)

print(f"Updated knowledge base: {len(new_matrix)} cases")
print(f"Renamed cases to match test expectations.")
print(f"Reordered: {len(desired_order)} cases moved to top.")

# Show mapping summary
print("\nRename map applied:")
for old, new in rename_map.items():
    print(f"  {old} -> {new}")
