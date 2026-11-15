"""T-AUD-24a (R5): UI OBD_TRIM_* constants match the SAE J1979 [-100.0, 99.22] % range."""

from __future__ import annotations

from ui_payload import OBD_TRIM_MAX, OBD_TRIM_MIN


def test_ui_obd_trim_bounds_match_j1979() -> None:
    """OBD_TRIM_MIN/MAX pin the SAE J1979 PIDs 06-09 range [-100.0, 99.22]."""
    assert OBD_TRIM_MIN == -100.0
    assert OBD_TRIM_MAX == 99.22
