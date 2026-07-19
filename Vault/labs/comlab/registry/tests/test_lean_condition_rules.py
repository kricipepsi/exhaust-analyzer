"""Targeted tests for registry/rules/lean_condition.json — the first v2 rule file."""

import json
import pathlib


from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
LEAN_CONDITION_FILE = RULES_DIR / "lean_condition.json"


def _load_ruleset():
    """Helper: load and validate the lean_condition rule file."""
    data = json.loads(LEAN_CONDITION_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert LEAN_CONDITION_FILE.is_file(), f"Missing {LEAN_CONDITION_FILE}"


def test_valid_json():
    data = json.loads(LEAN_CONDITION_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "lean_condition"


def test_at_least_three_rules():
    rs = _load_ruleset()
    assert len(rs.rules) >= 3, f"Expected >= 3 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


# ---------------------------------------------------------------------------
# Evidence-tier coverage
# ---------------------------------------------------------------------------


def test_lean_mixture_as_definitive():
    """LEAN_MIXTURE must appear as DEFINITIVE in at least one rule."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.LEAN_MIXTURE and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has LEAN_MIXTURE as DEFINITIVE evidence"


def test_timing_retarded_as_suggestive():
    """TIMING_RETARDED must appear as SUGGESTIVE in at least one rule — closes #1 v1 gap."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.TIMING_RETARDED and chem.tier == EvidenceTier.SUGGESTIVE:
                found = True
    assert found, "No rule has TIMING_RETARDED as SUGGESTIVE evidence — #1 v1 gap not closed"


# ---------------------------------------------------------------------------
# Rule contract integrity
# ---------------------------------------------------------------------------


def test_every_rule_has_passes_cases():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert len(rule.passes_cases) >= 1, f"{rule.rule_id}: passes_cases must not be empty"


def test_every_rule_has_wiki_refs():
    rs = _load_ruleset()
    for rule in rs.rules:
        assert len(rule.source_wiki_refs) >= 1, f"{rule.rule_id}: missing source_wiki_refs"


def test_no_bare_numeric_thresholds():
    """Every numeric threshold in OBD evidence must carry a wiki_ref."""
    rs = _load_ruleset()
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.operator != "in_range":
                assert obd.value is not None
            assert obd.wiki_ref is not None, (
                f"{rule.rule_id}: OBD pid '{obd.pid}' has no wiki_ref — bare magic number"
            )


def test_chemistry_wiki_refs():
    rs = _load_ruleset()
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            assert chem.wiki_ref is not None, (
                f"{rule.rule_id}: chemistry '{chem.state.value}' has no wiki_ref"
            )


# ---------------------------------------------------------------------------
# Competition group
# ---------------------------------------------------------------------------


def test_all_rules_in_same_competition_group():
    rs = _load_ruleset()
    groups = set(r.competition_group for r in rs.rules)
    assert groups == {"lean_condition"}, f"All rules should compete in 'lean_condition', got {groups}"


# ---------------------------------------------------------------------------
# No invented enum values
# ---------------------------------------------------------------------------


def test_no_invented_chemistry_states():
    rs = _load_ruleset()
    valid = set(s.value for s in ChemistryState)
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            assert chem.state.value in valid, f"{rule.rule_id}: unknown chemistry state '{chem.state.value}'"


def test_no_invented_evidence_tiers():
    rs = _load_ruleset()
    valid = set(t.value for t in EvidenceTier)
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            assert chem.tier.value in valid, f"{rule.rule_id}: unknown tier '{chem.tier.value}'"
        for obd in rule.obd_evidence:
            assert obd.tier.value in valid, f"{rule.rule_id}: unknown tier '{obd.tier.value}'"
        for dtc in rule.dtc_evidence:
            assert dtc.tier.value in valid, f"{rule.rule_id}: unknown tier '{dtc.tier.value}'"
