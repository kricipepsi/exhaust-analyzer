"""Per-``ChemicalSignature`` reachability probe for the rule engine.

Verifies that every ``ChemicalSignature`` value can be emitted by
``classify()`` given at least one valid ``GasReading`` + ``GasLabDnaView``
pair.  Uses the boundary grid for coarse coverage and fault-probe
midpoints for narrow-window values.

Created for T-P8-6.  References:
- ``GAS_WIKI §7.12`` (TIMING_OVER_ADVANCED)
- ``GAS_WIKI §7.16`` (WORN_ENGINE)
- ``GAS_WIKI §7.29`` (EGR_DILUTION_MISFIRE)
- ``GASLAB_AUDIT_2026-05-19.md`` (AF-1, AF-2, AF-3)
"""

from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.rule_engine import classify


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _dna(**overrides: object) -> GasLabDnaView:
    defaults: dict[str, object] = dict(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="NON_GDI",
        induction_type="NA",
        upstream_o2_type="NARROWBAND",
        has_catalyst=True,
        egr_equipped=False,
        confidence="HIGH",
    )
    defaults.update(overrides)
    return GasLabDnaView(**defaults)  # type: ignore[arg-type]


def _probe_grid() -> list[GasReading]:
    """Coarse boundary grid at key positions."""
    readings: list[GasReading] = []
    for hc in (0, 50, 100, 200, 500, 1000, 2000):
        for co in (0.0, 0.1, 0.5, 1.0, 2.0, 5.0):
            for co2 in (5.0, 10.0, 12.0, 14.0, 16.0):
                for o2 in (0.0, 0.3, 0.5, 1.0, 2.0, 5.0):
                    for nox in (0, 50, 100, 500, 1000, 2000):
                        readings.append(GasReading(hc=hc, co=co, co2=co2, o2=o2, nox=nox))
    return readings


def _fault_midpoint_readings(ontology: dict) -> list[tuple[str, GasReading]]:
    """Generate a midpoint reading for each fault signature in the ontology."""
    pairs: list[tuple[str, GasReading]] = []
    faults = ontology.get("faults", {})
    for name, entry in faults.items():
        if name in ("SAMPLE_INVALID", "COOLANT_LEAK_INTERNAL"):
            continue
        sig = entry["signature"]
        reading = GasReading(
            hc=int((sig["hc"]["min"] + sig["hc"]["max"]) / 2),
            co=(sig["co"]["min"] + sig["co"]["max"]) / 2,
            co2=(sig["co2"]["min"] + sig["co2"]["max"]) / 2,
            o2=(sig["o2"]["min"] + sig["o2"]["max"]) / 2,
            nox=int((sig["nox"]["min"] + sig["nox"]["max"]) / 2),
        )
        pairs.append((name, reading))
    return pairs


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def ontology() -> dict:
    return load_ontology()


@pytest.fixture(scope="module")
def dna_variants() -> list[GasLabDnaView]:
    return [
        _dna(),
        _dna(fuel_delivery_type="GDI"),
        _dna(egr_equipped=True),
        _dna(fuel_delivery_type="GDI", egr_equipped=True),
    ]


# ---------------------------------------------------------------------------
# T-P8-6 specific: the three AUDIT-unreachable values
# ---------------------------------------------------------------------------

T_P8_6_TARGETS = [
    "TIMING_OVER_ADVANCED",   # AF-1
    "EGR_DILUTION_MISFIRE",   # AF-2
    "WORN_ENGINE",            # AF-3
]

# Values that cannot be reached without external evidence GASLab cannot
# consume and are deferred pending architect decision.
DEFERRED_UNREACHABLE: set[str] = set()


@pytest.mark.parametrize("target", T_P8_6_TARGETS)
def test_t_p8_6_target_reachable(
    target: str, ontology: dict, dna_variants: list[GasLabDnaView]
) -> None:
    """Each T-P8-6 target value is reachable via classify().

    Uses probe grid + fault midpoints.  If a value is truly unreachable
    without cross-lab evidence, it must be listed in DEFERRED_UNREACHABLE
    with a justifying comment.
    """
    if target in DEFERRED_UNREACHABLE:
        pytest.skip(f"{target} deferred — see T-P8-6 progress note")

    engine_state = EngineStateBucket.STABILIZED_IDLE
    probe_readings = _probe_grid() + [
        r for _, r in _fault_midpoint_readings(ontology)
    ]

    seen = False
    for reading in probe_readings:
        for dna in dna_variants:
            chem, _ = classify(reading, dna, engine_state, ontology)
            if chem.value == target:
                seen = True
                break
        if seen:
            break

    assert seen, (
        f"{target} not reachable by any probe reading across "
        f"{len(dna_variants)} DNA variants. "
        f"Add to DEFERRED_UNREACHABLE with justification if cross-lab "
        f"evidence is required."
    )


# ---------------------------------------------------------------------------
# Full-enum reachability: every ChemicalSignature value
# ---------------------------------------------------------------------------

def _collect_reachable(
    ontology: dict, dna_variants: list[GasLabDnaView]
) -> set[str]:
    engine_state = EngineStateBucket.STABILIZED_IDLE
    seen: set[str] = set()

    # Probe grid
    for reading in _probe_grid():
        for dna in dna_variants:
            chem, _ = classify(reading, dna, engine_state, ontology)
            seen.add(chem.value)

    # Fault midpoints
    for _, reading in _fault_midpoint_readings(ontology):
        for dna in dna_variants:
            chem, _ = classify(reading, dna, engine_state, ontology)
            seen.add(chem.value)

    # Grammar-gated: COOLANT_LEAK_INTERNAL (requires block_test_passed)
    # wiki: GAS_WIKI §8.7
    coolant_probe = GasReading(hc=450, co=0.15, co2=11.2, o2=2.7, nox=5)
    chem, _ = classify(
        coolant_probe, dna_variants[0], engine_state, ontology,
        block_test_passed=True,
    )
    seen.add(chem.value)

    # Grammar-gated: CAM_TIMING_RETARDED_MAF via WVT rule (priority 82)
    # wiki: GAS_WIKI §8.6 — hc > 1000, o2 > 2.0
    maf_probe = GasReading(hc=1200, co=0.6, co2=10.0, o2=4.5, nox=80)
    for dna in dna_variants:
        chem, _ = classify(maf_probe, dna, engine_state, ontology)
        seen.add(chem.value)

    # CAM_TIMING_ADVANCED (valid triangle range)
    # wiki: GAS_WIKI §8.6
    adv_probe = GasReading(hc=300, co=0.3, co2=12.5, o2=1.5, nox=20)
    for dna in dna_variants:
        chem, _ = classify(adv_probe, dna, engine_state, ontology)
        seen.add(chem.value)

    # Grammar-gated: IGNITION_MISFIRE via masking rule (priority 85)
    # wiki: GAS_WIKI §8.4 — hc > 1000, o2 > 3.0, nox < 50
    mask_probe = GasReading(hc=1200, co=0.5, co2=11.0, o2=4.0, nox=30)
    for dna in dna_variants:
        chem, _ = classify(mask_probe, dna, engine_state, ontology)
        seen.add(chem.value)

    return seen


def test_all_chemical_signature_values_reachable(
    ontology: dict, dna_variants: list[GasLabDnaView],
) -> None:
    """Every ChemicalSignature value appears at least once via classify()."""
    seen = _collect_reachable(ontology, dna_variants)
    all_values = set(ChemicalSignature.__members__.values())
    missing = all_values - seen - DEFERRED_UNREACHABLE

    assert not missing, (
        f"{len(missing)} ChemicalSignature value(s) unreachable: "
        f"{sorted(v.value for v in missing)}. "
        f"Seen: {len(seen)}/{len(all_values)}. "
        f"Deferred: {sorted(DEFERRED_UNREACHABLE)}."
    )


# ---------------------------------------------------------------------------
# AF-1 specific: TIMING_OVER_ADVANCED differentiator check
# ---------------------------------------------------------------------------

def test_timing_over_advanced_distinct_from_hct(
    ontology: dict, dna_variants: list[GasLabDnaView],
) -> None:
    """TIMING_OVER_ADVANCED must be reachable by a reading that HCT cannot claim.

    The only gas-band distinction is co=0.0 (TOA co min=0.0 vs HCT co min=0.1).
    This verifies the boundary exists and the specificity tiebreak works.
    """
    if "TIMING_OVER_ADVANCED" in DEFERRED_UNREACHABLE:
        pytest.skip("TIMING_OVER_ADVANCED deferred")

    engine_state = EngineStateBucket.STABILIZED_IDLE

    # co=0.0 excludes HIGH_COMBUSTION_TEMP (co min 0.1) and
    # EGR_STUCK_CLOSED (co min 0.1), leaving TIMING_OVER_ADVANCED.
    reading = GasReading(hc=50, co=0.0, co2=15.0, o2=0.3, nox=1500)
    candidates: set[str] = set()
    for dna in dna_variants:
        chem, _ = classify(reading, dna, engine_state, ontology)
        candidates.add(chem.value)

    assert "TIMING_OVER_ADVANCED" in candidates, (
        f"TIMING_OVER_ADVANCED not reachable with co=0.0 reading. "
        f"Candidates: {sorted(candidates)}"
    )
    assert "HIGH_COMBUSTION_TEMP" not in candidates, (
        "HIGH_COMBUSTION_TEMP matched reading with co=0.0 "
        "(should be excluded by co min=0.1)"
    )
