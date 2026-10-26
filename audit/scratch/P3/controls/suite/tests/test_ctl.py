"""Planted tests: each name states the class the instrument must assign."""
from unittest.mock import Mock

from p3ctl.core import LIMIT, verdict


def test_clean_behaviour_value():  # clean control: must be behaviour, never placeholder
    assert verdict(20) == "HIGH"


def test_clean_behaviour_control_dependent():  # clean control: data flows through an if
    seen = False
    if verdict(1) == "LOW":
        seen = True
    assert seen


def test_planted_interface_shape():
    assert isinstance(verdict(1), str)


def test_planted_placeholder_constant():  # positive control: asserts a production constant only
    assert LIMIT == 5


def test_planted_placeholder_double():  # positive control: asserts only on a Mock
    m = Mock()
    m()
    m.assert_called_once()


def test_planted_placeholder_early_return():  # positive control: assert never executes
    if LIMIT:
        return
    assert verdict(1) == "LOW"


def test_planted_misnamed_verdict_is_high():  # name claims a value; it only checks presence
    assert verdict(20) is not None
