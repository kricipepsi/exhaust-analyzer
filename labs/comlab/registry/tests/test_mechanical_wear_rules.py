"""Targeted tests for registry/rules/mechanical_wear.json — v2 mechanical_wear rule file."""

import csv
import json
import pathlib

from registry.schema_v2 import (
    ChemistryState,
    EvidenceTier,
    FaultFamily,
    RuleSet,
)

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
CORPUS_FILE = RULES_DIR.parent / "corpus_curated.csv"
MECHANICAL_WEAR_FILE = RULES_DIR / "mechanical_wear.json"


def _load_ruleset():
    data = json.loads(MECHANICAL_WEAR_FILE.read_text())
    return RuleSet.model_validate(data)


def _load_corpus_case_ids():
    with open(CORPUS_FILE, newline="") as f:
        return {row["case_id"] for row in csv.DictReader(f)}


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert MECHANICAL_WEAR_FILE.is_file(), f"Missing {MECHANICAL_WEAR_FILE}"


def test_valid_json():
    data = json.loads(MECHANICAL_WEAR_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family == FaultFamily.MECHANICAL_WEAR


def test_exactly_nine_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 9, f"Expected 9 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


# ---------------------------------------------------------------------------
# passes_cases — every rule has cases, all resolve
# ---------------------------------------------------------------------------


def test_every_rule_has_passes_cases():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert len(rule.passes_cases) >= 1, (
            f"{rule.rule_id}: missing passes_cases"
        )


def test_all_case_ids_resolve():
    rs = _load_ruleset()
    corpus_ids = _load_corpus_case_ids()
    orphans = []
    for rule in rs.rules:
        for cid in rule.passes_cases:
            if cid not in corpus_ids:
                orphans.append(f"{rule.rule_id}: {cid}")
    assert not orphans, f"Orphan case refs: {orphans}"


# ---------------------------------------------------------------------------
# Chemistry evidence coverage
# ---------------------------------------------------------------------------


def test_mw001_worn_piston_rings_gating():
    """MW-001 must use WORN_PISTON_RINGS chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-001":
            found = any(
                chem.state == ChemistryState.WORN_PISTON_RINGS
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-001: missing WORN_PISTON_RINGS GATING chemistry"


def test_mw002_worn_valve_seals_gating():
    """MW-002 must use WORN_VALVE_SEALS chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-002":
            found = any(
                chem.state == ChemistryState.WORN_VALVE_SEALS
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-002: missing WORN_VALVE_SEALS GATING chemistry"


def test_mw003_coolant_leak_internal_gating():
    """MW-003 must use COOLANT_LEAK_INTERNAL chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-003":
            found = any(
                chem.state == ChemistryState.COOLANT_LEAK_INTERNAL
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-003: missing COOLANT_LEAK_INTERNAL GATING chemistry"


def test_mw004_worn_engine_gating():
    """MW-004 must use WORN_ENGINE chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-004":
            found = any(
                chem.state == ChemistryState.WORN_ENGINE
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-004: missing WORN_ENGINE GATING chemistry"


def test_mw004_incomplete_combustion_definitive():
    """MW-004 promotes INCOMPLETE_COMBUSTION to DEFINITIVE for FT-10 differentiation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-004":
            found = any(
                chem.state == ChemistryState.INCOMPLETE_COMBUSTION
                and chem.tier == EvidenceTier.DEFINITIVE
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-004: missing INCOMPLETE_COMBUSTION DEFINITIVE chemistry"


def test_mw005_incomplete_combustion_gating():
    """MW-005 must use INCOMPLETE_COMBUSTION chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-005":
            found = any(
                chem.state == ChemistryState.INCOMPLETE_COMBUSTION
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-005: missing INCOMPLETE_COMBUSTION GATING chemistry"


def test_mw006_timing_retarded_suggestive():
    """MW-006 must use TIMING_RETARDED chemistry as SUGGESTIVE evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-006":
            found = any(
                chem.state == ChemistryState.TIMING_RETARDED
                and chem.tier == EvidenceTier.SUGGESTIVE
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-006: missing TIMING_RETARDED SUGGESTIVE chemistry"


def test_mw007_ignition_misfire_gating():
    """MW-007 bridges GASLab IGNITION_MISFIRE chemistry to mechanical_wear only with discriminators."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-007":
            found = any(
                chem.state == ChemistryState.IGNITION_MISFIRE
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "MW-007: missing IGNITION_MISFIRE GATING chemistry"


# ---------------------------------------------------------------------------
# OBD evidence coverage
# ---------------------------------------------------------------------------


def test_mw003_ect_obd_evidence():
    """MW-003 must carry ect_c > 95.0 as SUGGESTIVE OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-003":
            found = any(
                obd.pid == "ect_c" and obd.operator == "gt"
                and obd.value == 95.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "MW-003: missing ect_c > 95.0 SUGGESTIVE OBD evidence"


def test_mw004_map_obd_evidence():
    """MW-004 must carry map_kpa < 30.0 as SUGGESTIVE OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-004":
            found = any(
                obd.pid == "map_kpa" and obd.operator == "lt"
                and obd.value == 30.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "MW-004: missing map_kpa < 30.0 SUGGESTIVE OBD evidence"


def test_mw005_rpm_gating_obd_evidence():
    """MW-005 must carry rpm > 600 as GATING OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-005":
            found = any(
                obd.pid == "rpm" and obd.operator == "gt"
                and obd.value == 600 and obd.tier == EvidenceTier.GATING
                for obd in rule.obd_evidence
            )
            assert found, "MW-005: missing rpm > 600 GATING OBD evidence"


def test_mw007_high_hc_definitive_obd_evidence():
    """MW-007 must require high HC as DEFINITIVE evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-007":
            found = any(
                obd.pid == "hc" and obd.operator == "ge"
                and obd.value == 200.0 and obd.tier == EvidenceTier.DEFINITIVE
                for obd in rule.obd_evidence
            )
            assert found, "MW-007: missing hc >= 200 DEFINITIVE OBD evidence"


def test_mw007_o2_ceiling_discriminator():
    """MW-007 must exclude high-O2 no-DTC true misfire while beating MF-001 on CSV-120."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-007":
            found = any(
                obd.pid == "o2" and obd.operator == "lt"
                and obd.value == 4.0 and obd.tier == EvidenceTier.GATING
                for obd in rule.obd_evidence
            )
            assert found, "MW-007: missing o2 < 4.0 GATING discriminator"


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_mw006_vvt_none_present_dtc_gating():
    """MW-006 must gate on VVT_HISTORY DTCs with strategy none_present."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-006":
            found = any(
                dtc.strategy == "none_present"
                and dtc.tier == EvidenceTier.GATING
                and any("P001" in code or "P002" in code for code in dtc.dtc_codes)
                for dtc in rule.dtc_evidence
            )
            assert found, (
                "MW-006: missing VVT_HISTORY DTC none_present GATING evidence"
            )


def test_mw006_no_vvt_codes_in_dtc_evidence():
    """MW-006 DTC none_present list must include P0010-P0025 range (VVT codes)."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-006":
            assert len(rule.dtc_evidence) == 1, (
                f"MW-006: expected exactly 1 DTC evidence entry, got {len(rule.dtc_evidence)}"
            )
            dtc = rule.dtc_evidence[0]
            assert dtc.strategy == "none_present"
            # Must include the P001x and P002x VVT ranges
            codes = dtc.dtc_codes
            assert "P0011" in codes, "MW-006: missing P0011 in none_present DTC list"
            assert "P0012" in codes, "MW-006: missing P0012 in none_present DTC list"
            assert "P0021" in codes, "MW-006: missing P0021 in none_present DTC list"
            assert len(codes) >= 12, (
                f"MW-006: expected >=12 VVT DTC codes, got {len(codes)}"
            )


def test_mw007_misfire_codes_none_present_definitive():
    """MW-007 differentiates mechanical wear from true misfire by absence of P030x DTCs."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-007":
            found = any(
                dtc.strategy == "none_present"
                and dtc.tier == EvidenceTier.DEFINITIVE
                and "P0300" in dtc.dtc_codes
                and "P0304" in dtc.dtc_codes
                for dtc in rule.dtc_evidence
            )
            assert found, "MW-007: missing P0300-P0304 none_present DEFINITIVE evidence"


# ---------------------------------------------------------------------------
# Wiki citations on numeric thresholds
# ---------------------------------------------------------------------------


def test_mw003_ect_wiki_ref():
    """MW-003 ect_c threshold must carry a wiki_ref citation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-003":
            for obd in rule.obd_evidence:
                if obd.pid == "ect_c":
                    assert obd.wiki_ref is not None, (
                        "MW-003: ect_c threshold missing wiki_ref"
                    )


def test_mw004_map_wiki_ref():
    """MW-004 map_kpa threshold must carry a wiki_ref citation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-004":
            for obd in rule.obd_evidence:
                if obd.pid == "map_kpa":
                    assert obd.wiki_ref is not None, (
                        "MW-004: map_kpa threshold missing wiki_ref"
                    )


def test_mw005_rpm_wiki_ref():
    """MW-005 rpm threshold must carry a wiki_ref citation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "MW-005":
            for obd in rule.obd_evidence:
                if obd.pid == "rpm":
                    assert obd.wiki_ref is not None, (
                        "MW-005: rpm threshold missing wiki_ref"
                    )


# ---------------------------------------------------------------------------
# Competition group integrity
# ---------------------------------------------------------------------------


def test_competition_group_mechanical_wear():
    """All rules must belong to mechanical_wear competition group."""
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.competition_group == "mechanical_wear", (
            f"{rule.rule_id}: expected competition_group 'mechanical_wear', "
            f"got '{rule.competition_group}'"
        )


def test_no_solo_survivor():
    """At least 2 rules must carry confidence_ceiling."""
    rs = _load_ruleset()
    ceiling_count = sum(1 for r in rs.rules if r.confidence_ceiling is not None)
    assert ceiling_count >= 2, (
        f"Only {ceiling_count} rule(s) carry confidence_ceiling; "
        "need ≥ 2 (no-solo-survivor discipline)"
    )


def test_confidence_ceiling_values_in_range():
    """All confidence_ceiling values must be in [0.0, 1.0]."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.confidence_ceiling is not None:
            assert 0.0 <= rule.confidence_ceiling <= 1.0, (
                f"{rule.rule_id}: confidence_ceiling {rule.confidence_ceiling} out of range"
            )


def test_base_weights_in_range():
    """All base_weight values must be in [0.0, 1.0]."""
    rs = _load_ruleset()
    for rule in rs.rules:
        assert 0.0 <= rule.base_weight <= 1.0, (
            f"{rule.rule_id}: base_weight {rule.base_weight} out of range"
        )


# ---------------------------------------------------------------------------
# Coverage — all 11 mechanical_wear cases appear in at least one passes_cases
# ---------------------------------------------------------------------------


def test_all_mechanical_wear_cases_covered():
    """Every mechanical_wear case in corpus_curated.csv must appear in ≥1 rule."""
    rs = _load_ruleset()
    all_passes = set()
    for rule in rs.rules:
        all_passes.update(rule.passes_cases)

    # Get mechanical_wear cases from corpus
    mw_cases = set()
    with open(CORPUS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("expected_top_fault_family") == "mechanical_wear":
                mw_cases.add(row["case_id"])

    uncovered = mw_cases - all_passes
    assert not uncovered, (
        f"Mechanical_wear cases not covered by any rule: {sorted(uncovered)}"
    )


# ---------------------------------------------------------------------------
# Rule count by case — every case covered by ≥2 competing rules where feasible
# ---------------------------------------------------------------------------


def test_mw_cases_have_competing_rules():
    """Cases with multiple chemistry states should be covered by ≥2 rules."""
    rs = _load_ruleset()
    # MECH-006 and EXT-222 should have ≥2 rules each (WORN_ENGINE + INCOMPLETE_COMBUSTION)
    for cid in ["MECH-006", "EXT-222"]:
        rule_count = sum(1 for r in rs.rules if cid in r.passes_cases)
        assert rule_count >= 2, (
            f"{cid}: covered by only {rule_count} rule(s); "
            "these cases produce multiple chemistry states and need competing rules"
        )
