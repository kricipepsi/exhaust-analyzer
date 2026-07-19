"""Targeted tests for registry/rules/overheating.json — v2 overheating rule file."""

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
OVERHEATING_FILE = RULES_DIR / "overheating.json"


def _load_ruleset():
    data = json.loads(OVERHEATING_FILE.read_text())
    return RuleSet.model_validate(data)


def _load_corpus_case_ids():
    with open(CORPUS_FILE, newline="") as f:
        return {row["case_id"] for row in csv.DictReader(f)}


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert OVERHEATING_FILE.is_file(), f"Missing {OVERHEATING_FILE}"


def test_valid_json():
    data = json.loads(OVERHEATING_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family == FaultFamily.OVERHEATING


def test_exactly_four_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 4, f"Expected 4 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


def test_rule_ids_match_pattern():
    rs = _load_ruleset()
    expected = {"OV-001", "OV-002", "OV-003", "OV-004"}
    actual = {r.rule_id for r in rs.rules}
    assert actual == expected, f"Rule ID mismatch: {actual} vs {expected}"


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
# Chemistry evidence — OBD-primary family; three of four rules are chemistry-empty
# ---------------------------------------------------------------------------


def _rule_by_id(rs: RuleSet, rid: str):
    for r in rs.rules:
        if r.rule_id == rid:
            return r
    raise AssertionError(f"rule_id {rid} not found")


def test_ov001_chemistry_empty():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-001")
    assert rule.chemistry_evidence == [], (
        "OV-001: chemistry_evidence must be empty — HIGH_COMBUSTION_TEMP is "
        "unreachable at idle NOx levels (GAS_VOCABULARY §10.5)"
    )


def test_ov002_chemistry_empty():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-002")
    assert rule.chemistry_evidence == [], (
        "OV-002: chemistry_evidence must be empty — DTC-gated rule, "
        "OBD-primary diagnostic"
    )


def test_ov003_coolant_leak_internal_suggestive():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-003")
    found = any(
        chem.state == ChemistryState.COOLANT_LEAK_INTERNAL
        and chem.tier == EvidenceTier.SUGGESTIVE
        for chem in rule.chemistry_evidence
    )
    assert found, (
        "OV-003: missing COOLANT_LEAK_INTERNAL SUGGESTIVE chemistry "
        "(emission not guaranteed at these synthetic values, so SUGGESTIVE not DEFINITIVE)"
    )


def test_ov004_chemistry_empty():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-004")
    assert rule.chemistry_evidence == [], (
        "OV-004: chemistry_evidence must be empty — silent fan failure, "
        "no chemistry signal"
    )


# ---------------------------------------------------------------------------
# OBD evidence — ECT and RPM thresholds per OBD_VOCABULARY §23
# ---------------------------------------------------------------------------


def test_ov001_ect_definitive_110():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-001")
    found = any(
        obd.pid == "ect_c" and obd.operator == "gt"
        and obd.value == 110.0 and obd.tier == EvidenceTier.DEFINITIVE
        for obd in rule.obd_evidence
    )
    assert found, "OV-001: missing ect_c gt 110.0 DEFINITIVE OBD"


def test_ov001_rpm_suggestive_gt_1000():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-001")
    found = any(
        obd.pid == "rpm" and obd.operator == "gt"
        and obd.value == 1000.0 and obd.tier == EvidenceTier.SUGGESTIVE
        for obd in rule.obd_evidence
    )
    assert found, "OV-001: missing rpm gt 1000.0 SUGGESTIVE OBD"


def test_ov002_ect_suggestive_105():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-002")
    found = any(
        obd.pid == "ect_c" and obd.operator == "gt"
        and obd.value == 105.0 and obd.tier == EvidenceTier.SUGGESTIVE
        for obd in rule.obd_evidence
    )
    assert found, "OV-002: missing ect_c gt 105.0 SUGGESTIVE OBD"


def test_ov002_p0128_gating():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-002")
    assert len(rule.dtc_evidence) == 1, (
        f"OV-002: expected exactly 1 DTC evidence entry, got {len(rule.dtc_evidence)}"
    )
    dtc = rule.dtc_evidence[0]
    assert dtc.strategy == "any_match"
    assert dtc.tier == EvidenceTier.GATING
    assert "P0128" in dtc.dtc_codes, "OV-002: missing P0128 in DTC list"


def test_ov003_ect_definitive_115():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-003")
    found = any(
        obd.pid == "ect_c" and obd.operator == "gt"
        and obd.value == 115.0 and obd.tier == EvidenceTier.DEFINITIVE
        for obd in rule.obd_evidence
    )
    assert found, "OV-003: missing ect_c gt 115.0 DEFINITIVE OBD"


def test_ov003_p0117_suggestive():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-003")
    assert len(rule.dtc_evidence) == 1, (
        f"OV-003: expected exactly 1 DTC evidence entry, got {len(rule.dtc_evidence)}"
    )
    dtc = rule.dtc_evidence[0]
    assert dtc.strategy == "any_match"
    assert dtc.tier == EvidenceTier.SUGGESTIVE
    assert "P0117" in dtc.dtc_codes, "OV-003: missing P0117 in DTC list"


def test_ov004_ect_definitive_105():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-004")
    found = any(
        obd.pid == "ect_c" and obd.operator == "gt"
        and obd.value == 105.0 and obd.tier == EvidenceTier.DEFINITIVE
        for obd in rule.obd_evidence
    )
    assert found, "OV-004: missing ect_c gt 105.0 DEFINITIVE OBD"


def test_ov004_rpm_suggestive_lt_1000():
    rs = _load_ruleset()
    rule = _rule_by_id(rs, "OV-004")
    found = any(
        obd.pid == "rpm" and obd.operator == "lt"
        and obd.value == 1000.0 and obd.tier == EvidenceTier.SUGGESTIVE
        for obd in rule.obd_evidence
    )
    assert found, "OV-004: missing rpm lt 1000.0 SUGGESTIVE OBD"


# ---------------------------------------------------------------------------
# DTC-driven rule presence
# ---------------------------------------------------------------------------


def test_at_least_one_dtc_driven_rule():
    rs = _load_ruleset()
    dtc_rules = [r for r in rs.rules if r.dtc_evidence]
    assert len(dtc_rules) >= 1, "At least one rule must carry DTC evidence"


def test_at_least_one_non_dtc_rule():
    rs = _load_ruleset()
    non_dtc = [r for r in rs.rules if not r.dtc_evidence]
    assert len(non_dtc) >= 1, (
        "At least one rule must handle a non-DTC overheating scenario "
        "(e.g., fan failure with no codes)"
    )


# ---------------------------------------------------------------------------
# Wiki citations on numeric thresholds
# ---------------------------------------------------------------------------


def test_every_obd_threshold_has_wiki_ref():
    rs = _load_ruleset()
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            assert obd.wiki_ref is not None, (
                f"{rule.rule_id}: OBD {obd.pid} missing wiki_ref"
            )


def test_every_dtc_evidence_has_wiki_ref():
    rs = _load_ruleset()
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            assert dtc.wiki_ref is not None, (
                f"{rule.rule_id}: DTC evidence missing wiki_ref"
            )


def test_every_chemistry_has_wiki_ref():
    rs = _load_ruleset()
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            assert chem.wiki_ref is not None, (
                f"{rule.rule_id}: chemistry {chem.state} missing wiki_ref"
            )


# ---------------------------------------------------------------------------
# Competition group / no-solo-survivor discipline
# ---------------------------------------------------------------------------


def test_competition_group_overheating():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.competition_group == "overheating", (
            f"{rule.rule_id}: expected competition_group 'overheating', "
            f"got '{rule.competition_group}'"
        )


def test_all_rules_have_confidence_ceiling():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.confidence_ceiling is not None, (
            f"{rule.rule_id}: must set confidence_ceiling (no-solo-survivor)"
        )


def test_confidence_ceiling_values_in_range():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.confidence_ceiling is not None:
            assert 0.0 <= rule.confidence_ceiling <= 1.0, (
                f"{rule.rule_id}: confidence_ceiling {rule.confidence_ceiling} out of range"
            )


def test_base_weights_in_range():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert 0.0 <= rule.base_weight <= 1.0, (
            f"{rule.rule_id}: base_weight {rule.base_weight} out of range"
        )


# ---------------------------------------------------------------------------
# Coverage — all 4 overheating placeholder cases appear in some passes_cases
# ---------------------------------------------------------------------------


def test_all_overheating_cases_covered():
    rs = _load_ruleset()
    all_passes = set()
    for rule in rs.rules:
        all_passes.update(rule.passes_cases)

    overheating_cases = set()
    with open(CORPUS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("expected_top_fault_family") == "overheating":
                overheating_cases.add(row["case_id"])

    uncovered = overheating_cases - all_passes
    assert not uncovered, (
        f"Overheating cases not covered by any rule: {sorted(uncovered)}"
    )


# ---------------------------------------------------------------------------
# Placeholder cases populated (not blank)
# ---------------------------------------------------------------------------


def test_placeholder_rows_populated():
    required_columns = ("hc", "lambda_analyser", "lambda_2500", "ect", "rpm")
    with open(CORPUS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            if not row["case_id"].startswith("NEW-overheating"):
                continue
            for col in required_columns:
                assert row[col], (
                    f"{row['case_id']}: {col} is blank — placeholder not populated"
                )


# ---------------------------------------------------------------------------
# Cross-family: no imports from any lab, COMLab, or 4DLabWired
# ---------------------------------------------------------------------------


def test_no_lab_imports():
    import ast

    src = open(__file__).read()
    banned = {"gaslab", "obdlab", "dtclab", "dnalab", "comlab", "4DLabWired"}
    tree = ast.parse(src)
    for node in ast.walk(tree):
        module = None
        if isinstance(node, ast.ImportFrom) and node.module:
            module = node.module
        elif isinstance(node, ast.Import):
            module = node.names[0].name
        if module:
            for part in module.split("."):
                if part.lower() in banned:
                    raise AssertionError(f"Banned import: {module}")
