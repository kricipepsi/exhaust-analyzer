"""T-V3-3D abstain-margin 0.02 calibration tests."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import ABSTAIN_MARGIN, FaultAtlasRouter
from tests.unit.test_abstain_family_margin import MockKGNode, _mock_v2_output, _registry_row
from tests.unit.test_fault_atlas_router import _make_request, _sanitized

WORKSPACE_ROOT = Path("/agent_workspace")
APPS_WIRED = str(WORKSPACE_ROOT / "apps/wired")
if APPS_WIRED not in sys.path:
    sys.path.insert(0, APPS_WIRED)

from fl_tasks.score_v3_yardstick import summarize  # type: ignore  # noqa: E402


def test_v1_family_aware_margin_002_boundary(monkeypatch: Any, registry_path: Path) -> None:
    """V1 path abstains at a different-family margin <= 0.02 and not above it."""
    router = FaultAtlasRouter(str(registry_path), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=False)
    winner = _registry_row("ERR-CF-001", "catalyst_efficiency_below_threshold")
    same_family_runner_up = _registry_row("ERR-CF-002", "catalyst_efficiency_limit")
    different_family_runner_up = _registry_row("ERR-IGN-001", "ignition_misfire")
    nodes = {
        "ERR-CF-001": MockKGNode("catalyst_failure"),
        "ERR-CF-002": MockKGNode("catalyst_failure"),
        "ERR-IGN-001": MockKGNode("ignition_fault"),
    }
    monkeypatch.setattr(router._kg, "resolve", lambda fault_id: nodes[fault_id])
    req = _make_request()

    monkeypatch.setattr(
        router,
        "execute_triage_loop",
        lambda sanitized: {
            "winner": winner,
            "winner_score": 0.82,
            "runner_ups": [(same_family_runner_up, 0.81), (different_family_runner_up, 0.80)],
        },
    )
    boundary = router.route(_sanitized(req))
    assert ABSTAIN_MARGIN == 0.02
    assert boundary.diagnostic_verdict.abstained is True
    assert boundary.diagnostic_verdict.abstain_reason == "margin"

    monkeypatch.setattr(
        router,
        "execute_triage_loop",
        lambda sanitized: {
            "winner": winner,
            "winner_score": 0.82,
            "runner_ups": [(same_family_runner_up, 0.81), (different_family_runner_up, 0.799)],
        },
    )
    above_boundary = router.route(_sanitized(req))
    assert above_boundary.diagnostic_verdict.abstained is False
    assert above_boundary.diagnostic_verdict.abstain_reason is None


def test_v2_family_aware_margin_002_boundary(monkeypatch: Any, registry_path: Path) -> None:
    """V2 path abstains at a different-family margin <= 0.02 and not above it."""
    router = FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=True,
        enable_delta_v2=False,
    )
    mock_out = _mock_v2_output(True, "ERR-CF-001", 0.82)
    req = _make_request()

    monkeypatch.setattr(
        "registry.integration_shim.route_case_with_diagnostics",
        lambda payload: (
            mock_out,
            {
                "scored_rules": [
                    {"rule_id": "ERR-CF-001", "fault_family": "catalyst_failure", "score": 0.82},
                    {"rule_id": "ERR-CF-002", "fault_family": "catalyst_failure", "score": 0.81},
                    {"rule_id": "ERR-IGN-001", "fault_family": "ignition_fault", "score": 0.80},
                ],
                "pruned_rules": [],
                "winner_rule_id": "ERR-CF-001",
            },
        ),
    )
    boundary = router.route(_sanitized(req))
    assert boundary.diagnostic_verdict.abstained is True
    assert boundary.diagnostic_verdict.abstain_reason == "margin"

    monkeypatch.setattr(
        "registry.integration_shim.route_case_with_diagnostics",
        lambda payload: (
            mock_out,
            {
                "scored_rules": [
                    {"rule_id": "ERR-CF-001", "fault_family": "catalyst_failure", "score": 0.82},
                    {"rule_id": "ERR-CF-002", "fault_family": "catalyst_failure", "score": 0.81},
                    {"rule_id": "ERR-IGN-001", "fault_family": "ignition_fault", "score": 0.799},
                ],
                "pruned_rules": [],
                "winner_rule_id": "ERR-CF-001",
            },
        ),
    )
    above_boundary = router.route(_sanitized(req))
    assert above_boundary.diagnostic_verdict.abstained is False
    assert above_boundary.diagnostic_verdict.abstain_reason is None


def test_scoreboard_top3_family_count_ignores_abstain_flag() -> None:
    """Scoreboard top3_family count is invariant when only the abstain flag changes."""
    corpus_rows = [
        {
            "case_id": "case-top3-hit",
            "tag": "viable",
            "accuracy_excluded": "false",
            "expected_fault_family": "ignition_fault",
        },
        {
            "case_id": "case-top3-miss",
            "tag": "viable",
            "accuracy_excluded": "false",
            "expected_fault_family": "sensor_fault",
        },
    ]
    localization_modes = {
        "case-top3-hit": {"mode": "OUTRANKED"},
        "case-top3-miss": {"mode": "OUTRANKED"},
    }
    base_results: list[dict[str, Any]] = [
        {
            "case_id": "case-top3-hit",
            "dimensions": {"fault_family": "FAIL", "state": "PASS"},
            "verdict": {
                "fault_family": "catalyst_failure",
                "abstained": False,
                "differential_siblings": [{"fault_family": "ignition_fault"}],
            },
        },
        {
            "case_id": "case-top3-miss",
            "dimensions": {"fault_family": "FAIL", "state": "PASS"},
            "verdict": {
                "fault_family": "catalyst_failure",
                "abstained": False,
                "differential_siblings": [{"fault_family": "ignition_fault"}],
            },
        },
    ]
    abstained_results = [
        {
            **row,
            "verdict": {**row["verdict"], "abstained": True},
        }
        for row in base_results
    ]

    before = summarize(
        label="before",
        result_rows=base_results,
        corpus_rows=corpus_rows,
        localization_modes=localization_modes,
        identity={},
    )
    after = summarize(
        label="after",
        result_rows=abstained_results,
        corpus_rows=corpus_rows,
        localization_modes=localization_modes,
        identity={},
    )

    assert before["overall"]["top3_family_pass"] == 1
    assert after["overall"]["top3_family_pass"] == before["overall"]["top3_family_pass"]
    assert after["overall"]["total_abstained"] == 2
