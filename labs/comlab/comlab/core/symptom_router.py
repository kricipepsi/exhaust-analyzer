"""SymptomDNA lab-suppression routing per data_flow_report.md §5.3.

Pure function: route_symptom(symptom_dna: Mapping[str, Any]) -> LabRoutingDirective

Reads:
  symptom_dna["environmental_conditions"]["engine_state"]  (str)
  symptom_dna["environmental_conditions"]["occurs_during"] (str)

All other SymptomDNA fields (tier_1, tier_2, free_text_notes) are
intentionally not read — no current consumer. See data_flow_report.md §5.3
for deferred routing candidates (promote_stress_idle, promote_evap_dtcs).

COMLab must never import from DNALab or SymptomLab.

Source: COMLab_LLD.md §6.2.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from comlab.schemas.vocabulary import LabRoutingDirective, LabRoutingDirectiveReason

__all__ = ["route_symptom"]

logger = logging.getLogger(__name__)

# WHY: mirror SymptomLab string values instead of importing across lab boundaries.
_ENGINE_STATE_NON_STARTER = "will_not_start"
_ENGINE_STATE_CRANKING = "cranking"

# Occurs-during string literal
_OCCURS_COLD_ONLY = "cold_only"


def route_symptom(symptom_dna: Mapping[str, Any]) -> LabRoutingDirective:
    """Derive lab routing flags from SymptomDNA environmental conditions.

    Routing rules per lld: §6.2:
      engine_state == will_not_start → suppress_gaslab, suppress_obd_live_pids,
                                       suppress_mode06_ui
                                       + reasons NON_STARTER_NO_EXHAUST,
                                         NON_RUNNING_NO_LIVE_PIDS,
                                         NON_RUNNING_MONITORS_NOT_READY
      engine_state == cranking      → suppress_obd_live_pids
                                       + reason NON_RUNNING_NO_LIVE_PIDS
      occurs_during == cold_only    → cold_start_mode
                                       + reason COLD_START_HYPOTHESIS

    Args:
        symptom_dna: read-only mapping from OrchestratorInboundRequest.symptom_dna.
            Missing keys default to neutral routing (all flags False).

    Returns:
        LabRoutingDirective with suppression flags and reasons tuple set.
    """
    env = symptom_dna.get("environmental_conditions", {})
    engine_state = env.get("engine_state", "")
    occurs_during = env.get("occurs_during", "")

    if not engine_state:
        logger.warning(
            "symptom_router: engine_state missing — defaulting to neutral routing"
        )

    suppress_gaslab = engine_state == _ENGINE_STATE_NON_STARTER
    suppress_obd_live_pids = engine_state in (
        _ENGINE_STATE_NON_STARTER,
        _ENGINE_STATE_CRANKING,
    )
    suppress_mode06_ui = engine_state == _ENGINE_STATE_NON_STARTER
    cold_start_mode = occurs_during == _OCCURS_COLD_ONLY

    reasons: list[LabRoutingDirectiveReason] = []

    # lld: §6.2 — routing rules with reasons
    if engine_state == _ENGINE_STATE_NON_STARTER:
        reasons.append(LabRoutingDirectiveReason.NON_STARTER_NO_EXHAUST)
        reasons.append(LabRoutingDirectiveReason.NON_RUNNING_NO_LIVE_PIDS)
        reasons.append(LabRoutingDirectiveReason.NON_RUNNING_MONITORS_NOT_READY)
    elif engine_state == _ENGINE_STATE_CRANKING:
        reasons.append(LabRoutingDirectiveReason.NON_RUNNING_NO_LIVE_PIDS)

    if cold_start_mode:
        reasons.append(LabRoutingDirectiveReason.COLD_START_HYPOTHESIS)

    return LabRoutingDirective(
        suppress_gaslab=suppress_gaslab,
        suppress_obd_live_pids=suppress_obd_live_pids,
        suppress_mode06_ui=suppress_mode06_ui,
        cold_start_mode=cold_start_mode,
        reasons=tuple(reasons),
    )
