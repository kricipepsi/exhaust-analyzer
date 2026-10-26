import pytest


@pytest.mark.skip(reason="planted")
def test_skipped():
    assert True


def test_always_fails():
    pytest.fail("planted")


def test_no_assert():
    int("1")


def test_dup():
    assert 1


def test_dup():  # noqa: F811
    assert 2
