"""Targeted tests for registry/rules/non_starter.json — v2 non_starter rule file."""

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
NON_STARTER_FILE = RULES_DIR / "non_starter.json"


def _load_ruleset():
    data = json.loads(NON_STARTER_FILE.read_text())
    return RuleSet.model_validate(data)


def _load_corpus_case_ids():
    with open(CORPUS_FILE, newline="") as f:
        return {row["case_id"] for row in csv.DictReader(f)}


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert NON_STARTER_FILE.is_file(), f"Missing {NON_STARTER_FILE}"


def test_valid_json():
    data = json.loads(NON_STARTER_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family == FaultFamily.NON_STARTER


def test_exactly_four_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 4, f"Expected 4 rules, got {len(rs.rules)}"


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


def test_ns001_lean_misfire_gating():
    """NS-001 must use LEAN_MISFIRE chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-001":
            found = any(
                chem.state == ChemistryState.LEAN_MISFIRE
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "NS-001: missing LEAN_MISFIRE GATING chemistry"


def test_ns002_rich_misfire_gating():
    """NS-002 must use RICH_MISFIRE chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-002":
            found = any(
                chem.state == ChemistryState.RICH_MISFIRE
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "NS-002: missing RICH_MISFIRE GATING chemistry"


def test_ns003_incomplete_combustion_gating():
    """NS-003 must use INCOMPLETE_COMBUSTION chemistry as GATING."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-003":
            found = any(
                chem.state == ChemistryState.INCOMPLETE_COMBUSTION
                and chem.tier == EvidenceTier.GATING
                for chem in rule.chemistry_evidence
            )
            assert found, "NS-003: missing INCOMPLETE_COMBUSTION GATING chemistry"


def test_ns004_lean_misfire_suggestive():
    """NS-004 must accept LEAN_MISFIRE chemistry as SUGGESTIVE evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-004":
            found = any(
                chem.state == ChemistryState.LEAN_MISFIRE
                and chem.tier == EvidenceTier.SUGGESTIVE
                for chem in rule.chemistry_evidence
            )
            assert found, "NS-004: missing LEAN_MISFIRE SUGGESTIVE chemistry"


# ---------------------------------------------------------------------------
# OBD evidence coverage
# ---------------------------------------------------------------------------


def test_ns001_rpm_suggestive():
    """NS-001 must carry rpm < 600 as SUGGESTIVE OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-001":
            found = any(
                obd.pid == "rpm" and obd.operator == "lt"
                and obd.value == 600 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "NS-001: missing rpm < 600 SUGGESTIVE OBD evidence"


def test_ns001_co2_suggestive():
    """NS-001 must carry co2 < 5.0 as SUGGESTIVE OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-001":
            found = any(
                obd.pid == "co2" and obd.operator == "lt"
                and obd.value == 5.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "NS-001: missing co2 < 5.0 SUGGESTIVE OBD evidence"


def test_ns001_frozen_trims_suggestive():
    """NS-001 must carry stft and ltft frozen-at-zero OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-001":
            stft_found = any(
                obd.pid == "stft_b1" and obd.operator == "in_range"
                and obd.range_low == -1.0 and obd.range_high == 1.0
                and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            ltft_found = any(
                obd.pid == "ltft_b1" and obd.operator == "in_range"
                and obd.range_low == -1.0 and obd.range_high == 1.0
                and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert stft_found, "NS-001: missing stft_b1 in_range [-1,1] SUGGESTIVE"
            assert ltft_found, "NS-001: missing ltft_b1 in_range [-1,1] SUGGESTIVE"


def test_ns002_ect_suggestive():
    """NS-002 must carry ect_c < 30.0 as SUGGESTIVE OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-002":
            found = any(
                obd.pid == "ect_c" and obd.operator == "lt"
                and obd.value == 30.0 and obd.tier == EvidenceTier.SUGGESTIVE
                for obd in rule.obd_evidence
            )
            assert found, "NS-002: missing ect_c < 30.0 SUGGESTIVE OBD evidence"


def test_ns003_rpm_gating():
    """NS-003 must carry rpm < 600 as GATING OBD evidence."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-003":
            found = any(
                obd.pid == "rpm" and obd.operator == "lt"
                and obd.value == 600 and obd.tier == EvidenceTier.GATING
                for obd in rule.obd_evidence
            )
            assert found, "NS-003: missing rpm < 600 GATING OBD evidence"


# ---------------------------------------------------------------------------
# DTC evidence coverage
# ---------------------------------------------------------------------------


def test_ns004_dtc_any_match_gating():
    """NS-004 must gate on fuel-delivery DTCs with strategy any_match."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-004":
            assert len(rule.dtc_evidence) == 1, (
                f"NS-004: expected exactly 1 DTC evidence entry, got {len(rule.dtc_evidence)}"
            )
            dtc = rule.dtc_evidence[0]
            assert dtc.strategy == "any_match"
            assert dtc.tier == EvidenceTier.GATING
            codes = dtc.dtc_codes
            assert "P0230" in codes, "NS-004: missing P0230 in DTC list"
            assert "P0087" in codes, "NS-004: missing P0087 in DTC list"
            assert "P0190" in codes, "NS-004: missing P0190 in DTC list"


# ---------------------------------------------------------------------------
# Wiki citations on numeric thresholds
# ---------------------------------------------------------------------------


def test_ns001_obd_wiki_refs():
    """NS-001: every OBD entry with a numeric threshold must carry wiki_ref."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-001":
            for obd in rule.obd_evidence:
                assert obd.wiki_ref is not None, (
                    f"NS-001: OBD {obd.pid} missing wiki_ref"
                )


def test_ns002_ect_wiki_ref():
    """NS-002 ect_c threshold must carry a wiki_ref citation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-002":
            for obd in rule.obd_evidence:
                if obd.pid == "ect_c":
                    assert obd.wiki_ref is not None, (
                        "NS-002: ect_c threshold missing wiki_ref"
                    )


def test_ns003_obd_wiki_refs():
    """NS-003: every OBD entry with a numeric threshold must carry wiki_ref."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-003":
            for obd in rule.obd_evidence:
                assert obd.wiki_ref is not None, (
                    f"NS-003: OBD {obd.pid} missing wiki_ref"
                )


def test_ns004_dtc_wiki_ref():
    """NS-004 DTC evidence must carry a wiki_ref citation."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.rule_id == "NS-004":
            for dtc in rule.dtc_evidence:
                assert dtc.wiki_ref is not None, (
                    "NS-004: DTC evidence missing wiki_ref"
                )


# ---------------------------------------------------------------------------
# Competition group integrity
# ---------------------------------------------------------------------------


def test_competition_group_non_starter():
    """All rules must belong to non_starter competition group."""
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.competition_group == "non_starter", (
            f"{rule.rule_id}: expected competition_group 'non_starter', "
            f"got '{rule.competition_group}'"
        )


def test_no_solo_survivor():
    """At least 2 rules must carry confidence_ceiling."""
    rs = _load_ruleset()
    ceiling_count = sum(1 for r in rs.rules if r.confidence_ceiling is not None)
    assert ceiling_count >= 2, (
        f"Only {ceiling_count} rule(s) carry confidence_ceiling; "
        "need >= 2 (no-solo-survivor discipline)"
    )


def test_all_rules_have_confidence_ceiling():
    """Every non_starter rule must carry confidence_ceiling — all 3 chemistry
    states (LEAN_MISFIRE, RICH_MISFIRE, INCOMPLETE_COMBUSTION) are shared with
    other families, and NS-004 is a DTC-only fallback."""
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.confidence_ceiling is not None, (
            f"{rule.rule_id}: must set confidence_ceiling — "
            "all non_starter rules share chemistry or are DTC-only"
        )


def test_confidence_ceiling_values_in_range():
    """All confidence_ceiling values must be in [0.0, 1.0]."""
    rs = _load_ruleset()
    for rule in rs.rules:
        if rule.confidence_ceiling is not None:
            assert 0.0 <= rule.confidence_ceiling <= 1.0, (
                f"{rule.rule_id}: confidence_ceiling {rule.confidence_ceiling} out of range"
            )


def test_base_weights_in_range():
    """All base_weight values must be in [0.0, 1.0]."""
    rs = _load_ruleset()
    for rule in rs.rules:
        assert 0.0 <= rule.base_weight <= 1.0, (
            f"{rule.rule_id}: base_weight {rule.base_weight} out of range"
        )


# ---------------------------------------------------------------------------
# Coverage — all 4 non_starter cases appear in at least one passes_cases
# ---------------------------------------------------------------------------


def test_all_non_starter_cases_covered():
    """Every non_starter case in corpus_curated.csv must appear in >= 1 rule."""
    rs = _load_ruleset()
    all_passes = set()
    for rule in rs.rules:
        all_passes.update(rule.passes_cases)

    ns_cases = set()
    with open(CORPUS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("expected_top_fault_family") == "non_starter":
                ns_cases.add(row["case_id"])

    uncovered = ns_cases - all_passes
    assert not uncovered, (
        f"Non_starter cases not covered by any rule: {sorted(uncovered)}"
    )


# ---------------------------------------------------------------------------
# Rule count by case — REAL-001 and REAL-003 have competing rules
# ---------------------------------------------------------------------------


def test_real001_has_competing_rules():
    """REAL-001 must be covered by >= 2 rules (LEAN_MISFIRE + INCOMPLETE_COMBUSTION)."""
    rs = _load_ruleset()
    rule_count = sum(1 for r in rs.rules if "REAL-001" in r.passes_cases)
    assert rule_count >= 2, (
        f"REAL-001: covered by only {rule_count} rule(s); "
        "produces multiple chemistry states and needs competing rules"
    )


def test_real003_has_competing_rules():
    """REAL-003 must be covered by >= 2 rules (RICH_MISFIRE + INCOMPLETE_COMBUSTION)."""
    rs = _load_ruleset()
    rule_count = sum(1 for r in rs.rules if "REAL-003" in r.passes_cases)
    assert rule_count >= 2, (
        f"REAL-003: covered by only {rule_count} rule(s); "
        "produces multiple chemistry states and needs competing rules"
    )
