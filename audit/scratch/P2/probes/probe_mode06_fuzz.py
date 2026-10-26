"""Probe: what DataFusionSanitizer.sanitize returns for the six inputs of dtclab test_mode06_fuzz.

Run (repo root): python audit/scratch/P2/probes/probe_mode06_fuzz.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "labs/dtclab"))
from tests.generative.test_fuzz import _MODE06_FUZZ, make_freeze_frame_raw  # noqa: E402
from dtclab.core.data_fusion_sanitizer import DataFusionSanitizer  # noqa: E402

for label, key, margin in _MODE06_FUZZ:
    try:
        out = DataFusionSanitizer(dna_view=None).sanitize(
            {"$03": ["P0171"], "$07": [], "$0A": []}, make_freeze_frame_raw(), {key: margin})
        d = out.model_dump() if hasattr(out, "model_dump") else out
        m06 = {k: v for k, v in d.items() if "06" in k.lower() or "monitor" in k.lower()}
        print(f"{label:26s} RETURNED  {m06}")
    except (ValueError, TypeError) as e:
        print(f"{label:26s} RAISED    {type(e).__name__}: {str(e).splitlines()[0][:100]}")

# Mutation: replace sanitize with a function that accepts everything and returns nothing.
# If test_mode06_fuzz could detect a fail-open regression, at least one call below would fail.
from tests.generative import test_fuzz as T  # noqa: E402

orig = DataFusionSanitizer.sanitize
DataFusionSanitizer.sanitize = lambda self, *a, **k: None  # fail-open mutant
passed = 0
for label, key, margin in _MODE06_FUZZ:
    T.test_mode06_fuzz(label, key, margin)
    passed += 1
DataFusionSanitizer.sanitize = orig
print(f"fail-open mutant: test_mode06_fuzz passed {passed}/{len(_MODE06_FUZZ)} cases")
