"""T-AUD-24a (R5): COMLab ingestion fuel-trim bounds follow SAE J1979 [-100.0, 99.22] %."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from comlab.schemas.ingestion import (
    EngineStateBucket,
    OBDLiveDataPayload,
    O2FailureMode,
    SecondOperatingPointFrame,
    TrimAnalyticsGate,
    VEValidity,
)


def _obd_kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "engine_warmed": True,
        "total_trim_correction_delta": 0.0,
        "ve_pct": 75.0,
        "ve_validity": VEValidity.VALID,
        "rpm_state_bucket": EngineStateBucket.STABILIZED_IDLE,
        "trim_analytics_gate": TrimAnalyticsGate.VALID,
        "o2_failure_mode": O2FailureMode.NO_FAULT,
    }
    base.update(overrides)
    return base


def test_ingestion_rejects_old_127_stft_idle_pct() -> None:
    """stft_idle_pct=127.0 (old T-W-6 rail) is rejected under SAE J1979 [-100.0, 99.22]."""
    with pytest.raises(ValidationError):
        OBDLiveDataPayload(**_obd_kwargs(stft_idle_pct=127.0))


def test_ingestion_rejects_old_254_total_trim_delta() -> None:
    """total_trim_correction_delta=254.0 (old T-W-6 doubled rail) is rejected."""
    with pytest.raises(ValidationError):
        OBDLiveDataPayload(**_obd_kwargs(total_trim_correction_delta=254.0))


def test_ingestion_accepts_j1979_total_trim_limits() -> None:
    """total_trim_correction_delta accepts SAE J1979 doubled limits [-200.0, 198.44]."""
    high = OBDLiveDataPayload(**_obd_kwargs(total_trim_correction_delta=198.44))
    low = OBDLiveDataPayload(**_obd_kwargs(total_trim_correction_delta=-200.0))
    assert high.total_trim_correction_delta == 198.44
    assert low.total_trim_correction_delta == -200.0


def test_ingestion_accepts_j1979_per_trim_limits() -> None:
    """Per-trim channels and SecondOperatingPointFrame accept [-100.0, 99.22]."""
    p = OBDLiveDataPayload(**_obd_kwargs(stft_idle_pct=-100.0, ltft_idle_pct=99.22))
    assert p.stft_idle_pct == -100.0
    assert p.ltft_idle_pct == 99.22

    frame = SecondOperatingPointFrame(
        rpm_state_bucket=EngineStateBucket.STRESS_IDLE,
        engine_rpm=3800,
        total_trim_correction_delta=198.44,
        shrtft1=99.22,
        longft1=-100.0,
    )
    assert frame.total_trim_correction_delta == 198.44
    assert frame.shrtft1 == 99.22
    assert frame.longft1 == -100.0
