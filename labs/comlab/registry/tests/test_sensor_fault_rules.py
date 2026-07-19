"""Targeted tests for registry/rules/sensor_fault.json — v2 sensor_fault rule file."""

import json
import pathlib

from registry.schema_v2 import ChemistryState, EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
SENSOR_FAULT_FILE = RULES_DIR / "sensor_fault.json"


def _load_ruleset():
    data = json.loads(SENSOR_FAULT_FILE.read_text())
    return RuleSet.model_validate(data)


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert SENSOR_FAULT_FILE.is_file(), f"Missing {SENSOR_FAULT_FILE}"


def test_valid_json():
    data = json.loads(SENSOR_FAULT_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "sensor_fault"


def test_exactly_eight_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 8, f"Expected 8 rules, got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


# ---------------------------------------------------------------------------
# Evidence-tier coverage — chemistry states
# ---------------------------------------------------------------------------


def test_sf008_no_chemistry_gate():
    """SF-008 is the catch-all rule: no chemistry evidence, no o2_voltage gate.
    Fires on lambda_perception_delta + trim response for sensor_fault cases where
    freeze-frame o2_voltage is absent and GASLab cannot classify the mixture.
    (FT-8 session 2: NORMAL_OPERATION GATING on SF-001/SF-002 was tried and reverted
    — it killed all 10 sensor_fault gains.) """
    rs = _load_ruleset()
    sf008 = next(r for r in rs.rules if r.rule_id == "SF-008")
    assert sf008.chemistry_evidence == [], (
        f"SF-008: expected empty chemistry_evidence, got {len(sf008.chemistry_evidence)} entries"
    )
    # SF-008 must use lambda_perception_delta as DEFINITIVE (both gt/lt)
    lpd_definitive = [e for e in sf008.obd_evidence
                      if e.pid == "lambda_perception_delta" and e.tier == EvidenceTier.DEFINITIVE]
    assert len(lpd_definitive) >= 2, (
        f"SF-008: expected >=2 lambda_perception_delta DEFINITIVE entries, got {len(lpd_definitive)}"
    )
    # SF-008 must use trim evidence as SUGGESTIVE
    trim_suggestive = [e for e in sf008.obd_evidence
                       if e.pid in ("shrtft1", "longft1") and e.tier == EvidenceTier.SUGGESTIVE]
    assert len(trim_suggestive) >= 2, (
        f"SF-008: expected >=2 trim SUGGESTIVE entries, got {len(trim_suggestive)}"
    )
    # SF-008 must carry confidence_ceiling (catch-all, not definitive)
    assert sf008.confidence_ceiling is not None, "SF-008: missing confidence_ceiling"
    assert sf008.confidence_ceiling <= 0.90, (
        f"SF-008: confidence_ceiling {sf008.confidence_ceiling} too high for catch-all"
    )


def test_o2_sensor_biased_high_definitive():
    """SF-001 must carry O2_SENSOR_BIASED_HIGH as DEFINITIVE (FT-8: promoted from SUGGESTIVE)."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if (
                chem.state == ChemistryState.O2_SENSOR_BIASED_HIGH
                and chem.tier == EvidenceTier.DEFINITIVE
            ):
                found = True
    assert found, "No rule uses O2_SENSOR_BIASED_HIGH DEFINITIVE chemistry (FT-8: should be SF-001)"


def test_o2_sensor_biased_low_definitive():
    """SF-002 must carry O2_SENSOR_BIASED_LOW as DEFINITIVE (FT-8: promoted from SUGGESTIVE)."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if (
                chem.state == ChemistryState.O2_SENSOR_BIASED_LOW
                and chem.tier == EvidenceTier.DEFINITIVE
            ):
                found = True
    assert found, "No rule uses O2_SENSOR_BIASED_LOW DEFINITIVE chemistry (FT-8: should be SF-002)"


def test_timing_retarded_suggestive_in_at_least_two_rules():
    """SF-005 and SF-006 use TIMING_RETARDED as SUGGESTIVE evidence."""
    rs = _load_ruleset()
    count = 0
    for rule in rs.rules:
        for chem in rule.chemistry_evidence:
            if (
                chem.state == ChemistryState.TIMING_RETARDED
                and chem.tier == EvidenceTier.SUGGESTIVE
            ):
                count += 1
    assert count >= 2, (
        f"Expected >= 2 rules with TIMING_RETARDED SUGGESTIVE, got {count}"
    )


# ---------------------------------------------------------------------------
# OBD evidence coverage
# ---------------------------------------------------------------------------


def test_o2_voltage_evidence():
    """SF-001, SF-002, SF-003, SF-007 must use o2_voltage OBD evidence."""
    rs = _load_ruleset()
    rules_with_o2_voltage = set()
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "o2_voltage":
                rules_with_o2_voltage.add(rule.rule_id)
    expected = {"SF-001", "SF-002", "SF-003", "SF-007"}
    missing = expected - rules_with_o2_voltage
    assert not missing, f"Rules missing o2_voltage OBD evidence: {missing}"


def test_maf_evidence():
    """SF-004 must use maf OBD evidence."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "maf":
                found = True
    assert found, "No rule uses maf OBD evidence — MAF sensor path not covered"


def test_map_kpa_evidence():
    """SF-005 must use map_kpa OBD evidence."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "map_kpa":
                found = True
    assert found, "No rule uses map_kpa OBD evidence — MAP sensor path not covered"


def test_ect_c_evidence():
    """SF-006 must use ect_c OBD evidence."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "ect_c":
                found = True
    assert found, "No rule uses ect_c OBD evidence — ECT sensor path not covered"


def test_o2_downstream_evidence():
    """SF-006 must use o2_downstream OBD evidence."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.pid == "o2_downstream":
                found = True
    assert found, "No rule uses o2_downstream OBD evidence — downstream O2 path not covered"


def test_gating_evidence_present():
    """SF-003 and SF-007 must use GATING-tier OBD evidence."""
    rs = _load_ruleset()
    rules_with_gating = set()
    for rule in rs.rules:
        for obd in rule.obd_evidence:
            if obd.tier == EvidenceTier.GATING:
                rules_with_gating.add(rule.rule_id)
    expected = {"SF-003", "SF-007"}
    missing = expected - rules_with_gating
    assert not missing, f"Rules missing GATING OBD evidence: {missing}"


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_o2_circuit_dtc_evidence():
    """SF-003 must use P0131/P0132/P0134 DTC evidence."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if any(code in ("P0131", "P0132", "P0134") for code in dtc.dtc_codes):
                found = True
    assert found, "No rule uses P0131/P0132/P0134 DTC evidence"


def test_maf_dtc_evidence():
    """SF-004 must use P0172 DTC evidence."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if "P0172" in dtc.dtc_codes:
                found = True
    assert found, "No rule uses P0172 DTC evidence"


def test_heater_dtc_evidence():
    """SF-007 must use P0053 DTC evidence."""
    rs = _load_ruleset()
    found = False
    for rule in rs.rules:
        for dtc in rule.dtc_evidence:
            if "P0053" in dtc.dtc_codes:
                found = True
    assert found, "No rule uses P0053 DTC evidence"


# ---------------------------------------------------------------------------
# Perception flag coverage
# ---------------------------------------------------------------------------


def test_perception_flag_on_o2_bias_rules():
    """SF-001 and SF-002 must carry perception_flag matching their O2 bias."""
    rs = _load_ruleset()
    flags = {}
    for rule in rs.rules:
        if rule.perception_flag is not None:
            flags[rule.rule_id] = rule.perception_flag
    assert "SF-001" in flags, "SF-001 missing perception_flag"
    assert "SF-002" in flags, "SF-002 missing perception_flag"
    assert flags["SF-001"] == "O2_SENSOR_BIASED_HIGH", (
        f"SF-001 perception_flag expected O2_SENSOR_BIASED_HIGH, got {flags['SF-001']}"
    )
    assert flags["SF-002"] == "O2_SENSOR_BIASED_LOW", (
        f"SF-002 perception_flag expected O2_SENSOR_BIASED_LOW, got {flags['SF-002']}"
    )


def test_no_perception_flag_on_non_o2_rules():
    """SF-003 through SF-007 must not carry perception_flag."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id in ("SF-001", "SF-002"):
            continue
        assert rule.perception_flag is None, (
            f"{rule.rule_id}: perception_flag must be null, got '{rule.perception_flag}'"
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


def test_at_least_two_rules_have_confidence_ceiling():
    """No solo survivor: at least 2 rules must carry confidence_ceiling."""
    rs = _load_ruleset()
    count = sum(1 for r in rs.rules if r.confidence_ceiling is not None)
    assert count >= 2, f"Expected >= 2 rules with confidence_ceiling, got {count}"


# ---------------------------------------------------------------------------
# Competition group
# ---------------------------------------------------------------------------


def test_all_rules_in_same_competition_group():
    rs = _load_ruleset()
    groups = set(r.competition_group for r in rs.rules)
    assert groups == {"sensor_fault"}, (
        f"All rules should compete in 'sensor_fault', got {groups}"
    )


# ---------------------------------------------------------------------------
# Reactivation of all 6 v1 sensor-fault subtypes
# ---------------------------------------------------------------------------


def test_all_v1_subtypes_reactivated():
    """Every v1 sensor-fault KG node (ERR-SF-001 through ERR-SF-006) must have a
    corresponding v2 rule.  SF-001/SF-002 = ERR-SF-001 (two perception paths),
    SF-003 = ERR-SF-002, SF-004 = ERR-SF-003, SF-005 = ERR-SF-004,
    SF-006 = ERR-SF-005 + ERR-SF-006 merged, SF-007 = heater (new v2),
    SF-008 = catch-all for cases without chemistry/o2_voltage (FT-8).
    """
    rs = _load_ruleset()
    ids = {r.rule_id for r in rs.rules}
    expected = {f"SF-{n:03d}" for n in range(1, 9)}
    assert ids == expected, f"Rule IDs: {sorted(ids)} — expected {sorted(expected)}"


# ---------------------------------------------------------------------------
# chemistry_evidence: [] is valid for OBD-primary rules
# ---------------------------------------------------------------------------


def test_empty_chemistry_evidence_valid():
    """SF-004 (MAF), SF-007 (heater), and SF-008 (catch-all) may have empty
    chemistry_evidence — they are OBD-primary rules with no chemistry gate."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id in ("SF-004", "SF-007", "SF-008"):
            assert rule.chemistry_evidence == [], (
                f"{rule.rule_id}: expected empty chemistry_evidence, "
                f"got {len(rule.chemistry_evidence)} entries"
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


# ---------------------------------------------------------------------------
# Total case count
# ---------------------------------------------------------------------------


def test_total_passes_cases_count():
    """20 curated sensor_fault cases assigned to rules (was 19; +1 from SF-008:
    case_046 which was previously unassigned)."""
    rs = _load_ruleset()
    all_cases = set()
    for rule in rs.rules:
        for cid in rule.passes_cases:
            all_cases.add(cid)
    assert len(all_cases) == 20, (
        f"Expected 20 distinct case IDs across all rules, got {len(all_cases)}: {sorted(all_cases)}"
    )
