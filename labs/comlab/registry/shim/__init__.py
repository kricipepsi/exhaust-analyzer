"""Registry shim helpers — payload-contract mirrors for the v2 integration.

Self-contained: stdlib + Pydantic only. No imports from any lab, COMLab, or
4DLabWired (the registry firewall). These helpers produce **plain dicts and
strings**; reconstruction into COMLab models happens at the COMLab boundary.
"""

from registry.shim.payload_mirrors import (
    resolve_session_id,
    resolve_user_input_echo_audit,
)

__all__ = [
    "resolve_session_id",
    "resolve_user_input_echo_audit",
]

