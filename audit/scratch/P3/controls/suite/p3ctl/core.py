"""Planted production module for the P3 instrument controls."""
LIMIT = 5


def verdict(x: float) -> str:
    if x > 10:
        return "HIGH"
    if x < 0:  # planted untaken branch: no control test passes a negative value
        return "NEG"
    return "LOW"


def never_called() -> int:  # planted unreached function
    return 42
