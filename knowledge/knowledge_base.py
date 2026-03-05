# Exhaust Gas Analyzer Knowledge Base
# Derived from: C:\Users\asus\.openclaw\workspace\memory\emissions.md (Sections 3 & 9.2)

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Range:
    """Normal range for a gas at a specific operating condition."""
    min: float
    max: float
    unit: str
    typical: float = None  # typical/ideal value

# Normal ranges for warm engine
NORMAL_IDLE = {
    "lambda": Range(0.98, 1.02, "ratio", 1.00),
    "co": Range(0.0, 0.2, "%", 0.1),
    "co2": Range(12.0, 14.0, "%", 13.0),
    "o2": Range(0.3, 1.0, "%", 0.7),
    "hc": Range(50, 150, "ppm", 100),
    "nox": Range(0, 100, "ppm", 50),  # idle typically low
}

# High idle (fast idle, ~1500-2000 rpm, no load)
NORMAL_HIGH_IDLE = {
    "lambda": Range(0.98, 1.02, "ratio", 1.00),
    "co": Range(0.0, 0.3, "%", 0.15),  # slightly higher possible
    "co2": Range(13.0, 15.0, "%", 14.0),
    "o2": Range(0.5, 1.5, "%", 0.9),  # slightly more excess air
    "hc": Range(30, 120, "ppm", 80),  # often lower than idle
    "nox": Range(50, 200, "ppm", 120),  # increases with temperature/rpm
}

# Diagnostic thresholds for abnormal readings
THRESHOLDS = {
    "lambda_low_rich": 0.90,    # λ < 0.90 → rich
    "lambda_high_lean": 1.10,   # λ > 1.10 → lean
    "co_high": 2.0,             # % - indicates rich if >2%
    "o2_low_rich": 0.5,         # % - rich if <0.5%
    "o2_high_lean": 2.0,        # % - lean if >2%
    "hc_critical": 2000,        # ppm - severe misfire
    "hc_high": 500,             # ppm - elevated
    "nocrit_matches_required": 2,  # minimum matching indicators to suggest a cause
    "nox_converter_max": 2000,  # ppm - typical converter capacity; above this indicates engine/aftertreatment issue
    "co2_inefficiency": 12.0,   # % - below this indicates combustion inefficiency (misfire, mechanical, etc.)
}

# Fault pattern signatures
# Each pattern maps to a set of observed conditions (gas readngs outside normal range)
FAULT_PATTERNS = {
    "rich_mixture": {
        "indicators": {
            "lambda": "<0.90",
            "co": ">2.0",
            "o2": "<0.5",
        },
        "culprits": [
            "Over-fueling (faulty injector, fuel pressure too high, bad coolant temp sensor)",
            "Faulty oxygen sensor (stuck lean, causing ECU to enrich)",
            "Weak fuel pump (causing pressure fluctuations - sometimes rich, sometimes lean)",
            "Faulty MAF/MAP sensor (under-reporting air → ECU adds fuel)",
            "Exhaust restriction (catalyst collapse) causing backpressure",
            "Clogged air filter (reducing airflow)",
        ],
        "notes": "Rich mixture increases CO and HC, decreases O2. Lambda confirms.",
    },
    "lean_mixture": {
        "indicators": {
            "lambda": ">1.10",
            "o2": ">2.0",
            "co": "low",
            "nox": "high",
        },
        "culprits": [
            "Vacuum leak (intake manifold, gasket, hose)",
            "Weak fuel pump (low pressure)",
            "Faulty fuel pressure regulator",
            "Dirty/blocked fuel filter",
            "Faulty MAF sensor (over-reporting air)",
            "EGR stuck open (at idle/part-load)",
            "Exhaust leak (before O2 sensor) introducing extra O2",
        ],
        "notes": "Lean condition raises NOx, O2. Can cause high HC if extreme.",
    },
    "misfire": {
        "indicators": {
            "hc": ">2000",
            "o2": "high",  # unburned O2 from skipped cycle
            "co": "low or irregular",
            "co2": "low",
        },
        "culprits": [
            "Fouled/failed spark plug",
            "Failed ignition coil or module",
            "Injector not pulsing (circuit issue)",
            "Compression loss (rings, valves, head gasket)",
            "Severely lean or rich mixture (outside combustible range)",
            "Damaged catalytic converter (increasing backpressure)",
        ],
        "notes": "Misfire is a symptom; find root cause (ignition, fuel, air, mechanical).",
    },
    "egr_stuck_open_idle": {
        "indicators": {
            "hc": "high (>200)",
            "co": "moderate",
            "o2": "moderate",
            "co2": "slightly low",
            "lambda": "~1.0 (normal)",
        },
        "culprits": [
            "EGR valve stuck open (mechanical or diaphragm fault)",
            "EGR passages clogged with carbon (partial opening)",
            "Faulty EGR solenoid or vacuum line",
            "Incorrect EGR base position (after cleaning/repair)",
        ],
        "notes": "EGR at idle dilutes charge → rough idle, elevated HC. Often worse when hot.",
    },
    "catalyst_failure": {
        "indicators": {
            "co": "high (>0.5%)",
            "hc": "high (>200 ppm)",
            "o2": "high (>1.0%) if converter completely failed",
            "nox": "variable",
        },
        "culprits": [
            "Catalyst substrate melted or broken (overheating from misfire or rich)",
            "Catalyst poisoned (silicone, lead, oil additives)",
            "Aged catalyst (end of life)",
            "Physical damage (impact, thermal shock)",
        ],
        "notes": "Usually a symptom of prior poor engine condition. Confirm with back-pressure test.",
    },
    "ignition_timing_issue": {
        "indicators": {
            "nox": "high",
            "co": "low-moderate",
            "lambda": "normal or slightly lean",
        },
        "culprits": [
            "Ignition timing overly advanced -> raises combustion temperature -> NOx up",
            "Faulty knock sensor causing ECU to retard/advance incorrectly",
            "Incorrect base timing (distributor/trigger wheel)",
            "Worn timing components (chain/gear stretch)",
        ],
        "notes": "Check timing with strobe. Retarding 2-3° can significantly reduce NOx with small HC/CO increase.",
    },
    "sensor_fault": {
        "indicators": {
            "lambda": "inconsistent or out of range",
            "o2": "out of expected range for mixture",
            "observations": "Readings don't align (e.g., lambda low but O2 high)",
        },
        "culprits": [
            "Faulty oxygen sensor (slow, contaminated, heater circuit)",
            "Faulty air temperature sensor (affects density calc)",
            "Faulty coolant temperature sensor (enrichment at wrong times)",
            "Wiring issue (ground, voltage drop)",
            "Contaminated sensor (lead, silicone, oil)",
        ],
        "notes": "Always verify sensor operation before mechanical repairs. Compare sensor voltages with scan tool.",
    },
    "o2_sensor_failure": {
        "indicators": {
            "lambda": "stuck at one value",
            "o2": "no switching / constant",
            "co": "erratic or consistently high/low",
        },
        "culprits": [
            "O2 sensor dead or contaminated",
            "O2 sensor heater circuit failed",
            "O2 sensor wiring damaged / connectors corroded",
            "O2 sensor contaminated by silicone or leaded fuel",
        ],
        "notes": "Narrowband sensors should switch 0.1-0.9V; wideband should track actual lambda. Check sensor voltage activity.",
    },
    "maf_sensor_fault": {
        "indicators": {
            "lambda": "lean at idle, richer at high airflow (or opposite)",
            "co": "inverse to airflow",
            "o2": "higher than normal",
        },
        "culprits": [
            "MAF sensor dirty or damaged (under-reads)",
            "MAF sensor wiring fault",
            "MAF sensor out of calibration",
            "Air leak between MAF and throttle (unmetered air)",
        ],
        "notes": "MAF should correlate with airflow. Use live data: compare grams/sec to expected for engine size & rpm.",
    },
    "fuel_pump_weak": {
        "indicators": {
            "lambda": "lean under load (but may be normal at idle)",
            "co": "low",
            "o2": "high under load",
            "hc": "may increase if too lean to fire",
        },
        "culprits": [
            "Weak fuel pump (low pressure)",
            "Clogged fuel filter",
            "Incorrect fuel pressure regulator",
            "Low voltage to fuel pump (bad relay, wiring)",
        ],
        "notes": "Check fuel pressure with gauge at idle and during a road load (hold at 3000 rpm). Pressure should stay within spec.",
    },
    "injector_clogged": {
        "indicators": {
            "lambda": "lean (especially on acceleration)",
            "co": "low",
            "o2": "high",
            "hc": "may increase on acceleration",
        },
        "culprits": [
            "Dirty/clogged fuel injector (reduced flow)",
            "Injector screen blocked",
            "Injector coil or driver circuit failing",
        ],
        "notes": "Injectors should flow within 5-10% of each other. Perform flow test or injector balance test.",
    },
    "air_filter_clogged": {
        "indicators": {
            "lambda": "slightly rich (reduced airflow)",
            "co": "moderately high",
            "co2": "slightly low",
            "o2": "slightly low",
        },
        "culprits": [
            "Dirty/clogged air filter element",
            "Restricted air intake ducting (crushed hose, debris)",
        ],
        "notes": "Check and replace air filter. Inspect entire intake path for restrictions.",
    },
    "oxygen_sensor_lazy": {
        "indicators": {
            "lambda": "slow to adjust after enrichment/leaning",
            "o2": "switching frequency too low or too high",
            "co": "oscillates but average may be off",
        },
        "culprits": [
            "Aged oxygen sensor (response degraded)",
            "Contaminated oxygen sensor",
            "Incorrect oxygen sensor type (narrowband used where wideband required)",
        ],
        "notes": "A good O2 sensor switches ~1-2 times per second at 1500-2500 rpm. Monitor voltage with scan tool.",
    },
    # New patterns from extended reference documents
    "air_injection_malfunction": {
        "indicators": {
            "o2": ">2.0",
            "co2": "<12.0",
            "lambda": "0.98-1.02",  # near stoichiometric, ECU may compensate
        },
        "culprits": [
            "Air injection pump failed",
            "Air injection check valve stuck",
            "Air injection diverter valve stuck open",
            "Air injection system leaking",
        ],
        "notes": "Secondary air injection adds oxygen to exhaust, diluting CO2 and raising O2 without changing lambda. Disable AIR to test; compare readings before/after.",
    },
    "combustion_inefficiency": {
        "indicators": {
            "co2": "<12.0",
        },
        "culprits": [
            "Ignition misfire",
            "Low compression (worn rings, valves, head gasket)",
            "Mechanical timing issues (chain/gear stretch)",
            "Fuel delivery problems (weak pump, clogged filter)",
            "Air/fuel imbalance (sensor faults, vacuum leaks)",
        ],
        "notes": "Low CO2 indicates incomplete combustion. With air injection disabled, CO2 below 12% suggests engine issues. If HC is high and CO2 normal, suspect catalytic converter instead.",
    },
}

# Euro 3 limits for reference (g/km), not directly used for tailpipe conc but helpful
EURO_3_LIMITS = {
    "co": 2.3,      # g/km
    "hc": 0.20,     # g/km
    "nox": 0.15,    # g/km
}

# UK MOT test limits (concentration)
MOT_LIMITS = {
    "co_idle_percent": 0.3,
    "co_raised_idle_percent": 0.2,
    "hc_raised_ppm": 200,
    "lambda_min": 0.97,
    "lambda_max": 1.03,
}

# ----------------------------------------------------------------------------
# Fault Pattern Reference Table (from tabelagas.xlsx)
# ----------------------------------------------------------------------------
# This table provides qualitative expected changes for each gas when a
# particular symptom/fault is present. The values are descriptive strings
# like "Large increase", "Some decrease", "No change", etc.
#
# Use `get_table_pattern()` to retrieve a pattern and optionally convert
# qualitative descriptors into numeric indicator conditions based on the
# normal ranges and thresholds defined above.
#
# Columns: Symptom | HC | CO | CO2 | O2 | NOx

TABLE_PATTERNS_RAW = {
    "ignition_misfire": {
        "hc": "Large increase",
        "co": "Some decrease",
        "co2": "Some Decrease",
        "o2": "Some-large increase",
        "nox": "Some-large decrease",
    },
    "compression_loss": {
        "hc": "Some-large Increase",
        "co": "Some decrease",
        "co2": "Some decrease",
        "o2": "Some Increase",
        "nox": "Some-large decrease",
    },
    "rich_mixture_alt": {  # Note: differs slightly from FAULT_PATTERNS['rich_mixture']
        "hc": "Some-large Increase",
        "co": "Large increase",
        "co2": "Some decrease",
        "o2": "Some Decrease",
        "nox": "Some-large decrease",
    },
    "lean_mixture_alt": {
        "hc": "Some Increase",
        "co": "Large Decrease",
        "co2": "Some Decrease",
        "o2": "Some Increase",
        "nox": "Some-large increase",
    },
    "very_lean_mixture": {
        "hc": "Large Increase",
        "co": "Large Decrease",
        "co2": "Some Decrease",
        "o2": "Large Increase",
        "nox": "Some-large decrease",
    },
    "slightly_retarded_timing": {
        "hc": "Some decrease",
        "co": "No change or Some increase",
        "co2": "No change",
        "o2": "No change",
        "nox": "Large Decrease",
    },
    "very_retarded_timing": {
        "hc": "Some Increase",
        "co": "No Change",
        "co2": "Some-large Decrease",
        "o2": "No Change",
        "nox": "Large Decrease",
    },
    "advanced_timing": {
        "hc": "Some Increase",
        "co": "No change or Some-decrease",
        "co2": "No change",
        "o2": "No Change",
        "nox": "Large Increase",
    },
    "egr_operating": {
        "hc": "No Change",
        "co": "No Change",
        "co2": "Some Decrease",
        "o2": "No Change",
        "nox": "Large Decrease",
    },
    "egr_leaking": {
        "hc": "Some Increase",
        "co": "No Change",
        "co2": "No change or Some decrease",
        "o2": "No Change",
        "nox": "Some decrease or No change",
    },
    "air_injection_operation": {
        "hc": "Large Decrease",
        "co": "Large Decrease",
        "co2": "Some-large Decrease",
        "o2": "Large Increase",
        "nox": "No Change",
    },
    "catalytic_converter_functional": {
        "hc": "Some Decrease",
        "co": "Some Decrease",
        "co2": "Some Increase",
        "o2": "Some Decrease",
        "nox": "Some Decrease W/3-w cat",  # note: weird text, keep as-is
    },
    "catalytic_converter_not_functional": {
        "hc": "Some-large Increase",
        "co": "Some-large increase",
        "co2": "Some Decrease",
        "o2": "Some Increase",
        "nox": "Some Increased W/3-w cat",
    },
    "exhaust_leak": {
        "hc": "Some Decrease",
        "co": "Some Decrease",
        "co2": "Some Decrease",
        "o2": "Some Increase",
        "nox": "No change",
    },
    "worn_engine": {
        "hc": "Some Increase",
        "co": "Some Increase",
        "co2": "Some Decrease",
        "o2": "Some Decrease",
        "nox": "No change or Slight decrease",
    },
    "o2_sensor_biased_low": {
        "hc": "Some Increase",
        "co": "Some-large Increase",
        "co2": "Some Decrease",
        "o2": "Some Decrease",
        "nox": "Some Decrease",
    },
    "o2_sensor_biased_high": {
        "hc": "Some Increase",
        "co": "Some decrease",
        "co2": "Some Decrease",
        "o2": "Some increase",
        "nox": "Some increase",
    },
    "flat_camshaft": {
        "hc": "No change or Some decrease",
        "co": "Some Decrease",
        "co2": "Some Decrease",
        "o2": "No change or Some decrease",
        "nox": "No change or Some decrease",
    },
}

# Mapping of qualitative change descriptors to numeric conditions.
# This is approximate and should be calibrated to specific engine/analyzer.
QUALITATIVE_TO_INDICATOR = {
    # Format: "descriptor": (comparison_op, threshold_modifier)
    # comparison_op: "<", ">", "~" (within normal), "!" (outside normal)
    # threshold_modifier: multiplier or absolute offset applied to normal range or THRESHOLDS
    "large increase": (">", 2.0),      # > 2x typical or > threshold_max
    "some increase": (">", 1.2),       # > 1.2x typical or > threshold_normal
    "some-large increase": (">", 1.5),
    "some decrease": ("<", 0.8),       # < 0.8x typical
    "some-large decrease": ("<", 0.6),
    "large decrease": ("<", 0.5),
    "no change": ("~", 1.0),           # within normal expected range
    "no change or some increase": ("~", 1.1),  # either normal or slightly above
    "no change or some decrease": ("~", 0.9),
    "some Decrease": ("<", 0.8),       # case variations
    "Some Increase": (">", 1.2),
    "Large Increase": (">", 2.0),
    "Large decrease": ("<", 0.5),
    "Some-large increase": (">", 1.5),
    "Some-large decrease": ("<", 0.6),
    "No Change": ("~", 1.0),
    # For mixed descriptors, fallback to moderate bounds
}

def get_table_pattern(symptom_key: str) -> Optional[Dict[str, str]]:
    """
    Retrieve the qualitative pattern for a given symptom from the reference table.
    Args:
        symptom_key: e.g., "ignition_misfire", "rich_mixture_alt"
    Returns:
        dict mapping gas names (hc, co, co2, o2, nox) to change descriptors, or None if not found.
    """
    return TABLE_PATTERNS_RAW.get(symptom_key)

def convert_qualitative_to_indicator(gas: str, descriptor: str, condition: str = "idle") -> Optional[str]:
    """
    Convert a qualitative change descriptor into a numeric condition string
    compatible with FAULT_PATTERNS indicator format.
    Example: "Large increase" for hc might become "hc > 2000" (using THRESHOLDS).
    This is approximate and may need tuning.
    Args:
        gas: one of "hc", "co", "co2", "o2", "nox", "lambda"
        descriptor: qualitative string like "Large increase"
        condition: "idle" or "high_idle" (to pick appropriate normal range)
    Returns:
        condition string like ">2000" or "<0.5", or None if unknown descriptor.
    """
    if gas not in ["lambda", "co", "co2", "o2", "hc", "nox"]:
        return None
    descriptor = descriptor.strip().lower()
    op, modifier = QUALITATIVE_TO_INDICATOR.get(descriptor, (">", 1.5) if "increase" in descriptor else ("<", 0.7))

    # Determine baseline normal value
    normals = NORMAL_IDLE if condition == "idle" else NORMAL_HIGH_IDLE
    if gas in normals:
        normal_range = normals[gas]
        typical = normal_range.typical if normal_range.typical is not None else (normal_range.min + normal_range.max) / 2
    elif gas == "lambda":
        # lambda handled separately but similar
        normal_range = normals.get("lambda", Range(0.98, 1.02, "ratio", 1.0))
        typical = normal_range.typical if normal_range.typical is not None else 1.0
    else:
        # unknown gas
        return None

    # For increase > typical
    if op == ">":
        # Use multiplier on typical or apply to threshold upper bound if available
        # For HC, use hc_high threshold; for CO use co_high; etc.
        thresholds = {
            "hc": THRESHOLDS.get("hc_high", 500),
            "co": THRESHOLDS.get("co_high", 2.0),
            "nox": THRESHOLDS.get("nox_converter_max", 2000),  # high NOx could indicate issue
            "o2": THRESHOLDS.get("o2_high_lean", 2.0),
            "co2": None,  # CO2 doesn't have a high threshold; use typical
            "lambda": THRESHOLDS.get("lambda_high_lean", 1.10),
        }
        if gas in thresholds and thresholds[gas] is not None:
            base = thresholds[gas]
        else:
            base = typical * 1.5  # fallback
        # Apply modifier: e.g., "large" (2.0) gives base*2, "some" (1.2) gives base*1.2
        val = base * modifier if modifier < 10 else modifier  # if modifier is absolute threshold
        if gas in ["co", "co2", "lambda", "o2"]:
            return f"{gas} > {val:.2f}"
        else:
            return f"{gas} > {int(val) if val >= 100 else val:.0f}"
    elif op == "<":
        # For decrease, use lower bound of normal range or threshold lower
        thresholds = {
            "hc": None,  # low HC not usually a problem; use normal min
            "co": None,
            "co2": THRESHOLDS.get("co2_inefficiency", 12.0),
            "o2": THRESHOLDS.get("o2_low_rich", 0.5),
            "nox": None,
            "lambda": THRESHOLDS.get("lambda_low_rich", 0.90),
        }
        if gas in thresholds and thresholds[gas] is not None:
            base = thresholds[gas]
        else:
            base = normal_range.min if gas in normals else 0.0
        val = base * modifier if modifier < 10 else modifier
        if gas in ["co", "co2", "lambda", "o2"]:
            return f"{gas} < {val:.2f}"
        else:
            return f"{gas} < {int(val) if val >= 100 else val:.0f}"
    else:  # "~" within normal
        return f"{gas} normal"

# Example usage:
#   pattern = get_table_pattern("ignition_misfire")
#   if pattern:
#       indicators = {g: convert_qualitative_to_indicator(g, d) for g, d in pattern.items()}
