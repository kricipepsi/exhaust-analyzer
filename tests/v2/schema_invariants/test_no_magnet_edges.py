"""Assert no edge weight > 0.30 without discriminator_gate (R7, L07)."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent
EDGES_PATH = ROOT / "schema" / "v2" / "edges.yaml"


def test_no_magnet_edges() -> None:
    """No edge weight > 0.30 without a discriminator_gate field."""
    with open(EDGES_PATH, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    edges = data.get("edges", [])
    violations: list[str] = []
    for edge in edges:
        weight = edge.get("weight", 0.0)
        if weight > 0.30 and "discriminator_gate" not in edge:
            violations.append(
                f"{edge['source']} -> {edge['target']}: "
                f"weight={weight} > 0.30, no discriminator_gate"
            )

    assert violations == [], (  # nosec B101
        "Magnet edges found — weight > 0.30 without discriminator_gate (L07):\n"
        + "\n".join(violations)
    )
