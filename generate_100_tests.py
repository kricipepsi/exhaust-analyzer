#!/usr/bin/env python3
"""Generate a 100-case petrol-only diagnostic test suite from archive rules and standard references."""

import csv
import random
from pathlib import Path

random.seed(42)  # For reproducibility

# Knowledge base patterns from ARCHIVE/diagnostic_rules.yaml
patterns = {
    # Healthy baseline
    'healthy_e0': {
        'name': 'Healthy Engine (E0)',
        'fuel': 'e0',
        'lambda': 1.00,
        'co': (0.05, 0.2),
        'co2': (14.0, 15.0),
        'hc': (10, 50),
        'o2': (0.1, 0.3),
        'nox': (20, 80),
        'stft': (-5, 5),
        'ltft': (-5, 5),
        'obd_lambda': 1.00,
        'dtc': None,
        'expected': 'Healthy Engine',
        'confidence': 0.95,
        'health': 100
    },
    'healthy_e10': {
        'name': 'Healthy Engine (E10)',
        'fuel': 'e10',
        'lambda': 1.00,
        'co': (0.08, 0.25),
        'co2': (13.5, 14.5),
        'hc': (10, 60),
        'o2': (0.1, 0.4),
        'nox': (15, 70),
        'stft': (-5, 5),
        'ltft': (-5, 5),
        'obd_lambda': 1.00,
        'dtc': None,
        'expected': 'Healthy Engine',
        'confidence': 0.95,
        'health': 100
    },
    'healthy_e85': {
        'name': 'Healthy Engine (E85)',
        'fuel': 'e85',
        'lambda': 1.00,
        'co': (0.1, 0.3),
        'co2': (12.5, 13.5),
        'hc': (20, 80),
        'o2': (0.15, 0.5),
        'nox': (10, 50),
        'stft': (-8, 8),
        'ltft': (-8, 8),
        'obd_lambda': 1.00,
        'dtc': None,
        'expected': 'Healthy Engine',
        'confidence': 0.90,
        'health': 100
    },

    # Rich conditions
    'rich_slight': {
        'name': 'Slightly Rich Running',
        'fuel': 'e10',
        'lambda': 0.95,
        'co': (0.8, 1.5),
        'co2': (12.0, 13.0),
        'hc': (50, 150),
        'o2': (0.05, 0.15),
        'nox': (20, 60),
        'stft': (-10, -5),
        'ltft': (-8, -3),
        'obd_lambda': 0.95,
        'dtc': 'P0172',
        'expected': 'System Running Rich',
        'confidence': 0.80,
        'health': 75
    },
    'rich_moderate': {
        'name': 'Moderately Rich Running',
        'fuel': 'e10',
        'lambda': 0.90,
        'co': (1.5, 3.0),
        'co2': (11.0, 12.5),
        'hc': (150, 500),
        'o2': (0.02, 0.1),
        'nox': (15, 50),
        'stft': (-15, -8),
        'ltft': (-12, -6),
        'obd_lambda': 0.90,
        'dtc': 'P0172',
        'expected': 'rich_exhaust',
        'confidence': 0.85,
        'health': 60
    },

    # Lean conditions
    'lean_slight': {
        'name': 'Slightly Lean Running',
        'fuel': 'e10',
        'lambda': 1.05,
        'co': (0.05, 0.15),
        'co2': (12.5, 13.5),
        'hc': (30, 100),
        'o2': (1.5, 3.0),
        'nox': (60, 150),
        'stft': (8, 15),
        'ltft': (5, 12),
        'obd_lambda': 1.05,
        'dtc': 'P0171',
        'expected': 'lean_exhaust',
        'confidence': 0.75,
        'health': 75
    },
    'lean_significant': {
        'name': 'Significant Lean Condition',
        'fuel': 'e10',
        'lambda': 1.12,
        'co': (0.02, 0.1),
        'co2': (11.5, 12.5),
        'hc': (100, 400),
        'o2': (3.0, 6.0),
        'nox': (100, 300),
        'stft': (15, 25),
        'ltft': (10, 20),
        'obd_lambda': 1.12,
        'dtc': 'P0171',
        'expected': 'lean_exhaust',
        'confidence': 0.80,
        'health': 60
    },

    # Vacuum leak (differential pattern - need both low and high, but we can simulate low data with high positive trims)
    'vacuum_leak': {
        'name': 'Intake Vacuum Leak',
        'fuel': 'e10',
        'lambda': 1.10,
        'co': (0.1, 0.3),
        'co2': (13.0, 14.0),
        'hc': (50, 150),
        'o2': (2.0, 4.0),
        'nox': (80, 200),
        'stft': (15, 25),
        'ltft': (10, 18),
        'obd_lambda': 1.10,
        'dtc': None,
        'expected': 'Intake Vacuum Leak',
        'confidence': 0.70,
        'health': 70
    },

    # MAF under-report
    'maf_under': {
        'name': 'MAF Sensor Under-Reading',
        'fuel': 'e10',
        'lambda': 1.08,
        'co': (0.1, 0.3),
        'co2': (13.0, 14.0),
        'hc': (40, 120),
        'o2': (1.5, 3.5),
        'nox': (100, 250),
        'stft': (12, 22),
        'ltft': (8, 16),
        'obd_lambda': 1.08,
        'dtc': 'P0101',
        'expected': 'MAF Sensor Under-Reading',
        'confidence': 0.75,
        'health': 65
    },

    # O2 sensor lazy
    'o2_lazy': {
        'name': 'O2 Sensor Sluggish',
        'fuel': 'e10',
        'lambda': 1.00,
        'co': (0.3, 0.8),
        'co2': (13.0, 14.0),
        'hc': (50, 150),
        'o2': (0.4, 0.6),  # Stuck middle
        'nox': (40, 100),
        'stft': (-3, 3),
        'ltft': (-3, 3),
        'obd_lambda': 1.00,
        'dtc': 'P0131',
        'expected': 'O2 Sensor Sluggish or Failed',
        'confidence': 0.65,
        'health': 70
    },

    # Catalyst failure (high NOx, moderate CO/HC)
    'catalyst_fail': {
        'name': 'Catalytic Converter Failure',
        'fuel': 'e10',
        'lambda': 0.98,
        'co': (0.8, 2.0),
        'co2': (13.0, 14.0),
        'hc': (100, 300),
        'o2': (0.3, 0.7),
        'nox': (1000, 2000),
        'stft': (-5, 5),
        'ltft': (-5, 5),
        'obd_lambda': 0.98,
        'dtc': 'P0420',
        'expected': 'Catalytic Converter Efficiency Failure',
        'confidence': 0.85,
        'health': 40
    },

    # Misfire (very high HC)
    'misfire': {
        'name': 'Engine Misfire',
        'fuel': 'e10',
        'lambda': 1.02,
        'co': (0.2, 1.0),
        'co2': (12.0, 13.5),
        'hc': (2000, 5000),
        'o2': (1.0, 3.0),
        'nox': (30, 100),
        'stft': (5, 15),
        'ltft': (3, 10),
        'obd_lambda': 1.02,
        'dtc': 'P0300',
        'expected': 'Engine Misfire',
        'confidence': 0.90,
        'health': 30
    },

    # Timing advanced (high NOx, good mixture)
    'timing_adv': {
        'name': 'Excessively Advanced Timing',
        'fuel': 'e10',
        'lambda': 1.00,
        'co': (0.1, 0.3),
        'co2': (13.5, 14.5),
        'hc': (20, 60),
        'o2': (0.1, 0.3),
        'nox': (800, 1500),
        'stft': (-2, 2),
        'ltft': (-2, 2),
        'obd_lambda': 1.00,
        'dtc': 'P0016',
        'expected': 'Excessively Advanced Timing',
        'confidence': 0.75,
        'health': 70
    },

    # Timing retarded (low NOx, higher CO)
    'timing_ret': {
        'name': 'Retarded Ignition Timing',
        'fuel': 'e10',
        'lambda': 1.00,
        'co': (0.8, 2.0),
        'co2': (12.5, 13.5),
        'hc': (50, 150),
        'o2': (0.2, 0.5),
        'nox': (10, 40),
        'stft': (-3, 3),
        'ltft': (-3, 3),
        'obd_lambda': 1.00,
        'dtc': 'P0016',
        'expected': 'Ignition Timing Issues',
        'confidence': 0.70,
        'health': 75
    },

    # Exhaust leak (pre-O2)
    'exhaust_leak': {
        'name': 'Exhaust Leak (pre-O2 sensor)',
        'fuel': 'e10',
        'lambda': 1.05,
        'co': (0.2, 0.6),
        'co2': (13.0, 14.0),
        'hc': (40, 120),
        'o2': (1.5, 3.5),  # extra O2 from leak
        'nox': (80, 200),
        'stft': (8, 15),
        'ltft': (5, 10),
        'obd_lambda': 1.05,
        'dtc': None,
        'expected': 'Exhaust Leak',
        'confidence': 0.60,
        'health': 75
    },

    # Fuel delivery (lean under load) - but at idle maybe moderate
    'fuel_delivery_lean': {
        'name': 'Fuel Delivery Problem (Lean)',
        'fuel': 'e10',
        'lambda': 1.08,
        'co': (0.1, 0.3),
        'co2': (12.5, 13.5),
        'hc': (80, 200),
        'o2': (2.0, 4.0),
        'nox': (120, 280),
        'stft': (12, 20),
        'ltft': (8, 16),
        'obd_lambda': 1.08,
        'dtc': 'P0171',
        'expected': 'Fuel Delivery Problem (Lean)',
        'confidence': 0.70,
        'health': 65
    },

    # Cold engine (enrichment)
    'cold_start': {
        'name': 'Cold Start Enrichment',
        'fuel': 'e10',
        'lambda': 0.85,
        'co': (2.0, 4.0),
        'co2': (11.0, 12.5),
        'hc': (500, 2000),
        'o2': (0.1, 0.3),
        'nox': (10, 40),
        'stft': (-15, -8),
        'ltft': (-10, -5),
        'obd_lambda': 0.85,
        'dtc': None,
        'expected': 'Cold Start Enrichment',
        'confidence': 0.80,
        'health': 90
    }
}

# Expand patterns with variations to reach 100 cases
cases = []
case_id = 1

# Add base patterns first
for key, pat in patterns.items():
    for fuel_variant in []:
        pass  # We'll use each pattern as-is and create variations

# We'll create base set first
base_cases = list(patterns.keys())

# Generate 100 cases by varying parameters slightly and assigning IDs
while len(cases) < 100:
    base_key = random.choice(base_cases)
    base = patterns[base_key]

    # Slight random variation within ranges
    def rand_range(r):
        return round(random.uniform(r[0], r[1]), 2) if isinstance(r[0], float) else random.randint(r[0], r[1])

    # For each base, we can create a few variants
    # To avoid too many duplicates, we track combinations
    fuel = base['fuel']
    lambda_val = base['lambda']
    co = rand_range(base['co'])
    co2 = rand_range(base['co2'])
    hc = rand_range(base['hc'])
    o2 = rand_range(base['o2'])
    nox = rand_range(base['nox'])
    stft = rand_range(base['stft'])
    ltft = rand_range(base['ltft'])
    obd_lambda = base['obd_lambda']

    # For some cases, use different DTCs for same pattern (e.g., catalyst failures can also have P0430)
    dtc = base['dtc']
    if base_key == 'catalyst_fail' and random.random() < 0.3:
        dtc = 'P0430'

    # Ensure ID is unique
    case_num = case_id
    case_id += 1

    cases.append({
        'ID': f'TC{case_num:03d}',
        'Fuel': fuel.upper(),
        'CO_Pct': co,
        'CO2_Pct': co2,
        'HC_PPM': hc,
        'O2_Pct': o2,
        'NOx_PPM': nox,
        'Lambda_Gas': round(lambda_val, 3),
        'OBD_STFT': stft,
        'OBD_LTFT': ltft,
        'OBD_Lambda': obd_lambda,
        'OBD_DTC': dtc if dtc else 'None',
        'Expected_Result': base['expected'],
        'Confidence_Score': base['confidence'],
        'ECU_Health': base['health']
    })

# Ensure we have exactly 100 (trim or expand)
if len(cases) > 100:
    cases = cases[:100]
elif len(cases) < 100:
    # Pad with more variants of healthy and common faults
    while len(cases) < 100:
        # pick random base
        base_key = random.choice(base_cases)
        base = patterns[base_key]
        # generate IDs
        case_num = len(cases) + 1
        fuel = base['fuel']
        lambda_val = base['lambda']
        co = round(random.uniform(*base['co']), 2)
        co2 = round(random.uniform(*base['co2']), 2)
        hc = random.randint(base['hc'][0], base['hc'][1])
        o2 = round(random.uniform(*base['o2']), 2)
        nox = random.randint(base['nox'][0], base['nox'][1])
        stft = round(random.uniform(*base['stft']), 1)
        ltft = round(random.uniform(*base['ltft']), 1)
        obd_lambda = base['obd_lambda']
        dtc = base['dtc'] if base['dtc'] else 'None'
        cases.append({
            'ID': f'TC{case_num:03d}',
            'Fuel': fuel.upper(),
            'CO_Pct': co,
            'CO2_Pct': co2,
            'HC_PPM': hc,
            'O2_Pct': o2,
            'NOx_PPM': nox,
            'Lambda_Gas': round(lambda_val, 3),
            'OBD_STFT': stft,
            'OBD_LTFT': ltft,
            'OBD_Lambda': obd_lambda,
            'OBD_DTC': dtc,
            'Expected_Result': base['expected'],
            'Confidence_Score': base['confidence'],
            'ECU_Health': base['health']
        })

# Shuffle to mix up order
random.shuffle(cases)

# Write CSV
output_path = Path('petrol_100_test_suite.csv')
with open(output_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'ID', 'Fuel', 'CO_Pct', 'CO2_Pct', 'HC_PPM', 'O2_Pct', 'NOx_PPM',
        'Lambda_Gas', 'OBD_STFT', 'OBD_LTFT', 'OBD_Lambda', 'OBD_DTC',
        'Expected_Result', 'Confidence_Score', 'ECU_Health'
    ])
    writer.writeheader()
    writer.writerows(cases)

print(f"Generated {len(cases)} test cases to {output_path}")

# Also write a README with category summary
categories = {}
for c in cases:
    exp = c['Expected_Result']
    categories[exp] = categories.get(exp, 0) + 1

readme = f"""# Petrol Diagnostic Test Suite

This directory contains a 100-case test validator suite for the petrol diagnostic application.

## Files
- `petrol_100_test_suite.csv` – Test cases in CSV format

## Test Case Format
Each case includes:
- **ID**: Unique test case identifier (TC001–TC100)
- **Fuel**: Petrol variant (E0, E5, E10, E85)
- **CO_Pct, CO2_Pct, HC_PPM, O2_Pct, NOx_PPM**: 5-gas analyzer readings
- **Lambda_Gas**: Calculated or measured lambda
- **OBD_STFT, OBD_LTFT, OBD_Lambda**: Live OBD-II PID data
- **OBD_DTC**: Diagnostic Trouble Code (if applicable)
- **Expected_Result**: The case name that should be matched
- **Confidence_Score**: Target confidence (0-1)
- **ECU_Health**: Target health score (0-100)

## Categories Covered ({len(categories)})
"""
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    readme += f"- {cat}: {count} cases\n"

readme += """
## Usage
Run the test validator (ensure engine is running):
```bash
cd petrol_diagnostic
python run_100cvs_tests.py
```
The script expects the CSV at the same name. It will output pass/fail counts and save detailed results to `test_100cvs_results.json`.

## Notes
- Cases are designed for petrol engines only.
- Ranges are based on real-world diagnostic patterns (AHAA, ASE, OEM references) and the project's `diagnostic_rules.yaml`.
- Some cases include DTCs to test confidence boosting.
- Healthy engine variations cover different ethanol blends.
"""

readme_path = Path('PETROL_TEST_SUITE_README.md')
readme_path.write_text(readme, encoding='utf-8')
print(f"Wrote README to {readme_path}")
print(f"\nCategory distribution:\n" + '\n'.join([f'  {k}: {v}' for k,v in categories.items()]))
