"""Targeted tests for registry/rules/rich_mixture.json — v2 rich_mixture rule file."""

import json
import pathlib


from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
RICH_MIXTURE_FILE = RULES_DIR / "rich_mixture.json"


def _load_ruleset():
    """Helper: load and validate the rich_mixture rule file."""
    data = json.loads(RICH_MIXTURE_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert RICH_MIXTURE_FILE.is_file(), f"Missing {RICH_MIXTURE_FILE}"


def test_valid_json():
    data = json.loads(RICH_MIXTURE_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "rich_mixture"


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


def test_rich_mixture_as_definitive():
    """RICH_MIXTURE must appear as DEFINITIVE in at least one rule."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.RICH_MIXTURE and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has RICH_MIXTURE as DEFINITIVE evidence"


def test_poa_signature_as_suggestive():
    """POA_SIGNATURE must appear as SUGGESTIVE in at least one rule."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.POA_SIGNATURE and chem.tier == EvidenceTier.SUGGESTIVE:
                found = True
    assert found, "No rule has POA_SIGNATURE as SUGGESTIVE evidence"


def test_sample_invalid_as_gating():
    """SAMPLE_INVALID must appear as GATING in at least one rule — closes SAMPLE_INVALID gap."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.SAMPLE_INVALID and chem.tier == EvidenceTier.GATING:
                found = True
    assert found, "No rule has SAMPLE_INVALID as GATING evidence — gap not closed"


def test_rich_history_dtc_evidence():
    """At least one rule must use P0172/P0175 DTC evidence — v1 had zero DTC-aware rich rules."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if any(code in dtc.dtc_codes for code in ["P0172", "P0175"]):
                found = True
    assert found, "No rule uses P0172/P0175 DTC evidence"


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
    assert groups == {"rich_mixture"}, f"All rules should compete in 'rich_mixture', got {groups}"


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
