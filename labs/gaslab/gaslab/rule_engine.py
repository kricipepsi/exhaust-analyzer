"""Rule engine — deterministic graph traversal for GASLab.

Pure functions that walk the YAML ontology, apply validity gates,
reasoning-grammar overrides, bound matching, and differentiator resolution
to produce a single ``(ChemicalSignature, SampleValidity)`` tuple.

Source: ``GAS_WIKI §6`` (validity gates), ``GAS_WIKI §8`` (reasoning grammar),
``GAS_WIKI §7`` (fault atlas).
"""

from __future__ import annotations

from gaslab.brettschneider import lambda_chem
from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.resolution import _euro_thresholds, _rich_co_ceiling, apply_differentiators
from gaslab.validity_gates import sample_validity

_GAS_KEYS: tuple[str, ...] = ("hc", "co", "co2", "o2", "nox", "lambda")


def _specificity(name: str, faults: dict) -> float:
    """Total width of a fault's signature ranges — lower is more specific.

    Used as a tie-breaker when multiple faults match the same reading.
    Narrower signatures describe more precise conditions and should win
    over catch-all entries like VVT_FAILURE or POA_SIGNATURE.
    """
    sig = faults[name]["signature"]
    return sum(
        sig[g]["max"] - sig[g]["min"]
        for g in _GAS_KEYS
    )


def _candidate_rank(name: str, faults: dict) -> tuple[bool, float]:
    """Return final candidate ordering with catch-all signatures last.

    Source: ``GAS_WIKI §7.23`` and ``GAS_WIKI §7.27``.
    """
    return (
        faults[name].get("signature_type") == "catch_all",
        _specificity(name, faults),
    )


def _is_low_triangle_exhaust_air_leak(reading: GasReading, ontology: dict) -> bool:
    """Return whether a low-triangle sample matches air-ingress chemistry.

    Source: ``GAS_WIKI §7.7`` and ``GAS_VOCABULARY §10.1``.
    """
    leak_signature = ontology.get("faults", {}).get(
        ChemicalSignature.EXHAUST_AIR_LEAK.value, {},
    ).get("signature", {})
    hc_bounds = leak_signature.get("hc", {})
    co_bounds = leak_signature.get("co", {})
    o2_bounds = leak_signature.get("o2", {})
    volumetric_sum = reading.co + reading.co2 + reading.o2  # wiki: GAS_WIKI §6.1

    return (
        volumetric_sum < 14.0  # wiki: GAS_WIKI §6.1; GAS_WIKI §7.7 reachability table
        and reading.hc <= hc_bounds.get("max", 100)  # vocab: GAS_VOCABULARY §10.1 normal_borderline.max
        and co_bounds.get("min", 0.1) <= reading.co <= co_bounds.get("max", 0.5)  # wiki: GAS_WIKI §7.7
        and reading.o2 > o2_bounds.get("min", 2.0)  # wiki: GAS_WIKI §7.7 — O2 > 2 %
    )


def _is_external_o2_suspect_leak(reading: GasReading, ontology: dict) -> bool:
    """Return whether an EXTERNAL_O2_SUSPECT-band sample matches leak chemistry.

    Source: ``GAS_WIKI §4.4``, ``GAS_WIKI §7.7`` and ``GAS_VOCABULARY §10.1``.
    """
    leak_signature = ontology.get("faults", {}).get(
        ChemicalSignature.EXHAUST_AIR_LEAK.value, {},
    ).get("signature", {})
    hc_bounds = leak_signature.get("hc", {})
    co_bounds = leak_signature.get("co", {})
    o2_bounds = leak_signature.get("o2", {})
    volumetric_sum = reading.co + reading.co2 + reading.o2

    return (
        16.0 < volumetric_sum <= 18.0  # wiki: GAS_WIKI §4.4
        and reading.hc <= hc_bounds.get("max", 100)  # vocab: GAS_VOCABULARY §10.1
        and co_bounds.get("min", 0.1) <= reading.co <= co_bounds.get("max", 0.5)  # wiki: GAS_WIKI §7.7
        and reading.o2 > o2_bounds.get("min", 2.0)  # wiki: GAS_WIKI §7.7
    )


def _signature_values(reading: GasReading) -> dict[str, float]:
    """Return the six gas-channel values used for bound matching.

    Source: ``GAS_WIKI §5`` and ``GAS_VOCABULARY §6``.
    """
    return {
        "hc": float(reading.hc),
        "co": reading.co,
        "co2": reading.co2,
        "o2": reading.o2,
        "nox": float(reading.nox),
        "lambda": lambda_chem(reading),
    }


def _signature_matches(signature: dict, values: dict[str, float]) -> bool:
    """Return whether all six gas-channel values sit inside ``signature``.

    Source: ``GAS_WIKI §7``.
    """
    return all(
        signature[gas_key]["min"] <= values[gas_key] <= signature[gas_key]["max"]
        for gas_key in _GAS_KEYS
    )


def _coc_adjust_normal_bounds(
    signature: dict,
    dna: GasLabDnaView,
) -> dict:
    """Return NORMAL_OPERATION signature bounds adjusted for per-vehicle CoC targets.

    When ``target_lambda_v112`` is present, the λ window is centered on
    ``v112 ± 0.005`` (clamped to a sane floor/ceiling). When absent, the
    generic ±0.005 window is kept.

    When ``co_low_idle`` is present, the CO max uses the per-vehicle CoC
    limit instead of the generic 0.45 %.

    Source: ``GAS_VOCABULARY §11``, ``GAS_WIKI §4.7``.
    """
    _LAMBDA_FLOOR = 0.85   # wiki: GAS_WIKI §4.7 — gasoline rich limit (~AFR 12.5)
    _LAMBDA_CEILING = 1.15  # wiki: GAS_WIKI §4.7 — gasoline lean limit (~AFR 16.9)

    adjusted = dict(signature)
    if dna.target_lambda_v112 is not None:
        lo = max(dna.target_lambda_v112 - 0.005, _LAMBDA_FLOOR)  # vocab: GAS_VOCABULARY §3
        hi = min(dna.target_lambda_v112 + 0.005, _LAMBDA_CEILING)  # vocab: GAS_VOCABULARY §3
        adjusted["lambda"] = {"min": lo, "max": hi}
        # wiki: GAS_WIKI §4.7 — CoC certified window [v112 - 0.005, v112 + 0.005]
    adjusted["co"] = dict(signature.get("co", {}))
    adjusted["co"]["max"] = _euro_thresholds(dna).co_idle_ceiling
    # wiki: GASWIKI-02 §2.8 — Euro-scaled idle CO ceiling
    if dna.co_low_idle is not None:
        adjusted["co"]["max"] = dna.co_low_idle
        # vocab: GAS_VOCABULARY §10.2 normal_with_cat — CO ceiling per CoC limit
    return adjusted


def _calibrate_o2_bias_low_bounds(
    signature: dict,
    dna: GasLabDnaView,
) -> dict:
    """Return O2_SENSOR_BIASED_LOW signature bounds calibrated for wideband.

    Source: ``GAS_WIKI §7.14``.
    """
    if dna.upstream_o2_type and "wideband" in dna.upstream_o2_type.lower():
        adjusted = dict(signature)
        adjusted["co"] = {"min": 5.0, "max": 8.0}  # wiki: GASWIKI-05 §7.14
        adjusted["lambda"] = {"min": 0.77, "max": 0.85}  # wiki: GASWIKI-05 §7.14
        return adjusted
    return signature


def _calibrate_o2_bias_high_bounds(
    signature: dict,
    dna: GasLabDnaView,
) -> dict:
    """Return O2_SENSOR_BIASED_HIGH signature bounds calibrated for wideband.

    Source: ``GAS_WIKI §7.15``.
    """
    if dna.upstream_o2_type and "wideband" in dna.upstream_o2_type.lower():
        adjusted = dict(signature)
        adjusted["lambda"] = {"min": 1.12, "max": 1.18}  # wiki: GASWIKI-05 §7.15
        return adjusted
    return signature


def _matching_fault_candidates(
    reading: GasReading,
    engine_state: EngineStateBucket,
    ontology: dict,
    dna: GasLabDnaView | None = None,
) -> list[str]:
    """Return ontology fault names whose six-channel signature matches.

    When *dna* carries per-vehicle CoC targets, NORMAL_OPERATION bounds are
    tightened or loosened before matching so the per-vehicle baseline determines
    what counts as normal.

    Source: ``GAS_WIKI §7``.
    """
    faults = ontology.get("faults", {})
    values = _signature_values(reading)
    candidates: list[str] = []

    for name, entry in faults.items():
        if name in ("SAMPLE_INVALID", "COOLANT_LEAK_INTERNAL"):
            continue  # grammar-gated — requires external context (block_test) not available in bound matching
        if entry.get("operating_state") != engine_state.value:
            continue

        sig = entry["signature"]
        if dna is not None:
            if name == "NORMAL_OPERATION":
                sig = _coc_adjust_normal_bounds(sig, dna)
            elif name == "O2_SENSOR_BIASED_LOW":
                sig = _calibrate_o2_bias_low_bounds(sig, dna)
            elif name == "O2_SENSOR_BIASED_HIGH":
                sig = _calibrate_o2_bias_high_bounds(sig, dna)

        if _signature_matches(sig, values):
            candidates.append(name)

    return candidates


def _resolve_candidates(
    candidates: list[str],
    reading: GasReading,
    dna: GasLabDnaView,
    ontology: dict,
    engine_state: EngineStateBucket,
    reading_high: GasReading | None = None,
    fuel_trim: float | None = None,
) -> list[str]:
    """Apply DNA, physical, and RPM differentiators to matched candidates.

    Source: ``GAS_WIKI §7.19/§7.20``, ``GAS_WIKI §7.23.1``,
    ``GAS_WIKI §7.8/§7.25``.
    """
    return apply_differentiators(
        candidates,
        reading,
        dna,
        ontology,
        engine_state,
        reading_high=reading_high,
        fuel_trim=fuel_trim,
    )


def _definitive_match(
    reading: GasReading,
    dna: GasLabDnaView,
    engine_state: EngineStateBucket,
    ontology: dict,
    block_test_passed: bool = False,
    reading_high: GasReading | None = None,
    fuel_trim: float | None = None,
) -> tuple[ChemicalSignature, SampleValidity] | None:
    """Return any pre-bound-match definitive traversal result.

    Source: ``GAS_WIKI §6`` and ``GAS_WIKI §8``.
    """
    if _is_low_triangle_exhaust_air_leak(reading, ontology):
        return ChemicalSignature.EXHAUST_AIR_LEAK, SampleValidity.EXTERNAL_O2_SUSPECT

    if fuel_trim is not None and _is_external_o2_suspect_leak(reading, ontology):
        # wiki: GAS_WIKI §4.4
        # vocab: GAS_VOCABULARY §10.8
        if fuel_trim > 8.0:  # vocab: GAS_VOCABULARY §10.8
            return ChemicalSignature.EXHAUST_AIR_LEAK, SampleValidity.EXTERNAL_O2_SUSPECT
        else:
            return ChemicalSignature.SAMPLE_INVALID, SampleValidity.INVALID

    validity = sample_validity(reading)
    if validity == SampleValidity.INVALID:
        return ChemicalSignature.SAMPLE_INVALID, validity

    grammar = ontology.get("reasoning_grammar", {})

    # Coolant intrusion — wiki: GAS_WIKI §8.7 (priority 87)
    coolant = grammar.get("coolant_intrusion_rule", {})
    if (
        reading.co2 <= coolant.get("co2_threshold", 12.0)  # wiki: GAS_WIKI §8.7
        and reading.hc >= coolant.get("hc_threshold", 300.0)  # wiki: GAS_WIKI §8.7
        and block_test_passed  # wiki: GAS_WIKI §8.7
    ):
        return ChemicalSignature.COOLANT_LEAK_INTERNAL, validity

    # Masking rule — wiki: GAS_WIKI §8.4 (priority 85)
    masking = grammar.get("masking_rule", {})
    if (
        reading.hc > masking.get("hc_threshold", 1000)  # wiki: GAS_WIKI §8.4
        and reading.o2 > masking.get("o2_threshold", 3.0)  # wiki: GAS_WIKI §8.4
        and reading.nox < masking.get("nox_threshold", 50)  # wiki: GAS_WIKI §8.4
    ):
        # wiki: GASWIKI-05 §FAULT_IGNITION_MISFIRE
        inferred_cyl = round(reading.o2 / (21 / dna.cylinder_count))  # wiki: GAS_WIKI §3.4
        # masking confirmed only if the O2 spike is consistent with >=1 dropped cylinder
        if inferred_cyl >= 1:  # wiki: GASWIKI-05 §FAULT_IGNITION_MISFIRE
            return ChemicalSignature.IGNITION_MISFIRE, validity

    # Cam-timing rule — wiki: GAS_WIKI §8.6 (priority 82)
    wvt = grammar.get("cam_timing_rule", {})
    if (
        reading.hc > wvt.get("hc_threshold", 1000)  # wiki: GAS_WIKI §8.6
        and reading.o2 > wvt.get("o2_threshold", 2.0)  # wiki: GAS_WIKI §8.6
        and reading.co > 0.0  # wiki: GAS_WIKI §8.6
    ):
        lchem = lambda_chem(reading)
        if 2.0 <= reading.o2 <= 4.5 and 1.08 <= lchem <= 1.18:  # wiki: GAS_WIKI §8.6
            # If reading_high is provided, verify it persists at 2500 RPM
            # high idle vector: O2 1.0-2.5%, lambda 1.03-1.09, HC 150-400, CO 0.10-0.30%, NOx 150-500
            if reading_high is not None:
                lchem_high = lambda_chem(reading_high)
                if (
                    1.0 <= reading_high.o2 <= 2.5  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAF (2500)
                    and 1.03 <= lchem_high <= 1.09
                    and 150 <= reading_high.hc <= 400
                    and 0.10 <= reading_high.co <= 0.30
                    and 150 <= reading_high.nox <= 500
                ):
                    return ChemicalSignature.CAM_TIMING_RETARDED_MAF, validity
            else:
                return ChemicalSignature.CAM_TIMING_RETARDED_MAF, validity
        elif 1.2 <= reading.o2 <= 2.5 and 1.03 <= lchem <= 1.08:  # wiki: GAS_WIKI §8.6
            # If reading_high is provided, verify NOx rises at 2500 RPM
            # high idle vector: O2 0.80-1.80%, lambda 1.01-1.05, HC 100-300, CO 0.15-0.50%, NOx 300-900
            if reading_high is not None:
                lchem_high = lambda_chem(reading_high)
                if (
                    0.80 <= reading_high.o2 <= 1.80  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_ADVANCED (2500)
                    and 1.01 <= lchem_high <= 1.05
                    and 300 <= reading_high.nox <= 900
                    and 100 <= reading_high.hc <= 300
                    and 0.15 <= reading_high.co <= 0.50
                ):
                    return ChemicalSignature.CAM_TIMING_ADVANCED, validity
            else:
                return ChemicalSignature.CAM_TIMING_ADVANCED, validity

    # RPM-differential routes — wiki: GAS_WIKI §7.23.1
    rpm_routed = _resolve_candidates(
        [], reading, dna, ontology, engine_state, reading_high, fuel_trim=fuel_trim
    )
    if rpm_routed:
        return ChemicalSignature(rpm_routed[0]), validity

    # Collision rule — wiki: GAS_WIKI §8.5 (priority 80)
    collision = grammar.get("collision_rule", {})
    if (
        reading.co > collision.get("co_tier_max", 0.45)  # wiki: GAS_WIKI §8.5
        and reading.o2 > collision.get("o2_threshold", 2.0)  # wiki: GAS_WIKI §8.5
    ):
        volumetric_sum = reading.co + reading.co2 + reading.o2  # wiki: GAS_WIKI §6.1
        if volumetric_sum <= collision.get("triangle_sum_threshold", 16.0):  # wiki: GAS_WIKI §8.5 — CO dominates
            return ChemicalSignature.RICH_MISFIRE, SampleValidity.EXTERNAL_O2_SUSPECT
        # wiki: GAS_WIKI §7.7 — EXHAUST_AIR_LEAK requires HC Normal;
        # high HC in the collision pattern is RICH_MISFIRE, not a pure leak
        if reading.hc <= collision.get("hc_max", 100):  # vocab: GAS_VOCABULARY §10.1 normal_borderline.max
            return ChemicalSignature.EXHAUST_AIR_LEAK, SampleValidity.EXTERNAL_O2_SUSPECT
        return ChemicalSignature.RICH_MISFIRE, SampleValidity.EXTERNAL_O2_SUSPECT

    # Rich timing branch rule (Priority 40 fallback) — wiki: GAS_WIKI §4.10, §7.24
    if (
        reading_high is not None
        and 400 <= reading.hc <= 1200
        and 3.5 <= reading.co <= 7.0
        and 0.75 <= lambda_chem(reading) <= 0.88
        and reading.o2 <= 0.5
    ):
        lchem_high = lambda_chem(reading_high)
        co_ceiling = _rich_co_ceiling(dna)
        hc_ceiling = _euro_thresholds(dna).hc_2500_ceiling
        if (
            200 <= reading_high.hc  # wiki: GASWIKI-06B §FAULT_CAM_TIMING_RETARDED_MAP (2500)
            and (hc_ceiling is None or reading_high.hc <= hc_ceiling)
            and co_ceiling <= reading_high.co <= 4.5
            and 11.0 <= reading_high.co2 <= 13.0
            and reading_high.o2 <= 0.5
            and 100 <= reading_high.nox <= 400
            and 0.85 <= lchem_high <= 0.95
        ):
            return ChemicalSignature.CAM_TIMING_RETARDED_MAP, validity

    return None


def classify(
    reading: GasReading,
    dna: GasLabDnaView,
    engine_state: EngineStateBucket,
    ontology: dict,
    block_test_passed: bool = False,
    reading_high: GasReading | None = None,
    fuel_trim: float | None = None,
) -> tuple[ChemicalSignature, SampleValidity]:
    """Run the 5-step diagnostic traversal.

    Source: ``GAS_WIKI §6`` traversal diagram.
    """
    # Step 1: validity gates — wiki: GAS_WIKI §6
    validity = sample_validity(reading)

    definitive = _definitive_match(
        reading, dna, engine_state, ontology,
        block_test_passed=block_test_passed,
        reading_high=reading_high,
        fuel_trim=fuel_trim,
    )
    if definitive is not None:
        return definitive

    # Step 3: fault bound matching — wiki: GAS_WIKI §7
    faults = ontology.get("faults", {})
    candidates = _matching_fault_candidates(reading, engine_state, ontology, dna)

    # Step 4: resolution — wiki: GAS_WIKI §7.19/§7.20, §7.8/§7.25
    candidates = _resolve_candidates(
        candidates, reading, dna, ontology, engine_state, reading_high, fuel_trim=fuel_trim
    )

    # Step 5: emit — wiki: GAS_WIKI §2.3
    if not candidates:
        return ChemicalSignature.NORMAL_OPERATION, validity

    best = min(candidates, key=lambda n: _candidate_rank(n, faults))
    return ChemicalSignature(best), validity
