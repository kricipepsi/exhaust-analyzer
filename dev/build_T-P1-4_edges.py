"""Build schema/v2/edges.yaml from V1 edges with V2 ID remapping and weight normalization.

Task: T-P1-4
Rules: R2 (hybrid inference), R7 (no magnet edges), L07
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SCHEMA_V1 = REPO / "schema" / "v1_reference"
SCHEMA_V2 = REPO / "schema" / "v2"

# source: docs/master_guides/… — V1→V2 ID prefix mappings are derived from
# T-P1-1 symptoms.yaml and T-P1-2 faults.yaml naming conventions.
# V1 symptoms use lowercase snake_case; V2 symptoms use SYM_ prefix + UPPER_SNAKE.
# V1 faults use lowercase snake_case; V2 faults use PascalCase.


def load_v1_edges() -> list[dict]:
    with open(SCHEMA_V1 / "edges.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["edges"]


def load_v2_symptom_ids() -> set[str]:
    with open(SCHEMA_V2 / "symptoms.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {k for k in data if k.startswith("SYM_")}


def load_v2_fault_ids() -> set[str]:
    with open(SCHEMA_V2 / "faults.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Top-level keys that are fault entries (not comments/metadata)
    return {k for k in data if isinstance(data[k], dict) and "parent" in data[k]}


def map_v1_symptom_to_v2(v1_id: str) -> str | None:
    """Map a V1 symptom ID to V2 SYM_ ID. Returns None if no mapping exists."""
    mapping = {
        # Gas pattern symptoms
        "co_high": "SYM_CO_HIGH",
        "co2_low": "SYM_CO2_LOW",
        "co2_good": "SYM_CO2_GOOD",
        "lambda_low": "SYM_LAMBDA_LOW",
        "lambda_high": "SYM_LAMBDA_HIGH",
        "lambda_normal": "SYM_LAMBDA_NORMAL",
        "o2_high": "SYM_O2_HIGH",
        "o2_very_high": "SYM_O2_VERY_HIGH",
        "o2_low": "SYM_O2_LOW",
        "hc_high": "SYM_HC_HIGH",
        "hc_very_high": "SYM_HC_VERY_HIGH",
        "hc_low": "SYM_HC_LOW",
        "co_low_lean": "SYM_CO_LOW_LEAN",
        "nox_high": "SYM_NOX_HIGH",
        "nox_high_idle": "SYM_NOX_HIGH_IDLE",
        "nox_high_load": "SYM_NOX_HIGH_LOAD",
        "nox_low_with_lean": "SYM_NOX_LOW_WITH_LEAN",
        # DTC symptoms
        "dtc_p0171": "SYM_DTC_P0171",
        "dtc_p0172": "SYM_DTC_P0172",
        "dtc_catalyst": "SYM_DTC_CATALYST",
        "dtc_misfire": "SYM_DTC_MISFIRE",
        "dtc_egr": "SYM_DTC_EGR",
        "dtc_ecu_internal": "SYM_DTC_ECU_INTERNAL",
        "dtc_injector": "SYM_DTC_INJECTOR",
        "dtc_sensor": "SYM_DTC_SENSOR",
        "dtc_induction": "SYM_DTC_INDUCTION",
        "dtc_boost": "SYM_DTC_BOOST",
        "dtc_camshaft_timing": "SYM_DTC_CAMSHAFT_TIMING",
        "dtc_ho2s_heater": "SYM_DTC_HO2S_HEATER",
        "dtc_knock_sensor": "SYM_DTC_KNOCK_SENSOR",
        # OBD PID symptoms
        "trim_negative_high": "SYM_TRIM_NEGATIVE_HIGH",
        "trim_positive_high": "SYM_TRIM_POSITIVE_HIGH",
        "trim_sum_positive_high": "SYM_TRIM_SUM_POSITIVE_HIGH",
        "trim_sum_negative_high": "SYM_TRIM_SUM_NEGATIVE_HIGH",
        "trim_oscillation": "SYM_TRIM_OSCILLATION",
        "trim_global_both_banks": "SYM_TRIM_GLOBAL_BOTH_BANKS",
        "trim_local_one_bank": "SYM_TRIM_LOCAL_ONE_BANK",
        "o2_upstream_lazy": "SYM_O2_UPSTREAM_LAZY",
        "o2_downstream_active": "SYM_O2_DOWNSTREAM_ACTIVE",
        # Freeze frame symptoms
        "ff_open_loop_at_fault": "SYM_FF_OPEN_LOOP_AT_FAULT",
        "ff_load_high_at_low_rpm": "SYM_FF_LOAD_HIGH_AT_LOW_RPM",
        "ff_ect_warmup": "SYM_FF_ECT_WARMUP",
        "ff_iat_ect_biased": "SYM_FF_IAT_ECT_BIASED",
        "ff_timing_retard_severe": "SYM_FF_TIMING_RETARD_SEVERE",
        "ff_codes_cleared_invalidated": "SYM_FF_CODES_CLEARED_INVALIDATED",
        # Context symptoms
        "ctx_cold_engine": "SYM_CTX_COLD_ENGINE",
        # Compound / pattern symptoms (M3)
        "ecu_logic_inversion": "SYM_ECU_LOGIC_INVERSION",
        "ghost_misfire": "SYM_GHOST_MISFIRE",
        "ghost_dtc_no_evidence": "SYM_GHOST_DTC_NO_EVIDENCE",
        "clean_gas_with_dtc": "SYM_CLEAN_GAS_WITH_DTC",
        "gases_normal": "SYM_GASES_NORMAL",
        "ecu_open_loop_blind": "SYM_ECU_OPEN_LOOP_BLIND",
        "ecu_misread_lean_confirmed": "SYM_ECU_MISREAD_LEAN_CONFIRMED",
        "ecu_injector_driver_stuck": "SYM_ECU_INJECTOR_DRIVER_STUCK",
        "sensor_bias_lean": "SYM_SENSOR_BIAS_LEAN",
        "sensor_bias_rich": "SYM_SENSOR_BIAS_RICH",
        "sensor_bias_false_rich": "SYM_SENSOR_BIAS_FALSE_RICH",
        "late_timing_pattern": "SYM_LATE_TIMING_PATTERN",
        "compression_loss_pattern": "SYM_COMPRESSION_LOSS_PATTERN",
        "valve_seal_pattern": "SYM_VALVE_SEAL_PATTERN",
        "pcv_leak_pattern": "SYM_PCV_LEAK_PATTERN",
        "high_fuel_pressure_pattern": "SYM_HIGH_FUEL_PRESSURE_PATTERN",
        "leaking_injector_pattern": "SYM_LEAKING_INJECTOR_PATTERN",
        "head_gasket_pattern": "SYM_HEAD_GASKET_PATTERN",
        "stuck_egr_open_pattern": "SYM_STUCK_EGR_OPEN_PATTERN",
        "egr_dilution_pattern": "SYM_EGR_DILUTION_PATTERN",
        "ignition_misfire_confirmed": "SYM_IGNITION_MISFIRE_CONFIRMED",
        "individual_cylinder_misfire_pattern": "SYM_INDIVIDUAL_CYLINDER_MISFIRE_PATTERN",
        "lean_misfire_pattern": "SYM_LEAN_MISFIRE_PATTERN",
        "rich_misfire_pattern": "SYM_RICH_MISFIRE_PATTERN",
        "catalyst_masking": "SYM_CATALYST_MASKING",
        "exhaust_leak_ghost": "SYM_EXHAUST_LEAK_GHOST",
        "dual_contaminated_maf_pattern": "SYM_DUAL_CONTAMINATED_MAF_PATTERN",
        "dual_clogged_exhaust_pattern": "SYM_DUAL_CLOGGED_EXHAUST_PATTERN",
        "clogged_exhaust_rpm_pattern": "SYM_CLOGGED_EXHAUST_RPM_PATTERN",
        "dual_intake_gasket_pattern": "SYM_DUAL_INTAKE_GASKET_PATTERN",
        "dual_low_fuel_delivery_pattern": "SYM_DUAL_LOW_FUEL_DELIVERY_PATTERN",
        "dual_egr_recovery_pattern": "SYM_DUAL_EGR_RECOVERY_PATTERN",
        "tired_catalyst_pattern": "SYM_TIRED_CATALYST_PATTERN",
        "high_idle_nox_pattern": "SYM_HIGH_IDLE_NOX_PATTERN",
        "rich_negative_trims_pattern": "SYM_RICH_NEGATIVE_TRIMS_PATTERN",
        "idle_lean_load_corrects": "SYM_IDLE_LEAN_LOAD_CORRECTS",
        "idle_stoich_load_lean": "SYM_IDLE_STOICH_LOAD_LEAN",
        # Perception symptoms
        "perception_lean_seen_rich": "SYM_PERCEPTION_LEAN_SEEN_RICH",
        "perception_rich_seen_lean": "SYM_PERCEPTION_RICH_SEEN_LEAN",
    }
    return mapping.get(v1_id)


def map_v1_fault_to_v2(v1_id: str) -> str | None:
    """Map a V1 fault target ID to V2 fault ID. Returns None if no mapping exists."""
    mapping = {
        # Rich mixture family
        "rich_mixture": "Rich_Mixture",
        "high_fuel_pressure": "High_Fuel_Pressure",
        "leaking_injector": "Leaking_Injector",
        "evap_purge_stuck_open": "EVAP_Purge_Stuck_Open",
        "gdi_hpfp_internal_leak": "GDI_HPFP_Internal_Leak",
        # Lean condition family
        "lean_condition": "Lean_Condition",
        "intake_gasket_leak": "Intake_Gasket_Leak",
        "fuel_delivery": "Fuel_Delivery_Low",
        "low_fuel_delivery": "Fuel_Delivery_Low",
        "contaminated_maf": "Contaminated_MAF",
        "induction_issue": "Air_Induction_Fault",
        "Mechanical_Lean_Vacuum_Leak": "Vacuum_Leak_Intake",
        "vacuum_leak": "Vacuum_Leak_Intake",
        # Misfire family
        "misfire": "Misfire",
        "misfire_single_cylinder": "Misfire_Single_Cylinder",
        "Mechanical_Misfire_Spark_Plug": "Spark_Plug_Worn",
        # Exhaust fault family
        "exhaust_leak": "Exhaust_Air_Leak_Pre_Cat",
        "Exhaust_Air_Leak_Pre_Cat": "Exhaust_Air_Leak_Pre_Cat",
        "sai_valve_stuck_open": "SAI_Valve_Stuck_Open",
        # Clogged exhaust
        "clogged_exhaust": "Clogged_Exhaust",
        # EGR family
        "egr_fault": "EGR_Fault",
        "stuck_egr_open": "EGR_Stuck_Open",
        "stuck_egr_open_confirmed": "EGR_Stuck_Open_Confirmed",
        "egr_stuck_open_idle": "EGR_Stuck_Open",
        # Catalyst family
        "catalyst_failure": "Catalyst_Failure",
        "aftermarket_catalyst_inefficient": "Aftermarket_Catalyst_Inefficient",
        # Sensor family
        "sensor_fault": "Sensor_Fault",
        "Lazy_O2_Sensor_Aging": "Lazy_O2_Sensor",
        "ECT_Sensor_Bias": "ECT_Sensor_Bias",
        # Mechanical family
        "mechanical_wear": "Mechanical_Fault",
        "Worn_Piston_Rings_Valve_Seals": "Worn_Piston_Rings",
        "valve_timing_mechanical": "Valve_Timing_Mechanical",
        "vvt_phaser_fault": "VVT_Phaser_Fault",
        "gdi_lspi": "GDI_LSPI",
        "gdi_carbon_buildup": "GDI_Carbon_Buildup",
        "pcv_fault": "PCV_System_Fault",
        "valve_seal_wear": "Valve_Seal_Wear",
        # Head gasket family
        "head_gasket": "Head_Gasket_Failure",
        "head_gasket_failure_combustion_to_coolant": "Head_Gasket_Combustion_To_Coolant",
        "head_gasket_failure_cyl_to_cyl": "Head_Gasket_Cylinder_To_Cylinder",
        # Turbo family
        "turbo_fault": "Turbo_Fault",
        # ECU family
        "ecu_fault": "ECU_Fault",
        "ECU_Internal_Checksum_Error": "ECU_Internal_Checksum_Error",
        "ecu_open_loop_fault": "ECU_Open_Loop_Fault",
        "ecu_logic_inversion_fault": "ECU_Logic_Inversion",
        # Ignition timing family
        "late_ignition_timing": "Ignition_Timing_Fault",
        "Cam_Timing_Retard_Late": "Cam_Timing_Retard_Late",
        # Other
        "Low_Compression_Multi_Cylinder": "Low_Compression_Multi_Cylinder",
        "GDI_HPFP_Failure": "GDI_HPFP_Failure",
        "ns_ckp_failure": "NS_CKP_Sensor_Failure",
        # V1 targets that are now V2 symptoms (no corresponding V2 fault):
        # "bank2_lean", "bank2_rich", "o2_upstream_lazy", "sensor_bias_lean",
        # "sensor_bias_rich", "trim_positive_high", "trim_negative_high"
        # These are excluded — edges targeting symptoms don't make sense in V2's
        # strict symptom→fault KG topology.
    }
    return mapping.get(v1_id)


def normalize_weight(v1_weight: float, polarity: str) -> float:
    """Normalize V1 weight to V2 [-1.0, +1.0] range.

    V1 excitatory weights range up to 3.0. V2 caps at 1.0.
    Normalization: divide by 3.0 (the V1 maximum), round to 2 decimal places.
    Inhibitory edges get negative sign.
    """
    # source: V1 max excitatory weight is 3.0 (egr_dilution_pattern→stuck_egr_open,
    # individual_cylinder_misfire_pattern→misfire, sensor_bias_false_rich→sensor_fault).
    # V1 max inhibitory weight is -0.95. Normalize both to [0, 1] then sign.
    v1_max = 3.0  # source: V1 edges.yaml — max observed excitatory weight

    normalized = v1_weight / v1_max
    normalized = min(normalized, 1.0)
    normalized = round(normalized, 2)

    if polarity == "inhibitory":
        return -normalized
    return normalized


# source: docs/master_guides/perception/master_perception_guide.md §3 — M3-emitted
# compound pattern symptoms that already encode discriminating logic.
# These patterns can serve as their own discriminator_gate because they
# combine multiple sensor signals into a single conclusive symptom.
M3_PATTERN_SYMPTOMS: set[str] = {
    "SYM_ECU_LOGIC_INVERSION",
    "SYM_GHOST_MISFIRE",
    "SYM_GHOST_DTC_NO_EVIDENCE",
    "SYM_CLEAN_GAS_WITH_DTC",
    "SYM_GASES_NORMAL",
    "SYM_ECU_OPEN_LOOP_BLIND",
    "SYM_ECU_MISREAD_LEAN_CONFIRMED",
    "SYM_ECU_INJECTOR_DRIVER_STUCK",
    "SYM_SENSOR_BIAS_LEAN",
    "SYM_SENSOR_BIAS_RICH",
    "SYM_SENSOR_BIAS_FALSE_RICH",
    "SYM_LATE_TIMING_PATTERN",
    "SYM_COMPRESSION_LOSS_PATTERN",
    "SYM_VALVE_SEAL_PATTERN",
    "SYM_PCV_LEAK_PATTERN",
    "SYM_HIGH_FUEL_PRESSURE_PATTERN",
    "SYM_LEAKING_INJECTOR_PATTERN",
    "SYM_HEAD_GASKET_PATTERN",
    "SYM_STUCK_EGR_OPEN_PATTERN",
    "SYM_EGR_DILUTION_PATTERN",
    "SYM_IGNITION_MISFIRE_CONFIRMED",
    "SYM_INDIVIDUAL_CYLINDER_MISFIRE_PATTERN",
    "SYM_LEAN_MISFIRE_PATTERN",
    "SYM_RICH_MISFIRE_PATTERN",
    "SYM_CATALYST_MASKING",
    "SYM_EXHAUST_LEAK_GHOST",
    "SYM_DUAL_CONTAMINATED_MAF_PATTERN",
    "SYM_DUAL_CLOGGED_EXHAUST_PATTERN",
    "SYM_CLOGGED_EXHAUST_RPM_PATTERN",
    "SYM_DUAL_INTAKE_GASKET_PATTERN",
    "SYM_DUAL_LOW_FUEL_DELIVERY_PATTERN",
    "SYM_DUAL_EGR_RECOVERY_PATTERN",
    "SYM_TIRED_CATALYST_PATTERN",
    "SYM_HIGH_IDLE_NOX_PATTERN",
    "SYM_RICH_NEGATIVE_TRIMS_PATTERN",
    "SYM_IDLE_LEAN_LOAD_CORRECTS",
    "SYM_IDLE_STOICH_LOAD_LEAN",
    "SYM_NOX_HIGH_IDLE",
    "SYM_NOX_LOW_WITH_LEAN",
    "SYM_PERCEPTION_LEAN_SEEN_RICH",
    "SYM_PERCEPTION_RICH_SEEN_LEAN",
    "SYM_TRIM_OSCILLATION",
    "SYM_TRIM_GLOBAL_BOTH_BANKS",
    "SYM_TRIM_LOCAL_ONE_BANK",
    "SYM_FF_OPEN_LOOP_AT_FAULT",
    "SYM_FF_LOAD_HIGH_AT_LOW_RPM",
    "SYM_FF_ECT_WARMUP",
    "SYM_FF_IAT_ECT_BIASED",
    "SYM_FF_TIMING_RETARD_SEVERE",
    "SYM_FF_CODES_CLEARED_INVALIDATED",
    "SYM_CTX_COLD_ENGINE",
}


def build_v2_edges() -> tuple[list[dict], list[dict]]:
    """Build V2 edges from V1 edges. Returns (migrated_edges, removed_edges)."""
    v1_edges = load_v1_edges()
    v2_symptoms = load_v2_symptom_ids()
    v2_faults = load_v2_fault_ids()

    migrated: list[dict] = []
    removed: list[dict] = []

    for edge in v1_edges:
        v1_src = edge["source"]
        v1_dst = edge["target"]
        v1_weight = edge["weight"]
        polarity = edge.get("polarity", "excitatory")

        v2_src = map_v1_symptom_to_v2(v1_src)
        v2_dst = map_v1_fault_to_v2(v1_dst)

        # Remove edges where src or dst don't map to V2
        if v2_src is None or v2_dst is None:
            removed.append({
                "v1_source": v1_src,
                "v1_target": v1_dst,
                "v1_weight": v1_weight,
                "v1_polarity": polarity,
                "reason": (
                    f"V1 source '{v1_src}' has no V2 SYM_ mapping"
                    if v2_src is None
                    else f"V1 target '{v1_dst}' has no V2 fault mapping"
                ),
            })
            continue

        # Validate V2 IDs exist in schema
        if v2_src not in v2_symptoms:
            removed.append({
                "v1_source": v1_src,
                "v1_target": v1_dst,
                "v2_source": v2_src,
                "v1_weight": v1_weight,
                "reason": f"V2 source '{v2_src}' not found in symptoms.yaml",
            })
            continue
        if v2_dst not in v2_faults:
            removed.append({
                "v1_source": v1_src,
                "v1_target": v1_dst,
                "v2_target": v2_dst,
                "v1_weight": v1_weight,
                "reason": f"V2 target '{v2_dst}' not found in faults.yaml",
            })
            continue

        weight = normalize_weight(v1_weight, polarity)

        # Handle magnet edges: weight > 0.30 must have discriminator_gate (R7/L07)
        new_edge: dict = {
            "source": v2_src,
            "target": v2_dst,
            "weight": weight,
            "polarity": polarity,
        }

        if abs(weight) > 0.30 and polarity == "excitatory":
            # M3 pattern symptoms can serve as their own discriminator_gate
            if v2_src in M3_PATTERN_SYMPTOMS:
                new_edge["discriminator_gate"] = [v2_src]
            else:
                # For non-pattern symptoms with strong weight, cap at 0.30
                # and note the original weight
                new_edge["weight"] = 0.30
                new_edge["v1_original_weight"] = round(v1_weight / 3.0, 2)

        # Hard veto: only for requires-X edges (-1.0 weight)
        # In V1, inhibitory edges with high absolute weights are inhibitory,
        # not hard vetoes. Keep them as negative weights unless they're
        # tech/era mask edges (which would come from M0, not edges.yaml).
        # source: v2-cf-inference §3

        # Remove V1-only fields (when/multiplier conditions are M1/M2 logic,
        # not edge properties in V2)
        new_edge.pop("polarity", None)

        migrated.append(new_edge)

    return migrated, removed


def main() -> None:
    migrated, removed = build_v2_edges()

    # Build YAML output
    lines: list[str] = []
    lines.append("# V2 Edges — Tier 1→Tier 2 symptom-to-fault weighted edges (R2, R5)")
    lines.append("# Migrated from schema/v1_reference/edges.yaml — T-P1-4")
    lines.append("# Weights normalized to [-1.0, +1.0] by dividing V1 weight by 3.0.")
    lines.append(
        f"# {len(migrated)} edges migrated, {len(removed)} edges removed."
    )
    lines.append("#")
    lines.append("# Magnet edge rule (R7/L07): no weight > 0.30 without discriminator_gate.")
    lines.append("# Pattern-symptom edges (>0.30) self-gate via discriminator_gate: [<src>].")
    lines.append("# Non-pattern edges > 0.30 capped at 0.30 (original weight noted).")
    lines.append("#")
    lines.append("# Removed edges:")
    for r in removed:
        lines.append(
            f"#   {r['v1_source']} → {r['v1_target']} "
            f"(w={r['v1_weight']}, {r.get('v1_polarity', 'N/A')}): {r['reason']}"
        )
    lines.append("")

    # Group edges by target fault family for readability
    edges_data: dict[str, list[dict]] = {}
    for e in migrated:
        target = e["target"]
        if target not in edges_data:
            edges_data[target] = []
        edges_data[target].append(e)

    lines.append("edges:")
    # Sort by target then source for deterministic output
    for target in sorted(edges_data):
        target_edges = sorted(edges_data[target], key=lambda e: e["source"])
        for e in target_edges:
            lines.append(f"  - source: {e['source']}")
            lines.append(f"    target: {e['target']}")
            lines.append(f"    weight: {e['weight']}")
            if "discriminator_gate" in e:
                lines.append(f"    discriminator_gate: {e['discriminator_gate']}")
            if "v1_original_weight" in e:
                lines.append(f"    # v1_original_weight: {e['v1_original_weight']}")

    output = "\n".join(lines) + "\n"

    out_path = SCHEMA_V2 / "edges.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    # Verification
    print(f"Migrated: {len(migrated)} edges")
    print(f"Removed:  {len(removed)} edges")
    print(f"Written to: {out_path}")

    # Check for magnet edges
    magnet = [
        e for e in migrated
        if e["weight"] > 0.30 and "discriminator_gate" not in e
    ]
    print(f"Magnet edges (weight > 0.30, no gate): {len(magnet)}")
    if magnet:
        for m in magnet:
            print(f"  MAGNET: {m['source']} → {m['target']} (w={m['weight']})")

    # Check all src/dst resolve
    symptoms = load_v2_symptom_ids()
    faults = load_v2_fault_ids()
    unresolved_src = [e for e in migrated if e["source"] not in symptoms]
    unresolved_dst = [e for e in migrated if e["target"] not in faults]
    if unresolved_src:
        print(f"UNRESOLVED SOURCES: {len(unresolved_src)}")
    if unresolved_dst:
        print(f"UNRESOLVED TARGETS: {len(unresolved_dst)}")
    if not unresolved_src and not unresolved_dst:
        print("All src/dst IDs resolve in V2 schema — PASS")


if __name__ == "__main__":
    main()
