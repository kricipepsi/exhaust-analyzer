"""Assert every fault has a non-empty era[] list with valid era buckets (R6)."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
FAULTS_PATH = ROOT / "schema" / "v2" / "faults.yaml"

VALID_ERAS: frozenset[str] = frozenset({
    "1990-1995",
    "1996-2005",
    "2006-2015",
    "2016-2020",
})


def test_era_validity() -> None:
    """Every fault must have a non-empty era[] list with valid era bucket strings."""
    with open(FAULTS_PATH, encoding="utf-8") as fh:
        faults = yaml.safe_load(fh)

    violations: list[str] = []
    for fault_id, fault_data in faults.items():
        era = fault_data.get("era")
        if isinstance(era, str):
            violations.append(
                f"'{fault_id}': era is a string '{era}', expected list"
            )
            continue
        if not era:
            violations.append(f"'{fault_id}': missing or empty era[]")
            continue
        for bucket in era:
            if bucket not in VALID_ERAS:
                violations.append(
                    f"'{fault_id}': invalid era bucket '{bucket}'"
                )

    assert violations == [], (  # nosec B101
        "Fault era validity violations (R6):\n"
        + "\n".join(violations)
    )
