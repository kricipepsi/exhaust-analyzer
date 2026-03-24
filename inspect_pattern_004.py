#!/usr/bin/env python3
import json
kb = json.load(open('data/expanded_knowledge_base.json'))
for c in kb['diagnostic_matrix']:
    if c.get('case_id') == 'pattern_004':
        print(f"ID: {c['case_id']}")
        print(f"Name: {c['name']}")
        print(f"Logic: {c.get('logic')}")
        print(f"Health Score: {c.get('health_score')}")
        print(f"Verdict: {c.get('verdict')}")
        break