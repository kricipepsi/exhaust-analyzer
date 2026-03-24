#!/usr/bin/env python3
import csv, io
from pathlib import Path
with open(path) as f:
    rows = list(csv.DictReader(f))

# Find all Excessively Advanced Timing tests
print("=== Excessively Advanced Timing cases ===")
for r in rows:
    if r['Expected_Result'] == 'Excessively Advanced Timing':
        print(f"ID {r['ID']}: CO={r['CO_Pct']}, CO2={r['CO2_Pct']}, HC={r['HC_PPM']}, O2={r['O2_Pct']}, NOx={r['NOx_PPM']}, Lambda={r['Lambda_Gas']}")

print("\n=== Cold Start Enrichment cases ===")
for r in rows:
    if r['Expected_Result'] == 'Cold Start Enrichment':
        print(f"ID {r['ID']}: CO={r['CO_Pct']}, CO2={r['CO2_Pct']}, HC={r['HC_PPM']}, O2={r['O2_Pct']}, NOx={r['NOx_PPM']}, Lambda={r['Lambda_Gas']}")

print("\n=== lean_exhaust cases ===")
for r in rows:
    if r['Expected_Result'] == 'lean_exhaust':
        print(f"ID {r['ID']}: CO={r['CO_Pct']}, CO2={r['CO2_Pct']}, HC={r['HC_PPM']}, O2={r['O2_Pct']}, NOx={r['NOx_PPM']}, Lambda={r['Lambda_Gas']}")

print("\n=== System Running Rich cases ===")
for r in rows:
    if r['Expected_Result'] == 'System Running Rich':
        print(f"ID {r['ID']}: CO={r['CO_Pct']}, CO2={r['CO2_Pct']}, HC={r['HC_PPM']}, O2={r['O2_Pct']}, NOx={r['NOx_PPM']}, Lambda={r['Lambda_Gas']}")

print("\n=== Catalytic Converter Efficiency Failure cases ===")
for r in rows:
    if r['Expected_Result'] == 'Catalytic Converter Efficiency Failure':
        print(f"ID {r['ID']}: CO={r['CO_Pct']}, CO2={r['CO2_Pct']}, HC={r['HC_PPM']}, O2={r['O2_Pct']}, NOx={r['NOx_PPM']}, Lambda={r['Lambda_Gas']}")
