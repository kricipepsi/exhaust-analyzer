"""Entity resolution layer — handles overlapping fault signatures.

Pure functions for detecting and resolving overlaps between fault signatures
in the GASLab ontology.  Two faults overlap when their per-gas [min, max]
intervals intersect for all five analyser gases plus lambda at the same
``operating_state``.

Source: ``GAS_WIKI §7.19/§7.20`` (VR diaphragm rupture ↔ GDI HPFP seal leak),
``GAS_WIKI §7.8/§7.25`` (HIGH_COMBUSTION_TEMP ↔ EGR_STUCK_CLOSED),
``GAS_WIKI §13.1`` (reference appendix — rule-of-thumb overlap separation).
"""

from __future__ import annotations

from typing import NamedTuple

from gaslab.audits import _is_catch_all
from gaslab.brettschneider import lambda_chem
from gaslab.contracts import EngineStateBucket, GasReading
from gaslab.dna_view import GasLabDnaView


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_GAS_KEYS: list[str] = ["hc", "co", "co2", "o2", "nox", "lambda"]
HC_IGNITION_MISFIRE_FLOOR = 1000  # vocab: GAS_VOCABULARY §10.1


class EuroThresholds(NamedTuple):
    """Euro-class default emissions ceilings from ``CONCEPT_EURO_SCALING``."""

    co_idle_ceiling: float
    hc_2500_ceiling: int | None


_EURO_THRESHOLDS: dict[str, EuroThresholds] = {
    "1": EuroThresholds(4.5, None),  # wiki: GASWIKI-02 §2.8
    "2": EuroThresholds(0.5, 1200),  # wiki: GASWIKI-02 §2.8
    "3": EuroThresholds(0.3, 200),  # wiki: GASWIKI-02 §2.8
    "4": EuroThresholds(0.2, 200),  # wiki: GASWIKI-02 §2.8
    "5": EuroThresholds(0.2, 200),  # wiki: GASWIKI-02 §2.8
}


def _euro_thresholds(dna: GasLabDnaView) -> EuroThresholds:
    """Return Euro-scaled CO/HC ceilings, defaulting unknown values to Euro 4."""
    category = dna.euro_emission_category.upper().replace("_", " ").replace("-", " ")
    for euro_class, thresholds in _EURO_THRESHOLDS.items():
        if euro_class in category:
            return thresholds
    return _EURO_THRESHOLDS["4"]  # wiki: GASWIKI-02 §2.8


_CAM_TIMING_SIGNATURES: set[str] = {
    "CAM_TIMING_RETARDED_MAP",
    "CAM_TIMING_RETARDED_MAF",
    "CAM_TIMING_ADVANCED",
}
_MISFIRE_FAMILY_SIGNATURES: set[str] = {
    "IGNITION_MISFIRE",
    "LEAN_MISFIRE",
    "RICH_MISFIRE",
    "EGR_DILUTION_MISFIRE",
    "INCOMPLETE_COMBUSTION",
}


def _ranges_overlap(a_min: float, a_max: float, b_min: float, b_max: float) -> bool:
    """True if two closed intervals [a_min, a_max] and [b_min, b_max] intersect."""
    return max(a_min, b_min) <= min(a_max, b_max)


def _resolve_dna_field(dna: GasLabDnaView, field_path: str):
    """Resolve a dotted YAML field path to a ``GasLabDnaView`` attribute value.

    The YAML uses logical namespace prefixes (e.g. ``emissions.egr_equipped``).
    The last dot-segment is the flat attribute name on ``GasLabDnaView``.
    """
    attr = field_path.split(".")[-1]
    return getattr(dna, attr, None)


def _value_within_bounds(value: float, bounds: dict) -> bool:
    """Return whether ``value`` satisfies a declarative min/max bound."""
    minimum = bounds.get("min")
    maximum = bounds.get("max")
    return (
        (minimum is None or value >= minimum)
        and (maximum is None or value <= maximum)
    )


def _rich_co_ceiling(dna: GasLabDnaView) -> float:
    """Rich-CO ceiling (``mild_rich.max``) at 2500 RPM for the CAM_MAP branch.

    The per-vehicle ``co_high_idle`` from the vehicle's CoC overrides the Euro
    default, but only when the DNA lookup is HIGH-confidence and the field is
    populated.  Otherwise the Euro threshold table applies.

    Source: ``GAS_VOCABULARY §11`` (per-vehicle override gate, confidence=HIGH) +
    ``GASWIKI-02 §2.8`` (Euro-scaled defaults).
    """
    if dna.confidence == "HIGH" and dna.co_high_idle is not None:  # vocab: GAS_VOCABULARY §11
        return dna.co_high_idle
    return _euro_thresholds(dna).co_idle_ceiling  # wiki: GASWIKI-02 §2.8


def _prune_low_hc_misfires_when_timing_confirmed(
    survivors: list[str],
    reading: GasReading,
) -> list[str]:
    """Remove generic misfire survivors when RPM-confirmed cam timing explains the overlap.

    Source: ``GAS_WIKI §8.9`` (RPM family-separation matrix) and
    ``GAS_VOCABULARY §10.1`` (``ignition_misfire_floor``).
    """
    timing_confirmed = any(c in _CAM_TIMING_SIGNATURES for c in survivors)
    if not timing_confirmed or reading.hc >= HC_IGNITION_MISFIRE_FLOOR:
        return survivors
    return [c for c in survivors if c not in _MISFIRE_FAMILY_SIGNATURES]


def _resolve_lean_timing_cosurvival(
    survivors: list[str],
    *,
    lean_normalises_at_high_idle: bool,
    cam_maf_persists_at_high_idle: bool,
) -> list[str]:
    """Enforce LEAN_MIXTURE vs CAM_MAF mutual exclusion after RPM gates.

    Source: ``GAS_WIKI §8.9`` (normalise/persist RPM separation) and
    ``GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF``.
    """
    has_lean_and_cam_maf = (
        "LEAN_MIXTURE" in survivors and "CAM_TIMING_RETARDED_MAF" in survivors
    )
    if not has_lean_and_cam_maf:
        return survivors

    # A vacuum/fuel lean normalises at high idle; a retarded-cam MAF lean persists.
    # Source: GAS_WIKI §8.9 and GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF.
    if lean_normalises_at_high_idle:
        return [c for c in survivors if c != "CAM_TIMING_RETARDED_MAF"]
    if cam_maf_persists_at_high_idle:
        return [c for c in survivors if c != "LEAN_MIXTURE"]
    return survivors


def _rpm_route_matches(
    edge: dict,
    reading: GasReading,
    engine_state: EngineStateBucket | None,
) -> bool:
    """Return whether an ``rpm_differential`` route edge matches this reading.

    Source: ``GAS_WIKI §7.23.1``.
    """
    if edge.get("type") != "rpm_differential" or not edge.get("route_when_matched"):
        return False
    if engine_state is None:
        return False

    allowed = edge.get("route_appears_in_states", edge.get("appears_in_states", []))
    if allowed and engine_state.value not in allowed:
        return False

    signature = edge.get("signature", {})
    values = {
        "hc": float(reading.hc),
        "co": reading.co,
        "co2": reading.co2,
        "o2": reading.o2,
        "nox": float(reading.nox),
        "lambda": lambda_chem(reading),
    }
    return all(
        gas_key in values and _value_within_bounds(values[gas_key], bounds)
        for gas_key, bounds in signature.items()
    )


def _append_rpm_routes(
    candidates: list[str],
    reading: GasReading,
    ontology: dict,
    engine_state: EngineStateBucket | None,
) -> list[str]:
    """Append ontology-declared RPM-differential route targets.

    Source: ``GAS_WIKI §7.23.1``.
    """
    routed = list(candidates)
    faults = ontology["faults"]
    for name, entry in faults.items():
        for edge in entry.get("differentiator_edges") or []:
            if not _rpm_route_matches(edge, reading, engine_state):
                continue
            target = edge.get("routes_to", name)
            if target in faults and target not in routed:
                routed.append(target)
    return routed


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def find_overlaps(ontology: dict) -> list[tuple[str, str]]:
    """Return fault-name pairs whose signature ranges overlap on all gases.

    Two faults overlap when their per-gas [min, max] intervals intersect for
    all five analyser gases plus lambda, at the same ``operating_state``.

    Args:
        ontology: Parsed ontology dict with a ``faults`` key.

    Returns:
        Sorted list of ``(name_a, name_b)`` tuples.  Each pair appears once
        (``name_a < name_b`` lexicographically).
    """
    faults = ontology["faults"]
    pairs: list[tuple[str, str]] = []

    names = sorted(faults.keys())
    for i, name_a in enumerate(names):
        if name_a == "SAMPLE_INVALID":
            continue
        entry_a = faults[name_a]
        if _is_catch_all(entry_a):
            continue
        sig_a = entry_a["signature"]
        state_a = entry_a.get("operating_state")
        for name_b in names[i + 1:]:
            if name_b == "SAMPLE_INVALID":
                continue
            entry_b = faults[name_b]
            if _is_catch_all(entry_b):
                continue
            state_b = entry_b.get("operating_state")
            if state_a != state_b:
                continue
            sig_b = entry_b["signature"]
            if all(
                _ranges_overlap(
                    sig_a[g]["min"], sig_a[g]["max"],
                    sig_b[g]["min"], sig_b[g]["max"],
                )
                for g in _GAS_KEYS
            ):
                pairs.append((name_a, name_b))

    return pairs


def apply_differentiators(
    candidates: list[str],
    reading: GasReading,
    dna: GasLabDnaView,
    ontology: dict,
    engine_state: EngineStateBucket | None = None,
    reading_high: GasReading | None = None,
    fuel_trim: float | None = None,
) -> list[str]:
    """Filter candidates by ``dna_gate`` and ``differentiator_edges`` declarations.

    Each candidate is checked against its ontology entry:

    1. If the entry declares a ``dna_gate``, the DNA view must match.
    2. If the entry declares ``differentiator_edges``, each edge of type
       ``dna`` must match the DNA view.  Edges of type ``physical_check``
       are informational — they never filter.
    3. Edges of type ``rpm_differential`` compare the ``appears_in_states``
       list against the current ``engine_state``; if ``engine_state`` is
       ``None`` the edge is treated as informational (backwards-compat).

    Args:
        candidates: Fault names that match the gas signature.
        reading: The raw gas reading (reserved for rpm-dependent edges).
        dna: The slim DNA view for this vehicle.
        ontology: Parsed ontology dict.
        engine_state: RPM-bucket label for rpm_differential edge filtering.
            Default ``None`` preserves backwards compatibility.
        reading_high: Optional high-idle (2500 RPM) gas reading.
        fuel_trim: Optional short-term fuel trim context input (2500 RPM / high-idle).

    Returns:
        Candidates that survive all applicable gates and differentiators.
    """
    faults = ontology["faults"]
    survivors: list[str] = []

    for name in candidates:
        entry = faults.get(name)
        if entry is None:
            continue

        # 1. dna_gate — must match if present
        dna_gate = entry.get("dna_gate")
        if dna_gate is not None:
            field_path: str = dna_gate["field"]
            expected = dna_gate["value"]
            actual = _resolve_dna_field(dna, field_path)
            if actual != expected:
                continue

        # 2. differentiator_edges — dna-type edges must match
        edges: list[dict] | None = entry.get("differentiator_edges")
        if edges:
            rejected = False
            for edge in edges:
                if edge.get("type") == "dna":
                    edge_field: str = edge["field"]
                    edge_expected = edge["equals"]
                    edge_actual = _resolve_dna_field(dna, edge_field)
                    if edge_actual != edge_expected:
                        rejected = True
                        break
                elif edge.get("type") == "rpm_differential" and engine_state is not None:  # wiki: GAS_VOCABULARY §7
                    allowed = edge.get("appears_in_states", [])
                    if allowed and engine_state.value not in allowed:
                        rejected = True
                        break
                # physical_check edges are informational
            if rejected:
                continue

        survivors.append(name)

    # Vacuum leak normalisation check for LEAN_MIXTURE (Rule 8.9)
    lean_normalises_at_high_idle = False
    if "LEAN_MIXTURE" in survivors and reading_high is not None:
        lchem_high = lambda_chem(reading_high)
        lean_normalises_at_high_idle = (
            reading_high.o2 < 1.0  # wiki: GAS_WIKI §8.9 - lean normalises at 2500
            and 0.985 <= lchem_high <= 1.015  # wiki: GAS_WIKI §8.9 - lambda normalises toward 1.0
        )
        if not lean_normalises_at_high_idle:
            survivors = [c for c in survivors if c != "LEAN_MIXTURE"]

    # Timing family — idle→2500 RPM-differential separation.
    # The discriminator is the idle→2500 *behaviour* (normalise / persist /
    # NOx-rise), not a single-point 2500 window.
    # Source: GASWIKI-08 §8.9 TEST_RPM_SEPARATION_MATRIX
    # + the three cam-timing fault vectors (GASWIKI-06B).
    if reading_high is not None:
        lchem_idle = lambda_chem(reading)
        lchem_high = lambda_chem(reading_high)
        cam_maf_persists_at_high_idle = False

        if "CAM_TIMING_RETARDED_MAF" in survivors:
            # Lean at idle, persists lean at 2500 (no normalisation): a vacuum
            # leak normalises against metered air; the mechanical phasing error
            # does not.  Source: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF.
            cam_maf_persists_at_high_idle = (
                2.0 <= reading.o2 <= 4.5  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (idle)
                and 1.08 <= lchem_idle <= 1.18  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (idle)
                and 1.0 <= reading_high.o2 <= 2.5  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (2500)
                and 1.03 <= lchem_high <= 1.09  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (2500)
                and 150 <= reading_high.hc <= 400  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (2500)
                and 0.10 <= reading_high.co <= 0.30  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (2500)
                and 150 <= reading_high.nox <= 500  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (2500)
            )
            if not cam_maf_persists_at_high_idle:
                survivors = [c for c in survivors if c != "CAM_TIMING_RETARDED_MAF"]

        if "CAM_TIMING_ADVANCED" in survivors:
            # Rough idle with a mild-lean idle λ-offset (cam, not ignition); at
            # 2500 dynamic scavenging stabilises combustion (HC/CO fall) while
            # NOx rises with peak pressure/temperature.  The idle λ-offset +
            # rough-idle HC separates this from ignition TIMING_OVER_ADVANCED
            # (clean idle, NOx-only high-idle spike).
            # Source: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED.
            if not (
                250 <= reading.hc <= 600  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (idle)
                and 1.03 <= lchem_idle <= 1.08  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (idle)
                and reading_high.nox > reading.nox  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED — NOx rises idle→2500
                and reading_high.hc < reading.hc  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED — HC falls idle→2500
                and reading_high.co < reading.co  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED — CO falls idle→2500
                and 0.80 <= reading_high.o2 <= 1.80  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (2500)
                and 1.01 <= lchem_high <= 1.05  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (2500)
                and 100 <= reading_high.hc <= 300  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (2500)
                and 0.15 <= reading_high.co <= 0.50  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (2500)
                and 300 <= reading_high.nox <= 900  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (2500)
            ):
                survivors = [c for c in survivors if c != "CAM_TIMING_ADVANCED"]

        if "CAM_TIMING_RETARDED_MAP" in survivors:
            # Rich at idle (Speed-Density over-fuel), partially normalising
            # toward 2500 as vacuum recovers (λ rises toward 1.0, CO falls); a
            # sensor/fuelling rich-bias stays flat and is rejected.
            # Rich-CO lower bound = Euro-scaled ceiling; per-vehicle
            # co_high_idle overrides that default when confidence is HIGH
            # (GAS_VOCABULARY §11, GASWIKI-02 §2.8).
            # Source: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP.
            co_ceiling = _rich_co_ceiling(dna)  # vocab: GAS_VOCABULARY §11/§10.2
            hc_ceiling = _euro_thresholds(dna).hc_2500_ceiling
            if not (
                0.75 <= lchem_idle <= 0.88  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP (idle)
                and reading.o2 <= 0.5  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP (idle)
                and lchem_high > lchem_idle  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP — λ rises toward 1.0; flat rich rejected
                and reading_high.co < reading.co  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP — CO falls idle→2500
                and reading_high.o2 <= 0.5  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP (2500)
                and 0.85 <= lchem_high <= 0.95  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP (2500)
                and 200 <= reading_high.hc  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP (2500)
                and (
                    hc_ceiling is None or reading_high.hc <= hc_ceiling
                )  # wiki: GASWIKI-02 §2.8
                and co_ceiling <= reading_high.co <= 4.5  # vocab: GAS_VOCABULARY §10.2
                and 100 <= reading_high.nox <= 400  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP (2500)
            ):
                survivors = [c for c in survivors if c != "CAM_TIMING_RETARDED_MAP"]

        survivors = _resolve_lean_timing_cosurvival(
            survivors,
            lean_normalises_at_high_idle=lean_normalises_at_high_idle,
            cam_maf_persists_at_high_idle=cam_maf_persists_at_high_idle,
        )

        # Once an idle->2500 RPM discriminator has confirmed a cam-timing
        # state, low-HC generic misfire candidates are overlap noise rather
        # than a competing fault. True high-HC misfire remains a co-fault.
        # Source: GAS_WIKI §8.9 (TEST_RPM_SEPARATION_MATRIX).
        survivors = _prune_low_hc_misfires_when_timing_confirmed(survivors, reading)

        # Ignition over-advance vs the cam family: a clean idle with a
        # NOx-only spike at 2500 RPM is ignition timing, not cam timing (the
        # cam family shows rough idle + an idle λ-offset, gated above).
        # Source: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED.
        toa_clean_idle = (
            120 <= reading.hc <= 250  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED (idle)
            and 0.10 <= reading.co <= 0.30  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED (idle)
            and 11.5 <= reading.co2 <= 13.0  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED (idle)
            and 0.8 <= reading.o2 <= 1.5  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED (idle)
            and 20 <= reading.nox <= 60  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED (idle)
            and 1.01 <= lchem_idle <= 1.04  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED (idle)
        )
        toa_nox_spike = (
            reading_high.nox > 1200  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED — NOx very high at 2500
            and 1.0 <= lchem_high <= 1.06  # wiki: GASWIKI-05 §FAULT_TIMING_OVER_ADVANCED (2500)
            and reading_high.hc <= 100  # vocab: GAS_VOCABULARY §10.1 normal_borderline.max — "others near normal"
            and reading_high.co <= 0.45  # vocab: GAS_VOCABULARY §10.2 normal_with_cat.max — "others near normal"
        )
        if toa_clean_idle and toa_nox_spike and "TIMING_OVER_ADVANCED" not in survivors:
            survivors.append("TIMING_OVER_ADVANCED")

        # Mechanical wear family — idle→2500 HC change direction + load-state CO + λ.
        # Resolves POA_SIGNATURE (catch-all) and co-surviving WORN_* to a specific leaf.
        # Source: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR.
        mechanical_wear_family = {"POA_SIGNATURE", "WORN_VALVE_SEALS", "WORN_PISTON_RINGS", "WORN_ENGINE"}
        if any(c in survivors for c in mechanical_wear_family):
            routed_leaf = None
            if (
                300 <= reading.hc <= 500  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.hc <= 35  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.hc < reading.hc  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.co <= 0.15  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and 0.96 <= lchem_high <= 1.0  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and (fuel_trim is None or -8.0 <= fuel_trim <= 8.0)  # vocab: GAS_VOCABULARY §10.8 stable_band
            ):
                routed_leaf = "WORN_VALVE_SEALS"
            elif (
                100 <= reading.hc <= 150  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.hc > 300  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.hc > reading.hc  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.co > 0.5  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and lchem_high < 0.99  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and (fuel_trim is None or fuel_trim <= -12.0)  # vocab: GAS_VOCABULARY §10.8 negative_load_cut
            ):
                routed_leaf = "WORN_PISTON_RINGS"
            elif (
                150 <= reading.hc <= 300  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and 150 <= reading_high.hc <= 300  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.co >= reading.co  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and 1.0 <= lchem_high <= 1.03  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
            ):
                routed_leaf = "WORN_ENGINE"
            elif (
                dna.induction_type == "forced"  # wiki: GASWIKI-01 §CONCEPT_GASLABDNAVIEW
                and reading.hc > 500  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.hc < reading.hc  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading.co <= 0.10  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.co <= 0.10  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and 0.995 <= lchem_idle <= 1.005  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and 0.995 <= lchem_high <= 1.005  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
            ):
                routed_leaf = "POA_SIGNATURE"
            elif (
                reading.hc > 500  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and reading_high.hc > 500  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
                and (lchem_high < 0.95 or lchem_high > 1.05)  # wiki: GASWIKI-06A §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR
            ):
                routed_leaf = "POA_SIGNATURE"

            if routed_leaf is not None:
                new_survivors = []
                inserted = False
                for c in survivors:
                    if c in mechanical_wear_family:
                        if not inserted:
                            new_survivors.append(routed_leaf)
                            inserted = True
                    else:
                        new_survivors.append(c)
                survivors = new_survivors
            else:
                survivors = [c for c in survivors if c not in mechanical_wear_family]

    # Catalyst dual-idle weak-vs-dead logic (Rule 7.6)
    if dna.has_catalyst and reading_high is not None:
        lchem = lambda_chem(reading)
        lchem_high = lambda_chem(reading_high)

        # Precondition: fuel control must be healthy (lambda at both speeds in [0.98, 1.02])
        if not (0.98 <= lchem <= 1.02 and 0.98 <= lchem_high <= 1.02):  # wiki: GAS_WIKI §7.6
            # Fuel control is bad, reject both catalyst states
            survivors = [c for c in survivors if c not in ("CATALYST_NOT_LIGHTING_OFF", "CATALYST_OVERWHELMED")]
        else:
            # Working catalyst at 2500 RPM: CO2 14.5-16.0%, O2 < 0.5%, CO < 0.2%, HC < 35 ppm
            high_is_working = (
                14.5 <= reading_high.co2 <= 16.0  # wiki: GAS_WIKI §7.6
                and reading_high.o2 < 0.5  # wiki: GAS_WIKI §7.6
                and reading_high.co < 0.2  # wiki: GAS_WIKI §7.6
                and reading_high.hc < 35  # wiki: GAS_WIKI §7.6
            )
            # Weak catalyst at idle: CO2 13.5-14.5%, O2 0.3-0.7%, CO 0.5-0.9%, HC 75-125 ppm
            idle_is_weak = (
                13.5 <= reading.co2 <= 14.5  # wiki: GAS_WIKI §7.6
                and 0.3 <= reading.o2 <= 0.7  # wiki: GAS_WIKI §7.6
                and 0.5 <= reading.co <= 0.9  # wiki: GAS_WIKI §7.6
                and 75 <= reading.hc <= 125  # wiki: GAS_WIKI §7.6
            )
            # Dead catalyst at 2500 RPM: CO2 < 13.5%, HC > 100, CO > 0.5%, O2 > 0.5%
            high_is_dead = (
                reading_high.co2 < 13.5  # wiki: GAS_WIKI §7.6
                and reading_high.hc > 100  # wiki: GAS_WIKI §7.6
                and reading_high.co > 0.5  # wiki: GAS_WIKI §7.6
                and reading_high.o2 > 0.5  # wiki: GAS_WIKI §7.6
            )
            # Dead catalyst at idle: CO2 < 13.5%, HC > 100, CO > 0.5%, O2 > 0.5%
            idle_is_dead = (
                reading.co2 < 13.5  # wiki: GAS_WIKI §7.6
                and reading.hc > 100  # wiki: GAS_WIKI §7.6
                and reading.co > 0.5  # wiki: GAS_WIKI §7.6
                and reading.o2 > 0.5  # wiki: GAS_WIKI §7.6
            )

            # Routing checks
            has_weak_delta = idle_is_weak and high_is_working
            has_dead_both = idle_is_dead and high_is_dead

            new_survivors = []
            for c in survivors:
                if c == "CATALYST_NOT_LIGHTING_OFF":
                    if has_weak_delta:
                        new_survivors.append(c)
                    elif has_dead_both:
                        # Route from weak to overwhelmed if dead at both speeds
                        if "CATALYST_OVERWHELMED" not in new_survivors:
                            new_survivors.append("CATALYST_OVERWHELMED")
                elif c == "CATALYST_OVERWHELMED":
                    if has_dead_both:
                        new_survivors.append(c)
                else:
                    new_survivors.append(c)
            survivors = new_survivors

    return _append_rpm_routes(survivors, reading, ontology, engine_state)


def is_resolved(candidates: list[str]) -> bool:
    """Return True if at most one candidate survives resolution."""
    return len(candidates) <= 1
