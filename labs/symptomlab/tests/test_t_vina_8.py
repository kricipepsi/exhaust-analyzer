"""T-VINA-8: SymptomLab refuses a non-string tier with SymptomValidationError (F-C6-13)."""
from __future__ import annotations

import pytest
from symptomlab import resolve
from symptomlab.models import SymptomDNA, SymptomValidationError

GOOD = dict(occurs_during="always", engine_state="running", load_state="idle")


def _payload():
    return resolve("rough_idle_shudder", "surging_hunting_idle", **GOOD).to_json_payload()


def test_from_json_round_trips():
    p = _payload()
    assert SymptomDNA.from_json(p).to_json_payload() == p


@pytest.mark.parametrize("tier_1,tier_2", [
    (["rough_idle_shudder"], "surging_hunting_idle"),
    ({"x": 1}, "surging_hunting_idle"),
    ("rough_idle_shudder", ["surging_hunting_idle"]),
    (None, "surging_hunting_idle"),
])
def test_non_string_tier_is_validation_error(tier_1, tier_2):
    with pytest.raises(SymptomValidationError, match="must be strings"):
        resolve(tier_1, tier_2, **GOOD)
