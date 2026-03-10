#!/usr/bin/env python3
"""
Comprehensive Knowledge Extraction from avto-2 study materials
Integrates new diagnostic patterns, test procedures, sensor specs, DTCs, and raw knowledge
into the exhaust-analyzer knowledge base (diagnostics.db)
"""

import os
import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# --- Configuration ---
AVTO2_DIR = r"C:\Users\asus\Documents\avto-2"
DB_PATH = r"C:\Users\asus\.openclaw\workspace\exhaust-analyzer\knowledge\diagnostics.db"

# Logging
LOG_FILE = Path("avto2_extraction_log.txt")

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

# --- Database helpers ---
def get_db():
    return sqlite3.connect(DB_PATH)

def get_domain_id(conn, code: str) -> Optional[int]:
    cur = conn.cursor()
    cur.execute("SELECT id FROM knowledge_domains WHERE code = ?", (code,))
    row = cur.fetchone()
    return row[0] if row else None

def add_knowledge_entry(conn, domain_id: int, title: str, content: str, source: str, tags: List[str] = None):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO knowledge_entries (domain_id, title, content, source, tags, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (domain_id, title, content, source, json.dumps(tags or []), True)
    )
    return cur.lastrowid

def add_diagnostic_pattern(conn, pattern_data: Dict) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO diagnostic_patterns (
            pattern_name, domain_id, exhaust_gas_profile, sensor_readings,
            fuel_trim_conditions, dtc_codes, likely_causes, recommended_tests,
            pass_fail_criteria, common_mistakes, confidence, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            pattern_data["pattern_name"],
            pattern_data["domain_id"],
            json.dumps(pattern_data.get("exhaust_gas_profile", {})),
            json.dumps(pattern_data.get("sensor_readings", {})),
            json.dumps(pattern_data.get("fuel_trim_conditions", {})),
            json.dumps(pattern_data.get("dtc_codes", [])),
            json.dumps(pattern_data.get("likely_causes", [])),
            json.dumps(pattern_data.get("recommended_tests", [])),
            pattern_data.get("pass_fail_criteria", ""),
            pattern_data.get("common_mistakes", ""),
            pattern_data.get("confidence", 0.7),
            pattern_data.get("source", "")
        )
    )
    return cur.lastrowid

def add_test_procedure(conn, proc: Dict) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO test_procedures (
            procedure_name, component, test_type, purpose,
            required_tools, steps, pass_criteria, fail_criteria,
            safety_notes, time_estimate_min, difficulty, source,
            is_active, mot_section, is_mandatory
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            proc["procedure_name"],
            proc.get("component", "general"),
            proc.get("test_type", "functional"),
            proc.get("purpose", ""),
            json.dumps(proc.get("required_tools", [])),
            proc.get("steps", ""),
            proc.get("pass_criteria", ""),
            proc.get("fail_criteria", ""),
            proc.get("safety_notes", ""),
            proc.get("time_estimate_min", 30),
            proc.get("difficulty", "intermediate"),
            proc.get("source", ""),
            True,
            proc.get("mot_section", ""),
            proc.get("is_mandatory", False)
        )
    )
    return cur.lastrowid

def add_sensor_spec(conn, spec: Dict) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO sensor_specifications (
            sensor_name, sensor_type, description,
            voltage_range_min, voltage_range_max, voltage_typical,
            frequency_min, frequency_max, frequency_typical,
            impedance_min, impedance_max, response_time_ms,
            heater_control, expected_values_json, thresholds_json,
            typical_failures, test_procedures, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            spec["sensor_name"],
            spec["sensor_type"],
            spec.get("description", ""),
            spec.get("voltage_range_min"),
            spec.get("voltage_range_max"),
            spec.get("voltage_typical"),
            spec.get("frequency_min"),
            spec.get("frequency_max"),
            spec.get("frequency_typical"),
            spec.get("impedance_min"),
            spec.get("impedance_max"),
            spec.get("response_time_ms"),
            spec.get("heater_control", False),
            json.dumps(spec.get("expected_values", {})),
            json.dumps(spec.get("thresholds", {})),
            json.dumps(spec.get("typical_failures", [])),
            json.dumps(spec.get("test_procedures", [])),
            spec.get("source", "")
        )
    )
    return cur.lastrowid

def add_dtc(conn, dtc: Dict) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO dtc_codes (
            code, code_type, description, category, severity,
            applicable_systems, causes, symptoms, reference_data, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dtc["code"],
            dtc.get("code_type", "generic_p"),
            dtc.get("description", ""),
            dtc.get("category", "uncategorized"),
            dtc.get("severity", "moderate"),
            json.dumps(dtc.get("applicable_systems", [])),
            json.dumps(dtc.get("causes", [])),
            json.dumps(dtc.get("symptoms", [])),
            json.dumps(dtc.get("reference_data", {})),
            dtc.get("source", "")
        )
    )
    return cur.lastrowid

# --- Parser functions per file type ---

def parse_oxygen_sensor_info(text: str, filename: str) -> Dict[str, List]:
    """Extract O2 sensor specifications and test procedures."""
    patterns = []
    procedures = []
    specs = []
    dtcs = []

    # Extract DTC patterns for O2 sensors (P0130-P0164 series)
    dtc_ranges = {
        "P0130": "O2 sensor circuit malfunction (Bank 1 Sensor 1)",
        "P0131": "O2 sensor circuit low voltage (Bank 1 Sensor 1)",
        "P0132": "O2 sensor circuit high voltage (Bank 1 Sensor 1)",
        "P0133": "O2 sensor circuit slow response (Bank 1 Sensor 1)",
        "P0134": "O2 sensor circuit no activity (Bank 1 Sensor 1)",
        "P0135": "O2 sensor heater circuit (Bank 1 Sensor 1)",
        "P0140": "O2 sensor circuit malfunction (Bank 1 Sensor 2)",
        "P0141": "O2 sensor heater circuit (Bank 1 Sensor 2)",
        "P0150": "O2 sensor circuit malfunction (Bank 2 Sensor 1)",
        "P0155": "O2 sensor heater circuit (Bank 2 Sensor 1)",
        "P0160": "O2 sensor circuit malfunction (Bank 2 Sensor 2)",
        "P0161": "O2 sensor heater circuit (Bank 2 Sensor 2)",
    }
    for code, desc in dtc_ranges.items():
        dtcs.append({
            "code": code,
            "code_type": "generic_p",
            "description": desc,
            "category": "o2_sensor",
            "severity": "moderate",
            "applicable_systems": ["oxygen_sensor"],
            "causes": [],
            "symptoms": [],
            "source": filename
        })

    # Extract wideband specific info
    if "wideband" in filename.lower():
        specs.append({
            "sensor_name": "O2_sensor_wideband",
            "sensor_type": "gas_concentration",
            "description": "Wideband oxygen sensor provides true air-fuel ratio measurement over a wide range (typically 0.5-2.0 lambda). Uses a pumping cell to maintain reference chamber at stoichiometry.",
            "voltage_range_min": 0.1,
            "voltage_range_max": 4.9,
            "voltage_typical": 2.5,
            "response_time_ms": 50,  # typically faster than narrowband
            "expected_values": {
                "afr_range": "0.5-2.0 lambda",
                "lambda_display": "0.5-2.0",
                "pump_current": "varies with AFR"
            },
            "thresholds": {
                "lean_limit": "lambda > 1.2 may cause overheating",
                "rich_limit": "lambda < 0.8 may cause soot"
            },
            "typical_failures": [
                "Pump cell degradation",
                "Reference cell drift",
                "Heater failure",
                "Contamination from leaded fuel"
            ],
            "source": filename
        })

        # Add wideband test procedure
        procedures.append({
            "procedure_name": "Wideband O2 Sensor Calibration Check",
            "component": "wideband_oxygen_sensor",
            "test_type": "calibration",
            "purpose": "Verify wideband sensor accuracy and calibration",
            "required_tools": ["wideband_analyzer", "calibration_air_cell", "lambda_target_gas"],
            "steps": "1. Power up wideband controller and allow warm-up (5-10 min). 2. Perform air calibration (0% fuel, clean air). 3. Perform span calibration using known AFR gas (typically 14.7:1). 4. Check sensor heater resistance. 5. Run self-test if available.",
            "pass_criteria": "Calibration passes; sensor reading within ±0.1 lambda of target",
            "fail_criteria": "Calibration fails, heater circuit fault, or sensor slow response",
            "time_estimate_min": 20,
            "difficulty": "intermediate",
            "source": filename
        })

    # Narrowband spec (if info present)
    if "narrowband" in filename.lower() or "oxygen-sensor-information" in filename.lower():
        specs.append({
            "sensor_name": "O2_sensor_narrowband",
            "sensor_type": "oxygen",
            "description": "Standard zirconia O2 sensor; switches between ~0.1V (rich) and ~0.9V (lean) around stoichiometry. Used for closed-loop fuel control.",
            "voltage_range_min": 0.1,
            "voltage_range_max": 0.9,
            "voltage_typical": 0.45,
            "response_time_ms": 100,
            "expected_values": {
                "switching_frequency": "8-12 Hz at steady RPM",
                "voltage_sine_wave": "0.1-0.9V AC",
                "lambda_target": "0.97-1.03"
            },
            "thresholds": {
                "stuck_rich": "voltage >0.6V constant",
                "stuck_lean": "voltage <0.4V constant",
                "no_switching": "voltage steady"
            },
            "typical_failures": [
                "Contamination (lead, silicone, phosphorus)",
                "Heater element failure",
                "Wiring open/short",
                "Slow response due to aging"
            ],
            "source": filename
        })

        # Add switching test procedure
        procedures.append({
            "procedure_name": "Narrowband O2 Sensor Switching Frequency Test",
            "component": "oxygen_sensor",
            "test_type": "electrical",
            "purpose": "Verify O2 sensor voltage switching rate indicates proper mixture control",
            "required_tools": ["O2_sensor_tester", "multimeter", "lab_scope"],
            "steps": "1. Connect meter to O2 signal wire. 2. Warm engine and hold steady at 2500 RPM. 3. Observe voltage switching between ~0.1-0.9V. 4. Count switch cycles per second (ideally 8-12 Hz).",
            "pass_criteria": "Switching frequency >8 Hz at constant RPM; voltage swings full range",
            "fail_criteria": "Slow switching, stuck rich/lean, or no switching",
            "time_estimate_min": 15,
            "difficulty": "intermediate",
            "source": filename
        })

    return {"patterns": patterns, "procedures": procedures, "specs": specs, "dtcs": dtcs}

def parse_fuel_trim_analysis(text: str, filename: str) -> Dict[str, List]:
    """Extract fuel trim patterns and test procedures."""
    patterns = []
    procedures = []
    domain_id = None  # will be set by caller

    # Pattern: Rich condition (positive trims)
    patterns.append({
        "pattern_name": "fuel_trim_rich_indication",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "FUEL_TRIM"),
        "exhaust_gas_profile": {"co": "high", "hc": "high", "o2": "low", "lambda": "low"},
        "sensor_readings": {"stft": ">+10%", "ltft": ">+10%"},
        "dtc_codes": ["P0172", "P0175"],
        "likely_causes": [
            "Fuel pressure too high (bad regulator, restricted return)",
            "Leaking or stuck open injectors",
            "Faulty MAF sensor (under-reporting airflow)",
            "Bad coolant temp sensor (cold reading → enrich)",
            "Exhaust restriction (catalyst clog) causing backpressure"
        ],
        "recommended_tests": ["fuel_pressure_test", "injector_leak_test", "maf_sensor_analysis"],
        "confidence": 0.8,
        "source": filename
    })

    # Pattern: Lean condition (negative trims)
    patterns.append({
        "pattern_name": "fuel_trim_lean_indication",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "FUEL_TRIM"),
        "exhaust_gas_profile": {"co": "low", "o2": "high", "hc": "high_misfire", "nox": "high"},
        "sensor_readings": {"stft": "<-5%", "ltft": "<-5%"},
        "dtc_codes": ["P0171", "P0174"],
        "likely_causes": [
            "Vacuum leak (intake manifold gasket, hoses, throttle body)",
            "Weak fuel pump or clogged filter",
            "Faulty fuel pressure regulator (low pressure)",
            "Dirty/blocked fuel Injector (low flow)",
            "Faulty MAF (over-reporting airflow)",
            "Exhaust leak upstream of O2 sensor"
        ],
        "recommended_tests": ["vacuum_leak_test", "fuel_pressure_test", "maf_voltage_check"],
        "confidence": 0.8,
        "source": filename
    })

    # Procedure: Fuel trim analysis test
    procedures.append({
        "procedure_name": "Fuel Trim Diagnostic Procedure",
        "component": "fuel_control",
        "test_type": "analysis",
        "purpose": "Interpret short-term and long-term fuel trims to diagnose lean/rich conditions",
        "required_tools": ["scan_tool"],
        "steps": "1. Connect scan tool and live data. 2. View STFT and LTFT at idle, 1500 RPM, and under light load. 3. Note values and trends. 4. Positive trims indicate ECU adding fuel (lean condition); negative trims indicate ECU reducing fuel (rich condition). 5. Compare to specifications (typically ±10% is acceptable).",
        "pass_criteria": "STFT and LTFT within ±10% of each other and within ±10% of zero; no significant discrepancy between banks",
        "fail_criteria": "Trims >20% positive or negative, or large difference between STFT and LTFT, or one bank significantly different from the other",
        "time_estimate_min": 20,
        "difficulty": "basic",
        "source": filename
    })

    return {"patterns": patterns, "procedures": procedures, "specs": [], "dtcs": []}

def parse_misfire_diagnosis(text: str, filename: str) -> Dict[str, List]:
    """Extract misfire patterns, test procedures."""
    patterns = []
    procedures = []

    # Pattern: Ignition-related misfire
    patterns.append({
        "pattern_name": "misfire_ignition_failure",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "MISFIRE_DIAGNOSIS"),
        "exhaust_gas_profile": {"hc": "very_high", "co": "low", "o2": "high", "lambda": "erratic"},
        "sensor_readings": {},
        "dtc_codes": ["P0300", "P0301", "P0302", "P0303", "P0304"],
        "likely_causes": [
            "Worn or fouled spark plugs",
            "Failed ignition coil(s)",
            "Ignition wires (high resistance, arcing)",
            "Damaged distributor cap/rotor (if applicable)",
            "Failed ignition control module"
        ],
        "recommended_tests": ["spark_tester_analysis", "coil_resistance_check", "wires_resistance_check", "compression_test"],
        "confidence": 0.9,
        "source": filename
    })

    # Pattern: Fuel-related misfire
    patterns.append({
        "pattern_name": "misfire_fuel_delivery",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "MISFIRE_DIAGNOSIS"),
        "exhaust_gas_profile": {"hc": "high", "co": "low_or_fluctuating", "o2": "high"},
        "sensor_readings": {},
        "dtc_codes": ["P0300-P0304"],
        "likely_causes": [
            "Clogged or failed fuel injector",
            "Low fuel pressure (weak pump, clogged filter)",
            "Contaminated fuel (water, dirt)",
            "Incorrect injector pulse width (ECU driver issue)"
        ],
        "recommended_tests": ["injector_flow_test", "fuel_pressure_test", "injector_balance_test"],
        "confidence": 0.8,
        "source": filename
    })

    # Pattern: Mechanical misfire
    patterns.append({
        "pattern_name": "misfire_mechanical",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "MISFIRE_DIAGNOSIS"),
        "exhaust_gas_profile": {"hc": "high", "co": "low", "o2": "high", "nox": "low"},
        "sensor_readings": {},
        "dtc_codes": ["P0300-P0304"],
        "likely_causes": [
            "Worn piston rings or cylinder wall",
            "Leaking or burnt valves",
            "Blown head gasket",
            "Worn cam lobe",
            "Incorrect valve timing (belt/chain jumped)"
        ],
        "recommended_tests": ["compression_test", "leak_down_test", "camera_inspection"],
        "confidence": 0.85,
        "source": filename
    })

    # Test procedures from misfire diagnosis
    procedures.extend([
        {
            "procedure_name": "Cylinder Balance Test (Power Balance)",
            "component": "ignition_system",
            "test_type": "functional",
            "purpose": "Identify weak or misfiring cylinder by disabling each cylinder",
            "required_tools": ["scan_tool", "tachometer"],
            "steps": "1. Warm engine. 2. Record idle RPM. 3. Use scan tool to disable each cylinder one at a time. 4. Note RPM drop for each cylinder. A healthy cylinder should drop ~150-200 RPM. Less indicates misfire.",
            "pass_criteria": "All cylinders show similar RPM drop (within 20% of each other)",
            "fail_criteria": "One or more cylinders show significantly lower RPM drop (<100 RPM)",
            "time_estimate_min": 20,
            "difficulty": "intermediate",
            "source": filename
        },
        {
            "procedure_name": "Spark Tester Analysis",
            "component": "ignition_system",
            "test_type": "electrical",
            "purpose": "Visual assessment of spark intensity to find weak ignition",
            "required_tools": ["spark_tester", "screwdriver", "safety_wires"],
            "steps": "1. Remove spark plug wire or coil. 2. Connect spark tester in cylinder hole. 3. Ground tester to engine block. 4. Crank engine and observe spark intensity across cylinders. Compare brightness and consistency.",
            "pass_criteria": "Bright blue/violet spark, consistent across cylinders, jumps 15-20mm gap easily",
            "fail_criteria": "Weak yellow/orange spark, intermittent, or no spark",
            "safety_notes": "Never hold wire by hand; use insulated tools; keep clear of moving parts",
            "time_estimate_min": 30,
            "difficulty": "basic",
            "source": filename
        }
    ])

    return {"patterns": patterns, "procedures": procedures, "specs": [], "dtcs": []}

def parse_map_sensor(text: str, filename: str) -> Dict[str, List]:
    """Extract MAP sensor specifications and troubleshooting patterns."""
    patterns = []
    procedures = []
    specs = []
    dtcs = []

    # MAP sensor spec
    specs.append({
        "sensor_name": "MAP_sensor_absolute",
        "sensor_type": "pressure",
        "description": "Manifold Absolute Pressure sensor; measures atmospheric pressure in intake manifold for engine load calculation. Works with IAT for speed-density fueling.",
        "voltage_range_min": 0.33,
        "voltage_range_max": 4.9,
        "voltage_typical": 2.5,
        "impedance_min": 1000,
        "impedance_max": 5000,
        "expected_values": {
            "supply_voltage": "5V",
            "output_range": "0.33V = high vacuum (~0 bar), 4.9V = atmospheric (~1.013 bar)",
            "barometric_at_ignition": "~4.9V at sea level key-on engine-off",
            "vacuum_at_idle": "drops to ~1.5-2.0V depending on engine load"
        },
        "thresholds": {
            "min_voltage_idle_vacuum": "<2.0V indicates good vacuum",
            "voltage_stuck_at_4.9V": "possible vacuum leak or bad sensor",
            "voltage_stuck_at_low": "sensor or wiring issue"
        },
        "typical_failures": [
            "Sensor stuck (no movement with throttle changes)",
            "IAT sensor integrated failure",
            "Vacuum hose disconnected/leaking",
            "Contaminated with oil (from blow-by)",
            "Wiring short/open"
        ],
        "test_procedures": ["map_voltage_vacuum_correlation", "scan_data_comparison"],
        "source": filename
    })

    # Pattern: MAP sensor out of range
    patterns.append({
        "pattern_name": "map_sensor_out_of_range",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "SENSORS"),
        "exhaust_gas_profile": {},  # not directly exhaust gases
        "sensor_readings": {"map_voltage": "out of spec", "maf_voltage": "inconsistent"},
        "dtc_codes": ["P0106", "P0107", "P0108"],
        "likely_causes": [
            "MAP sensor electrical failure (short, open)",
            "Vacuum hose cracked/blocked",
            "Sensor diaphragm damage",
            "Incorrect sensor for application"
        ],
        "recommended_tests": ["map_voltage_check_at_known_vacuum", "compare_to_maf_data", "sensor_resistance_test"],
        "confidence": 0.8,
        "source": filename
    })

    # Procedure: MAP sensor voltage vs vacuum test
    procedures.append({
        "procedure_name": "MAP Sensor Voltage vs Vacuum Test",
        "component": "map_sensor",
        "test_type": "electrical",
        "purpose": "Verify MAP sensor output voltage changes correctly with manifold vacuum",
        "required_tools": ["multimeter", "vacuum_pump", "scan_tool"],
        "steps": "1. Connect scan tool to read MAP voltage/PID. 2. With engine off, key ON, record voltage (should be ~4.9V at sea level). 3. Start engine and let idle; note voltage (should drop to 1.5-2.0V). 4. Apply vacuum to sensor with hand pump and observe voltage decrease linearly. 5. Compare to manufacturer graph.",
        "pass_criteria": "Voltage decreases smoothly as vacuum increases; values match specification within ±0.2V",
        "fail_criteria": "Voltage stuck, erratic, or out of range at known vacuum levels",
        "time_estimate_min": 20,
        "difficulty": "intermediate",
        "source": filename
    })

    return {"patterns": patterns, "procedures": procedures, "specs": specs, "dtcs": dtcs}

def parse_elm327_datasheet(text: str, filename: str) -> Dict[str, List]:
    """Extract OBD-II interface information and protocol details."""
    dtcs = []
    procedures = []

    # Extract common OBD-II PIDs and parameters
    # Not directly diagnostic patterns but can add as knowledge entries

    # Procedure: Using ELM327 for basic diagnostics
    procedures.append({
        "procedure_name": "ELM327 OBD-II Interface Basic Usage",
        "component": "obd_interface",
        "test_type": "communication",
        "purpose": "Connect to vehicle OBD-II port and retrieve diagnostic data",
        "required_tools": ["ELM327_adapter", "OBD2_software", "laptop_or_phone"],
        "steps": "1. Plug adapter into vehicle OBD-II port (under dash). 2. Pair or connect via USB/Bluetooth. 3. Launch terminal or app. 4. Initialize with 'ATZ' (reset), 'ATSP0' (auto protocol). 5. Read DTCs with '03' (store) or '07' (pending). 6. Clear codes with '04'. 7. Read live data with '01 0C' (RPM), '01 05' ( coolant temp), etc.",
        "pass_criteria": "Adapter responds 'OK' to commands; can retrieve VIN, DTCs, and live parameters",
        "fail_criteria": "No communication, 'NO DATA' responses, or repeated 'UNABLE TO CONNECT'",
        "time_estimate_min": 15,
        "difficulty": "basic",
        "source": filename
    })

    return {"patterns": [], "procedures": procedures, "specs": [], "dtcs": []}

def parse_wideband_vs_narrow(text: str, filename: str) -> Dict[str, List]:
    """Compare wideband and narrowband O2 sensors."""
    specs = []
    procedures = []

    specs.append({
        "sensor_name": "O2_sensor_narrowband",
        "sensor_type": "oxygen",
        "description": "Standard zirconia sensor; outputs ~0.1-0.9V rich/lean switch; narrow range around stoichiometry; good for fuel trim but not absolute AFR.",
        "voltage_range_min": 0.1,
        "voltage_range_max": 0.9,
        "voltage_typical": 0.45,
        "response_time_ms": 100,
        "expected_values": {
            "lambda_switch_range": "0.97-1.03",
            "output_signal": "0.1V (lean) -> 0.9V (rich)"
        },
        "thresholds": {},
        "typical_failures": ["contamination", "heater_failure"],
        "source": filename
    })

    specs.append({
        "sensor_name": "O2_sensor_wideband",
        "sensor_type": "gas_concentration",
        "description": "Wideband sensor uses pumping cell to measure actual AFR across 0.5-2.0 lambda; accurate for tuning; requires dedicated controller.",
        "voltage_range_min": 0.1,
        "voltage_range_max": 4.9,
        "voltage_typical": 2.5,
        "response_time_ms": 50,
        "expected_values": {
            "lambda_range": "0.5-2.0",
            "output_signal": "linear voltage or digital"
        },
        "thresholds": {},
        "typical_failures": ["pump_cell_degradation", "reference_cell_drift"],
        "source": filename
    })

    procedures.append({
        "procedure_name": "Choosing between Narrowband and Wideband",
        "component": "oxygen_sensor",
        "test_type": "selection",
        "purpose": "Know when to use narrowband vs wideband for diagnostics and tuning",
        "required_tools": [],
        "steps": "Narrowband: sufficient for basic fuel trim monitoring; detects rich/lean but not exact AFR. Wideband: needed for precise AFR tuning, diesel particulate filter diagnostics, and lean-burn engines. Use wideband for advanced diagnostics and performance tuning.",
        "pass_criteria": "Correct sensor type selected for application",
        "fail_criteria": "Using narrowband for precise AFR work; using wideband on a system not designed for it without proper controller",
        "time_estimate_min": 10,
        "difficulty": "basic",
        "source": filename
    })

    return {"patterns": [], "procedures": procedures, "specs": specs, "dtcs": []}

def parse_spark_burn_time(text: str, filename: str) -> Dict[str, List]:
    """Extract spark burn time diagnostic patterns and procedure."""
    patterns = []
    procedures = []

    # Pattern: Short spark burn time
    patterns.append({
        "pattern_name": "spark_burn_time_short",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "IGNITION_DIAGNOSIS"),
        "exhaust_gas_profile": {"hc": "high", "co": "may_be_high"},
        "sensor_readings": {},
        "dtc_codes": ["P0321", "P0322", "P0323", "P0325", "P0327", "P0328"],
        "likely_causes": [
            "High secondary circuit resistance (spark plug gap too wide, cracked plug, HT lead damage)",
            "Weak coil output (low primary voltage, failing coil)",
            "Shorted spark plug (cracked insulator, carbon track)"
        ],
        "recommended_tests": ["spark_burn_time_measurement", "secondary_resistance_test", "coil_primary_resistance", "spark_plug_inspection"],
        "confidence": 0.75,
        "source": filename
    })

    # Pattern: Long spark burn time
    patterns.append({
        "pattern_name": "spark_burn_time_long",
        "domain_id": get_domain_id(sqlite3.connect(DB_PATH), "IGNITION_DIAGNOSIS"),
        "exhaust_gas_profile": {"hc": "high", "co": "may_be_low"},
        "sensor_readings": {},
        "dtc_codes": ["P0321", "P0325"],
        "likely_causes": [
            "Open secondary circuit (broken wire, disconnected plug)",
            " Excessive resistance in primary circuit (corroded connections, failing control module)",
            "Failing ignition control module (low dwell time)"
        ],
        "recommended_tests": ["spark_burn_time_measurement", "primary_resistance_test", "coil_electrical_test"],
        "confidence": 0.7,
        "source": filename
    })

    procedures.append({
        "procedure_name": "Spark Burn Time Measurement",
        "component": "ignition_system",
        "test_type": "electrical",
        "purpose": "Assess secondary ignition system health by measuring spark arc duration",
        "required_tools": ["spark_tester_with_timing_light", "lab_scope", "amplified_sensor"],
        "steps": "1. Connect spark tester to cylinder and scope to measure burn duration. 2. Observe waveform: time from voltage peak to collapse. 3. Compare across cylinders. 4. Typical burn time: 1-2 ms. Shorter or longer indicates problem.",
        "pass_criteria": "Burn time within 1-2 ms for all cylinders; similar across cylinders",
        "fail_criteria": "Burn time <0.5 ms (high resistance/shorted) or >3 ms (open/weak coil)",
        "time_estimate_min": 30,
        "difficulty": "advanced",
        "source": filename
    })

    return {"patterns": patterns, "procedures": procedures, "specs": [], "dtcs": []}

def parse_advanced_fault_diagnosis(text: str, filename: str) -> Dict[str, List]:
    """Parse generic advanced fault diagnosis content (e.g., Tom Denton)."""
    patterns = []
    # We'll simply store the whole text as a knowledge entry
    # Could also extract additional patterns with NLP, but manual review best
    return {"patterns": patterns, "procedures": [], "specs": [], "dtcs": []}

def parse_automotive_technology(text: str, filename: str) -> Dict[str, List]:
    """Store large textbook as knowledge entry."""
    return {"patterns": [], "procedures": [], "specs": [], "dtcs": []}

def parse_ase_advanced(text: str, filename: str) -> Dict[str, List]:
    """ASE Advanced Engine Performance study guide."""
    patterns = []
    # Could extract driveability patterns, emission-related patterns
    # For now, store as knowledge entry
    return {"patterns": patterns, "procedures": [], "specs": [], "dtcs": []}

def parse_generic_md(text: str, filename: str) -> Dict[str, List]:
    """Generic markdown parser - store as knowledge entry."""
    return {"patterns": [], "procedures": [], "specs": [], "dtcs": []}

# --- Routing based on filename ---
def route_parser(filename: str):
    low = filename.lower()
    if "oxygen" in low or "o2" in low or "sensor-information" in low:
        return parse_oxygen_sensor_info
    elif "fuel-trim" in low:
        return parse_fuel_trim_analysis
    elif "misfire" in low:
        return parse_misfire_diagnosis
    elif "map" in low:
        return parse_map_sensor
    elif "elm327" in low or "can-test" in low:
        return parse_elm327_datasheet
    elif "wideband" in low:
        return parse_wideband_vs_narrow
    elif "spark-burn" in low:
        return parse_spark_burn_time
    elif "advanced-fault-diagnosis" in low and "2nd" in low:
        return parse_advanced_fault_diagnosis
    elif "automotive-technology" in low:
        return parse_automotive_technology
    elif "ase-advanced" in low:
        return parse_ase_advanced
    elif "timing-advanced" in low or "ignition-timing" in low:
        return parse_misfire_diagnosis  # reuse for now; will refine later
    elif "emission-faults" in low:
        return parse_fuel_trim_analysis  # reuse
    elif "electrical" in low:
        return parse_elm327_datasheet  # reuse for electrical probes/checks
    else:
        return parse_generic_md

# --- Main processing ---
def main():
    conn = get_db()
    log("=== AVTO-2 KNOWLEDGE EXTRACTION STARTED ===")

    files = [f for f in os.listdir(AVTO2_DIR) if f.lower().endswith('.md')]
    log(f"Found {len(files)} markdown files to process")

    total_added = {"patterns": 0, "procedures": 0, "specs": 0, "dtcs": 0, "entries": 0}

    for fname in sorted(files):
        fpath = os.path.join(AVTO2_DIR, fname)
        log(f"\nProcessing: {fname}")
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            log(f"  ERROR reading file: {e}")
            continue

        parser = route_parser(fname)
        try:
            result = parser(text, fname)
            # Insert results
            # Patterns
            for pat in result["patterns"]:
                try:
                    # ensure domain_id
                    pat["domain_id"] = pat.get("domain_id") or get_domain_id(conn, "DIAGNOSTIC_PROCEDURES")
                    add_diagnostic_pattern(conn, pat)
                    total_added["patterns"] += 1
                    log(f"  Stored pattern: {pat['pattern_name']}")
                except Exception as e:
                    log(f"  Error storing pattern: {e}")

            # Procedures
            for proc in result["procedures"]:
                try:
                    add_test_procedure(conn, proc)
                    total_added["procedures"] += 1
                    log(f"  Stored procedure: {proc['procedure_name']}")
                except Exception as e:
                    log(f"  Error storing procedure: {e}")

            # Sensor specs
            for spec in result["specs"]:
                try:
                    add_sensor_spec(conn, spec)
                    total_added["specs"] += 1
                    log(f"  Stored spec: {spec['sensor_name']}")
                except Exception as e:
                    log(f"  Error storing spec: {e}")

            # DTCs
            for dtc in result["dtcs"]:
                try:
                    add_dtc(conn, dtc)
                    total_added["dtcs"] += 1
                    log(f"  Stored DTC: {dtc['code']}")
                except Exception as e:
                    log(f"  Error storing DTC: {e}")

            # If no structured data extracted, store whole document as knowledge entry
            if not any([result["patterns"], result["procedures"], result["specs"], result["dtcs"]]):
                try:
                    # Determine domain based on filename or use "REFERENCE"
                    domain_map = {
                        "automotive-technology": "ENGINE_MECHANICS",
                        "ase-advanced": "EMISSIONS_CONTROL",
                        "electrical-systems": "ELECTRICAL",
                        "can-test-box": "NETWORKS",
                    }
                    domain_code = "REFERENCE"
                    for key, code in domain_map.items():
                        if key in fname.lower():
                            domain_code = code
                            break
                    domain_id = get_domain_id(conn, domain_code) or get_domain_id(conn, "REFERENCE")
                    add_knowledge_entry(conn, domain_id, fname, text, f"avto-2: {fname}", tags=["avto2", "raw"])
                    total_added["entries"] += 1
                    log(f"  Stored full text as knowledge entry (domain: {domain_code})")
                except Exception as e:
                    log(f"  Error storing entry: {e}")

            conn.commit()
        except Exception as e:
            log(f"  FATAL parser error: {e}")
            import traceback
            log(traceback.format_exc())

    conn.close()
    log("\n=== EXTRACTION COMPLETE ===")
    log(f"Total added: {total_added}")
    log(f"Patterns: {total_added['patterns']}, Procedures: {total_added['procedures']}, Specs: {total_added['specs']}, DTCs: {total_added['dtcs']}, Entries: {total_added['entries']}")

if __name__ == "__main__":
    main()
