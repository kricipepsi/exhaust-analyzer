import pytest


def _check(x):
    assert x == 1


def test_via_helper():
    _check(1)


def test_raises():
    with pytest.raises(ValueError):
        int("x")
