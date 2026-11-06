"""T-AUD-4s (F-C4-8): the composition's raw OBD ranges equal the UI form's.

Tags: NEW fails on the base fix/T-AUD-4s spec commit (no _OBD_RAW_RANGES).
"""

from __future__ import annotations

import re
from pathlib import Path

import ui_payload as U

from wired import composition as wc

APP = Path(__file__).resolve().parents[1] / "app.py"

_TRIMS = ("stft_idle_pct", "ltft_idle_pct", "stft_2500_pct", "ltft_2500_pct", "stft_load_pct", "ltft_load_pct")
_UI_RANGES = {
    **{k: (U.OBD_TRIM_MIN, U.OBD_TRIM_MAX) for k in _TRIMS},
    "mode06_catalyst_margin_pct": (U.ADV_CAT_MARGIN_MIN, U.ADV_CAT_MARGIN_MAX),
    "catalyst_index_ratio": (U.ADV_CAT_INDEX_MIN, U.ADV_CAT_INDEX_MAX),
    "mode06_o2_response_margin_pct": (U.ADV_O2_MARGIN_MIN, U.ADV_O2_MARGIN_MAX),
    "maf_actual_calc_delta_pct_idle": (U.ADV_MAF_DELTA_MIN, U.ADV_MAF_DELTA_MAX),
    "maf_actual_calc_delta_pct_2500": (U.ADV_MAF_DELTA_MIN, U.ADV_MAF_DELTA_MAX),
    "propane_trim_shift_pct": (U.ADV_MAF_DELTA_MIN, U.ADV_MAF_DELTA_MAX),
    "maf_gps_idle": (U.ADV_MAF_GPS_MIN, U.ADV_MAF_GPS_MAX),
    "maf_gps_2500": (U.ADV_MAF_GPS_MIN, U.ADV_MAF_GPS_MAX),
    "calc_airflow_gps_idle": (U.ADV_MAF_GPS_MIN, U.ADV_MAF_GPS_MAX),
    "calc_airflow_gps_2500": (U.ADV_MAF_GPS_MIN, U.ADV_MAF_GPS_MAX),
    "koeo_map_baro_delta_kpa": (U.ADV_MAP_BARO_MIN, U.ADV_MAP_BARO_MAX),
    "module_voltage_loaded_v": (U.ADV_VOLTAGE_MIN, U.ADV_VOLTAGE_MAX),
    "dlc_signal_ground_drop_v": (U.ADV_GND_DROP_MIN, U.ADV_GND_DROP_MAX),
    "calc_load_wot_pct": (U.OBD_LOAD_MIN, U.OBD_LOAD_MAX),
    "fuel_rail_pressure_load_kpa": (U.ADV_PRESSURE_MIN, U.ADV_PRESSURE_MAX),
    "wideband_lambda_wot": (U.ADV_LAMBDA_WOT_MIN, U.ADV_LAMBDA_WOT_MAX),
    "co2_idle_pct": (U.ADV_CO2_MIN, U.ADV_CO2_MAX),
    "tailpipe_o2_elevation_pct": (U.ADV_O2_ELEV_MIN, U.ADV_O2_ELEV_MAX),
    "downstream_o2_v": (U.OBD_O2_DN_MIN, U.OBD_O2_DN_MAX),
    "stored_dtc_count": (U.ADV_DTC_COUNT_MIN, U.ADV_DTC_COUNT_MAX),
    "pending_dtc_count": (U.ADV_DTC_COUNT_MIN, U.ADV_DTC_COUNT_MAX),
    "permanent_dtc_count": (U.ADV_DTC_COUNT_MIN, U.ADV_DTC_COUNT_MAX),
    "warmup_cycles_since_clear": (U.ADV_WARMUP_MIN, U.ADV_WARMUP_MAX),
    "miles_since_clear": (U.ADV_MILES_MIN, U.ADV_MILES_MAX),
}


def test_ranges_equal_the_ui_form() -> None:
    """NEW: every composition range equals the UI constant's range."""
    got = {k: (lo, hi) for k, (lo, hi, _kind) in wc._OBD_RAW_RANGES.items()}
    assert {k: v for k, v in got.items() if k != "mode06_min_margin_pct"} == _UI_RANGES


def test_mode06_min_margin_equals_the_app_literal() -> None:
    """NEW: mode06_min_margin_pct has no constant; its range is app.py's number_input literal."""
    src = APP.read_text(encoding="utf-8")
    m = re.search(r'"mode06_min_margin_pct \(%\)", min_value=(-?[\d.]+), max_value=(-?[\d.]+)', src)
    assert m is not None
    assert wc._OBD_RAW_RANGES["mode06_min_margin_pct"][:2] == (float(m.group(1)), float(m.group(2)))


def test_integer_channels_are_the_counts() -> None:
    """NEW: the int channels are the three DTC counts, the warm-up cycles and the miles."""
    ints = {k for k, (_lo, _hi, kind) in wc._OBD_RAW_RANGES.items() if kind is int}
    assert ints == {"stored_dtc_count", "pending_dtc_count", "permanent_dtc_count",
                    "warmup_cycles_since_clear", "miles_since_clear"}
