"""REG-V2 activation guard for the wired app.

The side-by-side harness refuses to run against a partial registry. The current
registry ships 73 rules; this guard keeps the wired package pinned to that count.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_EXPECTED_RULE_COUNT = 73  # dossier: registry/docs/REGISTRY_PROGRESS.md wired-registry-guard-rule-count-drift
_DEFAULT_RULES_DIR = Path(__file__).resolve().parents[3] / "labs" / "comlab" / "registry" / "rules"


class RegistryActivationError(RuntimeError):
    """Raised when REG-V2 rule files are missing or drift from the expected count."""


def assert_registry_ready(rules_dir: Path | None = None) -> None:
    """Validate that the on-disk REG-V2 registry has the expected 73 rules."""
    root = rules_dir or _DEFAULT_RULES_DIR
    if not root.exists():
        raise RegistryActivationError(f"registry rules dir not found: {root}")

    rule_count = _count_rules(root)
    if rule_count != _EXPECTED_RULE_COUNT:
        raise RegistryActivationError(
            f"REG-V2 registry expected {_EXPECTED_RULE_COUNT} rules, found {rule_count} in {root}"
        )


def _count_rules(rules_dir: Path) -> int:
    """Count JSON rule objects under ``rules_dir`` without importing COMLab internals."""
    total = 0
    for rule_file in sorted(rules_dir.glob("*.json")):
        payload: Any = json.loads(rule_file.read_text(encoding="utf-8"))
        rules = payload.get("rules") if isinstance(payload, dict) else None
        if not isinstance(rules, list):
            raise RegistryActivationError(f"registry rule file lacks list 'rules': {rule_file}")
        total += len(rules)
    return total


__all__ = ["RegistryActivationError", "assert_registry_ready"]
