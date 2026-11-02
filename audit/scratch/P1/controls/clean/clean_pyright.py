"""Clean control: the same shapes, guarded. pyright basic must stay silent."""


def optional_member(x: str | None) -> str:
    return x.upper() if x is not None else ""


def possibly_unbound(flag: bool) -> int:
    y = 0
    if flag:
        y = 1
    return y


def good_attribute() -> int:
    return (1).bit_length()
