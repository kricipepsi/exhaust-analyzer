"""T-COMA-19 (F-C1-15): resolved_horizon is upper-cased and must be one of the three eras; never defaulted to MODERN."""
from __future__ import annotations

import pytest
from comlab.schemas.ingestion import SessionMetadata
from comlab.schemas.vocabulary import Horizon
from pydantic import ValidationError

SID = "6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60"


def _meta(horizon: object) -> SessionMetadata:
    return SessionMetadata(session_id=SID, vin_dna_string="WVWZZZ1JZ3W000001", resolved_horizon=horizon,
                           cylinder_count=4)


@pytest.mark.parametrize("bad", ["", "HORIZON_FOO", "MODERN", None])
def test_unknown_horizon_is_rejected(bad: object) -> None:
    with pytest.raises(ValidationError):
        _meta(bad)


@pytest.mark.parametrize("given, stored", [
    ("horizon_legacy", "HORIZON_LEGACY"),
    (" HORIZON_ADAPTIVE ", "HORIZON_ADAPTIVE"),
    (Horizon.MODERN, "HORIZON_MODERN"),
])
def test_known_horizon_is_normalised(given: object, stored: str) -> None:
    assert _meta(given).resolved_horizon == stored
