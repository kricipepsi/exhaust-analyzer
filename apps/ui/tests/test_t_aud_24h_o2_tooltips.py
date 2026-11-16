"""Tests for T-AUD-24h: per-widget upstream-O2 tooltip ranges."""

from pathlib import Path

from ui_payload import (
    FIELD_HELP,
    UPSTREAM_O2_NARROWBAND_MAX,
    UPSTREAM_O2_NARROWBAND_MIN,
    UPSTREAM_O2_WIDEBAND_AFR_MAX,
    UPSTREAM_O2_WIDEBAND_AFR_MIN,
    UPSTREAM_O2_WIDEBAND_LAMBDA_MAX,
    UPSTREAM_O2_WIDEBAND_LAMBDA_MIN,
)


def test_upstream_o2_field_help_bounds():
    """Each upstream-O2 FIELD_HELP entry matches its ui_payload min/max constants."""
    expected = {
        "obd_upstream_o2_val": (UPSTREAM_O2_NARROWBAND_MIN, UPSTREAM_O2_NARROWBAND_MAX),
        "obd_upstream_o2_lambda": (
            UPSTREAM_O2_WIDEBAND_LAMBDA_MIN,
            UPSTREAM_O2_WIDEBAND_LAMBDA_MAX,
        ),
        "obd_upstream_o2_afr": (
            UPSTREAM_O2_WIDEBAND_AFR_MIN,
            UPSTREAM_O2_WIDEBAND_AFR_MAX,
        ),
    }
    for key, bounds in expected.items():
        fh = FIELD_HELP[key]
        assert (fh.min_val, fh.max_val) == bounds


def test_upstream_o2_tooltip_suffixes():
    """Each upstream-O2 tooltip ends with its sensor-specific Range line."""
    expected_suffixes = {
        "obd_upstream_o2_val": "Range: 0.0\u20131.0 V",
        "obd_upstream_o2_lambda": "Range: 0.7\u20131.3 \u03bb",
        "obd_upstream_o2_afr": "Range: 10.0\u201320.0 AFR",
    }
    for key, suffix in expected_suffixes.items():
        assert FIELD_HELP[key].get_tooltip().endswith(suffix)


def test_app_py_upstream_o2_widgets_use_matching_field_help():
    """Each upstream-O2 st.number_input line in app.py binds its matching FIELD_HELP key."""
    app_text = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8"
    )
    lines = app_text.splitlines()
    expected_pairs = [
        ("UPSTREAM_O2_NARROWBAND_MIN", "obd_upstream_o2_val"),
        ("UPSTREAM_O2_WIDEBAND_LAMBDA_MIN", "obd_upstream_o2_lambda"),
        ("UPSTREAM_O2_WIDEBAND_AFR_MIN", "obd_upstream_o2_afr"),
    ]
    for const_min, key in expected_pairs:
        matching = [line for line in lines if f"min_value={const_min}" in line]
        assert len(matching) == 1
        assert f'help=FIELD_HELP["{key}"].get_tooltip()' in matching[0]
