"""T-COMA-6 (F-C1-1): on healthy gas, one weak evidence row does not name a fault.

When the chemistry state is NORMAL_OPERATION, a registry rule fires only with strict support: a DEFINITIVE row, a
positive DTC row, two rows, or a matched GATING chemistry state plus one row. A ``none_present`` DTC row and a
NORMAL_OPERATION chemistry row are not support. Any other chemistry state keeps the permissive predicate.
Tags: NEW fails on the base; PIN passes on the base and after.
"""

from __future__ import annotations

import pytest

from v7.load_corpus import load_corpus
from wired.composition import diagnose

IDLE = {"map_kpa": 30.0, "maf": 2.0, "rpm": 800.0, "co2": 15.0, "hc": 20.0, "co": 0.2, "o2": 0.3, "nox": 20.0,
        "obd_lambda": 1.0, "longft1": 0.0, "shrtft1": 0.0}


def _rule_and_obs(rule_id: str, dtcs: tuple[str, ...] = (), **pids: float):
    """A registry rule and a healthy idle observation (NORMAL_OPERATION, lambda 1.00, trims 0), with overrides."""
    from registry.integration_shim import RegistryV2Router, _Observation
    from registry.schema_v2 import ChemistryState

    obs = _Observation(chemistry_state=ChemistryState.NORMAL_OPERATION, dtcs=list(dtcs), dtc_routing_tags=[],
                       obd_pids={**IDLE, **pids})
    return next(r for r in RegistryV2Router().rules if r.rule_id == rule_id), obs


@pytest.mark.parametrize("rule_id", ["LC-002", "LC-003", "CF-002", "CF-004", "MF-004", "MF-005", "OV-004"])
def test_one_weak_row_does_not_fire_on_healthy_gas(rule_id):
    """NEW: seven rules that fired on the healthy car (one SUGGESTIVE row, none_present, or the NORMAL row) do not."""
    from registry.integration_shim import _score_rule

    rule, obs = _rule_and_obs(rule_id)
    assert _score_rule(rule, obs) is None


def test_none_present_is_not_a_second_row():
    """NEW: MF-005 with HC 210 ppm and no misfire code has one support row, not two: it does not fire on healthy gas."""
    from registry.integration_shim import _score_rule

    rule, obs = _rule_and_obs("MF-005", hc=210.0)
    assert _score_rule(rule, obs) is None


def test_weak_rule_prune_is_attributed():
    """NEW: a rule stopped only by strict support is attributed as weak support (the telemetry complement)."""
    from registry.integration_shim import _prune_attribution

    rule, obs = _rule_and_obs("LC-002")
    assert _prune_attribution(rule, obs) == ("missing_evidence", "weak_support_only")


@pytest.mark.parametrize(("rule_id", "dtcs", "pids"), [("CF-002", (), {"longft1": 12.0}), ("MF-004", ("P0301",), {})])
def test_real_evidence_on_healthy_gas_still_fires(rule_id, dtcs, pids):
    """PIN: catalyst masking (LTFT >= 10 with clean HC) and a misfire code on normal gas still fire."""
    from registry.integration_shim import _score_rule

    rule, obs = _rule_and_obs(rule_id, dtcs, **pids)
    assert _score_rule(rule, obs) is not None


@pytest.mark.parametrize(("case_id", "family"), [("EXP-N012", "catalyst_failure"), ("YAML-PDF_4G_05", "ecu_fault")])
def test_thin_evidence_on_other_gas_is_unchanged(case_id, family):
    """PIN: chemistry not NORMAL_OPERATION keeps the permissive predicate: a one-row verdict still names its fault."""
    raw = next(r for cid, r, *_ in load_corpus() if cid == case_id)
    v = diagnose(raw).diagnostic_verdict
    assert v.fault_family == family
    assert v.is_fault_detected is True


def _synthetic(chem_tier, with_obd: bool):
    """CF-002 reshaped: its NORMAL_OPERATION chemistry row at ``chem_tier``, optionally LC-002's map_kpa row, no DTC."""
    from registry.schema_v2 import EvidenceTier

    base, obs = _rule_and_obs("CF-002")
    lc002, _ = _rule_and_obs("LC-002")
    chem = base.chemistry_evidence[0].model_copy(update={"tier": getattr(EvidenceTier, chem_tier)})
    obd = [e for e in lc002.obd_evidence if e.pid == "map_kpa"] if with_obd else []
    return base.model_copy(update={"chemistry_evidence": [chem], "obd_evidence": obd, "dtc_evidence": []}), obs


@pytest.mark.parametrize(("chem_tier", "with_obd"), [("DEFINITIVE", False), ("SUGGESTIVE", False), ("GATING", True)])
def test_normal_row_alone_or_as_anchor_does_not_fire(chem_tier, with_obd):
    """NEW (correction 1): a rule whose only support row is NORMAL_OPERATION, or a GATING NORMAL row plus one weak
    row, does not fire on healthy gas, and the prune is attributed as weak support."""
    from registry.integration_shim import _prune_attribution, _score_rule

    rule, obs = _synthetic(chem_tier, with_obd)
    assert _score_rule(rule, obs) is None
    assert _prune_attribution(rule, obs) == ("missing_evidence", "weak_support_only")
