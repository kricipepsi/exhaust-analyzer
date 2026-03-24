#!/usr/bin/env python3
"""Run the petrol_100_test_suite through the diagnostic engine and report results."""

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

# Load test suite
test_csv = Path("petrol_100_test_suite.csv")
if not test_csv.exists():
    print(f"ERROR: Test suite not found: {test_csv}")
    sys.exit(1)

tests = []
with open(test_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tests.append({
            'id': row['ID'],
            'fuel': row['Fuel'].lower(),
            'co': float(row['CO_Pct']),
            'co2': float(row['CO2_Pct']),
            'hc': int(row['HC_PPM']),
            'o2': float(row['O2_Pct']),
            'nox': int(row['NOx_PPM']),
            'lambda_gas': float(row['Lambda_Gas']),
            'stft': float(row['OBD_STFT']),
            'ltft': float(row['OBD_LTFT']),
            'obd_lambda': float(row['OBD_Lambda']),
            'dtc': row['OBD_DTC'] if row['OBD_DTC'] != 'None' else None,
            'expected': row['Expected_Result'],
            'expected_confidence': float(row['Confidence_Score']),
            'expected_health': int(row['ECU_Health'])
        })

print(f"Loaded {len(tests)} test cases from {test_csv}\n")
print("=" * 60)
print("PETROL DIAGNOSTIC ENGINE - TEST SUITE RUN")
print("=" * 60)
print()

passed = 0
failed = 0
results = []

# Statistics by category
category_stats = {}

for test in tests:
    # Build low_idle gas data (using wideband lambda as sensor)
    low_idle = {
        'lambda': test['obd_lambda'],
        'co': test['co'],
        'co2': test['co2'],
        'hc': test['hc'],
        'o2': test['o2'],
        'nox': test['nox']
    }

    # Validate input
    valid, msg = validate_gas_data(low_idle)
    if not valid:
        print(f"[FAIL] {test['id']}: Validation error: {msg}")
        failed += 1
        results.append({
            'id': test['id'],
            'expected': test['expected'],
            'actual': 'VALIDATION_FAILED',
            'confidence': 0.0,
            'match': False,
            'note': msg,
            'category': test['expected']
        })
        continue

    # Calculate lambda via Bretschneider
    try:
        # Use fuel type: if e0, e5, e10, e85; else default to e10
        fuel_type = test['fuel'] if test['fuel'] in ['e0', 'e5', 'e10', 'e85'] else 'e10'
        calc = calculate_lambda(
            co=test['co'],
            co2=test['co2'],
            hc_ppm=test['hc'],
            o2=test['o2'],
            fuel_type=fuel_type
        )
        calc_lambda = calc['lambda']
    except Exception as e:
        print(f"[FAIL] {test['id']}: Bretschneider error: {e}")
        failed += 1
        results.append({
            'id': test['id'],
            'expected': test['expected'],
            'actual': 'CALC_ERROR',
            'confidence': 0.0,
            'match': False,
            'note': str(e),
            'category': test['expected']
        })
        continue

    # Collect tier data
    dtc_list = [test['dtc']] if test['dtc'] else []
    tier4_low = {
        '0C': 0,  # RPM not provided
        '06': test['stft'],
        '07': test['ltft'],
        '44': test['obd_lambda'],
        '10': 0,  # MAF
        '0B': 0,  # MAP
        '11': 0   # Throttle
    }

    # Run diagnosis
    matched = match_case(
        low_idle=low_idle,
        calculated_lambda=calc_lambda,
        measured_lambda=test['obd_lambda'],
        knowledge_base=kb,
        high_idle=None,
        dtc_codes=dtc_list,
        freeze_frame=None,
        tier4_low=tier4_low,
        tier4_high=None
    )

    actual_name = matched.get('name', '').strip()
    actual_id = matched.get('case_id', '')

    # Normalize strings for comparison
    def normalize(s):
        return s.replace('_', ' ').lower().strip()

    expected_norm = normalize(test['expected'])
    actual_norm = normalize(actual_name) if actual_name else normalize(actual_id)

    # Match if normalized strings equal OR if both indicate same concept (e.g., 'lean running condition' vs 'lean_exhaust')
    # Simple mapping: if expected contains 'lean' and actual contains 'lean', consider partial; but we want exact for strict testing
    success = (expected_norm == actual_norm)

    # Record category stats
    cat = test['expected']
    if cat not in category_stats:
        category_stats[cat] = {'passed': 0, 'failed': 0}
    if success:
        category_stats[cat]['passed'] += 1
    else:
        category_stats[cat]['failed'] += 1

    if success:
        print(f"[PASS] {test['id']}: expected '{test['expected']}', got '{actual_name}'")
        passed += 1
    else:
        print(f"[FAIL] {test['id']}: expected '{test['expected']}', got '{actual_name}'")
        failed += 1

    results.append({
        'id': test['id'],
        'expected': test['expected'],
        'actual': actual_name,
        'actual_id': actual_id,
        'confidence': matched.get('confidence_score', 0.0),
        'match': success,
        'category': cat
    })

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total tests: {len(tests)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Accuracy: {passed/len(tests)*100:.1f}%")
print()

# Category breakdown
print("Category Performance:")
for cat, stats in sorted(category_stats.items(), key=lambda x: -x[1]['passed']):
    total = stats['passed'] + stats['failed']
    pct = stats['passed'] / total * 100 if total > 0 else 0
    print(f"  {cat}: {stats['passed']}/{total} ({pct:.0f}%)")

print()

# Save detailed results
output = {
    'run_date': datetime.now().isoformat(),
    'total': len(tests),
    'passed': passed,
    'failed': failed,
    'accuracy': passed/len(tests)*100,
    'category_stats': category_stats,
    'results': results
}
out_json = Path('petrol_test_run_results.json')
with open(out_json, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Detailed results saved to: {out_json}")

# Exit with code 0 if all passed, else 1
sys.exit(0 if failed == 0 else 1)
