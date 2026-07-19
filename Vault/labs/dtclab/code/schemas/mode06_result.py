"""Mode06MonitorResult — Mode $06 on-board monitor test result.

Every field sourced from DTC_VOCABULARY.md §13.
"""

from pydantic import BaseModel, Field

from dtclab.schemas.vocabulary import Mode06MonitorState

# wiki: §13.1 — MID/TID key form: MID_<HEX>_TID_<HEX>
MID_KEY_PATTERN: str = r"^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$"


class Mode06MonitorResult(BaseModel):
    """Single Mode $06 monitor test result.

    Source: DTC_VOCABULARY.md §13.
    """

    monitor_id: str = Field(pattern=MID_KEY_PATTERN)
    # wiki: §13.1 — e.g. "MID_A2_TID_0B"

    state: Mode06MonitorState
    # wiki: §7 — tri-state classification

    margin_pct: float
    # wiki: §7 — 0–100; negative = past limit

    target_component: str
    # wiki: §13.2 — looked up from mode_06_hex_dictionary.json
