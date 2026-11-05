"""T-AUD-4h — the user's DTC codes reach OBDLab as ``active_dtcs`` (F-C3-3).

Ruling R1 of the task. NEW tags fail on the base commit (the helper does not exist).
"""

from __future__ import annotations

from wired.composition import _with_user_dtcs


def test_user_codes_become_active_dtcs() -> None:
    """NEW: codes of every mode, in order, without duplicates; the caller's dict is untouched."""
    obd_inputs = {"shrtft1": 1.0}
    dtc_inputs = {"raw_dtcs": {"$03": ["P0131", "P0300"], "$07": ["P0131", "P0340"]}}
    out = _with_user_dtcs(obd_inputs, dtc_inputs)
    assert out["active_dtcs"] == ["P0131", "P0300", "P0340"]
    assert "active_dtcs" not in obd_inputs


def test_explicit_active_dtcs_win() -> None:
    """NEW: a non-empty ``active_dtcs`` in the OBD inputs stays unchanged."""
    dtc_inputs = {"raw_dtcs": {"$03": ["P0131"]}}
    out = _with_user_dtcs({"active_dtcs": ["P0171"]}, dtc_inputs)
    assert out["active_dtcs"] == ["P0171"]


def test_no_dtc_input_or_no_codes_adds_nothing() -> None:
    """NEW: no DTC input, or no codes, adds no key."""
    assert "active_dtcs" not in _with_user_dtcs({"shrtft1": 1.0}, None)
    assert "active_dtcs" not in _with_user_dtcs({"shrtft1": 1.0}, {"raw_dtcs": {}})
