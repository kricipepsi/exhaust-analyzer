#!/usr/bin/env python3
"""Test Exhaust Dilution (P_003) with appropriate data."""

from core.matrix import _safe_eval
from core.bretschneider import calculate_lambda

# P_003 logic: measured_lambda > calculated_lambda + 0.05 and low_idle.o2 > 2.0
# We need measured_lambda significantly higher than calculated_lambda.

# Let's try to find gas values where calculated lambda is low (< 1.0) but measured is high (>1.05).
# For example: If the gases indicate rich mixture (low lambda), but the O2 sensor reads lean.
# But dilution wouldn't cause that; it's usually the opposite: gases indicate lean but measured even leaner?
# Actually dilution: The O2 sensor sees extra air from leak, so measured lambda > calculated.
# So we need calculated to be moderate (maybe 0.95) and measured > 1.0.

# Let's try: co=1.0, co2=12.0, hc=500, o2=2.0 -> compute lambda?
test_gases = {
    'co': 1.0,
    'co2': 12.0,
    'hc': 500,
    'o2': 2.0
}

calc = calculate_lambda(co=1.0, co2=12.0, hc_ppm=500, o2=2.0, fuel_type='e10')
calc_lambda = calc['lambda']
print(f"Test gases: co={test_gases['co']}, co2={test_gases['co2']}, hc={test_gases['hc']}, o2={test_gases['o2']}")
print(f"Calculated lambda: {calc_lambda:.3f}")

# We want measured > calc + 0.05. Let measured = max(calc + 0.06, 1.05)
measured_lambda = max(round(calc_lambda + 0.06, 3), 1.05)
print(f"Measured lambda: {measured_lambda}")
print()

low_idle = {
    'lambda': measured_lambda,
    'co': test_gases['co'],
    'co2': test_gases['co2'],
    'hc': test_gases['hc'],
    'o2': test_gases['o2'],
    'nox': 50
}

logic = "measured_lambda > calculated_lambda + 0.05 and low_idle.o2 > 2.0"
context = {
    'low_idle': low_idle,
    'calculated_lambda': calc_lambda,
    'measured_lambda': measured_lambda,
    'high_idle': None
}
result = _safe_eval(logic, context)
print(f"P_003 condition: {result}")

# Also check other requirements: P_003 is at row index 2 in the matrix.
# Let's also check that P_003 matches before any earlier case that might also match.