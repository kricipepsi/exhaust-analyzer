"""C1 audit probes — path setup only (evidence, never product code).

Puts labs/comlab on sys.path so ``registry.integration_shim`` resolves the same
way labs/comlab's own pytest run resolves it (rootdir insertion).
"""
import sys
from pathlib import Path

_COMLAB = Path(__file__).resolve().parents[3] / "labs" / "comlab"
if str(_COMLAB) not in sys.path:
    sys.path.insert(0, str(_COMLAB))
