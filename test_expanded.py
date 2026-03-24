#!/usr/bin/env python3
"""Test suite for expanded knowledge base after reordering fix."""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from core.matrix import match_case
from core.bretschneider import calculate_lambda

# Load expanded KB
with open("data/expanded_knowledge_base.json", 'r') as f:
    kb = json.load(f)

print("=== EXPANDED KB REGRESSION TESTS ===\n")

test_cases = [
    {
        "name": "Catalyst Failure (P0420 pattern)",
        "data": {
            'lambda': 0.979,
            'co': 1.26,
            'co2': 13.81,
            'hc': 166,
            'o2': 0.426,
            'nox': 1183
        },
        "expected_id": "catalyst_failure",
        "fuel": "e10"
    },
    {
        "name": "EGR Stuck Open at Idle",
        "data": {
            'lambda': 0.99,
            'co': 2.27,
            'co2': 12.52,
            'hc': 1663,
            'o2': 2.71,
            'nox': 13.2
        },
        "expected_id": "pattern_004",  # EGR Stuck Open
        "fuel": "e10"
    },
    {
        "name": "Healthy Engine",
        "data": {
            'lambda': 1.00,
            'co': 0.10,
            'co2': 15.2,
            'hc': 20,
            'o2': 0.15,
            'nox': 30
        },
        "expected_id": "P_100",
        "fuel": "e10"
    },
    {
        "name": "Exhaust Dilution (False Lean)",
        "data": {
            'lambda': 1.12,
            'co': 0.15,
            'co2': 13.0,
            'hc': 800,
            'o2': 3.0,
            'nox': 50
        },
        # Measured lambda > calculated -> dilution
        "expected_id": "P_003",
        "fuel": "e10"
    },
    {
        "name": "Vacuum Leak Differential (with high idle)",
        "data": {
            'low': {
                'lambda': 1.10,
                'co': 0.15,
                'co2': 13.5,
                'hc': 80,
                'o2': 2.5,
                'nox': 50
            },
            'high': {
                'lambda': 1.00,
                'co': 0.10,
                'co2': 15.0,
                'hc': 20,
                'o2': 0.3,
                'nox': 30
            }
        },
        "expected_id": "P_001",
        "fuel": "e10"
    },
    {
        "name": "High NOx + Lean (EGR cooling failure)",
        "data": {
            'lambda': 1.08,
            'co': 0.20,
            'co2': 13.0,
            'hc': 100,
            'o2': 1.8,
            'nox': 900
        },
        "expected_id": "high_nox_lean_egr",
        "fuel": "e10"
    },
    {
        "name": "High NOx + Timing Over-Advanced",
        "data": {
            'lambda': 1.00,
            'co': 0.10,
            'co2': 14.0,
            'hc': 30,
            'o2': 0.3,
            'nox': 600
        },
        "expected_id": "high_nox_timing_advance",
        "fuel": "e10"
    }
]

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    name = test['name']
    expected = test['expected_id']
    fuel = test.get('fuel', 'e10')

    if 'low' in test['data'] and 'high' in test['data']:
        # Vacuum leak test with high idle
        low = test['data']['low']
        high = test['data']['high']
        calc = calculate_lambda(
            co=low['co'], co2=low['co2'], hc_ppm=low['hc'], o2=low['o2'], fuel_type=fuel
        )
        calc_lambda = calc['lambda']
        matched = match_case(low, calc_lambda, low['lambda'], kb, high_idle=high)
    else:
        low = test['data']
        calc = calculate_lambda(
            co=low['co'], co2=low['co2'], hc_ppm=low['hc'], o2=low['o2'], fuel_type=fuel
        )
        calc_lambda = calc['lambda']
        matched = match_case(low, calc_lambda, low['lambda'], kb, high_idle=None)

    got = matched.get('case_id')
    if got == expected:
        print(f"[PASS] Test {i}: {name}")
        passed += 1
    else:
        print(f"[FAIL] Test {i}: {name}")
        print(f"    Expected: {expected}")
        print(f"    Got: {got}")
        failed += 1

print(f"\n=== SUMMARY ===")
print(f"Passed: {passed}/{len(test_cases)}")
print(f"Failed: {failed}/{len(test_cases)}")

if failed == 0:
    print("\nAll expanded KB tests passed!")
else:
    print("\nSome tests failed. Review knowledge base ordering/rules.")
    sys.exit(1)
