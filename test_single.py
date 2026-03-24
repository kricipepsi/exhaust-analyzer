from generate_aligned_100 import gen_catalyst
from core.matrix import match_case
from core.bretschneider import calculate_lambda
import json

kb = json.load(open('data/expanded_knowledge_base.json'))
case = gen_catalyst()
low_idle = {
    'lambda': float(case['OBD_Lambda']),
    'co': float(case['CO_Pct']),
    'co2': float(case['CO2_Pct']),
    'hc': int(case['HC_PPM']),
    'o2': float(case['O2_Pct']),
    'nox': int(float(case['NOx_PPM']))
}
fuel_type = case['Fuel'].lower() if case['Fuel'].lower() in ['e0','e5','e10','e85'] else 'e10'
calc = calculate_lambda(co=low_idle['co'], co2=low_idle['co2'], hc_ppm=low_idle['hc'], o2=low_idle['o2'], fuel_type=fuel_type)
calc_lambda = calc['lambda']
dtc_list = [case['OBD_DTC']] if case['OBD_DTC'] != 'None' else []
tier4_low = {'0C':0, '06': float(case['OBD_STFT']), '07': float(case['OBD_LTFT']), '44': float(case['OBD_Lambda']), '10':0, '0B':0, '11':0}
matched = match_case(low_idle, calc_lambda, low_idle['lambda'], kb, None, dtc_list, None, tier4_low, None)
print("Expected:", case['Expected_Result'])
print("Actual:", matched.get('name'))
print("Match:", matched.get('name') == case['Expected_Result'])