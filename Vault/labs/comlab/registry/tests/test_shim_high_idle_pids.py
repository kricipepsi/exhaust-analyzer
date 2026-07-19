from __future__ import annotations

from pathlib import Path

from registry.integration_shim import (
    RegistryV2Router,
    _build_observation,
)
from registry.tests.test_integration_shim import (
    _minimal_rule,
    _write_ruleset,
)

def test_resolves_high_idle_hc() -> None:
    payload = {
        "gas_lab_output": {
            "chemical_state": "WORN_PISTON_RINGS",
            "sample_validity": "VALID",
            "gas_hc": 380,
            "gas_co2": 12.0,
            "gas_o2": 2.0,
            "high_idle_hc": 130,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    obs = _build_observation(payload)
    assert obs.obd_pids.get("high_idle_hc") == 130.0
    assert obs.obd_pids.get("high_idle_co") is None


def test_rule_with_high_idle_gate_fires(tmp_path: Path) -> None:
    # A fixture rule with an obd_evidence row {pid: high_idle_hc, operator: lt, value: 200}
    # fires for a turbo-shaped payload and is pruned for a rings-shaped one.
    rule = _minimal_rule(
        "MW-HIGH-IDLE",
        "mechanical_wear",
        base_weight=0.80,
        confidence_ceiling=0.95,
        chemistry_evidence=[{"state": "WORN_PISTON_RINGS", "tier": "GATING"}],
        obd_evidence=[
            {
                "pid": "high_idle_hc",
                "operator": "lt",
                "value": 200.0,
                "tier": "GATING",
                "units": "ppm",
                "wiki_ref": "GAS_VOCABULARY §2"
            }
        ]
    )
    _write_ruleset(tmp_path, "mechanical_wear.json", "mechanical_wear", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=frozenset(["mechanical_wear.json"]))

    # Turbo-shaped payload (high_idle_hc < 200) -> fires
    turbo_payload = {
        "gas_lab_output": {
            "chemical_state": "WORN_PISTON_RINGS",
            "sample_validity": "VALID",
            "gas_hc": 380,
            "high_idle_hc": 130,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    out, diag = router.route_case_with_diagnostics(turbo_payload)
    assert diag["winner_rule_id"] == "MW-HIGH-IDLE"

    # Rings-shaped payload (high_idle_hc >= 200) -> pruned
    rings_payload = {
        "gas_lab_output": {
            "chemical_state": "WORN_PISTON_RINGS",
            "sample_validity": "VALID",
            "gas_hc": 380,
            "high_idle_hc": 380,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    out, diag = router.route_case_with_diagnostics(rings_payload)
    assert diag["winner_rule_id"] == "__NONE__"
    # Verify prune reason
    pruned_rules = diag.get("pruned_rules") or []
    pruned = next((r for r in pruned_rules if r["rule_id"] == "MW-HIGH-IDLE"), None)
    assert pruned is not None
    assert pruned["prune_reason"] == "missing_evidence"
    assert pruned["failed_gating_key"] == "obd:high_idle_hc"


def test_missing_high_idle_safely_prunes(tmp_path: Path) -> None:
    # Missing high-idle (legacy single-snapshot payload) -> resolver returns None
    # and any high-idle-gated rule is pruned, not crashed.
    rule = _minimal_rule(
        "MW-HIGH-IDLE",
        "mechanical_wear",
        base_weight=0.80,
        confidence_ceiling=0.95,
        chemistry_evidence=[{"state": "WORN_PISTON_RINGS", "tier": "GATING"}],
        obd_evidence=[
            {
                "pid": "high_idle_hc",
                "operator": "lt",
                "value": 200.0,
                "tier": "GATING",
                "units": "ppm",
                "wiki_ref": "GAS_VOCABULARY §2"
            }
        ]
    )
    _write_ruleset(tmp_path, "mechanical_wear.json", "mechanical_wear", [rule])
    router = RegistryV2Router(rules_dir=tmp_path, expected_files=frozenset(["mechanical_wear.json"]))

    legacy_payload = {
        "gas_lab_output": {
            "chemical_state": "WORN_PISTON_RINGS",
            "sample_validity": "VALID",
            "gas_hc": 380,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    # Should not crash, and should prune the rule
    out, diag = router.route_case_with_diagnostics(legacy_payload)
    assert diag["winner_rule_id"] == "__NONE__"
    pruned_rules = diag.get("pruned_rules") or []
    pruned = next((r for r in pruned_rules if r["rule_id"] == "MW-HIGH-IDLE"), None)
    assert pruned is not None
    assert pruned["prune_reason"] == "missing_evidence"
    assert pruned["failed_gating_key"] == "obd:high_idle_hc"
