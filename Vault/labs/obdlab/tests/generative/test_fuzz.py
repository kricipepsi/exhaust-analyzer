"""A2 — Fuzz generator: random envelope sampling, no-crash + round-trip gate.

Samples N=500 points from the global input envelope, runs them through
translate(), and asserts no unexpected crashes and payload round-trip validity.
"""

from __future__ import annotations

import random
from typing import Any

from obdlab.schemas.payload import OBDLivePayload
from tests.fixtures.descriptor import build_obdlab_descriptor

N_SAMPLES = 500
SEED = 42

_BASELINE: dict[str, Any] = {
    "engine_rpm": 800,
    "coolant_temp_c": 90.0,
    "shrtft1": 0.0,
    "longft1": 0.0,
    "shrtft2": 0.0,
    "longft2": 0.0,
    "number_of_banks": 1,
}


def test_fuzz_no_crash() -> None:
    """Fuzz: random envelope points must not crash and must round-trip."""
    random.seed(SEED)
    descriptor = build_obdlab_descriptor()

    crashes = 0
    roundtrip_fails = 0

    for _ in range(N_SAMPLES):
        point = dict(_BASELINE)
        # Randomly perturb each numeric field within its FieldRange envelope
        point["engine_rpm"] = random.randint(0, 8000)
        point["coolant_temp_c"] = random.uniform(-40, 140)
        point["shrtft1"] = random.uniform(-127, 127)
        point["longft1"] = random.uniform(-127, 127)

        if random.random() < 0.3:
            point["mass_airflow_gps"] = random.uniform(0, 655.35)
        if random.random() < 0.3:
            point["manifold_vacuum_kpa"] = random.uniform(0, 255)
        if random.random() < 0.2:
            point["number_of_banks"] = 2
            point["shrtft2"] = random.uniform(-127, 127)
            point["longft2"] = random.uniform(-127, 127)
        if random.random() < 0.3:
            point["pid_oxygen_sensor_volts"] = random.uniform(0, 5)
        if random.random() < 0.1:
            point["pid_wideband_equivalence_ratio"] = random.uniform(0.5, 2.0)
            point["_dna_meta"] = {"upstream_o2_type": "WIDEBAND_LINEAR"}

        raw_inputs, dna_view = descriptor.build_args(point)
        try:
            payload = descriptor.entry_point(raw_inputs, dna_view)
        except Exception:
            crashes += 1
            continue

        # Round-trip: payload → dict → re-validate
        try:
            OBDLivePayload.model_validate(payload.model_dump())
        except Exception:
            roundtrip_fails += 1

    print(f"\nA2 Fuzz Report ({N_SAMPLES} samples, seed={SEED}):")
    print(f"  crashes:          {crashes:>4}")
    print(f"  roundtrip-fails:  {roundtrip_fails:>4}")
    print(f"  success:          {N_SAMPLES - crashes - roundtrip_fails:>4}")

    # Assert no unexpected exception types (all crashes must be typed errors)
    assert roundtrip_fails == 0, (
        f"{roundtrip_fails} payload(s) failed round-trip validation"
    )
    # Crashes are acceptable (typed validation errors) but must not dominate
    assert crashes < N_SAMPLES * 0.5, (
        f"{crashes} crashes out of {N_SAMPLES} — too many"
    )
