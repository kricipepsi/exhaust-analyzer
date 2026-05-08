"""Assert no forbidden fuel-type tokens in engine/v2/ and schema/v2/.

Enforces R12 and L20: petrol-only is a CI lint, not a convention.
Any token lpg, cng, e85, diesel, or hybrid in these directories fails.
"""
from pathlib import Path

FORBIDDEN: frozenset[str] = frozenset({"lpg", "cng", "e85", "diesel", "hybrid"})
ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENGINE_V2 = ROOT / "engine" / "v2"
SCHEMA_V2 = ROOT / "schema" / "v2"


def _scan_dir(directory: Path) -> list[str]:
    violations: list[str] = []
    if not directory.exists():
        return violations
    for filepath in directory.rglob("*"):
        if not filepath.is_file():
            continue
        try:
            text = filepath.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            continue
        for token in FORBIDDEN:
            if token in text:
                violations.append(
                    f"{filepath.relative_to(ROOT)}: forbidden token '{token}'"
                )
    return violations


def test_engine_v2_no_forbidden_tokens() -> None:
    """engine/v2/ must not contain lpg, cng, e85, diesel, or hybrid."""
    violations = _scan_dir(ENGINE_V2)
    assert violations == [], (  # nosec B101
        "Forbidden tokens found in engine/v2/:\n" + "\n".join(violations)
    )


def test_schema_v2_no_forbidden_tokens() -> None:
    """schema/v2/ must not contain lpg, cng, e85, diesel, or hybrid."""
    violations = _scan_dir(SCHEMA_V2)
    assert violations == [], (  # nosec B101
        "Forbidden tokens found in schema/v2/:\n" + "\n".join(violations)
    )
