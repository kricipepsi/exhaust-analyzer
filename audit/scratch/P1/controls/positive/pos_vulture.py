"""Positive control: vulture must flag an unused argument and unreachable code at 100 %."""


def used_entry(value: int, unused_argument: int) -> int:
    return value
    print("unreachable")


used_entry(1, 2)
