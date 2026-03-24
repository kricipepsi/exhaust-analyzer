#!/usr/bin/env python3
from core.bretschneider import calculate_lambda
calc = calculate_lambda(co=0.15, co2=13.0, hc_ppm=800, o2=3.0, fuel_type='e10')
print(f"Calculated lambda: {calc['lambda']}")
print(f"Measured lambda: 1.12")
print(f"Delta: {1.12 - calc['lambda']:.3f}")

# Check P_003 logic
logic = "measured_lambda > calculated_lambda + 0.05 and low_idle.o2 > 2.0"
context = {
    'low_idle': {'lambda': 1.12, 'o2': 3.0, 'co': 0.15, 'co2': 13.0, 'hc': 800, 'nox': 50},
    'calculated_lambda': calc['lambda'],
    'measured_lambda': 1.12,
    'high_idle': None
}
from core.matrix import _safe_eval
result = _safe_eval(logic, context)
print(f"P_003 evaluates: {result}")

# Check P_004 logic (EGR Stuck Open)
logic4 = "low_idle.o2 > 2.0 and low_idle.o2 < 6.0 and low_idle.co > 2.0 and low_idle.co < 7.0 and low_idle.hc > 1000 and low_idle.hc < 7000 and low_idle.nox < 100"
result4 = _safe_eval(logic4, context)
print(f"P_004 evaluates: {result4}")