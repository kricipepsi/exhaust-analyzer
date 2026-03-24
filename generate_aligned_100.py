#!/usr/bin/env python3
"""Generate a 100-case test suite perfectly aligned with the knowledge base matrix."""

import csv
import random
from pathlib import Path

random.seed(12345)  # reproducible

# Define generators for each case based on exact logic constraints
def gen_catalyst():
    # nox > 1000, lambda 0.98-1.02, co2 > 13.0, hc < 1000
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.8, 2.0), 2),
        'CO2_Pct': round(random.uniform(13.2, 14.5), 1),
        'HC_PPM': random.randint(100, 600),
        'O2_Pct': round(random.uniform(0.3, 0.7), 2),
        'NOx_PPM': random.randint(1001, 2000),
        'Lambda_Gas': round(random.uniform(0.98, 1.02), 3),
        'OBD_STFT': random.randint(-5, 5),
        'OBD_LTFT': random.randint(-5, 5),
        'OBD_Lambda': round(random.uniform(0.98, 1.02), 3),
        'OBD_DTC': random.choice(['P0420','P0430']),
        'Expected_Result': 'Catalytic Converter Efficiency Failure',
        'Confidence_Score': 0.9,
        'ECU_Health': 40
    }

def gen_timing_advance():
    # nox > 500, co < 0.35, hc < 60, lambda 0.99-1.03
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.05, 0.30), 2),
        'CO2_Pct': round(random.uniform(13.5, 15.0), 1),
        'HC_PPM': random.randint(15, 50),
        'O2_Pct': round(random.uniform(0.1, 0.3), 2),
        'NOx_PPM': random.randint(501, 1500),
        'Lambda_Gas': round(random.uniform(0.99, 1.03), 3),
        'OBD_STFT': random.randint(-3, 3),
        'OBD_LTFT': random.randint(-3, 3),
        'OBD_Lambda': round(random.uniform(0.99, 1.03), 3),
        'OBD_DTC': 'P0016',
        'Expected_Result': 'Excessively Advanced Timing',
        'Confidence_Score': 0.75,
        'ECU_Health': 50
    }

def gen_exhaust_leak():
    # o2 > 3.5, lambda > 1.02, co < 0.4, hc < 100, nox < 150
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.1, 0.35), 2),
        'CO2_Pct': round(random.uniform(12.0, 13.0), 1),
        'HC_PPM': random.randint(20, 90),
        'O2_Pct': round(random.uniform(3.6, 5.5), 2),
        'NOx_PPM': random.randint(50, 140),
        'Lambda_Gas': round(random.uniform(1.03, 1.15), 3),
        'OBD_STFT': random.randint(10, 18),
        'OBD_LTFT': random.randint(6, 14),
        'OBD_Lambda': round(random.uniform(1.03, 1.15), 3),
        'OBD_DTC': 'None',
        'Expected_Result': 'Exhaust Leak (False Lean)',
        'Confidence_Score': 0.75,
        'ECU_Health': 55
    }

def gen_misfire():
    # hc > 1500, o2 > 1.5, co < 1.0, co2 > 5.0
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.2, 0.9), 2),
        'CO2_Pct': round(random.uniform(6.0, 10.0), 1),
        'HC_PPM': random.randint(1600, 5000),
        'O2_Pct': round(random.uniform(1.6, 4.0), 2),
        'NOx_PPM': random.randint(20, 150),
        'Lambda_Gas': round(random.uniform(1.00, 1.08), 3),
        'OBD_STFT': random.randint(5, 15),
        'OBD_LTFT': random.randint(3, 10),
        'OBD_Lambda': round(random.uniform(1.00, 1.08), 3),
        'OBD_DTC': random.choice(['P0300','P0301','P0302','P0303']),
        'Expected_Result': 'Engine Misfire',
        'Confidence_Score': 0.9,
        'ECU_Health': 30
    }

def gen_cold_start():
    # co > 2.5, hc > 5000, co2 < 13.0, lambda < 0.75
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(2.6, 4.5), 2),
        'CO2_Pct': round(random.uniform(11.0, 12.5), 1),
        'HC_PPM': random.randint(6000, 20000),
        'O2_Pct': round(random.uniform(0.1, 0.3), 2),
        'NOx_PPM': random.randint(10, 40),
        'Lambda_Gas': round(random.uniform(0.65, 0.74), 3),
        'OBD_STFT': random.randint(-15, -8),
        'OBD_LTFT': random.randint(-10, -5),
        'OBD_Lambda': round(random.uniform(0.65, 0.74), 3),
        'OBD_DTC': 'None',
        'Expected_Result': 'Cold Start Enrichment',
        'Confidence_Score': 0.8,
        'ECU_Health': 40
    }

def gen_fuel_lean():
    # lambda > 1.07, o2 > 1.5, stft > 10, ltft > 8, nox > 150, DTC in {P0171,P0174}
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.1, 0.3), 2),
        'CO2_Pct': round(random.uniform(12.0, 13.0), 1),
        'HC_PPM': random.randint(80, 200),
        'O2_Pct': round(random.uniform(1.6, 3.0), 2),
        'NOx_PPM': random.randint(151, 300),
        'Lambda_Gas': round(random.uniform(1.08, 1.20), 3),
        'OBD_STFT': random.randint(12, 20),
        'OBD_LTFT': random.randint(9, 16),
        'OBD_Lambda': round(random.uniform(1.08, 1.20), 3),
        'OBD_DTC': random.choice(['P0171','P0174']),
        'Expected_Result': 'Fuel Delivery Problem (Lean)',
        'Confidence_Score': 0.8,
        'ECU_Health': 55
    }

def gen_vacuum_leak():
    # lambda > 1.05, o2 > 2.0 and <=3.5, co < 0.5, co2 < 13.0, nox < 200, and DTC not P0171/P0174
    # Ensure DTC is None or other
    dtc = random.choice(['None','P0420','P0300','P0016'])
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.1, 0.4), 2),
        'CO2_Pct': round(random.uniform(12.0, 12.8), 1),
        'HC_PPM': random.randint(50, 180),
        'O2_Pct': round(random.uniform(2.1, 3.4), 2),
        'NOx_PPM': random.randint(50, 190),
        'Lambda_Gas': round(random.uniform(1.06, 1.12), 3),
        'OBD_STFT': random.randint(12, 22),
        'OBD_LTFT': random.randint(8, 16),
        'OBD_Lambda': round(random.uniform(1.06, 1.12), 3),
        'OBD_DTC': dtc,
        'Expected_Result': 'Intake Vacuum Leak',
        'Confidence_Score': 0.75,
        'ECU_Health': 60
    }

def gen_rich_running():
    # lambda < 0.92, co > 2.0, o2 < 0.2, hc < 2000
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(2.1, 3.5), 2),
        'CO2_Pct': round(random.uniform(11.5, 12.8), 1),
        'HC_PPM': random.randint(100, 1800),
        'O2_Pct': round(random.uniform(0.02, 0.15), 2),
        'NOx_PPM': random.randint(10, 80),
        'Lambda_Gas': round(random.uniform(0.88, 0.91), 3),
        'OBD_STFT': random.randint(-15, -8),
        'OBD_LTFT': random.randint(-12, -6),
        'OBD_Lambda': round(random.uniform(0.88, 0.91), 3),
        'OBD_DTC': 'P0172',
        'Expected_Result': 'System Running Rich',
        'Confidence_Score': 0.75,
        'ECU_Health': 45
    }

def gen_o2_lazy():
    # lambda 0.96-1.04, o2 0.4-0.7, co > 0.3, nox < 200
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.35, 0.8), 2),
        'CO2_Pct': round(random.uniform(13.0, 14.0), 1),
        'HC_PPM': random.randint(50, 150),
        'O2_Pct': round(random.uniform(0.45, 0.65), 2),
        'NOx_PPM': random.randint(40, 180),
        'Lambda_Gas': round(random.uniform(0.97, 1.03), 3),
        'OBD_STFT': random.randint(-3, 3),
        'OBD_LTFT': random.randint(-3, 3),
        'OBD_Lambda': round(random.uniform(0.97, 1.03), 3),
        'OBD_DTC': random.choice(['P0131','P0132','P0133','P0134']),
        'Expected_Result': 'O2 Sensor Sluggish or Failed',
        'Confidence_Score': 0.7,
        'ECU_Health': 60
    }

def gen_timing_retard():
    # nox < 30, co > 0.8, lambda 0.98-1.03
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.8, 1.6), 2),
        'CO2_Pct': round(random.uniform(12.0, 13.0), 1),
        'HC_PPM': random.randint(50, 150),
        'O2_Pct': round(random.uniform(0.2, 0.5), 2),
        'NOx_PPM': random.randint(10, 28),
        'Lambda_Gas': round(random.uniform(0.98, 1.02), 3),
        'OBD_STFT': random.randint(-3, 3),
        'OBD_LTFT': random.randint(-3, 3),
        'OBD_Lambda': round(random.uniform(0.98, 1.02), 3),
        'OBD_DTC': random.choice(['P0016','P0017']),
        'Expected_Result': 'Ignition Timing Issues (Retard)',
        'Confidence_Score': 0.65,
        'ECU_Health': 50
    }

def gen_maf_under():
    # lambda > 1.06, stft > 10, ltft > 8, nox > 80, and DTC not P0171/P0174
    dtc = random.choice(['P0101','P0102','None'])
    return {
        'Fuel': 'E10',
        'CO_Pct': round(random.uniform(0.1, 0.3), 2),
        'CO2_Pct': round(random.uniform(13.0, 14.0), 1),
        'HC_PPM': random.randint(40, 120),
        'O2_Pct': round(random.uniform(1.5, 3.0), 2),
        'NOx_PPM': random.randint(81, 250),
        'Lambda_Gas': round(random.uniform(1.07, 1.15), 3),
        'OBD_STFT': random.randint(12, 20),
        'OBD_LTFT': random.randint(9, 16),
        'OBD_Lambda': round(random.uniform(1.07, 1.15), 3),
        'OBD_DTC': dtc,
        'Expected_Result': 'MAF Sensor Under-Reading',
        'Confidence_Score': 0.7,
        'ECU_Health': 50
    }

def gen_healthy(fuel=None):
    fuel = fuel or random.choice(['E0','E5','E10','E85'])
    # lambda 0.99-1.01, co < 0.3, co2 >= 14.0 for E0/E5/E10; for E85, co2 slightly lower? We'll keep same for simplicity.
    co2_min = 14.0 if fuel in ['E0','E5','E10'] else 13.5
    return {
        'Fuel': fuel,
        'CO_Pct': round(random.uniform(0.05, 0.25), 2),
        'CO2_Pct': round(random.uniform(co2_min, 15.5), 1),
        'HC_PPM': random.randint(10, 55),
        'O2_Pct': round(random.uniform(0.1, 0.4), 2),
        'NOx_PPM': random.randint(15, 80),
        'Lambda_Gas': round(random.uniform(0.99, 1.01), 3),
        'OBD_STFT': random.randint(-5, 5),
        'OBD_LTFT': random.randint(-5, 5),
        'OBD_Lambda': round(random.uniform(0.99, 1.01), 3),
        'OBD_DTC': 'None',
        'Expected_Result': 'Healthy Engine',
        'Confidence_Score': 0.95,
        'ECU_Health': 100
    }

# Category weights to total 100
weights = {
    'Healthy Engine': 15,
    'Catalytic Converter Efficiency Failure': 10,
    'Exhaust Leak (False Lean)': 8,
    'Intake Vacuum Leak': 12,
    'Fuel Delivery Problem (Lean)': 10,
    'System Running Rich': 8,
    'Cold Start Enrichment': 8,
    'Engine Misfire': 8,
    'Excessively Advanced Timing': 6,
    'Ignition Timing Issues (Retard)': 5,
    'O2 Sensor Sluggish or Failed': 5,
    'MAF Sensor Under-Reading': 5
}
assert sum(weights.values()) == 100

generators = {
    'Healthy Engine': gen_healthy,
    'Catalytic Converter Efficiency Failure': gen_catalyst,
    'Exhaust Leak (False Lean)': gen_exhaust_leak,
    'Intake Vacuum Leak': gen_vacuum_leak,
    'Fuel Delivery Problem (Lean)': gen_fuel_lean,
    'System Running Rich': gen_rich_running,
    'Cold Start Enrichment': gen_cold_start,
    'Engine Misfire': gen_misfire,
    'Excessively Advanced Timing': gen_timing_advance,
    'Ignition Timing Issues (Retard)': gen_timing_retard,
    'O2 Sensor Sluggish or Failed': gen_o2_lazy,
    'MAF Sensor Under-Reading': gen_maf_under
}

# Generate cases
cases = []
case_id = 1
for category, count in weights.items():
    gen = generators[category]
    for _ in range(count):
        case = gen()
        case['ID'] = f'TC{case_id:03d}'
        cases.append(case)
        case_id += 1

# Shuffle to mix order (but keep IDs sequential? We'll reorder IDs after shuffle to be sequential)
random.shuffle(cases)
# Reassign IDs to be sequential after shuffle
for i, case in enumerate(cases, 1):
    case['ID'] = f'TC{i:03d}'

# Write CSV
fieldnames = ['ID','Fuel','CO_Pct','CO2_Pct','HC_PPM','O2_Pct','NOx_PPM','Lambda_Gas','OBD_STFT','OBD_LTFT','OBD_Lambda','OBD_DTC','Expected_Result','Confidence_Score','ECU_Health']
csv_path = Path('petrol_100_test_suite.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases)

print(f"Generated {len(cases)} cases with aligned ranges to {csv_path}")

# Print category distribution
dist = {}
for c in cases:
    exp = c['Expected_Result']
    dist[exp] = dist.get(exp, 0) + 1
print("Distribution:")
for cat, cnt in sorted(dist.items()):
    print(f"  {cat}: {cnt}")
