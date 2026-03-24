#!/usr/bin/env python3
"""Manually add 15 high-priority diagnostic cases from YAML review."""

import json

# Load existing expanded KB
with open('data/expanded_knowledge_base.json', 'r') as f:
    kb = json.load(f)

# New cases to add (based on diagnostic_rules_enhanced.yaml patterns)
new_cases = [
    {
        "case_id": "late_ignition_timing",
        "name": "Late Ignition Timing",
        "logic": "low_idle.co > 7.0 and low_idle.hc > 7000 and low_idle.o2 > 6.0 and low_idle.co2 < 8.0 and (0.85 <= calculated_lambda <= 0.95)",
        "health_score": 40,
        "verdict": "Late Ignition Timing - High CO/HC with low CO2 and excess O2 in rich condition",
        "action": "Check ignition timing, VVT system, cam/crank sensors, mechanical timing stretch"
    },
    {
        "case_id": "ignition_failure_no_spark",
        "name": "Ignition System Failure (No Spark)",
        "logic": "low_idle.hc > 20000 and low_idle.co < 0.1 and low_idle.co2 < 1.0 and low_idle.o2 > 15.0 and (0.95 <= calculated_lambda <= 1.2)",
        "health_score": 30,
        "verdict": "No Spark - Extreme HC with near-zero CO/CO2 and atmospheric O2",
        "action": "Check ignition coils, spark plugs, wires, crank/cam sensors"
    },
    {
        "case_id": "fuel_delivery_lean",
        "name": "Fuel Delivery Problem (Lean)",
        "logic": "low_idle.hc > 2000 and low_idle.o2 > 15.0 and low_idle.co2 < 5.0 and calculated_lambda > 1.3",
        "health_score": 40,
        "verdict": "Lean Condition - High O2/HC with low CO2, no lambda control",
        "action": "Inspect fuel pump, filter, pressure regulator, injectors for clogging"
    },
    {
        "case_id": "fuel_delivery_rich_injector_leak",
        "name": "Rich from Injector Leak / High Pressure",
        "logic": "low_idle.co > 3.0 and low_idle.hc > 500 and low_idle.o2 < 0.5 and low_idle.co2 < 13.0 and calculated_lambda < 0.9",
        "health_score": 45,
        "verdict": "System Rich - Excess fuel from leaky injectors or high pressure",
        "action": "Check injectors for leakage, fuel pressure regulator, air filter restriction, O2 sensor bias"
    },
    {
        "case_id": "egr_stuck_open_idle",
        "name": "EGR Valve Stuck Open at Idle",
        "logic": "0.98 <= calculated_lambda <= 1.02 and low_idle.co > 2.0 and low_idle.o2 > 2.0 and low_idle.co2 < 13.0 and low_idle.hc > 1000",
        "health_score": 55,
        "verdict": "EGR Stuck Open - Stoichiometric but poor combustion due to dilution",
        "action": "Check EGR valve operation, position sensor, vacuum lines; test at higher RPM to confirm"
    },
    {
        "case_id": "catalyst_failure_high_nox",
        "name": "Catalytic Converter NOx Conversion Failure",
        "logic": "calculated_lambda > 1.05 and low_idle.nox > 1000",
        "health_score": 50,
        "verdict": "Catalyst NOx Failure - Lean combustion with high NOx indicates poor three-way conversion",
        "action": "Replace catalytic converter; check for codes P0420/P0430; inspect for oil/fuel contamination"
    },
    {
        "case_id": "cold_start_over_enrichment",
        "name": "Cold Start Enrichment Fault",
        "logic": "low_idle.co > 3.0 and low_idle.hc > 20000 and low_idle.co2 < 5.0",
        "health_score": 50,
        "verdict": "Over-enrichment during cold start - Excessive fuel not being burned",
        "action": "Check coolant temperature sensor, cold start injector/pump pulse width, fuel mixture enrichment parameters"
    },
    {
        "case_id": "mass_airflow_underreport",
        "name": "MAF Sensor Under-Reading",
        "logic": "calculated_lambda > 1.05 and low_idle.o2 > 1.5 and (low_idle.co < 0.5 or low_idle.co2 < 12.0)",
        "health_score": 55,
        "verdict": "MAF Under-Reporting - Lean condition persists across RPM range, airflow signal low",
        "action": "Check MAF sensor for contamination, wiring, voltage supply; compare MAF vs. rpm vs. throttle"
    },
    {
        "case_id": "o2_sensor_lazy",
        "name": "O2 Sensor Sluggish or Failed",
        "logic": "low_idle.o2 > 1.0 and low_idle.o2 < 2.0 and low_idle.co2 > 14.0 and low_idle.hc < 100",
        "health_score": 60,
        "verdict": "O2 Sensor Not Switching - Voltage stuck mid-range, slow response",
        "action": "Test O2 sensor frequency and amplitude at >2000 RPM; replace if <1 Hz or narrow range"
    },
    {
        "case_id": "ignition_misfire_high_hc_o2",
        "name": "Ignition Misfire (High HC + High O2)",
        "logic": "low_idle.hc > 300 and low_idle.o2 > 2.0 and low_idle.co < 0.5",
        "health_score": 35,
        "verdict": "Misfire Detected - Raw fuel and unburned oxygen exiting cylinders",
        "action": "Check spark plugs, ignition coils, wires, compression, fuel injector operation"
    },
    {
        "case_id": "system_rich_negative_trims",
        "name": "System Rich with Negative Fuel Trims",
        "logic": "low_idle.co > 2.0 and low_idle.hc > 200 and low_idle.o2 < 0.3 and low_idle.co2 < 13.0",
        "health_score": 50,
        "verdict": "Rich Mixture - Negative fuel trim territory, possible injector leak or O2 bias",
        "action": "Inspect for leaking injectors, fuel pressure regulator, contaminated O2 sensor, coolant temp sensor reading cold"
    },
    {
        "case_id": "exhaust_leak_false_lean",
        "name": "Exhaust Leak Causing False Lean",
        "logic": "measured_lambda > calculated_lambda + 0.05 and low_idle.o2 > 2.0",
        "health_score": 85,
        "verdict": "Exhaust Dilution - Air entering tailpipe inflates measured lambda; engine actually healthy",
        "action": "Inspect exhaust manifold, gaskets, downpipe for holes before O2 sensor; seal leak"
    },
    {
        "case_id": "vacuum_leak_differential",
        "name": "Vacuum Leak (Idle Only)",
        "logic": "low_idle.lambda > 1.05 and low_idle.o2 > 1.5",
        "health_score": 60,
        "verdict": "Idle-Only Air Leak - Extra air unmetered at idle, stabilizes at speed",
        "action": "Check intake manifold gaskets, vacuum hoses, brake booster, throttle body gasket"
    },
    {
        "case_id": "cat_inefficiency_perfect_lambda",
        "name": "Catalyst Inefficiency (Perfect Lambda)",
        "logic": "abs(calculated_lambda - 1.0) < 0.02 and low_idle.co > 0.6 and low_idle.co2 < 12.5",
        "health_score": 40,
        "verdict": "Dead Catalyst - Engine combustion perfect but converter not oxidizing pollutants",
        "action": "Replace catalytic converter; check for prior misfire codes that may have melted it"
    },
    {
        "case_id": "engine_wear_oil_burning",
        "name": "Engine Oil Burning (Worn Rings/Valves)",
        "logic": "low_idle.hc > 500 and low_idle.co > 0.5 and low_idle.o2 < 1.0 and low_idle.co2 < 12.0",
        "health_score": 55,
        "verdict": "Oil Combustion - Elevated HC and CO with rich-ish mixture indicates oil burning",
        "action": "Perform compression test, leak-down; inspect valve guides, piston rings; check for blue smoke"
    }
]

# Append new cases (avoid duplicate IDs)
existing_ids = set(c['case_id'] for c in kb['diagnostic_matrix'])
added = 0
for case in new_cases:
    if case['case_id'] not in existing_ids:
        kb['diagnostic_matrix'].append(case)
        added += 1
        existing_ids.add(case['case_id'])

# Save
with open('data/expanded_knowledge_base.json', 'w') as f:
    json.dump(kb, f, indent=2)

print(f"Added {added} new manual cases.")
print(f"Total cases: {len(kb['diagnostic_matrix'])}")
print("New IDs:", [c['case_id'] for c in new_cases if c['case_id'] in existing_ids])
