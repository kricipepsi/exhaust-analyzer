"""DataFusionSanitizer — public surface that wires the full DTCLab pipeline.

Ingests raw OBD-II Mode $03/$07/$0A (DTCs), Mode $02 (freeze frame), and
Mode $06 (on-board monitor results) and emits a single validated
``DTCLabPayload`` for COMLab consumption.

Source: DTC_VOCABULARY.md §11 (payload fields), §17 (COMLab integration contract);
        DTC_WIKI.md §0 (data-isolation invariant, three-mode coupling).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from dtclab.core.dtc_ingestion_gate import validate_dtc_list
from dtclab.core.freeze_frame_extractor import (
    evaluate_coolant_dtc_context,
    extract_freeze_frame,
)
from dtclab.core.historical_context_classifier import classify_historical_context
from dtclab.core.mode06_evaluator import evaluate_monitor
from dtclab.core.routing_tag_mapper import RoutingTagMapper
from dtclab.schemas.dna_view import DtcLabDnaView
from dtclab.schemas.payload import DTCLabPayload
from dtclab.schemas.vocabulary import DTCRoutingTag

__all__ = ["DataFusionSanitizer"]

logger = logging.getLogger(__name__)

_CONFIG_DIR = Path(__file__).parent.parent / "config"
_ROUTING_TAG_MAP_PATH = _CONFIG_DIR / "routing_tag_map.yaml"
_MODE06_DICTIONARY_PATH = _CONFIG_DIR / "mode_06_hex_dictionary.json"


class DataFusionSanitizer:
    """Wires the full DTCLab compilation pipeline into a single public surface.

    Constructor receives the typed DNA view (not a loose dict) per the
    DNA-first architecture (NewArchProposal_ImplementationPlan.md §4 Step 4).
    ``dna_view=None`` is permitted and treated as ``confidence == NONE``
    (pure DTC-pattern routing, no DNA gates).

    Source: DTC_VOCABULARY.md §11, §17.
    """

    def __init__(self, dna_view: DtcLabDnaView | None = None) -> None:
        self._dna_view = dna_view
        self._tag_mapper = RoutingTagMapper(_ROUTING_TAG_MAP_PATH, dna_view)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def sanitize(
        self,
        raw_dtcs: dict[str, list[str]],
        raw_freeze_frame: dict[str, Any],
        raw_mode06: dict[str, float],
        *,
        codes_cleared: bool = False,
        active_mil: bool = False,
        mil_flashing: bool = False,
    ) -> DTCLabPayload:
        """Compile raw OBD-II inputs into a validated ``DTCLabPayload``.

        Args:
            raw_dtcs: Dict keyed by OBD mode (``"$03"``, ``"$07"``, ``"$0A"``)
                      each mapping to a list of DTC code strings.
            raw_freeze_frame: Dict of bare PID name → value from Mode $02.
            raw_mode06: Dict of ``MID_<HEX>_TID_<HEX>`` → margin_pct.
            codes_cleared: ``True`` if DTCs were cleared this session.
            active_mil: ``True`` if the MIL is currently illuminated.
            mil_flashing: ``True`` if the MIL is flashing (Class A misfire).

        Returns:
            A fully validated ``DTCLabPayload`` ready for COMLab ingestion.

        Pipeline order (DTC_VOCABULARY.md §11):
        1. Validate DTC lists against the canonical regex.
        2. Extract and validate the freeze-frame record.
        3. Classify historical fault context from freeze-frame PIDs.
        4. Evaluate each Mode $06 monitor result.
        5. Map confirmed DTCs to routing tags (with DNA gates).
        6. Assemble and Pydantic-validate the payload.
        """
        # Step 1 — DTC ingestion gate (T-P0-3)
        confirmed_dtcs = validate_dtc_list(raw_dtcs.get("$03", []), "$03")
        pending_dtcs = validate_dtc_list(raw_dtcs.get("$07", []), "$07")
        permanent_dtcs = validate_dtc_list(raw_dtcs.get("$0A", []), "$0A")

        # Step 2 — Freeze frame extraction (T-P0-5)
        freeze_frame = extract_freeze_frame(raw_freeze_frame, codes_cleared)

        # Step 3 — Historical fault context (T-P0-7)
        historical_context = classify_historical_context(
            coolant_temp_c=freeze_frame.coolant_temp_c,
            engine_rpm=freeze_frame.engine_rpm,
            calculated_load_pct=freeze_frame.calculated_load_pct,
        )

        # Step 4 — Mode $06 evaluation (T-P0-6)
        monitors: dict[str, Any] = {}
        for mid_key, margin_pct in raw_mode06.items():
            monitors[mid_key] = evaluate_monitor(
                mid_key=mid_key,
                margin_pct=margin_pct,
                dictionary_path=_MODE06_DICTIONARY_PATH,
            )

        # Step 5 — Routing tag mapping (T-P0-4)
        routing_tags = self._tag_mapper.map(confirmed_dtcs)

        # Step 5b — Coolant/fluid cross-field context (CoolantLeakSig.md §4)
        for dtc in confirmed_dtcs:
            coolant_tag = evaluate_coolant_dtc_context(
                dtc, freeze_frame.fuel_system_status
            )
            if coolant_tag is not None:
                tag_enum = DTCRoutingTag(coolant_tag)
                if tag_enum not in routing_tags:
                    routing_tags.append(tag_enum)

        # Step 6 — Assemble and validate
        payload = DTCLabPayload.model_validate(
            {
                "active_mil": active_mil,
                "mil_flashing": mil_flashing,
                "confirmed_dtcs": confirmed_dtcs,
                "pending_dtcs": pending_dtcs,
                "permanent_dtcs": permanent_dtcs,
                "routing_tags": routing_tags,
                "mode_06_monitors": monitors,
                "historical_fault_context": historical_context,
                "freeze_frame": freeze_frame.model_dump(),
            }
        )

        logger.info(
            "dtclab_payload_emitted: confirmed=%d pending=%d permanent=%d "
            "tags=%d monitors=%d",
            len(confirmed_dtcs),
            len(pending_dtcs),
            len(permanent_dtcs),
            len(routing_tags),
            len(monitors),
        )

        return payload
