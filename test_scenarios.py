#!/usr/bin/env python3
"""Test suite for Exhaust Analyzer with realistic scenarios."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.assessor import DiagnosticEngine

def test_scenario(name, idle, high):
    print(f"\n=== {name.upper()} ===")
    engine = DiagnosticEngine(rpm=800)
    results = engine.assess(idle, high)
    print(f"Health Score: {results['overall']['health_score']}")
    print(f"Urgent: {results['overall']['urgent']}")
    print("Idle deviations:", ", ".join([f"{d['gas']}={d['measured']}" for d in results['idle']['deviations']]) if results['idle'].get('deviations') else "None")
    print("High idle deviations:", ", ".join([f"{d['gas']}={d['measured']}" for d in results['high_idle']['deviations']]) if results['high_idle'].get('deviations') else "None")
    print("Top patterns:")
    for p in results['overall']['patterns'][:2]:
        culprit = p['culprits'][0].replace('→', '->')
        print(f"  - {p['pattern']} ({p['confidence']:.0%}): {culprit}")
    rec = results['overall']['recommendations'][0].replace('→', '->')
    print("Recommendation:", rec)

# 1. Normal healthy engine
test_scenario("Normal healthy", 
    {"lambda": 1.00, "co": 0.08, "co2": 13.5, "o2": 0.6, "hc": 80, "nox": 60},
    {"lambda": 1.00, "co": 0.12, "co2": 14.2, "o2": 0.9, "hc": 60, "nox": 120}
)

# 2. Rich mixture (over-fueling)
test_scenario("Rich mixture",
    {"lambda": 0.85, "co": 3.2, "co2": 12.0, "o2": 0.3, "hc": 250, "nox": 40},
    {"lambda": 0.88, "co": 2.5, "co2": 12.5, "o2": 0.4, "hc": 180, "nox": 50}
)

# 3. Lean condition (vacuum leak)
test_scenario("Lean condition",
    {"lambda": 1.18, "co": 0.05, "co2": 11.0, "o2": 3.2, "hc": 300, "nox": 350},
    {"lambda": 1.20, "co": 0.06, "co2": 11.5, "o2": 3.5, "hc": 250, "nox": 400}
)

# 4. Misfire (ignition failure)
test_scenario("Misfire",
    {"lambda": 1.05, "co": 0.5, "co2": 10.0, "o2": 2.0, "hc": 2500, "nox": 30},
    {"lambda": 1.08, "co": 0.4, "co2": 10.5, "o2": 2.2, "hc": 2200, "nox": 40}
)

# 5. EGR stuck open at idle
test_scenario("EGR stuck open idle",
    {"lambda": 1.02, "co": 0.8, "co2": 12.5, "o2": 1.2, "hc": 350, "nox": 40},
    {"lambda": 1.01, "co": 0.6, "co2": 13.0, "o2": 1.0, "hc": 150, "nox": 80}
)

# 6. High NOx (timing too advanced)
test_scenario("High NOx (timing)",
    {"lambda": 1.05, "co": 0.2, "co2": 13.0, "o2": 1.5, "hc": 100, "nox": 450},
    {"lambda": 1.06, "co": 0.2, "co2": 13.5, "o2": 1.6, "hc": 80, "nox": 550}
)

# 7. O2 sensor failure (stuck rich)
test_scenario("O2 sensor stuck rich",
    {"lambda": 0.80, "co": 4.0, "co2": 11.0, "o2": 0.2, "hc": 200, "nox": 30},
    {"lambda": 0.82, "co": 3.5, "co2": 11.5, "o2": 0.3, "hc": 150, "nox": 40}
)

# 8. MAF over-reporting (lean)
test_scenario("MAF over-reporting (lean)",
    {"lambda": 1.22, "co": 0.04, "co2": 10.5, "o2": 4.0, "hc": 200, "nox": 300},
    {"lambda": 1.25, "co": 0.05, "co2": 11.0, "o2": 4.2, "hc": 180, "nox": 350}
)

# 9. Weak fuel pump (lean under load) – simulated as high idle lean
test_scenario("Weak fuel pump",
    {"lambda": 1.05, "co": 0.3, "co2": 12.0, "o2": 1.8, "hc": 120, "nox": 150},
    {"lambda": 1.18, "co": 0.1, "co2": 11.0, "o2": 3.5, "hc": 300, "nox": 380}
)

# 10. Clogged air filter (slightly rich)
test_scenario("Clogged air filter",
    {"lambda": 0.92, "co": 0.6, "co2": 13.0, "o2": 0.4, "hc": 90, "nox": 70},
    {"lambda": 0.94, "co": 0.5, "co2": 13.5, "o2": 0.5, "hc": 70, "nox": 90}
)

print("\n=== Test complete ===")
