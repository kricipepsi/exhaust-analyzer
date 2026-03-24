#!/usr/bin/env python3
import json
kb = json.load(open('data/expanded_knowledge_base.json'))
print("Current case_id and name values:")
for i, c in enumerate(kb['diagnostic_matrix']):
    print(f"{i:3d}: {c['case_id']:30s} - {c['name']}")
