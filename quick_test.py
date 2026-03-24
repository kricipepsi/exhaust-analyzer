#!/usr/bin/env python3
"""Quick validation of core modules without pytest."""

import sys
sys.path.insert(0, '.')

from core.bretschneider import calculate_lambda
from core.catalyst import catalyst_efficiency
from core.validator import validate_gas_data, check_probe_placement
from core.matrix import match_case
from core.reporter import generate_report
import json

# Load KB
with open('data/master_knowledge_base.json', 'r') as f:
    kb = json.load(f)

print("=== VALIDATION TESTS ===\n")

# Test 1: Bretschneider Gold Standard
print("1. Bretschneider Gold Standard (G-001):")
result = calculate_lambda(co=0.05, co2=15.2, hc_ppm=12, o2=0.10, fuel_type='petrol')
print(f"   Lambda: {result['lambda']} (expected ~1.00)")
assert abs(result['lambda'] - 1.00) < 0.02, "Gold standard failed"
print("   PASS\n")

# Test 2: Bretschneider Fail Case (F-001: vacuum leak)
print("2. Bretschneider Fail Case (F-001 - Vacuum Leak):")
result = calculate_lambda(co=0.10, co2=11.5, hc_ppm=450, o2=3.5, fuel_type='petrol')
print(f"   Lambda: {result['lambda']} (expected ~1.15)")
assert result['lambda'] > 1.10, "Vacuum leak lambda too low"
print("   PASS\n")

# Test 3: Catalyst Efficiency Optimal
print("3. Catalyst Efficiency (Optimal):")
eff, status = catalyst_efficiency({'co2': 15.0, 'co': 0.1, 'o2': 0.2}, config=kb.get('catalyst_config'))
print(f"   Efficiency: {eff}%, Status: {status}")
assert eff > 90 and status == "Optimal", "Optimal catalyst failed"
print("   PASS\n")

# Test 4: Catalyst Efficiency Failed
print("4. Catalyst Efficiency (Failed):")
eff, status = catalyst_efficiency({'co2': 10.0, 'co': 1.0, 'o2': 1.0}, config=kb.get('catalyst_config'))
print(f"   Efficiency: {eff}%, Status: {status}")
assert eff < 80 and status == "Failed", "Failed catalyst failed"
print("   PASS\n")

# Test 5: Validator Gatekeeper
print("5. Validator Gatekeeper:")
valid, msg = validate_gas_data({'co': 0.1, 'co2': 14.0, 'hc': 100, 'o2': 0.5, 'lambda': 1.0})
print(f"   Valid: {valid}, Msg: {msg}")
assert valid == True, "Valid data rejected"
print("   PASS\n")

# Test 6: Validator Reject Out of Range
print("6. Validator Reject Out-of-Range:")
valid, msg = validate_gas_data({'co': 20.0, 'co2': 14.0, 'hc': 100, 'o2': 0.5, 'lambda': 1.0})
print(f"   Valid: {valid}, Msg: {msg}")
assert valid == False, "Invalid data should be rejected"
print("   PASS\n")

# Test 6b: Validator NOx Range
print("6b. Validator NOx Range:")
valid, msg = validate_gas_data({'co': 0.1, 'co2': 14.0, 'hc': 100, 'o2': 0.5, 'lambda': 1.0, 'nox': 6000})
print(f"   Valid: {valid}, Msg: {msg}")
assert valid == False, "NOx=6000 should be rejected"
print("   PASS\n")

# Test 7: Probe Placement Check
print("7. Probe Placement Check:")
result = check_probe_placement(co=2.0, co2=5.0)  # sum = 7.0 < 12
print(f"   Warning: {result['message'] if result else 'None'}")
assert result is not None, "Should warn about probe placement"
print("   PASS\n")

# Test 8: Matrix Match Healthy Engine
print("8. Matrix Match (Healthy Engine P_100):")
low_idle = {'lambda': 1.00, 'co': 0.10, 'co2': 15.1, 'hc': 20, 'o2': 0.15, 'nox': 50}
case = match_case(low_idle, 1.00, 1.00, kb)
print(f"   Matched: {case['case_id']} - {case['name']}")
assert case['case_id'] == 'P_100', f"Expected P_100, got {case['case_id']}"
print("   PASS\n")

# Test 9: Matrix Match Exhaust Dilution (P_003)
print("9. Matrix Match (Exhaust Dilution P_003):")
low_idle = {'lambda': 1.12, 'co': 0.15, 'co2': 13.0, 'hc': 800, 'o2': 3.0, 'nox': 50}
case = match_case(low_idle, 1.00, 1.12, kb)  # measured > calculated = dilution trigger
print(f"   Matched: {case['case_id']} - {case['name']}")
assert case['case_id'] == 'P_003', f"Expected P_003, got {case['case_id']}"
print("   PASS\n")

# Test 10: Reporter Penalties
print("10. Reporter Penalties (lambda delta + catalyst):")
report = generate_report(
    low_idle={'lambda': 1.0},
    measured_lambda=1.10,
    calculated_lambda=1.00,
    cat_eff=70,
    cat_status="Failed",
    matched_case={'case_id': 'P_100', 'name': 'Healthy', 'verdict': 'OK', 'action': 'None', 'health_score': 100},
    knowledge_base=kb
)
expected_health = 100 - 10 - 15  # 75
print(f"    Health: {report['overall_health']} (expected {expected_health})")
assert report['overall_health'] == expected_health, "Penalties misapplied"
print("    PASS\n")

# Test 11: High Idle Differential Matching (Vacuum Leak)
print("11. High Idle Differential (Vacuum Leak P_001):")
low_idle_vl = {'lambda': 1.10, 'co': 0.15, 'co2': 13.5, 'hc': 80, 'o2': 2.5, 'nox': 50}
high_idle_vl = {'lambda': 1.00, 'co': 0.10, 'co2': 15.0, 'hc': 20, 'o2': 0.3, 'lambda': 1.00, 'nox': 30}
case = match_case(low_idle_vl, 1.10, 1.10, kb, high_idle=high_idle_vl)
print(f"   Matched: {case['case_id']} - {case['name']}")
assert case['case_id'] == 'P_001', f"Expected P_001, got {case['case_id']}"
print("   PASS\n")

# Test 12: NOx Health Penalty (severe)
print("12. NOx Health Penalty (severe nox=2000):")
report_nox = generate_report(
    low_idle={'lambda': 1.0, 'nox': 2000},
    measured_lambda=1.00,
    calculated_lambda=1.00,
    cat_eff=95,
    cat_status="Optimal",
    matched_case={'case_id': 'P_100', 'name': 'Healthy', 'verdict': 'OK', 'action': 'None', 'health_score': 100},
    knowledge_base=kb
)
print(f"    Health: {report_nox['overall_health']} (expected 85, 100-15 for severe NOx)")
assert report_nox['overall_health'] == 85, f"Expected 85, got {report_nox['overall_health']}"
assert report_nox['nox_warning'] is not None, "Should have nox_warning"
print(f"    Warning: {report_nox['nox_warning']}")
print("    PASS\n")

print("=== ALL TESTS PASSED ===")
print("Core modules are functioning correctly.")
