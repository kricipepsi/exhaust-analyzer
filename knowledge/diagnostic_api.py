"""
Automotive Diagnostic Interpretation API
Provides advanced diagnostic functions for exhaust gas analysis.
"""

import sqlite3
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import os

# Database path - relative to this file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagnostics.db")

# ============================================
# DATA CLASSES
# ============================================

@dataclass
class GasReadings:
    """Exhaust gas measurements at a specific engine state."""
    co: float  # % volume
    hc: int    # ppm
    co2: float  # % volume
    o2: float   # % volume
    lambda_val: float  # air-fuel ratio / 14.7
    nox: int = 0  # ppm (optional)
    rpm: int = 800  # engine speed during measurement
    engine_load: float = 0.0  # percent load if known

@dataclass
class DiagnosticResult:
    """Result of diagnostic interpretation."""
    pass_fail: Dict[str, bool]
    violations: List[str]
    probable_causes: List[Dict]
    recommended_tests: List[Dict]
    pattern_matches: List[Dict]
    timestamp: str

# ============================================
# DATABASE HELPERS
# ============================================

def get_db():
    return sqlite3.connect(DB_PATH)

# ============================================
# EMISSION STANDARDS CHECK
# ============================================

def check_emission_compliance(vehicle_category: str, gas: GasReadings) -> Tuple[bool, List[str], Dict]:
    """Check if gas readings meet MOT emission standards for vehicle category."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT test_type, limits FROM emission_standards
        WHERE vehicle_category = ? AND is_active = 1
        ORDER BY id
    """, (vehicle_category,))

    standards = cur.fetchall()
    conn.close()

    if not standards:
        return True, [], {}

    violations = []
    pass_fail = {}
    standards_used = {}

    for test_type, limits_json in standards:
        limits = json.loads(limits_json)
        standards_used[test_type] = limits
        test_passed = True

        if test_type == "fast_idle":
            if gas.co > limits.get("co_max", 999):
                violations.append(f"CO too high at fast idle: {gas.co}% > {limits['co_max']}%")
                test_passed = False
            if gas.hc > limits.get("hc_max", 99999):
                violations.append(f"HC too high at fast idle: {gas.hc} ppm > {limits['hc_max']} ppm")
                test_passed = False
            if gas.lambda_val < limits.get("lambda_min", 0):
                violations.append(f"Lambda too low at fast idle: {gas.lambda_val} < {limits['lambda_min']}")
                test_passed = False
            if gas.lambda_val > limits.get("lambda_max", 999):
                violations.append(f"Lambda too high at fast idle: {gas.lambda_val} > {limits['lambda_max']}")
                test_passed = False
            pass_fail["fast_idle"] = test_passed

        elif test_type == "normal_idle":
            if gas.co > limits.get("co_max", 999):
                violations.append(f"CO too high at normal idle: {gas.co}% > {limits['co_max']}%")
                test_passed = False
            pass_fail["normal_idle"] = test_passed

        elif test_type == "fast_acceleration" and vehicle_category == "diesel":
            pass_fail["smoke"] = True

    overall_pass = all(pass_fail.values()) if pass_fail else True
    return overall_pass, violations, standards_used

# ============================================
# DIAGNOSTIC PATTERN MATCHING
# ============================================

def match_diagnostic_patterns(
    gas: GasReadings,
    dtc_codes: List[str],
    vehicle_category: str = None,
    min_confidence: float = 0.3
) -> List[Dict]:
    """Query diagnostic_patterns table for patterns matching gas profile and DTCs."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT pattern_name, domain_id, exhaust_gas_profile, fuel_trim_conditions,
               dtc_codes, likely_causes, recommended_tests, pass_fail_criteria,
               confidence, source
        FROM diagnostic_patterns
        WHERE is_active = 1
    """)

    patterns = []
    for row in cur.fetchall():
        pattern = {
            "pattern_name": row[0],
            "domain_id": row[1],
            "exhaust_gas_profile": json.loads(row[2]) if row[2] else {},
            "fuel_trim_conditions": json.loads(row[3]) if row[3] else {},
            "dtc_codes": json.loads(row[4]) if row[4] else [],
            "likely_causes": json.loads(row[5]) if row[5] else [],
            "recommended_tests": json.loads(row[6]) if row[6] else [],
            "pass_fail_criteria": json.loads(row[7]) if row[7] else {},
            "base_confidence": row[8],
            "source": row[9]
        }
        patterns.append(pattern)

    conn.close()

    matches = []
    for pattern in patterns:
        score = 0.0
        max_possible = 0.0

        profile = pattern["exhaust_gas_profile"]
        for gas_name, condition in profile.items():
            max_possible += 1
            actual_val = getattr(gas, gas_name.lower(), None)
            if actual_val is None:
                continue

            cond_str = str(condition).lower()
            if ">" in cond_str:
                try:
                    threshold = float(cond_str.split(">")[1].strip())
                    if actual_val > threshold:
                        score += 1
                except:
                    pass
            elif "<" in cond_str:
                try:
                    threshold = float(cond_str.split("<")[1].strip())
                    if actual_val < threshold:
                        score += 1
                except:
                    pass

        if dtc_codes and pattern["dtc_codes"]:
            max_possible += 1
            matching_codes = [c for c in dtc_codes if c in pattern["dtc_codes"]]
            if matching_codes:
                score += 1

        if max_possible > 0:
            match_ratio = score / max_possible
            final_confidence = match_ratio * pattern["base_confidence"]
        else:
            final_confidence = pattern["base_confidence"]

        if final_confidence >= min_confidence:
            matches.append({
                "pattern_name": pattern["pattern_name"],
                "confidence": round(final_confidence, 3),
                "likely_causes": pattern["likely_causes"],
                "recommended_tests": pattern["recommended_tests"],
                "source": pattern["source"]
            })

    matches.sort(key=lambda x: x["confidence"], reverse=True)
    return matches

# ============================================
# FUEL TRIM INTERPRETATION
# ============================================

def interpret_fuel_trim(stft: float, ltft: float) -> Dict:
    """Interpret short-term and long-term fuel trim values."""
    result = {
        "stft_condition": None,
        "ltft_condition": None,
        "overall_diagnosis": None,
        "likely_causes": [],
        "notes": ""
    }

    if stft > 10:
        result["stft_condition"] = "high_positive"
        result["likely_causes"].append("Vacuum leak (unmetered air)")
    elif stft < -10:
        result["stft_condition"] = "high_negative"
        result["likely_causes"].append("Rich condition (over-fueling or under-reporting airflow)")

    if ltft > 15:
        result["ltft_condition"] = "high_positive"
        if stft > 10:
            result["overall_diagnosis"] = "lean_condition"
            result["likely_causes"].extend([
                "Vacuum leak", "MAF sensor over-reporting", "Weak fuel pump", "Clogged fuel filter"
            ])
        else:
            result["overall_diagnosis"] = "lean_learned"
            result["notes"] = "ECU has learned to compensate for lean condition"
    elif ltft < -15:
        result["ltft_condition"] = "high_negative"
        if stft < -10:
            result["overall_diagnosis"] = "rich_condition"
            result["likely_causes"].extend([
                "Faulty MAF (under-reporting)", "High fuel pressure", "Leaking injector"
            ])
        else:
            result["overall_diagnosis"] = "rich_learned"
    else:
        result["ltft_condition"] = "normal"
        if not result["overall_diagnosis"]:
            result["overall_diagnosis"] = "within_normal_range"

    return result

# ============================================
# MAIN INTERPRETATION FUNCTION
# ============================================

def analyze_emissions(
    vehicle_category: str,
    gas_readings: Dict,
    dtc_codes: List[str] = None,
    fuel_trims: Dict = None
) -> DiagnosticResult:
    """
    Comprehensive emissions diagnostic analysis.

    Args:
        vehicle_category: 'petrol_catalyst', 'petrol_non_catalyst', 'diesel'
        gas_readings: dict with co, hc, co2, o2, lambda_val, nox (optional)
        dtc_codes: list of OBD-II trouble codes
        fuel_trims: dict with stft, ltft (percentages)

    Returns:
        DiagnosticResult dataclass
    """
    gas = GasReadings(**gas_readings)
    dtc_codes = dtc_codes or []
    fuel_trims = fuel_trims or {}

    violations = []
    pass_fail = {}

    # 1. Emission compliance check
    overall_pass, std_violations, standards = check_emission_compliance(vehicle_category, gas)
    violations.extend(std_violations)
    pass_fail["emission_standards"] = overall_pass

    # 2. Diagnostic pattern matching
    pattern_matches = match_diagnostic_patterns(gas, dtc_codes, vehicle_category)

    # 3. Fuel trim interpretation
    ft_interpretation = None
    if fuel_trims:
        ft_interpretation = interpret_fuel_trim(fuel_trims.get("stft", 0), fuel_trims.get("ltft", 0))
        if ft_interpretation["overall_diagnosis"] not in ["within_normal_range", "normal"]:
            violations.append(f"Fuel trim issue: {ft_interpretation['overall_diagnosis']}")
            pass_fail["fuel_trim"] = False

    # 4. Aggregate recommended tests
    recommended_tests = []
    seen = set()
    for match in pattern_matches[:3]:
        for test in match["recommended_tests"]:
            if isinstance(test, dict):
                name = test.get("procedure_name", test.get("name", "Unknown"))
                if name not in seen:
                    recommended_tests.append(test)
                    seen.add(name)
            elif isinstance(test, str) and test not in seen:
                recommended_tests.append({"procedure_name": test, "description": ""})
                seen.add(test)

    # 5. Probable causes (deduplicated, ranked)
    probable_causes = []
    for match in pattern_matches[:5]:
        for cause in match["likely_causes"]:
            if not any(pc["cause"] == cause for pc in probable_causes):
                probable_causes.append({
                    "cause": cause,
                    "confidence": match["confidence"],
                    "source_pattern": match["pattern_name"],
                    "supporting_dtcs": [c for c in dtc_codes if c in match.get("dtc_codes", [])]
                })
    probable_causes.sort(key=lambda x: x["confidence"], reverse=True)

    return DiagnosticResult(
        pass_fail=pass_fail,
        violations=violations,
        probable_causes=probable_causes[:10],
        recommended_tests=recommended_tests[:10],
        pattern_matches=pattern_matches[:5],
        timestamp=datetime.now().isoformat()
    )

# ============================================
# CONVENIENCE FUNCTIONS
# ============================================

def get_dtc_info(dtc_code: str) -> Optional[Dict]:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT code, description, category, severity, causes, symptoms
        FROM dtc_codes WHERE code = ? AND is_active = 1
    """, (dtc_code.upper(),))
    row = cur.fetchone()
    conn.close()

    if row:
        return {
            "code": row[0],
            "description": row[1],
            "category": row[2],
            "severity": row[3],
            "causes": json.loads(row[4]) if row[4] else [],
            "symptoms": json.loads(row[5]) if row[5] else []
        }
    return None
