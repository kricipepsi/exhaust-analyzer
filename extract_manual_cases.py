#!/usr/bin/env python3
"""Extract test cases from testsuitemanual.md and create CSV."""

from pathlib import Path
import re

manual_path = Path(r"C:\Users\asus\Documents\1nov\testsuitemanual.md")
content = manual_path.read_text(encoding='utf-8')

# Find all batch sections
batch_sections = re.findall(r'(Batch \d+:.*?)(?=Batch \d+|$)', content, re.DOTALL)
print(f"Found {len(batch_sections)} batch sections")

cases = []

for batch_text in batch_sections:
    # Extract lines that look like case rows: start with digits (ID) then numbers
    lines = batch_text.splitlines()
    for line in lines:
        line = line.strip()
        # Skip headers and empty
        if not line or line.startswith('ID ') or line.startswith('Batch ') or line.startswith('SKG ') or line.startswith('The ') or line.startswith('In ') or line.startswith('AI ') or line.startswith('Use ') or line.startswith('JSON ') or line.startswith('Key ') or line.startswith('Next ') or line.startswith('u great') or line.startswith('yes and'):
            continue
        # Tokenize: split on whitespace
        tokens = line.split()
        if len(tokens) < 9:
            continue
        # First token is ID
        cid = tokens[0]
        # Ensure ID looks like digits
        if not re.match(r'^\d+$', cid):
            continue
        # Next 8 tokens are numeric measurements: L_CO, L_HC, L_O2, L_CO2, H_CO, H_HC, H_O2, H_CO2
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
        # The rest is the expected diagnosis (may include spaces)
        diagnosis = ' '.join(tokens[9:]) if len(tokens) > 9 else ''
        # For our test format, we need a single set of low_idle values (use L_ values) and OBD fields; we'll map:
        # Fuel: assume E10 for all (could infer from context but not given)
        # CO_Pct: L_CO
        # HC_PPM: L_HC
        # O2_Pct: L_O2
        # CO2_Pct: L_CO2
        # NOx_PPM: not given; set to 0
        # Lambda_Gas: not given; calculate from gases? But manual expects us to input; set to 1.0 as placeholder
        # OBD_STFT, OBD_LTFT: 0
        # OBD_Lambda: 1.0
        # DTC: None
        # Expected_Result: diagnosis string
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

print(f"Extracted {len(cases)} cases from manual")

# Write CSV
import csv
csv_path = Path('extracted_manual_cases.csv')
fieldnames = ['ID','Fuel','CO_Pct','CO2_Pct','HC_PPM','O2_Pct','NOx_PPM','Lambda_Gas','OBD_STFT','OBD_LTFT','OBD_Lambda','OBD_DTC','Expected_Result','Confidence_Score','ECU_Health']
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases)
print(f"Wrote {csv_path}")
