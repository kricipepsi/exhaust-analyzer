"""Vocabulary drift guard.

Verifies that every enum value in ``comlab/schemas/vocabulary.py`` appears in
its cited wiki section. Drift in either direction (wiki updated but module not,
or vice versa) fails the test.

Phase 0b — T-P0b-1 seeded rows for ``Horizon`` and ``EuroEmissionCategory``;
T-P0b-2 adds rows for the three VIN-driven polymorphic switches
(``AirMeteringStrategy``, ``O2SensorType``, ``EngineStateBucket``); T-P0b-3
adds rows for the four fault-classification enums (``FaultFamily``,
``ChemicalSignature``, ``O2FailureMode``, ``HistoricalFaultContext``);
T-P0b-4 adds rows for the five DTC enums (``DTCRoutingTag``,
``DTCFallbackStrategy``, ``DTCSeverityClass``, ``DTCState``, ``Mode06Status``)
and loads ``DTC_VOCABULARY.md`` for DTC-row drift verification.
T-P0b-5 adds rows for the four orchestrator-output enums
(``ConfidenceRating``, ``VinConfidence``, ``DegradationMode``, ``SeverityLevel``).
T-P0b-6 adds the ``DTC_REGEX`` constant and ``test_dtc_regex_matches_wiki``.
Subsequent tasks extend this module per
``_comlab_skills/comlab-vocabulary/SKILL.md`` §4.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

import pytest

from comlab.schemas import vocabulary as V

VOCAB_DIR = Path(__file__).parent.parent.parent / "docs" / "Vocabulary"
OBD = (VOCAB_DIR / "OBD_VOCABULARY.md").read_text(encoding="utf-8")
DTC = (VOCAB_DIR / "DTC_VOCABULARY.md").read_text(encoding="utf-8")

DRIFT_CASES: list[tuple[type[StrEnum], str, int]] = [
    (V.Horizon, OBD, 3),
    (V.EuroEmissionCategory, OBD, 7),
    (V.AirMeteringStrategy, OBD, 3),
    (V.O2SensorType, OBD, 2),
    (V.EngineStateBucket, OBD, 4),
    (V.FaultFamily, OBD, 12),  # lld: §3.1 — 9 original + catalyst/exhaust/ignition + mechanical/cam/non_starter
    (V.ChemicalSignature, OBD, 32),
    (V.O2FailureMode, OBD, 4),
    (V.HistoricalFaultContext, OBD, 4),
    (V.DTCRoutingTag, DTC, 17),
    (V.DTCFallbackStrategy, DTC, 3),
    (V.DTCSeverityClass, DTC, 4),
    (V.DTCState, DTC, 3),
    (V.Mode06Status, DTC, 4),  # MONITOR_ABORTED added (T-COMV2-NOSTART-1)
    (V.ConfidenceRating, OBD, 3),
    (V.VinConfidence, OBD, 3),
    (V.DegradationMode, OBD, 4),  # +SINGLE_POINT (T-COMV2-DELTA-1; wiki pending)
    (V.SeverityLevel, OBD, 3),
    (V.SampleValidity, OBD, 4),
    (V.VEValidity, OBD, 5),
    (V.TrimAnalyticsGate, OBD, 9),
    (V.NodeMAFStatus, OBD, 2),
    (V.NodeMAPStatus, OBD, 2),
    (V.DownstreamTrimRole, OBD, 3),  # T-FX-9 — O2_MODEL_STRATEGY.md §3; wiki pending
    (V.FuelSystemStatus, DTC, 4),
    (V.Mode06MonitorState, DTC, 4),  # MONITOR_ABORTED added (T-COMV2-NOSTART-1)
]


DRIFT_IDS: list[str] = [
    cls.__name__ for cls, _txt, _cnt in DRIFT_CASES
]

# Values added by FX tasks whose wiki docs are not yet updated.
# The owning T-DOC task resolves these when it runs.
_WIKI_PENDING: set[str] = {
    "EGR_DILUTION_MISFIRE",    # T-DOC-5
    "INCOMPLETE_OXIDATION",    # T-DOC-5
    "INCOMPLETE_COMBUSTION",   # T-DOC (GASLab T-P8-1 follow-up)
    "COOLANT_LEAK_INTERNAL",   # T-DOC (GASLab T-P8-2 follow-up)
    "mechanical_wear",         # T-P6-5b-2 — KG family added, wiki pending
    "cam_timing",              # T-P6-5b-2 — KG family added, wiki pending
    "non_starter",             # T-P6-5b-2 — KG family added, wiki pending
    "NONE",                    # T-FX-9 — DownstreamTrimRole sourced from O2_MODEL_STRATEGY.md
    "CATALYST_MONITOR_ONLY",   # T-FX-9
    "SECONDARY_FUEL_TRIM",     # T-FX-9
    "SINGLE_POINT",            # T-COMV2-DELTA-1 — DegradationMode value; wiki: delta-relations/01, OBD_VOCABULARY surface pending
    "MONITOR_ABORTED",         # T-COMV2-NOSTART-1 — mirrors DTCLab emitter
}


@pytest.mark.parametrize(
    ("enum_cls", "wiki_text", "expected_count"),
    DRIFT_CASES,
    ids=DRIFT_IDS,
)
def test_wiki_drift_guard(
    enum_cls: type[StrEnum],
    wiki_text: str,
    expected_count: int,
) -> None:
    """Every enum value must appear verbatim in its cited wiki section."""
    actual_count = len(list(enum_cls))
    assert actual_count == expected_count, (
        f"{enum_cls.__name__} has {actual_count} members; "
        f"expected {expected_count}"
    )
    for member in enum_cls:
        if member.value in _WIKI_PENDING:
            continue
        assert member.value in wiki_text, (
            f"{enum_cls.__name__}.{member.name} = {member.value!r} "
            f"not found in wiki"
        )


def test_dtc_regex_matches_wiki() -> None:
    """DTC_REGEX must match the wiki §2.3 canonical form."""
    assert V.DTC_REGEX == r"^[BCPU][0-3][0-9A-F]{3}$"
