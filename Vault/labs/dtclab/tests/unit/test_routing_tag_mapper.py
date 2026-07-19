"""Unit tests for RoutingTagMapper — DNA-gated DTC→tag fan-out.

Covers: basic fan-out, all four DNA gates (HIGH suppress / PARTIAL emit /
NONE emit), empty DTC list, unmapped DTCs, dna_view=None fallback,
unknown-gate fail-open branch, POA_HISTORY never emitted by mapper.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from dtclab.core.routing_tag_mapper import RoutingTagMapper
from dtclab.schemas.dna_view import (
    AirMeteringStrategy,
    DtcEmissionsView,
    DtcLabDnaView,
    EuroEmissionCategory,
    ResolvedHorizon,
    VinConfidence,
)
from dtclab.schemas.vocabulary import DTCRoutingTag

MAP_PATH = Path(__file__).parent.parent.parent / "dtclab" / "config" / "routing_tag_map.yaml"


# ------------------------------------------------------------------
# DNA view factories
# ------------------------------------------------------------------


def _dna_view(
    *,
    has_catalyst: bool = True,
    egr_equipped: bool = False,
    resolved_horizon: ResolvedHorizon = ResolvedHorizon.HORIZON_CLASSIC,
    confidence: VinConfidence = VinConfidence.HIGH,
) -> DtcLabDnaView:
    return DtcLabDnaView.model_validate(
        {
            "make": "Toyota",
            "model": "Corolla",
            "model_year": 2010,
            "euro_emission_category": EuroEmissionCategory.EURO_4,
            "air_metering_strategy": AirMeteringStrategy.MAF,
            "resolved_horizon": resolved_horizon,
            "emissions": DtcEmissionsView(
                has_catalyst=has_catalyst,
                egr_equipped=egr_equipped,
            ),
            "confidence": confidence,
        }
    )


# ------------------------------------------------------------------
# Basic DTC → tag fan-out
# ------------------------------------------------------------------


def test_p0171_maps_to_lean_history():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    assert mapper.map(["P0171"]) == [DTCRoutingTag.LEAN_HISTORY]


def test_p0300_maps_to_misfire_history():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    assert mapper.map(["P0300"]) == [DTCRoutingTag.MISFIRE_HISTORY]


def test_p0172_maps_to_rich_history():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    assert mapper.map(["P0172"]) == [DTCRoutingTag.RICH_HISTORY]


def test_p0420_maps_to_catalyst_history():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view(has_catalyst=True))
    assert DTCRoutingTag.CATALYST_HISTORY in mapper.map(["P0420"])


def test_multiple_tags_from_multiple_dtcs():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    tags = mapper.map(["P0171", "P0172", "P0300"])
    assert DTCRoutingTag.LEAN_HISTORY in tags
    assert DTCRoutingTag.RICH_HISTORY in tags
    assert DTCRoutingTag.MISFIRE_HISTORY in tags


def test_returns_enum_definition_order():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    tags = mapper.map(["P0300", "P0171", "P0420"])
    # LEAN_HISTORY (index 0) before MISFIRE_HISTORY (index 2)
    # before CATALYST_HISTORY (index 3)
    assert tags == sorted(tags, key=lambda t: list(DTCRoutingTag).index(t))


# ------------------------------------------------------------------
# CATALYST gate
# ------------------------------------------------------------------


def test_catalyst_suppressed_on_no_catalyst_high_confidence():
    dna = _dna_view(has_catalyst=False, confidence=VinConfidence.HIGH)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0420"])
    assert DTCRoutingTag.CATALYST_HISTORY not in tags


def test_catalyst_emitted_with_catalyst_high_confidence():
    dna = _dna_view(has_catalyst=True, confidence=VinConfidence.HIGH)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0420"])
    assert DTCRoutingTag.CATALYST_HISTORY in tags


def test_catalyst_emitted_on_partial_confidence_without_catalyst():
    dna = _dna_view(has_catalyst=False, confidence=VinConfidence.PARTIAL)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0420"])
    assert DTCRoutingTag.CATALYST_HISTORY in tags


def test_catalyst_emitted_on_none_confidence_without_catalyst():
    dna = _dna_view(has_catalyst=False, confidence=VinConfidence.NONE)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0420"])
    assert DTCRoutingTag.CATALYST_HISTORY in tags


def test_p0430_catalyst_gate():
    """P0430 also routes to CATALYST_HISTORY with same gate logic."""
    dna = _dna_view(has_catalyst=True, confidence=VinConfidence.HIGH)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0430"])
    assert DTCRoutingTag.CATALYST_HISTORY in tags


# ------------------------------------------------------------------
# EGR gate
# ------------------------------------------------------------------


def test_egr_suppressed_on_no_egr_high_confidence():
    dna = _dna_view(egr_equipped=False, confidence=VinConfidence.HIGH)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0400"])
    assert DTCRoutingTag.EGR_HISTORY not in tags


def test_egr_emitted_with_egr_high_confidence():
    dna = _dna_view(egr_equipped=True, confidence=VinConfidence.HIGH)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0400"])
    assert DTCRoutingTag.EGR_HISTORY in tags


def test_egr_emitted_on_partial_confidence_without_egr():
    dna = _dna_view(egr_equipped=False, confidence=VinConfidence.PARTIAL)
    mapper = RoutingTagMapper(MAP_PATH, dna_view=dna)
    tags = mapper.map(["P0400"])
    assert DTCRoutingTag.EGR_HISTORY in tags


# ------------------------------------------------------------------
# POA_HISTORY never emitted by mapper (T-FX-3 — moved to COMLab)
# ------------------------------------------------------------------


def test_poa_history_never_emitted_by_mapper():
    """POA_HISTORY has no DTC-pattern mapping — it is injected by COMLab."""
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    tags = mapper.map(["P0171", "P0172", "P0300", "P0420"])
    assert DTCRoutingTag.POA_HISTORY not in tags


def test_poa_history_never_emitted_for_empty_dtc_list():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    assert DTCRoutingTag.POA_HISTORY not in mapper.map([])


# ------------------------------------------------------------------
# dna_view=None (treat as confidence=NONE)
# ------------------------------------------------------------------


def test_dna_view_none_emits_all_matched_tags():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=None)
    tags = mapper.map(["P0420", "P0400", "P0300"])
    assert DTCRoutingTag.CATALYST_HISTORY in tags
    assert DTCRoutingTag.EGR_HISTORY in tags
    assert DTCRoutingTag.MISFIRE_HISTORY in tags


# ------------------------------------------------------------------
# Edge cases
# ------------------------------------------------------------------


def test_empty_dtc_list_returns_empty():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    assert mapper.map([]) == []


def test_unmapped_dtc_produces_no_tag():
    """Transmission DTCs (P0700) are recognised by regex but not mapped."""
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    assert mapper.map(["P0700"]) == []


def test_unmapped_dtc_with_valid_dtc():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    tags = mapper.map(["P0700", "P0171"])
    assert tags == [DTCRoutingTag.LEAN_HISTORY]


def test_duplicate_tags_deduplicated():
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    tags = mapper.map(["P0171", "P0174"])  # both LEAN_HISTORY
    assert tags == [DTCRoutingTag.LEAN_HISTORY]


# ------------------------------------------------------------------
# Unknown-gate fail-open (L4 audit — coverage gap)
# ------------------------------------------------------------------


def _bogus_gate_yaml() -> str:
    """Return a routing YAML string with an unrecognised dna_gate name."""
    return """\
entries:
  - patterns:
      - "^P0100$"
    tag: LEAN_HISTORY
    dna_gate: nonexistent_gate_xyz
"""


def test_unknown_gate_fail_open(tmp_path, caplog):
    """An unknown dna_gate name triggers the fail-open branch.

    Under HIGH-confidence DNA, an unrecognised gate should emit the tag
    (fail open) and log a warning with the gate name.
    """
    yaml_path = tmp_path / "bogus_gate_map.yaml"
    yaml_path.write_text(_bogus_gate_yaml(), encoding="utf-8")

    mapper = RoutingTagMapper(
        yaml_path,
        dna_view=_dna_view(confidence=VinConfidence.HIGH),
    )
    with caplog.at_level(logging.WARNING, logger="dtclab.core.routing_tag_mapper"):
        tags = mapper.map(["P0100"])

    assert tags == [DTCRoutingTag.LEAN_HISTORY]
    assert len(caplog.records) == 1
    assert "nonexistent_gate_xyz" in caplog.records[0].message
    assert caplog.records[0].levelname == "WARNING"


# ------------------------------------------------------------------
# Comprehensive fan-out spot-checks (DTC_VOCABULARY.md §4.2 prose anchors)
# ------------------------------------------------------------------

FAN_OUT_CASES = [
    ("P0010", DTCRoutingTag.VVT_HISTORY),
    ("P0100", DTCRoutingTag.LEAN_HISTORY),
    ("P0116", DTCRoutingTag.THERMAL_HISTORY),
    ("P0130", DTCRoutingTag.O2_HISTORY),
    ("P0200", DTCRoutingTag.INJECTOR_HISTORY),
    ("P0234", DTCRoutingTag.BOOST_HISTORY),
    ("P0299", DTCRoutingTag.BOOST_HISTORY),
    ("P0301", DTCRoutingTag.MISFIRE_HISTORY),
    ("P0325", DTCRoutingTag.KNOCK_HISTORY),
    ("P0335", DTCRoutingTag.MISFIRE_HISTORY),
    ("P0351", DTCRoutingTag.MISFIRE_HISTORY),
    ("P0440", DTCRoutingTag.EVAP_HISTORY),
    ("P0505", DTCRoutingTag.IDLE_CONTROL_HISTORY),
    ("P0562", DTCRoutingTag.ECU_INTERNAL_HISTORY),
    ("P0600", DTCRoutingTag.ECU_INTERNAL_HISTORY),
    ("P0606", DTCRoutingTag.ECU_INTERNAL_HISTORY),
    ("P0641", DTCRoutingTag.ECU_INTERNAL_HISTORY),
]


@pytest.mark.parametrize(("dtc", "expected_tag"), FAN_OUT_CASES)
def test_fan_out(dtc, expected_tag):
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())
    tags = mapper.map([dtc])
    assert expected_tag in tags, f"{dtc} should route to {expected_tag.value}"
