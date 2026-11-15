"""T-AUD-24a (R5): wired composition rejects old ±127 trim bounds and accepts SAE J1979 [-100.0, 99.22]."""

from __future__ import annotations

import pytest
from test_t_aud_1a_inputs import OBD, _assert_abort, _raw

from wired import composition as wc

PROBE_OBD = {
    "engine_rpm": 800,
    "coolant_temp_c": 90.0,
    "shrtft1": 2.0,
    "longft1": 3.0,
    "fuel_sys_status": "CL",
    "pid_oxygen_sensor_volts": 0.45,
}


def test_run_obdlab_rejects_old_127_stft_idle_pct() -> None:
    """stft_idle_pct=127.0 is rejected by _run_obdlab as out of SAE J1979 range."""
    with pytest.raises(ValueError, match="stft_idle_pct"):
        wc._run_obdlab(dict(PROBE_OBD, stft_idle_pct=127.0), wc._build_fallback_vin_dna(""))


def test_diagnose_aborts_on_old_127_stft_idle_pct() -> None:
    """diagnose aborts with OBD_INPUT_OUT_OF_RANGE when stft_idle_pct=127.0."""
    res = wc.diagnose(_raw(obd=dict(OBD, stft_idle_pct=127.0)))
    _assert_abort(res, "OBD_INPUT_OUT_OF_RANGE", "stft_idle_pct")


def test_run_obdlab_accepts_j1979_trim_limits_and_rejects_just_outside() -> None:
    """_run_obdlab accepts [-100.0, 99.22] and rejects -100.1 / 99.3 on stft_idle_pct."""
    low = wc._run_obdlab(dict(PROBE_OBD, stft_idle_pct=-100.0), wc._build_fallback_vin_dna(""))
    high = wc._run_obdlab(dict(PROBE_OBD, stft_idle_pct=99.22), wc._build_fallback_vin_dna(""))
    assert low.stft_idle_pct == -100.0
    assert high.stft_idle_pct == 99.22

    for bad in (-100.1, 99.3):
        with pytest.raises(ValueError, match="stft_idle_pct"):
            wc._run_obdlab(dict(PROBE_OBD, stft_idle_pct=bad), wc._build_fallback_vin_dna(""))
