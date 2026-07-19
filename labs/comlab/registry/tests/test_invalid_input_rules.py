"""Targeted tests for registry/rules/invalid_input.json."""

import ast
import json
import pathlib
from typing import Any

from registry.integration_shim import RegistryV2Router
from registry.schema_v2 import EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
INVALID_INPUT_FILE = RULES_DIR / "invalid_input.json"
CORPUS_FILE = RULES_DIR.parent / "TestSuite" / "cases_petrol_master_v6.csv"


def _load_ruleset() -> RuleSet:
    data = json.loads(INVALID_INPUT_FILE.read_text(encoding="utf-8"))
    return RuleSet.model_validate(data)


def _route(payload: dict[str, Any]) -> tuple[str, str]:
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    family = output["diagnostic_verdict"]["fault_family"]
    return family, str(diagnostics["winner_rule_id"])


def _payload(
    *,
    chemical_state: str = "NORMAL_OPERATION",
    hc: float = 10.0,
    co: float = 0.1,
    co2: float = 15.0,
    o2: float = 0.3,
    nox: float = 25.0,
    dtcs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "metadata": {"session_id": "00000000-0000-4000-8000-000000000000"},
        "horizon_ctx": "HORIZON_MODERN",
        "degradation_mode": "FULL_FUSION",
        "gas_lab_output": {
            "chemical_state": chemical_state,
            "sample_validity": "VALID",
            "gas_hc": hc,
            "gas_co": co,
            "gas_co2": co2,
            "gas_o2": o2,
            "gas_nox": nox,
        },
        "obd_live_data": {"normalized_obd_lambda": 1.0},
        "dtc_lab_output": {
            "confirmed_dtcs": dtcs or [],
            "routing_tags": [],
            "freeze_frame": {},
        },
    }


# ---------------------------------------------------------------------------
# Structural tests
# ---------------------------------------------------------------------------


def test_file_exists() -> None:
    assert INVALID_INPUT_FILE.is_file(), f"Missing {INVALID_INPUT_FILE}"


def test_valid_json() -> None:
    data = json.loads(INVALID_INPUT_FILE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_ruleset_validates() -> None:
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "invalid_input"
    assert len(rs.rules) == 2


def test_no_duplicate_rule_ids() -> None:
    rs = _load_ruleset()
    ids = [rule.rule_id for rule in rs.rules]
    assert len(ids) == len(set(ids)), f"Duplicate rule IDs: {ids}"
    assert set(ids) == {"II-001", "II-002"}


def test_every_rule_is_gating_tight() -> None:
    rs = _load_ruleset()
    for rule in rs.rules:
        evidence = [
            *rule.chemistry_evidence,
            *rule.obd_evidence,
            *rule.dtc_evidence,
        ]
        assert evidence, f"{rule.rule_id}: expected evidence rows"
        assert all(ev.tier == EvidenceTier.GATING for ev in evidence), (
            f"{rule.rule_id}: invalid_input rules must be GATING-tight"
        )


# ---------------------------------------------------------------------------
# passes_cases
# ---------------------------------------------------------------------------


def test_every_rule_has_passes_cases() -> None:
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.passes_cases, f"{rule.rule_id}: passes_cases must not be empty"
        assert len(rule.passes_cases) >= 1, (
            f"{rule.rule_id}: expected >= 1 case in passes_cases"
        )


# ---------------------------------------------------------------------------
# II-001 evidence tests
# ---------------------------------------------------------------------------


def test_ii001_has_exactly_one_obd_evidence() -> None:
    rs = _load_ruleset()
    ii001 = next(r for r in rs.rules if r.rule_id == "II-001")
    assert len(ii001.obd_evidence) == 1
    assert ii001.chemistry_evidence == []
    assert ii001.dtc_evidence == []


def test_ii001_co2_gt_16_gating() -> None:
    rs = _load_ruleset()
    ii001 = next(r for r in rs.rules if r.rule_id == "II-001")
    ev = ii001.obd_evidence[0]
    assert ev.pid == "co2"
    assert ev.operator == "gt"
    assert ev.value == 16.0
    assert ev.tier == EvidenceTier.GATING


# ---------------------------------------------------------------------------
# II-002 evidence tests
# ---------------------------------------------------------------------------


def test_ii002_has_exactly_two_obd_evidence() -> None:
    rs = _load_ruleset()
    ii002 = next(r for r in rs.rules if r.rule_id == "II-002")
    assert len(ii002.obd_evidence) == 2
    assert ii002.chemistry_evidence == []
    assert ii002.dtc_evidence == []


def test_ii002_o2_gt_18_gating() -> None:
    rs = _load_ruleset()
    ii002 = next(r for r in rs.rules if r.rule_id == "II-002")
    o2_ev = next(ev for ev in ii002.obd_evidence if ev.pid == "o2")
    assert o2_ev.operator == "gt"
    assert o2_ev.value == 18.0
    assert o2_ev.tier == EvidenceTier.GATING


def test_ii002_co2_lt_5_gating() -> None:
    rs = _load_ruleset()
    ii002 = next(r for r in rs.rules if r.rule_id == "II-002")
    co2_ev = next(ev for ev in ii002.obd_evidence if ev.pid == "co2")
    assert co2_ev.operator == "lt"
    assert co2_ev.value == 5.0
    assert co2_ev.tier == EvidenceTier.GATING


# ---------------------------------------------------------------------------
# Competition group and confidence tests
# ---------------------------------------------------------------------------


def test_competition_group_invalid_input() -> None:
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.competition_group == "invalid_input", (
            f"{rule.rule_id}: expected competition_group 'invalid_input'"
        )


def test_all_rules_have_confidence_ceiling() -> None:
    rs = _load_ruleset()
    for rule in rs.rules:
        assert rule.confidence_ceiling is not None, (
            f"{rule.rule_id}: expected confidence_ceiling"
        )


def test_confidence_ceiling_values_in_range() -> None:
    rs = _load_ruleset()
    for rule in rs.rules:
        ceiling = rule.confidence_ceiling
        assert ceiling is not None, f"{rule.rule_id}: expected confidence_ceiling"
        assert 0.0 <= ceiling <= 1.0, (
            f"{rule.rule_id}: confidence_ceiling {ceiling} out of range"
        )


def test_base_weights_in_range() -> None:
    rs = _load_ruleset()
    for rule in rs.rules:
        assert 0.0 <= rule.base_weight <= 1.0, (
            f"{rule.rule_id}: base_weight {rule.base_weight} out of range"
        )


def test_no_solo_survivor() -> None:
    rs = _load_ruleset()
    with_ceiling = [r for r in rs.rules if r.confidence_ceiling is not None]
    assert len(with_ceiling) >= 2, "fewer than 2 rules carry confidence_ceiling"


# ---------------------------------------------------------------------------
# Wiki citation tests
# ---------------------------------------------------------------------------


def test_ii001_obd_evidence_has_wiki_ref() -> None:
    rs = _load_ruleset()
    ii001 = next(r for r in rs.rules if r.rule_id == "II-001")
    for ev in ii001.obd_evidence:
        assert ev.wiki_ref, f"{ii001.rule_id}: obd evidence missing wiki_ref"


def test_ii002_obd_evidence_has_wiki_ref() -> None:
    rs = _load_ruleset()
    ii002 = next(r for r in rs.rules if r.rule_id == "II-002")
    for ev in ii002.obd_evidence:
        assert ev.wiki_ref, f"{ii002.rule_id}: obd evidence missing wiki_ref"


# ---------------------------------------------------------------------------
# Router integration tests
# ---------------------------------------------------------------------------


def test_ii001_fires_on_co2_above_16() -> None:
    family, winner = _route(_payload(co2=17.0, o2=0.3))
    assert family == "invalid_input", f"got {family}, expected invalid_input"
    assert winner == "II-001", f"got {winner}, expected II-001"


def test_ii002_fires_on_o2_above_18_and_co2_below_5() -> None:
    family, winner = _route(_payload(co2=3.0, o2=19.0))
    assert family == "invalid_input", f"got {family}, expected invalid_input"
    assert winner == "II-002", f"got {winner}, expected II-002"


def test_invalid_input_does_not_fire_on_normal_gas() -> None:
    family, _ = _route(_payload(co2=15.0, o2=0.3))
    assert family != "invalid_input", "invalid_input fired on normal gas"


def test_invalid_input_does_not_shadow_lean_condition() -> None:
    family, winner = _route(
        _payload(
            chemical_state="LEAN_MIXTURE",
            hc=45.0,
            co=0.02,
            co2=11.5,
            o2=4.5,
            nox=120.0,
        )
    )
    assert family == "lean_condition", f"got {family}, expected lean_condition"
    assert winner.startswith("LC-")


def test_invalid_input_does_not_shadow_misfire() -> None:
    family, winner = _route(
        _payload(
            chemical_state="IGNITION_MISFIRE",
            hc=250.0,
            co=0.3,
            co2=13.0,
            o2=2.0,
            nox=150.0,
            dtcs=["P0300"],
        )
    )
    assert family == "misfire", f"got {family}, expected misfire"
    assert winner.startswith("MF-")


# ---------------------------------------------------------------------------
# Cross-family import firewall
# ---------------------------------------------------------------------------

FORBIDDEN_IMPORTS = frozenset(
    {
        "gaslab", "obdlab", "dtclab", "dnalab", "comlab", "4DLabWired",
    }
)


def test_no_lab_imports() -> None:
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    imports: list[str] = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                imports.append(node.module)
    violations = [
        imp
        for imp in imports
        if any(imp == fb or imp.startswith(fb + ".") for fb in FORBIDDEN_IMPORTS)
    ]
    assert not violations, f"Forbidden cross-lab imports: {violations}"
