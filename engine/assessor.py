#!/usr/bin/env python3
"""
Exhaust Gas Diagnostic Engine
Analyzes 5-gas measurements (idle and high idle) to assess engine health.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from knowledge.knowledge_base import (
    NORMAL_IDLE, NORMAL_HIGH_IDLE, THRESHOLDS, FAULT_PATTERNS,
    TABLE_PATTERNS_RAW, get_table_pattern, convert_qualitative_to_indicator
)

@dataclass
class GasReading:
    """Container for a single gas measurement."""
    value: float
    unit: str
    condition: str  # "idle" or "high_idle"

@dataclass
class Deviation:
    gas: str
    measured: float
    normal_min: float
    normal_max: float
    severity: str  # "low", "moderate", "high", "critical"
    direction: str  # "high" or "low"

@dataclass
class MatchedPattern:
    pattern_name: str
    matched_indicators: int
    total_indicators: int
    confidence: float
    culprits: List[str]
    notes: str

class DiagnosticEngine:
    """Core engine for exhaust gas diagnosis."""

    def __init__(self, rpm: int = 800):
        """Initialize with approximate idle rpm (for range selection)."""
        self.rpm = rpm
        self.normal = NORMAL_IDLE if rpm < 1200 else NORMAL_HIGH_IDLE

    def validate_input(self, measurements: Dict[str, float], condition: str) -> Tuple[bool, List[str]]:
        """Check that measurements are numeric and within plausible bounds."""
        errors = []
        for gas, value in measurements.items():
            if not isinstance(value, (int, float)):
                errors.append(f"{gas} must be a number")
                continue
            if value < 0:
                errors.append(f"{gas} cannot be negative")
            if gas == "lambda" and (value < 0.5 or value > 2.0):
                errors.append(f"Lambda {value} out of plausible range (0.5-2.0)")
            if gas == "co" and value > 20:
                errors.append(f"CO {value}% seems too high (check probe)")
            if gas == "co2" and value > 25:
                errors.append(f"CO2 {value}% exceeds normal max")
            if gas == "o2" and value > 25:
                errors.append(f"O2 {value}% exceeds atmospheric levels (~21%)")
            if gas == "hc" and value > 20000:
                errors.append(f"HC {value} ppm seems excessive")
            if gas == "nox" and value > 5000:
                errors.append(f"NOx {value} ppm seems excessive")
        return len(errors) == 0, errors

    def find_deviations(self, measurements: Dict[str, float], condition: str) -> List[Deviation]:
        """Identify which gas readings fall outside normal ranges."""
        deviations = []
        ranges = NORMAL_IDLE if condition == "idle" else NORMAL_HIGH_IDLE
        for gas, norms in ranges.items():
            if gas in measurements:
                val = measurements[gas]
                if val < norms.min or val > norms.max:
                    # Determine severity
                    if gas == "hc" and val > THRESHOLDS["hc_critical"]:
                        severity = "critical"
                    elif gas == "co" and val > THRESHOLDS["co_high"]:
                        severity = "high"
                    elif gas == "o2" and (val < THRESHOLDS["o2_low_rich"] or val > THRESHOLDS["o2_high_lean"]):
                        severity = "high"
                    elif gas == "lambda" and (val < THRESHOLDS["lambda_low_rich"] or val > THRESHOLDS["lambda_high_lean"]):
                        severity = "high"
                    else:
                        severity = "moderate"
                    deviations.append(Deviation(
                        gas=gas,
                        measured=val,
                        normal_min=norms.min,
                        normal_max=norms.max,
                        severity=severity,
                        direction="high" if val > norms.max else "low"
                    ))
        return deviations

    def match_patterns(self, deviations: List[dict], measurements: Dict[str, float]) -> List[MatchedPattern]:
        """Compare observed deviations against known fault patterns.
        deviations: list of dicts with keys: gas, measured, severity, direction
        Returns combined matches from FAULT_PATTERNS and TABLE_PATTERNS_RAW.
        """
        matches = []

        # 1. Match against explicit FAULT_PATTERNS (existing)
        for pattern_name, pattern in FAULT_PATTERNS.items():
            matched = 0
            total = len(pattern["indicators"])
            for indicator_gas, condition in pattern["indicators"].items():
                # Check if this indicator matches
                if indicator_gas == "lambda":
                    val = measurements.get("lambda")
                    if val is not None:
                        if condition == "<0.90" and val < 0.90:
                            matched += 1
                        elif condition == ">1.10" and val > 1.10:
                            matched += 1
                elif indicator_gas == "co":
                    val = measurements.get("co")
                    if val is not None:
                        if condition == ">2.0" and val > 2.0:
                            matched += 1
                        elif condition == "low or irregular" and (val < 0.5 or any(d["gas"]=="co" and d["direction"]=="low" for d in deviations)):
                            matched += 1
                elif indicator_gas == "o2":
                    val = measurements.get("o2")
                    if val is not None:
                        if condition == "<0.5" and val < 0.5:
                            matched += 1
                        elif condition == ">2.0" and val > 2.0:
                            matched += 1
                        elif condition == "moderate" and (0.2 <= val <= 2.0):
                            matched += 1
                        elif condition == "high" and val > 1.5:
                            matched += 1
                elif indicator_gas == "hc":
                    val = measurements.get("hc")
                    if val is not None:
                        if condition == ">2000" and val > 2000:
                            matched += 1
                        elif condition == "high (>200)" and val > 200:
                            matched += 1
                        elif condition == "moderate" and (100 <= val <= 500):
                            matched += 1
                elif indicator_gas == "nox":
                    val = measurements.get("nox")
                    if val is not None:
                        if condition == "high" and val > 200:
                            matched += 1
                        if condition == "low" and val < 100:
                            matched += 1
                        if condition == "variable":
                            matched += 1  # always counts
                # Handle string descriptions (like "slightly low") - these are notes not thresholds
            # If enough indicators match, include this pattern
            if matched >= 1:  # at least one strong indicator
                confidence = matched / total
                matches.append(MatchedPattern(
                    pattern_name=pattern_name,
                    matched_indicators=matched,
                    total_indicators=total,
                    confidence=confidence,
                    culprits=pattern["culprits"],
                    notes=pattern.get("notes", "")
                ))

        # 2. Match against TABLE_PATTERNS_RAW (qualitative table)
        # For each table pattern, convert descriptors to numeric conditions and check against measurements
        for table_key, table_pat in TABLE_PATTERNS_RAW.items():
            matched = 0
            total = len(table_pat)
            for gas, descriptor in table_pat.items():
                # Convert descriptor to a numeric condition (e.g., "hc > 2000")
                cond_str = convert_qualitative_to_indicator(gas, descriptor, condition="idle")
                if not cond_str:
                    continue
                # Parse condition: "gas > value" or "gas < value" or "gas normal"
                parts = cond_str.split()
                if len(parts) < 3:
                    continue
                gas_key = parts[0]
                op = parts[1]
                try:
                    threshold = float(parts[2])
                except ValueError:
                    continue
                val = measurements.get(gas_key)
                if val is None:
                    continue
                # Evaluate
                if op == ">" and val > threshold:
                    matched += 1
                elif op == "<" and val < threshold:
                    matched += 1
                # "~" means within normal; we don't use it for matching (too permissive)
            if matched >= 2:  # require at least 2 indicators to match
                confidence = matched / total
                # Use human-friendly name from table key
                display_name = table_key.replace('_', ' ').title()
                matches.append(MatchedPattern(
                    pattern_name=display_name,
                    matched_indicators=matched,
                    total_indicators=total,
                    confidence=confidence,
                    culprits=[f"Pattern from reference table: {display_name}"],  # generic; user should interpret
                    notes=f"Matched {matched}/{total} gas changes according to tabelagas.xlsx reference."
                ))

        # Deduplicate by pattern_name (keep highest confidence)
        best = {}
        for m in matches:
            if m.pattern_name not in best or m.confidence > best[m.pattern_name].confidence:
                best[m.pattern_name] = m
        return sorted(best.values(), key=lambda x: x.confidence, reverse=True)

    def assess(self, idle_measurements: Dict[str, float], high_idle_measurements: Dict[str, float]) -> Dict:
        """Run full assessment on both idle and high idle data."""
        results = {
            "idle": {},
            "high_idle": {},
            "overall": {
                "deviations": [],
                "patterns": [],
                "health_score": None,
                "recommendations": [],
                "urgent": False,
            },
            # Include raw measurements for charts
            "raw_idle": idle_measurements,
            "raw_high": high_idle_measurements,
        }

        # Validate and assess idle
        valid, errors = self.validate_input(idle_measurements, "idle")
        if not valid:
            results["idle"]["errors"] = errors
        else:
            devs = self.find_deviations(idle_measurements, "idle")
            results["idle"]["deviations"] = [
                {"gas": d.gas, "measured": d.measured, "normal_range": f"{self.normal[d.gas].min}-{self.normal[d.gas].max} {self.normal[d.gas].unit}", "severity": d.severity, "direction": d.direction}
                for d in devs
            ]
            results["overall"]["deviations"].extend(results["idle"]["deviations"])  # already dict

        # Validate and assess high idle
        valid2, errors2 = self.validate_input(high_idle_measurements, "high_idle")
        if not valid2:
            results["high_idle"]["errors"] = errors2
        else:
            devs2 = self.find_deviations(high_idle_measurements, "high_idle")
            results["high_idle"]["deviations"] = [
                {"gas": d.gas, "measured": d.measured, "normal_range": f"{NORMAL_HIGH_IDLE[d.gas].min}-{NORMAL_HIGH_IDLE[d.gas].max} {NORMAL_HIGH_IDLE[d.gas].unit}", "severity": d.severity, "direction": d.direction}
                for d in devs2
            ]
            results["overall"]["deviations"].extend(results["high_idle"]["deviations"])  # already dict

        # Combine measurements for pattern matching
        all_measurements = {**idle_measurements, **{f"{k}_high": v for k, v in high_idle_measurements.items()}}
        # Use lambda if available, else calculate approximate from O2? For now just use what we have
        patterns = self.match_patterns(results["overall"]["deviations"], idle_measurements)
        results["overall"]["patterns"] = [
            {
                "pattern": p.pattern_name,
                "confidence": round(p.confidence, 2),
                "culprits": p.culprits,
                "notes": p.notes,
            }
            for p in patterns
        ]

        # Health score: simple heuristic (0-100)
        # Start at 100, subtract for each moderate deviation, more for high/critical
        score = 100
        for d in results["overall"]["deviations"]:
            if d["severity"] == "high":
                score -= 15
            elif d["severity"] == "critical":
                score -= 30
            else:
                score -= 5
        score = max(0, min(100, score))
        results["overall"]["health_score"] = score

        # Urgent flag
        results["overall"]["urgent"] = any(d["severity"] in ("high", "critical") for d in results["overall"]["deviations"])

        # Recommendations
        recs = []
        if any(d["gas"] == "lambda" and d["direction"] == "low" for d in results["overall"]["deviations"]):
            recs.append("Check for rich condition: verify fuel pressure, inspect oxygen sensor, look for intake air leaks after MAF (if applicable), check for clogged air filter.")
        if any(d["gas"] == "lambda" and d["direction"] == "high" for d in results["overall"]["deviations"]):
            recs.append("Check for lean condition: inspect for vacuum leaks, verify fuel pump pressure, check fuel filter, examine MAF/MAP sensor.")
        if any(d["gas"] == "hc" and d["severity"] in ("high", "critical") for d in results["overall"]["deviations"]):
            recs.append("High HC indicates misfire. Perform ignition system check: spark plugs, coils, wires. Also verify injector operation and compression if needed.")
        if any(d["gas"] == "nox" and d["direction"] == "high" for d in results["overall"]["deviations"]):
            recs.append("High NOx suggests high combustion temperature. Check ignition timing (may be too advanced), consider slight enrichment or EGR function.")
        if any(d["gas"] == "co" and d["direction"] == "high" for d in results["overall"]["deviations"]):
            recs.append("High CO indicates incomplete combustion. Often tied to rich mixture or weak spark. Check fuel mixture and ignition system.")
        if not recs:
            recs.append("All readings within acceptable ranges. No immediate issues detected.")
        results["overall"]["recommendations"] = recs

        return results

def format_results(results: Dict) -> str:
    """Create human-readable report."""
    lines = []
    lines.append("=== 5-Gas Exhaust Diagnostic Report ===\n")
    lines.append(f"Overall Health Score: {results['overall']['health_score']}/100")
    if results['overall']['urgent']:
        lines.append("⚠️  URGENT: Significant deviations detected - address promptly.")
    lines.append("\n--- Idle Measurements ---")
    if "errors" in results["idle"]:
        lines.append("Errors: " + ", ".join(results["idle"]["errors"]))
    else:
        for d in results["idle"]["deviations"]:
            lines.append(f"• {d['gas'].upper()}: {d['measured']} (normal: {d['normal_range']}) – {d['severity']}")
        if not results["idle"]["deviations"]:
            lines.append("All within normal range.")
    lines.append("\n--- High Idle Measurements ---")
    if "errors" in results["high_idle"]:
        lines.append("Errors: " + ", ".join(results["high_idle"]["errors"]))
    else:
        for d in results["high_idle"]["deviations"]:
            lines.append(f"• {d['gas'].upper()}: {d['measured']} (normal: {d['normal_range']}) – {d['severity']}")
        if not results["high_idle"]["deviations"]:
            lines.append("All within normal range.")
    lines.append("\n--- Diagnostic Patterns ---")
    if results["overall"]["patterns"]:
        for p in results["overall"]["patterns"][:3]:  # top 3
            lines.append(f"• {p['pattern'].replace('_', ' ').title()} (confidence: {p['confidence']:.0%})")
            for culprit in p["culprits"][:2]:  # top 2 culprits
                lines.append(f"  - {culprit}")
            if p["notes"]:
                lines.append(f"  Note: {p['notes']}")
    else:
        lines.append("No fault patterns matched.")
    lines.append("\n--- Recommendations ---")
    for rec in results["overall"]["recommendations"]:
        lines.append(f"• {rec}")
    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    # Quick self-test (avoid unicode arrows in Windows console)
    sample_idle = {"lambda": 0.95, "co": 1.5, "co2": 13.0, "o2": 0.4, "hc": 200, "nox": 80}
    sample_high = {"lambda": 0.97, "co": 1.2, "co2": 14.0, "o2": 0.8, "hc": 120, "nox": 150}
    engine = DiagnosticEngine()
    results = engine.assess(sample_idle, sample_high)
    # Print plain text, avoid arrows
    print("=== 5-Gas Diagnostic Report ===")
    print(f"Overall Health Score: {results['overall']['health_score']}/100")
    if results['overall']['urgent']:
        print("URGENT: Significant deviations detected.")
    print("\n--- Idle Measurements ---")
    if "errors" in results["idle"]:
        print("Errors: " + ", ".join(results["idle"]["errors"]))
    else:
        for d in results["idle"]["deviations"]:
            print(f"* {d['gas'].upper()}: {d['measured']} (normal: {d['normal_range']}) - {d['severity']}")
        if not results["idle"]["deviations"]:
            print("All within normal range.")
    print("\n--- High Idle Measurements ---")
    if "errors" in results["high_idle"]:
        print("Errors: " + ", ".join(results["high_idle"]["errors"]))
    else:
        for d in results["high_idle"]["deviations"]:
            print(f"* {d['gas'].upper()}: {d['measured']} (normal: {d['normal_range']}) - {d['severity']}")
        if not results["high_idle"]["deviations"]:
            print("All within normal range.")
    print("\n--- Diagnostic Patterns ---")
    if results["overall"]["patterns"]:
        for p in results["overall"]["patterns"][:3]:
            print(f"* {p['pattern'].replace('_', ' ').title()} (confidence: {p['confidence']:.0%})")
            for culprit in p["culprits"][:2]:
                print(f"  - {culprit}")
    else:
        print("No fault patterns matched.")
    print("\n--- Recommendations ---")
    for rec in results["overall"]["recommendations"]:
        print(f"* {rec}")
