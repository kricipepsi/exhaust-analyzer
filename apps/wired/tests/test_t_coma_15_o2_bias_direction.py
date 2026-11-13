"""T-COMA-15 (F-D2-1): the O2 bias direction. A sensor that reads lean (OBD lambda leaner than the chemistry) is
O2_SENSOR_BIASED_LOW; one that reads rich is O2_SENSOR_BIASED_HIGH (vocabulary.py, COMLab_BDD, the GASLab atlas).
Tags: NEW fails on the base; PIN passes on the base and after.
"""

from __future__ import annotations

import pytest


@pytest.mark.parametrize(("obd_lambda", "label"), [(1.12, "O2_SENSOR_BIASED_LOW"), (0.88, "O2_SENSOR_BIASED_HIGH")])
def test_perception_label_follows_the_vocabulary(obd_lambda, label):
    """NEW: BDD "A biased-lean sensor is surfaced against near-normal chemistry ... O2_SENSOR_BIASED_LOW"."""
    from comlab.core.perception_contradiction import detect

    result = detect(lambda_chem=1.00, normalized_obd_lambda=obd_lambda, era_lambda_tolerance=0.02)
    assert result.bias_verdict.value == label


def _rule(rule_id: str):
    from registry.integration_shim import RegistryV2Router

    return next(r for r in RegistryV2Router().rules if r.rule_id == rule_id)


@pytest.mark.parametrize(("rule_id", "state", "operator"), [("SF-001", "O2_SENSOR_BIASED_HIGH", "lt"),
                                                            ("SF-002", "O2_SENSOR_BIASED_LOW", "gt")])
def test_rule_delta_row_agrees_with_its_chemistry_state(rule_id, state, operator):
    """NEW: SF-001 (biased high, reads rich) needs delta < 0; SF-002 (biased low, reads lean) needs delta > 0."""
    rule = _rule(rule_id)
    assert [e.state.value for e in rule.chemistry_evidence] == [state]
    rows = [e for e in rule.obd_evidence if e.pid == "lambda_perception_delta"]
    assert [e.operator for e in rows] == [operator]


@pytest.mark.parametrize(("rule_id", "pid", "operator"), [("SF-001", "o2_voltage", "ge"), ("SF-002", "o2_voltage", "le")])
def test_voltage_rows_unchanged(rule_id, pid, operator):
    """PIN: SF-001 keeps o2_voltage >= 0.55 (reads rich) and SF-002 keeps o2_voltage <= 0.35 (reads lean)."""
    rows = [e for e in _rule(rule_id).obd_evidence if e.pid == pid]
    assert [e.operator for e in rows] == [operator]
