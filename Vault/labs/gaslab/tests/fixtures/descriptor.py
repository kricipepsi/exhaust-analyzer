"""GASLab ModuleDescriptor declaration."""

from __future__ import annotations

from typing import Any
from harness.descriptor import FaultBox, FieldRange, ModuleDescriptor

_ENVELOPE = {
    "gas_hc": (0.0, 20000.0),
    "gas_co": (0.0, 15.0),
    "gas_co2": (0.0, 22.0),
    "gas_o2": (0.0, 22.0),
    "gas_nox": (0.0, 5000.0),
}

# Map each ChemicalSignature to its documented gas-dimension bounds.
_BOX_DEFS: list[dict[str, Any]] = [
    # --- §7.1 NORMAL_OPERATION ---
    {
        "sig": "NORMAL_OPERATION",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.5), "gas_co2": (13, 16), "gas_o2": (0, 0.5), "gas_nox": (0, 100)},
        "src": "GAS_WIKI §7.1; GAS_VOCABULARY §10.1-10.5",
    },
    # --- §7.2 RICH_MIXTURE ---
    {
        "sig": "RICH_MIXTURE",
        "dims": {"gas_hc": (0, 500), "gas_co": (1.5, 15), "gas_co2": (0, 14), "gas_o2": (0, 0.5), "gas_nox": (0, 500)},
        "src": "GAS_WIKI §7.2; GAS_VOCABULARY §10.2 clear_rich",
    },
    # --- §7.3 LEAN_MIXTURE ---
    {
        "sig": "LEAN_MIXTURE",
        "dims": {"gas_hc": (0, 200), "gas_co": (0, 0.1), "gas_co2": (0, 14), "gas_o2": (2.5, 22), "gas_nox": (0, 500)},
        "src": "GAS_WIKI §7.3; GAS_VOCABULARY §10.4 mild_lean",
    },
    # --- §7.4 IGNITION_MISFIRE (pri-85 masking rule) ---
    {
        "sig": "IGNITION_MISFIRE",
        "dims": {"gas_hc": (1000, 20000), "gas_co": (0, 15), "gas_co2": (0, 16), "gas_o2": (3.0, 22), "gas_nox": (0, 50)},
        "src": "GAS_WIKI §7.4 §8.4; GAS_VOCABULARY §10.1 ignition_misfire_floor",
    },
    # --- §7.5 LEAN_MISFIRE ---
    {
        "sig": "LEAN_MISFIRE",
        "dims": {"gas_hc": (200, 600), "gas_co": (0, 0.2), "gas_co2": (0, 12), "gas_o2": (4.0, 22), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.5; GAS_VOCABULARY §10.4 severe_lean_or_misfire",
    },
    # --- §7.6 RICH_MISFIRE (collision-rule branch, vsum <= 16) ---
    {
        "sig": "RICH_MISFIRE",
        "dims": {"gas_hc": (200, 20000), "gas_co": (0.45, 15), "gas_co2": (5, 15), "gas_o2": (2.0, 22), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.6 §8.5; GAS_VOCABULARY §10.1-10.5",
    },
    # --- §7.7 EXHAUST_AIR_LEAK (collision-rule branch, vsum > 16) ---
    {
        "sig": "EXHAUST_AIR_LEAK",
        "dims": {"gas_hc": (0, 20000), "gas_co": (0.45, 15), "gas_co2": (0, 16), "gas_o2": (2.0, 22), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.7 §8.5; GAS_VOCABULARY §10.1-10.5",
    },
    # --- §7.8 HIGH_COMBUSTION_TEMP ---
    {
        "sig": "HIGH_COMBUSTION_TEMP",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.5), "gas_co2": (13, 16), "gas_o2": (0, 0.5), "gas_nox": (1000, 5000)},
        "src": "GAS_WIKI §7.8; GAS_VOCABULARY §10.5 high_combustion_temp",
    },
    # --- §7.9 CATALYST_NOT_LIGHTING_OFF ---
    {
        "sig": "CATALYST_NOT_LIGHTING_OFF",
        "dims": {"gas_hc": (75, 125), "gas_co": (0.5, 0.9), "gas_co2": (13.5, 14.5), "gas_o2": (0.3, 0.7), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.9; GAS_VOCABULARY §10.2 cat_not_lit_band §3.1 dna_gate",
    },
    # --- §7.10 CATALYST_OVERWHELMED ---
    {
        "sig": "CATALYST_OVERWHELMED",
        "dims": {"gas_hc": (200, 20000), "gas_co": (1.0, 15), "gas_co2": (0, 12), "gas_o2": (0, 2.0), "gas_nox": (500, 5000)},
        "src": "GAS_WIKI §7.10; GAS_VOCABULARY §10.5 elevated_idle §3.1 dna_gate",
    },
    # --- SAMPLE_INVALID (validity-gate pre-empt; no gas signature of its own) ---
    {
        "sig": "SAMPLE_INVALID",
        "dims": dict(_ENVELOPE),
        "src": "GAS_WIKI §6.1-6.2; GAS_VOCABULARY §5 (validity gate — not a gas-signature box)",
    },
    # --- §7.12 TIMING_OVER_ADVANCED (unreachable in v1 — audit AF-1) ---
    {
        "sig": "TIMING_OVER_ADVANCED",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.5), "gas_co2": (13, 16), "gas_o2": (0, 0.5), "gas_nox": (1000, 5000)},
        "src": "GAS_WIKI §7.12; GAS_VOCABULARY §10.5 high_combustion_temp (identical gas signature to HCT; unreachable in v1 — audit AF-1)",
    },
    # --- §7.13 TIMING_RETARDED ---
    {
        "sig": "TIMING_RETARDED",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.5), "gas_co2": (13, 16), "gas_o2": (0, 0.5), "gas_nox": (0, 50)},
        "src": "GAS_WIKI §7.13; GAS_VOCABULARY §10.5 misfire_suppression",
    },
    # --- §7.14 O2_SENSOR_BIASED_LOW ---
    {
        "sig": "O2_SENSOR_BIASED_LOW",
        "dims": {"gas_hc": (0, 100), "gas_co": (0.5, 3.0), "gas_co2": (13, 16), "gas_o2": (0, 0.3), "gas_nox": (0, 500)},
        "src": "GAS_WIKI §7.14; GAS_VOCABULARY §10.2 mild_rich",
    },
    # --- §7.15 O2_SENSOR_BIASED_HIGH ---
    {
        "sig": "O2_SENSOR_BIASED_HIGH",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.2), "gas_co2": (13, 16), "gas_o2": (0.5, 2.0), "gas_nox": (0, 500)},
        "src": "GAS_WIKI §7.15; GAS_VOCABULARY §10.1-10.5",
    },
    # --- §7.16 WORN_ENGINE (unreachable in v1 — audit AF-3) ---
    {
        "sig": "WORN_ENGINE",
        "dims": {"gas_hc": (35, 300), "gas_co": (0.1, 1.0), "gas_co2": (13, 16), "gas_o2": (0, 0.3), "gas_nox": (0, 100)},
        "src": "GAS_WIKI §7.16; GAS_VOCABULARY §10.1-10.5 (unreachable in v1 — audit AF-3)",
    },
    # --- §7.17 FLAT_CAMSHAFT ---
    {
        "sig": "FLAT_CAMSHAFT",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.5), "gas_co2": (13, 16), "gas_o2": (0, 0.5), "gas_nox": (0, 100)},
        "src": "GAS_WIKI §7.17; GAS_VOCABULARY §10.1-10.5",
    },
    # --- §7.18 GDI_INTAKE_VALVE_CARBON ---
    {
        "sig": "GDI_INTAKE_VALVE_CARBON",
        "dims": {"gas_hc": (100, 20000), "gas_co": (0, 0.45), "gas_co2": (0, 16), "gas_o2": (2.0, 22), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.18; GAS_VOCABULARY §10.1 real_combustion_fault §3.1 dna_gate",
    },
    # --- §7.19 VACUUM_REGULATOR_DIAPHRAGM_RUPTURE ---
    {
        "sig": "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE",
        "dims": {"gas_hc": (300, 20000), "gas_co": (3.0, 15), "gas_co2": (0, 14), "gas_o2": (0, 0.3), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.19; GAS_VOCABULARY §10.2 very_rich",
    },
    # --- §7.20 GDI_HPFP_INTERNAL_SEAL_LEAK ---
    {
        "sig": "GDI_HPFP_INTERNAL_SEAL_LEAK",
        "dims": {"gas_hc": (300, 20000), "gas_co": (3.0, 15), "gas_co2": (0, 14), "gas_o2": (0, 0.3), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.20; GAS_VOCABULARY §10.2 very_rich §3.1 dna_gate (same gas as VAC; differentiated by fuel_delivery_type=GDI)",
    },
    # --- §7.21 WORN_VALVE_SEALS ---
    {
        "sig": "WORN_VALVE_SEALS",
        "dims": {"gas_hc": (75, 250), "gas_co": (0, 0.5), "gas_co2": (11, 14.5), "gas_o2": (0, 0.5), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.21; GAS_VOCABULARY §10.1 minor_inefficiency",
    },
    # --- §7.22 WORN_PISTON_RINGS ---
    {
        "sig": "WORN_PISTON_RINGS",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.5), "gas_co2": (14.5, 16), "gas_o2": (0, 0.5), "gas_nox": (0, 100)},
        "src": "GAS_WIKI §7.22; GAS_VOCABULARY §10.1-10.5",
    },
    # --- §7.23 POA_SIGNATURE (catch-all) ---
    {
        "sig": "POA_SIGNATURE",
        "dims": {"gas_hc": (500, 20000), "gas_co": (0, 15), "gas_co2": (0, 14.5), "gas_o2": (0, 22), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.23; GAS_VOCABULARY §10.1 severe_misfire",
    },
    # --- CAM_TIMING_RETARDED_MAP (gas bounds TBD — use envelope) ---
    {
        "sig": "CAM_TIMING_RETARDED_MAP",
        "dims": dict(_ENVELOPE),
        "src": "GAS_VOCABULARY §3 (bounds not yet documented in wiki; using measurement envelope)",
    },
    # --- CAM_TIMING_RETARDED_MAF (gas bounds TBD — use envelope) ---
    {
        "sig": "CAM_TIMING_RETARDED_MAF",
        "dims": dict(_ENVELOPE),
        "src": "GAS_VOCABULARY §3 (bounds not yet documented in wiki; using measurement envelope)",
    },
    # --- CAM_TIMING_ADVANCED (gas bounds TBD — use envelope) ---
    {
        "sig": "CAM_TIMING_ADVANCED",
        "dims": dict(_ENVELOPE),
        "src": "GAS_VOCABULARY §3 (bounds not yet documented in wiki; using measurement envelope)",
    },
    # --- §7.25 EGR_STUCK_CLOSED (same gas as HCT; differentiated by DNA) ---
    {
        "sig": "EGR_STUCK_CLOSED",
        "dims": {"gas_hc": (0, 100), "gas_co": (0, 0.5), "gas_co2": (13, 16), "gas_o2": (0, 0.5), "gas_nox": (1000, 5000)},
        "src": "GAS_WIKI §7.25; GAS_VOCABULARY §10.5 high_combustion_temp §3.1 dna_gate (same gas as HCT; differentiated by egr_equipped=True)",
    },
    # --- §7.26 EGR_STUCK_OPEN ---
    {
        "sig": "EGR_STUCK_OPEN",
        "dims": {"gas_hc": (100, 20000), "gas_co": (0.5, 15), "gas_co2": (0, 14), "gas_o2": (0, 2.0), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.26; GAS_VOCABULARY §10.1-10.5 §3.1 dna_gate",
    },
    # --- §7.27 VVT_FAILURE (catch-all for elevated nox) ---
    {
        "sig": "VVT_FAILURE",
        "dims": {"gas_hc": (0, 500), "gas_co": (0, 15), "gas_co2": (0, 22), "gas_o2": (0, 22), "gas_nox": (500, 5000)},
        "src": "GAS_WIKI §7.27; GAS_VOCABULARY §10.5 elevated_idle",
    },
    # --- §7.28 EVAP_CANISTER_SATURATED ---
    {
        "sig": "EVAP_CANISTER_SATURATED",
        "dims": {"gas_hc": (100, 500), "gas_co": (0.5, 3.0), "gas_co2": (0, 13), "gas_o2": (0, 0.5), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.28; GAS_VOCABULARY §10.2 mild_rich",
    },
    # --- §7.29 EGR_DILUTION_MISFIRE (unreachable in v1 — audit AF-2) ---
    {
        "sig": "EGR_DILUTION_MISFIRE",
        "dims": {"gas_hc": (500, 20000), "gas_co": (0, 15), "gas_co2": (0, 14.5), "gas_o2": (0, 22), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.29 (unreachable in v1 — requires DTC evidence; audit AF-2)",
    },
    # --- §7.30 INCOMPLETE_OXIDATION ---
    {
        "sig": "INCOMPLETE_OXIDATION",
        "dims": {"gas_hc": (200, 20000), "gas_co": (0.5, 15), "gas_co2": (0, 13), "gas_o2": (0, 22), "gas_nox": (0, 5000)},
        "src": "GAS_WIKI §7.30; GAS_VOCABULARY §10.1-10.5",
    },
    # --- INCOMPLETE_COMBUSTION (bounds TBD — use envelope) ---
    {
        "sig": "INCOMPLETE_COMBUSTION",
        "dims": dict(_ENVELOPE),
        "src": "GAS_VOCABULARY §3 (bounds not yet documented in wiki; using measurement envelope)",
    },
    # --- COOLANT_LEAK_INTERNAL (bounds TBD — use envelope) ---
    {
        "sig": "COOLANT_LEAK_INTERNAL",
        "dims": dict(_ENVELOPE),
        "src": "GAS_VOCABULARY §3 (bounds not yet documented in wiki; using measurement envelope)",
    },
]


def build_gaslab_descriptor() -> ModuleDescriptor:
    """Build a ModuleDescriptor for the GASLab fork."""
    from gaslab import GasLabContext, process
    from gaslab.contracts import EngineStateBucket, GasReading
    from gaslab.dna_view import GasLabDnaView

    # --- Field ranges ---
    fields = [
        FieldRange("gas_hc", "int", 0, 20000),
        FieldRange("gas_co", "float", 0.0, 15.0),
        FieldRange("gas_co2", "float", 0.0, 22.0),
        FieldRange("gas_o2", "float", 0.0, 22.0),
        FieldRange("gas_nox", "int", 0, 5000),
        FieldRange("ctx_engine_state", "str", enum_values=[e.value for e in EngineStateBucket]),
        FieldRange("ctx_secondary_air_injection_active", "bool"),
        FieldRange("ctx_lambda_measured", "Optional[float]", 0.5, 2.0),
        FieldRange("ctx_block_test_passed", "bool"),
        FieldRange("dna_engine_displacement_liters", "float", 0.1, 10.0),
        FieldRange("dna_cylinder_count", "int", 1, 16),
        FieldRange("dna_number_of_banks", "int", 1, 4),
        FieldRange("dna_euro_emission_category", "str"),
        FieldRange("dna_fuel_delivery_type", "str"),
        FieldRange("dna_induction_type", "str"),
        FieldRange("dna_upstream_o2_type", "str"),
        FieldRange("dna_secondary_air_equipped", "bool"),
        FieldRange("dna_has_catalyst", "bool"),
        FieldRange("dna_egr_equipped", "bool"),
        FieldRange("dna_target_lambda_v112", "Optional[float]", 0.5, 2.5),
        FieldRange("dna_co_low_idle", "Optional[float]", 0.0, 15.0),
        FieldRange("dna_co_high_idle", "Optional[float]", 0.0, 15.0),
        FieldRange("dna_confidence", "str"),
    ]

    # --- Box table ---
    boxes: dict[str, FaultBox] = {}
    for bd in _BOX_DEFS:
        boxes[bd["sig"]] = FaultBox(
            signature=bd["sig"],
            dimensions=bd["dims"],
            source=bd["src"],
        )

    # --- Row parser helpers (mirror gaslab_suite_runner.py) ---
    BASIC_DNA_DEFAULTS = {
        "engine_displacement_liters": 1.6,
        "cylinder_count": 4,
        "number_of_banks": 1,
        "euro_emission_category": "EURO_4",
        "fuel_delivery_type": "NON_GDI",
        "induction_type": "NATURALLY_ASPIRATED",
        "upstream_o2_type": "NARROWBAND_0_TO_1V",
        "has_catalyst": True,
        "egr_equipped": False,
        "target_lambda_v112": None,
        "co_low_idle": None,
        "co_high_idle": None,
        "confidence": "NONE",
    }

    def _parse_float(raw: str) -> float | None:
        s = raw.strip()
        return None if s == "" else float(s)

    def _parse_bool(raw: str) -> bool:
        s = raw.strip()
        if s == "True":
            return True
        if s == "False":
            return False
        raise ValueError(f"Invalid boolean value: {raw!r}")

    def _build_dna(row: dict[str, str]) -> GasLabDnaView:
        if "dna_has_catalyst" not in row:
            return GasLabDnaView(**BASIC_DNA_DEFAULTS)
        return GasLabDnaView(
            engine_displacement_liters=float(row["dna_engine_displacement_liters"]),
            cylinder_count=int(row["dna_cylinder_count"]),
            number_of_banks=int(row["dna_number_of_banks"]),
            euro_emission_category=row["dna_euro_emission_category"],
            fuel_delivery_type=row["dna_fuel_delivery_type"],
            induction_type=row["dna_induction_type"],
            upstream_o2_type=row["dna_upstream_o2_type"],
            has_catalyst=_parse_bool(row["dna_has_catalyst"]),
            egr_equipped=_parse_bool(row["dna_egr_equipped"]),
            target_lambda_v112=_parse_float(row.get("dna_target_lambda_v112", "")),
            co_low_idle=_parse_float(row.get("dna_co_low_idle", "")),
            co_high_idle=_parse_float(row.get("dna_co_high_idle", "")),
            confidence=row.get("dna_confidence", "").strip() or "NONE",
        )

    def build_args(row: dict[str, str]) -> tuple:
        reading = GasReading(
            hc=int(row["gas_hc"]),
            co=float(row["gas_co"]),
            co2=float(row["gas_co2"]),
            o2=float(row["gas_o2"]),
            nox=int(row["gas_nox"]),
        )
        dna = _build_dna(row)
        block_test_passed = _parse_bool(row.get("ctx_block_test_passed", "") or "False")
        if "ctx_engine_state" not in row:
            context = GasLabContext(
                dna=dna,
                engine_state=EngineStateBucket.STABILIZED_IDLE,
                lambda_measured=_parse_float(row.get("ctx_lambda_measured", "")),
                block_test_passed=block_test_passed,
            )
        else:
            context = GasLabContext(
                dna=dna,
                engine_state=EngineStateBucket(row["ctx_engine_state"]),
                lambda_measured=_parse_float(row.get("ctx_lambda_measured", "")),
                block_test_passed=block_test_passed,
            )
        return (reading, context)

    def extract_expected(row: dict[str, str]) -> dict[str, Any]:
        return {
            "chemical_state": row.get("expected_chemical_state", "").strip(),
            "lambda_chem": row.get("expected_lambda_chem", "").strip(),
            "sample_validity": row.get("expected_sample_validity", "").strip(),
            "error": row.get("expected_error", "").strip(),
        }

    def diff(actual: Any, expected: dict[str, Any]) -> list[str]:
        mismatches: list[str] = []
        if expected["chemical_state"] and actual.chemical_state.value != expected["chemical_state"]:
            mismatches.append(
                f"chemical_state: expected={expected['chemical_state']}, "
                f"actual={actual.chemical_state.value}"
            )
        if expected["lambda_chem"]:
            exp_lam = float(expected["lambda_chem"])
            if abs(actual.lambda_chem - exp_lam) > 0.001:
                mismatches.append(
                    f"lambda_chem: expected={exp_lam}, actual={actual.lambda_chem}"
                )
        if expected["sample_validity"] and actual.sample_validity.value != expected["sample_validity"]:
            mismatches.append(
                f"sample_validity: expected={expected['sample_validity']}, "
                f"actual={actual.sample_validity.value}"
            )
        return mismatches

    return ModuleDescriptor(
        name="GASLab",
        fields=fields,
        boxes=boxes,
        build_args=build_args,
        entry_point=process,
        extract_expected=extract_expected,
        diff=diff,
    )
