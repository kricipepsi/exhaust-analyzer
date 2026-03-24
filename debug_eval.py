#!/usr/bin/env python3
from core.matrix import _safe_eval
from core.bretschneider import calculate_lambda

low_idle = {
    'lambda': 1.126,
    'co': 1.0,
    'co2': 12.0,
    'hc': 500,
    'o2': 2.0,
    'nox': 50
}
calc_lambda = 1.066
measured_lambda = 1.126

logic = "measured_lambda > calculated_lambda + 0.05 and low_idle.o2 > 2.0"
context = {
    'low_idle': low_idle,
    'calculated_lambda': calc_lambda,
    'measured_lambda': measured_lambda,
    'high_idle': None
}
print("Context:", context)
print("Logic:", logic)
result = _safe_eval(logic, context)
print("Result:", result)