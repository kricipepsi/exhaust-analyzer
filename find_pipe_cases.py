#!/usr/bin/env python3
from pathlib import Path
import re

manual_path = Path(r"C:\Users\asus\Documents\1nov\testsuitemanual.md")
content = manual_path.read_text(encoding='utf-8')
lines = content.splitlines()

# Look for lines with pipes and many numeric tokens
pipe_lines = []
for line in lines:
    if '|' in line:
        # remove leading/traiting pipes and split
        parts = [p.strip() for p in line.strip('|').split('|')]
        # Count numeric cells
        numeric_count = 0
        for p in parts:
            if re.match(r'^[\d.]+%?$', p):
                numeric_count += 1
        if numeric_count >= 8:
            pipe_lines.append(line)

print(f"Found {len(pipe_lines)} pipe-delimited rows with many numbers")
if pipe_lines:
    print("Sample:")
    for pl in pipe_lines[:5]:
        print(pl)
