#!/usr/bin/env python3
"""Run the diagnostic_test_suite.csv with mapping to knowledge base case names."""

import sys
from pathlib import Path
import csv
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.matrix import match_case
from core.bretschneider import calculate_lambda
from core.validator import validate_gas_data

# Load knowledge base
with open("data/expanded_knowledge_base.json", 'r') as f:
    kb = json.load(f)

# Mapping from Expected_Result codes to actual case names in KB
EXPECTED_MAP = {
    'P0420': 'Catalytic Converter Efficiency Failure',
    'P0430': 'Catalytic Converter Efficiency Failure',  # same case
    'EXHAUST_LEAK': 'Exhaust Leak (False Lean)',
    'VACUUM_LEAK': 'Intake Vacuum Leak',
    'RICH': 'System Running Rich',
    'LEAN': 'Fuel Delivery Problem (Lean)',  # our lean pattern
    'MISFIRE': 'Engine Misfire',
    'COLD_START': 'Cold Start Enrichment',
    'O2_SENSOR': 'O2 Sensor Sluggish or Failed',
    'MAF_UNDER': 'MAF Sensor Under-Reading',
    'HEALTHY': 'Healthy Engine',
    'TIMING_ADVANCE': 'Excessively Advanced Timing',
    'TIMING_RETARD': 'Ignition Timing Issues (Retard)',
    # Add fallback: if code not in map, use as-is after replacing underscores
}

# Load test suite
csv_path = Path(r"C:\Users\asus\Documents\1nov\diagnostic_test_suite.csv")
if not csv_path.exists():
    print(f"ERROR: Test suite not found: {csv_path}")
    sys.exit(1)

with open(csv_path, 'r', encoding='utf-16') as f:
    reader = csv.DictReader(f)
    tests = []
    for row in reader:
        # Map expected result
        expected_code = row['Expected_Result'].strip()
        expected_name = EXPECTED_MAP.get(expected_code, expected_code.replace('_', ' ').title())
        tests.append({
            'ID': row['ID'],
            'Fuel': row['Fuel'],
            'CO_Pct': float(row['CO_Pct']),
            'CO2_Pct': float(row['CO2_Pct']),
            'HC_PPM': int(row['HC_PPM']),
            'O2_Pct': float(row['O2_Pct']),
            'NOx_PPM': int(float(row['NOx_PPM'])),
            'Lambda_Gas': float(row['Lambda_Gas']),
            'OBD_STFT': float(row['OBD_STFT']),
            'OBD_LTFT': float(row['OBD_LTFT']),
            'OBD_Lambda': float(row['OBD_Lambda']),
            'OBD_DTC': row['OBD_DTC'] if row['OBD_DTC'] and row['OBD_DTC'] != 'None' else None,
            'expected': expected_name
        })

print(f"Loaded {len(tests)} test cases from diagnostic_test_suite.csv")
print("Expected categories:", sorted(set([t['expected'] for t in tests])))
print()

passed = 0
failed = 0
fails = []

for test in tests:
    low_idle = {
        'lambda': test['OBD_Lambda'],
        'co': test['CO_Pct'],
        'co2': test['CO2_Pct'],
        'hc': test['HC_PPM'],
        'o2': test['O2_Pct'],
        'nox': test['NOx_PPM']
    }
    valid, vmsg = validate_gas_data(low_idle)
    if not valid:
        failed += 1
        fails.append((test['ID'], test['expected'], f"VALIDATION: {vmsg}"))
        continue

    try:
        fuel_type = test['Fuel'].lower() if test['Fuel'].lower() in ['e0','e5','e10','e85'] else 'e10'
        calc = calculate_lambda(co=test['CO_Pct'], co2=test['CO2_Pct'], hc_ppm=test['HC_PPM'], o2=test['O2_Pct'], fuel_type=fuel_type)
        calc_lambda = calc['lambda']
    except Exception as e:
        failed += 1
        fails.append((test['ID'], test['expected'], f"CALC: {e}"))
        continue

    dtc_list = [test['OBD_DTC']] if test['OBD_DTC'] else []
    tier4_low = {
        '0C': 0,
        '06': test['OBD_STFT'],
        '07': test['OBD_LTFT'],
        '44': test['OBD_Lambda'],
        '10': 0,
        '0B': 0,
        '11': 0
    }

    matched = match_case(
        low_idle=low_idle,
        calculated_lambda=calc_lambda,
        measured_lambda=test['OBD_Lambda'],
        knowledge_base=kb,
        high_idle=None,
        dtc_codes=dtc_list,
        freeze_frame=None,
        tier4_low=tier4_low,
        tier4_high=None
    )
    actual = matched.get('name','').strip()
    # Normalize
    norm_actual = actual.replace('_',' ').lower()
    norm_expected = test['expected'].replace('_',' ').lower()
    if norm_actual == norm_expected:
        passed += 1
    else:
        failed += 1
        fails.append((test['ID'], test['expected'], actual))

print("="*60)
print(f"TOTAL: {len(tests)}  PASSED: {passed}  FAILED: {failed}  ACCURACY: {passed/len(tests)*100:.1f}%")
print("="*60)

# Save detailed failures CSV
fail_csv = Path('diagnostic_suite_failures.csv')
with open(fail_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID','Expected','Actual'])
    for tid, exp, act in fails:
        writer.writerow([tid, exp, act])
print(f"\nFailure details CSV written to: {fail_csv}")

# Also print summary by category
from collections import Counter
cat_fails = Counter()
for tid, exp, act in fails:
    cat_fails[exp] += 1
print("\nFailure breakdown by expected category:")
for cat, cnt in cat_fails.most_common():
    print(f"  {cat}: {cnt}")

# Save summary
summary = {
    'timestamp': datetime.now().isoformat(),
    'total': len(tests),
    'passed': passed,
    'failed': failed,
    'accuracy': passed/len(tests)*100,
    'failures': fails
}
with open('diagnostic_suite_results.json','w') as f:
    json.dump(summary, f, indent=2)
print("Results saved to diagnostic_suite_results.json")

sys.exit(0 if failed==0 else 1)
