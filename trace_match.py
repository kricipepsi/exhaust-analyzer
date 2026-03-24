#!/usr/bin/env python3
"""Diagnose the sample data with detailed trace."""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from core.matrix import match_case, _safe_eval
from core.bretschneider import calculate_lambda

# Load KB
with open("data/expanded_knowledge_base.json", 'r') as f:
    kb = json.load(f)

# Sample data
low_idle = {
    'lambda': 0.979,
    'co': 1.26,
    'co2': 13.81,
    'hc': 166,
    'o2': 0.426,
    'nox': 1183
}

# Calculate lambda
calc = calculate_lambda(co=1.26, co2=13.81, hc_ppm=166, o2=0.426, fuel_type='e10')
calculated_lambda = calc['lambda']

print(f"Calculated lambda: {calculated_lambda}")
print()

# Manually iterate to see which case matches first
matrix = kb.get('diagnostic_matrix', [])
high_idle_ctx = low_idle  # none provided

for idx, case in enumerate(matrix):
    logic = case.get('logic', '')
    if not logic:
        continue
    context = {
        'low_idle': low_idle,
        'calculated_lambda': calculated_lambda,
        'measured_lambda': low_idle['lambda'],
        'high_idle': high_idle_ctx
    }
    try:
        result = _safe_eval(logic, context)
        if result:
            print(f"FIRST MATCH at row {idx}: {case['case_id']} - {case['name']}")
            print(f"Logic: {logic}")
            print()
            # Print a few more subsequent matches to see alternatives
            print("Subsequent matching cases:")
            for j in range(idx+1, len(matrix)):
                c2 = matrix[j]
                l2 = c2.get('logic', '')
                if not l2:
                    continue
                if _safe_eval(l2, context):
                    print(f"  Row {j}: {c2['case_id']} - {c2['name']}")
            break
    except Exception as e:
        print(f"Error in row {idx}: {e}")
        continue
else:
    print("No match found.")
