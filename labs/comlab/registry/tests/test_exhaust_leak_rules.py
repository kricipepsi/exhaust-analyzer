"""Targeted tests for registry/rules/exhaust_leak.json — v2 exhaust_leak rule file."""

import json
import pathlib


from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
EXHAUST_LEAK_FILE = RULES_DIR / "exhaust_leak.json"


def _load_ruleset():
    data = json.loads(EXHAUST_LEAK_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert EXHAUST_LEAK_FILE.is_file(), f"Missing {EXHAUST_LEAK_FILE}"


def test_valid_json():
    data = json.loads(EXHAUST_LEAK_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "exhaust_leak"


def test_exactly_three_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 3, f"Expected 3 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


# ---------------------------------------------------------------------------
# Evidence-tier coverage — chemistry states
# ---------------------------------------------------------------------------


def test_exhaust_air_leak_as_definitive_in_at_least_two_rules():
    rs = _load_ruleset()
    count = 0
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if chem.state == ChemistryState.EXHAUST_AIR_LEAK and chem.tier == EvidenceTier.DEFINITIVE:
                count += 1
    assert count >= 2, f"Expected >= 2 rules with EXHAUST_AIR_LEAK DEFINITIVE, got {count}"


def test_no_normal_operation_chemistry():
    """NORMAL_OPERATION must not appear — ERR-EL-004 false-positive path removed in v2."""
    rs = _load_ruleset()
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            assert chem.state != ChemistryState.NORMAL_OPERATION, (
                f"{rule.rule_id}: NORMAL_OPERATION chemistry found — false-positive path must be removed"
            )


# ---------------------------------------------------------------------------
# OBD evidence coverage
# ---------------------------------------------------------------------------


def test_pre_cat_ltft_evidence():
    """At least one rule must use longft1 >= 8%% OBD evidence — pre-cat leak signal."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "longft1" and obd.operator == "ge" and obd.value is not None and obd.value >= 8.0:
                found = True
    assert found, "No rule uses longft1 >= 8%% OBD evidence — pre-cat leak path not covered"


def test_post_cat_downstream_o2_evidence():
    """At least one rule must use o2_downstream OBD evidence — post-cat leak signal."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "o2_downstream":
                found = True
    assert found, "No rule uses o2_downstream OBD evidence — post-cat leak path not covered"


def test_probe_tip_hc_o2_evidence():
    """At least one rule must use HC + O2 OBD evidence — probe-tip/manifold dilution signal."""
    rs = _load_ruleset()
    found_hc = False
    found_o2 = False
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "hc" and obd.operator == "ge":
                found_hc = True
            if obd.pid == "o2" and obd.operator == "ge":
                found_o2 = True
    assert found_hc, "No rule uses HC OBD evidence — probe-tip leak path not covered"
    assert found_o2, "No rule uses O2 OBD evidence — probe-tip leak path not covered"


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_pre_cat_lean_dtc():
    """At least one rule must use P0171/P0174 DTC evidence — pre-cat lean DTC signal."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if any(code in ("P0171", "P0174") for code in dtc.dtc_codes):
                found = True
    assert found, "No rule uses P0171/P0174 DTC evidence"


def test_post_cat_trim_dtc():
    """At least one rule must use P2096/P2098 DTC evidence — post-cat trim DTC signal."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if any(code in ("P2096", "P2098") for code in dtc.dtc_codes):
                found = True
    assert found, "No rule uses P2096/P2098 DTC evidence — post-cat leak path not covered"


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
    assert groups == {"exhaust_leak"}, (
        f"All rules should compete in 'exhaust_leak', got {groups}"
    )


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
