"""Targeted tests for registry/rules/cam_timing.json — v2 cam_timing rule file."""

import json
import pathlib

from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
CAM_TIMING_FILE = RULES_DIR / "cam_timing.json"


def _load_ruleset():
    data = json.loads(CAM_TIMING_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert CAM_TIMING_FILE.is_file(), f"Missing {CAM_TIMING_FILE}"


def test_valid_json():
    data = json.loads(CAM_TIMING_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "cam_timing"


def test_exactly_eight_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 8, f"Expected 8 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


# ---------------------------------------------------------------------------
# Chemistry evidence coverage
# ---------------------------------------------------------------------------


def test_ct001_cam_timing_retarded_maf_gating():
    """CT-001 must use CAM_TIMING_RETARDED_MAF chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-001":
            found = any(
                chem.state == ChemistryState.CAM_TIMING_RETARDED_MAF
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "CT-001: missing CAM_TIMING_RETARDED_MAF GATING chemistry"


def test_ct003_ignition_misfire_gating():
    """CT-003 must use IGNITION_MISFIRE chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-003":
            found = any(
                chem.state == ChemistryState.IGNITION_MISFIRE
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "CT-003: missing IGNITION_MISFIRE GATING chemistry"


def test_ct002_ct004_vvt_failure_gating():
    """CT-002 and CT-004 must use VVT_FAILURE chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id in ("CT-002", "CT-004"):
            found = any(
                chem.state == ChemistryState.VVT_FAILURE
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, f"{rule.rule_id}: missing VVT_FAILURE GATING chemistry"


def test_ct002_ct006_timing_retarded_suggestive():
    """CT-002 and CT-006 must carry TIMING_RETARDED as SUGGESTIVE evidence —
    closes the ~3-case Tier B gap for cam_timing."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id in ("CT-002", "CT-006"):
            found = any(
                chem.state == ChemistryState.TIMING_RETARDED
                and chem.tier == EvidenceTier.SUGGESTIVE
                for chem in rule.chemistry_evidence
            )
            assert found, f"{rule.rule_id}: missing TIMING_RETARDED SUGGESTIVE chemistry"


def test_ct005_empty_chemistry():
    """CT-005 must have empty chemistry_evidence — DTC-primary rule with no chemistry gate."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-005":
            assert rule.chemistry_evidence == [], (
                f"CT-005: expected empty chemistry_evidence, got {len(rule.chemistry_evidence)} entries"
            )


def test_ct001_empty_dtc():
    """CT-001 must have empty dtc_evidence — mechanical timing on non-VVT engines
    produces no cam sensor DTC."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-001":
            assert rule.dtc_evidence == [], (
                f"CT-001: expected empty dtc_evidence, got {len(rule.dtc_evidence)} entries"
            )


# ---------------------------------------------------------------------------
# OBD evidence coverage
# ---------------------------------------------------------------------------


def test_ct002_stft_suggestive():
    """CT-002 must use stft_b1 OBD evidence as SUGGESTIVE for phaser lag trim
    compensation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-002":
            found = any(
                obd.pid == "stft_b1" and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "CT-002: missing stft_b1 SUGGESTIVE OBD evidence"


def test_ct004_negative_trim_obd():
    """CT-004 must use stft_b1 and ltft_b1 with negative thresholds as SUGGESTIVE
    — advance/knock pattern pushes trims negative."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-004":
            stft_neg = any(
                obd.pid == "stft_b1" and obd.operator == "le" and obd.value == -5.0
                for obd in rule.obd_evidence
            )
            ltft_neg = any(
                obd.pid == "ltft_b1" and obd.operator == "le" and obd.value == -5.0
                for obd in rule.obd_evidence
            )
            assert stft_neg, "CT-004: missing stft_b1 <= -5.0 OBD evidence"
            assert ltft_neg, "CT-004: missing ltft_b1 <= -5.0 OBD evidence"


def test_ct005_trim_near_zero_obd():
    """CT-005 must use stft_b1 and ltft_b1 in_range for near-zero trim detection —
    solenoid drift causes marginal trim response, not saturation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-005":
            in_range_ops = [obd for obd in rule.obd_evidence if obd.operator == "in_range"]
            assert len(in_range_ops) >= 2, (
                f"CT-005: expected >=2 in_range OBD entries, got {len(in_range_ops)}"
            )


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_ct002_ct004_vvt_dtc_suggestive():
    """CT-002 and CT-004 use P0011/P0012 DTC as SUGGESTIVE evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id in ("CT-002", "CT-004"):
            found = any(
                "P0011" in dtc.dtc_codes and dtc.tier == EvidenceTier.SUGGESTIVE
                for dtc in rule.dtc_evidence
            )
            assert found, f"{rule.rule_id}: missing P0011/P0012 SUGGESTIVE DTC evidence"


def test_ct003_vvt_dtc_definitive():
    """CT-003 promotes VVT DTCs to DEFINITIVE as the FT-10 shared-chemistry discriminator."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-003":
            found = any(
                "P0011" in dtc.dtc_codes and dtc.tier == EvidenceTier.DEFINITIVE
                for dtc in rule.dtc_evidence
            )
            assert found, "CT-003: missing P0011/P0012 DEFINITIVE DTC evidence"


def test_ct005_vvt_history_gating():
    """CT-005 must use VVT_HISTORY range DTCs (P0010-P0025) as GATING evidence
    with any_match strategy."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-005":
            found = False
            for dtc in rule.dtc_evidence:
                if dtc.tier == EvidenceTier.GATING and dtc.strategy == "any_match":
                    vvt_prefix = sum(1 for c in dtc.dtc_codes if c.startswith("P001") or c.startswith("P002"))
                    if vvt_prefix >= 5:
                        found = True
            assert found, "CT-005: missing VVT_HISTORY GATING DTC evidence"


def test_ct006_vvt_dtc_gating():
    """CT-006 must use VVT DTCs (P0011-P0024) as GATING evidence with any_match
    strategy."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-006":
            found = False
            for dtc in rule.dtc_evidence:
                if dtc.tier == EvidenceTier.GATING and dtc.strategy == "any_match":
                    if "P0011" in dtc.dtc_codes and "P0012" in dtc.dtc_codes:
                        found = True
            assert found, "CT-006: missing VVT DTC GATING evidence"


def test_ct007_vvt_dtc_gating_shared_chemistry_bridge():
    """CT-007 must gate shared bad-combustion chemistry behind VVT DTC evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-007":
            dtc_gate = any(
                dtc.tier == EvidenceTier.GATING
                and dtc.strategy == "any_match"
                and "P0011" in dtc.dtc_codes
                and "P0012" in dtc.dtc_codes
                for dtc in rule.dtc_evidence
            )
            chem_states = {chem.state for chem in rule.chemistry_evidence}
            assert dtc_gate, "CT-007: missing VVT DTC GATING evidence"
            assert ChemistryState.INCOMPLETE_COMBUSTION in chem_states
            assert ChemistryState.SAMPLE_INVALID in chem_states
            assert ChemistryState.VVT_FAILURE in chem_states


def test_ct008_no_dtc_incomplete_combustion_bridge():
    """CT-008 covers the no-DTC non-VVT incomplete-combustion cam timing signature."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-008":
            chem_gate = any(
                chem.state == ChemistryState.INCOMPLETE_COMBUSTION
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            no_shadow_dtc_gate = any(
                dtc.strategy == "none_present"
                and dtc.tier == EvidenceTier.GATING
                and "P0171" in dtc.dtc_codes
                and "P0300" in dtc.dtc_codes
                and "P0011" in dtc.dtc_codes
                for dtc in rule.dtc_evidence
            )
            assert chem_gate, "CT-008: missing INCOMPLETE_COMBUSTION GATING chemistry"
            assert no_shadow_dtc_gate, "CT-008: missing no-shadow DTC none_present gate"
            assert any(
                obd.pid == "hc" and obd.tier == EvidenceTier.DEFINITIVE
                for obd in rule.obd_evidence
            ), "CT-008: missing definitive HC window evidence"
            assert rule.base_weight <= 0.80, "CT-008 must win through evidence, not base weight"


# ---------------------------------------------------------------------------
# Non-VVT path (CT-001)
# ---------------------------------------------------------------------------


def test_ct001_no_vvt_precondition():
    """CT-001 must NOT require vvt_equipped — closes the v1 gap where
    4 of 5 rules required vvt_equipped: true."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "CT-001":
            pre = rule.precondition or ""
            assert "vvt_equipped: true" not in pre, (
                f"CT-001: must not require vvt_equipped, got precondition='{pre}'"
            )


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
                f"{rule.rule_id}: OBD pid '{obd.pid}' has no wiki_ref"
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


# ---------------------------------------------------------------------------
# Competition group
# ---------------------------------------------------------------------------


def test_all_rules_in_same_competition_group():
    rs = _load_ruleset()
    groups = set(r.competition_group for r in rs.rules)
    assert groups == {"cam_timing"}, (
        f"All rules should compete in 'cam_timing', got {groups}"
    )


# ---------------------------------------------------------------------------
# Total case coverage — all 8 coverable cam_timing cases assigned
# ---------------------------------------------------------------------------


def test_all_8_coverable_cases_assigned():
    """All 8 coverable curated cam_timing case IDs must appear in at least one
    rule's passes_cases list. EXP-N023 is excluded — uncoverable with current
    OBD PID set (no DTC, no MAP, no RPM)."""
    rs = _load_ruleset()
    all_assigned = set()
    for rule in rs.rules:
        for cid in rule.passes_cases:
            all_assigned.add(cid)
    expected_8 = {
        "MECH-004",
        "CSV-115", "CSV-116",
        "EXT-209", "EXT-210",
        "CASE-018",
        "EXP-N007",
        "case_042",
    }
    missing = expected_8 - all_assigned
    assert not missing, f"Cases not assigned to any rule: {missing}"


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
