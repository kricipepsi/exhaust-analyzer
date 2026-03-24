#!/usr/bin/env python3
"""Run the 100CVS test suite against the diagnostic engine."""

import sys
from pathlib import Path
import json
import csv
import io

sys.path.insert(0, str(Path(__file__).parent))

from core.matrix import match_case
from core.bretschneider import calculate_lambda
from core.validator import validate_gas_data

# Load knowledge base
with open("data/expanded_knowledge_base.json", 'r') as f:
    kb = json.load(f)

# Parse the 100CVS.md data (CSV format)
csv_path = Path(r"C:\Users\asus\Documents\1nov\100CVS.md")
with open(csv_path, 'r', encoding='utf-8') as f:
    content = f.read().strip()

reader = csv.DictReader(io.StringIO(content))
tests = []
for row in reader:
    tests.append({
        'id': row['ID'],
        'fuel': row['Fuel'].lower(),
        'co': float(row['CO_Pct']),
        'co2': float(row['CO2_Pct']),
        'hc': int(row['HC_PPM']),
        'o2': float(row['O2_Pct']),
        'nox': int(float(row['NOx_PPM'])),
        'lambda_gas': float(row['Lambda_Gas']),  # computed lambda (unused)
        'stft': float(row['OBD_STFT']),
        'ltft': float(row['OBD_LTFT']),
        'obd_lambda': float(row['OBD_Lambda']),  # wideband lambda - sensor reading
        'dtc': row['OBD_DTC'] if row['OBD_DTC'] != 'None' else None,
        'expected': row['Expected_Result'],
        'expected_confidence': float(row['Confidence_Score']),
        'expected_health': int(row['ECU_Health'])
    })

print(f"Loaded {len(tests)} test cases from 100CVS.md\n")
print("=== Running Diagnostic Engine ===\n")

passed = 0
failed = 0
results = []

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

    # Step: Validate input
    valid, msg = validate_gas_data(low_idle)

    # Check if this is expected to be invalid
    is_invalid_expected = test['expected'].startswith('INVALID_INPUT')
    if is_invalid_expected:
        if not valid:
            print(f"[PASS] Test {test['id']}: Expected invalid input, caught: {msg}")
            passed += 1
            results.append({
                'id': test['id'],
                'expected': test['expected'],
                'actual': 'INVALID_REJECTED',
                'actual_id': None,
                'confidence': 0.0,
                'match': True,
                'note': msg
            })
            continue
        else:
            print(f"[FAIL] Test {test['id']}: Expected invalid input but validation passed: {msg}")
            failed += 1
            results.append({
                'id': test['id'],
                'expected': test['expected'],
                'actual': 'VALID_UNEXPECTED',
                'actual_id': None,
                'confidence': 0.0,
                'match': False,
                'note': msg
            })
            continue

    if not valid:
        print(f"[FAIL] Test {test['id']}: Validation error: {msg}")
        failed += 1
        results.append({
            'id': test['id'],
            'expected': test['expected'],
            'actual': 'VALIDATION_FAILED',
            'actual_id': None,
            'confidence': 0.0,
            'match': False,
            'note': msg
        })
        continue

    # Calculate lambda using Bretschneider
    try:
        fuel_type = test['fuel'] if test['fuel'] in ['e0','e5','e10','e85'] else 'e10'
        calc = calculate_lambda(
            co=test['co'],
            co2=test['co2'],
            hc_ppm=test['hc'],
            o2=test['o2'],
            fuel_type=fuel_type
        )
        calc_lambda = calc['lambda']
    except Exception as e:
        print(f"[FAIL] Test {test['id']}: Bretschneider error: {e}")
        failed += 1
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

    # Normalize for comparison: replace underscores with spaces, lower case
    def normalize(s):
        return s.replace('_', ' ').lower()

    expected_norm = normalize(test['expected'])
    actual_norm = normalize(actual_name) if actual_name else normalize(actual_id)

    success = (expected_norm == actual_norm)

    success = (expected_norm == actual_norm)

    if success:
        print(f"[PASS] Test {test['id']}: expected '{test['expected']}', got '{actual_name}' (conf: {matched.get('confidence_score', 0):.2f})")
        passed += 1
    else:
        print(f"[FAIL] Test {test['id']}: expected '{test['expected']}', got '{actual_name}' (case_id: {actual_id})")
        failed += 1

    results.append({
        'id': test['id'],
        'expected': test['expected'],
        'actual': actual_name,
        'actual_id': actual_id,
        'confidence': matched.get('confidence_score', 0),
        'match': success
    })

# Summary
print("\n=== TEST RESULTS SUMMARY ===")
print(f"Total: {len(tests)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Accuracy: {passed/len(tests)*100:.1f}%\n")

if failed > 0:
    print("=== FAILURES ===")
    for r in results:
        if not r['match']:
            print(f"ID {r['id']}: expected '{r['expected']}', got '{r['actual']}' (conf: {r['confidence']:.2f})")
    print()

# Save detailed results
output = {
    'total': len(tests),
    'passed': passed,
    'failed': failed,
    'accuracy': passed/len(tests)*100,
    'results': results
}
with open('test_100cvs_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print("Detailed results saved to test_100cvs_results.json")
