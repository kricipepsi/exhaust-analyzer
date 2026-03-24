#!/usr/bin/env python3
from pathlib import Path
import re

manual_path = Path(r"C:\Users\asus\Documents\1nov\testsuitemanual.md")
content = manual_path.read_text(encoding='utf-8')
lines = content.splitlines()

# Capture any line that starts with a 2-3 digit number and contains numbers with possible % and integers
pattern = re.compile(r'^\s*(\d{2,3})\s+([\d.]+)%?\s+(\d+)\s+([\d.]+)%?\s+([\d.]+)%?\s+([\d.]+)%?\s+(\d+)\s+([\d.]+)%?\s+([\d.]+)%?\s+([\d.]+)%?')
# Actually better: split tokens approach

candidates = []
for line in lines:
    line = line.strip()
    tokens = line.split()
    if len(tokens) >= 9:
        # First token numeric ID
        if re.match(r'^\d{2,3}$', tokens[0]):
            # Try parse numeric tokens 1-8
            try:
                vals = []
                for i in range(1,9):
                    t = tokens[i]
                    if t.endswith('%'):
                        t = t[:-1]
                    vals.append(float(t))
                # Success
                candidates.append({
                    'line': line,
                    'id': tokens[0],
                    'values': vals
                })
            except:
                pass

print(f"Found {len(candidates)} candidate case lines")
# Show IDs
ids = sorted([int(c['id']) for c in candidates])
print("IDs found:", ids[:20], "...", ids[-20:] if len(ids)>40 else ids)
