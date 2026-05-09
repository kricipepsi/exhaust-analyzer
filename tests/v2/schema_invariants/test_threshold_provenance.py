"""Assert every numeric threshold cites a source_guide comment (R10, L08)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
THRESHOLDS_PATH = ROOT / "schema" / "v2" / "thresholds.yaml"

_NUMERIC_LINE = re.compile(r"^\s+\w+:\s+\d+\.?\d*\b")


def test_threshold_provenance() -> None:
    """Every numeric threshold in thresholds.yaml must have a # source_guide: comment."""
    lines = THRESHOLDS_PATH.read_text(encoding="utf-8").splitlines()
    violations: list[str] = []
    for i, line in enumerate(lines, start=1):
        if _NUMERIC_LINE.match(line) and "source_guide:" not in line:
            violations.append(f"Line {i}: {line.strip()}")

    assert violations == [], (  # nosec B101
        "Numeric thresholds without source_guide comment (L08):\n"
        + "\n".join(violations)
    )
