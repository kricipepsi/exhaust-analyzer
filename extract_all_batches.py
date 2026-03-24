#!/usr/bin/env python3
from pathlib import Path
import re

manual_path = Path(r"C:\Users\asus\Documents\1nov\testsuitemanual.md")
content = manual_path.read_text(encoding='utf-8')
lines = content.splitlines()

# Identify batch starts
batch_indices = []
for i, line in enumerate(lines):
    if re.search(r'Batch\s+\d+', line, re.IGNORECASE):
        batch_indices.append(i)
print(f"Batch headers at lines: {batch_indices}")

cases = []
for idx_idx, start_idx in enumerate(batch_indices):
    # end_idx is next batch start or end of lines
    end_idx = batch_indices[idx_idx+1] if idx_idx+1 < len(batch_indices) else len(lines)
    # Process lines in this section
    for line in lines[start_idx+1:end_idx]:
        line = line.strip()
        if not line:
            continue
        # Skip known non-data lines
        if line.startswith(('ID ', 'SKG ', 'The ', 'In ', 'AI ', 'Use ', 'JSON ', 'Key ', 'Next ', 'u great', 'yes and', 'Batch')):
            continue
        tokens = line.split()
        if len(tokens) < 9:
            continue
        # ID token
        cid = tokens[0]
        if not re.match(r'^\d+$', cid):
            continue
        # numeric fields 1-8
        try:
            l_co = float(tokens[1].replace('%',''))
            l_hc = int(tokens[2])
            l_o2 = float(tokens[3].replace('%',''))
            l_co2 = float(tokens[4].replace('%',''))
            h_co = float(tokens[5].replace('%',''))
            h_hc = int(tokens[6])
            h_o2 = float(tokens[7].replace('%',''))
            h_co2 = float(tokens[8].replace('%',''))
        except ValueError:
            continue
        diagnosis = ' '.join(tokens[9:]) if len(tokens) > 9 else ''
        cases.append({
            'ID': cid,
            'Fuel': 'E10',
            'CO_Pct': l_co,
            'HC_PPM': l_hc,
            'O2_Pct': l_o2,
            'CO2_Pct': l_co2,
            'NOx_PPM': 0,
            'Lambda_Gas': 1.0,
            'OBD_STFT': 0,
            'OBD_LTFT': 0,
            'OBD_Lambda': 1.0,
            'OBD_DTC': 'None',
            'Expected_Result': diagnosis,
            'Confidence_Score': 0.8,
            'ECU_Health': 50
        })

print(f"Total cases extracted: {len(cases)}")
# Check ID range
ids = sorted([int(c['ID']) for c in cases])
if ids:
    print(f"ID range: {ids[0]} - {ids[-1]}")

# Deduplicate by ID (in case overlapping)
unique = {c['ID']: c for c in cases}
cases_unique = list(unique.values())
print(f"Unique cases: {len(cases_unique)}")

# Write CSV
import csv
fieldnames = ['ID','Fuel','CO_Pct','CO2_Pct','HC_PPM','O2_Pct','NOx_PPM','Lambda_Gas','OBD_STFT','OBD_LTFT','OBD_Lambda','OBD_DTC','Expected_Result','Confidence_Score','ECU_Health']
csv_path = Path('extracted_manual_cases.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases_unique)
print(f"Wrote {csv_path} with {len(cases_unique)} cases")
