#!/usr/bin/env python3
import csv
from pathlib import Path

csv_path = Path('petrol_100_test_suite.csv')
with open(csv_path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

def show(category):
    print(f"\n=== {category} cases ===")
    for r in rows:
        if r['Expected_Result'] == category:
            print(f"ID {r['ID']}: CO={r['CO_Pct']}, CO2={r['CO2_Pct']}, HC={r['HC_PPM']}, O2={r['O2_Pct']}, NOx={r['NOx_PPM']}, Lambda={r['Lambda_Gas']}")

show('Excessively Advanced Timing')
show('Cold Start Enrichment')
show('lean_exhaust')
show('System Running Rich')
show('Catalytic Converter Efficiency Failure')
