"""Trim vector aggregator per OBDLab_KG_Wiki.md §12.

Computes total_trim_correction_delta = shrtft1 + longft1 (Bank 1 only).
Bank 2 is returned separately as total_trim_correction_delta_b2
when number_of_banks == 2. Bank-2 values must not be None when banks == 2.
Source: OBDLab_KG_Wiki.md §5 / §12.1.
"""

import logging
from typing import Any

from obdlab.core.exceptions import PIDValidationError

logger = logging.getLogger(__name__)


class TrimVectorAggregator:
    """Aggregate STFT + LTFT per bank into trim correction deltas.

    Source: OBDLab_KG_Wiki.md §5 / §12.1.
    """

    @staticmethod
    def aggregate(sanitized_pids: dict[str, Any]) -> tuple[float, float | None, float | None]:
        """Compute per-bank total_trim_correction_delta from sanitized PID dict.

        Args:
            sanitized_pids: PID dict with shrtft1, longft1, number_of_banks.
                May also contain shrtft2, longft2 for V-engines.

        Returns:
            (bank1_tft, bank2_tft_or_None, per_bank_trim_delta_or_None) — Bank 1 is always computed;
            Bank 2 and per_bank_trim_delta are None when number_of_banks != 2.

        Raises:
            PIDValidationError: number_of_banks == 2 but bank-2 fields are None.
        """
        # wiki: §12.1 — Bank 1 is always required
        shrtft1 = sanitized_pids.get("shrtft1")
        longft1 = sanitized_pids.get("longft1")

        # wiki: §12.1 — total_trim_correction_delta = shrtft1 + longft1
        bank1 = _safe_float(shrtft1, "shrtft1") + _safe_float(longft1, "longft1")

        banks = sanitized_pids.get("number_of_banks", 1)
        if banks != 2:
            return (bank1, None, None)

        shrtft2 = sanitized_pids.get("shrtft2")
        longft2 = sanitized_pids.get("longft2")

        # wiki: §3.1 — bank-2 null contract: must be present (not None) when banks==2
        if shrtft2 is None:
            raise PIDValidationError(
                "shrtft2 must not be null when number_of_banks == 2"
            )
        if longft2 is None:
            raise PIDValidationError(
                "longft2 must not be null when number_of_banks == 2"
            )

        # wiki: §12.1 — total_trim_correction_delta_b2 = shrtft2 + longft2
        bank2 = shrtft2 + longft2
        # wiki: §12.1 — per_bank_trim_delta = B1 - B2
        per_bank_trim_delta = bank1 - bank2
        return (bank1, bank2, per_bank_trim_delta)


def _safe_float(value: Any, field_name: str) -> float:
    """Coerce value to float, raising PIDValidationError on None."""
    if value is None:
        raise PIDValidationError(
            f"{field_name} is required for trim vector aggregation but was None"
        )
    return float(value)
