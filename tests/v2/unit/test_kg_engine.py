"""Unit tests for M4 kg_engine.py — CF combination, tech/era vetoes, hard vetoes.

Covers R2 (CF math golden outputs), R6 (era masking), R7 (hard veto guard).
"""

from __future__ import annotations

import pytest

from engine.v2.arbitrator import MasterEvidenceVector
from engine.v2.dna_core import (
    ERA_CAN,
    ERA_MODERN,
    ERA_OBDII_EARLY,
    ERA_PRE_OBDII,
    DNAOutput,
)
from engine.v2.kg_engine import (
    ROOT_CAUSE_PARENT_THRESHOLD,
    _has_hard_veto,
    _tech_vetoed,
    combine_cf,
    score_faults,
    score_root_causes,
)

# ── helpers ───────────────────────────────────────────────────────────────────


def _make_dna(
    *,
    era_bucket: str = ERA_OBDII_EARLY,
    tech_mask: dict[str, bool] | None = None,
) -> DNAOutput:
    if tech_mask is None:
        tech_mask = {
            "has_vvt": False,
            "has_gdi": False,
            "has_turbo": False,
            "is_v_engine": False,
            "has_egr": False,
            "has_secondary_air": False,
        }
    return DNAOutput(
        engine_state="warm_closed_loop",
        era_bucket=era_bucket,
        tech_mask=tech_mask,
        o2_type="NB",
        target_rpm_u2=2500,
        target_lambda_v112=1.000,
        vref_missing=False,
        confidence_ceiling=1.00,
        warnings=[],
    )


def _make_evidence(symptoms: dict[str, float] | None = None) -> MasterEvidenceVector:
    return MasterEvidenceVector(active_symptoms=symptoms or {})


# ── combine_cf golden outputs (v2-cf-inference §4) ────────────────────────────


@pytest.mark.parametrize(
    "weights,expected",
    [
        ([], 0.0),
        ([0.0], 0.0),
        ([1.0], 1.0),
        ([0.5], 0.5),
        ([0.5, 0.5], 0.75),
        ([0.3, 0.4], 0.58),
        ([0.5, -0.5], 0.0),
        ([0.8, 0.8], 0.96),
        ([0.5, 0.5, 0.5], 0.875),
        ([1.0, 1.0], 1.0),
    ],
)
def test_combine_cf_golden(weights: list[float], expected: float) -> None:
    result = combine_cf(weights)
    assert result == pytest.approx(expected, abs=0.001)


def test_combine_cf_result_in_bounds() -> None:
    """CF combination must stay within [0.0, 1.0] for all-positive inputs."""
    result = combine_cf([0.9, 0.9, 0.9, 0.9, 0.9])
    assert 0.0 <= result <= 1.0


def test_combine_cf_commutative() -> None:
    """CF combination should be order-independent (commutative property)."""
    a = combine_cf([0.3, 0.6])
    b = combine_cf([0.6, 0.3])
    assert a == pytest.approx(b, abs=0.001)


# ── tech veto ─────────────────────────────────────────────────────────────────


def test_tech_veto_gdi_required_engine_lacks_gdi() -> None:
    """Fault requiring has_gdi on non-GDI engine → score 0.0."""
    fault = {"tech_required": ["has_gdi"], "era": ["1996-2005"]}
    dna = _make_dna(tech_mask={"has_gdi": False})
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges: list[dict] = []
    faults = {"GDI_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["GDI_Fault"] == 0.0


def test_tech_veto_gdi_present_scores_normally() -> None:
    """Fault requiring has_gdi on GDI engine → scores normally (not vetoed)."""
    fault = {"tech_required": ["has_gdi"], "era": ["2016-2020"]}
    dna = _make_dna(
        era_bucket=ERA_MODERN,
        tech_mask={"has_gdi": True},
    )
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "GDI_Fault", "weight": 0.3},
    ]
    faults = {"GDI_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["GDI_Fault"] > 0.0


def test_tech_veto_multiple_flags_one_missing() -> None:
    """Fault requiring [has_turbo, has_gdi] on turbo-only engine → vetoed."""
    fault = {"tech_required": ["has_turbo", "has_gdi"], "era": ["2016-2020"]}
    dna = _make_dna(
        era_bucket=ERA_MODERN,
        tech_mask={"has_turbo": True, "has_gdi": False},
    )
    evidence = _make_evidence()
    edges: list[dict] = []
    faults = {"Turbo_GDI_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["Turbo_GDI_Fault"] == 0.0


# ── era veto ──────────────────────────────────────────────────────────────────


def test_era_veto_wrong_bucket() -> None:
    """Fault restricted to 2006-2015 on MY=1998 vehicle → score 0.0."""
    fault = {"tech_required": [], "era": ["2006-2015"]}
    dna = _make_dna(era_bucket=ERA_OBDII_EARLY)  # 1996-2005
    evidence = _make_evidence()
    edges: list[dict] = []
    faults = {"CAN_Bus_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["CAN_Bus_Fault"] == 0.0


def test_era_veto_matching_bucket_scores() -> None:
    """Fault in matching era → scores normally."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna(era_bucket=ERA_OBDII_EARLY)
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "O2_Sensor_Fault", "weight": 0.3},
    ]
    faults = {"O2_Sensor_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["O2_Sensor_Fault"] > 0.0


def test_era_veto_multi_era_fault() -> None:
    """Fault valid in multiple eras including vehicle's era → scores."""
    fault = {
        "tech_required": [],
        "era": ["1990-1995", "1996-2005", "2006-2015", "2016-2020"],
    }
    dna = _make_dna(era_bucket=ERA_CAN)
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "Universal_Fault", "weight": 0.3},
    ]
    faults = {"Universal_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["Universal_Fault"] > 0.0


# ── hard edge veto ────────────────────────────────────────────────────────────


def test_hard_veto_edge_zeroes_score() -> None:
    """Hard veto edge (weight == -1.0) from active symptom → score 0.0."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna()
    evidence = _make_evidence({"SYM_TECH_ABSENT": 1.0})
    edges = [
        {"source": "SYM_TECH_ABSENT", "target": "Turbo_Fault", "weight": -1.0},
    ]
    faults = {"Turbo_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["Turbo_Fault"] == 0.0


def test_hard_veto_inactive_symptom_no_effect() -> None:
    """Hard veto edge from a symptom that is NOT active → does not veto."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna()
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges = [
        {"source": "SYM_TECH_ABSENT", "target": "Turbo_Fault", "weight": -1.0},
        {"source": "SYM_LAMBDA_LOW", "target": "Turbo_Fault", "weight": 0.3},
    ]
    faults = {"Turbo_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["Turbo_Fault"] > 0.0


# ── _tech_vetoed unit ─────────────────────────────────────────────────────────


def test__tech_vetoed_no_requirements() -> None:
    assert not _tech_vetoed({"tech_required": []}, {})


def test__tech_vetoed_all_met() -> None:
    assert not _tech_vetoed(
        {"tech_required": ["has_gdi"]}, {"has_gdi": True}
    )


def test__tech_vetoed_one_missing() -> None:
    assert _tech_vetoed(
        {"tech_required": ["has_gdi"]}, {"has_gdi": False}
    )


# ── _has_hard_veto unit ───────────────────────────────────────────────────────


def test__has_hard_veto_no_hard_veto_edges() -> None:
    edges = [{"source": "SYM_A", "target": "Fault_X", "weight": 0.3}]
    assert not _has_hard_veto(edges, {"SYM_A": 0.85})


def test__has_hard_veto_active_hard_veto() -> None:
    edges = [{"source": "SYM_A", "target": "Fault_X", "weight": -1.0}]
    assert _has_hard_veto(edges, {"SYM_A": 0.85})


def test__has_hard_veto_hard_veto_not_active() -> None:
    edges = [{"source": "SYM_A", "target": "Fault_X", "weight": -1.0}]
    assert not _has_hard_veto(edges, {"SYM_OTHER": 0.85})


# ── positive CF scoring ───────────────────────────────────────────────────────


def test_cf_scoring_single_symptom() -> None:
    """Single symptom with edge weight 0.3 at CF 0.85 → contribution = 0.255."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna()
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "Rich_Fault", "weight": 0.3},
    ]
    faults = {"Rich_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["Rich_Fault"] == pytest.approx(0.255, abs=0.001)


def test_cf_scoring_two_symptoms() -> None:
    """Two symptoms combine via MYCIN CF rule."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna()
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85, "SYM_CO_HIGH": 0.70})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "Rich_Fault", "weight": 0.3},
        {"source": "SYM_CO_HIGH", "target": "Rich_Fault", "weight": 0.2},
    ]
    faults = {"Rich_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    c1 = 0.3 * 0.85  # 0.255
    c2 = 0.2 * 0.70  # 0.14
    expected = c1 + c2 * (1.0 - c1)  # 0.255 + 0.14 * 0.745 = 0.3593
    assert result["Rich_Fault"] == pytest.approx(expected, abs=0.001)


# ── inhibitory subtraction ────────────────────────────────────────────────────


def test_inhibitory_subtraction() -> None:
    """Inhibitory edge (-0.25 < w < 0) reduces CF score."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna()
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85, "SYM_CONTRARY": 0.70})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "Rich_Fault", "weight": 0.5},
        {"source": "SYM_CONTRARY", "target": "Rich_Fault", "weight": -0.25},
    ]
    faults = {"Rich_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    cf_pos = 0.5 * 0.85  # 0.425
    inhibitor = abs(-0.25 * 0.70)  # 0.175
    expected = max(0.0, cf_pos - inhibitor)  # 0.25
    assert result["Rich_Fault"] == pytest.approx(expected, abs=0.001)


def test_inhibitory_floor_at_zero() -> None:
    """Inhibitory subtraction floors at 0.0, never negative."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna()
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.30, "SYM_CONTRARY": 1.0})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "Rich_Fault", "weight": 0.1},
        {"source": "SYM_CONTRARY", "target": "Rich_Fault", "weight": -0.5},
    ]
    faults = {"Rich_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["Rich_Fault"] == 0.0


# ── edge cases ────────────────────────────────────────────────────────────────


def test_no_active_symptoms_all_zero() -> None:
    """No active symptoms → all faults score 0.0."""
    faults = {
        "Fault_A": {"tech_required": [], "era": ["1996-2005"]},
        "Fault_B": {"tech_required": [], "era": ["1996-2005"]},
    }
    dna = _make_dna()
    evidence = _make_evidence({})
    edges: list[dict] = []

    result = score_faults(evidence, dna, faults, edges)
    assert result["Fault_A"] == 0.0
    assert result["Fault_B"] == 0.0


def test_fault_with_no_incoming_edges_scores_zero() -> None:
    """Fault with no incoming edges gets 0.0 (no evidence)."""
    fault = {"tech_required": [], "era": ["1996-2005"]}
    dna = _make_dna()
    evidence = _make_evidence({"SYM_IRRELEVANT": 0.85})
    edges: list[dict] = []
    faults = {"Orphan_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["Orphan_Fault"] == 0.0


def test_pre_veto_applied_before_all_else() -> None:
    """Tech veto short-circuits — edge weights never inspected."""
    fault = {"tech_required": ["has_gdi"], "era": ["1996-2005"]}
    dna = _make_dna(tech_mask={"has_gdi": False})
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "GDI_Fault", "weight": 0.5},
    ]
    faults = {"GDI_Fault": fault}

    result = score_faults(evidence, dna, faults, edges)
    assert result["GDI_Fault"] == 0.0


def test_different_era_buckets() -> None:
    """Verify all four era bucket mappings."""
    fault_all = {
        "tech_required": [],
        "era": ["1990-1995", "1996-2005", "2006-2015", "2016-2020"],
    }
    evidence = _make_evidence({"SYM_LAMBDA_LOW": 0.85})
    edges = [
        {"source": "SYM_LAMBDA_LOW", "target": "Test_Fault", "weight": 0.3},
    ]
    faults = {"Test_Fault": fault_all}

    for era_const in (ERA_PRE_OBDII, ERA_OBDII_EARLY, ERA_CAN, ERA_MODERN):
        dna = _make_dna(era_bucket=era_const)
        result = score_faults(evidence, dna, faults, edges)
        assert result["Test_Fault"] > 0.0


def test_score_faults_never_calls_resolve_conflicts() -> None:
    """R7: kg_engine must not import or call resolve_conflicts."""
    import ast

    import engine.v2.kg_engine as m4

    with open(m4.__file__, encoding="utf-8") as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and ast.unparse(node.func).endswith(
            "resolve_conflicts"
        ):
            raise AssertionError(
                f"M4 must not call resolve_conflicts(): {ast.unparse(node)}"
            )
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if "resolve_conflicts" in alias.name:
                    raise AssertionError(
                        f"M4 must not import resolve_conflicts: {ast.unparse(node)}"
                    )


# ── score_root_causes — parent ≥ 0.80 gate ────────────────────────────────────


def test_root_cause_parent_below_threshold_excluded() -> None:
    """Root cause whose parent fault scores < 0.80 must be excluded."""
    raw_probs = {"Rich_Fault": 0.75}
    root_causes = {
        "RC_FPR_Leak": {
            "applies_to_fault": "Rich_Fault",
            "prompt": "Check FPR vacuum line.",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    assert "RC_FPR_Leak" not in result


def test_root_cause_parent_at_threshold_included() -> None:
    """Root cause whose parent fault scores exactly 0.80 must be included."""
    raw_probs = {"Rich_Fault": 0.80}
    root_causes = {
        "RC_FPR_Leak": {
            "applies_to_fault": "Rich_Fault",
            "prompt": "Check FPR vacuum line.",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    assert "RC_FPR_Leak" in result
    assert result["RC_FPR_Leak"]["parent_score"] == 0.80


def test_root_cause_parent_above_threshold_included() -> None:
    """Root cause whose parent fault scores > 0.80 must be included."""
    raw_probs = {"Rich_Fault": 0.85}
    root_causes = {
        "RC_FPR_Leak": {
            "applies_to_fault": "Rich_Fault",
            "prompt": "Check FPR vacuum line.",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    assert "RC_FPR_Leak" in result
    assert result["RC_FPR_Leak"]["parent_score"] == 0.85


def test_root_cause_parent_not_in_raw_probs_excluded() -> None:
    """Root cause whose parent fault is missing from raw_probs is excluded."""
    raw_probs: dict[str, float] = {}
    root_causes = {
        "RC_FPR_Leak": {
            "applies_to_fault": "Rich_Fault",
            "prompt": "Check FPR vacuum line.",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    assert "RC_FPR_Leak" not in result


def test_multiple_root_causes_same_parent() -> None:
    """Multiple root causes linked to the same qualifying parent all pass."""
    raw_probs = {"EVAP_Stuck": 0.90}
    root_causes = {
        "RC_Solenoid": {
            "applies_to_fault": "EVAP_Stuck",
            "prompt": "Disconnect purge line.",
        },
        "RC_Canister": {
            "applies_to_fault": "EVAP_Stuck",
            "prompt": "Weigh canister vs new-spec.",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    assert "RC_Solenoid" in result
    assert "RC_Canister" in result


def test_mixed_qualifying_and_excluded_root_causes() -> None:
    """Only root causes with qualifying parents pass."""
    raw_probs = {"Rich_Fault": 0.85, "Lean_Fault": 0.45}
    root_causes = {
        "RC_Rich": {
            "applies_to_fault": "Rich_Fault",
            "prompt": "Check fuel pressure.",
        },
        "RC_Lean": {
            "applies_to_fault": "Lean_Fault",
            "prompt": "Check vacuum lines.",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    assert "RC_Rich" in result
    assert "RC_Lean" not in result


def test_root_cause_missing_applies_to_fault_skipped() -> None:
    """Root cause without applies_to_fault field is silently skipped."""
    raw_probs = {"Rich_Fault": 0.90}
    root_causes = {
        "RC_Orphan": {
            "prompt": "No parent fault specified.",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    assert "RC_Orphan" not in result


def test_root_cause_preserves_original_fields() -> None:
    """Qualified root cause dict includes all original fields plus parent_score."""
    raw_probs = {"Rich_Fault": 0.88}
    root_causes = {
        "RC_FPR_Leak": {
            "applies_to_fault": "Rich_Fault",
            "prompt": "Check FPR vacuum line.",
            "source_guide": "docs/master_guides/fuel_system/guide.md §4.1",
        },
    }
    result = score_root_causes(raw_probs, root_causes)
    entry = result["RC_FPR_Leak"]
    assert entry["applies_to_fault"] == "Rich_Fault"
    assert entry["prompt"] == "Check FPR vacuum line."
    assert entry["source_guide"] == "docs/master_guides/fuel_system/guide.md §4.1"
    assert entry["parent_score"] == 0.88


def test_score_root_causes_does_not_mutate_input() -> None:
    """score_root_causes must not mutate the root_causes argument."""
    raw_probs = {"Rich_Fault": 0.90}
    root_causes = {
        "RC_FPR_Leak": {
            "applies_to_fault": "Rich_Fault",
            "prompt": "Check FPR vacuum line.",
        },
    }
    original = dict(root_causes["RC_FPR_Leak"])
    score_root_causes(raw_probs, root_causes)
    assert root_causes["RC_FPR_Leak"] == original
    assert "parent_score" not in root_causes["RC_FPR_Leak"]


def test_root_cause_parent_threshold_constant() -> None:
    """Threshold constant must be exactly 0.80 per v2-cf-inference §5."""
    assert ROOT_CAUSE_PARENT_THRESHOLD == 0.80
