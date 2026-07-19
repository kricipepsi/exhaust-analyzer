"""Drift-guard tests for obdlab.schemas.vocabulary against OBDLab_KG_Wiki.md."""

from pathlib import Path

import pytest

from obdlab.schemas.vocabulary import (
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    O2NormalizationMode,
    RpmStateBucket,
    TrimAnalyticsGate,
    VEValidity,
)

WIKI = Path(__file__).resolve().parents[2] / "wiki" / "OBDLab_KG_Wiki.md"  # v2: wiki/ co-located in lab

# wiki: code-only sentinels added by audit fixes — exempt from wiki-text presence check
_WIKI_EXEMPT = {"O2_CHANNEL_FAULT", "NO_FAULT", "WIDEBAND_OFFSET_CANDIDATE"}

DRIFT_CASES = [
    (RpmStateBucket,        ["STABILIZED_IDLE", "REGULATORY_HIGH_IDLE", "STRESS_IDLE", "COLD_OPEN_LOOP_INVALID"]),
    (O2NormalizationMode,   ["NARROWBAND_VOLTAGE_TO_LAMBDA", "WIDEBAND_PASSTHROUGH", "WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA", "O2_CHANNEL_FAULT"]),
    (VEValidity,            ["VALID", "FAULT_VE_IDLE_COLLAPSE", "FAULT_MAF_CONTAMINATION", "FAULT_VE_SENSOR_SKEW", "UNKNOWN"]),
    (TrimAnalyticsGate,     ["VALID", "ENGINE_COLD", "OPEN_LOOP", "O2_FAULT_ACTIVE", "CKP_CMP_FAULT_ACTIVE", "CODES_RECENTLY_CLEARED", "WOT_ACTIVE", "DFCO_ACTIVE", "SEMANTIC_ERROR"]),
    (NodeMAFStatus,         ["REAL_SENSOR_FEED", "VIRTUAL_EMULATION"]),
    (NodeMAPStatus,         ["REAL_SENSOR_FEED", "BACK_CALCULATED"]),
    (O2FailureMode,         ["NO_FAULT", "STUCK_LEAN", "STUCK_RICH", "WIDEBAND_OFFSET_CANDIDATE"]),
]



@pytest.mark.parametrize("enum_cls, expected", DRIFT_CASES)
def test_wiki_drift_guard(enum_cls, expected):
    """Every enum value must appear verbatim in OBDLab_KG_Wiki.md §6."""
    actual = [m.value for m in enum_cls]
    assert actual == expected, f"{enum_cls.__name__} drifted: got {actual}"
    wiki_text = WIKI.read_text(encoding="utf-8")
    for value in expected:
        if value in _WIKI_EXEMPT:
            continue
        assert value in wiki_text, f"{value} not found in OBDLab_KG_Wiki.md"


def test_rpm_bucket_names_canonical():
    """REGULATORY_HIGH_IDLE is canonical (§6.1)."""
    assert "REGULATORY_HIGH_IDLE" in [m.value for m in RpmStateBucket]


def test_high_idle_load_is_forbidden():
    """HIGH_IDLE_LOAD is BP-era and forbidden anywhere in obdlab/."""
    assert "HIGH_IDLE_LOAD" not in [m.value for m in RpmStateBucket]
    obdlab_root = Path(__file__).resolve().parents[2] / "obdlab"
    for py_file in obdlab_root.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        assert "HIGH_IDLE_LOAD" not in content, f"HIGH_IDLE_LOAD found in {py_file}"
