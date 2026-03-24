#!/usr/bin/env python3
"""End-to-end integration test: simulate running the full diagnostic on typical data."""

import json
from core.validator import validate_gas_data, check_probe_placement
from core.bretschneider import calculate_lambda
from core.catalyst import catalyst_efficiency
from core.matrix import match_case
from core.reporter import generate_report

# Load expanded KB
kb = json.load(open('data/expanded_knowledge_base.json'))

# Simulate a healthy engine reading
low_idle = {
    'lambda': 1.00,   # wideband O2 sensor
    'co': 0.12,
    'co2': 14.8,
    'hc': 25,
    'o2': 0.25,
    'nox': 50
}
fuel_type = 'e10'

print("=== END-TO-END DIAGNOSTIC TEST ===\n")

# 1. Validate
valid, msg = validate_gas_data(low_idle)
print(f"1. Validation: {msg}")
if not valid:
    print("   ABORT")
    exit(1)

# 2. Probe check
probe = check_probe_placement(low_idle['co'], low_idle['co2'])
if probe:
    print(f"2. Probe Warning: {probe['message']}")

# 3. Calculate theoretical lambda
calc = calculate_lambda(low_idle['co'], low_idle['co2'], low_idle['hc'], low_idle['o2'], fuel_type)
calc_lambda = calc['lambda']
print(f"3. Bretschneider Lambda: {calc_lambda:.3f} (measured: {low_idle['lambda']})")

# 4. Catalyst efficiency
cat_eff, cat_status = catalyst_efficiency(low_idle, config=kb.get('catalyst_config'))
print(f"4. Catalyst Efficiency: {cat_eff}% ({cat_status})")

# 5. Match case
high_idle = None  # No high idle data for this test
case = match_case(low_idle, calc_lambda, low_idle['lambda'], kb, high_idle=high_idle)
print(f"5. Matched Case: {case['case_id']} - {case['name']}")

# 6. Generate final report
report = generate_report(
    low_idle=low_idle,
    measured_lambda=low_idle['lambda'],
    calculated_lambda=calc_lambda,
    cat_eff=cat_eff,
    cat_status=cat_status,
    matched_case=case,
    knowledge_base=kb
)

print(f"\n=== FINAL ASSESSMENT ===")
print(f"Overall Health: {report['overall_health']}/100")
print(f"Verdict: {report['verdict']}")
print(f"Action: {report['action']}")
print(f"Lambda Delta: {report['lambda_delta']:.3f}")
