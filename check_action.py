#!/usr/bin/env python3
import json
kb = json.load(open('data/expanded_knowledge_base.json'))
for c in kb['diagnostic_matrix']:
    if c.get('case_id') == 'pattern_004':
        print("Action field:")
        print(repr(c.get('action')))
        break