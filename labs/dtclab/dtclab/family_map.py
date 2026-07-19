"""Canonical family mapping for DTCLab routing tags.

Maps each DTCRoutingTag (17-value surface, DTC_VOCABULARY.md §4) to a canonical
fault family from the COMLabSimple 16-family vocabulary.  Tags with no canonical-
family home are context-only (return None) — they inform COMLab's fault-atlas
router without voting on a family.  DESIGN_dtc_percent_sourcing.md §2 governs
the reach table; every mapping cites DTC_VOCABULARY.md §4.

No numbers, no scoring — this is the routing-tag→family *relation* only.
The scorer (T-DT2-2) and emitter (T-DT2-3) consume this map.
"""

from __future__ import annotations

from typing import Final

from dtclab.schemas.vocabulary import DTCRoutingTag

__all__ = [
    "CANONICAL_FAMILIES",
    "ROUTING_TAG_TO_FAMILY",
    "families_for_tags",
]

# ---------------------------------------------------------------------------
# Canonical family vocabulary — mirrored from COMLabSimple FaultFamilyLit
# (COMLab comlab/schemas/response.py, kg.py).  No cross-lab import.
# ---------------------------------------------------------------------------

CANONICAL_FAMILIES: Final[frozenset[str]] = frozenset(
    {
        "lean_condition",
        "rich_mixture",
        "misfire",
        "sensor_fault",
        "ecu_fault",
        "catalyst_failure",
        "exhaust_leak",
        "ignition_fault",
        "mechanical_wear",
        "cam_timing",
        "non_starter",
        "no_fault",
        "invalid_input",
        "vacuum_leak",
        "overheating",
        "charging_system",
    }
)
"""The 16-family canonical set used by COMLabSimple combine() (FU-1)."""

# ---------------------------------------------------------------------------
# Routing-tag → canonical family map
# ---------------------------------------------------------------------------

ROUTING_TAG_TO_FAMILY: Final[dict[DTCRoutingTag, str | None]] = {
    # -- Direct mappings (DESIGN_dtc_percent_sourcing.md §2) ---------------
    DTCRoutingTag.LEAN_HISTORY: "lean_condition",  # wiki: §4 — P0171, P0174
    DTCRoutingTag.RICH_HISTORY: "rich_mixture",  # wiki: §4 — P0172, P0175
    DTCRoutingTag.MISFIRE_HISTORY: "misfire",  # wiki: §4 — P0300–P0312
    DTCRoutingTag.CATALYST_HISTORY: "catalyst_failure",  # wiki: §4 — P0420, P0430 (DNA-gated)
    DTCRoutingTag.O2_HISTORY: "sensor_fault",  # wiki: §4 — P0130–P0161
    DTCRoutingTag.VVT_HISTORY: "cam_timing",  # wiki: §4 — P0010–P0023
    # -- Name-match mappings (family exists in canonical 16) ----------------
    DTCRoutingTag.ECU_INTERNAL_HISTORY: "ecu_fault",  # wiki: §4 — P0600–P0699
    DTCRoutingTag.KNOCK_HISTORY: "ignition_fault",  # wiki: §4 — P0325–P0334; DESIGN §2
    DTCRoutingTag.INJECTOR_HISTORY: "mechanical_wear",  # wiki: §4 — P0200–P0212; GASLab §7.18/7.21/7.22
    # -- Never emitted (COMLab injects from GASLab) ------------------------
    DTCRoutingTag.POA_HISTORY: None,  # wiki: §4 — gas-chem signature; DESIGN §2
    # -- Context-only (no single canonical family) --------------------------
    DTCRoutingTag.EGR_HISTORY: None,  # wiki: §4, §4.1 — P0400–P0409; system, not family
    DTCRoutingTag.EVAP_HISTORY: None,  # wiki: §4 — P0440–P0459; system, not family
    DTCRoutingTag.THERMAL_HISTORY: None,  # wiki: §4 — P0116–P0128; sensor vs thermal ambiguous
    DTCRoutingTag.IDLE_CONTROL_HISTORY: None,  # wiki: §4 — P0505–P0511; system, not family
    DTCRoutingTag.BOOST_HISTORY: None,  # wiki: §4 — P0234/P0299/P0235–P0245; system, not family

    DTCRoutingTag.COOLANT_SYSTEM_MALFUNCTION: None,  # wiki: §4 — cross-field (P0128/P0117 + OL_FAULT)
    DTCRoutingTag.CYLINDER_FLUID_MISFIRE: None,  # wiki: §4 — cross-field (P030x + CL)
}
"""Every DTCRoutingTag → canonical family | None.  None = context-only / not voted on."""


def families_for_tags(tags: list[DTCRoutingTag]) -> list[str]:
    """Return deduplicated, ordered canonical families for active routing tags.

    Strips None entries (context-only / POA_HISTORY) and preserves insertion
    order without duplicates.

    Args:
        tags: Active DTCRoutingTag values from the routing-tag mapper.

    Returns:
        Ordered, deduplicated list of canonical family strings.
    """
    seen: set[str] = set()
    result: list[str] = []
    for tag in tags:
        family = ROUTING_TAG_TO_FAMILY.get(tag)
        if family is not None and family not in seen:
            seen.add(family)
            result.append(family)
    return result
