#!/usr/bin/env python3
from pathlib import Path
import re

manual_path = Path(r"C:\Users\asus\Documents\1nov\testsuitemanual.md")
content = manual_path.read_text(encoding='utf-8')
lines = content.splitlines()

def is_numeric_token(t):
    t = t.strip().rstrip('%')
    try:
        float(t)
        return True
    except:
        return False

candidates = []
for line in lines:
    stripped = line.strip()
    if not stripped:
        continue
    tokens = stripped.split()
    if len(tokens) < 9:
        continue
    # ID must be first token and all digits
    if not tokens[0].isdigit():
        continue
    # Check tokens 1-8 are numeric
    if all(is_numeric_token(t) for t in tokens[1:9]):
        # Ensure the 9th token (index 8) is numeric too? We need 8 numeric after ID, indices 1-8 inclusive
        candidates.append({
            'id': tokens[0],
            'line': stripped
        })

print(f"Found {len(candidates)} candidate rows")
# Deduplicate by ID
unique_ids = {}
for c in candidates:
    uid = int(c['id'])
    if uid not in unique_ids:
        unique_ids[uid] = c
unique_cases = sorted(unique_ids.values(), key=lambda x: int(x['id']))
print(f"Unique IDs: {len(unique_cases)}")
if unique_cases:
    print("First few IDs:", [c['id'] for c in unique_cases][:10])
    print("Last few IDs:", [c['id'] for c in unique_cases][-10:])

# Write IDs to file for inspection
with open('candidate_case_lines.txt','w') as f:
    for c in unique_cases:
        f.write(c['line']+"\n")
print("Wrote candidate_case_lines.txt")
