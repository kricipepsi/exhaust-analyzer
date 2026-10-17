"""D2 probe — BDD scenario -> test traceability (COMLab, GASLab).

Run from the repo root:
    python audit/scratch/D2/d2_bdd_trace.py [comlab|gaslab]

1. Parses every ``Scenario:`` in labs/comlab/docs/COMLab_BDD.md and the ``*Tests: ...*``
   module list of its Feature.
2. Checks each named module exists.
3. For each scenario, looks for candidate tests: a test function (AST) in ANY comlab test
   module whose source contains ALL of the scenario's key tokens (curated below from the
   scenario's own Given/Then literals). Reports whether a candidate sits in a named module,
   is skipped, and how many candidates exist. Zero candidates = ORPHAN.
Read-only.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAB = sys.argv[1] if len(sys.argv) > 1 else "comlab"
BDD = ROOT / {"comlab": "labs/comlab/docs/COMLab_BDD.md", "gaslab": "labs/gaslab/docs/BDD_GASLab.md"}[LAB]
TESTS = ROOT / f"labs/{LAB}/tests"

# Scenario title -> list of tokens that a covering test must contain (all, case-sensitive).
# Tokens are the scenario's own literals (codes, enum values, field names).
KEYS: dict[str, list[str]] = {
    "A well-formed payload is accepted": ["model_validate", "OrchestratorInboundRequest"],
    "A malformed DTC string is rejected": ["ERR-CONTRACT-001", "confirmed_dtcs"],
    "An air-metering strategy inconsistent with its sensors is rejected": ["ERR-CONTRACT-002", "DUAL_MAF_MAP_CROSSCHECK", "OrchestratorInboundRequest"],
    "A downstream trim role without a downstream sensor is rejected": ["ERR-CONTRACT-003"],
    "An invalid gas sample aborts the session": ["INVALID", "ERR-ABORT-001", "FATAL_INCOMPLETE"],
    "A borderline gas sample is allowed through": ["BORDERLINE"],
    "A cold engine aborts the session": ["engine_warmed", "ERR-ABORT-002"],
    "An undecodable VIN aborts the session": ["NONE", "ERR-ABORT-004"],
    "A non-start engine does not abort on missing gas data": ["will_not_start", "enable_fatal_gates"],
    "A no-start engine suppresses gas, live PIDs, and monitors": ["will_not_start", "NON_STARTER_NO_EXHAUST"],
    "A cranking engine suppresses live PIDs only": ["cranking", "suppress_obd_live_pids"],
    "A cold-only complaint activates the cold-start hypothesis": ["cold_only", "COLD_START_HYPOTHESIS"],
    "Unread symptom fields route nothing": ["route_symptom({})", "reasons == ()"],  # nearest: empty dict, not tier_1+free_text
    "A biased-lean sensor is surfaced against near-normal chemistry": ["O2_SENSOR_BIASED_LOW", "normalized_obd_lambda=1.1"],
    "Agreement within tolerance reports no bias": ["bias_verdict is None"],
    "A no-OBD session falls back to the measured analyser lambda": ["lambda_measured", "select_perception_lambda"],
    "The detector goes inert with no perception lambda at all": ["select_perception_lambda", "None"],
    "A rule not targeting the resolved horizon is pruned": ["prune_removes_wrong_horizon"],
    "The same request always produces the same verdict": ["twice"],
    "No rule clearing the confidence floor yields no fault": ["MIN_CONFIDENCE_THRESHOLD"],
    "A POA chemistry state injects the POA routing tag": ["POA_SIGNATURE", "POA_HISTORY"],
    "A flashing MIL with a misfire code forces a critical stop": ["mil_flashing", "CRITICAL_IMMEDIATE_STOP"],
    "A solid MIL with the same misfire code does not force a stop": ["mil_flashing", "False", "P030"],
    "The winning fault is enriched from its KG node": ["fault_enrichment", "component_group", "ui_remediation_steps"],
    "Every registry fault has a KG node and vice versa": ["global_fault_registry", "all_fault_ids"],
    "A duplicate fault_id across KG files fails at boot": ["duplicate"],
    "Runtime runner-ups and editor-curated siblings are merged": ["_merge_differential_siblings", "5"],
    "An editor-curated sibling that did not fire has no score": ["editor_curated", "confidence_score is None"],
    "A second operating point promotes the delta-matched family": ["with_second_point=True", "enable_delta=True"],
    "Without a second frame the path is single-point": ["SINGLE_POINT", "execution_meta.degradation_mode"],
    "A MAP-only architecture abstains from a trim delta": ["MAP_ONLY_SPEED_DENSITY", "_architecture_gate"],
    "A delta frame measured at the wrong RPM bucket abstains": ["band_mismatch"],
    "VE evidence is gated to valid cross-checks": ["FAULT_MAF_CONTAMINATION"],
    "Trim evidence is suppressed outside closed loop": ["OL_FAULT", "open_loop"],
    "Trim analytics blocked upstream are not used": ["trim_analytics_gate", "ENGINE_COLD"],
    "Railed sensors with broken bank symmetry flag an ECU hardware fault": ["is_ecu_hardware_fault", "0.80"],
    "Plausible sensor values report no ECU hardware fault": ["is_ecu_hardware_fault"],
    "All four labs reporting cleanly is full fusion": ["execution_meta.degradation_mode", "fixture[\"expected\"]"],  # regression fixtures pin FULL_FUSION/HIGH_ASSURANCE
    "A legacy car without a scanner degrades to gas-dominant": ["GAS_DOMINANT", "obd_live_data"],
    "The result always carries the routing directive and echo audit": ["lab_routing_directive", "user_input_echo_audit"],
}


# GASLab: tests are named descriptively, so the key is the covering test's own
# definition line (auditor's mapping, verified to exist / not skipped by the script),
# plus a scenario literal where one exists. Empty match = ORPHAN.
KEYS_GASLAB: dict[str, list[str]] = {
    "A clean idle sample is accepted": ["def test_sample_validity_all_green"],
    "A diluted or contaminated sample halts the diagnosis": ["def test_sample_invalid_halts", "SAMPLE_INVALID"],
    "An air-rich sample is flagged but not rejected": ["def test_triangle_external_o2_suspect"],
    "A sample that passes the triangle but fails dilution is rejected": ["def test_sample_validity_dilution_fails"],
    "A stoichiometric burn reads near unity": ["def test_stoich_idle_lambda_near_unity"],
    "A misfiring cylinder does not fool lambda": ["def test_misfire_immunity"],
    "NOx is included when the analyser reports it": ["lambda_chem", "nox_correction"],
    "A degenerate all-zero sample returns a safe value": ["co=0.0", "co2=0.0", "lambda_chem"],
    "Combustion gases in the coolant are caught only with the block test": ["def test_coolant_intrusion_rule_fires_with_positive_block_test"],
    "The same chemistry without the block test does not claim a coolant leak": ["def test_coolant_intrusion_rule_bypassed_without_block_test"],
    "An ignition misfire is confirmed by the oxygen spike": ["def test_misfire_masking_confirmed_with_cylinder_count"],
    "A collision pattern with low HC routes to an air leak": ["EXHAUST_AIR_LEAK", "EXTERNAL_O2_SUSPECT", "hc"],
    "A collision pattern with high HC stays a rich misfire": ["def test_hc_101_routes_to_rich_misfire"],
    "A leak chemistry with strong positive trim is a real air leak": ["def test_leak_physical_when_fuel_trim_positive"],
    "The same chemistry without compensating trim is treated as a bad sample": ["def test_leak_sampling_error_when_fuel_trim_in_band"],
    "A catalyst fault is impossible on a catalyst-free vehicle": ["has_catalyst=False"],
    "A GDI fault is impossible on a port-injected vehicle": ["def test_dna_gate_suppresses_gdi_fault"],
    "An EGR fault is impossible on a vehicle without EGR": ["egr_equipped=False", "EGR_STUCK_CLOSED"],
    "A certified lambda target tightens the normal band": ["def test_normal_lambda_window_centres_on_v112"],
    "A per-vehicle idle CO ceiling overrides the Euro default": ["def test_per_vehicle_coc_overrides_euro_default"],
    "A wideband upstream sensor recalibrates the O2-bias signatures": ["def test_o2_bias_calibrated_by_sensor_type"],
    "A retarded-cam MAF lean persists at high idle": ["def test_cam_timing_retarded_maf_persists_at_2500"],
    "A vacuum lean that normalises at high idle is not cam timing": ["def test_lean_mixture_vacuum_leak_normalises"],
    "An advanced cam shows rising NOx and falling HC into high idle": ["def test_cam_timing_advanced_nox_rises"],
    "A retarded-cam MAP rich condition partially normalises at high idle": ["def test_cam_timing_retarded_map_partially_normalises"],
    "An over-advanced ignition shows a clean idle with a NOx-only spike": ["def test_ignition_over_advanced_clean_idle_not_cam"],
    "A confirmed cam timing prunes generic low-HC misfire noise": ["def test_timing_confirmed_prunes_low_hc_misfire"],
    "A catalyst weak at idle but working at high idle is not lighting off": ["def test_weak_catalyst_delta_routes_to_not_lighting_off"],
    "A catalyst degraded at both speeds is overwhelmed": ["def test_dead_catalyst_raw_both_speeds_routes_to_overwhelmed"],
    "Bad fuel control rejects any catalyst verdict": ["def test_catalyst_precondition_lambda_out_of_bounds"],
    "HC that drops sharply into high idle points to worn valve seals": ["def test_worn_valve_seals_idle_hc_drops_at_2500"],
    "HC that climbs under load points to worn piston rings": ["def test_worn_piston_rings_load_hc_co_high"],
    "A wear pattern with no matching leaf drops the whole family": ["WORN_", "not in", "reading_high", "POA_SIGNATURE", "WORN_ENGINE", "WORN_VALVE_SEALS", "WORN_PISTON_RINGS", "== set()"],
    "The narrowest signature wins over a broader one": ["def test_specificity_prefers_narrowest_match"],
    "Catch-all signatures are chosen last": ["_candidate_rank", "catch_all"],
    "No surviving candidate yields normal operation": ["apply_differentiators", "NORMAL_OPERATION", "== []"],
    "Identical candidates resolve deterministically": ["declaration order"],
    "Every diagnosis emits a complete, in-bounds payload": ["def test_payload_round_trip"],
    "A directly-measured lambda is passed through when supplied": ["process(", "lambda_measured="],
    "No directly-measured lambda leaves the field null": ["process(", "lambda_measured is None"],
}


def parse_bdd():
    feats, cur_mods = [], []
    for n, ln in enumerate(BDD.read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^\*Tests: (.*)\*$", ln)
        if m:
            cur_mods = re.findall(r"`([^`]+\.py)`", m.group(1))
        m = re.match(r"^Scenario: (.*)$", ln)
        if m:
            feats.append((n, m.group(1).strip(), list(cur_mods)))
    return feats


def test_functions():
    out = []
    for py in sorted(TESTS.rglob("test_*.py")):
        src = py.read_text(encoding="utf-8")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
                body = ast.get_source_segment(src, node) or ""
                deco = " ".join(ast.get_source_segment(src, d) or "" for d in node.decorator_list)
                skipped = "skip" in deco
                out.append((py.relative_to(TESTS).as_posix(), node.lineno, node.name, body, skipped))
    return out


def main() -> None:
    funcs = test_functions()
    orphans = 0
    for line, title, mods in parse_bdd():
        missing_mods = [m for m in mods if not (TESTS / m).exists()]
        keys = (KEYS if LAB == "comlab" else KEYS_GASLAB).get(title)
        if keys is None:
            print(f"UNMAPPED  {BDD.name}:{line} {title}")
            continue
        cands = [f for f in funcs if all(k in f[3] for k in keys)]
        live = [f for f in cands if not f[4]]
        in_named = [f for f in live if f[0] in mods]
        if not live:
            orphans += 1
            status = "ORPHAN   "
        elif not in_named:
            status = "ELSEWHERE"
        else:
            status = "COVERED  "
        ex = ", ".join(f"{f[0]}:{f[1]}::{f[2]}" for f in (in_named or live)[:2])
        sk = [f"{f[0]}:{f[1]}" for f in cands if f[4]]
        print(f"{status} {BDD.name}:{line} '{title}' keys={keys} live={len(live)}"
              + (f" e.g. {ex}" if ex else "") + (f" SKIPPED={sk}" if sk else "")
              + (f" MISSING_MODULES={missing_mods}" if missing_mods else ""))
    print(f"\nscenarios={len(parse_bdd())} orphans={orphans}")


if __name__ == "__main__":
    main()
