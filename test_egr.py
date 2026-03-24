#!/usr/bin/env python3
"""Test EGR stuck open at idle case."""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from core.matrix import match_case, _safe_eval
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

print(f"Calculated lambda: {calculated_lambda}")
print()

# Run diagnosis
matched = match_case(
    low_idle=low_idle,
    calculated_lambda=calculated_lambda,
    measured_lambda=low_idle['lambda'],
    knowledge_base=kb,
    high_idle=None
)

print("=== Match Result ===")
print(f"Case ID: {matched.get('case_id')}")
print(f"Name: {matched.get('name')}")
print(f"Health Score: {matched.get('health_score')}")
print(f"Verdict: {matched.get('verdict')}")
action = matched.get('action', 'N/A')
print(f"Action: {action}")
print()

# Let's also see what the egr_stuck_open_idle case logic evaluates to directly
matrix = kb.get('diagnostic_matrix', [])
egr_case = None
for case in matrix:
    if case.get('case_id') == 'egr_stuck_open_idle':
        egr_case = case
        break

if egr_case:
    print("=== egr_stuck_open_idle case evaluation ===")
    context = {
        'low_idle': low_idle,
        'calculated_lambda': calculated_lambda,
        'measured_lambda': low_idle['lambda'],
        'high_idle': low_idle
    }
    result = _safe_eval(egr_case['logic'], context)
    print(f"Logic: {egr_case['logic']}")
    print(f"Evaluates to: {result}")
    print()

# Show first 5 matches to ensure no earlier shadowing occurs
print("=== First 5 matching cases (to check ordering) ===")
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
        if _safe_eval(logic, context):
            count += 1
            print(f"Row {idx}: {case['case_id']} - {case['name']}")
            if count >= 5:
                break
    except:
        continue
