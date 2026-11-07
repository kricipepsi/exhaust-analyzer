"""T-AUD-10c (F-C5-12): apps/ui/app.py imports no lab; it decodes the VIN through wired.

Tags: NEW fails on the base fix/T-AUD-10e (`import vinlab` in the VIN Lookup block).
"""

from __future__ import annotations

import re
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"
LABS = r"(vinlab|gaslab|obdlab|dtclab|comlab|dnalab|symptomlab)"


def test_app_imports_no_lab() -> None:
    """NEW: no import line of app.py names a lab package (the audit probe test_f12_ regex)."""
    text = APP.read_text(encoding="utf-8")
    assert re.findall(rf"^\s*(?:import|from)\s+{LABS}\b.*$", text, re.M) == []
    assert re.findall(rf"\b{LABS}\.", text) == []


def test_app_decodes_through_wired() -> None:
    """NEW: decode_vehicle comes from wired.composition and decodes the typed VIN."""
    text = APP.read_text(encoding="utf-8")
    assert "from wired.composition import decode_vehicle, diagnose\n" in text
    assert text.count("dna = decode_vehicle(vin_input)") == 1
