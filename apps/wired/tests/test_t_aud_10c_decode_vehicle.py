"""T-AUD-10c (F-C5-12): wired.composition.decode_vehicle is the decode diagnose runs.

Tags: NEW fails on the base fix/T-AUD-10e (no decode_vehicle).
"""

from __future__ import annotations

import pytest
import vinlab

import wired.composition as composition

DECODABLE_VIN = "WME01MC01XH072806"  # vinlab: PARTIAL, HORIZON_LEGACY


def test_decode_vehicle_returns_the_vinlab_decode() -> None:
    """NEW: the same VinDNA as vinlab.decode for a decodable VIN."""
    dna = composition.decode_vehicle(DECODABLE_VIN)
    assert isinstance(dna, vinlab.VinDNA)
    assert dna.to_json_payload() == vinlab.decode(DECODABLE_VIN).to_json_payload()


def test_decode_vehicle_delegates_to_the_composition_decode(monkeypatch: pytest.MonkeyPatch) -> None:
    """NEW: decode_vehicle calls the composition's own decode_vin, so the form and the labs share one decode."""
    seen: list[str] = []
    sentinel = object()

    def fake(vin: str) -> object:
        seen.append(vin)
        return sentinel

    monkeypatch.setattr(composition, "decode_vin", fake)
    assert composition.decode_vehicle(DECODABLE_VIN) is sentinel
    assert seen == [DECODABLE_VIN]


def test_undecodable_vin_raises_like_vinlab() -> None:
    """NEW: an undecodable VIN raises VINDecodeError, as vinlab.decode does."""
    with pytest.raises(vinlab.VINDecodeError):
        vinlab.decode("UNKNOWNVIN0000000")
    with pytest.raises(vinlab.VINDecodeError):
        composition.decode_vehicle("UNKNOWNVIN0000000")
