"""Reachability scan: sample each ontology fault's own signature box, classify, count self-hits.

Usage (repo root): python audit/scratch/C2/reach_scan.py [N]
Deterministic (seeded). Audit scratch only.
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _c2 import ONT, R, dna, run  # noqa: E402
from gaslab.brettschneider import lambda_chem  # noqa: E402
from gaslab.validity_gates import sample_validity  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
rng = random.Random(20261017)


def dna_for(name: str):
    kw = {}
    if name.startswith("GDI_"):
        kw["fuel_delivery_type"] = "GDI"
    if name.startswith("EGR_"):
        kw["egr_equipped"] = True
    return dna(**kw)


def clip(lo, hi, cap):
    return lo, min(hi, cap)


print(f"{'fault':38s} {'in-box&valid':>12s} {'self-hit':>8s}  top verdicts")
for name, entry in ONT["faults"].items():
    if name == "SAMPLE_INVALID":
        continue
    sig = entry["signature"]
    d = dna_for(name)
    valid = 0
    hits = 0
    verdicts: Counter = Counter()
    for _ in range(N):
        hc = int(rng.uniform(*clip(sig["hc"]["min"], sig["hc"]["max"], 3000)))
        co = round(rng.uniform(sig["co"]["min"], sig["co"]["max"]), 2)
        co2 = round(rng.uniform(sig["co2"]["min"], sig["co2"]["max"]), 2)
        o2 = round(rng.uniform(*clip(sig["o2"]["min"], sig["o2"]["max"], 8.0)), 2)
        nox = int(rng.uniform(sig["nox"]["min"], sig["nox"]["max"]))
        r = R(hc, co, co2, o2, nox)
        lam = lambda_chem(r)
        if not (sig["lambda"]["min"] <= lam <= sig["lambda"]["max"]):
            continue
        if sample_validity(r).value == "INVALID":
            continue
        valid += 1
        v, _ = run(r, d)
        verdicts[v] += 1
        hits += v == name
    top = ", ".join(f"{k}:{c}" for k, c in verdicts.most_common(3))
    print(f"{name:38s} {valid:12d} {hits:8d}  {top}")
