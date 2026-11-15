from __future__ import annotations

from pathlib import Path

import yaml

_ERA_MASKS_PATH = (
    Path(__file__).resolve().parents[2] / "comlab" / "config" / "eras_sensitivity_masks.yaml"
)

_EXPECTED_LAMBDA_TOLERANCE = {
    "HORIZON_LEGACY": 0.10,
    "HORIZON_ADAPTIVE": 0.05,
    "HORIZON_MODERN": 0.02,
}


def test_era_masks_drop_dead_co_hc_keys() -> None:
    data = yaml.safe_load(_ERA_MASKS_PATH.read_text(encoding="utf-8"))
    horizons = data["horizons"]
    for name, horizon in horizons.items():
        thresholds = horizon.get("gas_lab_thresholds", {})
        assert "gas_co_max_pct" not in thresholds, f"{name} still has gas_co_max_pct"
        assert "gas_hc_max_ppm" not in thresholds, f"{name} still has gas_hc_max_ppm"


def test_era_masks_preserve_lambda_tolerance() -> None:
    data = yaml.safe_load(_ERA_MASKS_PATH.read_text(encoding="utf-8"))
    horizons = data["horizons"]
    actual = {
        name: horizon["gas_lab_thresholds"]["lambda_tolerance"]
        for name, horizon in horizons.items()
    }
    assert actual == _EXPECTED_LAMBDA_TOLERANCE
