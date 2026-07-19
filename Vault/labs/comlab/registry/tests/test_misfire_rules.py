"""Targeted tests for registry/rules/misfire.json — v2 misfire rule file."""

import json
import pathlib


from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
MISFIRE_FILE = RULES_DIR / "misfire.json"


def _load_ruleset():
    """Helper: load and validate the misfire rule file."""
    data = json.loads(MISFIRE_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert MISFIRE_FILE.is_file(), f"Missing {MISFIRE_FILE}"


def test_valid_json():
    data = json.loads(MISFIRE_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "misfire"


def test_at_least_five_rules():
    rs = _load_ruleset()
    assert len(rs.rules) >= 5, f"Expected >= 5 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


# ---------------------------------------------------------------------------
# Evidence-tier coverage — chemistry states
# ---------------------------------------------------------------------------


def test_ignition_misfire_as_definitive():
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.IGNITION_MISFIRE and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has IGNITION_MISFIRE as DEFINITIVE evidence"


def test_lean_misfire_as_definitive():
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.LEAN_MISFIRE and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has LEAN_MISFIRE as DEFINITIVE evidence"


def test_rich_misfire_as_definitive():
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.RICH_MISFIRE and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has RICH_MISFIRE as DEFINITIVE evidence"


def test_normal_operation_as_definitive():
    """NORMAL_OPERATION must appear as DEFINITIVE — ghost-misfire pattern."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.NORMAL_OPERATION and chem.tier == EvidenceTier.DEFINITIVE:
                found = True
    assert found, "No rule has NORMAL_OPERATION as DEFINITIVE — ghost-misfire gap not covered"


def test_sample_invalid_as_gating():
    """SAMPLE_INVALID must appear as GATING — closes #2 v1 gap for misfire family."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.SAMPLE_INVALID and chem.tier == EvidenceTier.GATING:
                found = True
    assert found, "No rule has SAMPLE_INVALID as GATING evidence — gap not closed"


def test_timing_retarded_as_suggestive():
    """TIMING_RETARDED must appear as SUGGESTIVE — closes TIMING_RETARDED gap for misfire family."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.TIMING_RETARDED and chem.tier == EvidenceTier.SUGGESTIVE:
                found = True
    assert found, "No rule has TIMING_RETARDED as SUGGESTIVE evidence — gap not closed"


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_misfire_history_dtc():
    """At least one rule must use MISFIRE_HISTORY DTC codes (P0300-P0312)."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if any(code.startswith("P030") for code in dtc.dtc_codes):
                found = True
    assert found, "No rule uses P030x DTC evidence"


def test_misfire_history_none_present():
    """At least one rule must use MISFIRE_HISTORY with strategy none_present — ECU blindness gap."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            codes = dtc.dtc_codes
            if any(c.startswith("P030") for c in codes) and dtc.strategy == "none_present":
                found = True
    assert found, "No rule uses MISFIRE_HISTORY with strategy none_present — ECU blindness gap not covered"


def test_perception_flag_present():
    """At least one rule must carry a perception_flag — truth-vs-perception override."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        if rule.perception_flag is not None:
            found = True
    assert found, "No rule has a perception_flag set"


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


def test_dtc_wiki_refs():
    rs = _load_ruleset()
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            assert dtc.wiki_ref is not None, (
                f"{rule.rule_id}: DTC evidence has no wiki_ref"
            )


# ---------------------------------------------------------------------------
# Confidence ceiling — solo survivor prevention
# ---------------------------------------------------------------------------


def test_low_base_weight_rules_have_confidence_ceiling():
    """Rules with base_weight <= 0.65 must carry a confidence_ceiling."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.base_weight <= 0.65:
            assert rule.confidence_ceiling is not None, (
                f"{rule.rule_id}: base_weight={rule.base_weight} <= 0.65 but no confidence_ceiling"
            )


# ---------------------------------------------------------------------------
# Competition group
# ---------------------------------------------------------------------------


def test_all_rules_in_same_competition_group():
    rs = _load_ruleset()
    groups = set(r.competition_group for r in rs.rules)
    assert groups == {"misfire"}, f"All rules should compete in 'misfire', got {groups}"


# ---------------------------------------------------------------------------
# No invented enum values
# ---------------------------------------------------------------------------


def test_no_invented_chemistry_states():
    rs = _load_ruleset()
    valid = set(s.value for s in ChemistryState)
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            assert chem.state.value in valid, (
                f"{rule.rule_id}: unknown chemistry state '{chem.state.value}'"
            )


def test_no_invented_evidence_tiers():
    rs = _load_ruleset()
    valid = set(t.value for t in EvidenceTier)
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            assert chem.tier.value in valid, (
                f"{rule.rule_id}: unknown tier '{chem.tier.value}'"
            )
        for obd in rule.obd_evidence:
            assert obd.tier.value in valid, (
                f"{rule.rule_id}: unknown tier '{obd.tier.value}'"
            )
        for dtc in rule.dtc_evidence:
            assert dtc.tier.value in valid, (
                f"{rule.rule_id}: unknown tier '{dtc.tier.value}'"
            )
