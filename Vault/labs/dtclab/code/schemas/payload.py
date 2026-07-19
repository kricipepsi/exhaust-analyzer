"""DTCLabPayload — top-level JSON contract emitted to COMLab.

Every field and constraint is sourced verbatim from DTC_VOCABULARY.md §11.
Re-exports FreezeFrameRecord (§12) and Mode06MonitorResult (§13) for
convenience so the sanitizer imports from a single schema module.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, field_validator

from dtclab.schemas.freeze_frame import FreezeFrameRecord
from dtclab.schemas.mode06_result import MID_KEY_PATTERN, Mode06MonitorResult
from dtclab.schemas.vocabulary import (
    DTC_REGEX,
    DTCRoutingTag,
    HistoricalFaultContext,
)

__all__ = [
    "DTCLabPayload",
    "FreezeFrameRecord",
    "Mode06MonitorResult",
]

_COMPILED_DTC_REGEX: re.Pattern[str] = re.compile(DTC_REGEX)
_COMPILED_MID_KEY_REGEX: re.Pattern[str] = re.compile(MID_KEY_PATTERN)


class DTCLabPayload(BaseModel):
    """Top-level DTCLab output — the single JSON payload at the COMLab boundary.

    Source: DTC_VOCABULARY.md §11.
    Consumed by COMLab ``lab_pipeline_aggregator`` at the ``dtc_lab_output``
    key of ``OrchestratorInboundRequest`` (per §17).
    """

    active_mil: bool
    # wiki: §11 — MIL illuminated (solid)

    mil_flashing: bool
    # wiki: §11 — MIL flashing (Class A misfire active)

    confirmed_dtcs: list[str]
    # wiki: §11 — each matches DTC_REGEX (ERR-CONTRACT-001 on violation)

    pending_dtcs: list[str]
    # wiki: §11 — each matches DTC_REGEX

    permanent_dtcs: list[str]
    # wiki: §11 — each matches DTC_REGEX

    routing_tags: list[DTCRoutingTag]
    # wiki: §11 — valid DTCRoutingTag enum values (ERR-CONTRACT-002 on violation)

    mode_06_monitors: dict[str, Mode06MonitorResult]
    # wiki: §11 — keys match MID_<HEX>_TID_<HEX>

    historical_fault_context: HistoricalFaultContext
    # wiki: §11 — load / thermal context at DTC storage moment

    freeze_frame: FreezeFrameRecord
    # wiki: §11 — Mode $02 snapshot at fault confirmation

    # ------------------------------------------------------------------
    # Field validators
    # ------------------------------------------------------------------

    @field_validator("confirmed_dtcs", "pending_dtcs", "permanent_dtcs")
    @classmethod
    def _validate_dtc_list(cls, v: list[str]) -> list[str]:
        """Validate DTC list."""
        for code in v:
            if not _COMPILED_DTC_REGEX.match(code):
                raise ValueError(
                    f"DTC {code!r} does not match {DTC_REGEX} "
                    f"(ERR-CONTRACT-001)"
                )
        return v

    @field_validator("routing_tags", mode="before")
    @classmethod
    def _validate_routing_tags(
        cls, v: list[str | DTCRoutingTag]
    ) -> list[str | DTCRoutingTag]:
        """Validate routing tags."""
        valid = frozenset(t.value for t in DTCRoutingTag)
        for item in v:
            if isinstance(item, DTCRoutingTag):
                continue
            if item not in valid:
                raise ValueError(
                    f"Routing tag {item!r} is not a valid DTCRoutingTag "
                    f"(ERR-CONTRACT-002)  # wiki: DTC_VOCABULARY.md §11"
                )
        return v

    @field_validator("mode_06_monitors")
    @classmethod
    def _validate_monitor_keys(cls, v: dict[str, Mode06MonitorResult]) -> dict[str, Mode06MonitorResult]:
        """Validate monitor keys."""
        for key in v:
            if not _COMPILED_MID_KEY_REGEX.match(key):
                raise ValueError(
                    f"Mode $06 monitor key {key!r} does not match "
                    f"MID_<HEX>_TID_<HEX> (wiki §13.1)"
                )
        return v
