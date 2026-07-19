"""Per-signature reachability tests for ``iter_edge_probes()``.

Verifies that each of the four hand-tuned edge probes in
``tests/fixtures/synthetic_grid.py`` classifies to its intended
``ChemicalSignature`` under at least one ``(GasLabDnaView,
EngineStateBucket)`` combination.

Closes: T-P5-1d → T-P6-6.
"""

from __future__ import annotations

import pytest

from gaslab.contracts import EngineStateBucket
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.rule_engine import classify
from tests.fixtures.synthetic_grid import iter_edge_probes


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _dna(**overrides: object) -> GasLabDnaView:
    """Build a minimal valid ``GasLabDnaView`` with optional overrides."""
    defaults: dict[str, object] = dict(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="NON_GDI",
        induction_type="NA",
        upstream_o2_type="WIDEBAND",
        has_catalyst=True,
        egr_equipped=False,
        confidence="HIGH",
    )
    defaults.update(overrides)
    return GasLabDnaView(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Parametrized reachability test
# ---------------------------------------------------------------------------

# Each case: (target_signature, dna_override, note)
# dna_override = None means "try default (PORT) AND gated (GDI+EGR+catalyst)"
_HARD_SIGNATURES: list[tuple[str, dict[str, object] | None]] = [
    ("FLAT_CAMSHAFT", None),                       # wiki: GAS_WIKI §7.17
    ("VACUUM_REGULATOR_DIAPHRAGM_RUPTURE", None),  # wiki: GAS_WIKI §7.19 — needs NON_GDI
    ("WORN_ENGINE", None),                          # wiki: GAS_WIKI §7.16
    ("WORN_VALVE_SEALS", None),                     # wiki: GAS_WIKI §7.21
    ("INCOMPLETE_COMBUSTION", None),                # wiki: GAS_WIKI §7.31 — compression-loss partial combustion
]


@pytest.mark.parametrize("target,dna_override", _HARD_SIGNATURES)
def test_each_hard_signature_appears(
    target: str, dna_override: dict[str, object] | None
) -> None:
    """Every hard-to-reach signature appears at least once via edge probes.

    Runs ``iter_edge_probes()`` through ``classify()`` against two DNA
    views (default PORT and GDI+EGR+catalyst) plus two engine states
    (STABILIZED_IDLE and STRESS_IDLE for rpm_differential branches).
    The target signature must appear in the verdict set for at least
    one combination.
    """
    ontology = load_ontology()
    engine_states = (EngineStateBucket.STABILIZED_IDLE, EngineStateBucket.STRESS_IDLE)

    # Build DNA views to exercise
    dna_views: list[GasLabDnaView]
    if dna_override is not None:
        dna_views = [_dna(**dna_override)]
    else:
        dna_views = [
            _dna(),                                                      # NON_GDI
            _dna(                                                        # GDI + EGR + catalyst
                fuel_delivery_type="GDI",
                egr_equipped=True,
                has_catalyst=True,
            ),
        ]

    seen: set[str] = set()
    for reading in iter_edge_probes():
        for dna in dna_views:
            for engine_state in engine_states:
                chem, _ = classify(reading, dna, engine_state, ontology)
                seen.add(chem.value)

    assert target in seen, (
        f"{target} not reachable by any edge probe. "
        f"Seen signatures: {sorted(seen)}"
    )
