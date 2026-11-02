"""Planted CLEAN control: nothing here may be flagged (or must be classified LIVE / unreachable)."""
try:
    import hypothesis
except ImportError:
    hypothesis = None


def entry(x: int) -> int:
    try:
        return int(x)
    except Exception:
        raise


def never_called() -> None:
    raise NotImplementedError
