from __future__ import annotations

import json
from pathlib import Path

import pytest

from vinlab import decode

FIXTURES_DIR = Path(__file__).parents[1] / "fixtures" / "vindna_pre_refactor"


def _fixture_paths() -> list[Path]:
    return sorted(FIXTURES_DIR.glob("*.json"))


@pytest.mark.parametrize("fixture_path", _fixture_paths(), ids=lambda p: p.name)
def test_vindna_roundtrip_byte_identical(fixture_path: Path) -> None:
    """decode().to_json() output is byte-identical to the pre-refactor fixture."""
    with open(fixture_path, encoding="utf-8") as fh:
        expected = json.load(fh)
    actual = decode(expected["vin"]).to_json_payload()
    assert json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
