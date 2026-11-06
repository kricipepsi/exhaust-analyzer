"""T-AUD-4s (F-C4-8): raw OBD channels COMLab reads straight from the input are range-checked.

R1 _run_obdlab parses each of the 31 numeric raw channels through _raw_obd_value (ValueError when out
of range, not finite or not whole); R2 diagnose aborts with OBD_INPUT_OUT_OF_RANGE before any lab runs.
Tags: NEW fails on the base fix/T-AUD-4s spec commit; PIN passes there and after.
"""

from __future__ import annotations

from typing import Any

import pytest
from test_t_aud_1a_inputs import OBD, _assert_abort, _raw

from wired import composition as wc

PROBE_OBD = {"engine_rpm": 800, "coolant_temp_c": 90.0, "shrtft1": 2.0, "longft1": 3.0,
             "fuel_sys_status": "CL", "pid_oxygen_sensor_volts": 0.45}


def _run(**extra: Any):
    return wc._run_obdlab(dict(PROBE_OBD, **extra), wc._build_fallback_vin_dna(""))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("downstream_o2_v", 5.0),  # audit f7
        ("downstream_o2_v", "nan"),  # audit f7
        ("co2_idle_pct", -40.0),  # audit f7
        ("stft_idle_pct", 150),  # PIN: the mirror bound already raised (pydantic ValidationError is a ValueError)
        ("stored_dtc_count", "2.5"),  # audit: was a bare int() ValueError
        ("miles_since_clear", "inf"),
        ("catalyst_index_ratio", "abc"),
    ],
)
def test_run_obdlab_rejects_bad_raw_channel(field: str, value: Any) -> None:
    """NEW (PIN for stft_idle_pct): every bad raw channel raises ValueError naming the channel."""
    with pytest.raises(ValueError, match=field):
        _run(**{field: value})


def test_run_obdlab_accepts_every_range_edge() -> None:
    """NEW: each channel at its low and its high edge passes through unchanged (31 channels)."""
    assert len(wc._OBD_RAW_RANGES) == 31
    for edge in (0, 1):
        values = {key: rng[edge] for key, rng in wc._OBD_RAW_RANGES.items()}
        out = _run(**values)
        for key, expected in values.items():
            assert getattr(out, key) == expected, (key, edge)


def test_blank_raw_channel_stays_none() -> None:
    """PIN: an absent or blank raw channel is None, as before."""
    out = _run(downstream_o2_v="", co2_idle_pct=None)
    assert out.downstream_o2_v is None
    assert out.co2_idle_pct is None


def test_diagnose_aborts_out_of_range() -> None:
    """NEW: diagnose returns the invalid_input verdict naming every bad channel; no lab runs."""
    res = wc.diagnose(_raw(obd=dict(OBD, downstream_o2_v=5.0, co2_idle_pct=-40.0)))
    _assert_abort(res, "OBD_INPUT_OUT_OF_RANGE", "downstream_o2_v", "co2_idle_pct")


def test_diagnose_aborts_instead_of_crashing() -> None:
    """NEW: a value outside a mirror bound gives the abort verdict, not an exception out of diagnose."""
    res = wc.diagnose(_raw(obd=dict(OBD, stft_idle_pct=150)))
    _assert_abort(res, "OBD_INPUT_OUT_OF_RANGE", "stft_idle_pct")


def test_diagnose_in_range_runs() -> None:
    """PIN: in-range raw channels give a verdict, not an abort."""
    res = wc.diagnose(_raw(obd=dict(OBD, downstream_o2_v=0.7, co2_idle_pct=14.5)))
    assert res.diagnostic_verdict.fault_family != "invalid_input"
