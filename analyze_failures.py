#!/usr/bin/env python3
import csv
from pathlib import Path

csv_path = Path('petrol_100_test_suite.csv')
with open(csv_path, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

failed_ids = {
    'TC030': 'Exhaust Leak',
    'TC034': 'Intake Vacuum Leak',
    'TC035': 'Intake Vacuum Leak',
    'TC036': 'Intake Vacuum Leak',
    'TC037': 'Intake Vacuum Leak',
    'TC038': 'Intake Vacuum Leak',
    'TC039': 'Intake Vacuum Leak',
    'TC040': 'Intake Vacuum Leak',
    'TC041': 'Intake Vacuum Leak',
    'TC042': 'Intake Vacuum Leak',
    'TC043': 'Intake Vacuum Leak',
    'TC044': 'Intake Vacuum Leak',
    'TC045': 'Intake Vacuum Leak',
    'TC046': 'Fuel Delivery Problem (Lean)',
    'TC047': 'Fuel Delivery Problem (Lean)',
    'TC048': 'Fuel Delivery Problem (Lean)',
    'TC049': 'Fuel Delivery Problem (Lean)',
    'TC050': 'Fuel Delivery Problem (Lean)',
    'TC051': 'Fuel Delivery Problem (Lean)',
    'TC052': 'Fuel Delivery Problem (Lean)',
    'TC053': 'Fuel Delivery Problem (Lean)',
    'TC054': 'Fuel Delivery Problem (Lean)',
    'TC055': 'Fuel Delivery Problem (Lean)',
    'TC064': 'Cold Start Enrichment',
    'TC065': 'Cold Start Enrichment',
    'TC066': 'Cold Start Enrichment',
    'TC067': 'Cold Start Enrichment',
    'TC068': 'Cold Start Enrichment',
    'TC069': 'Cold Start Enrichment',
    'TC070': 'Cold Start Enrichment',
    'TC071': 'Cold Start Enrichment',
    'TC073': 'Engine Misfire',
    'TC080': 'Excessively Advanced Timing',
    'TC081': 'Excessively Advanced Timing',
    'TC082': 'Excessively Advanced Timing',
    'TC096': 'MAF Sensor Under-Reading',
    'TC097': 'MAF Sensor Under-Reading',
    'TC098': 'MAF Sensor Under-Reading',
    'TC099': 'MAF Sensor Under-Reading',
    'TC100': 'MAF Sensor Under-Reading'
}

print("=== Detailed Failure Analysis ===\n")
for r in rows:
    if r['ID'] in failed_ids:
        print(f"{r['ID']}: {failed_ids[r['ID']]}")
        print(f"  Fuel={r['Fuel']}, CO={r['CO_Pct']}, CO2={r['CO2_Pct']}, HC={r['HC_PPM']}, O2={r['O2_Pct']}, NOx={r['NOx_PPM']}, Lambda={r['Lambda_Gas']}")
        print()
