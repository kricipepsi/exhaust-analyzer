"""Planted POSITIVE control: every census kind must flag something here."""
from typing import Any

try:
    import json
except ImportError:
    json = None

try:
    import p2_no_such_module_xyz
except ImportError:
    p2_no_such_module_xyz = None


def entry(x: Any) -> Any:
    fn = caller  # reference edge, called indirectly
    fn()
    return helper(x)


def helper(x):  # type: ignore
    # TODO: planted reachable todo
    try:
        return int(x)
    except Exception:
        return 0


def unfinished():
    raise NotImplementedError


def swallow():
    try:
        unfinished()
    except:  # noqa: E722
        pass


def caller():
    swallow()

