#!/usr/bin/env python3
import json
kb = json.load(open('data/expanded_knowledge_base.json'))
for i, c in enumerate(kb['diagnostic_matrix'][:20]):
    print(f"{i}: {c['case_id']} - {c['name']}")
    print(f"   {c.get('logic')}")
    print()
