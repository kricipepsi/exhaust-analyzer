"""Minimal validation tests for registry.schema_v2."""

import pytest
from pydantic import ValidationError

from registry.schema_v2 import (
    ChemistryState,
    DTCEvidence,
    DTCRoutingTag,
    EvidenceTier,
    FaultFamily,
    OBDEvidence,
    Rule,
    RuleSet,
)


# ---------------------------------------------------------------------------
# Enum sizes — catch accidental regressions in vocabulary mirroring
# ---------------------------------------------------------------------------


def test_chemistry_state_count():
    """Mirror must have all 34 GASLab ChemicalSignature values."""
    assert len(ChemistryState) == 34, f"Expected 34, got {len(ChemistryState)}"


def test_fault_family_count():
    """Must have 16 families (13 existing + 3 new per cvsgaps.md)."""
    assert len(FaultFamily) == 16, f"Expected 16, got {len(FaultFamily)}"


def test_evidence_tier_count():
    assert len(EvidenceTier) == 3


def test_dtc_routing_tag_count():
    """Must have 20 values (19 DTCLab + CYLINDER_FLUID_MISFIRE + UNKNOWN_FORMAT)."""
    actual = len(DTCRoutingTag)
    assert actual >= 19, f"Expected >= 19, got {actual}"


# ---------------------------------------------------------------------------
# Minimal valid rule — the simplest rule that should validate
# ---------------------------------------------------------------------------

MINIMAL_VALID_RULE = {
    "rule_id": "LC-001",
    "fault_family": "lean_condition",
    "description": "Lean mixture confirmed by Brettschneider lambda > 1.03",
    "chemistry_evidence": [
        {
            "state": "LEAN_MIXTURE",
            "tier": "DEFINITIVE",
            "wiki_ref": "GAS_VOCABULARY §3",
        }
    ],
    "base_weight": 0.85,
    "competition_group": "lean_condition",
    "confidence_ceiling": 0.70,
    "passes_cases": ["CSV-016", "CSV-068"],
    "source_wiki_refs": ["GAS_VOCABULARY §3"],
}


def test_minimal_valid_rule_validates():
    rule = Rule.model_validate(MINIMAL_VALID_RULE)
    assert rule.rule_id == "LC-001"
    assert rule.fault_family == FaultFamily.LEAN_CONDITION
    assert len(rule.chemistry_evidence) == 1


def test_minimal_valid_rule_json_roundtrip():
    rule = Rule.model_validate(MINIMAL_VALID_RULE)
    json_str = rule.model_dump_json(indent=2)
    rule2 = Rule.model_validate_json(json_str)
    assert rule2 == rule


# ---------------------------------------------------------------------------
# passes_cases — must not be empty
# ---------------------------------------------------------------------------


def test_empty_passes_cases_rejected():
    data = dict(MINIMAL_VALID_RULE, passes_cases=[])
    with pytest.raises(ValidationError) as exc:
        Rule.model_validate(data)
    errors = str(exc.value)
    assert "passes_cases" in errors.lower() or "1" in errors


# ---------------------------------------------------------------------------
# Enum membership — invented values are rejected
# ---------------------------------------------------------------------------


def test_invalid_chemistry_state_rejected():
    data = dict(MINIMAL_VALID_RULE)
    data["chemistry_evidence"] = [
        {"state": "MADE_UP_STATE", "tier": "DEFINITIVE"}
    ]
    with pytest.raises(ValidationError):
        Rule.model_validate(data)


def test_invalid_fault_family_rejected():
    data = dict(MINIMAL_VALID_RULE, fault_family="nonexistent")
    with pytest.raises(ValidationError):
        Rule.model_validate(data)


def test_invalid_evidence_tier_rejected():
    data = dict(MINIMAL_VALID_RULE)
    data["chemistry_evidence"] = [
        {"state": "LEAN_MIXTURE", "tier": "MADE_UP_TIER"}
    ]
    with pytest.raises(ValidationError):
        Rule.model_validate(data)


# ---------------------------------------------------------------------------
# OBD evidence — operator validation
# ---------------------------------------------------------------------------


def test_obd_in_range_requires_range_bounds():
    with pytest.raises(ValidationError):
        OBDEvidence(
            pid="map_kpa",
            operator="in_range",
            tier=EvidenceTier.SUGGESTIVE,
        )


def test_obd_in_range_rejects_crossed_bounds():
    with pytest.raises(ValidationError):
        OBDEvidence(
            pid="map_kpa",
            operator="in_range",
            range_low=75.0,
            range_high=30.0,
            tier=EvidenceTier.SUGGESTIVE,
        )


def test_obd_scalar_requires_value():
    with pytest.raises(ValidationError):
        OBDEvidence(
            pid="longft1",
            operator="gt",
            tier=EvidenceTier.SUGGESTIVE,
        )


def test_obd_scalar_valid():
    obd = OBDEvidence(
        pid="longft1",
        operator="ge",
        value=10.0,
        tier=EvidenceTier.DEFINITIVE,
        units="%",
        wiki_ref="GAS_VOCABULARY §2",
    )
    assert obd.value == 10.0


# ---------------------------------------------------------------------------
# RuleSet — cross-rule validation
# ---------------------------------------------------------------------------


VALID_RULESET = {
    "fault_family": "lean_condition",
    "rules": [
        {
            "rule_id": "LC-001",
            "fault_family": "lean_condition",
            "description": "Lean mixture from air leak",
            "chemistry_evidence": [
                {"state": "LEAN_MIXTURE", "tier": "DEFINITIVE", "wiki_ref": "GAS_VOCABULARY §3"},
            ],
            "competition_group": "lean_condition",
            "confidence_ceiling": 0.70,
            "passes_cases": ["CSV-016"],
        },
        {
            "rule_id": "LC-002",
            "fault_family": "lean_condition",
            "description": "Lean mixture from vacuum leak — trims correct at 2500 RPM",
            "chemistry_evidence": [
                {"state": "TIMING_RETARDED", "tier": "SUGGESTIVE", "wiki_ref": "GAS_VOCABULARY §3"},
            ],
            "obd_evidence": [
                {
                    "pid": "longft1",
                    "operator": "ge",
                    "value": 10.0,
                    "tier": "SUGGESTIVE",
                    "units": "%",
                    "wiki_ref": "GAS_VOCABULARY §2",
                },
            ],
            "competition_group": "lean_condition",
            "passes_cases": ["CSV-100"],
        },
    ],
}


def test_ruleset_validates():
    rs = RuleSet.model_validate(VALID_RULESET)
    assert rs.version == "2.0"
    assert len(rs.rules) == 2


def test_ruleset_rejects_duplicate_ids():
    data = dict(VALID_RULESET)
    data["rules"] = [dict(VALID_RULESET["rules"][0]), dict(VALID_RULESET["rules"][0])]
    with pytest.raises(ValidationError) as exc:
        RuleSet.model_validate(data)
    assert "duplicate" in str(exc.value).lower()


def test_ruleset_rejects_solo_rule_without_confidence_ceiling():
    solo_rule = dict(VALID_RULESET["rules"][0])
    solo_rule.pop("confidence_ceiling")
    data = dict(VALID_RULESET, rules=[solo_rule])
    with pytest.raises(ValidationError) as exc:
        RuleSet.model_validate(data)
    assert "confidence_ceiling" in str(exc.value).lower()


def test_ruleset_solo_rule_with_ceiling_passes():
    solo_rule = dict(VALID_RULESET["rules"][0])
    solo_rule["confidence_ceiling"] = 0.65
    data = dict(VALID_RULESET, rules=[solo_rule])
    rs = RuleSet.model_validate(data)
    assert len(rs.rules) == 1


# ---------------------------------------------------------------------------
# DTCEvidence
# ---------------------------------------------------------------------------


def test_dtc_evidence_any_match():
    dtc = DTCEvidence(dtc_codes=["P0171", "P0174"], strategy="any_match")
    assert dtc.tier == EvidenceTier.SUGGESTIVE


def test_dtc_evidence_all_match():
    dtc = DTCEvidence(
        dtc_codes=["P0420"],
        strategy="all_match",
        tier=EvidenceTier.DEFINITIVE,
        wiki_ref="DTC_VOCABULARY §4",
    )
    assert dtc.tier == EvidenceTier.DEFINITIVE


def test_dtc_evidence_empty_codes_rejected():
    with pytest.raises(ValidationError):
        DTCEvidence(dtc_codes=[], strategy="any_match")


# ---------------------------------------------------------------------------
# Extra fields are forbidden (no drift from schema)
# ---------------------------------------------------------------------------


def test_rule_rejects_extra_fields():
    data = dict(MINIMAL_VALID_RULE, made_up_field="should_fail")
    with pytest.raises(ValidationError):
        Rule.model_validate(data)


def test_ruleset_rejects_extra_fields():
    data = dict(VALID_RULESET, made_up_field="should_fail")
    with pytest.raises(ValidationError):
        RuleSet.model_validate(data)
