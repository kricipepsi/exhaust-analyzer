#!/usr/bin/env python3
"""Validate that all case_ids are present and have valid logic."""

import json
from core.matrix import match_case

kb = json.load(open('data/expanded_knowledge_base.json', 'r'))
cases = kb['diagnostic_matrix']

print(f"Total cases: {len(cases)}\n")
print("Checking logic validity:")

# Try to match each case with a minimal context
failed = []
for case in cases:
    logic = case.get('logic', '')
    if not logic:
        print(f"  {case['case_id']}: NO LOGIC")
        failed.append(case['case_id'])
        continue

    # Create a dummy low_idle that might satisfy if logic is simple
    low_idle = {
        'lambda': 1.0,
        'co': 0.0,
        'co2': 15.0,
        'hc': 0,
        'o2': 0.0,
        'nox': 0
    }

    # Quick attempt to compile/eval
    try:
        from core.matrix import _safe_eval
        _safe_eval(logic, {
            'low_idle': low_idle,
            'calculated_lambda': 1.0,
            'measured_lambda': 1.0,
            'high_idle': {'co': 0.0, 'co2': 15.0, 'hc': 0, 'o2': 0.0, 'lambda': 1.0, 'nox': 0}
        })
        # Mark OK even if False; we just want to ensure no errors
        print(f"  {case['case_id']}: OK")
    except Exception as e:
        print(f"  {case['case_id']}: ERROR - {e}")
        failed.append(case['case_id'])

print(f"\nCases with bad logic: {len(failed)}")
if failed:
    print("Failed:", failed)
else:
    print("All case logics are syntactically valid and evaluatable.")

# Also verify case_ids are unique
ids = [c['case_id'] for c in cases]
duplicates = set([x for x in ids if ids.count(x) > 1])
if duplicates:
    print(f"Duplicate case_ids: {duplicates}")
else:
    print("All case_ids are unique.")

print("\n=== CASE ID LIST (first 20) ===")
print(ids[:20])
print(f"... plus {len(ids)-20} more")
