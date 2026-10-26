"""Clean control: every name is used; vulture must stay silent."""


def used_entry(value: int, other: int) -> int:
    return value + other


print(used_entry(1, 2))
