"""Tests for ``registry.shim.payload_mirrors``.

These cover the output-contract defaulting that keeps the shim's emitted dict
acceptable to COMLab's ``OrchestratorFinalUIOutput`` (UUID4 ``session_id`` and
a non-null ``user_input_echo_audit``) — the schema-drift fix locked as Option
(a) under REG-V2-INTEGRATE.

The mirror produces **plain dicts/strings**, never COMLab model instances —
the registry self-contained firewall forbids importing COMLab schemas. The
reconstruction into ``OrchestratorFinalUIOutput`` happens at the COMLab
boundary.
"""

from __future__ import annotations

from datetime import datetime

from registry.shim.payload_mirrors import (
    _SENTINEL_SESSION_ID,
    resolve_session_id,
    resolve_user_input_echo_audit,
)


# ---------------------------------------------------------------------------
# resolve_session_id
# ---------------------------------------------------------------------------


def test_session_id_passes_through_valid_uuid4() -> None:
    """A valid UUID4 in metadata.session_id is preserved verbatim — this is
    the traceability key across the v1/v2 side-by-side harness.
    """
    uid = "12345678-1234-4234-8234-123456789abc"
    payload = {"metadata": {"session_id": uid}}
    assert resolve_session_id(payload) == uid


def test_session_id_sentinel_when_absent() -> None:
    """Missing metadata → the fixed sentinel UUID, NOT a freshly-generated one
    (a fresh UUID per call would destroy cross-run traceability).
    """
    assert resolve_session_id({}) == _SENTINEL_SESSION_ID
    assert resolve_session_id({"metadata": {}}) == _SENTINEL_SESSION_ID


def test_session_id_sentinel_when_not_valid_uuid4() -> None:
    """A non-UUID string (or a non-v4 UUID) falls back to the sentinel."""
    payload = {"metadata": {"session_id": "not-a-uuid"}}
    assert resolve_session_id(payload) == _SENTINEL_SESSION_ID


def test_session_id_sentinel_is_stable_across_calls() -> None:
    """The sentinel must be identical across calls — deterministic traceability."""
    a = resolve_session_id({})
    b = resolve_session_id({"metadata": {"session_id": None}})
    assert a == b == _SENTINEL_SESSION_ID


def test_sentinel_is_valid_uuid4_shape() -> None:
    """The sentinel itself must satisfy the UUID4 contract COMLab enforces."""
    from uuid import UUID

    parsed = UUID(_SENTINEL_SESSION_ID)
    assert parsed.version == 4


# ---------------------------------------------------------------------------
# resolve_user_input_echo_audit
# ---------------------------------------------------------------------------


def test_echo_audit_passes_through_when_present() -> None:
    """A present echo-audit dict is carried through verbatim (COMLab does not
    generate the echo — it passes it through; the shim does the same).
    """
    echo = {
        "submitted_at": "2026-05-29T10:00:00",
        "groups": [{"screen_id": "gas", "label": "Gas", "fields": {}}],
    }
    payload = {"user_input_echo_audit": echo}
    assert resolve_user_input_echo_audit(payload) is echo


def test_echo_audit_sentinel_when_absent() -> None:
    """Missing echo-audit → sentinel with groups=[] and a parseable
    submitted_at timestamp (per UserInputEchoAudit docstring: "If omitted,
    Stage D emits a sentinel with submitted_at=<now> and groups=[]").
    """
    result = resolve_user_input_echo_audit({})
    assert result["groups"] == []
    # submitted_at must be an ISO-8601 string COMLab's datetime field accepts.
    parsed = datetime.fromisoformat(result["submitted_at"])
    assert isinstance(parsed, datetime)


def test_echo_audit_sentinel_when_none() -> None:
    """Explicit None for user_input_echo_audit also triggers the sentinel."""
    result = resolve_user_input_echo_audit({"user_input_echo_audit": None})
    assert result["groups"] == []
    assert "submitted_at" in result
