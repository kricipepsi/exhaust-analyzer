"""Test calibration data for the diagnostic engine.

Gold Standard Cases: Lambda near 1.0, healthy combustion
Fail Standard Cases: Various fault conditions with expected lambdas and health scores.
"""

from typing import List, Dict

# Gold Standard Cases (healthy operating conditions)
# These should yield lambda ~1.00 and high health (>95)
GOLD_STANDARD = [
    {
        "case_id": "G-001",
        "rpm": "Low Idle",
        "co": 0.05,
        "co2": 15.2,
        "hc": 12,
        "o2": 0.10,
        "lambda": 1.00,
        "expected_health": 100
    },
    {
        "case_id": "G-002",
        "rpm": "Low Idle",
        "co": 0.08,
        "co2": 15.0,
        "hc": 20,
        "o2": 0.15,
        "lambda": 1.01,
        "expected_health": 100
    },
    {
        "case_id": "G-003",
        "rpm": "Low Idle",
        "co": 0.12,
        "co2": 14.8,
        "hc": 8,
        "o2": 0.20,
        "lambda": 0.99,
        "expected_health": 100
    },
    {
        "case_id": "G-004",
        "rpm": "Low Idle",
        "co": 0.03,
        "co2": 15.4,
        "hc": 15,
        "o2": 0.08,
        "lambda": 1.00,
        "expected_health": 100
    },
    {
        "case_id": "G-005",
        "rpm": "Low Idle",
        "co": 0.10,
        "co2": 15.1,
        "hc": 25,
        "o2": 0.12,
        "lambda": 1.01,
        "expected_health": 100
    },
    {
        "case_id": "G-006",
        "rpm": "Low Idle",
        "co": 0.06,
        "co2": 15.3,
        "hc": 10,
        "o2": 0.09,
        "lambda": 1.00,
        "expected_health": 100
    },
    {
        "case_id": "G-007",
        "rpm": "Low Idle",
        "co": 0.15,
        "co2": 14.7,
        "hc": 18,
        "o2": 0.18,
        "lambda": 0.99,
        "expected_health": 100
    },
    {
        "case_id": "G-008",
        "rpm": "Low Idle",
        "co": 0.07,
        "co2": 15.25,
        "hc": 14,
        "o2": 0.11,
        "lambda": 1.00,
        "expected_health": 100
    },
    {
        "case_id": "G-009",
        "rpm": "Low Idle",
        "co": 0.09,
        "co2": 15.0,
        "hc": 22,
        "o2": 0.14,
        "lambda": 1.00,
        "expected_health": 100
    },
    {
        "case_id": "G-010",
        "rpm": "Low Idle",
        "co": 0.11,
        "co2": 14.9,
        "hc": 16,
        "o2": 0.16,
        "lambda": 1.01,
        "expected_health": 100
    }
]

# Fail Standard Cases (various fault conditions)
# These should yield lambda outside 0.98-1.02 and lower health scores
FAIL_STANDARD = [
    {
        "case_id": "F-001",
        "rpm": "Low Idle",
        "co": 0.10,
        "co2": 11.5,
        "hc": 450,
        "o2": 3.5,
        "lambda": 1.15,
        "expected_verdict": "Vacuum Leak",
        "expected_health": 45
    },
    {
        "case_id": "F-002",
        "rpm": "Low Idle",
        "co": 2.5,
        "co2": 10.0,
        "hc": 200,
        "o2": 1.0,
        "lambda": 0.88,
        "expected_verdict": "Systemic Rich Mixture",
        "expected_health": 45
    },
    {
        "case_id": "F-003",
        "rpm": "Low Idle",
        "co": 0.05,
        "co2": 13.5,
        "hc": 600,
        "o2": 2.5,
        "lambda": 1.12,
        "expected_verdict": "Ignition Misfire",
        "expected_health": 30
    },
    {
        "case_id": "F-004",
        "rpm": "Low Idle",
        "co": 0.08,
        "co2": 9.0,
        "hc": 15,
        "o2": 8.0,
        "lambda": 1.25,
        "expected_verdict": "Exhaust Dilution",
        "expected_health": 85
    },
    {
        "case_id": "F-005",
        "rpm": "Low Idle",
        "co": 0.12,
        "co2": 14.0,
        "hc": 10,
        "o2": 0.5,
        "lambda": 1.02,
        "expected_verdict": "Healthy Engine",
        "expected_health": 100
    },
    {
        "case_id": "F-006",
        "rpm": "Low Idle",
        "co": 1.2,
        "co2": 11.0,
        "hc": 150,
        "o2": 0.8,
        "lambda": 0.92,
        "expected_verdict": "Systemic Rich Mixture",
        "expected_health": 45
    },
    {
        "case_id": "F-007",
        "rpm": "Low Idle",
        "co": 0.06,
        "co2": 12.5,
        "hc": 800,
        "o2": 3.0,
        "lambda": 1.18,
        "expected_verdict": "Ignition Misfire",
        "expected_health": 30
    },
    {
        "case_id": "F-008",
        "rpm": "Low Idle",
        "co": 0.15,
        "co2": 8.5,
        "hc": 30,
        "o2": 6.5,
        "lambda": 1.28,
        "expected_verdict": "Exhaust Dilution",
        "expected_health": 85
    },
    {
        "case_id": "F-009",
        "rpm": "Low Idle",
        "co": 0.07,
        "co2": 13.8,
        "hc": 12,
        "o2": 0.3,
        "lambda": 1.01,
        "expected_verdict": "Healthy Engine",
        "expected_health": 100
    },
    {
        "case_id": "F-010",
        "rpm": "Low Idle",
        "co": 0.09,
        "co2": 14.2,
        "hc": 20,
        "o2": 0.4,
        "lambda": 1.00,
        "expected_verdict": "Healthy Engine",
        "expected_health": 100
    }
]
