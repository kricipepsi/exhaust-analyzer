"""Canonical family mapping for GASLab chemical signatures.

Source: GAS_WIKI §7 and GASLabSimple DESIGN_percent_sourcing.md §6 Q2.
The family strings mirror COMLabSimple PropSimple.md §1 without a cross-lab import.
"""

from gaslab.contracts import ChemicalSignature

CANONICAL_FAMILIES: frozenset[str] = frozenset(
    {
        "cam_timing",
        "catalyst_failure",
        "ecu_fault",
        "exhaust_leak",
        "ignition_fault",
        "invalid_input",
        "lean_condition",
        "mechanical_wear",
        "misfire",
        "no_fault",
        "non_starter",
        "rich_mixture",
        "sensor_fault",
    }
)
"""The COMLabSimple canonical family vocabulary mirrored locally."""

SIGNATURE_TO_FAMILY: dict[ChemicalSignature, str] = {
    ChemicalSignature.NORMAL_OPERATION: "no_fault",  # wiki: GAS_WIKI §7.1
    ChemicalSignature.RICH_MIXTURE: "rich_mixture",  # wiki: GAS_WIKI §7.2
    ChemicalSignature.LEAN_MIXTURE: "lean_condition",  # wiki: GAS_WIKI §7.3
    ChemicalSignature.IGNITION_MISFIRE: "misfire",  # wiki: GAS_WIKI §7.4
    ChemicalSignature.LEAN_MISFIRE: "misfire",  # wiki: GAS_WIKI §7.5
    ChemicalSignature.RICH_MISFIRE: "misfire",  # wiki: GAS_WIKI §7.6
    ChemicalSignature.EXHAUST_AIR_LEAK: "exhaust_leak",  # wiki: GAS_WIKI §7.7
    ChemicalSignature.HIGH_COMBUSTION_TEMP: "lean_condition",  # wiki: GAS_WIKI §7.8
    ChemicalSignature.CATALYST_NOT_LIGHTING_OFF: "catalyst_failure",  # wiki: GAS_WIKI §7.9
    ChemicalSignature.CATALYST_OVERWHELMED: "catalyst_failure",  # wiki: GAS_WIKI §7.10
    ChemicalSignature.SAMPLE_INVALID: "invalid_input",  # wiki: GAS_WIKI §7.11
    ChemicalSignature.TIMING_OVER_ADVANCED: "ignition_fault",  # wiki: GAS_WIKI §7.12
    ChemicalSignature.TIMING_RETARDED: "ignition_fault",  # wiki: GAS_WIKI §7.13
    ChemicalSignature.O2_SENSOR_BIASED_LOW: "sensor_fault",  # wiki: GAS_WIKI §7.14
    ChemicalSignature.O2_SENSOR_BIASED_HIGH: "sensor_fault",  # wiki: GAS_WIKI §7.15
    ChemicalSignature.WORN_ENGINE: "mechanical_wear",  # wiki: GAS_WIKI §7.16
    ChemicalSignature.FLAT_CAMSHAFT: "cam_timing",  # wiki: GAS_WIKI §7.17
    ChemicalSignature.GDI_INTAKE_VALVE_CARBON: "mechanical_wear",  # wiki: GAS_WIKI §7.18
    ChemicalSignature.VACUUM_REGULATOR_DIAPHRAGM_RUPTURE: "rich_mixture",  # wiki: GAS_WIKI §7.19
    ChemicalSignature.GDI_HPFP_INTERNAL_SEAL_LEAK: "rich_mixture",  # wiki: GAS_WIKI §7.20
    ChemicalSignature.WORN_VALVE_SEALS: "mechanical_wear",  # wiki: GAS_WIKI §7.21
    ChemicalSignature.WORN_PISTON_RINGS: "mechanical_wear",  # wiki: GAS_WIKI §7.22
    ChemicalSignature.POA_SIGNATURE: "mechanical_wear",  # wiki: GAS_WIKI §7.23
    ChemicalSignature.CAM_TIMING_RETARDED_MAP: "cam_timing",  # wiki: GAS_WIKI §7.24
    ChemicalSignature.CAM_TIMING_RETARDED_MAF: "cam_timing",  # wiki: GAS_WIKI §7.24
    ChemicalSignature.CAM_TIMING_ADVANCED: "cam_timing",  # wiki: GAS_WIKI §7.24
    ChemicalSignature.EGR_STUCK_CLOSED: "lean_condition",  # wiki: GAS_WIKI §7.25
    ChemicalSignature.EGR_STUCK_OPEN: "misfire",  # wiki: GAS_WIKI §7.26
    ChemicalSignature.VVT_FAILURE: "cam_timing",  # wiki: GAS_WIKI §7.27
    ChemicalSignature.EVAP_CANISTER_SATURATED: "rich_mixture",  # wiki: GAS_WIKI §7.28
    ChemicalSignature.EGR_DILUTION_MISFIRE: "misfire",  # wiki: GAS_WIKI §7.29
    ChemicalSignature.INCOMPLETE_OXIDATION: "catalyst_failure",  # wiki: GAS_WIKI §7.30
    ChemicalSignature.INCOMPLETE_COMBUSTION: "misfire",  # wiki: GAS_WIKI §7.31
    ChemicalSignature.COOLANT_LEAK_INTERNAL: "mechanical_wear",  # wiki: GAS_WIKI §7.32
}
"""Exhaustive mapping from GASLab signatures to canonical fusion families."""

__all__ = ["CANONICAL_FAMILIES", "SIGNATURE_TO_FAMILY"]
