"""T-AUD-4j: the UI tags a tier pair with a key the symptom prior knows (F-C5-4)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

import ui_payload as up

PRIOR = Path(__file__).resolve().parents[3] / "labs/comlab/comlab/config/symptom_prior.yaml"


def _tag(tier_1: str, tier_2: str, engine: str) -> Any:
    widgets = {
        "vin": "",
        "dna_module": True,
        "triage_tier_1": tier_1,
        "triage_tier_2": tier_2,
        "triage_occurs_during": "Always",
        "triage_engine_state": engine,
    }
    return up.build_diagnose_payload(widgets)["triage"].get("csv_primary_symptom")


_CASES = [
    ("🔧 Rough Idle / Shudder", "Constant shudder / vibration", "Running", "running_rough"),
    ("🚫 Vehicle Won't Start", "Normal crank / zero RPM (prolonged crank)", "Won't start", "non_starter"),
    ("🚫 Vehicle Won't Start", "Normal crank / zero RPM (prolonged crank)", "Running", "hard_start_cold"),
]


@pytest.mark.parametrize(("tier_1", "tier_2", "engine", "expected"), _CASES)
def test_tier_pair_tag(tier_1: str, tier_2: str, engine: str, expected: str) -> None:
    assert _tag(tier_1, tier_2, engine) == expected


def test_every_ui_tag_is_a_prior_key() -> None:
    keys = set(yaml.safe_load(PRIOR.read_text(encoding="utf-8"))["mappings"])
    tags = {_tag(t1, t2, eng) for t1, t2, eng, _ in _CASES}
    assert tags <= keys
