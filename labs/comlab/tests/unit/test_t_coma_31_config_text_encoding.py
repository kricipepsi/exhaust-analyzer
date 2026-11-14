"""T-COMA-31: no string in global_fault_registry.json or config/kg/*.json is UTF-8 text that was decoded as cp1252 (mojibake such as 'â€”' for '—').

Found by the T-AUD-22c survey: 372 escape runs in global_fault_registry.json and 11 KG files. Fixed in place.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

CONFIG = Path(__file__).resolve().parents[2] / "comlab" / "config"
FILES = sorted([CONFIG / "global_fault_registry.json", *(CONFIG / "kg").glob("*.json")])


def _mojibake(s: str) -> bool:
    if s.isascii():
        return False
    try:
        return s.encode("cp1252").decode("utf-8") != s
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False


def _strings(node: object):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from _strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v)


def test_config_files_found() -> None:
    assert len(FILES) == 15  # global_fault_registry.json + 14 KG files (T-COMA-31 review L3)


# Independent of the cp1252 round-trip (review M2): the raw text holds no escaped or literal mojibake lead bytes.
_BS = chr(92)
_RAW_MARKERS = (_BS + "u00e2" + _BS + "u20ac", _BS + "u00c3", _BS + "u00c2", "â€", "Ã", "Â")


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_no_raw_mojibake_markers(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    hits = [m for m in _RAW_MARKERS if m in raw]
    assert not hits, f"{path.name}: raw mojibake markers {hits}"


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_no_double_encoded_text(path: Path) -> None:
    bad = [s[:60] for s in _strings(json.loads(path.read_text(encoding="utf-8"))) if _mojibake(s)]
    assert not bad, f"{path.name}: {len(bad)} double-encoded strings, first {bad[0]!r}"


def test_detector_catches_the_defect() -> None:
    assert _mojibake("Ignition / Fuel Interface â€” Spark Energy")
    assert not _mojibake("Ignition / Fuel Interface — Spark Energy")
