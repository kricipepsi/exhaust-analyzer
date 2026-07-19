"""Targeted tests for registry/rules/ecu_fault.json — v2 ecu_fault rule file."""

import json
import pathlib

from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
ECU_FAULT_FILE = RULES_DIR / "ecu_fault.json"


def _load_ruleset():
    data = json.loads(ECU_FAULT_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert ECU_FAULT_FILE.is_file(), f"Missing {ECU_FAULT_FILE}"


def test_valid_json():
    data = json.loads(ECU_FAULT_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "ecu_fault"


def test_exactly_five_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 5, f"Expected 5 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


# ---------------------------------------------------------------------------
# Evidence-tier coverage — OBD fuel trim evidence
# ---------------------------------------------------------------------------


def test_ef001_ef002_ef003_use_longft1_obd():
    """EF-001, EF-002, EF-003 must use longft1 OBD evidence as GATING."""
    rs = _load_ruleset()
    rules_with_longft1 = set()
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "longft1" and obd.tier == EvidenceTier.GATING:
                rules_with_longft1.add(rule.rule_id)
    expected = {"EF-001", "EF-002", "EF-003"}
    missing = expected - rules_with_longft1
    assert not missing, f"Rules missing longft1 GATING OBD evidence: {missing}"


def test_ef001_ef002_ef003_use_shrtft1_obd():
    """EF-001, EF-002, EF-003 must use shrtft1 OBD evidence as GATING."""
    rs = _load_ruleset()
    rules_with_shrtft1 = set()
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "shrtft1" and obd.tier == EvidenceTier.GATING:
                rules_with_shrtft1.add(rule.rule_id)
    expected = {"EF-001", "EF-002", "EF-003"}
    missing = expected - rules_with_shrtft1
    assert not missing, f"Rules missing shrtft1 GATING OBD evidence: {missing}"


def test_ef004_ef005_no_obd_evidence():
    """EF-004 and EF-005 are DTC-primary / chemistry-gated - no OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id in ("EF-004", "EF-005"):
            assert rule.obd_evidence == [], (
                f"{rule.rule_id}: expected empty obd_evidence, "
                f"got {len(rule.obd_evidence)} entries"
            )


def test_lambda_perception_delta_definitive_only_on_obd_primary_rules():
    """Retained FT-8 ECU delta: only EF-001/002/003 get DEFINITIVE lambda evidence."""
    rs = _load_ruleset()
    expected = {
        "EF-001": {("gt", 0.02)},
        "EF-002": {("lt", -0.02)},
        "EF-003": {("gt", 0.03), ("lt", -0.03)},
    }
    observed = {}
    unexpected = []

    for rule in rs.rules:
        entries = [obd for obd in rule.obd_evidence if obd.pid == "lambda_perception_delta"]
        if entries:
            observed[rule.rule_id] = {(obd.operator, obd.value) for obd in entries}
        for obd in entries:
            if rule.rule_id not in expected or obd.tier != EvidenceTier.DEFINITIVE:
                unexpected.append((rule.rule_id, obd.operator, obd.value, obd.tier))

    assert observed == expected
    assert unexpected == []


def test_ef003_uses_in_range_operator():
    """EF-003 must use in_range operator for frozen-trim detection."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-003":
            in_range_ops = [obd for obd in rule.obd_evidence if obd.operator == "in_range"]
            assert len(in_range_ops) >= 2, (
                f"EF-003: expected >=2 in_range OBD entries, got {len(in_range_ops)}"
            )


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_ef001_p0171_dtc():
    """EF-001 must use P0171 DTC SUGGESTIVE evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-001":
            found = any("P0171" in dtc.dtc_codes for dtc in rule.dtc_evidence)
            assert found, "EF-001: missing P0171 DTC evidence"


def test_ef002_p0172_dtc():
    """EF-002 must use P0172 DTC SUGGESTIVE evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-002":
            found = any("P0172" in dtc.dtc_codes for dtc in rule.dtc_evidence)
            assert found, "EF-002: missing P0172 DTC evidence"


def test_ef003_multi_dtc_coverage():
    """EF-003 must cover P0113, P0201, P0606, P0128 in DTC evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-003":
            all_codes = set()
            for dtc in rule.dtc_evidence:
                all_codes.update(dtc.dtc_codes)
            required = {"P0113", "P0201", "P0606", "P0128"}
            missing = required - all_codes
            assert not missing, f"EF-003: DTC evidence missing codes: {missing}"


def test_ef004_p0606_definitive_dtc():
    """EF-004 must use P0606 DTC at DEFINITIVE tier."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-004":
            found = False
            for dtc in rule.dtc_evidence:
                if "P0606" in dtc.dtc_codes and dtc.tier == EvidenceTier.DEFINITIVE:
                    found = True
            assert found, "EF-004: P0606 DTC not at DEFINITIVE tier"


def test_ef005_multi_dtc_coverage():
    """EF-005 must cover P0171, P0172, P0606 in DTC evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-005":
            all_codes = set()
            for dtc in rule.dtc_evidence:
                all_codes.update(dtc.dtc_codes)
            required = {"P0171", "P0172", "P0606"}
            missing = required - all_codes
            assert not missing, f"EF-005: DTC evidence missing codes: {missing}"


# ---------------------------------------------------------------------------
# Chemistry evidence coverage
# ---------------------------------------------------------------------------


def test_ef001_ef002_ef003_empty_chemistry():
    """EF-001, EF-002, EF-003 must have empty chemistry_evidence -
    they are OBD-primary rules with no chemistry gate."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id in ("EF-001", "EF-002", "EF-003"):
            assert rule.chemistry_evidence == [], (
                f"{rule.rule_id}: expected empty chemistry_evidence, "
                f"got {len(rule.chemistry_evidence)} entries"
            )


def test_ef004_timing_retarded_suggestive():
    """EF-004 must carry TIMING_RETARDED as SUGGESTIVE chemistry evidence —
    closes the ~10-case Tier B gap for ecu_fault."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-004":
            found = any(
                chem.state == ChemistryState.TIMING_RETARDED
                and chem.tier == EvidenceTier.SUGGESTIVE
                for chem in rule.chemistry_evidence
            )
            assert found, "EF-004: missing TIMING_RETARDED SUGGESTIVE chemistry"


def test_ef005_sample_invalid_gating():
    """EF-005 must carry SAMPLE_INVALID as GATING chemistry evidence —
    the rule only evaluates when GASLab emits SAMPLE_INVALID."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "EF-005":
            found = any(
                chem.state == ChemistryState.SAMPLE_INVALID
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "EF-005: missing SAMPLE_INVALID GATING chemistry"


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


def test_at_least_two_rules_have_confidence_ceiling():
    """No solo survivor: at least 2 rules must carry confidence_ceiling."""
    rs = _load_ruleset()
    count = sum(1 for r in rs.rules if r.confidence_ceiling is not None)
    assert count >= 2, f"Expected >= 2 rules with confidence_ceiling, got {count}"


def test_low_base_weight_rules_have_confidence_ceiling():
    """Rules with base_weight <= 0.70 must carry a confidence_ceiling."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.base_weight <= 0.70:
            assert rule.confidence_ceiling is not None, (
                f"{rule.rule_id}: base_weight={rule.base_weight} <= 0.70 but no confidence_ceiling"
            )


def test_pre_ft8_weights_and_confidence_ceilings_restored():
    rs = _load_ruleset()
    expected = {
        "EF-001": (0.80, 0.90),
        "EF-002": (0.80, 0.90),
        "EF-003": (0.75, 0.85),
        "EF-004": (0.85, None),
        "EF-005": (0.70, 0.80),
    }
    for rule in rs.rules:
        assert (rule.base_weight, rule.confidence_ceiling) == expected[rule.rule_id]


# ---------------------------------------------------------------------------
# Competition group
# ---------------------------------------------------------------------------


def test_all_rules_in_same_competition_group():
    rs = _load_ruleset()
    groups = set(r.competition_group for r in rs.rules)
    assert groups == {"ecu_fault"}, (
        f"All rules should compete in 'ecu_fault', got {groups}"
    )


# ---------------------------------------------------------------------------
# Total case coverage — all 28 ecu_fault cases assigned
# ---------------------------------------------------------------------------


def test_all_28_cases_assigned():
    """All 28 curated ecu_fault case IDs must appear in at least one rule's
    passes_cases list."""
    rs = _load_ruleset()
    all_assigned = set()
    for rule in rs.rules:
        for cid in rule.passes_cases:
            all_assigned.add(cid)
    expected_28 = {
        "CSV-041", "CSV-043", "CSV-045", "CSV-072",
        "CSV-123", "CSV-124", "CSV-125", "CSV-126",
        "ECU-001", "ECU-002", "ECU-003", "ECU-009",
        "EXP-N002", "EXP-N004", "EXP-N005", "EXP-N027",
        "EXT-221",
        "TC-021",
        "YAML-CSV41", "YAML-CSV43", "YAML-CSV45", "YAML-CSV72",
        "YAML-TC22", "YAML-TC47",
        "case_001", "case_013", "case_027", "case_033",
    }
    missing = expected_28 - all_assigned
    assert not missing, f"Cases not assigned to any rule: {missing}"
    extra = all_assigned - expected_28
    assert not extra, f"Unknown case IDs in passes_cases: {extra}"


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
