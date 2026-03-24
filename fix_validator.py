#!/usr/bin/env python3
import json
from pathlib import Path

kb_path = Path('data/master_knowledge_base.json')
with open(kb_path, 'r') as f:
    kb = json.load(f)

# Update validation ranges
ranges = kb.get('validation_gatekeeper', {}).get('ranges', {})
if 'hc' in ranges:
    ranges['hc']['max'] = 10000
    print("Updated HC max to 10000")
else:
    print("Warning: hc range not found")

# Save
with open(kb_path, 'w') as f:
    json.dump(kb, f, indent=2)
print(f"Saved {kb_path}")
