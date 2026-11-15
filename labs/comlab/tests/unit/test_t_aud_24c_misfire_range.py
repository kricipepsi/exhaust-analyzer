from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_COMLAB_ROOT = Path(__file__).resolve().parents[2]
_MISFIRE_RULE_FILES = (
    _COMLAB_ROOT / "comlab" / "config" / "global_fault_registry.json",
    _COMLAB_ROOT / "registry" / "rules" / "misfire.json",
    _COMLAB_ROOT / "registry" / "rules" / "mechanical_wear.json",
)
_EXTENDED_CYLINDER_CODES = tuple(f"P03{idx:02d}" for idx in range(5, 13))


def _walk_misfire_lists(node: Any, out: list[list[str]]) -> None:
    if isinstance(node, list):
        if all(isinstance(item, str) for item in node) and "P0301" in node and "P0304" in node:
            out.append(node)
        for item in node:
            _walk_misfire_lists(item, out)
    elif isinstance(node, dict):
        for value in node.values():
            _walk_misfire_lists(value, out)


def test_misfire_dtc_lists_extend_to_p0312() -> None:
    matched_lists: list[tuple[str, list[str]]] = []
    for path in _MISFIRE_RULE_FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        found: list[list[str]] = []
        _walk_misfire_lists(data, found)
        for dtc_list in found:
            matched_lists.append((path.name, dtc_list))

    assert len(matched_lists) >= 15, f"Expected at least 15 misfire lists, found {len(matched_lists)}"
    for filename, dtc_list in matched_lists:
        missing = [code for code in _EXTENDED_CYLINDER_CODES if code not in dtc_list]
        assert not missing, f"{filename} list missing extended misfire codes: {missing}"
