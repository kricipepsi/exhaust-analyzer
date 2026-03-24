#!/usr/bin/env python3
from pathlib import Path
import re

manual_path = Path(r"C:\Users\asus\Documents\1nov\testsuitemanual.md")
content = manual_path.read_text(encoding='utf-8')
lines = content.splitlines()

cases = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    # Skip obvious non-data lines
    if line.startswith(('ID ', 'SKG ', 'The ', 'In ', 'AI ', 'Use ', 'JSON ', 'Key ', 'Next ', 'u great', 'yes and', 'Batch', 'This ', 'To ', 'In a ', 'Case', 'Map', 'AI responses', 'Would you', 'There ', 'Next Steps', 'Key Recommendation', 'Use code', 'Would you like', 'To show you', 'The Input', 'Step', 'The SKG', 'Logic:', 'JSON Schema', 'Final Graph', 'Use code', 'AI responses')):
        continue
    tokens = line.split()
    if len(tokens) < 9:
        continue
    # ID = first token
    cid = tokens[0]
    if not re.match(r'^\d+$', cid):
        continue
    # Parse numeric fields: L_CO% L_HC L_O2% L_CO2% H_CO% H_HC H_O2% H_CO2%
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

print(f"Extracted {len(cases)} case rows")
# Deduplicate
unique = {c['ID']: c for c in cases}
cases_unique = list(unique.values())
print(f"Unique cases: {len(cases_unique)}")
ids = sorted([int(c['ID']) for c in cases_unique])
if ids:
    print(f"IDs: {ids[0]} - {ids[-1]}")

import csv
fieldnames = ['ID','Fuel','CO_Pct','CO2_Pct','HC_PPM','O2_Pct','NOx_PPM','Lambda_Gas','OBD_STFT','OBD_LTFT','OBD_Lambda','OBD_DTC','Expected_Result','Confidence_Score','ECU_Health']
csv_path = Path('extracted_manual_cases.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases_unique)
print(f"Wrote {csv_path} with {len(cases_unique)} cases")
