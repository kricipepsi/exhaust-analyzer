"""Mode $06 on-board monitor evaluator — margin tri-state classifier.

Source: DTC_VOCABULARY.md §7 (margin tri-state), §13 (MID/TID key form, universal MID inventory).
"""

from __future__ import annotations

import functools
import json
import logging
import re
from pathlib import Path
from typing import Any, Final

from dtclab.schemas.dna_view import EuroEmissionCategory
from dtclab.schemas.mode06_result import MID_KEY_PATTERN, Mode06MonitorResult
from dtclab.schemas.vocabulary import Mode06MonitorState

logger = logging.getLogger(__name__)

_MID_KEY_REGEX: Final[re.Pattern[str]] = re.compile(MID_KEY_PATTERN)
_CAN_PORTABLE_EURO_CATEGORIES: Final[frozenset[EuroEmissionCategory]] = frozenset(
    {
        EuroEmissionCategory.EURO_4,
        EuroEmissionCategory.EURO_5,
        EuroEmissionCategory.EURO_6,
        EuroEmissionCategory.EURO_7,
    }
)
_NOSTART_ABORTED_MONITOR_KEY: Final[str] = "MID_A1_TID_53"


def classify_margin(margin_pct: float) -> Mode06MonitorState:
    """Classify a Mode $06 margin percentage into its tri-state.

    Source: DTC_VOCABULARY.md §7.

    Args:
        margin_pct: The margin-to-limit as a percentage.
                    0–100 for within-limit monitors; negative for past-limit.

    Returns:
        The appropriate ``Mode06MonitorState``.
    """
    # wiki: §7 — margin ≤ 0 → CRITICAL_FAIL (boundary inclusive on fail side)
    if margin_pct <= 0:
        return Mode06MonitorState.CRITICAL_FAIL
    # wiki: §7 — margin 1–15 → PENDING_FAIL_MARGINAL
    if margin_pct <= 15:
        return Mode06MonitorState.PENDING_FAIL_MARGINAL
    # wiki: §7 — margin ≥ 16 → PASSED
    return Mode06MonitorState.PASSED


def _lookup_component(mid_hex: str, dictionary: dict[str, Any]) -> str:
    """Return the target component name for *mid_hex* from the dictionary.

    Returns ``"UNKNOWN"`` when *mid_hex* is absent or not a valid entry.
    """
    entry = dictionary.get(mid_hex)
    if entry is None or not isinstance(entry, dict):
        return "UNKNOWN"
    return str(entry.get("name", "UNKNOWN"))


@functools.lru_cache(maxsize=4)
def _load_dictionary(path: Path) -> dict[str, Any]:
    """Return the parsed Mode $06 hex dictionary at *path*.

    Cached per distinct *path* for the process lifetime;
    the config is static at runtime so stale reads are not a concern.
    """
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def evaluate_monitor(
    mid_key: str,
    margin_pct: float,
    dictionary_path: Path,
    *,
    monitor_incomplete: bool = False,
    euro_emission_category: EuroEmissionCategory | None = None,
) -> Mode06MonitorResult:
    """Evaluate a single Mode $06 monitor result.

    Args:
        mid_key: The MID/TID key (e.g. ``"MID_A2_TID_0B"``).
        margin_pct: The margin-to-limit percentage.
        dictionary_path: Path to ``mode_06_hex_dictionary.json``.
        monitor_incomplete: ``True`` when the ECU reports an explicit
            Incomplete / all-zero monitor state.
        euro_emission_category: DNA-derived emissions era gate.  Only
            Euro 4+ asserts portable CAN-era Mode $06 monitor-aborted.

    Returns:
        A fully populated ``Mode06MonitorResult``.

    Raises:
        ValueError: If *mid_key* does not match the canonical
            ``MID_<HEX>_TID_<HEX>`` form (wiki §13.1).
    """
    if not _MID_KEY_REGEX.match(mid_key):
        raise ValueError(
            f"Invalid MID key {mid_key!r}; "
            f"expected form MID_<HEX>_TID_<HEX> (wiki §13.1)"
        )

    # wiki: §13.1 — extract the MID portion from the key
    # "MID_A2_TID_0B" → parts = ["MID", "A2", "TID", "0B"]
    parts = mid_key.split("_")
    mid_hex = parts[1]  # the MID hex component

    dictionary = _load_dictionary(dictionary_path)
    target_component = _lookup_component(mid_hex, dictionary)
    state = (
        Mode06MonitorState.MONITOR_ABORTED
        if _is_can_portable_monitor_aborted(
            mid_key=mid_key,
            monitor_incomplete=monitor_incomplete,
            euro_emission_category=euro_emission_category,
        )
        else classify_margin(margin_pct)
    )

    return Mode06MonitorResult(
        monitor_id=mid_key,
        state=state,
        margin_pct=margin_pct,
        target_component=target_component,
    )


def _is_can_portable_monitor_aborted(
    *,
    mid_key: str,
    monitor_incomplete: bool,
    euro_emission_category: EuroEmissionCategory | None,
) -> bool:
    """Return True for the CAN-era no-start aborted monitor assertion.

    wiki: 10_nonstart_diagnostics.md §10.1 and §10.3; OBDLab audit Q8.
    """
    return (
        monitor_incomplete
        and mid_key == _NOSTART_ABORTED_MONITOR_KEY
        and euro_emission_category in _CAN_PORTABLE_EURO_CATEGORIES
    )
