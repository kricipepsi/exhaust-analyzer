"""Drift-guard tests for obdlab.schemas.dna_view against canonical wiki sources.

OBDLab DNA-view enums source from two wikis:
- obdlab-vocabulary enums (AirMeteringStrategy, O2SensorType, EuroEmissionCategory)
  anchor to OBD_VOCABULARY.md §4.
- cross-contract enums (InductionType, ResolvedHorizon, VinConfidence)
  anchor to SEMANTIC_CONTRACT.md §8.
"""

from pathlib import Path
from typing import NamedTuple

import pytest

from obdlab.schemas.dna_view import (
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)

OBDLAB_ROOT = Path(__file__).resolve().parents[2]  # v2: labs/obdlab (lab root)


# Cross-lab contract anchor (OBD↔COMLab). COMLab migrated into labs/comlab (T-RM-2-COM);
# the current live vocabulary notes live under docs/Vocabulary. Keep the legacy docs/wiki
# fallbacks for old checkouts only.
def _find_comlab_vocab(start: Path) -> Path:
    for anc in start.parents:
        vocab_dir = anc / "labs" / "comlab" / "docs" / "Vocabulary"
        if vocab_dir.is_dir():
            return vocab_dir
    for anc in start.parents:
        wiki_dir = anc / "labs" / "comlab" / "docs" / "wiki"
        if wiki_dir.is_dir():
            return wiki_dir
    for anc in start.parents:
        wiki_dir = anc / "COMLab" / "docs" / "wiki"
        if wiki_dir.is_dir():
            return wiki_dir
    return OBDLAB_ROOT.parents[1] / "labs" / "comlab" / "docs" / "Vocabulary"


COMLAB_VOCAB = _find_comlab_vocab(Path(__file__).resolve())

OBD_VOCABULARY = COMLAB_VOCAB / "OBD_VOCABULARY.md"
SEMANTIC_CONTRACT = COMLAB_VOCAB / "SEMANTIC_CONTRACT.md"


class EnumAnchor(NamedTuple):
    enum_cls: type
    expected_values: list[str]
    wiki_path: Path


DNA_VIEW_ANCHORS = [
    EnumAnchor(AirMeteringStrategy,
               ["DUAL_MAF_MAP_CROSSCHECK", "MAP_ONLY_SPEED_DENSITY", "MAF_ONLY"],
               OBD_VOCABULARY),
    EnumAnchor(O2SensorType,
               ["NARROWBAND_0_TO_1V", "WIDEBAND_LINEAR", "WIDEBAND_NB_SIM"],
               OBD_VOCABULARY),
    EnumAnchor(InductionType,
               ["NATURALLY_ASPIRATED", "TURBOCHARGED"],
               SEMANTIC_CONTRACT),
    EnumAnchor(VinConfidence,
               ["HIGH", "PARTIAL", "NONE"],
               SEMANTIC_CONTRACT),
]


# --- Enum drift guard ---

@pytest.mark.parametrize("anchor", DNA_VIEW_ANCHORS)
def test_dna_enum_member_count(anchor):
    actual = [m.value for m in anchor.enum_cls]
    assert actual == anchor.expected_values, (
        f"{anchor.enum_cls.__name__} drifted: got {actual}"
    )


@pytest.mark.parametrize("anchor", DNA_VIEW_ANCHORS)
def test_dna_enum_values_in_wiki(anchor):
    wiki_text = anchor.wiki_path.read_text(encoding="utf-8")
    for value in anchor.expected_values:
        assert value in wiki_text, (
            f"{value} ({anchor.enum_cls.__name__}) not found in {anchor.wiki_path.name}"
        )


# --- ObdLabDnaView field set ---

def test_obd_lab_dna_view_fields():
    expected = {
        "engine_displacement_liters", "rated_rpm",
        "stress_idle_rpm_target", "air_metering_strategy", "upstream_o2_type",
        "induction_type", "confidence",
    }
    actual = set(ObdLabDnaView.model_fields)
    assert actual == expected, f"ObdLabDnaView fields drifted: got {actual}"



# --- model_validate round-trip ---

def test_model_validate_round_trip_high_confidence():
    view = ObdLabDnaView.model_validate({
        "engine_displacement_liters": 2.0,
        "rated_rpm": 6500,
        "stress_idle_rpm_target": 4000,
        "air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK",
        "upstream_o2_type": "WIDEBAND_LINEAR",
        "induction_type": "NATURALLY_ASPIRATED",
        "confidence": "HIGH",
    })
    assert view.engine_displacement_liters == 2.0
    assert view.rated_rpm == 6500
    assert view.stress_idle_rpm_target == 4000
    assert view.air_metering_strategy == AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK
    assert view.upstream_o2_type == O2SensorType.WIDEBAND_LINEAR
    assert view.induction_type == InductionType.NATURALLY_ASPIRATED
    assert view.confidence == VinConfidence.HIGH


def test_model_validate_defaults_on_minimal():
    view = ObdLabDnaView.model_validate({
        "air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK",
        "upstream_o2_type": "NARROWBAND_0_TO_1V",
        "induction_type": "NATURALLY_ASPIRATED",
        "confidence": "HIGH",
    })
    assert view.engine_displacement_liters is None
    assert view.rated_rpm is None
    assert view.stress_idle_rpm_target is None



def test_model_validate_confidence_none():
    view = ObdLabDnaView.model_validate({
        "air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK",
        "upstream_o2_type": "WIDEBAND_LINEAR",
        "induction_type": "TURBOCHARGED",
        "confidence": "NONE",
    })
    assert view.confidence == VinConfidence.NONE


# --- No cross-lab imports in dna_view module ---

def test_no_cross_lab_imports():
    import re
    src = (OBDLAB_ROOT / "obdlab" / "schemas" / "dna_view.py").read_text(encoding="utf-8")  # v2: no code/ level
    for lab in ("comlab", "dnalab", "vinlab"):
        pattern = rf"^(from|import)\s+{lab}"
        assert not re.search(pattern, src, re.MULTILINE), (
            f"Forbidden import of '{lab}' in dna_view.py"
        )


# --- HIGH_IDLE_LOAD forbidden ---

def test_high_idle_load_forbidden():
    src = (OBDLAB_ROOT / "obdlab" / "schemas" / "dna_view.py").read_text(encoding="utf-8")  # v2: no code/ level
    assert "HIGH_IDLE_LOAD" not in src, "HIGH_IDLE_LOAD found in dna_view.py"
