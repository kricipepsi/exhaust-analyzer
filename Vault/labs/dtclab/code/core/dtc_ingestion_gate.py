"""DTC ingestion gate — validates raw DTC strings against the canonical regex.

Source: DTC_VOCABULARY.md §2 (code structure), §10 (DTC_REGEX constant), §3 (modes).
"""

from __future__ import annotations

import re
from typing import Final

from dtclab.schemas.vocabulary import DTC_REGEX

_VALID_MODES: Final[tuple[str, ...]] = ("$03", "$07", "$0A")  # wiki: §3
_COMPILED_REGEX: Final[re.Pattern[str]] = re.compile(DTC_REGEX)


class DTCFormatError(ValueError):
    """Raised when a DTC string does not match the canonical regex.

    Source: DTC_VOCABULARY.md §2.3 — canonical form ^[BCPU][0-3][0-9A-F]{3}$.
    Ingestion errors go straight to the UI per NewArchProposal §3.2.
    """

    def __init__(self, code: str, mode: str) -> None:
        self.code = code
        self.mode = mode
        super().__init__(
            f"DTC {code!r} does not match {DTC_REGEX} (mode {mode})"
        )


def validate_dtc_list(codes: list[str], mode: str) -> list[str]:
    """Validate every code in *codes* against the canonical DTC regex.

    Args:
        codes: Raw DTC strings from Mode $03, $07, or $0A.
        mode: The OBD mode identifier (``"$03"``, ``"$07"``, ``"$0A"``).

    Returns:
        The input list unchanged (pass-through on full validation).

    Raises:
        DTCFormatError: On the **first** code that fails validation.
        ValueError: If *mode* is not one of the three recognised OBD modes.
    """
    if mode not in _VALID_MODES:
        raise ValueError(
            f"Unknown OBD mode {mode!r}; expected one of {_VALID_MODES}"
        )
    for code in codes:
        if not _COMPILED_REGEX.match(code):
            raise DTCFormatError(code, mode)
    return codes
