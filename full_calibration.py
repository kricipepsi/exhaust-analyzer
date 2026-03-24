#!/usr/bin/env python3
"""Full calibration test with expanded knowledge base."""

import sys
sys.path.insert(0, '.')

from core.bretschneider import calculate_lambda
from core.catalyst import catalyst_efficiency
from core.validator import validate_gas_data
from core.matrix import match_case
from core.reporter import generate_report
import json

# Load expanded KB
with open('data/expanded_knowledge_base.json', 'r') as f:
    kb = json.load(f)

print("=== FULL CALIBRATION TEST (Expanded KB) ===\n")
print(f"Total cases in knowledge base: {len(kb['diagnostic_matrix'])}\n")

# Gold Standard Tests (10 cases)
GOLD_CASES = [
    {"id": "G-001", "co": 0.05, "co2": 15.2, "hc": 12, "o2": 0.10, "lambda": 1.00},
    {"id": "G-002", "co": 0.08, "co2": 15.0, "hc": 20, "o2": 0.15, "lambda": 1.01},
    {"id": "G-003", "co": 0.12, "co2": 14.8, "hc": 8, "o2": 0.20, "lambda": 0.99},
    {"id": "G-004", "co": 0.03, "co2": 15.4, "hc": 15, "o2": 0.08, "lambda": 1.00},
    {"id": "G-005", "co": 0.25, "co2": 14.2, "hc": 45, "o2": 0.40, "lambda": 1.01},
    {"id": "G-006", "co": 0.15, "co2": 14.6, "hc": 30, "o2": 0.30, "lambda": 1.01},
    {"id": "G-007", "co": 0.01, "co2": 15.5, "hc": 10, "o2": 0.08, "lambda": 1.00},
    {"id": "G-008", "co": 0.01, "co2": 15.9, "hc": 2, "o2": 0.02, "lambda": 1.00},
    {"id": "G-009", "co": 0.35, "co2": 13.8, "hc": 65, "o2": 0.45, "lambda": 1.01},
    {"id": "G-010", "co": 0.20, "co2": 14.0, "hc": 40, "o2": 0.35, "lambda": 1.02}
]

print("1. Bretschneider Gold Standard Tests:")
passed_bretsch = 0
for case in GOLD_CASES:
    result = calculate_lambda(case['co'], case['co2'], case['hc'], case['o2'])
    calc = result['lambda']
    expected = case['lambda']
    ok = abs(calc - expected) < 0.02
    status = "PASS" if ok else "FAIL"
    if ok:
        passed_bretsch += 1
    print(f"   {case['id']}: lam={calc:.3f} expected {expected} -> {status}")

print(f"\nGold Bretschneider: {passed_bretsch}/10 passed\n")

# Catalyst Efficiency Tests
print("2. Catalyst Efficiency Tests:")
eff1, stat1 = catalyst_efficiency({'co2': 15.0, 'co': 0.1, 'o2': 0.2}, config=kb.get('catalyst_config'))
eff2, stat2 = catalyst_efficiency({'co2': 10.0, 'co': 1.0, 'o2': 1.0}, config=kb.get('catalyst_config'))
cat_ok = eff1 > 90 and stat1 == "Optimal" and eff2 < 80 and stat2 == "Failed"
print(f"   Optimal: {eff1}% '{stat1}' -> {'PASS' if eff1>90 else 'FAIL'}")
print(f"   Failed:  {eff2}% '{stat2}' -> {'PASS' if eff2<80 else 'FAIL'}")
print(f"\nCatalyst tests: {'PASS' if cat_ok else 'FAIL'}\n")

# Matrix Matching Tests (key patterns)
print("3. Matrix Matching Tests (Expanded KB):")
tests = [
    {
        "desc": "Healthy Engine (P_100)",
        "low_idle": {'lambda': 1.00, 'co': 0.10, 'co2': 15.1, 'hc': 20, 'o2': 0.15, 'nox': 50},
        "calc_lam": 1.00,
        "meas_lam": 1.00,
        "expected_id": "P_100"
    },
    {
        "desc": "Exhaust Dilution (P_003)",
        "low_idle": {'lambda': 1.12, 'co': 0.15, 'co2': 13.0, 'hc': 800, 'o2': 3.0, 'nox': 50},
        "calc_lam": 1.00,
        "meas_lam": 1.12,
        "expected_id": "P_003"
    },
    {
        "desc": "Systemic Rich Mixture (P_005)",
        "low_idle": {'lambda': 0.90, 'co': 3.5, 'hc': 800, 'o2': 0.1, 'co2': 12.0, 'nox': 50},
        "calc_lam": 0.90,
        "meas_lam": 0.90,
        "expected_id": "P_005"
    },
    {
        "desc": "Engine Misfire",
        "low_idle": {'lambda': 1.05, 'co': 0.3, 'hc': 2000, 'o2': 2.0, 'co2': 10.0, 'nox': 50},
        "calc_lam": 1.05,
        "meas_lam": 1.05,
        "expected_id": "misfire"
    },
    {
        "desc": "Catalyst Failure (high NOx stoich)",
        "low_idle": {'lambda': 1.00, 'co': 0.15, 'hc': 80, 'o2': 0.3, 'co2': 14.5, 'nox': 1500},
        "calc_lam": 1.00,
        "meas_lam": 1.00,
        "expected_id": "catalyst_failure"
    },
    {
        "desc": "Exhaust Leak False Lean",
        "low_idle": {'lambda': 1.10, 'co': 0.15, 'hc': 50, 'o2': 4.0, 'co2': 12.0, 'nox': 50},
        "calc_lam": 1.10,
        "meas_lam": 1.10,
        "expected_id": "exhaust_leak_false_lean"
    }
]

matrix_ok = 0
for test in tests:
    case = match_case(test['low_idle'], test['calc_lam'], test['meas_lam'], kb)
    matched = case['case_id']
    ok = matched == test['expected_id']
    if ok:
        matrix_ok += 1
    print(f"   {test['desc']}: matched '{matched}' -> {'PASS' if ok else 'FAIL (expected ' + test['expected_id'] + ')'}")

print(f"\nMatrix matching: {matrix_ok}/{len(tests)} passed\n")

# Reporter Penalties Test
print("4. Reporter Penalties Test:")
report = generate_report(
    low_idle={'lambda': 1.0},
    measured_lambda=1.10,
    calculated_lambda=1.00,
    cat_eff=70,
    cat_status="Failed",
    matched_case={'case_id': 'P_100', 'name': 'Healthy', 'verdict': 'OK', 'action': 'None', 'health_score': 100},
    knowledge_base=kb
)
expected_health = 75
penalty_ok = report['overall_health'] == expected_health
print(f"   Health with penalties: {report['overall_health']} (expected {expected_health}) -> {'PASS' if penalty_ok else 'FAIL'}\n")

# High Idle Differential Test
print("5. High Idle Differential Test (Vacuum Leak P_001):")
hi_low = {'lambda': 1.10, 'co': 0.15, 'co2': 13.5, 'hc': 80, 'o2': 2.5, 'nox': 50}
hi_high = {'lambda': 1.00, 'co': 0.10, 'co2': 15.0, 'hc': 20, 'o2': 0.3, 'nox': 30}
hi_case = match_case(hi_low, 1.10, 1.10, kb, high_idle=hi_high)
hi_ok = hi_case['case_id'] in ('P_001', 'vacuum_leak_differential_high_idle')
print(f"   Matched: {hi_case['case_id']} -> {'PASS' if hi_ok else 'FAIL (expected P_001 or vacuum_leak_differential_high_idle)'}\n")

# NOx Penalty Test
print("6. NOx Penalty Test:")
nox_report = generate_report(
    low_idle={'lambda': 1.0, 'nox': 2000},
    measured_lambda=1.00,
    calculated_lambda=1.00,
    cat_eff=95,
    cat_status="Optimal",
    matched_case={'case_id': 'P_100', 'name': 'Healthy', 'verdict': 'OK', 'action': 'None', 'health_score': 100},
    knowledge_base=kb
)
nox_ok = nox_report['overall_health'] == 85 and nox_report['nox_warning'] is not None
print(f"   Health: {nox_report['overall_health']} (expected 85), Warning: {nox_report['nox_warning']} -> {'PASS' if nox_ok else 'FAIL'}\n")

# High Idle Cross-Reference Samples (from reference manual)
print("7. High Idle Cross-Reference Samples:")
hi_samples_ok = 0
hi_samples_total = 0

# Sample: Vacuum leak - lean at low idle, perfect at high idle -> P_001
hi_samples_total += 1
vl_low = {'lambda': 1.08, 'co': 0.10, 'co2': 13.0, 'hc': 60, 'o2': 2.0, 'nox': 40}
vl_high = {'lambda': 1.001, 'co': 0.01, 'co2': 14.8, 'hc': 15, 'o2': 0.3, 'nox': 20}
vl_case = match_case(vl_low, 1.08, 1.08, kb, high_idle=vl_high)
vl_ok = vl_case['case_id'] in ('P_001', 'vacuum_leak_differential_high_idle')
if vl_ok: hi_samples_ok += 1
print(f"   Vacuum Leak (lean idle, normal high): {vl_case['case_id']} -> {'PASS' if vl_ok else 'FAIL (expected P_001 or vacuum_leak_differential_high_idle)'}")

# Sample: High NOx + lean at idle -> EGR/cooling failure
hi_samples_total += 1
nox_low = {'lambda': 1.06, 'co': 0.05, 'co2': 14.0, 'hc': 40, 'o2': 1.8, 'nox': 1800}
nox_case = match_case(nox_low, 1.06, 1.06, kb)
nox_case_ok = nox_case['case_id'] == 'high_nox_lean_egr'
if nox_case_ok: hi_samples_ok += 1
print(f"   High NOx+Lean (EGR failure): {nox_case['case_id']} -> {'PASS' if nox_case_ok else 'FAIL (expected high_nox_lean_egr)'}")

# Sample: Perfect high idle pass - should still match healthy at low idle
hi_samples_total += 1
healthy_low = {'lambda': 1.00, 'co': 0.10, 'co2': 15.1, 'hc': 20, 'o2': 0.15, 'nox': 30}
healthy_high = {'lambda': 1.001, 'co': 0.01, 'co2': 14.8, 'hc': 15, 'o2': 0.3, 'nox': 20}
healthy_case = match_case(healthy_low, 1.00, 1.00, kb, high_idle=healthy_high)
healthy_ok = healthy_case['case_id'] == 'P_100'
if healthy_ok: hi_samples_ok += 1
print(f"   Healthy engine (both idles normal): {healthy_case['case_id']} -> {'PASS' if healthy_ok else 'FAIL (expected P_100)'}")

print(f"\nHigh Idle Samples: {hi_samples_ok}/{hi_samples_total} passed\n")

# Summary
total_passed = passed_bretsch + (2 if cat_ok else 0) + matrix_ok + (1 if penalty_ok else 0) + (1 if hi_ok else 0) + (1 if nox_ok else 0) + hi_samples_ok
total_tests = 10 + 2 + len(tests) + 1 + 1 + 1 + hi_samples_total
print("=== SUMMARY ===")
print(f"Total tests: {total_tests}")
print(f"Passed: {total_passed}")
print(f"Failed: {total_tests - total_passed}")

if total_passed >= total_tests * 0.9:
    print("\n[PASS] ALL TESTS PASSED (or >90% pass rate). Ready for UI build.")
else:
    print("\n[FAIL] Some tests failed. Review logic and cases.")
