"""Targeted tests for registry/rules/charging_system.json — v2 charging_system rule file.

Family ships with 2 rules (CS-001 + CS-002). All DTC codes are grounded in
DTC_VOCABULARY §15: only P0562, P0563, and P0300 are cited. P0620-P0626
(generator/regulator) are NOT in the wiki and are explicitly forbidden here.

CS-002 is the first rule in the registry to gate on NORMAL_OPERATION chemistry
— a positive evidence-of-absence pattern used to discriminate from misfire-family
rule MF-004. The test_cs_002_ceiling_dominates_mf_004 test reads MF-004 from
rules/misfire.json and asserts CS-002's ceiling is strictly greater; it pins
MF-004's rule_id before comparing so a future renumber of MF-004 fails loudly
rather than silently.
"""

import csv
import json
import pathlib
import re

from registry.schema_v2 import (
    ChemistryState,
    DTCRoutingTag,
    EvidenceTier,
    FaultFamily,
    RuleSet,
)

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
CORPUS_FILE = RULES_DIR.parent / "corpus_curated.csv"
CHARGING_FILE = RULES_DIR / "charging_system.json"
MISFIRE_FILE = RULES_DIR / "misfire.json"

ALLOWED_DTC_CODES = {"P0562", "P0563", "P0300"}


def _load_ruleset() -> RuleSet:
    data = json.loads(CHARGING_FILE.read_text())
    return RuleSet.model_validate(data)


def _load_corpus_case_ids() -> set[str]:
    with open(CORPUS_FILE, newline="") as f:
        return {row["case_id"] for row in csv.DictReader(f)}


def _get_rule(rs: RuleSet, rule_id: str):
    for r in rs.rules:
        if r.rule_id == rule_id:
            return r
    raise AssertionError(f"Rule {rule_id} not found")


# ---------------------------------------------------------------------------
# Structural — file exists, parses, validates
# ---------------------------------------------------------------------------


def test_file_exists():
    assert CHARGING_FILE.is_file(), f"Missing {CHARGING_FILE}"


def test_valid_json():
    data = json.loads(CHARGING_FILE.read_text())
    assert "rules" in data
    assert "fault_family" in data


def test_ruleset_validates():
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family == FaultFamily.CHARGING_SYSTEM


def test_exactly_two_rules():
    rs = _load_ruleset()
    assert len(rs.rules) == 2, f"Expected 2 rules (CS-001 + CS-002), got {len(rs.rules)}"


def test_no_duplicate_rule_ids():
    rs = _load_ruleset()
    ids = [r.rule_id for r in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule_ids: {ids}"


def test_rule_ids_follow_pattern():
    rs = _load_ruleset()
    pat = re.compile(r"^CS-00[12]$")
    for r in rs.rules:
        assert pat.match(r.rule_id), f"rule_id {r.rule_id!r} does not match ^CS-00[12]$"


# ---------------------------------------------------------------------------
# Contract — every rule has passes_cases, every case resolves, every rule
# carries a confidence_ceiling
# ---------------------------------------------------------------------------


def test_every_rule_has_passes_cases():
    rs = _load_ruleset()
    for r in rs.rules:
        assert len(r.passes_cases) >= 1, f"{r.rule_id} has no passes_cases"


def test_every_passes_case_resolves():
    rs = _load_ruleset()
    corpus_ids = _load_corpus_case_ids()
    orphans: list[str] = []
    for r in rs.rules:
        for cid in r.passes_cases:
            if cid not in corpus_ids:
                orphans.append(f"{r.rule_id}: {cid}")
    assert not orphans, f"Orphan case refs (not in corpus_curated.csv): {orphans}"


def test_every_rule_has_confidence_ceiling():
    rs = _load_ruleset()
    for r in rs.rules:
        assert r.confidence_ceiling is not None, (
            f"{r.rule_id} has no confidence_ceiling (no-solo-survivor discipline)"
        )


def test_competition_group_charging_system():
    rs = _load_ruleset()
    for r in rs.rules:
        assert r.competition_group == "charging_system", (
            f"{r.rule_id} competition_group is {r.competition_group!r}, expected 'charging_system'"
        )


# ---------------------------------------------------------------------------
# DTC gating discipline — every rule has at least one GATING DTC entry with
# strategy "any_match"
# ---------------------------------------------------------------------------


def test_every_rule_is_dtc_gated():
    rs = _load_ruleset()
    for r in rs.rules:
        gating = [
            d for d in r.dtc_evidence
            if d.tier == EvidenceTier.GATING and d.strategy == "any_match"
        ]
        assert gating, f"{r.rule_id} has no GATING any_match DTCEvidence entry"


# ---------------------------------------------------------------------------
# CS-001 specifics
# ---------------------------------------------------------------------------


def test_cs_001_dtc_codes():
    rs = _load_ruleset()
    cs_001 = _get_rule(rs, "CS-001")
    gating = [d for d in cs_001.dtc_evidence if d.tier == EvidenceTier.GATING]
    assert len(gating) == 1, f"CS-001 should have exactly 1 GATING DTC entry, got {len(gating)}"
    assert gating[0].dtc_codes == ["P0562", "P0563"], (
        f"CS-001 GATING dtc_codes are {gating[0].dtc_codes}, expected ['P0562', 'P0563']"
    )


def test_cs_001_no_chemistry_no_obd():
    rs = _load_ruleset()
    cs_001 = _get_rule(rs, "CS-001")
    assert cs_001.chemistry_evidence == [], (
        f"CS-001 chemistry_evidence should be empty, got {cs_001.chemistry_evidence}"
    )
    assert cs_001.obd_evidence == [], (
        f"CS-001 obd_evidence should be empty, got {cs_001.obd_evidence}"
    )


def test_cs_001_ceiling_matches_overheating_precedent():
    """CS-001 ceiling = 0.85 matches OV-002 (single-specific-DTC pathognomonic rule)."""
    rs = _load_ruleset()
    cs_001 = _get_rule(rs, "CS-001")
    assert cs_001.confidence_ceiling == 0.85, (
        f"CS-001 ceiling is {cs_001.confidence_ceiling}, expected 0.85 (matches OV-002 precedent)"
    )


# ---------------------------------------------------------------------------
# CS-002 specifics — the novel NORMAL_OPERATION-GATING pattern + MF-004
# competition discipline
# ---------------------------------------------------------------------------


def test_cs_002_has_two_dtc_entries():
    rs = _load_ruleset()
    cs_002 = _get_rule(rs, "CS-002")
    assert len(cs_002.dtc_evidence) == 2, (
        f"CS-002 should have exactly 2 DTCEvidence entries, got {len(cs_002.dtc_evidence)}"
    )


def test_cs_002_charging_dtc_gating():
    rs = _load_ruleset()
    cs_002 = _get_rule(rs, "CS-002")
    gating = [d for d in cs_002.dtc_evidence if d.tier == EvidenceTier.GATING]
    assert len(gating) == 1, f"CS-002 should have exactly 1 GATING DTC entry, got {len(gating)}"
    assert gating[0].dtc_codes == ["P0562", "P0563"], (
        f"CS-002 GATING dtc_codes are {gating[0].dtc_codes}, expected ['P0562', 'P0563']"
    )


def test_cs_002_p0300_suggestive():
    rs = _load_ruleset()
    cs_002 = _get_rule(rs, "CS-002")
    suggestive = [d for d in cs_002.dtc_evidence if d.tier == EvidenceTier.SUGGESTIVE]
    assert len(suggestive) == 1, (
        f"CS-002 should have exactly 1 SUGGESTIVE DTC entry, got {len(suggestive)}"
    )
    assert suggestive[0].dtc_codes == ["P0300"], (
        f"CS-002 SUGGESTIVE dtc_codes are {suggestive[0].dtc_codes}, expected ['P0300']"
    )


def test_cs_002_chemistry_normal_gating():
    """The novel pattern: NORMAL_OPERATION at tier GATING.

    This is the first rule in the registry to gate on NORMAL_OPERATION (as
    opposed to gating on an anomalous chemistry state).  It is the
    discriminator from MF-004.
    """
    rs = _load_ruleset()
    cs_002 = _get_rule(rs, "CS-002")
    assert len(cs_002.chemistry_evidence) == 1, (
        f"CS-002 should have exactly 1 ChemistryEvidence entry, got {len(cs_002.chemistry_evidence)}"
    )
    ce = cs_002.chemistry_evidence[0]
    assert ce.state == ChemistryState.NORMAL_OPERATION, (
        f"CS-002 chemistry state is {ce.state}, expected NORMAL_OPERATION"
    )
    assert ce.tier == EvidenceTier.GATING, (
        f"CS-002 chemistry tier is {ce.tier}, expected GATING"
    )


def test_cs_002_ceiling_dominates_mf_004():
    """CS-002 must strictly outscore MF-004 on the ghost-misfire ambiguity.

    Reads MF-004 directly from rules/misfire.json.  Asserts the fetched rule
    actually has rule_id 'MF-004' before comparing — guards against a silent
    pass if MF-004 is renumbered.
    """
    rs = _load_ruleset()
    cs_002 = _get_rule(rs, "CS-002")
    assert cs_002.confidence_ceiling is not None  # for type narrowing

    mf_data = json.loads(MISFIRE_FILE.read_text())
    mf_004 = None
    for r in mf_data["rules"]:
        if r["rule_id"] == "MF-004":
            mf_004 = r
            break
    assert mf_004 is not None, (
        "MF-004 not found in rules/misfire.json — CS-002 competition discipline "
        "assumes MF-004 exists.  If MF-004 has been renumbered, update CS-002's "
        "ceiling discipline accordingly."
    )
    assert mf_004["rule_id"] == "MF-004"  # pin the rule_id explicitly
    mf_004_ceiling = mf_004.get("confidence_ceiling")
    assert mf_004_ceiling is not None, "MF-004 has no confidence_ceiling"
    assert cs_002.confidence_ceiling > mf_004_ceiling, (
        f"CS-002 ceiling ({cs_002.confidence_ceiling}) must be strictly greater "
        f"than MF-004 ceiling ({mf_004_ceiling}) to dominate the ghost-misfire "
        f"ambiguity discriminator"
    )


# ---------------------------------------------------------------------------
# Schema mirror invariant + wiki-grounding invariant
# ---------------------------------------------------------------------------


def test_no_routing_tag_added():
    """DTCRoutingTag must still have exactly 19 members.

    This task adds NO new enum value.  The mirror with DTCLab is maintained
    manually (schema_v2.py L102-109); any drift must be a coordinated change,
    not a side effect of a rule-authoring task.
    """
    n = len(list(DTCRoutingTag))
    assert n == 19, (
        f"DTCRoutingTag has {n} members, expected 19.  The charging_system "
        f"task must not add routing-tag enum values."
    )


def test_no_unauthorised_dtc_codes():
    """Every DTC code in charging_system.json must be grounded in DTC_VOCABULARY §15.

    Only P0562, P0563, and P0300 are cited.  P0620-P0626 (generator/regulator)
    are NOT in the wiki and are explicitly forbidden here.  If a future task
    wants to add them, the wiki must be updated first.
    """
    data = json.loads(CHARGING_FILE.read_text())
    seen: set[str] = set()
    for r in data["rules"]:
        for de in r.get("dtc_evidence", []):
            for code in de["dtc_codes"]:
                seen.add(code)
    extra = seen - ALLOWED_DTC_CODES
    assert not extra, (
        f"Unauthorised DTC codes in charging_system rules: {sorted(extra)} "
        f"(only {sorted(ALLOWED_DTC_CODES)} grounded in DTC_VOCABULARY §15)"
    )
