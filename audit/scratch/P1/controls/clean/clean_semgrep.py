"""Clean control: the safe shapes of the same code; no custom rule may fire."""
import math

import yaml


def f(data, acc=None):
    if not data:
        raise ValueError("empty")
    try:
        return yaml.safe_load(data)
    except ValueError:
        return None
    finally:
        acc = acc or []
    return math.isclose(data, 0.02)
