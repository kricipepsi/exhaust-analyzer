"""A2 — Boundary generator: per-dimension edge-point sweep over fault boxes.

For each box, for each continuous dimension, generates 6 boundary points
(min±ε, max±ε) and asserts that interior points move the target channel
at ≥ 95% rate.
"""

from __future__ import annotations

from typing import Any

from tests.conftest import channel_moved_for_box, point_in_box
from tests.fixtures.descriptor import build_obdlab_descriptor

FLOOR_STANDALONE = 5.0  # max allowed miss rate = 5%, so min move rate = 95%
EPS_FLOAT = 0.01
EPS_INT = 1.0

# Baseline input values for fields the box dimensions don't cover.
# Without these the pipeline freezes (e.g. engine_rpm=0 triggers
# COLD_OPEN_LOOP_INVALID).
_BASELINE: dict[str, Any] = {
    "engine_rpm": 800,
    "coolant_temp_c": 90.0,
    "shrtft1": 0.0,
    "longft1": 0.0,
    "shrtft2": 0.0,
    "longft2": 0.0,
    "number_of_banks": 1,
}

# Box definitions from descriptor.py _BOX_DEFS — replicated here for
# the per-box dna_meta hints (narrowband vs wideband, etc.).
_BOX_META: dict[str, dict[str, Any]] = {
    "o2_stuck_lean": {"upstream_o2_type": "NARROWBAND_0_TO_1V"},
    "o2_stuck_rich": {"upstream_o2_type": "NARROWBAND_0_TO_1V"},
    "lambda_delta_rich": {"upstream_o2_type": "WIDEBAND_LINEAR"},
    "lambda_delta_lean": {"upstream_o2_type": "WIDEBAND_LINEAR"},
    "ve_idle_collapse": {"air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK"},
}


def _is_continuous_dim(dim: str, lo: float, hi: float) -> bool:
    """Enum/equality dimensions have lo == hi; continuous have lo < hi."""
    return lo < hi


def _eps_for(dim: str, lo: float, hi: float) -> float:
    """Pick epsilon based on dimension type."""
    if dim == "engine_rpm":
        return float(EPS_INT)
    return EPS_FLOAT * max(hi - lo, 1.0)


def _centroid(box_dims: dict[str, tuple[float, float]]) -> dict[str, float]:
    """Compute the centroid of a box."""
    return {dim: (lo + hi) / 2.0 for dim, (lo, hi) in box_dims.items()}


def test_boundary_channel_move_rate() -> None:
    """A2 boundary: ≥ 95% channel-move rate on interior points."""
    descriptor = build_obdlab_descriptor()

    total_interior = 0
    total_interior_moved = 0
    per_box: dict[str, dict[str, int]] = {}

    for sig, box in descriptor.boxes.items():
        dims = box.dimensions
        box_centroid = _centroid(dims)
        meta = _BOX_META.get(sig, {})
        interior = 0
        interior_moved = 0

        for dim, (lo, hi) in dims.items():
            if not _is_continuous_dim(dim, lo, hi):
                continue

            eps = _eps_for(dim, lo, hi)
            candidates = [lo - eps, lo, lo + eps, hi - eps, hi, hi + eps]

            for val in candidates:
                point = dict(_BASELINE)
                point.update(box_centroid)
                point[dim] = val
                # Add DNA meta so build_args knows narrowband vs wideband
                if meta:
                    point["_dna_meta"] = meta

                inside = point_in_box(point, dims)
                if not inside:
                    continue

                interior += 1
                raw_inputs, dna_view = descriptor.build_args(point)
                try:
                    payload = descriptor.entry_point(raw_inputs, dna_view)
                except Exception:
                    continue  # rejection — don't count against move rate

                if channel_moved_for_box(payload, sig):
                    interior_moved += 1

        per_box[sig] = {"interior": interior, "moved": interior_moved}
        total_interior += interior
        total_interior_moved += interior_moved

    # Report
    print(f"\nA2 Boundary Report ({len(descriptor.boxes)} boxes):")
    for sig, counts in sorted(per_box.items()):
        rate = (
            (counts["moved"] / counts["interior"] * 100)
            if counts["interior"] > 0
            else 100.0
        )
        print(
            f"  {sig:<25s}  interior={counts['interior']:>3d}  "
            f"moved={counts['moved']:>3d}  rate={rate:.0f}%"
        )

    overall_rate = (
        (total_interior_moved / total_interior * 100)
        if total_interior > 0
        else 100.0
    )
    print(
        f"  {'OVERALL':<25s}  interior={total_interior:>3d}  "
        f"moved={total_interior_moved:>3d}  rate={overall_rate:.0f}%"
    )

    # Gated boxes: well-calibrated, geometric oracle applies.  Must pass ≥95%.
    # Characterization boxes: approximate (VE) or complex (bank_asym) —
    # reported but not gated.
    _gated = {"trim_positive", "trim_negative", "o2_stuck_lean", "o2_stuck_rich",
              "lambda_delta_rich", "lambda_delta_lean"}
    gated_interior = sum(per_box[s]["interior"] for s in _gated)
    gated_moved = sum(per_box[s]["moved"] for s in _gated)
    gated_rate = (gated_moved / gated_interior * 100) if gated_interior > 0 else 100.0
    print(f"\n  Gated boxes ({len(_gated)}):  interior={gated_interior}  "
          f"moved={gated_moved}  rate={gated_rate:.0f}%")

    assert gated_interior > 0, (
        "FATAL: zero interior points in gated boxes — gate fails closed"
    )
    assert gated_rate >= (100.0 - FLOOR_STANDALONE), (
        f"Gated channel-move rate {gated_rate:.1f}% below floor "
        f"{100.0 - FLOOR_STANDALONE:.1f}%"
    )
