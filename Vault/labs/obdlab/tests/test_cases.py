"""A1 — CSV-driven bounce-rate gate over obdlab_cases.csv.

Parametrises over the master-derived projection (194 OBD-decidable rows).
Asserts a decision-rate floor: fewer than 5% of signal-bearing cases may
return default shape (FLOOR_STANDALONE).
"""

from __future__ import annotations

import csv
from pathlib import Path

from obdlab.core.exceptions import ObdLabError
from tests.conftest import (
    build_inputs_from_csv_row,
    is_default_shape,
    is_signal_bearing,
)
from tests.fixtures.descriptor import build_obdlab_descriptor

FLOOR_STANDALONE = 5.0
CSV_PATH = Path(__file__).resolve().parent / "fixtures" / "obdlab_cases.csv"


def test_csv_bounce_rate() -> None:
    """A1: bounce rate over obdlab_cases.csv must be < FLOOR_STANDALONE."""
    descriptor = build_obdlab_descriptor()

    rejections: list[str] = []
    correct_abstentions: list[str] = []
    bounces: list[str] = []
    signal_moved: list[str] = []

    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            case_id = row.get("case_id", "?")
            raw_inputs, dna_view = build_inputs_from_csv_row(row)

            error = None
            try:
                payload = descriptor.entry_point(raw_inputs, dna_view)
            except ObdLabError as exc:
                error = exc

            if error is not None:
                rejections.append(case_id)
            elif not is_signal_bearing(row):
                correct_abstentions.append(case_id)
            elif is_default_shape(payload):
                bounces.append(case_id)
            else:
                signal_moved.append(case_id)

    total = len(rejections) + len(correct_abstentions) + len(signal_moved) + len(bounces)
    signal_total = len(signal_moved) + len(bounces)
    bounce_rate = (len(bounces) / signal_total * 100) if signal_total > 0 else 0.0

    print(f"\nA1 Bounce Report ({total} rows total):")
    print(f"  rejections:          {len(rejections):>4}")
    print(f"  correct-abstentions: {len(correct_abstentions):>4}")
    print(f"  signal-moved:        {len(signal_moved):>4}")
    print(f"  BOUNCE:              {len(bounces):>4}")
    print(f"  signal-bearing:      {signal_total:>4}")
    print(f"  bounce rate:         {bounce_rate:.1f}%")
    print(f"  floor:               {FLOOR_STANDALONE}%")
    if bounces:
        print(f"  bounce cases:        {bounces[:5]}")

    assert signal_total > 0, (
        "FATAL: zero signal-bearing rows — denominator is empty, gate fails closed"
    )
    assert bounce_rate < FLOOR_STANDALONE, (
        f"Bounce rate {bounce_rate:.1f}% exceeds FLOOR_STANDALONE {FLOOR_STANDALONE}%"
    )
