"""Tests for dtclab.family_map — routing-tag → canonical-family map.

Covers: every tag decided, POA_HISTORY never emitted, direct mappings match
DESIGN §2, every emitted family is canonical.
"""

from __future__ import annotations

import pytest

from dtclab.family_map import CANONICAL_FAMILIES, ROUTING_TAG_TO_FAMILY, families_for_tags
from dtclab.schemas.vocabulary import DTCRoutingTag


# ---------------------------------------------------------------------------
# test_every_tag_has_a_decision
# ---------------------------------------------------------------------------

def test_every_tag_has_a_decision() -> None:
    """Every one of the 17 DTCRoutingTag values is a key in the map."""
    all_tags = list(DTCRoutingTag)
    assert len(all_tags) == 17, f"expected 17 DTCRoutingTag values, got {len(all_tags)}"

    for tag in all_tags:
        assert tag in ROUTING_TAG_TO_FAMILY, (
            f"{tag.name} is missing from ROUTING_TAG_TO_FAMILY — "
            "every tag must have an explicit decision"
        )


# ---------------------------------------------------------------------------
# test_poa_history_never_maps
# ---------------------------------------------------------------------------

def test_poa_history_never_maps() -> None:
    """POA_HISTORY maps to None — COMLab injects it from GASLab."""
    assert ROUTING_TAG_TO_FAMILY[DTCRoutingTag.POA_HISTORY] is None


# ---------------------------------------------------------------------------
# test_direct_mappings
# ---------------------------------------------------------------------------

DIRECT_MAPPINGS: list[tuple[DTCRoutingTag, str]] = [
    (DTCRoutingTag.LEAN_HISTORY, "lean_condition"),
    (DTCRoutingTag.RICH_HISTORY, "rich_mixture"),
    (DTCRoutingTag.MISFIRE_HISTORY, "misfire"),
    (DTCRoutingTag.CATALYST_HISTORY, "catalyst_failure"),
    (DTCRoutingTag.O2_HISTORY, "sensor_fault"),
    (DTCRoutingTag.VVT_HISTORY, "cam_timing"),
]


@pytest.mark.parametrize(("tag", "expected_family"), DIRECT_MAPPINGS)
def test_direct_mappings(tag: DTCRoutingTag, expected_family: str) -> None:
    """DESIGN §2 direct mappings match."""
    assert ROUTING_TAG_TO_FAMILY[tag] == expected_family, (
        f"{tag.name} → {ROUTING_TAG_TO_FAMILY[tag]!r}; expected {expected_family!r}"
    )


# ---------------------------------------------------------------------------
# test_families_are_canonical
# ---------------------------------------------------------------------------

def test_families_are_canonical() -> None:
    """Every non-None value in ROUTING_TAG_TO_FAMILY is in CANONICAL_FAMILIES."""
    for tag, family in ROUTING_TAG_TO_FAMILY.items():
        if family is None:
            continue
        assert family in CANONICAL_FAMILIES, (
            f"{tag.name} → {family!r} is not in CANONICAL_FAMILIES"
        )


# ---------------------------------------------------------------------------
# test_canonical_families_size
# ---------------------------------------------------------------------------

def test_canonical_families_size() -> None:
    """CANONICAL_FAMILIES must have 16 entries (COMLab FaultFamilyLit)."""
    assert len(CANONICAL_FAMILIES) == 16, (
        f"expected 16 canonical families, got {len(CANONICAL_FAMILIES)}"
    )


# ---------------------------------------------------------------------------
# test_families_for_tags
# ---------------------------------------------------------------------------

def test_families_for_tags_empty() -> None:
    """Empty tag list returns empty family list."""
    assert families_for_tags([]) == []


def test_families_for_tags_deduplicates() -> None:
    """Duplicate families are collapsed to one."""
    tags = [DTCRoutingTag.LEAN_HISTORY, DTCRoutingTag.RICH_HISTORY, DTCRoutingTag.LEAN_HISTORY]
    result = families_for_tags(tags)
    assert result == ["lean_condition", "rich_mixture"]


def test_families_for_tags_strips_none() -> None:
    """Context-only tags (None) are excluded from output."""
    tags = [DTCRoutingTag.POA_HISTORY, DTCRoutingTag.LEAN_HISTORY, DTCRoutingTag.EGR_HISTORY]
    result = families_for_tags(tags)
    assert result == ["lean_condition"]


def test_families_for_tags_preserves_order() -> None:
    """First occurrence determines position in output."""
    tags = [
        DTCRoutingTag.MISFIRE_HISTORY,
        DTCRoutingTag.VVT_HISTORY,
        DTCRoutingTag.O2_HISTORY,
    ]
    result = families_for_tags(tags)
    assert result == ["misfire", "cam_timing", "sensor_fault"]
