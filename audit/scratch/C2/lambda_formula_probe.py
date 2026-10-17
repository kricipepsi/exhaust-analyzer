"""Compare gaslab.lambda_chem with the wiki §2.3 / vocab §6 printed formula, evaluated literally.

Usage (repo root): python audit/scratch/C2/lambda_formula_probe.py
Audit scratch only.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _c2 import R, lam  # noqa: E402

HCV = 1.85  # vocab §6 constant table


def wiki_literal(r):
    """GASWIKI-02 §2.3 / GAS_VOCABULARY §6 numerator/denominator exactly as printed (HC in ppm*0.0025)."""
    co2, co, o2 = r.co2, r.co, r.o2
    num = co2 + co / 2 + o2 + (HCV / 4 * co2 / (co2 + co)) * co2
    den = co2 + co + r.hc * 0.0025
    return round(num / den, 4)


cases = {
    "healthy stoich (NORMAL vector)": R(20, 0.2, 15.0, 0.2, 50),
    "WORN_VALVE_SEALS wiki idle (λ 0.95-0.97)": R(400, 1.0, 13.0, 0.3, 50),
    "WORN_PISTON_RINGS wiki 2500 (λ <0.99)": R(350, 0.8, 13.0, 0.5, 100),
}
for k, r in cases.items():
    print(f"{k:42s} code lambda_chem={lam(r):.4f}  wiki-formula-literal={wiki_literal(r):.4f}")
