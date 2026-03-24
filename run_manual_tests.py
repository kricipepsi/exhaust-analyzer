#!/usr/bin/env python3
"""Run the 11-case manual test suite as defined in testsuitemanual.md."""

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

# Load manual test suite
test_csv = Path("manual_test_suite.csv")
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
            'nox': int(float(row['NOx_PPM'])),
            'lambda_gas': float(row['Lambda_Gas']),
            'stft': float(row['OBD_STFT']),
            'ltft': float(row['OBD_LTFT']),
            'obd_lambda': float(row['OBD_Lambda']),
            'dtc': row['OBD_DTC'] if row['OBD_DTC'] != 'None' else None,
            'expected': row['Expected_Result'],
            'expected_confidence': float(row['Confidence_Score']),
            'expected_health': int(row['ECU_Health'])
        })

print("=" * 70)
print("MANUAL TEST SUITE EXECUTION")
print("Based on: testsuitemanual.md")
print("=" * 70)
print()

passed = 0
failed = 0
results = []

for test in tests:
    # Build low_idle
    low_idle = {
        'lambda': test['obd_lambda'],
        'co': test['co'],
        'co2': test['co2'],
        'hc': test['hc'],
        'o2': test['o2'],
        'nox': test['nox']
    }

    # Validate
    valid, msg = validate_gas_data(low_idle)
    if not valid:
        print(f"[FAIL] {test['id']}: Validation error: {msg}")
        failed += 1
        results.append({**test, 'actual': 'VALIDATION_FAILED', 'match': False, 'note': msg})
        continue

    # Calculate lambda
    try:
        fuel_type = test['fuel'] if test['fuel'] in ['e0','e5','e10','e85'] else 'e10'
        calc = calculate_lambda(co=test['co'], co2=test['co2'], hc_ppm=test['hc'], o2=test['o2'], fuel_type=fuel_type)
        calc_lambda = calc['lambda']
    except Exception as e:
        print(f"[FAIL] {test['id']}: Bretschneider error: {e}")
        failed += 1
        results.append({**test, 'actual': 'CALC_ERROR', 'match': False, 'note': str(e)})
        continue

    # Collect tier data
    dtc_list = [test['dtc']] if test['dtc'] else []
    tier4_low = {
        '0C': 0,
        '06': test['stft'],
        '07': test['ltft'],
        '44': test['obd_lambda'],
        '10': 0,
        '0B': 0,
        '11': 0
    }

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

    # Normalize
    def norm(s):
        return s.replace('_', ' ').lower().strip()
    expected_norm = norm(test['expected'])
    actual_norm = norm(actual_name) if actual_name else norm(actual_id)

    match = (expected_norm == actual_norm)

    if match:
        print(f"[PASS] {test['id']}: expected '{test['expected']}', got '{actual_name}'")
        passed += 1
    else:
        print(f"[FAIL] {test['id']}: expected '{test['expected']}', got '{actual_name}'")
        failed += 1

    results.append({
        **test,
        'actual': actual_name,
        'actual_id': actual_id,
        'confidence': matched.get('confidence_score', 0),
        'match': match
    })

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total: {len(tests)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Accuracy: {passed/len(tests)*100:.1f}%")
print()

# Decision tree interpretation for failures (per manual Section 3)
if failed > 0:
    print("DECISION TREE ANALYSIS (per manual):")
    for r in results:
        if not r['match']:
            cid = r['id']
            if cid == 'TC001' and r['actual'] != 'Healthy Engine':
                print(f"  TC001: Not Healthy → Check Bretschneider formula stability or sensor drift.")
            elif cid == 'TC002' and r['actual'] != 'Catalytic Converter Efficiency Failure':
                print(f"  TC002: Not Catalyst → Check NOx logic (should be >1000) and ordering (catalyst before timing).")
            elif cid == 'TC003' and r['actual'] != 'Intake Vacuum Leak':
                print(f"  TC003: Not Vacuum Leak → Check for Exhaust Leak confusion. Exhaust Leak has O2 > 3.5; Vacuum Leak has O2 2-3.5.")
            elif cid == 'TC004' and r['actual'] != 'Exhaust Dilution (False Lean)':
                print(f"  TC004: Not Dilution → Check measured vs calculated lambda condition.")
            elif cid == 'TC006' and r['actual'] != 'Fuel Delivery Problem (Lean)':
                print(f"  TC006: Not Fuel Lean → Ensure DTC P0171 present and logic excludes Vacuum Leak.")
            elif cid == 'TC007' and r['actual'] != 'Cold Start Enrichment':
                print(f"  TC007: Not Cold Start → Check thresholds: CO>2.5, HC>20000, lambda<0.75.")
            elif cid == 'TC008' and r['actual'] != 'Engine Misfire':
                print(f"  TC008: Not Misfire → Check HC>1500 and O2>1.5 conditions.")
            elif cid == 'TC009' and r['actual'] != 'Excessively Advanced Timing':
                print(f"  TC009: Not Timing Advance → Check NOx>500, CO<0.35, lambda stoich range.")
            elif cid == 'TC010' and r['actual'] != 'System Running Rich':
                print(f"  TC010: Not Rich → Check lambda<0.92 and CO>2.0.")
            elif cid == 'TC011' and r['actual'] != 'O2 Sensor Sluggish or Failed':
                print(f"  TC011: Not O2 Sluggish → Check lambda ~1 and O2 0.4-0.7.")
    print()

# Save results
out = {
    'run_date': datetime.now().isoformat(),
    'total': len(tests),
    'passed': passed,
    'failed': failed,
    'accuracy': passed/len(tests)*100,
    'results': results
}
with open('manual_test_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"Detailed results saved to: manual_test_results.json")

# Exit code
sys.exit(0 if failed == 0 else 1)
