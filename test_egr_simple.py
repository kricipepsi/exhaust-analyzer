#!/usr/bin/env python3
"""Test EGR stuck open at idle case - simplified output."""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from core.matrix import match_case
from core.bretschneider import calculate_lambda

# Load KB
with open("data/expanded_knowledge_base.json", 'r') as f:
    kb = json.load(f)

# Sample data from user (EGR stuck open at idle)
low_idle = {
    'lambda': 0.99,
    'co': 2.27,
    'co2': 12.52,
    'hc': 1663,
    'o2': 2.71,
    'nox': 13.2
}

# Calculate lambda
calc = calculate_lambda(co=2.27, co2=12.52, hc_ppm=1663, o2=2.71, fuel_type='e10')
calculated_lambda = calc['lambda']

print(f"Calculated lambda: {calculated_lambda:.3f}")
print()

# Run diagnosis
matched = match_case(
    low_idle=low_idle,
    calculated_lambda=calculated_lambda,
    measured_lambda=low_idle['lambda'],
    knowledge_base=kb,
    high_idle=None
)

print("MATCH RESULT:")
print(f"  Case ID: {matched.get('case_id')}")
print(f"  Name: {matched.get('name')}")
print(f"  Health Score: {matched.get('health_score')}")
print()

# Show the first 3 matches to confirm no earlier shadowing
print("First 3 matching cases in order:")
matrix = kb.get('diagnostic_matrix', [])
count = 0
for idx, case in enumerate(matrix):
    logic = case.get('logic', '')
    if not logic:
        continue
    context = {
        'low_idle': low_idle,
        'calculated_lambda': calculated_lambda,
        'measured_lambda': low_idle['lambda'],
        'high_idle': low_idle
    }
    try:
        # Use internal eval
        from core.matrix import _safe_eval
        if _safe_eval(logic, context):
            count += 1
            print(f"  Row {idx}: {case['case_id']} - {case['name']}")
            if count >= 3:
                break
    except:
        continue
