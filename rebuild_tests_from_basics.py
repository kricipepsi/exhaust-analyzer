#!/usr/bin/env python3
"""Rebuild diagnostic matrix from fundamentals (basics.md) and regenerate matching test suite."""

import json
from pathlib import Path
import csv
import random

random.seed(42)

# Step 1: Build clean knowledge base with distinct, non-overlapping patterns
fresh_cases = [
    # 1. Healthy Engine (Stoich, good burn)
    {
        "case_id": "P_100",
        "name": "Healthy Engine",
        "logic": "0.99 <= low_idle.lambda <= 1.01 && low_idle.co < 0.3 && low_idle.co2 >= 14.0 && low_idle.hc < 60 && low_idle.o2 < 0.5",
        "health_score": 100,
        "verdict": "Excellent combustion and conversion.",
        "action": "No repairs needed.",
        "confidence_boosters": {"base_confidence": 0.95}
    },
    # 2. Catalytic Converter Failure (high NOx with stoich mix, decent CO2, moderate HC)
    {
        "case_id": "catalyst_failure",
        "name": "Catalytic Converter Efficiency Failure",
        "logic": "low_idle.nox > 1000 && 0.98 <= low_idle.lambda <= 1.02 && low_idle.co2 > 13.0 && low_idle.hc < 1000",
        "health_score": 40,
        "verdict": "Catalyst not reducing NOx; efficiency below threshold.",
        "action": "Replace catalytic converter; check for contamination sources.",
        "confidence_boosters": {"base_confidence": 0.9},
        "modular_addons": {"tier2_obd_dtc": ["P0420","P0430"]}
    },
    # 3. Exhaust Leak (pre-O2) – false lean, high O2, but NOx normal/low
    {
        "case_id": "exhaust_leak_false_lean",
        "name": "Exhaust Leak (False Lean)",
        "logic": "low_idle.o2 > 3.0 && low_idle.lambda > 1.02 && low_idle.co < 0.5 && low_idle.nox < 200",
        "health_score": 55,
        "verdict": "Exhaust leak upstream of O2 sensor introduces false oxygen, causing lean reading.",
        "action": "Inspect and repair exhaust manifold/downpipe leaks.",
        "confidence_boosters": {"base_confidence": 0.75}
    },
    # 4. Intake Vacuum Leak (unmetered air) – high O2, high lambda, high trims
    {
        "case_id": "vacuum_leak",
        "name": "Intake Vacuum Leak",
        "logic": "low_idle.lambda > 1.05 && low_idle.o2 > 2.0 && low_idle.co < 0.5 && low_idle.co2 < 13.0",
        "health_score": 60,
        "verdict": "Unmetered air entering intake, causing lean condition.",
        "action": "Smoke test intake system; repair leaks.",
        "confidence_boosters": {"base_confidence": 0.75}
    },
    # 5. Lean Running (Fuel Delivery) – high lambda, high O2, but not as extreme O2 as exhaust leak, includes fuel trims
    {
        "case_id": "fuel_delivery_lean",
        "name": "Fuel Delivery Problem (Lean)",
        "logic": "low_idle.lambda > 1.07 && low_idle.o2 > 1.5 && low_idle.stft > 10 && low_idle.ltft > 8",
        "health_score": 55,
        "verdict": "Insufficient fuel delivery causing lean mixture.",
        "action": "Check fuel pump, filter, regulator, injectors.",
        "confidence_boosters": {"base_confidence": 0.8},
        "modular_addons": {"tier2_obd_dtc": ["P0171","P0174"]}
    },
    # 6. Rich Running – low lambda, high CO, very low O2, HC moderate (not misfire levels)
    {
        "case_id": "rich_running",
        "name": "System Running Rich",
        "logic": "low_idle.lambda < 0.92 && low_idle.co > 2.0 && low_idle.o2 < 0.2 && low_idle.hc < 2000",
        "health_score": 45,
        "verdict": "Excessive fuel enrichment; lambda control failed.",
        "action": "Check for leaky injectors, high fuel pressure, faulty sensors.",
        "confidence_boosters": {"base_confidence": 0.75},
        "modular_addons": {"tier2_obd_dtc": ["P0172"]}
    },
    # 7. Cold Start Enrichment (very rich, high HC, low CO2)
    {
        "case_id": "cold_start_enrichment",
        "name": "Cold Start Enrichment",
        "logic": "low_idle.co > 3.0 && low_idle.hc > 20000 && low_idle.co2 < 5.0 && low_idle.lambda < 0.7",
        "health_score": 40,
        "verdict": "Extreme enrichment during cold start; sensor or control fault.",
        "action": "Check coolant temp sensor, cold start injector, IAC valve.",
        "confidence_boosters": {"base_confidence": 0.8}
    },
    # 8. Ignition Misfire – very high HC, high O2, low CO
    {
        "case_id": "misfire",
        "name": "Engine Misfire",
        "logic": "low_idle.hc > 1500 && low_idle.o2 > 1.5 && low_idle.co < 1.0 && low_idle.co2 > 5.0",
        "health_score": 30,
        "verdict": "Spark failure causing unburned fuel and air.",
        "action": "Inspect spark plugs, coils, ignition wires.",
        "confidence_boosters": {"base_confidence": 0.9},
        "modular_addons": {"tier2_obd_dtc": ["P0300","P0301","P0302","P0303","P0304","P0305","P0306"]}
    },
    # 9. Excessively Advanced Timing – high NOx, stoich mix, very clean (low CO/HC)
    {
        "case_id": "timing_advance",
        "name": "Excessively Advanced Timing",
        "logic": "low_idle.nox > 500 && low_idle.co < 0.25 && low_idle.hc < 50 && 0.99 <= low_idle.lambda <= 1.03",
        "health_score": 50,
        "verdict": "High combustion temperature from over-advanced timing elevates NOx.",
        "action": "Check base timing, VVT system, knock sensor.",
        "confidence_boosters": {"base_confidence": 0.75},
        "modular_addons": {"tier2_obd_dtc": ["P0016"]}
    },
    # 10. Retarded Timing – low NOx, higher CO, moderate HC
    {
        "case_id": "timing_retard",
        "name": "Ignition Timing Issues (Retard)",
        "logic": "low_idle.nox < 30 && low_idle.co > 0.8 && 0.98 <= low_idle.lambda <= 1.03",
        "health_score": 50,
        "verdict": "Low NOx with elevated CO suggests retarded ignition timing.",
        "action": "Verify mechanical timing and VVT operation.",
        "confidence_boosters": {"base_confidence": 0.65},
        "modular_addons": {"tier2_obd_dtc": ["P0016"]}
    },
    # 11. O2 Sensor Sluggish – lambda near 1, O2 stuck mid-range (0.4-0.6), CO moderate
    {
        "case_id": "o2_lazy",
        "name": "O2 Sensor Sluggish or Failed",
        "logic": "0.96 <= low_idle.lambda <= 1.04 && low_idle.o2 > 0.4 && low_idle.o2 < 0.7 && low_idle.co > 0.3 && low_idle.nox < 200",
        "health_score": 60,
        "verdict": "O2 sensor voltage does not switch properly; sensor degraded.",
        "action": "Test and replace O2 sensor as needed.",
        "confidence_boosters": {"base_confidence": 0.7},
        "modular_addons": {"tier2_obd_dtc": ["P0131","P0132","P0133","P0134"]}
    },
    # 12. MAF Under-Reading – high lambda, high trims, but NOx may be elevated
    {
        "case_id": "maf_under",
        "name": "MAF Sensor Under-Reading",
        "logic": "low_idle.lambda > 1.06 && low_idle.stft > 12 && low_idle.ltft > 10 && low_idble.nox > 100",
        "health_score": 50,
        "verdict": "MAF reading low; ECU adds fuel but still lean due to under-reported airflow.",
        "action": "Clean MAF sensor; check wiring and voltage supply.",
        "confidence_boosters": {"base_confidence": 0.7},
        "modular_addons": {"tier2_obd_dtc": ["P0101","P0102"]}
    }
]

# Ensure no duplicate IDs
assert len(set(c['case_id'] for c in fresh_cases)) == len(fresh_cases)

# Write knowledge base
kb_path = Path('data/expanded_knowledge_base.json')
backup = kb_path.with_suffix('.json.bak_clean')
import shutil
shutil.copy2(kb_path, backup)
print(f"Backed up current KB to {backup}")

# Keep metadata and validation, replace diagnostic_matrix
with open(kb_path, 'r') as f:
    kb = json.load(f)

kb['diagnostic_matrix'] = fresh_cases

with open(kb_path, 'w') as f:
    json.dump(kb, f, indent=2)

print(f"Wrote clean diagnostic matrix with {len(fresh_cases)} cases.")

# Step 2: Regenerate test suite aligned to these patterns
categories = {c['name']: c for c in fresh_cases}

# Define test case generators for each category
def gen_healthy(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.05, 0.25), 2),
        'co2': round(random.uniform(14.0, 16.0), 1),
        'hc': random.randint(10, 50),
        'o2': round(random.uniform(0.1, 0.4), 2),
        'nox': random.randint(20, 80),
        'lambda_gas': round(random.uniform(0.99, 1.01), 3),
        'stft': random.randint(-5, 5),
        'ltft': random.randint(-5, 5),
        'obd_lambda': round(random.uniform(0.99, 1.01), 3),
        'dtc': None,
        'expected': 'Healthy Engine',
        'confidence': 0.95,
        'health': 100
    }

def gen_catalyst(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.8, 2.0), 2),
        'co2': round(random.uniform(13.2, 14.5), 1),
        'hc': random.randint(100, 300),
        'o2': round(random.uniform(0.3, 0.7), 2),
        'nox': random.randint(1000, 2000),
        'lambda_gas': round(random.uniform(0.98, 1.02), 3),
        'stft': random.randint(-5, 5),
        'ltft': random.randint(-5, 5),
        'obd_lambda': round(random.uniform(0.98, 1.02), 3),
        'dtc': random.choice(['P0420','P0430']),
        'expected': 'Catalytic Converter Efficiency Failure',
        'confidence': 0.9,
        'health': 40
    }

def gen_exhaust_leak(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.2, 0.6), 2),
        'co2': round(random.uniform(12.5, 13.5), 1),
        'hc': random.randint(40, 120),
        'o2': round(random.uniform(3.0, 5.0), 2),
        'nox': random.randint(50, 150),
        'lambda_gas': round(random.uniform(1.03, 1.15), 3),
        'stft': random.randint(8, 15),
        'ltft': random.randint(5, 12),
        'obd_lambda': round(random.uniform(1.03, 1.15), 3),
        'dtc': None,
        'expected': 'Exhaust Leak (False Lean)',
        'confidence': 0.75,
        'health': 55
    }

def gen_vacuum_leak(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.1, 0.3), 2),
        'co2': round(random.uniform(12.5, 13.5), 1),
        'hc': random.randint(50, 150),
        'o2': round(random.uniform(2.0, 4.0), 2),
        'nox': random.randint(80, 200),
        'lambda_gas': round(random.uniform(1.06, 1.12), 3),
        'stft': random.randint(12, 22),
        'ltft': random.randint(8, 16),
        'obd_lambda': round(random.uniform(1.06, 1.12), 3),
        'dtc': None,
        'expected': 'Intake Vacuum Leak',
        'confidence': 0.75,
        'health': 60
    }

def gen_fuel_lean(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.1, 0.3), 2),
        'co2': round(random.uniform(12.0, 13.0), 1),
        'hc': random.randint(80, 200),
        'o2': round(random.uniform(1.5, 3.0), 2),
        'nox': random.randint(120, 280),
        'lambda_gas': round(random.uniform(1.08, 1.15), 3),
        'stft': random.randint(12, 20),
        'ltft': random.randint(8, 16),
        'obd_lambda': round(random.uniform(1.08, 1.15), 3),
        'dtc': random.choice(['P0171','P0174']),
        'expected': 'Fuel Delivery Problem (Lean)',
        'confidence': 0.8,
        'health': 55
    }

def gen_rich(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(2.0, 3.5), 2),
        'co2': round(random.uniform(11.5, 12.8), 1),
        'hc': random.randint(100, 300),
        'o2': round(random.uniform(0.02, 0.15), 2),
        'nox': random.randint(10, 50),
        'lambda_gas': round(random.uniform(0.88, 0.92), 3),
        'stft': random.randint(-15, -8),
        'ltft': random.randint(-12, -6),
        'obd_lambda': round(random.uniform(0.88, 0.92), 3),
        'dtc': 'P0172',
        'expected': 'System Running Rich',
        'confidence': 0.75,
        'health': 45
    }

def gen_cold_start(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(2.5, 4.5), 2),
        'co2': round(random.uniform(11.0, 12.5), 1),
        'hc': random.randint(5000, 20000),
        'o2': round(random.uniform(0.1, 0.3), 2),
        'nox': random.randint(10, 40),
        'lambda_gas': round(random.uniform(0.65, 0.75), 3),
        'stft': random.randint(-18, -10),
        'ltft': random.randint(-12, -6),
        'obd_lambda': round(random.uniform(0.65, 0.75), 3),
        'dtc': None,
        'expected': 'Cold Start Enrichment',
        'confidence': 0.8,
        'health': 40
    }

def gen_misfire(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.2, 1.0), 2),
        'co2': round(random.uniform(6.0, 10.0), 1),  # low CO2 due to poor combustion
        'hc': random.randint(2000, 5000),
        'o2': round(random.uniform(1.5, 3.5), 2),
        'nox': random.randint(20, 80),
        'lambda_gas': round(random.uniform(1.00, 1.08), 3),
        'stft': random.randint(5, 15),
        'ltft': random.randint(3, 10),
        'obd_lambda': round(random.uniform(1.00, 1.08), 3),
        'dtc': random.choice(['P0300','P0301','P0302','P0303']),
        'expected': 'Engine Misfire',
        'confidence': 0.9,
        'health': 30
    }

def gen_timing_advance(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.1, 0.2), 2),
        'co2': round(random.uniform(13.5, 15.0), 1),
        'hc': random.randint(20, 60),
        'o2': round(random.uniform(0.1, 0.3), 2),
        'nox': random.randint(800, 1500),
        'lambda_gas': round(random.uniform(0.99, 1.03), 3),
        'stft': random.randint(-2, 2),
        'ltft': random.randint(-2, 2),
        'obd_lambda': round(random.uniform(0.99, 1.03), 3),
        'dtc': 'P0016',
        'expected': 'Excessively Advanced Timing',
        'confidence': 0.75,
        'health': 50
    }

def gen_timing_retard(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.8, 1.5), 2),
        'co2': round(random.uniform(12.0, 13.2), 1),
        'hc': random.randint(50, 150),
        'o2': round(random.uniform(0.2, 0.5), 2),
        'nox': random.randint(10, 25),
        'lambda_gas': round(random.uniform(0.99, 1.01), 3),
        'stft': random.randint(-3, 3),
        'ltft': random.randint(-3, 3),
        'obd_lambda': round(random.uniform(0.99, 1.01), 3),
        'dtc': 'P0016',
        'expected': 'Ignition Timing Issues (Retard)',
        'confidence': 0.65,
        'health': 50
    }

def gen_o2_lazy(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.3, 0.8), 2),
        'co2': round(random.uniform(13.0, 14.0), 1),
        'hc': random.randint(50, 150),
        'o2': round(random.uniform(0.45, 0.65), 2),
        'nox': random.randint(40, 100),
        'lambda_gas': round(random.uniform(0.98, 1.02), 3),
        'stft': random.randint(-3, 3),
        'ltft': random.randint(-3, 3),
        'obd_lambda': round(random.uniform(0.98, 1.02), 3),
        'dtc': random.choice(['P0131','P0132','P0133','P0134']),
        'expected': 'O2 Sensor Sluggish or Failed',
        'confidence': 0.7,
        'health': 60
    }

def gen_maf_under(fuel):
    return {
        'fuel': fuel,
        'co': round(random.uniform(0.1, 0.3), 2),
        'co2': round(random.uniform(13.0, 14.0), 1),
        'hc': random.randint(40, 120),
        'o2': round(random.uniform(1.5, 3.5), 2),
        'nox': random.randint(100, 250),
        'lambda_gas': round(random.uniform(1.06, 1.12), 3),
        'stft': random.randint(12, 20),
        'ltft': random.randint(8, 14),
        'obd_lambda': round(random.uniform(1.06, 1.12), 3),
        'dtc': random.choice(['P0101','P0102']),
        'expected': 'MAF Sensor Under-Reading',
        'confidence': 0.7,
        'health': 50
    }

# Category distribution (target counts)
total_cases = 100
category_weights = {
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

# Adjust weights to sum 100
total_weight = sum(category_weights.values())
if total_weight != 100:
    scale = 100 / total_weight
    category_weights = {k: max(1, int(v * scale)) for k, v in category_weights.items()}
    # Ensure total is 100 by adjusting largest
    diff = 100 - sum(category_weights.values())
    category_weights['Healthy Engine'] += diff

# Generate cases
cases = []
case_id = 1
for category, count in category_weights.items():
    for _ in range(count):
        fuel = random.choice(['E0', 'E5', 'E10', 'E85'])
        if category == 'Healthy Engine':
            data = gen_healthy(fuel)
        elif category == 'Catalytic Converter Efficiency Failure':
            data = gen_catalyst(fuel)
        elif category == 'Exhaust Leak (False Lean)':
            data = gen_exhaust_leak(fuel)
        elif category == 'Intake Vacuum Leak':
            data = gen_vacuum_leak(fuel)
        elif category == 'Fuel Delivery Problem (Lean)':
            data = gen_fuel_lean(fuel)
        elif category == 'System Running Rich':
            data = gen_rich(fuel)
        elif category == 'Cold Start Enrichment':
            data = gen_cold_start(fuel)
        elif category == 'Engine Misfire':
            data = gen_misfire(fuel)
        elif category == 'Excessively Advanced Timing':
            data = gen_timing_advance(fuel)
        elif category == 'Ignition Timing Issues (Retard)':
            data = gen_timing_retard(fuel)
        elif category == 'O2 Sensor Sluggish or Failed':
            data = gen_o2_lazy(fuel)
        elif category == 'MAF Sensor Under-Reading':
            data = gen_maf_under(fuel)
        else:
            continue
        data['ID'] = f'TC{case_id:03d}'
        data['Expected_Result'] = data.pop('expected')
        data['Confidence_Score'] = data.pop('confidence')
        data['ECU_Health'] = data.pop('health')
        # Map to CSV columns
        cases.append({
            'ID': data['ID'],
            'Fuel': data['fuel'],
            'CO_Pct': data['co'],
            'CO2_Pct': data['co2'],
            'HC_PPM': data['hc'],
            'O2_Pct': data['o2'],
            'NOx_PPM': data['nox'],
            'Lambda_Gas': data['lambda_gas'],
            'OBD_STFT': data['stft'],
            'OBD_LTFT': data['ltft'],
            'OBD_Lambda': data['obd_lambda'],
            'OBD_DTC': data['dtc'] if data['dtc'] else 'None',
            'Expected_Result': data['Expected_Result'],
            'Confidence_Score': data['Confidence_Score'],
            'ECU_Health': data['ECU_Health']
        })
        case_id += 1

# Shuffle and trim to exactly 100
random.shuffle(cases)
cases = cases[:100]
cases.sort(key=lambda x: int(x['ID'][2:]))  # sort by ID

# Write CSV
csv_path = Path('petrol_100_test_suite.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'ID','Fuel','CO_Pct','CO2_Pct','HC_PPM','O2_Pct','NOx_PPM','Lambda_Gas',
        'OBD_STFT','OBD_LTFT','OBD_Lambda','OBD_DTC','Expected_Result','Confidence_Score','ECU_Health'
    ])
    writer.writeheader()
    writer.writerows(cases)

print(f"Generated new test suite: {len(cases)} cases")
print("Category counts:")
counts = {}
for c in cases:
    exp = c['Expected_Result']
    counts[exp] = counts.get(exp, 0) + 1
for cat, cnt in sorted(counts.items()):
    print(f"  {cat}: {cnt}")
