#!/usr/bin/env python3
"""Analyze diagnostic matrix to design safe reordering."""

import json
from pathlib import Path

kb_path = Path("data/expanded_knowledge_base.json")
with open(kb_path, 'r') as f:
    kb = json.load(f)

matrix = kb.get('diagnostic_matrix', [])

# Categorize cases
catalyst_cases = []
egr_cases = []
high_nox_cases = []
generic_lambda_cases = []
other_cases = []

for idx, case in enumerate(matrix):
    cid = case.get('case_id', '')
    name = case.get('name', '').lower()
    logic = case.get('logic', '').lower()

    # Tag categories
    tags = []
    if 'catalyst' in name or 'cat' in cid:
        tags.append('catalyst')
    if 'egr' in name:
        tags.append('egr')
    if 'nox' in logic:
        tags.append('high_nox')
    if 'calculated_lambda' in logic and len(logic) < 60 and '&&' not in logic:
        # Very simple lambda check only, likely generic
        tags.append('generic_lambda')

    # Print problematic ones
    if 'egr_stuck_open' in cid and 'idle' not in cid:
        print(f"Row {idx}: {cid} - {name}")
        print(f"  Logic: {case.get('logic')}")
        print(f"  --> TOO BROAD: Only checks lambda 0.98-1.02, will match most normal engines")
        print()

    if 'catalyst_failure' in cid:
        catalyst_cases.append((idx, cid, name, case.get('logic')))

print("=== Catalyst-related cases ===")
for idx, cid, name, logic in catalyst_cases:
    print(f"Row {idx}: {cid} - {name}")
    print(f"  Logic: {logic}")
    print()

print("=== Cases with high_nox only ===")
for idx, case in enumerate(matrix):
    logic = case.get('logic', '')
    if 'low_idle.nox > ' in logic and 'catalyst' not in case.get('name','').lower():
        print(f"Row {idx}: {case['case_id']} - {case['name']}")
        print(f"  Logic: {logic}")
        print()

print("=== Summary ===")
print(f"Total cases: {len(matrix)}")
print(f"Catalyst cases: {len(catalyst_cases)}")
print(f"EGR cases: {len([c for c in matrix if 'egr' in c.get('name','').lower()])}")
print(f"Generic lambda-only cases: {len([c for c in matrix if 'calculated_lambda' in c.get('logic','') and '&&' not in c.get('logic','')])}")
