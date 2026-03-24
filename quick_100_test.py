#!/usr/bin/env python3
import sys
from pathlib import Path
import csv
import json
import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.matrix import match_case
from core.bretschneider import calculate_lambda
from core.validator import validate_gas_data

# Load KB
with open("data/expanded_knowledge_base.json", 'r') as f:
    kb = json.load(f)

# Load test suite
with open("petrol_100_test_suite.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    tests = list(reader)

passed = 0
failed = 0
failures = []

for test in tests:
    try:
        low_idle = {
            'lambda': float(test['OBD_Lambda']),
            'co': float(test['CO_Pct']),
            'co2': float(test['CO2_Pct']),
            'hc': int(test['HC_PPM']),
            'o2': float(test['O2_Pct']),
            'nox': int(float(test['NOx_PPM']))
        }
        # Validate
        valid, vmsg = validate_gas_data(low_idle)
        if not valid:
            failed += 1
            failures.append((test['ID'], 'validation', test['Expected_Result'], vmsg))
            continue

        # Calc lambda
        try:
            fuel = test['Fuel'].lower()
            fuel_type = fuel if fuel in ['e0','e5','e10','e85'] else 'e10'
            calc = calculate_lambda(co=low_idle['co'], co2=low_idle['co2'], hc_ppm=low_idle['hc'], o2=low_idle['o2'], fuel_type=fuel_type)
            calc_lambda = calc['lambda']
        except Exception as e:
            failed += 1
            failures.append((test['ID'], 'calc', test['Expected_Result'], str(e)))
            continue

        dtc_list = [test['OBD_DTC']] if test['OBD_DTC'] != 'None' else []
        tier4_low = {'0C':0, '06': float(test['OBD_STFT']), '07': float(test['OBD_LTFT']), '44': float(test['OBD_Lambda']), '10':0, '0B':0, '11':0}

        matched = match_case(low_idle, calc_lambda, low_idle['lambda'], kb, None, dtc_list, None, tier4_low, None)
        actual = matched.get('name','').strip()
        expected = test['Expected_Result']
        if actual.replace('_',' ').lower() == expected.replace('_',' ').lower():
            passed += 1
        else:
            failed += 1
            failures.append((test['ID'], expected, actual, ''))
    except Exception as e:
        failed += 1
        failures.append((test['ID'], 'error', test.get('Expected_Result',''), str(e)))

print(f"Total: {len(tests)}; Passed: {passed}; Failed: {failed}; Accuracy: {passed/len(tests)*100:.1f}%")
if failures:
    print("Failures (first 10):")
    for fid, exp, act in failures[:10]:
        print(f"  {fid}: expected '{exp}', got '{act}'")
# Save detailed results
out = {
    'timestamp': datetime.datetime.now().isoformat(),
    'total': len(tests),
    'passed': passed,
    'failed': failed,
    'accuracy': passed/len(tests)*100,
    'failures': failures
}
with open('quick_100_results.json','w') as f:
    json.dump(out, f, indent=2)
print(f"\nResults saved to quick_100_results.json")
