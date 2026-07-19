"""DNALab assembly — build_vehicle_dna() orchestration."""

from __future__ import annotations

from typing import Any

from symptomlab import resolve as _resolve_symptom
from symptomlab.validator import SymptomValidationError
from vinlab import decode as _decode_vin

from dnalab.models import VehicleDNA


def build_vehicle_dna(vin: str, triage: dict[str, Any]) -> VehicleDNA:
    """Decode VIN and triage selection, combine into one VehicleDNA.

    Args:
        vin: 17-char VIN string. Passed verbatim to ``vinlab.decode()``.
        triage: dict with keys ``tier_1``, ``tier_2``, ``occurs_during``,
                ``engine_state``, ``load_state``. Passed to
                ``symptomlab.resolve()``.

    Returns:
        VehicleDNA (combined Part A + Part B + session metadata).

    Raises:
        vinlab.VINDecodeError: if the VIN is invalid or out of scope.
        symptomlab.SymptomValidationError: if the triage selection is invalid
            or a required key (tier_1, tier_2, occurs_during, engine_state,
            load_state) is missing from the triage dict.
    """
    required = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")
    # WHY: symptomlab.resolve() requires all five keys; a missing key would
    # produce a SymptomDNA with a silently empty field downstream.
    missing = [k for k in required if k not in triage]
    if missing:
        raise SymptomValidationError(
            f"build_vehicle_dna: missing required triage keys: {missing}"
        )
    physical = _decode_vin(vin)
    symptomatic = _resolve_symptom(
        tier_1=triage["tier_1"],
        tier_2=triage["tier_2"],
        occurs_during=triage["occurs_during"],
        engine_state=triage["engine_state"],
        load_state=triage["load_state"],
    )
    return VehicleDNA.new(vin_dna=physical, symptom_dna=symptomatic)
