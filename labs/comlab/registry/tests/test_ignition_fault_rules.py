"""Targeted tests for registry/rules/ignition_fault.json — the v2 ignition_fault rule file."""

import json
import pathlib


from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
IGNITION_FAULT_FILE = RULES_DIR / "ignition_fault.json"


def _load_ruleset():
    """Helper: load and validate the ignition_fault rule file."""
    data = json.loads(IGNITION_FAULT_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert IGNITION_FAULT_FILE.is_file(), f"Missing {IGNITION_FAULT_FILE}"


def test_valid_json():
    data = json.loads(IGNITION_FAULT_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "ignition_fault"


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


def test_ignition_misfire_as_definitive():
    """IGNITION_MISFIRE must appear as DEFINITIVE in at least one rule — IF-001 anchor."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.IGNITION_MISFIRE and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has IGNITION_MISFIRE as DEFINITIVE evidence"


def test_poa_signature_as_definitive():
    """POA_SIGNATURE must appear as DEFINITIVE in at least one rule — IF-002 anchor for knock cases."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.POA_SIGNATURE and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has POA_SIGNATURE as DEFINITIVE evidence"


def test_if_002_base_weight_sufficient():
    """IF-002 base_weight must be ≥ 0.86 to clear CF-001 at 0.90 on SAMPLE_INVALID cases where chemistry is None (hard-absence semantics)."""
    rs = _load_ruleset()
    if002 = next(r for r in rs.rules if r.rule_id == "IF-002")
    assert if002.base_weight >= 0.86, f"IF-002 base_weight {if002.base_weight} too low to beat CF-001 at 0.90 on chemistry-None cases"


def test_dtc_gating_present():
    """At least one rule must carry DTC evidence at GATING tier — the coil/knock discriminator."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if dtc.tier == EvidenceTier.GATING:
                found = True
    assert found, "No rule has DTC evidence at GATING tier — the family discriminator is missing"


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
    assert groups == {"ignition_fault"}, f"All rules should compete in 'ignition_fault', got {groups}"


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


# ---------------------------------------------------------------------------
# Target case coverage — the 3 curated consumer cases
# ---------------------------------------------------------------------------


def test_passes_cases_includes_exp_n026():
    """EXP-N026 must appear in passes_cases of the rule that targets it (IF-002)."""
    rs = _load_ruleset()
    all_cases: set[str] = set()
    for rule in rs.rules:
        all_cases.update(rule.passes_cases)
    assert "EXP-N026" in all_cases, "EXP-N026 not in any rule's passes_cases"


def test_passes_cases_includes_case_035():
    """CASE-035 must appear in passes_cases of the rule that targets it (IF-002)."""
    rs = _load_ruleset()
    all_cases: set[str] = set()
    for rule in rs.rules:
        all_cases.update(rule.passes_cases)
    assert "CASE-035" in all_cases, "CASE-035 not in any rule's passes_cases"


def test_passes_cases_includes_case_036():
    """case_036 must appear in passes_cases of the rule that targets it (IF-003)."""
    rs = _load_ruleset()
    all_cases: set[str] = set()
    for rule in rs.rules:
        all_cases.update(rule.passes_cases)
    assert "case_036" in all_cases, "case_036 not in any rule's passes_cases"
