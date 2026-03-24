#!/usr/bin/env python3
"""Run the 100-case petrol test suite in 5 chunks of 20, reporting per-chunk and overall results."""

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

# Load full test suite
csv_path = Path("petrol_100_test_suite.csv")
if not csv_path.exists():
    print(f"ERROR: Test suite not found: {csv_path}")
    sys.exit(1)

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_cases = list(reader)

total_cases = len(all_cases)
chunk_size = 20
num_chunks = (total_cases + chunk_size - 1) // chunk_size

print("="*70)
print("100-CASE TEST SUITE - 5 CHUNKS EXECUTION")
print("="*70)
print(f"Total cases: {total_cases}, chunk size: {chunk_size}, chunks: {num_chunks}")
print()

chunk_results = []

for chunk_idx in range(num_chunks):
    start = chunk_idx * chunk_size
    end = min(start + chunk_size, total_cases)
    chunk_cases = all_cases[start:end]
    chunk_num = chunk_idx + 1
    print(f"\n--- Chunk {chunk_num} (cases {start+1}-{end}) ---")
    passed = 0
    failed = 0
    details = []

    for test in chunk_cases:
        # Build low_idle
        low_idle = {
            'lambda': float(test['OBD_Lambda']),
            'co': float(test['CO_Pct']),
            'co2': float(test['CO2_Pct']),
            'hc': int(test['HC_PPM']),
            'o2': float(test['O2_Pct']),
            'nox': int(float(test['NOx_PPM']))
        }
        # Validate
        valid, msg = validate_gas_data(low_idle)
        if not valid:
            failed += 1
            details.append({**test, 'actual': 'VALIDATION_FAILED', 'match': False, 'note': msg})
            continue

        # Calculate lambda
        try:
            fuel = test['Fuel'].lower()
            fuel_type = fuel if fuel in ['e0','e5','e10','e85'] else 'e10'
            calc = calculate_lambda(
                co=low_idle['co'], co2=low_idle['co2'], hc_ppm=low_idle['hc'], o2=low_idle['o2'], fuel_type=fuel_type)
            calc_lambda = calc['lambda']
        except Exception as e:
            failed += 1
            details.append({**test, 'actual': 'CALC_ERROR', 'match': False, 'note': str(e)})
            continue

        # Tier data
        dtc_list = [test['OBD_DTC']] if test['OBD_DTC'] != 'None' else []
        tier4_low = {
            '0C': 0,
            '06': float(test['OBD_STFT']),
            '07': float(test['OBD_LTFT']),
            '44': float(test['OBD_Lambda']),
            '10': 0,
            '0B': 0,
            '11': 0
        }

        # Match
        matched = match_case(
            low_idle=low_idle,
            calculated_lambda=calc_lambda,
            measured_lambda=low_idle['lambda'],
            knowledge_base=kb,
            high_idle=None,
            dtc_codes=dtc_list,
            freeze_frame=None,
            tier4_low=tier4_low,
            tier4_high=None
        )
        actual_name = matched.get('name','').strip()
        expected_raw = test['Expected_Result']
        # Normalize comparison: replace underscores, casefold
        def norm(s):
            return s.replace('_',' ').lower().strip()
        match = norm(actual_name) == norm(expected_raw)
        if match:
            passed += 1
            print(f"[PASS] {test['ID']}: expected '{expected_raw}', got '{actual_name}'")
        else:
            failed += 1
            print(f"[FAIL] {test['ID']}: expected '{expected_raw}', got '{actual_name}'")
        details.append({**test, 'actual': actual_name, 'match': match})

    pct = (passed/len(chunk_cases))*100 if chunk_cases else 0
    print(f"Chunk {chunk_num} result: {passed}/{len(chunk_cases)} passed ({pct:.1f}%)")
    chunk_results.append({
        'chunk': chunk_num,
        'passed': passed,
        'failed': failed,
        'total': len(chunk_cases),
        'accuracy': pct,
        'details': details
    })

# Overall summary
overall_passed = sum(r['passed'] for r in chunk_results)
overall_failed = sum(r['failed'] for r in chunk_results)
overall_total = overall_passed + overall_failed
overall_acc = (overall_passed/overall_total)*100 if overall_total>0 else 0

print("\n" + "="*70)
print("OVERALL SUMMARY")
print("="*70)
for r in chunk_results:
    print(f"Chunk {r['chunk']}: {r['passed']}/{r['total']} ({r['accuracy']:.1f}%)")
print(f"TOTAL: {overall_passed}/{overall_total} ({overall_acc:.1f}%)")

# Save detailed results
out = {
    'run_date': datetime.now().isoformat(),
    'chunks': chunk_results,
    'overall': {
        'passed': overall_passed,
        'failed': overall_failed,
        'total': overall_total,
        'accuracy': overall_acc
    }
}
out_path = Path('petrol_100_chunked_results.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)
print(f"\nDetailed results saved to: {out_path}")

# Exit code
sys.exit(0 if overall_failed == 0 else 1)
