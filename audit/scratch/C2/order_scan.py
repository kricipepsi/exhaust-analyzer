"""Rule-order dependence scan: classify the same readings with the ontology `faults` mapping
in file order and in reversed order; report any verdict that changes.

Usage (repo root): python audit/scratch/C2/order_scan.py [N]
Deterministic (seeded). Audit scratch only.
"""

from __future__ import annotations

import copy
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _c2 import IDLE, ONT, R, dna, run  # noqa: E402
from gaslab.contracts import EngineStateBucket  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
rng = random.Random(7)

REV = copy.deepcopy(ONT)
REV["faults"] = dict(reversed(list(ONT["faults"].items())))

DNAS = [
    dna(),
    dna(fuel_delivery_type="GDI", egr_equipped=True),
    dna(induction_type="forced", euro_emission_category="EURO_2", has_catalyst=False),
]


def rand_reading():
    # draw inside the triangle gate (sum 14-18) so the bound-matching path is exercised
    total = rng.uniform(14.0, 18.0)
    co = round(rng.uniform(0, 7), 2)
    o2 = round(rng.uniform(0, min(6, total - co - 6.5)), 2)
    co2 = round(total - co - o2, 2)
    return R(int(rng.uniform(0, 2500)), co, co2, o2, int(rng.uniform(0, 1500)))


diffs = 0
examples = []
for i in range(N):
    r = rand_reading()
    hi = rand_reading() if i % 2 else None
    d = DNAS[i % len(DNAS)]
    state = IDLE if i % 5 else EngineStateBucket.REGULATORY_HIGH_IDLE
    a = run(r, d, state, ONT, reading_high=hi)
    b = run(r, d, state, REV, reading_high=hi)
    if a != b:
        diffs += 1
        if len(examples) < 5:
            examples.append((r, hi, d.fuel_delivery_type, state.value, a, b))
print(f"readings={N} verdict_changes_under_reversed_order={diffs}")
for e in examples:
    print(e)
