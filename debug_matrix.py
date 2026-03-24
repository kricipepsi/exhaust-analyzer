"""Debug matrix matching."""

from core.matrix import _safe_eval
import json

kb = json.load(open('data/master_knowledge_base.json', 'r'))

# Find P_100 case
p100 = next(c for c in kb['diagnostic_matrix'] if c['case_id'] == 'P_100')
print("P_100 logic:", p100['logic'])

low_idle = {'lambda': 1.00, 'co': 0.10, 'co2': 15.1, 'hc': 20, 'o2': 0.15}
context = {
    'low_idle': low_idle,
    'calculated_lambda': 1.00,
    'measured_lambda': 1.00,
    'high_idle': {'co': 0.10, 'co2': 15.1, 'hc': 20, 'o2': 0.15, 'lambda': 1.00, 'nox': 50}
}

result = _safe_eval(p100['logic'], context)
print("Evaluation result:", result)
print("Context:", context)
