"""Positive control: pyright basic must flag optional, unbound and attribute errors here."""


def optional_member(x: str | None) -> str:
    return x.upper()  # reportOptionalMemberAccess


def possibly_unbound(flag: bool) -> int:
    if flag:
        y = 1
    return y  # reportPossiblyUnbound


def bad_attribute() -> int:
    return (1).no_such_attribute  # reportAttributeAccessIssue
