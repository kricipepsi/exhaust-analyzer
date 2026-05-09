"""Assert no two sibling faults share identical discriminator[] sets (R5, L03)."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
FAULTS_PATH = ROOT / "schema" / "v2" / "faults.yaml"


def _load_faults() -> dict:
    with open(FAULTS_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def test_unique_discriminators_among_siblings() -> None:
    """Every child fault under the same parent must have a unique discriminator set."""
    faults = _load_faults()

    siblings: dict[str, list[tuple[str, frozenset[str]]]] = {}
    for fault_id, fault_data in faults.items():
        parent = fault_data.get("parent")
        if parent is None:
            continue
        discriminator = fault_data.get("discriminator")
        if discriminator is None:
            discriminator = []
        if isinstance(discriminator, str):
            discriminator = [discriminator]
        siblings.setdefault(parent, []).append((fault_id, frozenset(discriminator)))

    violations: list[str] = []
    for parent, children in siblings.items():
        seen: dict[frozenset[str], str] = {}
        for fault_id, disc_set in children:
            if disc_set in seen:
                violations.append(
                    f"Parent '{parent}': siblings '{seen[disc_set]}' and "
                    f"'{fault_id}' share identical discriminator[]: {sorted(disc_set)}"
                )
            else:
                seen[disc_set] = fault_id

    assert violations == [], (  # nosec B101
        "Sibling faults with identical discriminator[] sets found (L03):\n"
        + "\n".join(violations)
    )
