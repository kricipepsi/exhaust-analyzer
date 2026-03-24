"""Bretschneider formula implementation for lambda calculation.

Uses the exact formula from ARCHIVE/engine/chemistry.py
"""

from typing import Dict

# Fuel constants for petrol variants (from standard diagnostic reference tables)
# Hcv = hydrogen-to-carbon ratio, Ocv = oxygen-to-carbon ratio
# Midpoint values used where a range is specified
FUEL_DATA = {
    "e0":  {"hcv": 1.885, "ocv": 0.000, "stoich": 14.7},
    "e5":  {"hcv": 1.915, "ocv": 0.016, "stoich": 14.45},
    "e10": {"hcv": 2.005, "ocv": 0.054, "stoich": 14.1},
    "e85": {"hcv": 2.77,  "ocv": 0.385, "stoich": 9.7},
}

K1 = 3.5  # Water-gas shift constant


def calculate_lambda(co: float, co2: float, hc_ppm: int, o2: float, fuel_type: str = "e10") -> Dict[str, float]:
    """
    Calculate lambda, AFR, and stoichiometric ratio using the Brettschneider equation.

    Args:
        co: Carbon Monoxide (volume %)
        co2: Carbon Dioxide (volume %)
        hc_ppm: Hydrocarbons (ppm)
        o2: Oxygen (volume %)
        fuel_type: 'e0', 'e5', 'e10', or 'e85'

    Returns:
        dict with keys: 'lambda', 'afr', 'stoich'

    Formula (from ARCHIVE/engine/chemistry.py):
        - hc_pct = hc_ppm / 10000
        - if co2 == 0: co2 = 0.001
        - water_gas_factor = (Hcv/4) * (K1/(K1 + co/co2)) - (Ocv/2)
        - numerator = co2 + co/2 + o2 + water_gas_factor * (co2 + co)
        - denominator = (1 + Hcv/4 - Ocv/2) * (co2 + co + hc_pct)
        - lambda = numerator / denominator
        - afr = lambda * stoich
    """
    # Get fuel constants
    fuel = FUEL_DATA.get(fuel_type.lower(), FUEL_DATA["e10"])
    Hcv = fuel["hcv"]
    Ocv = fuel["ocv"]
    stoich = fuel["stoich"]

    # Convert HC from ppm to percentage
    hc_pct = hc_ppm / 10000.0

    # Protect against division by zero
    if co2 == 0:
        co2 = 0.001

    # Water-gas shift factor
    water_gas_factor = (Hcv / 4.0) * (K1 / (K1 + (co / co2))) - (Ocv / 2.0)

    # Numerator: CO2 + CO/2 + O2 + water_gas_factor*(CO2 + CO)
    numerator = co2 + (co / 2.0) + o2 + (water_gas_factor * (co2 + co))

    # Denominator: (1 + Hcv/4 - Ocv/2) * (CO2 + CO + HC_pct)
    denominator = (1.0 + (Hcv / 4.0) - (Ocv / 2.0)) * (co2 + co + hc_pct)

    if denominator == 0:
        lambda_val = 0.0
    else:
        lambda_val = numerator / denominator

    afr = lambda_val * stoich

    return {
        "lambda": round(lambda_val, 3),
        "afr": round(afr, 2),
        "stoich": stoich
    }
