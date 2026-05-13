"""Build label_aliases.yaml for T-P1-6.
Maps every V1 node ID → V2 ID (or null), plus the 10 timing/compression/VVT
aliases from timing_compression_forensic.md.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
V1_NODES = ROOT / "schema" / "v1_reference" / "nodes.yaml"
V2_SYMPTOMS = ROOT / "schema" / "v2" / "symptoms.yaml"
V2_FAULTS = ROOT / "schema" / "v2" / "faults.yaml"
OUT = ROOT / "schema" / "v2" / "label_aliases.yaml"

# source: timing_compression_forensic.md §"What's needed to fix both families"
FORENSIC_TIMING = {
    "Cam_Timing_Retard":                    ("Cam_Timing_Retard_Late", "Renamed for specificity in V2 schema"),
    "VVT_Phaser_Sludge_Lag":               ("Cam_Timing_Retard_Late", "V1 CSV case expected node; aliased to closest V2 fault"),
    "VVT_Solenoid_Resistance_Drift":       ("Cam_Timing_Retard_Late", "V1 CSV case expected node; aliased to closest V2 fault"),
    "Cam_Timing_Retard_VVT_Phaser_Lag":    ("Cam_Timing_Retard_Late", "V1 CSV case expected node; aliased to closest V2 fault"),
    "Cam_Timing_Advance_VVT_Phaser_Stuck": ("Cam_Timing_Retard_Late", "V1 CSV case expected node; aliased to closest V2 fault"),
    "VVT_Phaser_Lag_HC_Rises_Under_Load":  ("Cam_Timing_Retard_Late", "V1 CSV case expected node; aliased to closest V2 fault"),
    "vvt_fault":                           ("Cam_Timing_Retard_Late", "V1 CSV case expected node; aliased to closest V2 fault"),
}

FORENSIC_COMPRESSION = {
    "Low_Compression_Multi_Cylinder":                                  ("Worn_Piston_Rings", "T15d schema collapse removed node; aliased to closest V2 fault"),
    "Mechanical_Wear_Low_Compression_Multi_Cylinder_FF_HighLoad":      ("Worn_Piston_Rings", "V1 CSV annotation; aliased to closest V2 fault"),
    "Mechanical_Wear_Worn_Piston_Rings_FF_Idle":                       ("Worn_Piston_Rings", "V1 CSV annotation; aliased to closest V2 fault"),
}

def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}

def main() -> None:
    v1 = load_yaml(V1_NODES)
    v2_symptoms = set(load_yaml(V2_SYMPTOMS).keys())
    v2_faults = set(load_yaml(V2_FAULTS).keys())
    v2_all = v2_symptoms | v2_faults

    aliases: dict[str, dict] = {}

    # --- Pass 1: V1 nodes from nodes.yaml ---
    for node in v1.get("nodes", []):
        vid = node["id"]
        ntype = node.get("node_type", "fault")

        if vid in v2_all:
            continue  # exact match, no alias needed

        if ntype == "symptom":
            # V1 symptom → SYM_ prefix
            sym_id = "SYM_" + vid.upper()
            if sym_id in v2_symptoms:
                if vid != sym_id:
                    aliases[vid] = {
                        "target": sym_id,
                        "reason": f"V1 symptom ID migrated to V2 {sym_id}"
                    }
                continue
            # fallback: try common variations
            for candidate in v2_symptoms:
                if candidate == "SYM_" + vid.upper():
                    aliases[vid] = {"target": candidate, "reason": f"V1 symptom → V2 {candidate}"}
                    break
            else:
                print(f"WARNING: V1 symptom '{vid}' has no V2 SYM_ match")

        else:  # fault
            # Try PascalCase conversion
            pascal = "".join(word.capitalize() for word in vid.split("_"))
            if pascal in v2_faults:
                aliases[vid] = {
                    "target": pascal,
                    "reason": f"V1 snake_case fault ID migrated to V2 {pascal}"
                }
                continue

            # Try known renames
            found = False
            # Check case-insensitive match in V2 faults
            for v2f in v2_faults:
                if vid.upper() == v2f.upper():
                    aliases[vid] = {
                        "target": v2f,
                        "reason": f"V1 fault ID case-normalized to V2 {v2f}"
                    }
                    found = True
                    break

            if not found:
                # Check if it's a V1 PascalCase that doesn't match V2
                for v2f in v2_faults:
                    if v2f.upper() == vid.upper():
                        aliases[vid] = {
                            "target": v2f,
                            "reason": f"V1 fault ID case-normalized to V2 {v2f}"
                        }
                        found = True
                        break

            if not found:
                print(f"WARNING: V1 fault '{vid}' has no V2 match (pascal='{pascal}')")

    # --- Pass 2: Known renames that aren't simple case transforms ---
    known_renames = {
        # V1 snake_case → V2 PascalCase (non-obvious)
        "exhaust_leak":        ("Exhaust_Air_Leak_Pre_Cat", "V1 exhaust_leak family → V2 specific child fault"),
        "late_ignition_timing":("Ignition_Timing_Fault", "V1 late_ignition_timing → V2 Ignition_Timing_Fault family"),
        "mechanical_wear":     ("Mechanical_Fault", "V1 mechanical_wear → V2 Mechanical_Fault family"),
        "induction_issue":     ("Induction_Airflow_Fault", "V1 induction_issue → V2 Induction_Airflow_Fault family"),
        "fuel_delivery":       ("Fuel_Delivery_Low", "V1 fuel_delivery family → V2 Fuel_Delivery_Low"),
        "low_fuel_delivery":   ("Fuel_Delivery_Low", "V1 low_fuel_delivery merged into V2 Fuel_Delivery_Low"),
        "head_gasket":         ("Head_Gasket_Failure", "V1 head_gasket family → V2 Head_Gasket_Failure"),
        "Lazy_O2_Sensor_Aging":("Lazy_O2_Sensor", "V1 Lazy_O2_Sensor_Aging renamed to V2 Lazy_O2_Sensor"),
        "Mechanical_Lean_Vacuum_Leak": ("Vacuum_Leak_Intake", "V1 Mechanical_Lean_Vacuum_Leak renamed to V2 Vacuum_Leak_Intake"),
        "vacuum_leak":         ("Vacuum_Leak_Intake", "V1 vacuum_leak merged into V2 Vacuum_Leak_Intake"),
        "Mechanical_Misfire_Spark_Plug": ("Spark_Plug_Worn", "V1 Mechanical_Misfire_Spark_Plug renamed to V2 Spark_Plug_Worn"),
        "Worn_Piston_Rings_Valve_Seals": ("Worn_Piston_Rings", "V1 Worn_Piston_Rings_Valve_Seals renamed to V2 Worn_Piston_Rings"),
        "egr_stuck_open_idle": ("EGR_Stuck_Open", "V1 egr_stuck_open_idle merged into V2 EGR_Stuck_Open"),
        "stuck_egr_open":     ("EGR_Stuck_Open", "V1 stuck_egr_open → V2 EGR_Stuck_Open"),
        "stuck_egr_open_confirmed": ("EGR_Stuck_Open_Confirmed", "V1 stuck_egr_open_confirmed → V2 EGR_Stuck_Open_Confirmed"),
        "head_gasket_failure_combustion_to_coolant": ("Head_Gasket_Combustion_To_Coolant", "V1 full name → V2 Head_Gasket_Combustion_To_Coolant"),
        "head_gasket_failure_cyl_to_cyl": ("Head_Gasket_Cylinder_To_Cylinder", "V1 full name → V2 Head_Gasket_Cylinder_To_Cylinder"),
        "ns_ckp_failure":     ("NS_CKP_Sensor_Failure", "V1 ns_ckp_failure → V2 NS_CKP_Sensor_Failure"),
        "ecu_logic_inversion_fault": ("ECU_Logic_Inversion", "V1 ecu_logic_inversion_fault → V2 ECU_Logic_Inversion"),
    }

    for old_id, (new_id, reason) in known_renames.items():
        if old_id not in aliases:
            aliases[old_id] = {"target": new_id, "reason": reason}

    # Override with forensic-specified targets where they differ
    forensic_overrides = {
        "Low_Compression_Multi_Cylinder": FORENSIC_COMPRESSION["Low_Compression_Multi_Cylinder"],
    }
    for old_id, (new_id, reason) in forensic_overrides.items():
        aliases[old_id] = {"target": new_id, "reason": reason}

    # --- Pass 3: Forensic timing aliases ---
    for old_id, (new_id, reason) in FORENSIC_TIMING.items():
        if old_id not in aliases:
            aliases[old_id] = {"target": new_id, "reason": reason}

    # --- Pass 4: Forensic compression aliases ---
    for old_id, (new_id, reason) in FORENSIC_COMPRESSION.items():
        if old_id not in aliases:
            aliases[old_id] = {"target": new_id, "reason": reason}

    # --- Pass 5: Known removals (null target) ---
    null_aliases = {
        "Healthy_Engine": "L19: no pseudo-fault; engine returns insufficient_evidence instead",
        "clean_gas": "V1 legacy tag; replaced by SYM_GASES_NORMAL + insufficient_evidence state",
    }
    for old_id, reason in null_aliases.items():
        if old_id not in aliases:
            aliases[old_id] = {"target": None, "reason": reason}

    # --- Validate ---
    errors = []
    for old_id, entry in aliases.items():
        target = entry["target"]
        if target is not None and target not in v2_all:
            errors.append(f"UNRESOLVED: '{old_id}' → '{target}' does not exist in V2 schema")

    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  {e}")
        raise SystemExit(1)

    # --- Write output ---
    header = f"""# V2 label_aliases.yaml — T-P1-6
# Generated {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
# Maps V1 node IDs → V2 schema IDs (symptoms.yaml, faults.yaml, root_causes.yaml).
# target: null means the node was intentionally removed with no replacement.
# Closes L09: every removed/renamed node must have an alias entry.
#
# Sources:
#   V1 nodes: schema/v1_reference/nodes.yaml ({len(v1.get('nodes', []))} nodes)
#   V2 symptoms: schema/v2/symptoms.yaml ({len(v2_symptoms)} entries)
#   V2 faults: schema/v2/faults.yaml ({len(v2_faults)} entries)
#   Forensic: 02_inputs/lessons/timing_compression_forensic.md (10 VVT/compression aliases)
#   T-P0-5/T-P0-6: corpus case expected_fault references
#
# Total aliases: {len(aliases)}
# Null-target (removed): {sum(1 for a in aliases.values() if a['target'] is None)}
# Active remaps: {sum(1 for a in aliases.values() if a['target'] is not None)}
"""

    lines = [header]
    for old_id in sorted(aliases.keys(), key=str.lower):
        entry = aliases[old_id]
        target = entry["target"]
        reason = entry["reason"]
        if target is None:
            lines.append(f"{old_id}:")
            lines.append("  target: null")
            lines.append(f"  reason: \"{reason}\"")
        else:
            lines.append(f"{old_id}:")
            lines.append(f"  target: {target}")
            lines.append(f"  reason: \"{reason}\"")
        lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {len(aliases)} aliases to {OUT}")
    print(f"  Active: {sum(1 for a in aliases.values() if a['target'] is not None)}")
    print(f"  Null:   {sum(1 for a in aliases.values() if a['target'] is None)}")
    print("Validation PASSED")

if __name__ == "__main__":
    main()
