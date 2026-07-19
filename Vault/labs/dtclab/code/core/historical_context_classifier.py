"""Historical fault context classifier.

Derives a HistoricalFaultContext enum value from freeze-frame PID values
per DTC_VOCABULARY.md §9 trigger conditions and priority order.
"""

from __future__ import annotations

from dtclab.schemas.vocabulary import HistoricalFaultContext


def classify_historical_context(
    coolant_temp_c: float,
    engine_rpm: int,
    calculated_load_pct: float,
) -> HistoricalFaultContext:
    """Classify the historical context at the moment a DTC was stored.

    Priority order (DTC_VOCABULARY.md §9):
    1. Cold-start transit (ECT < 60°C) — evaluated first; dominates all others.
    2. Historical idle fault (RPM < 1000 AND load < 25%).
    3. Historical load fault (RPM > 2000 AND load > 45%).
    4. Unknown — none of the above.

    All comparisons are strict (per the wiki trigger table).
    """
    if coolant_temp_c < 60:  # wiki: DTC_VOCABULARY.md §9
        return HistoricalFaultContext.COLD_START_TRANSIT_FAULT

    if engine_rpm < 1000 and calculated_load_pct < 25:  # wiki: DTC_VOCABULARY.md §9
        return HistoricalFaultContext.HISTORICAL_IDLE_FAULT

    if engine_rpm > 2000 and calculated_load_pct > 45:  # wiki: DTC_VOCABULARY.md §9
        return HistoricalFaultContext.HISTORICAL_LOAD_FAULT

    return HistoricalFaultContext.UNKNOWN
