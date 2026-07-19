"""Tests for ``gaslab/resolution.py`` — entity resolution layer.

Covers the four success criteria from ``T-P3-1_entity_resolution.md`` plus
a parametrised sweep of every detected overlap pair.
"""

from __future__ import annotations

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.resolution import apply_differentiators, find_overlaps, is_resolved


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def ontology() -> dict:
    """Load the ontology once for all tests in this module."""
    return load_ontology()


@pytest.fixture(scope="module")
def overlaps(ontology: dict) -> list[tuple[str, str]]:
    """All detected overlap pairs from the ontology."""
    return find_overlaps(ontology)


# ---------------------------------------------------------------------------
# Shared test DNA / reading builders
# ---------------------------------------------------------------------------


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
        hc=10, co=0.2, co2=15.0, o2=0.2, nox=50,
    )
    defaults.update(overrides)
    return GasReading(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 1. test_overlap_detection_finds_known_pairs
# ---------------------------------------------------------------------------


def test_overlap_detection_finds_known_pairs(overlaps: list[tuple[str, str]]) -> None:
    """``find_overlaps`` returns at least the documented overlap pairs.

    Per ``GAS_WIKI §7.19/§7.20``, VACUUM_REGULATOR_DIAPHRAGM_RUPTURE and
    GDI_HPFP_INTERNAL_SEAL_LEAK share identical tailpipe signatures.

    Per ``GAS_WIKI §7.25``, EGR_STUCK_CLOSED has the same gas pattern as
    HIGH_COMBUSTION_TEMP (§7.8).
    """
    vr_dr = "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE"
    gdi_hpfp = "GDI_HPFP_INTERNAL_SEAL_LEAK"
    hct = "HIGH_COMBUSTION_TEMP"
    egr_closed = "EGR_STUCK_CLOSED"

    pairs_set = set(overlaps)

    # Canonical pair from GAS_WIKI §7.19/§7.20
    assert (vr_dr, gdi_hpfp) in pairs_set or (gdi_hpfp, vr_dr) in pairs_set, (
        f"expected ({vr_dr}, {gdi_hpfp}) in overlaps per GAS_WIKI §7.19/§7.20"
    )

    # GAS_WIKI §7.25 explicitly says same gas pattern as §7.8
    assert (hct, egr_closed) in pairs_set or (egr_closed, hct) in pairs_set, (
        f"expected ({hct}, {egr_closed}) in overlaps per GAS_WIKI §7.25"
    )


# ---------------------------------------------------------------------------
# 2. test_differentiator_resolves_overlap
# ---------------------------------------------------------------------------


def test_differentiator_resolves_overlap_gdi(ontology: dict) -> None:
    """Given GDI DNA, only the GDI variant survives the §7.19/§7.20 overlap."""
    candidates = [
        "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE",
        "GDI_HPFP_INTERNAL_SEAL_LEAK",
    ]
    dna = _dna(fuel_delivery_type="GDI")
    reading = _reading()

    result = apply_differentiators(candidates, reading, dna, ontology)
    assert result == ["GDI_HPFP_INTERNAL_SEAL_LEAK"], (
        f"GDI DNA should leave only GDI_HPFP, got {result}"
    )


def test_differentiator_resolves_overlap_non_gdi(ontology: dict) -> None:
    """Given non-GDI DNA, only the VR diaphragm rupture survives."""
    candidates = [
        "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE",
        "GDI_HPFP_INTERNAL_SEAL_LEAK",
    ]
    dna = _dna(fuel_delivery_type="NON_GDI")
    reading = _reading()

    result = apply_differentiators(candidates, reading, dna, ontology)
    assert result == ["VACUUM_REGULATOR_DIAPHRAGM_RUPTURE"], (
        f"non-GDI DNA should leave only VR_DR, got {result}"
    )


def test_differentiator_resolves_hct_vs_egr(ontology: dict) -> None:
    """Given egr_equipped DNA, EGR_STUCK_CLOSED survives; without it, HCT does."""
    candidates = ["HIGH_COMBUSTION_TEMP", "EGR_STUCK_CLOSED"]
    reading = _reading()

    # With EGR equipped → EGR_STUCK_CLOSED survives (dna_gate + differentiator)
    dna_egr = _dna(egr_equipped=True)
    result_egr = apply_differentiators(candidates, reading, dna_egr, ontology)
    assert "EGR_STUCK_CLOSED" in result_egr, (
        f"EGR equipped should admit EGR_STUCK_CLOSED, got {result_egr}"
    )
    assert "HIGH_COMBUSTION_TEMP" not in result_egr, (
        "HIGH_COMBUSTION_TEMP should be excluded when egr_equipped (differentiator edge)"
    )

    # Without EGR → HIGH_COMBUSTION_TEMP survives (EGR dna_gate rejects)
    dna_no_egr = _dna(egr_equipped=False)
    result_no_egr = apply_differentiators(candidates, reading, dna_no_egr, ontology)
    assert "HIGH_COMBUSTION_TEMP" in result_no_egr, (
        f"non-EGR should admit HIGH_COMBUSTION_TEMP, got {result_no_egr}"
    )
    assert "EGR_STUCK_CLOSED" not in result_no_egr, (
        "EGR_STUCK_CLOSED requires egr_equipped=true per dna_gate"
    )


# ---------------------------------------------------------------------------
# 3. test_no_orphan_after_resolution
# ---------------------------------------------------------------------------


def test_no_orphan_after_resolution(ontology: dict) -> None:
    """Every fault in the ontology is reachable via its key.

    No entry becomes orphaned after differentiator_edges are populated.
    """
    faults = ontology["faults"]
    for name in ChemicalSignature:
        assert name.value in faults, (
            f"{name.value}: missing from ontology faults — orphaned"
        )
    assert len(faults) == 34, f"expected 34 faults, got {len(faults)}"


# ---------------------------------------------------------------------------
# 4. test_all_overlaps_have_differentiators
# ---------------------------------------------------------------------------


def test_all_overlaps_have_differentiators(
    overlaps: list[tuple[str, str]], ontology: dict
) -> None:
    """Every wiki-documented overlap pair has at least one fault with
    ``differentiator_edges`` or ``dna_gate``.

    Only checks the pairs the wiki explicitly names as overlapping (§7.19/§7.20,
    §7.8/§7.25).  Mechanical overlaps caused by catch-all signatures
    (SAMPLE_INVALID full-range, VVT_FAILURE variable, EVAP_CANISTER_SATURATED
    wide bounds) are not required to carry differentiators — those are
    gate-halted states, not competing diagnoses.
    """
    wiki_pairs: set[tuple[str, str]] = {
        ("VACUUM_REGULATOR_DIAPHRAGM_RUPTURE", "GDI_HPFP_INTERNAL_SEAL_LEAK"),
        ("HIGH_COMBUSTION_TEMP", "EGR_STUCK_CLOSED"),
    }
    faults = ontology["faults"]
    undocumented: list[tuple[str, str]] = []

    for name_a, name_b in overlaps:
        pair = (name_a, name_b) if name_a < name_b else (name_b, name_a)
        if pair not in wiki_pairs:
            continue

        entry_a = faults[name_a]
        entry_b = faults[name_b]
        edges_a = entry_a.get("differentiator_edges")
        edges_b = entry_b.get("differentiator_edges")

        a_has = bool(edges_a) or entry_a.get("dna_gate") is not None
        b_has = bool(edges_b) or entry_b.get("dna_gate") is not None

        if not (a_has or b_has):
            undocumented.append(pair)

    assert not undocumented, (
        f"Wiki-documented overlap pairs without differentiators: {undocumented}"
    )


# ---------------------------------------------------------------------------
# Parametrised — every detected overlap is a valid pair
# ---------------------------------------------------------------------------


def test_every_overlap_pair_is_symmetric(
    overlaps: list[tuple[str, str]],
    ontology: dict,
) -> None:
    """Each detected overlap pair has valid fault entries on both sides."""
    faults = ontology["faults"]
    for name_a, name_b in overlaps:
        assert name_a in faults, f"{name_a} not in ontology faults"
        assert name_b in faults, f"{name_b} not in ontology faults"
        assert name_a < name_b, (
            f"overlap pair ({name_a}, {name_b}) not in lexicographic order"
        )


# ---------------------------------------------------------------------------
# is_resolved
# ---------------------------------------------------------------------------


def test_is_resolved_empty() -> None:
    """Zero candidates is resolved (no fault to choose)."""
    assert is_resolved([]) is True


def test_is_resolved_single() -> None:
    """One candidate is resolved."""
    assert is_resolved(["NORMAL_OPERATION"]) is True


def test_is_resolved_multiple() -> None:
    """Two or more candidates is not resolved."""
    assert is_resolved(["RICH_MIXTURE", "LEAN_MIXTURE"]) is False


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_apply_differentiators_unknown_candidate_skipped(ontology: dict) -> None:
    """A candidate not in the ontology is silently skipped."""
    result = apply_differentiators(
        ["NOT_A_REAL_FAULT"], _reading(), _dna(), ontology,
    )
    assert result == []


def test_find_overlaps_no_pair_is_self(overlaps: list[tuple[str, str]]) -> None:
    """No overlap pair is a self-match."""
    for name_a, name_b in overlaps:
        assert name_a != name_b, f"self-match: ({name_a}, {name_b})"


def test_differentiator_physical_check_does_not_filter(ontology: dict) -> None:
    """A physical_check differentiator edge is informational — never filters."""
    # GDI_HPFP has a physical_check edge — it should still survive
    candidates = ["GDI_HPFP_INTERNAL_SEAL_LEAK"]
    dna = _dna(fuel_delivery_type="GDI")
    result = apply_differentiators(candidates, _reading(), dna, ontology)
    assert result == ["GDI_HPFP_INTERNAL_SEAL_LEAK"]


# ---------------------------------------------------------------------------
# T-P6-4 — specificity-pair differentiator edges (closes T-P5-1c)
# ---------------------------------------------------------------------------


def test_specificity_pairs_have_differentiators(ontology: dict) -> None:
    """Each of the three T-P5-1c specificity pairs has non-empty ``differentiator_edges``.

    Per ``GASLAB_AUDIT_2026-05-19.md §4.4`` three pairs share >= 98%
    signature-width specificity: FLAT_CAMSHAFT/O2_SENSOR_BIASED_LOW,
    FLAT_CAMSHAFT/WORN_PISTON_RINGS, O2_SENSOR_BIASED_LOW/WORN_PISTON_RINGS.
    """
    required = ("FLAT_CAMSHAFT", "O2_SENSOR_BIASED_LOW", "WORN_PISTON_RINGS")
    faults = ontology["faults"]
    missing: list[str] = []
    for name in required:
        edges = faults[name].get("differentiator_edges")
        if not edges:
            missing.append(name)
    assert not missing, f"Faults missing differentiator_edges: {missing}"


def test_flat_camshaft_vs_o2_sensor_resolves_deterministic(
    ontology: dict,
) -> None:
    """FLAT_CAMSHAFT vs O2_SENSOR_BIASED_LOW overlap is documented with
    informational edges (physical_check + rpm_differential).

    No DNA-typed edge exists for this pair per GAS_WIKI §7.14/§7.17.
    apply_differentiators preserves both candidates with
    informational-only edges.  T-P6-5 will activate rpm_differential
    when EngineStateBucket plumbing is in place.
    """
    candidates = ["FLAT_CAMSHAFT", "O2_SENSOR_BIASED_LOW"]
    reading = _reading(hc=50, co=0.5, co2=14.5, o2=0.15, nox=50)
    dna = _dna()
    result = apply_differentiators(candidates, reading, dna, ontology)

    # Both survive — informational edges only (no dna-typed edge exists).
    assert set(result) == set(candidates), (
        f"expected both candidates to survive, got {result}"
    )

    # Edge shape: each entry carries 2 informational edges.
    faults = ontology["faults"]
    for name in candidates:
        edges = faults[name].get("differentiator_edges", [])
        edge_types = {e.get("type") for e in edges}
        assert edge_types == {"physical_check", "rpm_differential"}, (
            f"{name}: expected physical_check + rpm_differential, got {edge_types}"
        )


def test_flat_camshaft_vs_worn_piston_rings_resolves_deterministic(
    ontology: dict,
) -> None:
    """FLAT_CAMSHAFT vs WORN_PISTON_RINGS overlap is documented with
    informational edges (physical_check + rpm_differential).

    Both are mechanical faults with ~1.0 lambda.  The cylinder-contribution
    test (physical_check) and RPM behaviour distinguish them in the lab;
    algorithmic resolution via rpm_differential awaits T-P6-5.
    """
    candidates = ["FLAT_CAMSHAFT", "WORN_PISTON_RINGS"]
    reading = _reading(hc=50, co=0.25, co2=15.0, o2=0.25, nox=50)
    dna = _dna()
    result = apply_differentiators(candidates, reading, dna, ontology)

    # Both survive — informational edges only.
    assert set(result) == set(candidates), (
        f"expected both candidates to survive, got {result}"
    )

    faults = ontology["faults"]
    for name in candidates:
        edges = faults[name].get("differentiator_edges", [])
        edge_types = {e.get("type") for e in edges}
        assert edge_types == {"physical_check", "rpm_differential"}, (
            f"{name}: expected physical_check + rpm_differential, got {edge_types}"
        )


def test_o2_sensor_vs_worn_piston_rings_resolves_deterministic(
    ontology: dict,
) -> None:
    """O2_SENSOR_BIASED_LOW vs WORN_PISTON_RINGS overlap is documented with
    informational edges (physical_check + rpm_differential).

    Sensor voltage swing test distinguishes biased-low O2 from ring wear
    in the lab; RPM behaviour provides the algorithmic path (T-P6-5).
    """
    candidates = ["O2_SENSOR_BIASED_LOW", "WORN_PISTON_RINGS"]
    reading = _reading(hc=50, co=0.5, co2=15.0, o2=0.15, nox=50)
    dna = _dna()
    result = apply_differentiators(candidates, reading, dna, ontology)

    # Both survive — informational edges only (rpm_differential edges lack
    # appears_in_states, so they remain informational per T-P6-5).
    assert set(result) == set(candidates), (
        f"expected both candidates to survive, got {result}"
    )

    faults = ontology["faults"]
    for name in candidates:
        edges = faults[name].get("differentiator_edges", [])
        edge_types = {e.get("type") for e in edges}
        assert edge_types == {"physical_check", "rpm_differential"}, (
            f"{name}: expected physical_check + rpm_differential, got {edge_types}"
        )


# ---------------------------------------------------------------------------
# T-P6-5 — rpm_differential edge filtering (closes T-P3-1c)
# ---------------------------------------------------------------------------


def test_rpm_differential_edge_filters_by_engine_state() -> None:
    """A candidate with an ``rpm_differential`` edge demanding ``STRESS_IDLE``
    is filtered out when ``engine_state=STABILIZED_IDLE``.
    """
    ontology = {
        "faults": {
            "TEST_FAULT": {
                "differentiator_edges": [
                    {
                        "type": "rpm_differential",
                        "appears_in_states": ["STRESS_IDLE"],
                        "citation": "GAS_WIKI §7.22",
                    }
                ],
                "signature": {},
            }
        }
    }
    result = apply_differentiators(
        ["TEST_FAULT"],
        _reading(),
        _dna(),
        ontology,
        EngineStateBucket.STABILIZED_IDLE,
    )
    assert result == [], (
        f"STABILIZED_IDLE not in appears_in_states → should filter, got {result}"
    )


def test_rpm_differential_passes_when_state_matches() -> None:
    """A candidate with an ``rpm_differential`` edge survives when
    ``engine_state`` matches the edge's ``appears_in_states`` list.
    """
    ontology = {
        "faults": {
            "TEST_FAULT": {
                "differentiator_edges": [
                    {
                        "type": "rpm_differential",
                        "appears_in_states": ["STRESS_IDLE"],
                        "citation": "GAS_WIKI §7.22",
                    }
                ],
                "signature": {},
            }
        }
    }
    result = apply_differentiators(
        ["TEST_FAULT"],
        _reading(),
        _dna(),
        ontology,
        EngineStateBucket.STRESS_IDLE,
    )
    assert result == ["TEST_FAULT"], (
        f"STRESS_IDLE in appears_in_states → should survive, got {result}"
    )


# ---------------------------------------------------------------------------
# CHI-1 — co_high_idle overrides the rich-CO ceiling (mild_rich.max) in the
# CAM_TIMING_RETARDED_MAP rich branch, gated on HIGH confidence.
# Wiki: GAS_VOCABULARY §11 (per-vehicle override gate, confidence=HIGH) +
#       §10.2 (mild_rich.max default = 1.5 %CO at 2500 RPM).
# ---------------------------------------------------------------------------


def _cam_map_idle() -> GasReading:
    """A rich-idle reading inside the CAM_TIMING_RETARDED_MAP idle window.

    T-GV2-6a added idle-side gates to the CAM_MAP branch (rich idle λ∈[0.75,
    0.88], O₂ ≤ 0.5, partial normalisation toward 2500); this wiki-conformant
    idle vector satisfies every idle gate so the CHI-1 tests below still
    isolate CO as the sole deciding variable.  λ≈0.755, o2=0.2, co=4.5 >
    every ``_cam_map_high`` CO (1.8/2.2) so the CO-falls delta holds.
    Source: wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAP (idle vector).
    """
    return _reading(hc=800, co=4.5, co2=10.0, o2=0.2, nox=5)


def _cam_map_high(co: float) -> GasReading:
    """A 2500-RPM reading inside the CAM_TIMING_RETARDED_MAP window except CO.

    Every non-CO bound is satisfied for co in [1.8, 2.2]: o2=0.2 (≤0.5),
    hc=200 (Euro-4 2500-RPM ceiling), nox=200 (∈[100,400]), λ≈0.905–0.917 (∈[0.85,0.95]),
    both λ_high > λ_idle (≈0.755) and co < idle CO (4.5) per the T-GV2-6a
    partial-normalisation delta.
    CO is the sole deciding variable, so the rich-CO lower bound (mild_rich.max)
    is what these tests exercise.  Source: resolution.py CAM_MAP branch.
    """
    return _reading(hc=200, co=co, co2=12.0, o2=0.2, nox=200)


def test_co_high_idle_overrides_literal_when_high_conf(ontology: dict) -> None:
    """With confidence=HIGH and co_high_idle populated, the per-vehicle ceiling
    replaces the literal 1.5 (mild_rich.max) rich-CO lower bound for
    CAM_TIMING_RETARDED_MAP.

    Per-vehicle ceiling = 2.0 %CO.  reading_high.co just under it (1.8) drops
    CAM_TIMING_RETARDED_MAP — even though 1.8 ≥ the default 1.5 and would pass
    under the literal.  Just over (2.2) keeps it.  This proves the per-vehicle
    value, not the literal, is the active bound.  Wiki: GAS_VOCABULARY §11/§10.2.
    """
    dna = _dna(confidence="HIGH", co_high_idle=2.0)

    # Just under the per-vehicle ceiling → rejected (would have passed under 1.5).
    result_under = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"], _cam_map_idle(), dna, ontology,
        reading_high=_cam_map_high(co=1.8),
    )
    assert result_under == [], (
        f"co=1.8 < per-vehicle ceiling 2.0 → CAM_MAP should drop, got {result_under}"
    )

    # Just over the per-vehicle ceiling → kept.
    result_over = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"], _cam_map_idle(), dna, ontology,
        reading_high=_cam_map_high(co=2.2),
    )
    assert result_over == ["CAM_TIMING_RETARDED_MAP"], (
        f"co=2.2 ≥ per-vehicle ceiling 2.0 → CAM_MAP should survive, got {result_over}"
    )


def test_co_high_idle_falls_back_to_euro_default(ontology: dict) -> None:
    """With co_high_idle absent or not HIGH-confidence, the Euro default is used.
    co=1.8 is above the Euro-4 default and keeps CAM_TIMING_RETARDED_MAP; this
    is the regression guard against the override leaking into the default path.
    Wiki: GAS_VOCABULARY §11 (override gate), wikiNEW §2.8 (Euro default).
    """
    # Case A: co_high_idle absent -> Euro default.
    dna_none = _dna(confidence="HIGH", co_high_idle=None)
    result_none = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"], _cam_map_idle(), dna_none, ontology,
        reading_high=_cam_map_high(co=1.8),
    )
    assert result_none == ["CAM_TIMING_RETARDED_MAP"], (
        f"co_high_idle None -> Euro default active, co=1.8 survives, got {result_none}"
    )

    # Case B: co_high_idle populated but confidence != HIGH -> Euro default.
    dna_low_conf = _dna(confidence="MEDIUM", co_high_idle=2.0)
    result_low_conf = apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"], _cam_map_idle(), dna_low_conf, ontology,
        reading_high=_cam_map_high(co=1.8),
    )
    assert result_low_conf == ["CAM_TIMING_RETARDED_MAP"], (
        f"confidence != HIGH -> Euro default active, co=1.8 survives, got {result_low_conf}"
    )
