"""P4 probes for GASLab survivors. Run from labs/gaslab:
  cd labs/gaslab && python -m pytest -q -p no:cacheprovider ../../audit/scratch/P4/probes/test_p4_gaslab_probes.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "labs/gaslab/tests/unit"))
from test_resolution import _dna, _reading  # noqa: E402
from gaslab.brettschneider import lambda_chem  # noqa: E402
from gaslab.ontology_loader import load_ontology  # noqa: E402
from gaslab.resolution import apply_differentiators  # noqa: E402


def test_catalyst_weak_delta_needs_weak_idle_and_working_high():
    """Kills resolution.py:551 `idle_is_weak and high_is_working` -> `or` (mutant
    gas.apply_differentiators#0463). wiki 07 Step 2: 'Weak / degraded' needs the 2500 RPM working box AND
    the idle 'distinct divergence' box. A healthy idle (no delta) must not keep CATALYST_NOT_LIGHTING_OFF."""
    idle = _reading(hc=10, co=0.2, co2=15.0, o2=0.2, nox=50)          # healthy, not 'weak'
    high = _reading(hc=20, co=0.1, co2=15.5, o2=0.2, nox=50)          # 'working' at 2500
    assert 0.98 <= lambda_chem(idle) <= 1.02 and 0.98 <= lambda_chem(high) <= 1.02, (
        lambda_chem(idle), lambda_chem(high))                         # fuel-control precondition holds
    out = apply_differentiators(["CATALYST_NOT_LIGHTING_OFF"], idle, _dna(), load_ontology(),
                                reading_high=high)
    assert "CATALYST_NOT_LIGHTING_OFF" not in out, out


def test_collision_triangle_14_to_16_is_rich_misfire():
    """Kills rule_engine.py:348 guard deletion (mutant gas._definitive_match#0136). wiki 04 §4.9
    RULE_COLLISION: 'CO > tier_max AND O2 > 2.0 % AND triangle 14 - 16 % => RICH_MISFIRE'. The suite only
    tests the > 16 % arm (test_collision_routes_to_external_o2)."""
    from test_rule_engine import _dna as _dna_re, _reading as _reading_re
    from gaslab.contracts import EngineStateBucket
    from gaslab.rule_engine import ChemicalSignature, classify

    reading = _reading_re(hc=50, co=3.0, co2=10.0, o2=2.5, nox=50)     # triangle 15.5 %
    chem, _validity = classify(reading, _dna_re(), EngineStateBucket.STABILIZED_IDLE, load_ontology())
    assert chem == ChemicalSignature.RICH_MISFIRE, chem
