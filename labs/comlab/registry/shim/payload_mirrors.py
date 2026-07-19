"""Output-contract mirrors for the v2 integration shim.

Why this module exists (REG-V2-INTEGRATE-SCHEMA-DRIFT)
======================================================
The shim was originally built against the *input* payload shape
(``OrchestratorInboundRequest``) but emits an *output* dict that COMLab
reconstructs into ``OrchestratorFinalUIOutput``. Two output fields are
**stricter** than the shim's passthrough produced:

  * ``session_id`` — COMLab requires a ``UUID4``. The shim previously copied
    ``metadata.session_id`` verbatim, which fails reconstruction when the
    field is absent (empty payload) or not a v4 UUID.
  * ``user_input_echo_audit`` — COMLab requires a non-null
    ``UserInputEchoAudit``. The shim previously emitted ``None``.

This module centralises the defaulting so the contract is verified at both
ends. It deliberately returns **plain dicts/strings** — never COMLab model
instances — to keep the registry self-contained firewall intact. The
reconstruction into ``OrchestratorFinalUIOutput`` happens at the COMLab
boundary in ``fault_atlas_router.route()``.

Signal/noise: only fields with a **named v2 consumer** are mirrored.
``UserInputEchoAudit`` carries exactly ``submitted_at`` and ``groups``
(consumer: PRD §5.5 — Screen 6 echo audit); both are defaulted per the
schema's own sentinel contract. No other COMLab output field is stricter
than the shim already satisfies, so nothing else is mirrored here.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

logger = logging.getLogger(__name__)

# Fixed sentinel UUID4 used when the inbound payload carries no usable
# session_id. MUST be stable across calls — a fresh UUID per call would
# destroy traceability across the v1/v2 side-by-side harness. The nil-like
# all-zero-with-v4-nibbles value is unmistakably synthetic in logs.
# convention: REG-V2-INTEGRATE — deterministic no-session sentinel.
_SENTINEL_SESSION_ID: str = "00000000-0000-4000-8000-000000000000"


def _is_valid_uuid4(value: object) -> bool:
    """True iff ``value`` is a string parseable as a version-4 UUID."""
    if not isinstance(value, str):
        return False
    try:
        return UUID(value).version == 4
    except (ValueError, AttributeError, TypeError):
        return False


def resolve_session_id(payload: dict[str, Any]) -> str:
    """Return a UUID4 string for the output ``session_id``.

    Reads ``payload["metadata"]["session_id"]``. If absent or not a valid
    UUID4, returns the fixed ``_SENTINEL_SESSION_ID`` and logs a warning at the
    shim boundary. Never generates a fresh UUID — see module note on
    traceability.
    """
    metadata = payload.get("metadata") or {}
    candidate = metadata.get("session_id")
    if _is_valid_uuid4(candidate):
        return candidate  # type: ignore[return-value]  # narrowed by _is_valid_uuid4
    logger.warning(
        "v2 shim: inbound payload has no valid UUID4 session_id (got %r); "
        "emitting sentinel %s. Cross-run traceability for this case is degraded.",
        candidate,
        _SENTINEL_SESSION_ID,
    )
    return _SENTINEL_SESSION_ID


def resolve_user_input_echo_audit(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a ``UserInputEchoAudit``-shaped dict for the output.

    Passes through ``payload["user_input_echo_audit"]`` verbatim when present
    (COMLab carries the echo through; the shim does the same). When absent or
    ``None``, returns the schema-defined sentinel:
    ``{submitted_at: <now, ISO-8601>, groups: []}`` — per the
    ``UserInputEchoAudit`` docstring ("If omitted, Stage D emits a sentinel
    with submitted_at=<now> and groups=[]").

    Fields defaulted (each has a named consumer — PRD §5.5, Screen 6 echo):
      * ``submitted_at`` — ISO-8601 timestamp; consumer renders it on Screen 6.
      * ``groups``       — empty list; consumer renders zero wizard groups.
    """
    echo = payload.get("user_input_echo_audit")
    if echo is not None:
        return echo
    return {
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "groups": [],
    }


__all__ = [
    "resolve_session_id",
    "resolve_user_input_echo_audit",
    "_SENTINEL_SESSION_ID",
]
