"""A2 — Combinatorial generator: pairwise corner sweep over fault boxes.

For each box with ≥2 dimensions, generates 4 corners per unordered pair
and asserts that interior points move the target channel at ≥95% rate.
"""

from __future__ import annotations

import itertools
from typing import Any

from tests.conftest import channel_moved_for_box, point_in_box
from tests.fixtures.descriptor import build_obdlab_descriptor

FLOOR_STANDALONE = 5.0

_BASELINE: dict[str, Any] = {
    "engine_rpm": 800,
    "coolant_temp_c": 90.0,
    "shrtft1": 0.0,
    "longft1": 0.0,
    "shrtft2": 0.0,
    "longft2": 0.0,
    "number_of_banks": 1,
}

_BOX_META: dict[str, dict[str, Any]] = {
    "o2_stuck_lean": {"upstream_o2_type": "NARROWBAND_0_TO_1V"},
    "o2_stuck_rich": {"upstream_o2_type": "NARROWBAND_0_TO_1V"},
    "lambda_delta_rich": {"upstream_o2_type": "WIDEBAND_LINEAR"},
    "lambda_delta_lean": {"upstream_o2_type": "WIDEBAND_LINEAR"},
    "ve_idle_collapse": {"air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK"},
}

GATED = {"trim_positive", "trim_negative", "o2_stuck_lean", "o2_stuck_rich",
         "lambda_delta_rich", "lambda_delta_lean"}


def _centroid(dims: dict[str, tuple[float, float]]) -> dict[str, float]:
    return {dim: (lo + hi) / 2.0 for dim, (lo, hi) in dims.items()}


def test_combinatorial_channel_move_rate() -> None:
    """A2 combinatorial: pairwise corners, ≥95% channel-move on interior."""
    descriptor = build_obdlab_descriptor()

    per_box: dict[str, dict[str, int]] = {}

    for sig, box in descriptor.boxes.items():
        dims = box.dimensions
        if len(dims) < 2:
            continue

        centroid = _centroid(dims)
        meta = _BOX_META.get(sig, {})
        interior = 0
        interior_moved = 0

        # All unordered pairs of dimensions
        for d1, d2 in itertools.combinations(sorted(dims), 2):
            (lo1, hi1) = dims[d1]
            (lo2, hi2) = dims[d2]
            corners = [(lo1, lo2), (lo1, hi2), (hi1, lo2), (hi1, hi2)]

            for v1, v2 in corners:
                point = dict(_BASELINE)
                point.update(centroid)
                point[d1] = v1
                point[d2] = v2
                if meta:
                    point["_dna_meta"] = meta

                if not point_in_box(point, dims):
                    continue

                interior += 1
                raw_inputs, dna_view = descriptor.build_args(point)
                try:
                    payload = descriptor.entry_point(raw_inputs, dna_view)
                except Exception:
                    continue

                if channel_moved_for_box(payload, sig):
                    interior_moved += 1

        per_box[sig] = {"interior": interior, "moved": interior_moved}

    # Report
    print("\nA2 Combinatorial Report:")
    for sig, counts in sorted(per_box.items()):
        rate = (
            (counts["moved"] / counts["interior"] * 100)
            if counts["interior"] > 0
            else 100.0
        )
        gated_mark = " [GATED]" if sig in GATED else " [char]"
        print(
            f"  {sig:<25s}  interior={counts['interior']:>3d}  "
            f"moved={counts['moved']:>3d}  rate={rate:.0f}%{gated_mark}"
        )

    gated_interior = sum(per_box[s]["interior"] for s in GATED if s in per_box)
    gated_moved = sum(per_box[s]["moved"] for s in GATED if s in per_box)
    gated_rate = (gated_moved / gated_interior * 100) if gated_interior > 0 else 100.0
    print(f"  {'GATED OVERALL':<25s}  interior={gated_interior:>3d}  "
          f"moved={gated_moved:>3d}  rate={gated_rate:.0f}%")

    assert gated_interior > 0, (
        "FATAL: zero interior points in gated boxes"
    )
    assert gated_rate >= (100.0 - FLOOR_STANDALONE), (
        f"Gated channel-move rate {gated_rate:.1f}% below floor "
        f"{100.0 - FLOOR_STANDALONE:.1f}%"
    )
