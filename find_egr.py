#!/usr/bin/env python3
import json
from pathlib import Path

kb_path = Path("data/expanded_knowledge_base.json")
with open(kb_path, 'r') as f:
    kb = json.load(f)

matrix = kb.get('diagnostic_matrix', [])
for idx, case in enumerate(matrix):
    cid = case.get('case_id', '')
    name = case.get('name', '')
    if 'egr_stuck_open' in cid.lower() and 'idle' not in cid.lower():
        print(f"Row {idx}: {cid} - {name}")
        print(f"  Logic: {case.get('logic')}")
        print()
