#!/usr/bin/env python3
"""Generate a robust 100-case petrol diagnostic test suite.

This creates test cases that match the expected diagnostic categories
implemented in the knowledge base, with realistic gas readings and
optional OBD/PID data for future modules.
"""

import csv
import math
from pathlib import Path

# Bretschneider constants for different fuels
FUEL_DATA = {
    'e0':  {'hcv': 1.885, 'ocv': 0.000, 'stoich': 14.7},
    'e5':  {'hcv': 1.915, 'ocv': 0.016, 'stoich': 14.45},
    'e10': {'hcv': 2.005, 'ocv': 0.054, 'stoich': 14.1},
    'e85': {'hcv': 2.77,  'ocv': 0.385, 'stoich': 9.7},
}

K1 = 3.5

def calculate_lambda(co, co2, hc_ppm, o2, fuel='e10'):
    """Calculate lambda using Bretschneider formula."""
    fuel = FUEL_DATA.get(fuel.lower(), FUEL_DATA['e10'])
    Hcv, Ocv = fuel['hcv'], fuel['ocv']
    hc_pct = hc_ppm / 10000.0
    if co2 == 0:
        co2 = 0.001
    water_gas_factor = (Hcv / 4.0) * (K1 / (K1 + (co / co2))) - (Ocv / 2.0)
    numerator = co2 + (co / 2.0) + o2 + (water_gas_factor * (co2 + co))
    denominator = (1.0 + (Hcv / 4.0) - (Ocv / 2.0)) * (co2 + co + hc_pct)
    if denominator == 0:
        return 1.0
    lambda_val = numerator / denominator
    return round(lambda_val, 3)

def generate_test_suite():
    """Generate 100 test cases covering various petrol fault scenarios."""
    cases = []

    # Helper to add a case
    def add_case(idx, fuel, co, co2, hc, o2, nox, lambda_gas, stft, ltft, obd_lambda, dtc, expected, confidence, health):
        cases.append({
            'ID': str(idx),
            'Fuel': fuel,
            'CO_Pct': f"{co:.2f}",
            'CO2_Pct': f"{co2:.1f}",
            'HC_PPM': str(int(hc)),
            'O2_Pct': f"{o2:.2f}",
            'NOx_PPM': str(int(nox)),
            'Lambda_Gas': f"{lambda_gas:.2f}",
            'OBD_STFT': f"{stft:.1f}",
            'OBD_LTFT': f"{ltft:.1f}",
            'OBD_Lambda': f"{obd_lambda:.2f}",
            'OBD_DTC': dtc if dtc else 'None',
            'Expected_Result': expected,
            'Confidence_Score': str(int(confidence)),
            'ECU_Health': str(int(health))
        })

    # 1-10: Healthy Engine baseline (different fuels, slight variations)
    add_case(1, 'Petrol', 0.10, 15.2, 12, 0.30, 25, 1.00, 0, 2, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(2, 'Petrol', 0.05, 15.5, 5, 0.10, 15, 1.00, -1, 0, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(3, 'Petrol', 0.15, 14.9, 20, 0.40, 30, 1.00, 1, 3, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(4, 'Petrol', 0.08, 15.0, 8, 0.20, 20, 1.00, -2, 1, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(5, 'E85', 0.02, 13.0, 15, 0.50, 50, 1.00, 0, 0, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(6, 'E10', 0.12, 14.8, 25, 0.35, 35, 1.00, 2, 4, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(7, 'Petrol', 0.10, 15.1, 10, 0.25, 28, 1.00, -1, 2, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(8, 'Petrol', 0.20, 14.7, 30, 0.30, 22, 1.00, 1, 3, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(9, 'Petrol', 0.05, 15.3, 8, 0.15, 18, 1.00, 0, 1, 1.00, None, 'Healthy_Engine', 100, 100)
    add_case(10, 'Petrol', 0.12, 14.9, 15, 0.28, 26, 1.00, -1, 2, 1.00, None, 'Healthy_Engine', 100, 100)

    # 11-20: Vacuum Leak (high O2, high HC, lambda > 1.05)
    add_case(11, 'Petrol', 0.10, 11.5, 450, 4.50, 120, 1.20, 18, 12, 1.18, 'P0171', 'Vacuum_Leak', 90, 95)
    add_case(12, 'Petrol', 0.08, 12.0, 380, 4.00, 100, 1.15, 15, 10, 1.15, 'P0171', 'Vacuum_Leak', 90, 95)
    add_case(13, 'Petrol', 0.12, 10.5, 520, 5.20, 150, 1.25, 20, 14, 1.22, 'P0174', 'Vacuum_Leak', 90, 95)
    add_case(14, 'Petrol', 0.05, 13.0, 300, 3.50, 80, 1.12, 12, 8, 1.12, 'P0171', 'Vacuum_Leak', 90, 95)
    add_case(15, 'Petrol', 0.15, 11.0, 600, 5.00, 130, 1.30, 22, 16, 1.25, 'P0171', 'Vacuum_Leak', 90, 95)
    add_case(16, 'Petrol', 0.10, 12.5, 250, 2.50, 90, 1.10, 10, 6, 1.10, None, 'Vacuum_Leak', 70, 90)
    add_case(17, 'Petrol', 0.20, 10.0, 450, 6.00, 200, 1.40, 25, 20, 1.35, 'P0171', 'Vacuum_Leak', 90, 95)
    add_case(18, 'Petrol', 0.08, 13.0, 280, 4.00, 100, 1.18, 14, 9, 1.16, 'P0174', 'Vacuum_Leak', 90, 95)
    add_case(19, 'Petrol', 0.12, 11.8, 350, 4.80, 140, 1.22, 18, 11, 1.20, None, 'Vacuum_Leak', 70, 90)
    add_case(20, 'Petrol', 0.05, 12.8, 420, 3.80, 110, 1.15, 16, 13, 1.14, 'P0171', 'Vacuum_Leak', 90, 95)

    # 21-30: Rich Mixture (high CO, high HC, low O2, lambda < 0.95)
    add_case(21, 'Petrol', 4.50, 12.5, 180, 0.20, 30, 0.85, -15, -10, 0.86, 'P0172', 'Rich_Mixture', 85, 95)
    add_case(22, 'Petrol', 6.00, 10.0, 250, 0.10, 20, 0.75, -20, -15, 0.78, 'P0172', 'Rich_Mixture', 85, 95)
    add_case(23, 'Petrol', 3.80, 13.0, 150, 0.30, 40, 0.90, -12, -8, 0.90, 'P0172', 'Rich_Mixture', 85, 95)
    add_case(24, 'Petrol', 5.20, 11.5, 200, 0.15, 25, 0.82, -18, -12, 0.84, None, 'Rich_Mixture', 70, 90)
    add_case(25, 'Petrol', 4.00, 12.0, 120, 0.25, 35, 0.88, -10, -6, 0.88, 'P0172', 'Rich_Mixture', 85, 95)
    add_case(26, 'Petrol', 7.00, 9.0, 300, 0.05, 15, 0.70, -22, -18, 0.72, 'P0172', 'Rich_Mixture', 85, 95)
    add_case(27, 'Petrol', 3.50, 13.2, 180, 0.35, 45, 0.92, -8, -5, 0.92, None, 'Rich_Mixture', 70, 90)
    add_case(28, 'Petrol', 5.50, 10.8, 220, 0.12, 22, 0.78, -16, -11, 0.80, 'P0172', 'Rich_Mixture', 85, 95)
    add_case(29, 'Petrol', 4.20, 12.2, 160, 0.22, 32, 0.86, -14, -9, 0.87, None, 'Rich_Mixture', 70, 90)
    add_case(30, 'Petrol', 6.50, 10.5, 280, 0.10, 18, 0.72, -20, -16, 0.74, 'P0172', 'Rich_Mixture', 85, 95)

    # 31-40: Ignition Misfire (high HC, moderate CO, high O2)
    add_case(31, 'Petrol', 0.50, 10.0, 1200, 5.00, 20, 1.25, 10, 5, 1.20, 'P0300', 'Ignition_Misfire', 95, 95)
    add_case(32, 'Petrol', 0.30, 11.0, 1500, 4.50, 15, 1.20, 8, 4, 1.18, 'P0301', 'Ignition_Misfire', 95, 95)
    add_case(33, 'Petrol', 0.60, 9.5, 2000, 5.50, 10, 1.30, 12, 6, 1.25, 'P0302', 'Ignition_Misfire', 95, 95)
    add_case(34, 'Petrol', 0.40, 10.5, 1100, 4.80, 18, 1.18, 9, 5, 1.16, 'P0303', 'Ignition_Misfire', 95, 95)
    add_case(35, 'Petrol', 0.55, 9.8, 1700, 5.20, 12, 1.28, 11, 7, 1.22, None, 'Ignition_Misfire', 90, 90)
    add_case(36, 'Petrol', 0.35, 10.8, 1300, 4.20, 22, 1.15, 7, 3, 1.14, 'P0300', 'Ignition_Misfire', 95, 95)
    add_case(37, 'Petrol', 0.70, 9.0, 2200, 5.80, 8, 1.35, 14, 8, 1.28, 'P0304', 'Ignition_Misfire', 95, 95)
    add_case(38, 'Petrol', 0.45, 10.2, 1400, 4.60, 25, 1.22, 10, 6, 1.20, None, 'Ignition_Misfire', 90, 90)
    add_case(39, 'Petrol', 0.60, 9.2, 1800, 5.00, 15, 1.25, 12, 7, 1.24, 'P0300', 'Ignition_Misfire', 95, 95)
    add_case(40, 'Petrol', 0.30, 11.2, 1000, 4.00, 30, 1.12, 6, 2, 1.10, 'P0300', 'Ignition_Misfire', 95, 95)

    # 41-50: NOx issues (high NOx, often with specific lambda)
    add_case(41, 'Petrol', 0.10, 15.0, 20, 0.20, 1500, 1.00, 0, 0, 1.00, None, 'High_NOx', 70, 85)
    add_case(42, 'Petrol', 0.08, 15.5, 15, 0.15, 1200, 1.00, 2, 1, 1.00, None, 'High_NOx', 70, 85)
    add_case(43, 'Petrol', 0.12, 14.5, 25, 0.25, 2000, 1.00, -1, 0, 1.00, None, 'High_NOx', 70, 85)
    add_case(44, 'Petrol', 0.15, 14.0, 30, 0.30, 1800, 1.00, 0, 0, 1.00, None, 'High_NOx', 70, 85)
    add_case(45, 'Petrol', 0.05, 16.0, 10, 0.10, 1000, 1.00, -2, 2, 1.00, None, 'High_NOx', 70, 85)
    add_case(46, 'Petrol', 0.10, 15.2, 18, 0.22, 1300, 1.00, 1, 3, 1.00, None, 'High_NOx', 70, 85)
    add_case(47, 'Petrol', 0.08, 14.8, 12, 0.18, 1600, 1.00, -1, 1, 1.00, None, 'High_NOx', 70, 85)
    add_case(48, 'Petrol', 0.12, 14.2, 22, 0.28, 2200, 1.00, 0, 0, 1.00, None, 'High_NOx', 70, 85)
    add_case(49, 'Petrol', 0.10, 15.0, 16, 0.20, 2500, 1.00, -2, -1, 1.00, None, 'High_NOx', 70, 85)
    add_case(50, 'Petrol', 0.15, 13.8, 28, 0.35, 1900, 1.00, 1, 0, 1.00, None, 'High_NOx', 70, 85)

    # 51-60: Catalyst Efficiency Issues (based on NOx patterns, but we'll have separate catalyst case)
    add_case(51, 'Petrol', 0.50, 12.0, 200, 1.00, 800, 1.00, 0, 0, 1.00, 'P0420', 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(52, 'Petrol', 0.80, 11.0, 300, 1.20, 900, 1.00, 5, 3, 1.00, 'P0420', 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(53, 'Petrol', 0.40, 12.5, 150, 0.80, 1000, 1.00, 0, 0, 1.00, 'P0430', 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(54, 'Petrol', 0.60, 11.5, 250, 1.10, 1200, 1.00, 3, 2, 1.00, 'P0420', 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(55, 'Petrol', 0.30, 13.0, 120, 0.60, 850, 1.00, -2, 1, 1.00, None, 'Catalyst_Efficiency_Failure', 40, 75)
    add_case(56, 'Petrol', 0.70, 10.5, 350, 1.50, 1100, 1.00, 6, 4, 1.00, 'P0420', 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(57, 'Petrol', 0.45, 12.2, 180, 0.90, 950, 1.00, 2, 1, 1.00, 'P0430', 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(58, 'Petrol', 0.55, 11.8, 220, 1.30, 1300, 1.00, 4, 3, 1.00, None, 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(59, 'Petrol', 0.35, 12.8, 160, 0.70, 750, 1.00, 0, 0, 1.00, 'P0420', 'Catalyst_Efficiency_Failure', 40, 80)
    add_case(60, 'Petrol', 0.65, 11.2, 270, 1.40, 1150, 1.00, 5, 4, 1.00, 'P0430', 'Catalyst_Efficiency_Failure', 40, 80)

    # 61-70: Exhaust Leak Pre-Cat (high O2, but lambda around 1)
    add_case(61, 'Petrol', 0.10, 15.0, 20, 6.00, 30, 1.00, 5, 3, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(62, 'Petrol', 0.12, 14.5, 25, 5.50, 25, 1.00, 8, 5, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(63, 'Petrol', 0.08, 15.5, 15, 6.20, 20, 1.00, 4, 2, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(64, 'Petrol', 0.15, 14.0, 30, 5.80, 35, 1.00, 6, 4, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(65, 'Petrol', 0.10, 14.8, 18, 6.10, 28, 1.00, 7, 5, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(66, 'Petrol', 0.12, 15.2, 22, 5.90, 22, 1.00, 9, 6, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(67, 'Petrol', 0.08, 15.0, 12, 6.30, 18, 1.00, 5, 3, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(68, 'Petrol', 0.20, 13.5, 35, 5.50, 40, 1.00, 8, 6, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(69, 'Petrol', 0.10, 14.9, 19, 6.00, 26, 1.00, 6, 4, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)
    add_case(70, 'Petrol', 0.15, 14.2, 28, 5.70, 32, 1.00, 7, 5, 1.00, None, 'Exhaust_Air_Leak_Pre_Cat', 85, 80)

    # 71-80: O2 Sensor Issues (lazy, slow, no response)
    add_case(71, 'Petrol', 0.10, 15.0, 20, 0.20, 25, 1.00, 0, 0, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(72, 'Petrol', 0.10, 15.1, 18, 0.30, 28, 1.00, 10, -10, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(73, 'Petrol', 0.12, 14.8, 22, 0.25, 22, 1.00, 5, -5, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(74, 'Petrol', 0.08, 15.3, 15, 0.15, 20, 1.00, 2, 3, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(75, 'Petrol', 0.15, 14.5, 25, 0.35, 30, 1.00, 8, -8, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(76, 'Petrol', 0.10, 15.0, 20, 0.22, 26, 1.00, 6, -6, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(77, 'Petrol', 0.12, 14.9, 23, 0.28, 24, 1.00, 4, -4, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(78, 'Petrol', 0.09, 15.2, 17, 0.18, 21, 1.00, 1, 1, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(79, 'Petrol', 0.14, 14.6, 27, 0.30, 29, 1.00, 7, -7, 1.00, None, 'O2_Sensor_Aging', 75, 90)
    add_case(80, 'Petrol', 0.11, 15.0, 21, 0.24, 25, 1.00, 3, -3, 1.00, None, 'O2_Sensor_Aging', 75, 90)

    # 81-90: Exhaust Dilution (measured > calculated lambda)
    add_case(81, 'Petrol', 0.05, 15.5, 10, 2.00, 50, 1.12, 5, 3, 1.15, None, 'Exhaust_Dilution', 80, 85)
    add_case(82, 'Petrol', 0.08, 14.8, 15, 3.00, 80, 1.15, 8, 5, 1.18, None, 'Exhaust_Dilution', 80, 85)
    add_case(83, 'Petrol', 0.10, 14.0, 20, 4.00, 100, 1.20, 12, 8, 1.22, None, 'Exhaust_Dilution', 80, 85)
    add_case(84, 'Petrol', 0.06, 15.0, 12, 2.50, 60, 1.10, 6, 4, 1.12, None, 'Exhaust_Dilution', 80, 85)
    add_case(85, 'Petrol', 0.04, 16.0, 8, 1.80, 40, 1.08, 4, 2, 1.10, None, 'Exhaust_Dilution', 80, 85)
    add_case(86, 'Petrol', 0.12, 13.5, 25, 3.50, 90, 1.18, 10, 7, 1.20, None, 'Exhaust_Dilution', 80, 85)
    add_case(87, 'Petrol', 0.08, 15.2, 18, 2.20, 70, 1.14, 7, 5, 1.16, None, 'Exhaust_Dilution', 80, 85)
    add_case(88, 'Petrol', 0.10, 14.5, 22, 3.20, 85, 1.16, 9, 6, 1.18, None, 'Exhaust_Dilution', 80, 85)
    add_case(89, 'Petrol', 0.05, 15.8, 10, 2.10, 55, 1.11, 5, 3, 1.13, None, 'Exhaust_Dilution', 80, 85)
    add_case(90, 'Petrol', 0.15, 13.0, 30, 4.20, 110, 1.22, 14, 10, 1.24, None, 'Exhaust_Dilution', 80, 85)

    # 91-100: Various ECU Logic Faults and Miscellaneous
    add_case(91, 'Petrol', 3.50, 13.0, 150, 0.4, 40, 0.88, 25, 15, 1.15, 'P0171', 'ECU_Logic_Inversion_False_Lean', 95, 20)
    add_case(92, 'Petrol', 0.10, 15.2, 10, 0.2, 30, 1.00, 0, 0, 1.00, 'P0113', 'ECU_Input_Error_Ref_Volt_Drift', 85, 40)
    add_case(93, 'Petrol', 1.50, 13.5, 80, 1.5, 40, 1.05, 0, 0, 1.00, 'P0201', 'ECU_Output_Driver_Hardware_Fail', 90, 30)
    add_case(94, 'Petrol', 0.02, 15.5, 500, 4.5, 10, 1.20, 0, 0, 1.00, None, 'ECU_Misfire_Blindness', 92, 35)
    add_case(95, 'Petrol', 0.05, 15.5, 5, 0.1, 20, 1.00, 0, 0, 1.00, 'P0300', 'Ghost_Misfire_Electrical_Noise', 98, 45)
    add_case(96, 'Petrol', 0.08, 15.2, 10, 0.3, 35, 1.00, 2, -2, 1.00, 'P0171', 'Ghost_Lean_DTC_False_Trigger', 85, 50)
    add_case(97, 'Petrol', 0.10, 15.0, 15, 0.2, 25, 1.00, 0, 0, 1.00, 'P0606', 'ECU_Internal_Checksum_Error', 100, 10)
    add_case(98, 'Petrol', 7.00, 8.0, 400, 0.1, 10, 0.70, -25, -15, 0.75, 'P0172', 'Severe_Intake_Restriction', 95, 95)
    add_case(99, 'Petrol', 0.50, 10.0, 1200, 5.0, 20, 1.25, 10, 5, 1.20, 'P0302', 'Mechanical_Misfire_Spark_Plug', 95, 95)
    add_case(100, 'Petrol', 1.50, 12.0, 80, 1.5, 60, 1.05, 0, 0, 1.00, 'P0420', 'Catalyst_Efficiency_Failure_Alternate', 40, 75)

    return cases

# Generate and write CSV
cases = generate_test_suite()
fieldnames = ['ID', 'Fuel', 'CO_Pct', 'CO2_Pct', 'HC_PPM', 'O2_Pct', 'NOx_PPM', 'Lambda_Gas',
              'OBD_STFT', 'OBD_LTFT', 'OBD_Lambda', 'OBD_DTC', 'Expected_Result',
              'Confidence_Score', 'ECU_Health']

output_path = Path('petrol_diagnostic/test_suite_petrol_100.csv')
with open(output_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases)

print(f"Generated {len(cases)} test cases to {output_path}")
print("\nCategories covered:")
print("- Healthy Engine (10 cases)")
print("- Vacuum Leak (10 cases)")
print("- Rich Mixture (10 cases)")
print("- Ignition Misfire (10 cases)")
print("- High NOx (10 cases)")
print("- Catalyst Efficiency Failure (10 cases)")
print("- Exhaust Air Leak Pre-Cat (10 cases)")
print("- O2 Sensor Aging (10 cases)")
print("- Exhaust Dilution (10 cases)")
print("- ECU/Electrical Faults (10 cases)")
