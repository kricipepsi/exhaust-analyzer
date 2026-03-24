#!/usr/bin/env python3
"""Test diagnostic engine with sample catalyst fault data."""

import sys
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.matrix import match_case
from core.bretschneider import calculate_lambda

# Load knowledge base
kb_path = project_root / "data" / "expanded_knowledge_base.json"
with open(kb_path, 'r') as f:
    kb = json.load(f)

# Sample data from user (P0420 catalyst fault)
low_idle = {
    'lambda': 0.979,
    'co': 1.26,
    'co2': 13.81,
    'hc': 166,
    'o2': 0.426,
    'nox': 1183
}

# Calculate lambda using Bretschneider (assuming E10 fuel, cold engine=False)
calc_result = calculate_lambda(
    co=1.26,
    co2=13.81,
    hc_ppm=166,
    o2=0.426,
    fuel_type='e10'
)
calculated_lambda = calc_result['lambda']

print("=== Input Data ===")
print(f"Low idle: {low_idle}")
print(f"Calculated lambda: {calculated_lambda:.4f}")
print(f"Measured lambda: {low_idle['lambda']:.4f}")
print()

# Run diagnosis (no high idle data)
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
print(f"Action: {matched.get('action')}")
print()

# Show a few relevant cases that should have matched but maybe didn't
print("=== Checking specific cases ===")
matrix = kb.get('diagnostic_matrix', [])
catalyst_cases = [c for c in matrix if 'catalyst' in c.get('name', '').lower()]
egr_cases = [c for c in matrix if 'egr' in c.get('name', '').lower() and 'stuck' in c.get('name', '').lower()]

print(f"Found {len(catalyst_cases)} catalyst-related cases")
print(f"Found {len(egr_cases)} EGR stuck cases")
print()

# Show catalyst case logic
for c in catalyst_cases:
    print(f"[{c['case_id']}] {c['name']}")
    print(f"  Logic: {c.get('logic')}")
    print()

# Test each catalyst case manually
print("=== Manual evaluation of catalyst cases ===")
for case in catalyst_cases:
    logic = case.get('logic')
    if not logic:
        continue
    context = {
        'low_idle': low_idle,
        'calculated_lambda': calculated_lambda,
        'measured_lambda': low_idle['lambda'],
        'high_idle': low_idle  # mirror
    }
    # Use same safe eval as in matrix module
    from core.matrix import _safe_eval
    result = _safe_eval(logic, context)
    print(f"{case['case_id']}: {result}")
