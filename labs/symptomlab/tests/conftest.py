from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from symptomlab.models import (
    EngineState,
    EnvironmentalConditions,
    LoadState,
    OccursDuring,
    SymptomDNA,
)
from symptomlab.validator import SymptomValidator

_FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def good_allowed_path() -> Path:
    return _FIXTURE_DIR / "allowed_combinations.good21.yaml"


@pytest.fixture(scope="module")
def bad_allowed_path() -> Path:
    return _FIXTURE_DIR / "allowed_combinations.bad17.yaml"


@pytest.fixture(scope="module")
def validator(good_allowed_path: Path) -> SymptomValidator:
    return SymptomValidator(good_allowed_path)


@pytest.fixture(scope="module")
def allowed_pairs(good_allowed_path: Path) -> list[tuple[str, str]]:
    with open(good_allowed_path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    return [
        (tier_1, tier_2)
        for tier_1, tier_2_list in doc["combinations"].items()
        for tier_2 in tier_2_list
    ]


@pytest.fixture
def make_symptom_dna() -> Callable[..., SymptomDNA]:
    def _make_symptom_dna(**overrides: object) -> SymptomDNA:
        values = {
            "tier_1_primary_symptom": "visible_exhaust_smoke",
            "tier_2_subfield_filter": "black_smoke",
            "environmental_conditions": EnvironmentalConditions(
                occurs_during=OccursDuring.ALWAYS,
                engine_state=EngineState.RUNNING,
                load_state=LoadState.IDLE,
            ),
            "free_text_notes": None,
        } | overrides
        return SymptomDNA(**values)  # type: ignore[arg-type]

    return _make_symptom_dna
