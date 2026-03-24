#!/usr/bin/env python3
"""Add missing rich_exhaust case and finalize ordering."""

from pathlib import Path
import json

kb_path = Path('data/expanded_knowledge_base.json')
with open(kb_path, 'r') as f:
    kb = json.load(f)

matrix = kb.get('diagnostic_matrix', [])

# Add rich_exhaust case
rich_exhaust_case = {
    "case_id": "rich_exhaust",
    "name": "rich_exhaust",
    "logic": "low_idle.lambda < 0.98 && low_idle.co > 0.8 && low_idle.o2 < 0.5 && low_idle.hc > 50 && low_idle.hc < 1000 && low_idle.nox < 200",
    "health_score": 50,
    "verdict": "Rich exhaust with moderate CO and HC. Possible incomplete combustion.",
    "action": "Check for leaky injectors, high fuel pressure, or O2 sensor fault.",
    "confidence_boosters": {
        "base_confidence": 0.65
    },
    "modular_addons": {
        "tier2_obd_dtc": ["P0172"]
    }
}

# Insert after P_005 (System Running Rich) or near beginning? We'll append then re-sort
matrix.append(rich_exhaust_case)

# Desired ordering: put high-confidence specific patterns first, then medium, then generics
top_priority = [
    'catalyst_failure',
    'high_nox_timing_advance',
    'high_nox_lean_egr',
    'ignition_misfire_high_hc_o2',
    'cold_start_enrichment_fault',
    'P_004',
    'P_003',
    'rich_exhaust',  # specific rich
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
        idx = top_priority.index(cid)
        return (0, idx)
    except ValueError:
        return (1, 0)

new_matrix = sorted(matrix, key=sort_key)
kb['diagnostic_matrix'] = new_matrix

with open(kb_path, 'w') as f:
    json.dump(kb, f, indent=2)

print(f"Added rich_exhaust case and reordered. Total cases: {len(new_matrix)}")
