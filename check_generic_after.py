#!/usr/bin/env python3
import json
kb = json.load(open('data/expanded_knowledge_base.json'))
for i, c in enumerate(kb['diagnostic_matrix']):
    logic = c.get('logic', '').lower()
    # Check if only condition is a lambda/calculated_lambda check without other variables
    if ('calculated_lambda' in logic or 'low_idle.lambda' in logic or 'measured_lambda' in logic):
        # If the logic contains only one variable and no other variable names (like co, hc, nox, etc.)
        # Count variable names: lambda, calculated_lambda, measured_lambda are considered one
        # Exclude known other variable names
        others = [v for v in ['co', 'hc', 'o2', 'nox', 'co2', 'high_idle'] if v in logic]
        if not others:
            print(f"Row {i}: {c['case_id']} - {c['name']}")
            print(f"  Logic: {c.get('logic')}")
            print()
