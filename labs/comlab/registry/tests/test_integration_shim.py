"""Tests for ``registry.integration_shim``.

The 11 tests below cover the shim's two separable responsibilities:

1. **Algorithm correctness** (tests 5, 6, 8, 9, 10) — controlled synthetic
   ``tmp_path``-built RuleSets that exercise the 6-step algorithm directly,
   independent of how the real 68-rule corpus happens to score.

2. **Integration correctness vs the real registry** (tests 1, 4, 7) — assertions
   that hold across the full v2 corpus as authored. Test 7 is the CS-002
   router-assumption gate — see assertion message for traceability.

Tests 2/3 exercise loader failure modes (missing file, malformed JSON).
Test 11 is the AST-only no-imports invariant per the registry self-contained
rule.

Why synthetic vs real split: under the locked algorithm with the real rule
set as authored, the obvious "CS-001 fires on P0562 alone" or "competition
by ceiling" scenarios don't actually win cross-group (other rules with
chemistry DEFINITIVE evidence beat them). That is a v2-ruleset *tuning*
question (``REG-V2-INTEGRATE-TUNE``), not a shim correctness question.
Synthetic fixtures keep the unit tests focused on the shim itself; the
side-by-side harness covers integration vs the real authored corpus.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import pytest

from registry.integration_shim import (
    RegistryV2Router,
    _DEFAULT_RULES_DIR,
    _EXPECTED_RULE_FILES,
)


# =============================================================================
# Synthetic-fixture helpers
# =============================================================================


def _write_ruleset(
    tmp_path: Path,
    filename: str,
    fault_family: str,
    rules: list[dict[str, Any]],
) -> Path:
    """Write a minimal valid RuleSet JSON file under tmp_path and return the path.

    Caller is responsible for setting ``confidence_ceiling`` on single-rule
    fixtures (the schema's solo-survivor check rejects solo rules without it).
    """
    data = {
        "version": "2.0",
        "fault_family": fault_family,
        "rules": rules,
    }
    out = tmp_path / filename
    out.write_text(json.dumps(data), encoding="utf-8")
    return out


def _minimal_rule(
    rule_id: str,
    fault_family: str,
    *,
    base_weight: float = 0.70,
    competition_group: str | None = None,
    confidence_ceiling: float | None = None,
    chemistry_evidence: list[dict[str, Any]] | None = None,
    obd_evidence: list[dict[str, Any]] | None = None,
    dtc_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a single rule dict that validates against ``schema_v2.Rule``."""
    rule: dict[str, Any] = {
        "rule_id": rule_id,
        "fault_family": fault_family,
        "description": f"synthetic rule {rule_id}",
        "chemistry_evidence": chemistry_evidence or [],
        "obd_evidence": obd_evidence or [],
        "dtc_evidence": dtc_evidence or [],
        "base_weight": base_weight,
        "competition_group": competition_group or fault_family,
        "passes_cases": [f"CASE-{rule_id}-001"],
    }
    if confidence_ceiling is not None:
        rule["confidence_ceiling"] = confidence_ceiling
    return rule


# =============================================================================
# Test 1 — loader: real registry happy path
# =============================================================================


def test_shim_loads_all_16_rule_files() -> None:
    """Real-registry test. Constructing against the production rules dir
    loads exactly 73 rules across the 16 expected family files.
    """
    router = RegistryV2Router()
    assert len(router.rules) == 73
    families_seen = {rule.fault_family.value for rule in router.rules}
    # 16 family files; sanity-check a few canonical members.
    assert "charging_system" in families_seen
    assert "misfire" in families_seen
    assert "lean_condition" in families_seen
    assert "no_fault" in families_seen


def test_production_manifest_matches_rules_directory() -> None:
    """Production and glob-mode must load the same rule-family files."""
    rule_files = sorted(path.name for path in _DEFAULT_RULES_DIR.glob("*.json"))
    assert sorted(_EXPECTED_RULE_FILES) == rule_files


# =============================================================================
# Test 2 — loader: missing file raises with path in message
# =============================================================================


def test_shim_raises_on_missing_rule_file(tmp_path: Path) -> None:
    """Synthetic test. Construct in production mode (expected_files default)
    against a tmp dir that has only one of the 15 files; the loader raises
    ``FileNotFoundError`` with the missing path in the message.
    """
    # Write only ONE of the 14 expected files; the other 13 are missing.
    _write_ruleset(
        tmp_path,
        "charging_system.json",
        "charging_system",
        [
            _minimal_rule(
                "CS-SYN-1",
                "charging_system",
                confidence_ceiling=0.80,
                dtc_evidence=[
                    {
                        "dtc_codes": ["P0562"],
                        "strategy": "any_match",
                        "tier": "GATING",
                    }
                ],
            )
        ],
    )

    with pytest.raises(FileNotFoundError) as exc:
        RegistryV2Router(rules_dir=tmp_path)
    # Error message must include the path of one of the missing expected files.
    msg = str(exc.value)
    assert "cam_timing.json" in msg or "misfire.json" in msg or "vacuum_leak.json" in msg


# =============================================================================
# Test 3 — loader: malformed JSON raises with path in message
# =============================================================================


def test_shim_raises_on_invalid_rule_json(tmp_path: Path) -> None:
    """Synthetic test. Write a syntactically-broken JSON file in one of the
    15 expected slots; loader raises with the file path in the message.
    """
    # Write all 15 expected filenames as minimal valid stubs, except corrupt one.
    for filename in _EXPECTED_RULE_FILES:
        family = filename.replace(".json", "")
        _write_ruleset(
            tmp_path,
            filename,
            family,
            [
                _minimal_rule(
                    f"STUB-{family}",
                    family,
                    confidence_ceiling=0.70,
                    dtc_evidence=[
                        {
                            "dtc_codes": ["P9999"],
                            "strategy": "any_match",
                            "tier": "GATING",
                        }
                    ],
                )
            ],
        )
    # Now overwrite one with garbage.
    (tmp_path / "misfire.json").write_text("{not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError) as exc:
        RegistryV2Router(rules_dir=tmp_path)
    assert "misfire.json" in str(exc.value)


# =============================================================================
# Test 4 — public API: return shape
# =============================================================================


def test_route_case_returns_correct_shape() -> None:
    """Real-registry test. The shim's output dict carries the v1
    OrchestratorFinalUIOutput key set plus the alias keys downstream callers
    rely on (``fault_id``, ``ui_diagnostic_string``, ``confidence``).
    """
    router = RegistryV2Router()
    out = router.route_case({})

    # Top-level shape — verbatim per integration_shim._translate_to_output
    required_top = {
        "session_id",
        "execution_meta",
        "diagnostic_verdict",
        "performance_analytics",
        "fault_enrichment",
        "user_input_echo_audit",
        # Alias keys
        "fault_id",
        "ui_diagnostic_string",
        "confidence",
    }
    assert required_top.issubset(out.keys()), (
        f"Missing keys: {required_top - set(out.keys())}"
    )

    # diagnostic_verdict inner shape
    verdict = out["diagnostic_verdict"]
    required_verdict = {
        "is_fault_detected",
        "fault_code",
        "fault_name",
        "fault_family",
        "display_headline",
        "confidence_score",
        "actionable_remediation",
        "differential_siblings",
    }
    assert required_verdict.issubset(verdict.keys())


def test_route_case_with_diagnostics_returns_scored_rule_metadata(
    tmp_path: Path,
) -> None:
    """Synthetic test. The diagnostics API exposes scored rule IDs, families,
    and scores without changing the v1-shaped output payload.
    """
    _write_ruleset(
        tmp_path,
        "synthetic.json",
        "rich_mixture",
        [
            _minimal_rule(
                "RM-SYN-1",
                "rich_mixture",
                base_weight=0.70,
                confidence_ceiling=0.90,
                chemistry_evidence=[
                    {
                        "state": "RICH_MIXTURE",
                        "tier": "DEFINITIVE",
                    }
                ],
            ),
        ],
    )
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    output, diagnostics = router.route_case_with_diagnostics({
        "gas_lab_output": {
            "chemical_state": "RICH_MIXTURE",
            "sample_validity": "VALID",
        }
    })

    assert output["diagnostic_verdict"]["fault_family"] == "rich_mixture"
    assert diagnostics["scored_rules"] == [
        {
            "rule_id": "RM-SYN-1",
            "fault_family": "rich_mixture",
            "score": 0.7999999999999999,
        }
    ]
    assert diagnostics["winner_rule_id"] == "RM-SYN-1"


def test_render_ranked_rule_uses_canonical_output_translation(tmp_path: Path) -> None:
    rule = _minimal_rule(
        "MW-SYN-1",
        "mechanical_wear",
        base_weight=0.70,
        confidence_ceiling=1.0,
        chemistry_evidence=[
            {
                "state": "WORN_PISTON_RINGS",
                "tier": "DEFINITIVE",
            }
        ],
    )
    _write_ruleset(tmp_path, "synthetic.json", "mechanical_wear", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    output = router.render_ranked_rule({}, "MW-SYN-1", 0.92)

    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-SYN-1"
    assert verdict["fault_family"] == "mechanical_wear"
    assert verdict["confidence_score"] == pytest.approx(0.92)


# =============================================================================
# Test 5 — no-fault sentinel when no rules fire
# =============================================================================


def test_route_case_no_fault_when_no_rules_fire(tmp_path: Path) -> None:
    """Synthetic test. A 1-rule fixture whose GATING DTC is unreachable on the
    empty payload must produce the v1 OPTIMAL_HEALTH sentinel.

    Real-registry equivalent test is impossible — the production set includes
    ``none_present`` strategies (e.g. MF-005) that fire on empty payloads by
    design, so an empty payload against the real registry will *always*
    produce some fault.
    """
    _write_ruleset(
        tmp_path,
        "synthetic.json",
        "charging_system",  # any valid FaultFamily
        [
            _minimal_rule(
                "SYN-NOFIRE",
                "charging_system",
                confidence_ceiling=0.80,
                dtc_evidence=[
                    {
                        "dtc_codes": ["P9999"],
                        "strategy": "any_match",
                        "tier": "GATING",
                    }
                ],
            )
        ],
    )
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    out = router.route_case({"dtc_lab_output": {"confirmed_dtcs": []}})
    verdict = out["diagnostic_verdict"]
    assert verdict["is_fault_detected"] is False
    assert verdict["fault_code"] == "OPTIMAL_HEALTH"
    assert verdict["fault_family"] == "no_fault"
    # Alias key mirrors fault_code
    assert out["fault_id"] == "OPTIMAL_HEALTH"


# =============================================================================
# Test 6 — CS-001-style rule fires on P0562 (synthetic)
# =============================================================================


def test_cs_001_fires_on_p0562(tmp_path: Path) -> None:
    """Unit test of shim algorithm with synthetic ruleset. Real-registry
    behaviour for CS-001/CS-002 is covered by the side-by-side harness,
    not here.

    Two-rule fixture: CS-001-like (fires on P0562) competing against a
    weaker rule with a stricter GATING that the payload fails. CS-001-like
    must win.
    """
    cs_001_like = _minimal_rule(
        "CS-001-SYN",
        "charging_system",
        base_weight=0.75,
        competition_group="charging_system",
        confidence_ceiling=0.85,
        dtc_evidence=[
            {
                "dtc_codes": ["P0562"],
                "strategy": "any_match",
                "tier": "GATING",
            }
        ],
    )
    competitor = _minimal_rule(
        "COMPETITOR-SYN",
        "charging_system",
        base_weight=0.60,
        competition_group="other_group",
        confidence_ceiling=0.65,
        dtc_evidence=[
            {
                "dtc_codes": ["P9999"],  # not in payload — competitor will NOT fire
                "strategy": "any_match",
                "tier": "GATING",
            }
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "charging_system", [cs_001_like, competitor])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    out = router.route_case({"dtc_lab_output": {"confirmed_dtcs": ["P0562"]}})
    assert out["fault_id"] == "CS-001-SYN"
    assert out["diagnostic_verdict"]["fault_family"] == "charging_system"
    assert out["confidence"] <= 0.85


# =============================================================================
# Test 7 — CS-002 router-assumption gate (REAL REGISTRY)
# =============================================================================


def test_cs_002_no_fire_on_missing_chemistry() -> None:
    """REAL REGISTRY test — the CS-002 router-assumption gate.

    Payload: P0562 + P0300 + chemistry None + minimal OBD. The verdict's
    ``fault_family`` MUST NOT be ``charging_system`` and ``fault_id`` MUST
    NOT be ``CS-002``. The assertion message references the follow-up ID so
    a future failure is traceable.

    Per unplanned-follow-up ``CS-002-router-assumption`` (REGISTRY_PROGRESS.md
    L62): missing chemistry + charging DTC must NOT fire CS-002. This proves
    the hard-absence semantics — assertion holds regardless of which other
    rule wins cross-group.
    """
    router = RegistryV2Router()
    out = router.route_case(
        {
            "dtc_lab_output": {"confirmed_dtcs": ["P0562", "P0300"]},
            # gas_lab_output omitted → chemistry is None (hard absence)
        }
    )
    verdict = out["diagnostic_verdict"]
    assert verdict["fault_family"] != "charging_system", (
        f"CS-002-router-assumption FAILED: shim returned charging_system "
        f"on missing-chemistry + P0562 payload. fault_id={verdict['fault_code']!r}. "
        f"Verify hard-absence semantics in _check_chemistry_evidence."
    )
    assert verdict["fault_code"] != "CS-002", (
        "CS-002-router-assumption FAILED: CS-002 fired with chemistry=None. "
        "Hard-absence is violated."
    )


# =============================================================================
# Test 8 — CS-002 fires on NORMAL chemistry (synthetic, paired)
# =============================================================================


def test_cs_002_fires_on_normal_chemistry(tmp_path: Path) -> None:
    """Unit test of shim algorithm with synthetic ruleset. Pairs with test 7
    to prove the CS-002 hard-absence semantics is specifically about
    *absence*, not a blanket "CS-002 never fires" bug.

    Synthetic CS-002-like rule with NORMAL_OPERATION GATING + P0562 DEFINITIVE,
    no competitor. Payload supplies both → rule must fire and win.
    """
    cs_002_like = _minimal_rule(
        "CS-002",
        "charging_system",
        base_weight=0.70,
        competition_group="charging_system",
        confidence_ceiling=0.85,
        chemistry_evidence=[
            {
                "state": "NORMAL_OPERATION",
                "tier": "GATING",
            }
        ],
        dtc_evidence=[
            {
                "dtc_codes": ["P0562"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "charging_system", [cs_002_like])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    out = router.route_case(
        {
            "dtc_lab_output": {"confirmed_dtcs": ["P0562", "P0300"]},
            "gas_lab_output": {"chemical_state": "NORMAL_OPERATION"},
        }
    )
    assert out["fault_id"] == "CS-002"
    assert out["diagnostic_verdict"]["fault_family"] == "charging_system"


# =============================================================================
# Test 9 — competition resolution picks higher ceiling
# =============================================================================


def test_competition_resolution_picks_higher_ceiling(tmp_path: Path) -> None:
    """Unit test of shim algorithm with synthetic ruleset.

    Two rules in the same competition_group, both fire, both have identical
    base_weight and identical satisfied evidence — but different ceilings.
    Both rules accumulate a +0.10 DEFINITIVE bonus to reach a raw score of
    0.80, which is clamped by each rule's ceiling. The higher-ceiling rule
    must win.
    """
    higher = _minimal_rule(
        "HIGH-CEIL",
        "charging_system",
        base_weight=0.70,
        competition_group="shared_group",
        confidence_ceiling=0.85,
        dtc_evidence=[
            {
                "dtc_codes": ["P0562"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    lower = _minimal_rule(
        "LOW-CEIL",
        "charging_system",
        base_weight=0.70,
        competition_group="shared_group",
        confidence_ceiling=0.75,
        dtc_evidence=[
            {
                "dtc_codes": ["P0562"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "charging_system", [higher, lower])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    out = router.route_case({"dtc_lab_output": {"confirmed_dtcs": ["P0562"]}})
    assert out["fault_id"] == "HIGH-CEIL"
    # 0.70 + 0.10 DEFINITIVE = 0.80 (under 0.85 ceiling). pytest.approx absorbs
    # float-add noise like 0.7999999999999999.
    assert out["confidence"] == pytest.approx(0.80)


# =============================================================================
# Test 10 — evidence-corroborated tie-break
# =============================================================================


def test_evidence_tiebreak_promotes_corroborated_family_within_band(
    tmp_path: Path,
) -> None:
    """Synthetic FT-1 regression. A broad ECU rule wins the deterministic
    base/id tie-break today, but the observed DTC routing tag corroborates
    the same-scored misfire rule.
    """
    ecu_broad = _minimal_rule(
        "EF-BROAD",
        "ecu_fault",
        base_weight=0.85,
        competition_group="ecu_fault",
        confidence_ceiling=0.95,
        dtc_evidence=[
            {
                "dtc_codes": ["P0606"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    misfire_specific = _minimal_rule(
        "MF-SPECIFIC",
        "misfire",
        base_weight=0.85,
        competition_group="misfire",
        confidence_ceiling=0.95,
        dtc_evidence=[
            {
                "dtc_codes": ["P0300"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "ecu_fault", [ecu_broad, misfire_specific])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    out, diagnostics = router.route_case_with_diagnostics(
        {
            "dtc_lab_output": {
                "confirmed_dtcs": ["P0606", "P0300"],
                "routing_tags": ["MISFIRE_HISTORY"],
            }
        }
    )

    assert out["fault_id"] == "MF-SPECIFIC"
    assert out["diagnostic_verdict"]["fault_family"] == "misfire"
    assert diagnostics["scored_rules"][0]["rule_id"] == "MF-SPECIFIC"


def test_evidence_tiebreak_includes_exact_band_edge(tmp_path: Path) -> None:
    """Synthetic FT-1 regression. The empirical rank-2 corpus has 0.05 as
    its non-zero gap; the band edge is inclusive.
    """
    catalyst_broad = _minimal_rule(
        "CF-BROAD",
        "catalyst_failure",
        base_weight=0.90,
        competition_group="catalyst_failure",
        confidence_ceiling=1.0,
        dtc_evidence=[
            {
                "dtc_codes": ["P0420"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    lean_specific = _minimal_rule(
        "LC-SPECIFIC",
        "lean_condition",
        base_weight=0.85,
        competition_group="lean_condition",
        confidence_ceiling=0.95,
        chemistry_evidence=[
            {
                "state": "LEAN_MIXTURE",
                "tier": "SUGGESTIVE",
            }
        ],
        dtc_evidence=[
            {
                "dtc_codes": ["P0171"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "catalyst_failure", [catalyst_broad, lean_specific])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    out = router.route_case(
        {
            "gas_lab_output": {
                "chemical_state": "LEAN_MIXTURE",
                "sample_validity": "VALID",
            },
            "dtc_lab_output": {
                "confirmed_dtcs": ["P0420", "P0171"],
                "routing_tags": ["LEAN_HISTORY"],
            },
        }
    )

    assert out["fault_id"] == "LC-SPECIFIC"


def test_evidence_tiebreak_preserves_uncorroborated_or_outside_band_winner(
    tmp_path: Path,
) -> None:
    """Synthetic FT-1 regression. The tie-break is narrow: it does not move
    an uncorroborated lower rule, and it does not move a corroborated rule
    outside the empirical band.
    """
    broad = _minimal_rule(
        "CF-BROAD",
        "catalyst_failure",
        base_weight=0.90,
        competition_group="catalyst_failure",
        confidence_ceiling=1.0,
        chemistry_evidence=[
            {
                "state": "CATALYST_OVERWHELMED",
                "tier": "DEFINITIVE",
            }
        ],
    )
    uncorroborated_lean = _minimal_rule(
        "LC-UNCORROBORATED",
        "lean_condition",
        base_weight=0.86,
        competition_group="lean_condition",
        confidence_ceiling=0.96,
        dtc_evidence=[
            {
                "dtc_codes": ["P0171"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    outside_band_misfire = _minimal_rule(
        "MF-OUTSIDE",
        "misfire",
        base_weight=0.84,
        competition_group="misfire",
        confidence_ceiling=0.94,
        dtc_evidence=[
            {
                "dtc_codes": ["P0300"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    _write_ruleset(
        tmp_path,
        "syn.json",
        "catalyst_failure",
        [broad, uncorroborated_lean, outside_band_misfire],
    )
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    uncorroborated = router.route_case(
        {
            "gas_lab_output": {
                "chemical_state": "CATALYST_OVERWHELMED",
                "sample_validity": "VALID",
            },
            "dtc_lab_output": {
                "confirmed_dtcs": ["P0171"],
                "routing_tags": ["RICH_HISTORY"],
            },
        }
    )
    outside_band = router.route_case(
        {
            "gas_lab_output": {
                "chemical_state": "CATALYST_OVERWHELMED",
                "sample_validity": "VALID",
            },
            "dtc_lab_output": {
                "confirmed_dtcs": ["P0300"],
                "routing_tags": ["MISFIRE_HISTORY"],
            },
        }
    )

    assert uncorroborated["fault_id"] == "CF-BROAD"
    assert outside_band["fault_id"] == "CF-BROAD"


def test_evidence_tiebreak_is_order_independent(tmp_path: Path) -> None:
    """Synthetic FT-1 regression. Reversing rule-file order must not change
    the evidence-corroborated verdict.
    """
    broad = _minimal_rule(
        "EF-BROAD",
        "ecu_fault",
        base_weight=0.85,
        competition_group="ecu_fault",
        confidence_ceiling=0.95,
        dtc_evidence=[
            {
                "dtc_codes": ["P0606"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    specific = _minimal_rule(
        "MF-SPECIFIC",
        "misfire",
        base_weight=0.85,
        competition_group="misfire",
        confidence_ceiling=0.95,
        dtc_evidence=[
            {
                "dtc_codes": ["P0300"],
                "strategy": "any_match",
                "tier": "DEFINITIVE",
            }
        ],
    )
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    _write_ruleset(first_dir, "syn.json", "ecu_fault", [broad, specific])
    _write_ruleset(second_dir, "syn.json", "ecu_fault", [specific, broad])

    payload = {
        "dtc_lab_output": {
            "confirmed_dtcs": ["P0606", "P0300"],
            "routing_tags": ["MISFIRE_HISTORY"],
        }
    }

    first = RegistryV2Router(rules_dir=first_dir, expected_files=None).route_case(payload)
    second = RegistryV2Router(rules_dir=second_dir, expected_files=None).route_case(payload)

    assert first["fault_id"] == "MF-SPECIFIC"
    assert second["fault_id"] == "MF-SPECIFIC"


# =============================================================================
# Test 11 — OBD GATING unsatisfied → rule does not fire
# =============================================================================


def test_gating_obd_unsatisfied_does_not_fire(tmp_path: Path) -> None:
    """Unit test of shim algorithm with synthetic ruleset.

    1-rule fixture with an OBD GATING entry that the payload fails. Rule
    must not fire; shim returns the no-fault sentinel.
    """
    rule = _minimal_rule(
        "GATED",
        "lean_condition",
        base_weight=0.70,
        competition_group="lean_condition",
        confidence_ceiling=0.80,
        obd_evidence=[
            {
                "pid": "longft1",
                "operator": "gt",
                "value": 15.0,
                "tier": "GATING",
            }
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "lean_condition", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    # Payload supplies longft1 BELOW the gate threshold → GATING fails.
    payload = {
        "dtc_lab_output": {
            "confirmed_dtcs": [],
            "freeze_frame": {"long_term_ft1": 2.0},
        }
    }
    out = router.route_case(payload)
    assert out["diagnostic_verdict"]["is_fault_detected"] is False
    assert out["fault_id"] == "OPTIMAL_HEALTH"


# =============================================================================
# FT-3 — pre-scoring prune attribution in diagnostics (telemetry only)
# =============================================================================


def test_diagnostics_attributes_chemistry_gating_prune(tmp_path: Path) -> None:
    """FT-3. A rule whose GATING chemistry row is unsatisfied is reported in
    ``diagnostics["pruned_rules"]`` with reason 'chemistry' / key 'gas_lab_state'
    — matching the v1 prune contract the Jaeger analyser consumes.
    """
    rule = _minimal_rule(
        "CHEM-GATED",
        "rich_mixture",
        confidence_ceiling=0.80,
        chemistry_evidence=[{"state": "RICH_MIXTURE", "tier": "GATING"}],
    )
    _write_ruleset(tmp_path, "syn.json", "rich_mixture", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    # LEAN chemistry → RICH_MIXTURE GATING row fails.
    _out, diagnostics = router.route_case_with_diagnostics(
        {"gas_lab_output": {"chemical_state": "LEAN_MIXTURE", "sample_validity": "VALID"}}
    )

    assert diagnostics["scored_rules"] == []
    assert diagnostics["pruned_rules"] == [
        {
            "rule_id": "CHEM-GATED",
            "prune_reason": "chemistry",
            "failed_gating_key": "gas_lab_state",
        }
    ]


def test_diagnostics_attributes_obd_gating_prune(tmp_path: Path) -> None:
    """FT-3. An unsatisfied OBD GATING row → reason 'missing_evidence',
    key 'obd:<pid>'.
    """
    rule = _minimal_rule(
        "OBD-GATED",
        "lean_condition",
        confidence_ceiling=0.80,
        obd_evidence=[{"pid": "longft1", "operator": "gt", "value": 15.0, "tier": "GATING"}],
    )
    _write_ruleset(tmp_path, "syn.json", "lean_condition", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    _out, diagnostics = router.route_case_with_diagnostics(
        {"dtc_lab_output": {"confirmed_dtcs": [], "freeze_frame": {"long_term_ft1": 2.0}}}
    )

    assert diagnostics["scored_rules"] == []
    assert diagnostics["pruned_rules"] == [
        {
            "rule_id": "OBD-GATED",
            "prune_reason": "missing_evidence",
            "failed_gating_key": "obd:longft1",
        }
    ]


def test_diagnostics_attributes_no_evidence_prune(tmp_path: Path) -> None:
    """FT-3. A rule with no GATING but whose only (non-GATING) evidence row is
    unsatisfied → reason 'missing_evidence', key 'no_evidence_satisfied'
    (firing-predicate (b) failure).
    """
    rule = _minimal_rule(
        "NO-EVIDENCE",
        "rich_mixture",
        confidence_ceiling=0.80,
        chemistry_evidence=[{"state": "RICH_MIXTURE", "tier": "DEFINITIVE"}],
    )
    _write_ruleset(tmp_path, "syn.json", "rich_mixture", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    # No chemistry observed → GATING (none) passes, but no row is satisfied.
    _out, diagnostics = router.route_case_with_diagnostics(
        {"dtc_lab_output": {"confirmed_dtcs": []}}
    )

    assert diagnostics["scored_rules"] == []
    assert diagnostics["pruned_rules"] == [
        {
            "rule_id": "NO-EVIDENCE",
            "prune_reason": "missing_evidence",
            "failed_gating_key": "no_evidence_satisfied",
        }
    ]


def test_diagnostics_firing_rule_not_in_pruned_list(tmp_path: Path) -> None:
    """FT-3. A rule that fires appears in ``scored_rules`` and NOT in
    ``pruned_rules`` — the two lists partition the corpus, and adding the
    attribution does not change the verdict (scoring byte-identical).
    """
    rule = _minimal_rule(
        "RM-FIRES",
        "rich_mixture",
        base_weight=0.70,
        confidence_ceiling=0.90,
        chemistry_evidence=[{"state": "RICH_MIXTURE", "tier": "DEFINITIVE"}],
    )
    _write_ruleset(tmp_path, "syn.json", "rich_mixture", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    payload = {"gas_lab_output": {"chemical_state": "RICH_MIXTURE", "sample_validity": "VALID"}}
    output, diagnostics = router.route_case_with_diagnostics(payload)

    assert diagnostics["winner_rule_id"] == "RM-FIRES"
    assert [r["rule_id"] for r in diagnostics["scored_rules"]] == ["RM-FIRES"]
    assert diagnostics["pruned_rules"] == []
    # Verdict identical to route_case (no diagnostics-path divergence). Compare
    # the diagnostic verdict — not the full dict — because user_input_echo_audit
    # carries a per-call now() sentinel that is non-deterministic by design.
    assert output["diagnostic_verdict"] == router.route_case(payload)["diagnostic_verdict"]


def test_diagnostics_pruned_plus_scored_covers_real_corpus() -> None:
    """FT-3. Against the real registry, every rule is accounted for:
    each rule is either scored or pruned, never both and never dropped. This is
    the partition invariant that lets the phase.prune span set
    candidates_in == len(scored)+len(pruned). Verified on an empty payload
    (most rules pruned) — a few no-fault/`none_present` rules fire even here, so
    the test asserts the partition, not a specific pruned count.
    """
    router = RegistryV2Router()
    _out, diagnostics = router.route_case_with_diagnostics({})
    scored_ids = {r["rule_id"] for r in diagnostics["scored_rules"]}
    pruned_ids = {r["rule_id"] for r in diagnostics["pruned_rules"]}
    all_rule_ids = {rule.rule_id for rule in router.rules}
    total_rules = len(router.rules)

    # Partition: scored ∪ pruned == every rule, with no overlap.
    assert scored_ids.isdisjoint(pruned_ids)
    assert scored_ids | pruned_ids == all_rule_ids
    assert len(diagnostics["scored_rules"]) + len(diagnostics["pruned_rules"]) == total_rules
    # At least some rules are pruned on an empty payload (the bucket is real).
    assert pruned_ids
    # Every pruned entry carries the analyser's required keys with non-empty values.
    for entry in diagnostics["pruned_rules"]:
        assert entry["prune_reason"] in {"chemistry", "missing_evidence"}
        assert entry["failed_gating_key"]


# =============================================================================
# Test 12 — AST no-imports invariant
# =============================================================================


def test_no_unauthorised_imports() -> None:
    """Static-AST scan of ``integration_shim.py``: no import (``import X`` or
    ``from X import ...``) may name any lab or ``4DLabWired`` as its root.

    Mirrors the verification block in ``REG-V2-INTEGRATE_wire_to_comlab.md``
    lines 156-172.
    """
    shim_path = Path(__file__).parent.parent / "integration_shim.py"
    src = shim_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    forbidden_roots = {
        "comlab",
        "gaslab",
        "obdlab",
        "dtclab",
        "dnalab",
        "4DLabWired",
    }
    offenders: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = (alias.name or "").split(".")[0]
                if root in forbidden_roots:
                    offenders.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in forbidden_roots:
                offenders.append(node.module or "<relative>")
    assert not offenders, (
        f"integration_shim.py imports forbidden modules: {offenders}. "
        f"Registry self-contained rule violated."
    )


# =============================================================================
# Defensive — guard against future _DEFAULT_RULES_DIR drift
# =============================================================================


def test_default_rules_dir_resolves_to_registry_rules() -> None:
    """Sanity check: the default rules dir constant resolves to the
    ``registry/rules`` directory. Catches accidental refactors that point
    the production singleton at the wrong location.
    """
    assert _DEFAULT_RULES_DIR.name == "rules"
    assert _DEFAULT_RULES_DIR.parent.name == "registry"


# =============================================================================
# T-OBW-3 — live-first / freeze-frame fallback for trim PIDs
# =============================================================================


def test_live_trims_resolve_from_obd_live_data(tmp_path: Path) -> None:
    """When obd_live_data carries shrtft1/longft1, the shim resolves from live
    OBD, not freeze-frame. The payload provides BOTH sources with different
    values; the gate threshold is set so that only the live value passes,
    proving live-first resolution.
    """
    rule = _minimal_rule(
        "TRIM-LIVE",
        "lean_condition",
        base_weight=0.70,
        competition_group="lean_condition",
        confidence_ceiling=0.80,
        chemistry_evidence=[{"state": "LEAN_MIXTURE", "tier": "DEFINITIVE"}],
        obd_evidence=[
            {"pid": "longft1", "operator": "gt", "value": 5.0, "tier": "GATING"},
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "lean_condition", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    payload: dict[str, Any] = {
        "gas_lab_output": {"chemical_state": "LEAN_MIXTURE", "sample_validity": "VALID"},
        "obd_live_data": {"shrtft1": 12.0, "longft1": 8.0},
        "dtc_lab_output": {
            "confirmed_dtcs": [],
            "freeze_frame": {"short_term_ft1": 3.0, "long_term_ft1": 2.0},
        },
    }
    out = router.route_case(payload)
    assert out["diagnostic_verdict"]["is_fault_detected"] is True
    assert out["fault_id"] == "TRIM-LIVE"


def test_live_trims_fallback_to_freeze_frame(tmp_path: Path) -> None:
    """When obd_live_data is absent, the shim falls back to freeze-frame.
    Uses long_term_ft1=18.0 in freeze_frame with gate > 15.0 — only the
    fallback value can satisfy it.
    """
    rule = _minimal_rule(
        "TRIM-FF-FB",
        "lean_condition",
        base_weight=0.70,
        competition_group="lean_condition",
        confidence_ceiling=0.80,
        chemistry_evidence=[{"state": "LEAN_MIXTURE", "tier": "DEFINITIVE"}],
        obd_evidence=[
            {"pid": "longft1", "operator": "gt", "value": 15.0, "tier": "GATING"},
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "lean_condition", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    # No obd_live_data key at all — must degrade to freeze_frame.
    payload: dict[str, Any] = {
        "gas_lab_output": {"chemical_state": "LEAN_MIXTURE", "sample_validity": "VALID"},
        "dtc_lab_output": {
            "confirmed_dtcs": [],
            "freeze_frame": {"long_term_ft1": 18.0},
        },
    }
    out = router.route_case(payload)
    assert out["diagnostic_verdict"]["is_fault_detected"] is True
    assert out["fault_id"] == "TRIM-FF-FB"


def test_live_trims_both_absent_returns_none(tmp_path: Path) -> None:
    """When neither obd_live_data nor freeze_frame carries the trim, the PID
    resolves to None and the GATING leg is unsatisfied — rule does not fire.
    Covers both shrtft1 (live) and short_term_ft1 (ff) absence.
    """
    rule = _minimal_rule(
        "TRIM-NONE",
        "lean_condition",
        base_weight=0.70,
        competition_group="lean_condition",
        confidence_ceiling=0.80,
        chemistry_evidence=[{"state": "LEAN_MIXTURE", "tier": "DEFINITIVE"}],
        obd_evidence=[
            {"pid": "shrtft1", "operator": "gt", "value": 0.0, "tier": "GATING"},
        ],
    )
    _write_ruleset(tmp_path, "syn.json", "lean_condition", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=None)

    payload: dict[str, Any] = {
        "gas_lab_output": {"chemical_state": "LEAN_MIXTURE", "sample_validity": "VALID"},
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    out = router.route_case(payload)
    assert out["diagnostic_verdict"]["is_fault_detected"] is False
    assert out["fault_id"] == "OPTIMAL_HEALTH"
