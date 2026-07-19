"""Boundary-permutation grid generator for the 5-gas analyser envelope.

Produces synthetic ``GasReading`` instances spanning the full analyser
measurement envelope at coarse steps.  Used by the T-P5-1 boundary
permutation test to verify that every grid point resolves to a non-null
``chemical_state``.

Source: ``GasLabIteration §5`` boundary-permutation audit.
"""

from __future__ import annotations

from collections.abc import Iterator

from gaslab.contracts import GasReading


def boundary_grid() -> Iterator[GasReading]:
    """Yield ``GasReading`` points spanning the 5-gas analyser envelope.

    Ranges and steps per the T-P5-1 spec:
    - HC  ∈ [0, 2500]  step 250
    - CO  ∈ [0, 5]     step 0.5
    - CO₂ ∈ [5, 16]    step 1
    - O₂  ∈ [0, 8]     step 1
    - NOₓ ∈ [0, 2000]  step 250

    Full Cartesian product: 11 × 11 × 12 × 9 × 9 = 117,612 points.
    """
    for hc in range(0, 2501, 250):  # vocab: GAS_VOCABULARY §2 — HC range
        for co_int in range(0, 11):  # 0.0–5.0 step 0.5
            co = co_int * 0.5  # vocab: GAS_VOCABULARY §2 — CO range
            for co2_int in range(5, 17):  # 5.0–16.0 step 1.0
                co2 = float(co2_int)  # vocab: GAS_VOCABULARY §2 — CO₂ range
                for o2_int in range(0, 9):  # 0.0–8.0 step 1.0
                    o2 = float(o2_int)  # vocab: GAS_VOCABULARY §2 — O₂ range
                    for nox in range(0, 2001, 250):  # vocab: GAS_VOCABULARY §2 — NOₓ range
                        yield GasReading(hc=hc, co=co, co2=co2, o2=o2, nox=nox)


def iter_edge_probes() -> Iterator[GasReading]:
    """Hand-tuned probes for five hard-to-reach ChemicalSignature values.

    Each probe targets a narrow fault-signature corner that the
    boundary-grid step size skips.  Values are tuned to the centre of
    the per-fault box while escaping narrower competitor bounds.

    Sources: ``GAS_WIKI §7.16``, ``§7.17``, ``§7.19``, ``§7.21``, ``§7.31``.
    Closes: T-P5-1d → T-P6-6, T-P8-1.
    """
    # FLAT_CAMSHAFT — wiki: GAS_WIKI §7.17
    # Escapes NORMAL_OPERATION (hc > 35), TIMING_RETARDED (nox > 50),
    # and WORN_PISTON_RINGS (co2 < 14.5).  Lower specificity than
    # WORN_ENGINE (204 vs 369) so FLAT_CAMSHAFT wins tie-break.
    yield GasReading(hc=50, co=0.25, co2=13.75, o2=0.25, nox=75)  # wiki: GAS_WIKI §7.17

    # VACUUM_REGULATOR_DIAPHRAGM_RUPTURE — wiki: GAS_WIKI §7.19
    # Escapes RICH_MIXTURE (hc > 300).  Disambiguated from
    # GDI_HPFP_INTERNAL_SEAL_LEAK by dna_gate (NON_GDI vs GDI).
    yield GasReading(hc=600, co=5.0, co2=9.0, o2=0.15, nox=25)  # wiki: GAS_WIKI §7.19

    # WORN_ENGINE — wiki: GAS_WIKI §7.16
    # Escapes FLAT_CAMSHAFT (hc > 100), WORN_VALVE_SEALS (co2 > 14.5),
    # WORN_PISTON_RINGS (hc > 100), and TIMING_RETARDED (nox > 50).
    # co kept low (0.25) to preserve lambda ≈ 1.0.
    yield GasReading(hc=180, co=0.25, co2=14.8, o2=0.15, nox=65)  # wiki: GAS_WIKI §7.16

    # WORN_VALVE_SEALS — wiki: GAS_WIKI §7.21
    # Escapes FLAT_CAMSHAFT and WORN_PISTON_RINGS (hc > 100),
    # WORN_ENGINE (o2 > 0.3), and TIMING_RETARDED (nox > 50).
    # co2=14.0 keeps triangle sum ≥ 14.0 with co+o2=0.65.
    yield GasReading(hc=150, co=0.25, co2=14.0, o2=0.4, nox=75)  # wiki: GAS_WIKI §7.21

    # INCOMPLETE_COMBUSTION — wiki: GAS_WIKI §7.31
    # Escapes IGNITION_MISFIRE (hc < 1000), RICH_MISFIRE (o2 < 2.0),
    # LEAN_MISFIRE (co > 0.2), NORMAL_OPERATION (hc > 35, co2 < 14.5),
    # WORN_ENGINE (hc > 300, o2 > 0.3).  O2=1.8 keeps collision rule
    # dormant (O2 < 2.0 threshold).  Triangle sum = 14.3 (valid).
    # Lambda near-stoich + elevated HC + moderate CO — compression-loss
    # partial combustion, distinct from INCOMPLETE_OXIDATION (variable lambda).
    yield GasReading(hc=500, co=1.0, co2=11.5, o2=1.8, nox=30)  # wiki: GAS_WIKI §7.31
