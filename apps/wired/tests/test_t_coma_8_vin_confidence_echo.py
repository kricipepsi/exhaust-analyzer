"""T-COMA-8 (F-C1-9): execution_meta.vin_confidence echoes the decode grade instead of a hard-coded "HIGH".

Tags: NEW fails on the base (every completed run said HIGH).
"""

from __future__ import annotations

import pytest
from test_t_aud_1a_inputs import DECODABLE_VIN, GAS, OBD, TRIAGE

from wired.composition import diagnose


@pytest.mark.parametrize(("vin", "grade"), [(DECODABLE_VIN, "PARTIAL"), ("UNKNOWNVIN0000000", "NONE")])
def test_completed_run_echoes_the_vin_grade(vin, grade):
    """NEW: a PARTIAL decode and the no-VIN fallback (NONE) are shown as such, not as HIGH."""
    res = diagnose({"vin": vin, "triage": TRIAGE, "gas": GAS, "obd": dict(OBD)})
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"  # precondition: the full pipeline ran
    assert res.execution_meta.vin_confidence == grade
