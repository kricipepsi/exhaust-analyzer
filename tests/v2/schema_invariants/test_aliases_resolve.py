"""Assert every non-null alias target resolves to a valid schema ID (L09)."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
ALIASES_PATH = ROOT / "schema" / "v2" / "label_aliases.yaml"
SYMPTOMS_PATH = ROOT / "schema" / "v2" / "symptoms.yaml"
FAULTS_PATH = ROOT / "schema" / "v2" / "faults.yaml"


def _load_yaml_keys(path: Path) -> set[str]:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return set(data.keys()) if data else set()


def test_aliases_resolve() -> None:
    """Every non-null alias target must exist in symptoms.yaml or faults.yaml."""
    with open(ALIASES_PATH, encoding="utf-8") as fh:
        aliases = yaml.safe_load(fh)

    valid_ids = _load_yaml_keys(SYMPTOMS_PATH) | _load_yaml_keys(FAULTS_PATH)

    violations: list[str] = []
    for alias_id, entry in aliases.items():
        target = entry.get("target")
        if target is None:
            continue
        if target not in valid_ids:
            violations.append(
                f"Alias '{alias_id}' -> '{target}' does not resolve "
                f"in symptoms.yaml or faults.yaml"
            )

    assert violations == [], (  # nosec B101
        "Unresolvable alias targets found (L09):\n"
        + "\n".join(violations)
    )
