#!/usr/bin/env python3
"""Remove the overly broad 'egr_stuck_open' case from the diagnostic matrix."""

import json
from pathlib import Path

kb_path = Path("data/expanded_knowledge_base.json")
backup_path = Path("data/expanded_knowledge_base.json.bak")

# Backup original
import shutil
shutil.copy2(kb_path, backup_path)
print(f"Backed up original to: {backup_path}")

# Load
with open(kb_path, 'r') as f:
    kb = json.load(f)

matrix = kb.get('diagnostic_matrix', [])
original_len = len(matrix)

# Remove only the problematic case with case_id 'egr_stuck_open' (the generic lambda-only one)
new_matrix = [c for c in matrix if c.get('case_id') != 'egr_stuck_open']

removed_count = original_len - len(new_matrix)
print(f"Removed {removed_count} case(s).")

if removed_count == 0:
    print("WARNING: No case with case_id 'egr_stuck_open' found. Check if already removed.")
else:
    kb['diagnostic_matrix'] = new_matrix
    # Write back with pretty formatting (2-space indent)
    with open(kb_path, 'w') as f:
        json.dump(kb, f, indent=2)
    print("Updated knowledge base successfully.")

# Verify
with open(kb_path, 'r') as f:
    kb2 = json.load(f)
print(f"New matrix length: {len(kb2['diagnostic_matrix'])}")
