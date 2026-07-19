"""Tests for ``gaslab/rule_engine.py`` — rule engine graph traversal.

Covers the five success criteria from ``T-P4-1_rule_engine.md``.
"""

from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.resolution import _resolve_lean_timing_cosurvival, apply_differentiators
from gaslab.rule_engine import _coc_adjust_normal_bounds, _matching_fault_candidates, classify


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def ontology() -> dict:
    return load_ontology()


def _dna(**overrides: object) -> GasLabDnaView:
    """Build a minimal valid ``GasLabDnaView`` with optional overrides."""
    defaults: dict[str, object] = dict(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="PORT",
        induction_type="NA",
        upstream_o2_type="WIDEBAND",
        has_catalyst=True,
        egr_equipped=False,
        confidence="HIGH",
    )
    defaults.update(overrides)
    return GasLabDnaView(**defaults)  # type: ignore[arg-type]


def _reading(**overrides: object) -> GasReading:
    """Build a nominal ``GasReading`` with optional overrides."""
    defaults: dict[str, object] = dict(
        hc=15, co=0.2, co2=15.0, o2=0.2, nox=50,
    )
    defaults.update(overrides)
    return GasReading(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 1. test_normal_operation_classifies
# ---------------------------------------------------------------------------


def test_normal_operation_classifies(ontology: dict) -> None:
    """Given a normal-operation gas profile, classify returns NORMAL_OPERATION."""
    reading = _reading()
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.NORMAL_OPERATION
    assert validity == SampleValidity.VALID


# ---------------------------------------------------------------------------
# 2. test_misfire_via_masking_rule
# ---------------------------------------------------------------------------


def test_misfire_via_masking_rule(ontology: dict) -> None:
    """High HC + high O2 + low NOx triggers masking override → IGNITION_MISFIRE.

    Per ``GAS_WIKI §8.4``: HC > 1000 ppm AND O2 > 3.0 % AND NOx < 50 ppm
    must override any LEAN verdict to IGNITION_MISFIRE.
    """
    reading = _reading(
        hc=1500,  # wiki: GAS_WIKI §8.4 — > 1000 ppm
        co=0.2, co2=10.0,
        o2=5.0,  # wiki: GAS_WIKI §8.4 — > 3.0 %
        nox=30,  # wiki: GAS_WIKI §8.4 — < 50 ppm
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.IGNITION_MISFIRE, (
        f"masking rule should override to IGNITION_MISFIRE, got {chem}"
    )
    assert validity == SampleValidity.VALID


# ---------------------------------------------------------------------------
# 3. test_collision_routes_to_external_o2
# ---------------------------------------------------------------------------


def test_collision_routes_to_external_o2(ontology: dict) -> None:
    """High CO + high O2 triggers collision rule → EXTERNAL_O2_SUSPECT.

    Per ``GAS_WIKI §8.5``: CO > 0.45 % AND O2 > 2.0 % is physically
    impossible in a single combustion event.  The triangle sum determines
    whether RICH_MISFIRE or EXHAUST_AIR_LEAK is the correct label.
    """
    reading = _reading(
        hc=50,
        co=3.0,  # wiki: GAS_WIKI §8.5 — > 0.45 %
        co2=11.0,
        o2=2.5,  # wiki: GAS_WIKI §8.5 — > 2.0 %
        nox=50,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    # Triangle sum = 3.0 + 11.0 + 2.5 = 16.5 > 16 → EXHAUST_AIR_LEAK
    assert chem == ChemicalSignature.EXHAUST_AIR_LEAK, (
        f"collision with sum > 16 should emit EXHAUST_AIR_LEAK, got {chem}"
    )
    assert validity == SampleValidity.EXTERNAL_O2_SUSPECT, (
        f"collision should set EXTERNAL_O2_SUSPECT, got {validity}"
    )


# ---------------------------------------------------------------------------
# 4. test_dna_gate_suppresses_gdi_fault
# ---------------------------------------------------------------------------


def test_dna_gate_suppresses_gdi_fault(ontology: dict) -> None:
    """GDI_HPFP signature with non-GDI DNA → VACUUM_REGULATOR_DIAPHRAGM_RUPTURE.

    Per ``GAS_WIKI §7.19/§7.20``: both faults share identical tailpipe
    signatures.  The GDI_HPFP dna_gate requires fuel_delivery_type == GDI;
    when DNA says PORT, the GDI fault is suppressed and the VR diaphragm
    rupture survives via its differentiator edge.
    """
    reading = _reading(
        hc=500,  # wiki: GAS_WIKI §7.19 — > 300 ppm
        co=5.0,  # wiki: GAS_WIKI §7.19 — > 3.0 %
        co2=10.0,
        o2=0.1,  # wiki: GAS_WIKI §7.19 — very low
        nox=20,
    )
    dna = _dna(fuel_delivery_type="NON_GDI")
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.VACUUM_REGULATOR_DIAPHRAGM_RUPTURE, (
        f"non-GDI DNA should suppress GDI_HPFP, got {chem}"
    )
    assert validity == SampleValidity.VALID


# ---------------------------------------------------------------------------
# 5. test_sample_invalid_halts
# ---------------------------------------------------------------------------


def test_sample_invalid_halts(ontology: dict) -> None:
    """Triangle-failing reading halts → SAMPLE_INVALID without fault traversal.

    Per ``GAS_WIKI §6.1``: CO+CO2+O2 < 14 % → INVALID.  The engine must
    short-circuit and never enter the fault atlas.
    """
    reading = _reading(
        hc=10, co=0.1, co2=5.0, o2=1.0, nox=50,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.SAMPLE_INVALID, (
        f"triangle sum < 14 should emit SAMPLE_INVALID, got {chem}"
    )
    assert validity == SampleValidity.INVALID


def test_exhaust_air_leak_low_triangle_sum_routes_before_gate(ontology: dict) -> None:
    """Low triangle sum with HC-normal air ingress routes to EXHAUST_AIR_LEAK."""
    reading = _reading(
        hc=50,  # vocab: GAS_VOCABULARY §10.1 normal_borderline.max
        co=0.2,  # wiki: GAS_WIKI §7.7 — normal/low CO
        co2=10.5,  # wiki: GAS_WIKI §7.7 — low CO2
        o2=2.5,  # wiki: GAS_WIKI §7.7 — O2 > 2 %
        nox=50,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.EXHAUST_AIR_LEAK
    assert validity == SampleValidity.EXTERNAL_O2_SUSPECT


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 6. test_cam_timing_emitted_for_canonical_signature
# ---------------------------------------------------------------------------


def test_cam_timing_emitted_for_canonical_signature(ontology: dict) -> None:
    """Cam-timing signature (HC > 1000, O2 > 2.0, CO present, MAF bounds) classifies to CAM_TIMING_RETARDED_MAF.

    Per ``GAS_WIKI §8.6``: HC > 1000 ppm AND CO present AND O₂ > 2 %.
    The canonical reading below satisfies the collision rule as well
    (co > 0.45 AND o2 > 2.0), but the cam-timing rule at priority 82 fires
    before collision at priority 80.

    Triangle sum = 0.6 + 10.0 + 4.5 = 15.1 -> validity is VALID.
    """
    reading = _reading(
        hc=1200,  # wiki: GAS_WIKI §8.6 — > 1000 ppm
        co=0.6,   # wiki: GAS_WIKI §8.6 — present
        co2=10.0,
        o2=4.5,   # wiki: GAS_WIKI §8.6 — > 2.0 %
        nox=80,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.CAM_TIMING_RETARDED_MAF, (
        f"WVT rule should emit CAM_TIMING_RETARDED_MAF, got {chem}"
    )
    assert validity == SampleValidity.VALID


# ---------------------------------------------------------------------------
# 7. test_cam_timing_priority_above_collision
# ---------------------------------------------------------------------------


def test_cam_timing_priority_above_collision(ontology: dict) -> None:
    """Cam-timing rule (priority 82) wins over collision rule (priority 80).

    A reading that satisfies BOTH the cam-timing signature
    AND the collision rule (co > 0.45, o2 > 2.0) must classify to
    CAM_TIMING_RETARDED_MAF, not RICH_MISFIRE or EXHAUST_AIR_LEAK.
    """
    reading = _reading(
        hc=1200,  # wiki: GAS_WIKI §8.6 — > 1000 ppm
        co=0.6,   # above collision co_tier_max (0.45)
        co2=10.0,
        o2=4.5,   # above both WVT (2.0) and collision (2.0) thresholds
        nox=80,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.CAM_TIMING_RETARDED_MAF, (
        f"WVT priority 82 should beat collision priority 80, got {chem}"
    )
    assert validity == SampleValidity.VALID


# ---------------------------------------------------------------------------
# 8. test_collision_still_fires_when_hc_low
# ---------------------------------------------------------------------------


def test_collision_still_fires_when_hc_low(ontology: dict) -> None:
    """Collision rule still fires when HC is below the WVT threshold.

    Regression guard: a reading with co > 0.45 AND o2 > 2.0 but
    hc < 1000 must still classify via the collision rule (RICH_MISFIRE
    or EXHAUST_AIR_LEAK).  WVT rule must not eat collision's domain
    when HC is low.
    """
    reading = _reading(
        hc=300,   # below WVT hc_threshold (1000)
        co=2.0,   # above collision co_tier_max (0.45)
        co2=10.0,
        o2=4.0,   # above collision o2_threshold (2.0), below WVT (5.0)
        nox=80,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    # Triangle sum = 2.0 + 10.0 + 4.0 = 16.0 <= 16 → RICH_MISFIRE
    assert chem == ChemicalSignature.RICH_MISFIRE, (
        f"collision should still fire when hc < 1000, got {chem}"
    )
    assert validity == SampleValidity.EXTERNAL_O2_SUSPECT


def test_specificity_prefers_narrowest_match(ontology: dict) -> None:
    """When multiple faults match, the narrowest (most specific) wins.

    A reading on the edge of NORMAL_OPERATION also matches wider catch-all
    signatures (FLAT_CAMSHAFT, WORN_PISTON_RINGS). Specificity tie-breaking
    picks NORMAL_OPERATION because its bounds are the tightest.
    """
    reading = _reading(
        hc=15, co=0.2, co2=15.0, o2=0.2, nox=50,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.NORMAL_OPERATION, (
        f"specificity should prefer NORMAL_OPERATION (narrowest), got {chem}"
    )
    assert validity == SampleValidity.VALID


def test_worn_valve_seals_idle_hc_drops_at_2500(ontology: dict) -> None:
    """Idle HC elevation in the valve-seal RPM matrix emits WORN_VALVE_SEALS."""
    reading = _reading(
        hc=150,  # wiki: GAS_WIKI §7.21 — idle row 75-250 ppm
        co=0.2,  # wiki: GAS_WIKI §7.21 — low
        co2=14.0,  # wiki: GAS_WIKI §7.21 — low-moderate
        o2=0.2,  # wiki: GAS_WIKI §7.21 — low
        nox=50,  # wiki: GAS_WIKI §7.21 — low
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.WORN_VALVE_SEALS
    assert validity == SampleValidity.VALID


def test_worn_piston_rings_load_hc_co_high(ontology: dict) -> None:
    """High-idle HC + CO load signature emits WORN_PISTON_RINGS."""
    reading = _reading(
        hc=300,  # wiki: GAS_WIKI §7.23.1 — 2500 RPM row > 250 ppm
        co=0.9,  # wiki: GAS_WIKI §7.23.1 — 2500 RPM row > 0.8 %
        co2=14.0,  # wiki: GAS_WIKI §7.22 — drops under load
        o2=1.0,  # wiki: GAS_WIKI §7.22 — normal
        nox=50,  # wiki: GAS_WIKI §7.22 — low
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.REGULATORY_HIGH_IDLE, ontology)
    assert chem == ChemicalSignature.WORN_PISTON_RINGS
    assert validity == SampleValidity.VALID


def test_worn_engine_generalised_wear(ontology: dict) -> None:
    """Moderate HC + slight CO at lambda near 1 emits WORN_ENGINE."""
    reading = _reading(
        hc=150,  # wiki: GAS_WIKI §7.16 — slight-moderate increase
        co=0.6,  # wiki: GAS_WIKI §7.16 — slight increase
        co2=14.0,  # wiki: GAS_WIKI §7.16 — slight decrease
        o2=0.25,  # wiki: GAS_WIKI §7.16 — slight decrease
        nox=75,  # wiki: GAS_WIKI §7.16 — no change / slight decrease
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.WORN_ENGINE
    assert validity == SampleValidity.VALID


# ---------------------------------------------------------------------------
# T-GV2-7 — Mechanical Wear Leaf Routing
# ---------------------------------------------------------------------------


def test_poa_routes_to_worn_valve_seals_on_sharp_hc_dropoff(ontology: dict) -> None:
    """Idle HC at 500 and high-idle HC <= 35 routes to WORN_VALVE_SEALS."""
    reading = _reading(
        hc=500, co=0.9, co2=13.0, o2=0.2, nox=50,
    )
    reading_high = _reading(
        hc=30, co=0.15, co2=15.2, o2=0.1, nox=50,
    )
    dna = _dna()
    chem, validity = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high
    )
    assert chem == ChemicalSignature.WORN_VALVE_SEALS
    assert validity == SampleValidity.VALID


def test_poa_routes_to_worn_piston_rings_on_rising_hc_loaded_co(ontology: dict) -> None:
    """Idle HC at 120 and high-idle HC > 300 with high CO routes to WORN_PISTON_RINGS."""
    reading = _reading(
        hc=120, co=0.15, co2=14.0, o2=0.2, nox=50,
    )
    reading_high = _reading(
        hc=350, co=0.8, co2=13.0, o2=0.6, nox=50,
    )
    dna = _dna()
    chem, validity = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high
    )
    assert chem == ChemicalSignature.WORN_PISTON_RINGS
    assert validity == SampleValidity.VALID


def test_worn_valve_seals_trim_in_stable_band(ontology: dict) -> None:
    """Valve-seal HC/CO vector + reading_high + fuel_trim = 2.0 -> WORN_VALVE_SEALS."""
    reading = _reading(
        hc=500, co=0.9, co2=13.0, o2=0.2, nox=50,
    )
    reading_high = _reading(
        hc=30, co=0.15, co2=15.2, o2=0.1, nox=50,
    )
    dna = _dna()
    chem, validity = classify(
        reading,
        dna,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        reading_high=reading_high,
        fuel_trim=2.0,
    )
    assert chem == ChemicalSignature.WORN_VALVE_SEALS
    assert validity == SampleValidity.VALID


def test_worn_piston_rings_trim_negative_load_cut(ontology: dict) -> None:
    """Ring HC/CO vector + fuel_trim = -15.0 -> WORN_PISTON_RINGS."""
    reading = _reading(
        hc=120, co=0.15, co2=14.0, o2=0.2, nox=50,
    )
    reading_high = _reading(
        hc=350, co=0.8, co2=13.0, o2=0.6, nox=50,
    )
    dna = _dna()
    chem, validity = classify(
        reading,
        dna,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        reading_high=reading_high,
        fuel_trim=-15.0,
    )
    assert chem == ChemicalSignature.WORN_PISTON_RINGS
    assert validity == SampleValidity.VALID


def test_valve_seal_hc_but_negative_trim_falls_through(ontology: dict) -> None:
    """Valve-seal HC/CO but negative trim (-15.0) -> not WORN_VALVE_SEALS (falls through)."""
    reading = _reading(
        hc=500, co=0.9, co2=13.0, o2=0.2, nox=50,
    )
    reading_high = _reading(
        hc=30, co=0.15, co2=15.2, o2=0.1, nox=50,
    )
    dna = _dna()
    chem, validity = classify(
        reading,
        dna,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        reading_high=reading_high,
        fuel_trim=-15.0,
    )
    assert chem != ChemicalSignature.WORN_VALVE_SEALS
    assert validity == SampleValidity.VALID


def test_worn_routing_unchanged_when_fuel_trim_none(ontology: dict) -> None:
    """Both vectors with fuel_trim = None reproduce the exact outputs."""
    reading_valve = _reading(
        hc=500, co=0.9, co2=13.0, o2=0.2, nox=50,
    )
    reading_high_valve = _reading(
        hc=30, co=0.15, co2=15.2, o2=0.1, nox=50,
    )
    dna = _dna()
    chem_valve, _ = classify(
        reading_valve,
        dna,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        reading_high=reading_high_valve,
        fuel_trim=None,
    )
    assert chem_valve == ChemicalSignature.WORN_VALVE_SEALS

    reading_rings = _reading(
        hc=120, co=0.15, co2=14.0, o2=0.2, nox=50,
    )
    reading_high_rings = _reading(
        hc=350, co=0.8, co2=13.0, o2=0.6, nox=50,
    )
    chem_rings, _ = classify(
        reading_rings,
        dna,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        reading_high=reading_high_rings,
        fuel_trim=None,
    )
    assert chem_rings == ChemicalSignature.WORN_PISTON_RINGS


def test_poa_routes_to_worn_engine_on_flat_hc_no_cleanup(ontology: dict) -> None:
    """Idle HC at 200 and high-idle HC at 220 routes to WORN_ENGINE."""
    reading = _reading(
        hc=200, co=0.2, co2=14.0, o2=0.2, nox=50,
    )
    reading_high = _reading(
        hc=220, co=0.2, co2=13.0, o2=0.7, nox=50,
    )
    dna = _dna()
    chem, validity = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high
    )
    assert chem == ChemicalSignature.WORN_ENGINE
    assert validity == SampleValidity.VALID


def test_poa_stays_on_severe_persistent_hc_lambda_mismatch(ontology: dict) -> None:
    """Idle HC at 600 and high-idle HC at 650 with lambda mismatch stays on POA_SIGNATURE."""
    reading = _reading(
        hc=600, co=3.0, co2=10.0, o2=1.0, nox=50,
    )
    reading_high = _reading(
        hc=650, co=2.5, co2=10.0, o2=1.2, nox=50,
    )
    dna = _dna()
    chem, validity = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high
    )
    assert chem == ChemicalSignature.POA_SIGNATURE
    assert validity == SampleValidity.VALID


def test_mechanical_single_candidate_unchanged(ontology: dict) -> None:
    """With no reading_high, candidate behavior is unchanged."""
    reading = _reading(
        hc=150, co=0.6, co2=14.0, o2=0.25, nox=75,
    )
    dna = _dna()
    chem, validity = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=None
    )
    assert chem == ChemicalSignature.WORN_ENGINE
    assert validity == SampleValidity.VALID


def test_turbo_seal_submode_gated_on_forced(ontology: dict) -> None:
    """Extreme HC with stoichiometric lambda and near-zero CO routes to POA_SIGNATURE only when forced-induction."""
    # Idle: HC 720, CO 0.07, lambda=0.998 (stoich: co2=13.5, o2=1.8) -> POA_SIGNATURE
    # High: HC 130, CO 0.07, lambda=1.003 (stoich: co2=14.5, o2=0.4)
    reading = _reading(hc=720, co=0.07, co2=13.5, o2=1.8, nox=50)
    reading_high = _reading(hc=130, co=0.07, co2=14.5, o2=0.4, nox=50)

    # 1. Gated on forced-induction -> routes to POA_SIGNATURE (turbo-seal sub-mode)
    dna_forced = _dna(induction_type="forced")
    chem, validity = classify(
        reading, dna_forced, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high
    )
    assert chem == ChemicalSignature.POA_SIGNATURE
    assert validity == SampleValidity.VALID

    # 2. Naturally aspirated -> does NOT route to POA_SIGNATURE (not turbo-seal, and not severe/catastrophic either because HC drops)
    dna_na = _dna(induction_type="NA")
    chem_na, validity_na = classify(
        reading, dna_na, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high
    )
    assert chem_na != ChemicalSignature.POA_SIGNATURE
    assert validity_na == SampleValidity.VALID


# ---------------------------------------------------------------------------
# T-P6-5 — engine_state forwarding
# ---------------------------------------------------------------------------


def test_classify_passes_engine_state_to_apply_differentiators(
    ontology: dict, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``classify`` forwards ``engine_state`` to ``apply_differentiators``.

    Monkeypatches ``gaslab.rule_engine.apply_differentiators`` to capture
    the ``engine_state`` kwarg, then asserts ``classify`` passes the same
    ``EngineStateBucket`` value it received.
    """
    captured: dict[str, object] = {}

    import gaslab.rule_engine as _re

    def _fake_apply(
        candidates: list[str],
        reading: GasReading,
        dna: GasLabDnaView,
        ontology: dict,
        engine_state: EngineStateBucket | None = None,
        **kwargs: object,
    ) -> list[str]:
        captured["engine_state"] = engine_state
        return candidates

    monkeypatch.setattr(_re, "apply_differentiators", _fake_apply)

    classify(
        _reading(),
        _dna(),
        EngineStateBucket.STRESS_IDLE,
        ontology,
    )

    assert captured.get("engine_state") == EngineStateBucket.STRESS_IDLE, (
        f"expected classify to forward STRESS_IDLE, got {captured.get('engine_state')!r}"
    )


# ---------------------------------------------------------------------------
# T-P8-2 — coolant intrusion rule (priority 87)
# ---------------------------------------------------------------------------


def test_coolant_intrusion_rule_fires_with_positive_block_test(ontology: dict) -> None:
    """Priority 87 fires when co2 ≤ 12.0, hc ≥ 300, and block_test_passed=True."""
    reading = _reading(hc=450, co=0.15, co2=11.2, o2=2.7, nox=5)  # wiki: GAS_WIKI §8.7
    dna = _dna()
    chem, validity = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology,
        block_test_passed=True,
    )
    assert chem == ChemicalSignature.COOLANT_LEAK_INTERNAL, (
        f"expected COOLANT_LEAK_INTERNAL, got {chem}"
    )
    assert validity == SampleValidity.VALID


def test_coolant_intrusion_rule_bypassed_without_block_test(ontology: dict) -> None:
    """Priority 87 is skipped when block_test_passed=False — falls through to bound matching."""
    reading = _reading(hc=450, co=0.15, co2=11.2, o2=2.7, nox=5)  # wiki: GAS_WIKI §8.7
    dna = _dna()
    chem, _ = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology,
        block_test_passed=False,
    )
    assert chem != ChemicalSignature.COOLANT_LEAK_INTERNAL, (
        "COOLANT_LEAK_INTERNAL must not fire when block_test is negative"
    )


def test_coolant_intrusion_rule_boundary(ontology: dict) -> None:
    """Priority 87 fires at boundary: co2=12.0, hc=300, block_test_passed=True."""
    reading = _reading(hc=300, co=0.10, co2=12.0, o2=2.0, nox=10)  # wiki: GAS_WIKI §8.7
    dna = _dna()
    chem, _ = classify(
        reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology,
        block_test_passed=True,
    )
    assert chem == ChemicalSignature.COOLANT_LEAK_INTERNAL, (
        f"expected COOLANT_LEAK_INTERNAL at boundary, got {chem}"
    )


# ---------------------------------------------------------------------------
# T-GV2-3 — per-vehicle CoC target consumer tests (reconciled)
# ---------------------------------------------------------------------------


def test_normal_lambda_window_centres_on_v112(ontology: dict) -> None:
    """With target_lambda_v112 = 1.000, NORMAL matches lambda in [0.995, 1.005] and rejects 0.989/1.011.
    With v112 = None, the generic window is unchanged.
    """
    sig = {"lambda": {"min": 0.995, "max": 1.005}}
    
    # 1. target_lambda_v112 = 1.000 -> [0.995, 1.005]
    dna_1 = _dna(target_lambda_v112=1.000)
    adjusted_1 = _coc_adjust_normal_bounds(sig, dna_1)
    assert adjusted_1["lambda"]["min"] == pytest.approx(0.995)
    assert adjusted_1["lambda"]["max"] == pytest.approx(1.005)

    # Test match logic using candidates
    # Nominal reading (lambda is ~1.000) matches NORMAL_OPERATION
    reading_nominal = _reading(hc=15, co=0.2, co2=15.0, o2=0.2, nox=50)
    candidates_nominal = _matching_fault_candidates(
        reading_nominal, EngineStateBucket.STABILIZED_IDLE, ontology, dna_1,
    )
    assert "NORMAL_OPERATION" in candidates_nominal

    # Rich reading (lambda ~ 0.989) is outside [0.995, 1.005] and rejects NORMAL
    reading_rich = _reading(hc=15, co=0.45, co2=15.0, o2=0.01, nox=50)
    candidates_rich = _matching_fault_candidates(
        reading_rich, EngineStateBucket.STABILIZED_IDLE, ontology, dna_1,
    )
    assert "NORMAL_OPERATION" not in candidates_rich

    # Lean reading (lambda ~ 1.011) is outside [0.995, 1.005] and rejects NORMAL
    reading_lean = _reading(hc=15, co=0.10, co2=14.5, o2=0.45, nox=50)
    candidates_lean = _matching_fault_candidates(
        reading_lean, EngineStateBucket.STABILIZED_IDLE, ontology, dna_1,
    )
    assert "NORMAL_OPERATION" not in candidates_lean

    # 2. With v112 = None, the generic window is unchanged
    dna_none = _dna(target_lambda_v112=None)
    adjusted_none = _coc_adjust_normal_bounds(sig, dna_none)
    assert adjusted_none["lambda"] == sig["lambda"]


def test_co_low_idle_ceiling_unchanged() -> None:
    """Existing per-vehicle CO behavior preserved (regression guard)."""
    sig = {"co": {"min": 0.1, "max": 0.45}}
    dna = _dna(co_low_idle=0.30)
    adjusted = _coc_adjust_normal_bounds(sig, dna)
    assert adjusted["co"]["max"] == 0.30
    assert adjusted["co"]["min"] == 0.1  # unchanged


def test_coc_adjust_uses_euro_default_when_targets_none() -> None:
    """When CoC targets are None, Euro scaling still sets the CO ceiling."""
    sig = {"co": {"min": 0.1, "max": 0.45}, "lambda": {"min": 0.995, "max": 1.005}}
    dna = _dna(target_lambda_v112=None, co_low_idle=None)
    adjusted = _coc_adjust_normal_bounds(sig, dna)
    assert adjusted["co"]["max"] == 0.2
    assert adjusted["lambda"] == sig["lambda"]


def test_coc_tighter_lambda_shrinks_normal_window(ontology: dict) -> None:
    """A nominal reading is normal for generic bounds but outside when shifted.

    When target_lambda_v112=0.980, the NORMAL_OPERATION window becomes λ=0.975–0.985.
    A nominal reading (measured λ near 1.00) falls outside and must NOT match NORMAL_OPERATION.
    """
    reading = _reading(hc=15, co=0.2, co2=15.0, o2=0.2, nox=50)
    dna = _dna(target_lambda_v112=0.980)
    candidates = _matching_fault_candidates(
        reading, EngineStateBucket.STABILIZED_IDLE, ontology, dna,
    )
    assert "NORMAL_OPERATION" not in candidates, (
        f"CoC-shifted λ window [0.975,0.985] should reject measured λ near 1.00, got {candidates}"
    )


def test_coc_co_target_blocks_borderline_normal(ontology: dict) -> None:
    """CO=0.40 is normal at generic CO max 0.45 but outside CoC limit 0.30."""
    reading = _reading(hc=15, co=0.40, co2=15.0, o2=0.2, nox=50)
    dna = _dna(co_low_idle=0.30)
    candidates = _matching_fault_candidates(
        reading, EngineStateBucket.STABILIZED_IDLE, ontology, dna,
    )
    assert "NORMAL_OPERATION" not in candidates, (
        f"CoC CO limit 0.30 should reject CO=0.40, got {candidates}"
    )


def test_coc_classify_changes_verdict_with_tighter_target(ontology: dict) -> None:
    """Full classify() returns non-NORMAL_OPERATION when CoC target tightens bounds."""
    reading = _reading(hc=15, co=0.40, co2=15.0, o2=0.2, nox=50)
    # Euro-2 DNA: CO ≤ 0.50 → NORMAL_OPERATION
    dna_generic = _dna(euro_emission_category="Euro 2", co_low_idle=None)
    chem_generic, _ = classify(reading, dna_generic, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem_generic == ChemicalSignature.NORMAL_OPERATION
    # CoC DNA: CO ≤ 0.30 → NORMAL_OPERATION; CO=0.40 falls outside
    dna_coc = _dna(co_low_idle=0.30)
    chem_coc, _ = classify(reading, dna_coc, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem_coc != ChemicalSignature.NORMAL_OPERATION, (
        f"CoC-tightened CO max should change verdict from NORMAL_OPERATION, got {chem_coc}"
    )


def test_coc_graceful_degradation_when_fields_absent(ontology: dict) -> None:
    """When CoC fields are None, classify falls back to generic thresholds."""
    reading = _reading()
    dna = _dna(target_lambda_v112=None, co_low_idle=None, co_high_idle=None)
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.NORMAL_OPERATION
    assert validity == SampleValidity.VALID


def test_coc_shifted_lambda_admits_otherwise_rejected_lambda(ontology: dict) -> None:
    """A reading at λ=0.990 is rejected by generic bounds but admitted when target_lambda_v112=0.990."""
    reading = _reading(hc=15, co=0.40, co2=15.0, o2=0.05, nox=50)
    # Generic DNA: λ outside [0.995, 1.005] should NOT match NORMAL
    dna_generic = _dna(target_lambda_v112=None)
    candidates_gen = _matching_fault_candidates(
        reading, EngineStateBucket.STABILIZED_IDLE, ontology, dna_generic,
    )
    assert "NORMAL_OPERATION" not in candidates_gen, (
        "generic ±0.005 window should reject λ≈0.990"
    )

    # With shifted CoC target: λ=0.990 is admitted
    dna_shifted = _dna(euro_emission_category="Euro 2", target_lambda_v112=0.990)
    candidates_shifted = _matching_fault_candidates(
        reading, EngineStateBucket.STABILIZED_IDLE, ontology, dna_shifted,
    )
    assert "NORMAL_OPERATION" in candidates_shifted, (
        f"CoC target 0.990 should admit λ≈0.990, got {candidates_shifted}"
    )


def test_euro2_loosens_co_ceiling(ontology: dict) -> None:
    """Euro-2 admits a CO reading that the Euro-4 default rejects."""
    reading = _reading(hc=15, co=0.40, co2=15.0, o2=0.2, nox=50)

    candidates_euro4 = _matching_fault_candidates(
        reading,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        _dna(euro_emission_category="Euro 4", co_low_idle=None),
    )
    assert "NORMAL_OPERATION" not in candidates_euro4

    candidates_euro2 = _matching_fault_candidates(
        reading,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        _dna(euro_emission_category="Euro 2", co_low_idle=None),
    )
    assert "NORMAL_OPERATION" in candidates_euro2


def test_euro_default_is_euro4_when_absent(ontology: dict) -> None:
    """Unknown or absent Euro category falls back to the Euro-4 CO ceiling."""
    reading = _reading(hc=15, co=0.30, co2=15.0, o2=0.2, nox=50)

    candidates = _matching_fault_candidates(
        reading,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        _dna(euro_emission_category="", co_low_idle=None),
    )

    assert "NORMAL_OPERATION" not in candidates


def test_per_vehicle_coc_overrides_euro_default(ontology: dict) -> None:
    """HIGH-confidence per-vehicle CoC CO limit wins over Euro defaults."""
    reading = _reading(hc=15, co=0.40, co2=15.0, o2=0.2, nox=50)

    candidates = _matching_fault_candidates(
        reading,
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
        _dna(
            euro_emission_category="Euro 2",
            co_low_idle=0.30,
            confidence="HIGH",
        ),
    )

    assert "NORMAL_OPERATION" not in candidates


def test_euro4_tightens_hc_ceiling_2500(ontology: dict) -> None:
    """Euro-4 rejects a 2500-RPM CAM_MAP HC value that Euro-2 admits."""
    reading_high = _reading(hc=800, co=0.8, co2=12.5, o2=0.2, nox=200)

    euro4_result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"],
        _cam_map_idle_rich(),
        _dna(euro_emission_category="Euro 4"),
        ontology,
        reading_high=reading_high,
    )
    assert euro4_result == []

    euro2_result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"],
        _cam_map_idle_rich(),
        _dna(euro_emission_category="Euro 2"),
        ontology,
        reading_high=reading_high,
    )
    assert euro2_result == ["CAM_TIMING_RETARDED_MAP"]


def test_coc_lambda_clamped_to_sane_floor_ceiling() -> None:
    """CoC lambda edges are clamped to floor 0.85 / ceiling 1.15."""
    sig = {"lambda": {"min": 0.995, "max": 1.005}}
    
    # Extreme low v112 (0.80) -> lo gets clamped to floor 0.85, hi is 0.805
    dna_low = _dna(target_lambda_v112=0.80)
    adjusted_low = _coc_adjust_normal_bounds(sig, dna_low)
    assert adjusted_low["lambda"]["min"] == 0.85  # clamped
    assert adjusted_low["lambda"]["max"] == pytest.approx(0.805)

    # Extreme high v112 (1.20) -> lo is 1.195, hi gets clamped to ceiling 1.15
    dna_high = _dna(target_lambda_v112=1.20)
    adjusted_high = _coc_adjust_normal_bounds(sig, dna_high)
    assert adjusted_high["lambda"]["min"] == pytest.approx(1.195)
    assert adjusted_high["lambda"]["max"] == 1.15  # clamped


def test_cam_timing_retarded_maf_persists_at_2500(ontology: dict) -> None:
    """CAM_TIMING_RETARDED_MAF matches when the 2500-RPM reading persists, and rejects otherwise."""
    reading = _reading(hc=1200, co=0.3, co2=9.5, o2=4.2, nox=80) # lambda is around 1.08
    dna = _dna()
    
    # 1. Without reading_high, it should match CAM_TIMING_RETARDED_MAF
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.CAM_TIMING_RETARDED_MAF
    
    # 2. With matching reading_high, it should persist to CAM_TIMING_RETARDED_MAF
    # high idle vector: O2 1.0-2.5%, lambda 1.03-1.09, HC 150-400, CO 0.10-0.30%, NOx 150-500
    reading_high = _reading(hc=250, co=0.2, co2=12.7, o2=1.2, nox=300)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high)
    assert chem == ChemicalSignature.CAM_TIMING_RETARDED_MAF
    
    # 3. With mismatching reading_high, it should not match CAM_TIMING_RETARDED_MAF (falls through)
    reading_high_mismatch = _reading(hc=50, co=0.1, co2=14.5, o2=0.2, nox=10)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high_mismatch)
    assert chem != ChemicalSignature.CAM_TIMING_RETARDED_MAF


def test_cam_timing_advanced_nox_rises(ontology: dict) -> None:
    """CAM_TIMING_ADVANCED matches when the 2500-RPM reading shows high NOx (300-900), and rejects otherwise."""
    reading = _reading(hc=400, co=0.5, co2=12.0, o2=2.0, nox=20) # lambda is around 1.06
    dna = _dna()
    
    # 1. Without reading_high, it should match CAM_TIMING_ADVANCED
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.CAM_TIMING_ADVANCED
    
    # 2. With matching reading_high, it should match CAM_TIMING_ADVANCED
    # high idle vector: O2 0.80-1.80%, lambda 1.01-1.05, HC 100-300, CO 0.15-0.50%, NOx 300-900
    reading_high = _reading(hc=200, co=0.3, co2=13.0, o2=1.2, nox=500)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high)
    assert chem == ChemicalSignature.CAM_TIMING_ADVANCED
    
    # 3. With mismatching reading_high (low NOx), it should not match CAM_TIMING_ADVANCED (falls through)
    reading_high_mismatch = _reading(hc=200, co=0.3, co2=13.0, o2=1.2, nox=20)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high_mismatch)
    assert chem != ChemicalSignature.CAM_TIMING_ADVANCED


def test_cam_timing_retarded_map_partially_normalises(ontology: dict) -> None:
    """CAM_TIMING_RETARDED_MAP matches when the 2500-RPM reading partially normalises, and rejects otherwise."""
    reading = _reading(hc=800, co=4.0, co2=11.0, o2=0.2, nox=5) # lambda is around 0.78
    dna = _dna(euro_emission_category="Euro 2")
    
    # 1. Without reading_high, it should NOT match CAM_TIMING_RETARDED_MAP definitively (goes to bound matching)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem != ChemicalSignature.CAM_TIMING_RETARDED_MAP
    
    # 2. With matching reading_high, it should match CAM_TIMING_RETARDED_MAP
    # high idle vector: O2 < 0.5%, lambda 0.85-0.95, HC 200-600, CO 1.5-4.5%, NOx 100-400
    reading_high = _reading(hc=400, co=3.0, co2=12.0, o2=0.2, nox=200)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high)
    assert chem == ChemicalSignature.CAM_TIMING_RETARDED_MAP
    
    # 3. With mismatching reading_high, it should not match CAM_TIMING_RETARDED_MAP
    reading_high_mismatch = _reading(hc=50, co=0.1, co2=14.5, o2=0.2, nox=10)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high_mismatch)
    assert chem != ChemicalSignature.CAM_TIMING_RETARDED_MAP


def test_lean_mixture_vacuum_leak_normalises(ontology: dict) -> None:
    """LEAN_MIXTURE matches when the 2500-RPM reading normalises, and is rejected otherwise."""
    # idle: lean (O2 > 2.5%, lambda > 1.05)
    reading = _reading(hc=100, co=0.05, co2=12.0, o2=3.0, nox=100) # lambda is around 1.15
    dna = _dna()
    
    # 1. Without reading_high, it matches LEAN_MIXTURE
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.LEAN_MIXTURE
    
    # 2. With normalising reading_high, it matches LEAN_MIXTURE
    reading_high = _reading(hc=20, co=0.1, co2=14.5, o2=0.3, nox=50) # lambda is around 1.00
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high)
    assert chem == ChemicalSignature.LEAN_MIXTURE
    
    # 3. With non-normalising reading_high, it rejects LEAN_MIXTURE
    reading_high_mismatch = _reading(hc=100, co=0.05, co2=12.0, o2=3.0, nox=100) # still lean
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high_mismatch)
    assert chem != ChemicalSignature.LEAN_MIXTURE


def test_catalyst_precondition_lambda_out_of_bounds(ontology: dict) -> None:
    """Both catalyst signatures are rejected if lambda at either speed is out of bounds [0.98, 1.02]."""
    # Idle reading that normally matches CATALYST_NOT_LIGHTING_OFF
    reading = _reading(hc=100, co=0.7, co2=14.0, o2=0.6, nox=50)  # lambda is exactly 1.00
    dna = _dna(has_catalyst=True)

    # 1. High idle reading has out-of-bounds lambda (e.g. lean: lambda ~ 1.05)
    reading_high_bad_lambda = _reading(hc=15, co=0.1, co2=14.0, o2=0.8, nox=50)
    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high_bad_lambda)
    assert chem != ChemicalSignature.CATALYST_NOT_LIGHTING_OFF
    assert chem != ChemicalSignature.CATALYST_OVERWHELMED


def test_weak_catalyst_delta_routes_to_not_lighting_off(ontology: dict) -> None:
    """A clear idle-vs-2500 delta (idle matches weak, high matches working) resolves to CATALYST_NOT_LIGHTING_OFF."""
    # Idle matches weak catalyst
    reading = _reading(hc=100, co=0.7, co2=14.0, o2=0.6, nox=50)  # lambda around 1.00
    # High idle matches working catalyst
    reading_high = _reading(hc=15, co=0.1, co2=15.0, o2=0.05, nox=50)  # lambda around 1.00
    dna = _dna(has_catalyst=True)

    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high)
    assert chem == ChemicalSignature.CATALYST_NOT_LIGHTING_OFF


def test_dead_catalyst_raw_both_speeds_routes_to_overwhelmed(ontology: dict) -> None:
    """Raw engine-out readings at both speeds (idle matches dead, high matches dead) resolves to CATALYST_OVERWHELMED."""
    # Idle matches dead catalyst (raw engine-out)
    reading = _reading(hc=300, co=1.2, co2=11.5, o2=1.5, nox=500)  # lambda around 1.0129
    # High idle matches dead catalyst
    reading_high = _reading(hc=300, co=1.2, co2=11.5, o2=1.5, nox=500)  # lambda around 1.0129
    dna = _dna(has_catalyst=True)

    chem, _ = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, reading_high=reading_high)
    assert chem == ChemicalSignature.CATALYST_OVERWHELMED


# ---------------------------------------------------------------------------
# T-GV2-6a — timing family idle→2500 RPM-differential separation.
# These exercise apply_differentiators directly so the delta gates (not the
# rule_engine definitive branches) are the code under test.
# Wiki: wikiNEW/06b (cam family), wikiNEW/05a (ignition), GAS_WIKI §8.9
# (TEST_RPM_SEPARATION_MATRIX).
# ---------------------------------------------------------------------------


def _cam_map_idle_rich() -> GasReading:
    """Wiki-conformant CAM_TIMING_RETARDED_MAP rich-idle vector.

    λ≈0.755 (∈ [0.75, 0.88]), O₂ 0.2 ≤ 0.5.
    Source: wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAP (idle).
    """
    return _reading(hc=800, co=4.5, co2=10.0, o2=0.2, nox=5)


def test_cam_map_partial_normalisation_retained(ontology: dict) -> None:
    """Rich idle that partially normalises toward 2500 keeps CAM_TIMING_RETARDED_MAP.

    λ rises 0.755 → 0.886 (toward 1.0) and CO falls 4.5 → 3.0 as vacuum
    recovers.  Source: wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAP.
    """
    reading_high = _reading(hc=400, co=3.0, co2=12.0, o2=0.2, nox=200)  # lambda around 0.857
    result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"], _cam_map_idle_rich(), _dna(euro_emission_category="Euro 2"), ontology,
        reading_high=reading_high,
    )
    assert result == ["CAM_TIMING_RETARDED_MAP"], (
        f"partial normalisation should retain CAM_MAP, got {result}"
    )


def test_cam_map_flat_rich_rejected(ontology: dict) -> None:
    """A flat rich signature idle→2500 rejects CAM_TIMING_RETARDED_MAP.

    A sensor/fuelling rich-bias stays flat across RPM (no λ recovery, no CO
    fall) — that is not a retarded cam on Speed-Density.
    Source: wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAP discriminator.
    """
    # Same rich vector at both speeds: λ flat, CO flat.
    reading_high = _reading(hc=750, co=4.5, co2=10.0, o2=0.2, nox=5)
    result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"], _cam_map_idle_rich(), _dna(), ontology,
        reading_high=reading_high,
    )
    assert result == [], f"flat rich should reject CAM_MAP, got {result}"


def test_cam_maf_persists_lean_retained(ontology: dict) -> None:
    """Lean idle persisting lean at 2500 keeps CAM_TIMING_RETARDED_MAF.

    The mechanical phasing error persists across the RPM band (λ 1.157 idle →
    1.036 at 2500, still lean-side with O₂ 1.2).
    Source: wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAF.
    """
    reading = _reading(hc=600, co=0.3, co2=10.0, o2=3.5, nox=10)  # lambda around 1.157
    reading_high = _reading(hc=250, co=0.2, co2=12.7, o2=1.2, nox=300)  # lambda around 1.036
    result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAF"], reading, _dna(), ontology,
        reading_high=reading_high,
    )
    assert result == ["CAM_TIMING_RETARDED_MAF"], (
        f"persisting lean should retain CAM_MAF, got {result}"
    )


def test_cam_maf_normalising_rejected(ontology: dict) -> None:
    """A lean idle that normalises at 2500 rejects CAM_TIMING_RETARDED_MAF.

    A vacuum leak's lean normalises against metered air at 2500 (O₂ 0.3,
    λ → 1.0) — vacuum-leak behaviour, not a retarded cam on MAF.
    Source: wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAF discriminator.
    """
    reading = _reading(hc=600, co=0.3, co2=10.0, o2=3.5, nox=10)  # lambda around 1.157
    reading_high = _reading(hc=50, co=0.1, co2=14.5, o2=0.3, nox=50)  # lambda around 1.0
    result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAF"], reading, _dna(), ontology,
        reading_high=reading_high,
    )
    assert result == [], f"normalising lean should reject CAM_MAF, got {result}"


def test_cam_advanced_nox_rise_retained(ontology: dict) -> None:
    """Mild-lean rough idle with NOx rising and HC/CO falling keeps CAM_TIMING_ADVANCED.

    NOx 20 → 500 (rises with peak pressure/temperature), HC 400 → 200 and
    CO 0.5 → 0.3 (dynamic scavenging stabilises combustion).
    Source: wikiNEW/06b §FAULT_CAM_TIMING_ADVANCED.
    """
    reading = _reading(hc=400, co=0.5, co2=11.0, o2=2.0, nox=20)  # lambda around 1.06
    reading_high = _reading(hc=200, co=0.3, co2=13.0, o2=1.2, nox=500)  # lambda around 1.042
    result = apply_differentiators(
        ["CAM_TIMING_ADVANCED"], reading, _dna(), ontology,
        reading_high=reading_high,
    )
    assert result == ["CAM_TIMING_ADVANCED"], (
        f"NOx-rise + HC/CO-fall should retain CAM_ADVANCED, got {result}"
    )


def test_ignition_over_advanced_clean_idle_not_cam(ontology: dict) -> None:
    """Clean idle + NOx-only 2500 spike routes to ignition TIMING_OVER_ADVANCED, not cam.

    The cam family needs a rough idle with an idle λ-offset; a clean idle
    (HC 150, λ 1.03) whose only 2500 anomaly is NOx > 1200 is over-advanced
    *ignition* timing.  Source: wikiNEW/05a §FAULT_TIMING_OVER_ADVANCED.
    """
    reading = _reading(hc=150, co=0.25, co2=13.0, o2=0.9, nox=40)  # lambda around 1.03 — clean idle
    reading_high = _reading(hc=50, co=0.3, co2=13.5, o2=0.5, nox=1500)  # NOx-only spike
    result = apply_differentiators(
        ["CAM_TIMING_ADVANCED"], reading, _dna(), ontology,
        reading_high=reading_high,
    )
    assert "CAM_TIMING_ADVANCED" not in result, (
        f"clean idle must reject the cam family, got {result}"
    )
    assert result == ["TIMING_OVER_ADVANCED"], (
        f"clean idle + NOx-only spike should route to TIMING_OVER_ADVANCED, got {result}"
    )


# ---------------------------------------------------------------------------
# T-GV2-6b - misfire-vs-timing survivor precedence.
# ---------------------------------------------------------------------------


def test_timing_confirmed_prunes_low_hc_misfire(ontology: dict) -> None:
    """RPM-confirmed cam timing prunes a co-surviving low-HC generic misfire.

    The timing candidate has passed the idle->2500 discriminator, while HC
    remains below the ignition-misfire floor. Source: GAS_WIKI §8.9 and
    GAS_VOCABULARY §10.1.
    """
    reading_high = _reading(hc=400, co=3.0, co2=12.0, o2=0.2, nox=200)
    result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP", "IGNITION_MISFIRE"],
        _cam_map_idle_rich(),
        _dna(euro_emission_category="Euro 2"),
        ontology,
        reading_high=reading_high,
    )
    assert result == ["CAM_TIMING_RETARDED_MAP"], (
        f"RPM-confirmed timing should prune low-HC misfire, got {result}"
    )


def test_true_high_hc_misfire_survives_with_timing(ontology: dict) -> None:
    """A true high-HC misfire remains when cam timing is also RPM-confirmed.

    HC at or above the ignition-misfire floor is a real co-fault magnitude, not
    a generic misfire artefact to prune. Source: GAS_WIKI §8.9 and
    GAS_VOCABULARY §10.1.
    """
    reading = _reading(hc=1200, co=0.3, co2=10.0, o2=4.5, nox=10)
    reading_high = _reading(hc=250, co=0.2, co2=12.7, o2=1.2, nox=300)
    result = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAF", "IGNITION_MISFIRE"],
        reading,
        _dna(),
        ontology,
        reading_high=reading_high,
    )
    assert result == ["CAM_TIMING_RETARDED_MAF", "IGNITION_MISFIRE"], (
        f"high-HC misfire should survive alongside confirmed timing, got {result}"
    )


def test_no_timing_no_change(ontology: dict) -> None:
    """Without an RPM-confirmed timing survivor, low-HC misfire candidates are unchanged."""
    result = apply_differentiators(
        ["IGNITION_MISFIRE"],
        _cam_map_idle_rich(),
        _dna(),
        ontology,
        reading_high=_reading(hc=400, co=3.0, co2=12.0, o2=0.2, nox=200),
    )
    assert result == ["IGNITION_MISFIRE"], (
        f"misfire-only candidate set should be unchanged, got {result}"
    )


# ---------------------------------------------------------------------------
# T-GV2-6c - lean-condition vs timing co-survival precedence.
# ---------------------------------------------------------------------------


def test_normalising_lean_keeps_lean_mixture_drops_timing() -> None:
    """Normalising idle->2500 lean keeps LEAN_MIXTURE and prunes CAM_MAF.

    Source: GAS_WIKI §8.9 and wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAF.
    """
    result = _resolve_lean_timing_cosurvival(
        ["CAM_TIMING_RETARDED_MAF", "LEAN_MIXTURE"],
        lean_normalises_at_high_idle=True,
        cam_maf_persists_at_high_idle=False,
    )
    assert result == ["LEAN_MIXTURE"], (
        f"normalising lean should keep LEAN_MIXTURE only, got {result}"
    )


def test_persisting_lean_keeps_timing_drops_lean_mixture() -> None:
    """Persisting lean keeps CAM_MAF and prunes LEAN_MIXTURE.

    Source: GAS_WIKI §8.9 and wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAF.
    """
    result = _resolve_lean_timing_cosurvival(
        ["LEAN_MIXTURE", "CAM_TIMING_RETARDED_MAF"],
        lean_normalises_at_high_idle=False,
        cam_maf_persists_at_high_idle=True,
    )
    assert result == ["CAM_TIMING_RETARDED_MAF"], (
        f"persisting lean should keep CAM_MAF only, got {result}"
    )


def test_lean_family_no_cosurvival_unchanged() -> None:
    """A single lean-family candidate is unchanged by the 6c precedence rule."""
    result = _resolve_lean_timing_cosurvival(
        ["LEAN_MIXTURE"],
        lean_normalises_at_high_idle=False,
        cam_maf_persists_at_high_idle=True,
    )
    assert result == ["LEAN_MIXTURE"], (
        f"single-candidate lean set should be unchanged, got {result}"
    )


# ---------------------------------------------------------------------------
# T-GV2-10 - O2-Sensor-Bias Calibration by sensor type (narrowband vs wideband)
# ---------------------------------------------------------------------------


def test_o2_bias_calibrated_by_sensor_type(ontology: dict) -> None:
    """The same reading classifies as O2_SENSOR_BIASED_* for one sensor type but not another.

    Source: GAS_WIKI §7.14 / §7.15.
    """
    engine_state = EngineStateBucket.STABILIZED_IDLE

    # Reading 1: Fits default/narrowband BIASED_LOW signature but not wideband
    # (co=1.5 is in default [0.5, 3.0] but not wideband [5.0, 8.0])
    reading_low_nb = _reading(hc=50, co=1.5, co2=14.5, o2=0.1, nox=50)  # lambda is around 0.95
    dna_nb = _dna(upstream_o2_type="NARROWBAND")
    candidates_nb = _matching_fault_candidates(reading_low_nb, engine_state, ontology, dna_nb)
    assert "O2_SENSOR_BIASED_LOW" in candidates_nb

    dna_wb = _dna(upstream_o2_type="WIDEBAND_LAMBDA")
    candidates_wb = _matching_fault_candidates(reading_low_nb, engine_state, ontology, dna_wb)
    assert "O2_SENSOR_BIASED_LOW" not in candidates_wb

    # Reading 2: Fits wideband BIASED_LOW signature but not default/narrowband
    # (co=6.5 is in wideband [5.0, 8.0] but not default [0.5, 3.0])
    reading_low_wb = _reading(hc=50, co=6.5, co2=14.5, o2=0.1, nox=50)  # lambda is around 0.845
    candidates_nb_2 = _matching_fault_candidates(reading_low_wb, engine_state, ontology, dna_nb)
    assert "O2_SENSOR_BIASED_LOW" not in candidates_nb_2

    candidates_wb_2 = _matching_fault_candidates(reading_low_wb, engine_state, ontology, dna_wb)
    assert "O2_SENSOR_BIASED_LOW" in candidates_wb_2

    # Reading 3: Fits wideband BIASED_HIGH signature but not default/narrowband
    # (lambda=1.14 is in wideband [1.12, 1.18] and default [1.0, 2.5])
    reading_high_wb = _reading(hc=50, co=0.05, co2=13.0, o2=2.0, nox=50)  # lambda is around 1.14
    candidates_wb_3 = _matching_fault_candidates(reading_high_wb, engine_state, ontology, dna_wb)
    assert "O2_SENSOR_BIASED_HIGH" in candidates_wb_3

    # Reading 4: Fits default/narrowband BIASED_HIGH signature but not wideband
    # (lambda=1.024 is in default [1.0, 2.5] but not wideband [1.12, 1.18])
    reading_high_nb = _reading(hc=50, co=0.05, co2=14.5, o2=0.5, nox=50)  # lambda is around 1.024
    candidates_nb_4 = _matching_fault_candidates(reading_high_nb, engine_state, ontology, dna_nb)
    assert "O2_SENSOR_BIASED_HIGH" in candidates_nb_4

    candidates_wb_4 = _matching_fault_candidates(reading_high_nb, engine_state, ontology, dna_wb)
    assert "O2_SENSOR_BIASED_HIGH" not in candidates_wb_4


def test_o2_bias_default_when_type_absent(ontology: dict) -> None:
    """When type is absent/not wideband, default bounds from ontology are used.

    Source: GAS_WIKI §7.14 / §7.15.
    """
    engine_state = EngineStateBucket.STABILIZED_IDLE
    reading_low = _reading(hc=50, co=1.5, co2=14.5, o2=0.1, nox=50)  # lambda is around 0.95

    # With upstream_o2_type="NARROWBAND"
    dna_nb = _dna(upstream_o2_type="NARROWBAND")
    candidates_nb = _matching_fault_candidates(reading_low, engine_state, ontology, dna_nb)
    assert "O2_SENSOR_BIASED_LOW" in candidates_nb

    # With upstream_o2_type="ZIRCONIA"
    dna_zirconia = _dna(upstream_o2_type="ZIRCONIA")
    candidates_zirc = _matching_fault_candidates(reading_low, engine_state, ontology, dna_zirconia)
    assert "O2_SENSOR_BIASED_LOW" in candidates_zirc


def test_leak_physical_when_fuel_trim_positive(ontology: dict) -> None:
    """Dilution signature (low CO, high O₂, low HC, triangle in 16–18 band) with fuel_trim = 12.0 -> EXHAUST_AIR_LEAK.

    Source: GAS_WIKI §4.4, GAS_VOCABULARY §10.8.
    """
    reading = _reading(
        hc=15,
        co=0.2,
        co2=5.0,
        o2=11.5,
        nox=10,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, fuel_trim=12.0)
    assert chem == ChemicalSignature.EXHAUST_AIR_LEAK
    assert validity == SampleValidity.EXTERNAL_O2_SUSPECT


def test_leak_sampling_error_when_fuel_trim_in_band(ontology: dict) -> None:
    """Same gases with fuel_trim = 2.0 -> SAMPLE_INVALID.

    Source: GAS_WIKI §4.4, GAS_VOCABULARY §10.8.
    """
    reading = _reading(
        hc=15,
        co=0.2,
        co2=5.0,
        o2=11.5,
        nox=10,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, fuel_trim=2.0)
    assert chem == ChemicalSignature.SAMPLE_INVALID
    assert validity == SampleValidity.INVALID


def test_leak_unchanged_when_fuel_trim_none(ontology: dict) -> None:
    """Same gases, fuel_trim = None -> identical to today's output (no-OBD regression guard).

    Source: GAS_WIKI §4.4, GAS_VOCABULARY §10.8.
    """
    reading = _reading(
        hc=15,
        co=0.2,
        co2=5.0,
        o2=11.5,
        nox=10,
    )
    dna = _dna()
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology, fuel_trim=None)
    assert chem == ChemicalSignature.SAMPLE_INVALID
    assert validity == SampleValidity.INVALID


# ---------------------------------------------------------------------------
# T-GV2-15 - Misfire masking rule cylinder count confirmation tests
# ---------------------------------------------------------------------------


def test_misfire_masking_confirmed_with_cylinder_count(ontology: dict) -> None:
    """Masking gases with cylinder_count = 4 -> IGNITION_MISFIRE.

    Source: docs/GASLab/wikiNEW/05_fault_atlas_part_a.md §FAULT_IGNITION_MISFIRE
    """
    reading = _reading(
        hc=1500,  # wiki: GAS_WIKI §8.4 — > 1000 ppm
        co=0.2,
        co2=10.0,
        o2=5.0,   # wiki: GAS_WIKI §8.4 — > 3.0 %
        nox=30,   # wiki: GAS_WIKI §8.4 — < 50 ppm
    )
    dna = _dna(cylinder_count=4)
    chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem == ChemicalSignature.IGNITION_MISFIRE
    assert validity == SampleValidity.VALID


def test_misfire_masking_unchanged_across_cylinder_counts(ontology: dict) -> None:
    """Same gases at cylinder_count in {1, 4, 8, 12} all -> IGNITION_MISFIRE.

    Source: docs/GASLab/wikiNEW/05_fault_atlas_part_a.md §FAULT_IGNITION_MISFIRE
    """
    for cyl in (1, 4, 8, 12):
        # For cyl=1, we need O2 to be higher to confirm the cylinder dropout
        o2_val = 11.0 if cyl == 1 else 5.0
        co2_val = 6.5 if cyl == 1 else 10.0
        reading = _reading(
            hc=1500,  # wiki: GAS_WIKI §8.4
            co=0.2,
            co2=co2_val,
            o2=o2_val,  # wiki: GAS_WIKI §8.4
            nox=30,   # wiki: GAS_WIKI §8.4
        )
        dna = _dna(cylinder_count=cyl)
        chem, validity = classify(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
        assert chem == ChemicalSignature.IGNITION_MISFIRE, f"Failed at cylinder_count={cyl}"
        expected_validity = SampleValidity.EXTERNAL_O2_SUSPECT if cyl == 1 else SampleValidity.VALID
        assert validity == expected_validity, f"Failed validity at cylinder_count={cyl}"


def test_cylinder_count_read_in_masking_path(ontology: dict) -> None:
    """Assert cylinder_count actively participates in masking decision.

    Source: docs/GASLab/wikiNEW/05_fault_atlas_part_a.md §FAULT_IGNITION_MISFIRE
    """
    # At cylinder_count = 2 and o2 = 3.8:
    # inferred_cyl = round(3.8 / (21 / 2)) = round(0.36) = 0 < 1 -> should fail masking
    reading_fail = _reading(
        hc=1500,  # wiki: GAS_WIKI §8.4
        co=0.2,
        co2=10.0,
        o2=3.8,   # wiki: GAS_WIKI §8.4
        nox=30,   # wiki: GAS_WIKI §8.4
    )
    dna_fail = _dna(cylinder_count=2)
    chem_fail, _ = classify(reading_fail, dna_fail, EngineStateBucket.STABILIZED_IDLE, ontology)
    # Since it fails masking, it routes to another class or normal operation (not IGNITION_MISFIRE)
    assert chem_fail != ChemicalSignature.IGNITION_MISFIRE, (
        f"Should not classify as IGNITION_MISFIRE with cyl=2 and o2=3.8, got {chem_fail}"
    )

    # At cylinder_count = 12 and o2 = 3.8:
    # inferred_cyl = round(3.8 / (21 / 12)) = round(2.17) = 2 >= 1 -> should confirm masking
    dna_pass = _dna(cylinder_count=12)
    chem_pass, _ = classify(reading_fail, dna_pass, EngineStateBucket.STABILIZED_IDLE, ontology)
    assert chem_pass == ChemicalSignature.IGNITION_MISFIRE, (
        f"Should classify as IGNITION_MISFIRE with cyl=12 and o2=3.8, got {chem_pass}"
    )


