"""Positive control: each custom semgrep rule must fire once here."""
import sys

import yaml


def f(data, acc=[]):
    assert data
    sys.path.insert(0, "x")
    try:
        return yaml.load(data)
    except Exception:
        pass
    return data == 0.02
