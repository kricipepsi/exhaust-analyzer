"""Targeted tests for registry/rules/vacuum_leak.json — v2 vacuum_leak rule file."""

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
VACUUM_LEAK_FILE = RULES_DIR / "vacuum_leak.json"


def _load_ruleset():
    data = json.loads(VACUUM_LEAK_FILE.read_text())
    return RuleSet.model_validate(data)


def _load_corpus_case_ids():
    with open(CORPUS_FILE, newline="") as f:
        return {row["case_id"] for row in csv.DictReader(f)}


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert VACUUM_LEAK_FILE.is_file(), f"Missing {VACUUM_LEAK_FILE}"


def test_valid_json():
    data = json.loads(VACUUM_LEAK_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family == FaultFamily.VACUUM_LEAK


def test_exactly_three_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 3, f"Expected 3 rules, got {len(rs.rules)}"


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


def test_vl001_lean_mixture_definitive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-001":
            found = any(
                chem.state == ChemistryState.LEAN_MIXTURE
                and chem.tier == EvidenceTier.DEFINITIVE
                for chem in rule.chemistry_evidence
            )
            assert found, "VL-001: missing LEAN_MIXTURE DEFINITIVE chemistry"


def test_vl002_lean_mixture_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-002":
            found = any(
                chem.state == ChemistryState.LEAN_MIXTURE
                and chem.tier == EvidenceTier.SUGGESTIVE
                for chem in rule.chemistry_evidence
            )
            assert found, "VL-002: missing LEAN_MIXTURE SUGGESTIVE chemistry"


def test_vl003_lean_mixture_definitive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-003":
            found = any(
                chem.state == ChemistryState.LEAN_MIXTURE
                and chem.tier == EvidenceTier.DEFINITIVE
                for chem in rule.chemistry_evidence
            )
            assert found, "VL-003: missing LEAN_MIXTURE DEFINITIVE chemistry"


# ---------------------------------------------------------------------------
# OBD evidence coverage
# ---------------------------------------------------------------------------


def test_vl001_longft1_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-001":
            found = any(
                obd.pid == "longft1" and obd.operator == "ge"
                and obd.value == 10.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "VL-001: missing longft1 ge 10.0 SUGGESTIVE OBD"


def test_vl001_shrtft1_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-001":
            found = any(
                obd.pid == "shrtft1" and obd.operator == "ge"
                and obd.value == 5.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "VL-001: missing shrtft1 ge 5.0 SUGGESTIVE OBD"


def test_vl001_map_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-001":
            found = any(
                obd.pid == "map_kpa" and obd.operator == "gt"
                and obd.value == 40.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "VL-001: missing map_kpa gt 40.0 SUGGESTIVE OBD"


def test_vl002_longft1_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-002":
            found = any(
                obd.pid == "longft1" and obd.operator == "ge"
                and obd.value == 8.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "VL-002: missing longft1 ge 8.0 SUGGESTIVE OBD"


def test_vl002_shrtft1_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-002":
            found = any(
                obd.pid == "shrtft1" and obd.operator == "ge"
                and obd.value == 3.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "VL-002: missing shrtft1 ge 3.0 SUGGESTIVE OBD"


def test_vl003_map_gating():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-003":
            found = any(
                obd.pid == "map_kpa" and obd.operator == "gt"
                and obd.value == 50.0 and obd.tier == EvidenceTier.GATING
                for obd in rule.obd_evidence
            )
            assert found, "VL-003: missing map_kpa gt 50.0 GATING OBD"


def test_vl003_longft1_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-003":
            found = any(
                obd.pid == "longft1" and obd.operator == "ge"
                and obd.value == 15.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "VL-003: missing longft1 ge 15.0 SUGGESTIVE OBD"


def test_vl003_shrtft1_suggestive():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-003":
            found = any(
                obd.pid == "shrtft1" and obd.operator == "ge"
                and obd.value == 10.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "VL-003: missing shrtft1 ge 10.0 SUGGESTIVE OBD"


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_vl002_dtc_any_match_gating():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-002":
            assert len(rule.dtc_evidence) == 1, (
                f"VL-002: expected exactly 1 DTC evidence entry, got {len(rule.dtc_evidence)}"
            )
            dtc = rule.dtc_evidence[0]
            assert dtc.strategy == "any_match"
            assert dtc.tier == EvidenceTier.GATING
            codes = dtc.dtc_codes
            assert "P0171" in codes, "VL-002: missing P0171 in DTC list"
            assert "P0174" in codes, "VL-002: missing P0174 in DTC list"


# ---------------------------------------------------------------------------
# Wiki citations on numeric thresholds
# ---------------------------------------------------------------------------


def test_vl001_obd_wiki_refs():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-001":
            for obd in rule.obd_evidence:
                assert obd.wiki_ref is not None, (
                    f"VL-001: OBD {obd.pid} missing wiki_ref"
                )


def test_vl002_obd_wiki_refs():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-002":
            for obd in rule.obd_evidence:
                assert obd.wiki_ref is not None, (
                    f"VL-002: OBD {obd.pid} missing wiki_ref"
                )


def test_vl002_dtc_wiki_ref():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-002":
            for dtc in rule.dtc_evidence:
                assert dtc.wiki_ref is not None, (
                    "VL-002: DTC evidence missing wiki_ref"
                )


def test_vl003_obd_wiki_refs():
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "VL-003":
            for obd in rule.obd_evidence:
                assert obd.wiki_ref is not None, (
                    f"VL-003: OBD {obd.pid} missing wiki_ref"
                )


# ---------------------------------------------------------------------------
# Competition group integrity
# ---------------------------------------------------------------------------


def test_competition_group_vacuum_leak():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.competition_group == "vacuum_leak", (
            f"{rule.rule_id}: expected competition_group 'vacuum_leak', "
            f"got '{rule.competition_group}'"
        )


def test_all_rules_have_confidence_ceiling():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.confidence_ceiling is not None, (
            f"{rule.rule_id}: must set confidence_ceiling — "
            "all vacuum_leak rules share LEAN_MIXTURE chemistry with lean_condition"
        )


def test_no_solo_survivor():
    rs = _load_ruleset()
    ceiling_count = sum(1 for r in rs.rules if r.confidence_ceiling is not None)
    assert ceiling_count >= 2, (
        f"Only {ceiling_count} rule(s) carry confidence_ceiling; "
        "need >= 2 (no-solo-survivor discipline)"
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
# Coverage — all 4 vacuum_leak cases appear in at least one passes_cases
# ---------------------------------------------------------------------------


def test_all_vacuum_leak_cases_covered():
    rs = _load_ruleset()
    all_passes = set()
    for rule in rs.rules:
        all_passes.update(rule.passes_cases)

    vl_cases = set()
    with open(CORPUS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("expected_top_fault_family") == "vacuum_leak":
                vl_cases.add(row["case_id"])

    uncovered = vl_cases - all_passes
    assert not uncovered, (
        f"Vacuum_leak cases not covered by any rule: {sorted(uncovered)}"
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
