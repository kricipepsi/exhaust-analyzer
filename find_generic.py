#!/usr/bin/env python3
import json
kb = json.load(open('data/expanded_knowledge_base.json'))
for i, c in enumerate(kb['diagnostic_matrix']):
    logic = c.get('logic', '').lower()
    if 'calculated_lambda' in logic and '&&' not in logic and 'and' not in logic:
        print(f"Row {i}: {c['case_id']} - {c['name']}")
        print(f"  Logic: {c.get('logic')}")
        print()
