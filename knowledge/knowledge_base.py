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
