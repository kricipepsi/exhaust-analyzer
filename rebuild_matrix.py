#!/usr/bin/env python3
"""Replace entire diagnostic matrix with refined and reordered cases."""

from pathlib import Path
import json

kb_path = Path('data/expanded_knowledge_base.json')
backup_path = kb_path.with_suffix('.json.bak_20260323_final')
import shutil
if not backup_path.exists():
    shutil.copy2(kb_path, backup_path)
    print(f"Backup: {backup_path}")

with open(kb_path, 'r') as f:
    kb = json.load(f)

# Build fresh matrix
fresh_matrix = [
    # Catalyst failures (top priority)
    {
        "case_id": "catalyst_failure",
        "name": "Catalytic Converter Efficiency Failure",
        "logic": "low_idle.nox > 1000 && low_idle.co2 < 13.0 && low_idle.hc > 50",
        "health_score": 40,
        "verdict": "Catalytic Converter Efficiency Failure - Condition: nox=>1000",
        "action": "Follow diagnostic procedure for: Aged/failed catalyst substrate; Contaminated by oil or fuel additives; Thermal shock damage",
        "confidence_boosters": {"base_confidence": 0.85},
        "modular_addons": {"tier2_obd_dtc": ["P0420", "P0430"]}
    },
    # High NOx patterns
    {
        "case_id": "high_nox_timing_advance",
        "name": "Excessively Advanced Timing",
        "logic": "low_idle.nox > 500 && low_idle.co < 0.25 && low_idle.hc < 80 && 0.99 <= low_idle.lambda <= 1.03",
        "health_score": 50,
        "verdict": "High NOx with near-stoich mixture and clean burn indicates excessive ignition advance raising combustion temperature.",
        "action": "Check knock sensor, VVT cam phaser, base timing, and for carbon buildup increasing compression.",
        "confidence_boosters": {"base_confidence": 0.75}
    },
    {
        "case_id": "high_nox_lean_egr",
        "name": "High NOx + Lean Idle (EGR/Cooling Failure)",
        "logic": "low_idle.nox > 800 && low_idle.lambda > 1.03 && low_idle.o2 > 1.0",
        "health_score": 45,
        "verdict": "High NOx with lean idle indicates EGR not recirculating or cooling failure allowing excessive combustion temperatures.",
        "action": "Check EGR valve operation, EGR cooler, engine coolant temperature, and thermostat.",
        "confidence_boosters": {"base_confidence": 0.7}
    },
    # Misfire patterns
    {
        "case_id": "ignition_misfire_high_hc_o2",
        "name": "Engine Misfire",
        "logic": "low_idle.hc > 1500 && low_idle.o2 > 1.5 && low_idle.co < 1.0 && low_idle.co2 > 5.0 && low_idle.nox < 200",
        "health_score": 30,
        "verdict": "Raw fuel and air detected together. Spark was not triggered.",
        "action": "Check spark plugs, ignition coils, and high-tension leads immediately.",
        "confidence_boosters": {"base_confidence": 0.85},
        "modular_addons": {"tier2_obd_dtc": ["P0300","P0301","P0302","P0303","P0304","P0305","P0306"]}
    },
    {
        "case_id": "P_004",
        "name": "Ignition Misfire",
        "logic": "low_idle.hc > 500 && low_idle.hc < 3000 && low_idle.o2 > 1.5 && low_idle.co < 2.0",
        "health_score": 35,
        "verdict": "Misfire detected via exhaust gas composition.",
        "action": "Inspect ignition system: spark plugs, coils, wires; also fuel injector operation.",
        "confidence_boosters": {"base_confidence": 0.7}
    },
    # Enrichment patterns
    {
        "case_id": "cold_start_enrichment_fault",
        "name": "Cold Start Enrichment",
        "logic": "low_idle.co > 3.0 && low_idle.hc > 20000 && low_idle.co2 < 5.0 && low_idle.lambda < 0.75",
        "health_score": 40,
        "verdict": "Over-enrichment during cold start. Engine coolant temp sensor may be reading incorrectly low.",
        "action": "Check engine coolant temperature sensor, cold start injector (if equipped), and IAC/air control valve.",
        "confidence_boosters": {"base_confidence": 0.8}
    },
    {
        "case_id": "rich_exhaust",
        "name": "rich_exhaust",
        "logic": "low_idle.lambda < 0.98 && low_idle.co > 0.8 && low_idle.o2 < 0.5 && low_idle.hc > 50 && low_idle.hc < 1000 && low_idle.nox < 200",
        "health_score": 50,
        "verdict": "Rich exhaust with moderate CO and HC. Possible incomplete combustion.",
        "action": "Check for leaky injectors, high fuel pressure, or O2 sensor fault.",
        "confidence_boosters": {"base_confidence": 0.65},
        "modular_addons": {"tier2_obd_dtc": ["P0172"]}
    },
    {
        "case_id": "P_005",
        "name": "System Running Rich",
        "logic": "low_idle.lambda < 0.92 && low_idle.co > 2.0 && low_idle.o2 < 0.2 && low_idle.hc < 2000 && low_idle.nox < 100",
        "health_score": 45,
        "verdict": "Engine running excessively rich; lambda control lost.",
        "action": "Check fuel pressure regulator, injector leaks, coolant temp sensor, and clogged air filter.",
        "confidence_boosters": {"base_confidence": 0.7},
        "modular_addons": {"tier2_obd_dtc": ["P0172"]}
    },
    {
        "case_id": "pattern_001",
        "name": "System Running Rich",
        "logic": "low_idle.lambda < 0.95 && low_idle.co > 1.0 && low_idle.o2 < 0.3 && low_idle.hc < 3000",
        "health_score": 50,
        "verdict": "Rich mixture indicated by high CO, low O2, and sub-1.0 lambda.",
        "action": "Check for leaking injectors, high fuel pressure, clogged air filter, or O2 sensor fault.",
        "confidence_boosters": {"base_confidence": 0.65},
        "modular_addons": {"tier2_obd_dtc": ["P0172"]}
    },
    # Dilution and misfire
    {
        "case_id": "P_003",
        "name": "Exhaust Dilution (False Lean)",
        "logic": "measured_lambda > calculated_lambda + 0.05 && low_idle.o2 > 2.0",
        "health_score": 85,
        "verdict": "Bretschneider vs Measured Lambda mismatch. Atmospheric air entering tailpipe.",
        "action": "Find and seal exhaust leak near O2 sensor or flange.",
        "confidence_boosters": {"base_confidence": 0.8}
    },
    # Fuel delivery lean
    {
        "case_id": "fuel_delivery_lean",
        "name": "Fuel Delivery Problem (Lean)",
        "logic": "low_idle.lambda > 1.07 && low_idle.stft > 12 && low_idle.ltft > 8 && low_idle.nox > 100",
        "health_score": 55,
        "verdict": "Consistently lean with high fuel trims suggests insufficient fuel delivery.",
        "action": "Check fuel pump pressure, fuel filter, and injector flow rates.",
        "confidence_boosters": {"base_confidence": 0.7},
        "modular_addons": {"tier2_obd_dtc": ["P0171","P0174"]}
    },
    {
        "case_id": "pattern_012",
        "name": "Fuel Delivery Problem (Lean)",
        "logic": "low_idle.lambda > 1.06 && low_idle.o2 > 2.0 && low_idle.co < 0.3 && low_idle.co2 < 13.0",
        "health_score": 50,
        "verdict": "Lean condition with low CO and CO2 indicates fuel starvation.",
        "action": "Inspect fuel pump, filter, regulator, and injectors.",
        "confidence_boosters": {"base_confidence": 0.65}
    },
    # MAF under
    {
        "case_id": "mass_airflow_underreport",
        "name": "MAF Sensor Under-Reading",
        "logic": "low_idle.lambda > 1.06 && low_idle.stft > 15 && low_idle.ltft > 10 && low_idle.nox > 120",
        "health_score": 50,
        "verdict": "MAF reading low while trims positive indicates sensor under-reporting airflow.",
        "action": "Clean MAF sensor, check wiring, and perform MAF circuit test.",
        "confidence_boosters": {"base_confidence": 0.7},
        "modular_addons": {"tier2_obd_dtc": ["P0101","P0102"]}
    },
    # O2 lazy
    {
        "case_id": "o2_sensor_lazy",
        "name": "O2 Sensor Sluggish or Failed",
        "logic": "0.96 <= low_idle.lambda <= 1.04 && low_idle.o2 > 0.4 && low_idle.o2 < 0.7 && low_idle.co > 0.3 && low_idle.nox < 200",
        "health_score": 60,
        "verdict": "O2 sensor voltage appears stuck mid-range, not switching correctly.",
        "action": "Test O2 sensor response; replace if slow or dead.",
        "confidence_boosters": {"base_confidence": 0.65},
        "modular_addons": {"tier2_obd_dtc": ["P0131","P0132","P0133","P0134"]}
    },
    # Exhaust leak
    {
        "case_id": "exhaust_leak_false_lean",
        "name": "Exhaust Leak",
        "logic": "low_idle.o2 > 3.0 && low_idle.lambda > 1.05 && low_idle.co < 0.5 && low_idle.co2 < 12.0 && low_idle.nox < 100",
        "health_score": 55,
        "verdict": "High O2 and false lean condition due to exhaust leak upstream of O2 sensor.",
        "action": "Inspect exhaust manifold, downpipe, and flanges for leaks; repair.",
        "confidence_boosters": {"base_confidence": 0.6}
    },
    # Timing issues
    {
        "case_id": "timing_retard",
        "name": "Ignition Timing Issues",
        "logic": "low_idle.nox < 30 && low_idle.co > 0.8 && low_idle.co2 < 13.0 && 0.98 <= low_idle.lambda <= 1.02",
        "health_score": 50,
        "verdict": "Low NOx with higher CO suggests retarded ignition timing.",
        "action": "Check cam/crank sensor alignment, VVT system, mechanical timing stretch.",
        "confidence_boosters": {"base_confidence": 0.65},
        "modular_addons": {"tier2_obd_dtc": ["P0016","P0017"]}
    },
    {
        "case_id": "pattern_006",
        "name": "Ignition Timing Issues",
        "logic": "low_idle.nox < 40 && low_idle.co > 0.6 && low_idle.hc > 40 && low_idle.co2 < 13.5",
        "health_score": 55,
        "verdict": "Retarded timing causes higher CO and lower NOx.",
        "action": "Verify base timing and VVT phaser operation.",
        "confidence_boosters": {"base_confidence": 0.6}
    },
    # Lean exhaust pattern (distinct from fuel delivery)
    {
        "case_id": "pattern_002",
        "name": "lean_exhaust",
        "logic": "low_idle.lambda > 1.05 && low_idle.o2 > 2.0 && low_idle.co < 0.4 && low_idle.co2 < 13.0 && low_idle.hc < 500",
        "health_score": 60,
        "verdict": "Lean exhaust with high O2 and low CO/HC indicates too much air or insufficient fuel.",
        "action": "Check for vacuum leaks, fuel pressure, and MAF accuracy.",
        "confidence_boosters": {"base_confidence": 0.65}
    },
    # Vacuum leak patterns
    {
        "case_id": "vacuum_leak_differential_high_idle",
        "name": "Intake Vacuum Leak",
        "logic": "low_idle.lambda > 1.05 && high_idle.lambda < 1.02 && low_idle.o2 > 1.5 && high_idle.o2 < 1.0",
        "health_score": 65,
        "verdict": "Lean at low idle but normal at high idle confirms unmetered air at idle only.",
        "action": "Smoke test intake manifold, check vacuum hoses, brake booster, PCV valve, and throttle body gasket.",
        "confidence_boosters": {"base_confidence": 0.7}
    },
    {
        "case_id": "P_001",
        "name": "Intake Vacuum Leak",
        "logic": "low_idle.lambda > 1.08 && low_idle.o2 > 2.0 && low_idle.stft > 15",
        "health_score": 60,
        "verdict": "Significant positive fuel trims and high O2 indicate unmetered air entering intake.",
        "action": "Inspect intake manifold gaskets, vacuum hoses, brake booster, and PCV system.",
        "confidence_boosters": {"base_confidence": 0.65}
    },
    {
        "case_id": "pattern_010",
        "name": "Intake Vacuum Leak",
        "logic": "low_idle.lambda > 1.06 && low_idle.o2 > 1.8 && low_idle.co < 0.5 && low_idle.hc < 200",
        "health_score": 62,
        "verdict": " intake leak indicated by high O2 and lean lambda with low CO/HC.",
        "action": "Check all vacuum lines and intake gaskets for cracks/leaks.",
        "confidence_boosters": {"base_confidence": 0.65}
    },
    {
        "case_id": "vacuum_leak_differential",
        "name": "Intake Vacuum Leak",
        "logic": "low_idle.lambda > 1.08 && low_idle.o2 > 2.0 && low_idle.co < 0.4 && low_idle.hc < 200",
        "health_score": 62,
        "verdict": "High O2 and lean lambda indicate unmetered air entering intake.",
        "action": "Smoke test intake system for leaks.",
        "confidence_boosters": {"base_confidence": 0.65}
    },
    # Healthy engine
    {
        "case_id": "P_100",
        "name": "Healthy Engine",
        "logic": "0.99 <= low_idle.lambda <= 1.01 && low_idle.co < 0.3 && low_idle.hc < 60",
        "health_score": 100,
        "verdict": "Combustion and conversion are operating at peak efficiency.",
        "action": "No action required. Maintain regular service intervals.",
        "confidence_boosters": {
          "base_confidence": 0.9,
          "trim_match_weight": 0.05
        }
    }
]

kb['diagnostic_matrix'] = fresh_matrix

with open(kb_path, 'w') as f:
    json.dump(kb, f, indent=2)

print(f"Replace entire matrix with {len(fresh_matrix)} cases.")
print("Matrix completely refreshed with refined logics and proper ordering.")
