from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil

import pytest

from symptomlab import _get_validator, resolve


@pytest.fixture(autouse=True)
def _clear_validator_cache() -> Generator[None]:
    """Clear the lru_cache after each test to release resources."""
    yield
    _get_validator.cache_clear()


def test_same_allowed_path_returns_cached_instance(good_allowed_path: Path) -> None:
    """Calls with the same allowed_path reuse the cached validator instance."""
    v1 = _get_validator(good_allowed_path)
    v2 = _get_validator(good_allowed_path)
    assert v1 is v2


def test_different_allowed_path_returns_independent_instance(
    good_allowed_path: Path,
) -> None:
    """Calls with different allowed_path return different validator instances."""
    with TemporaryDirectory(ignore_cleanup_errors=True) as tmp1:
        tmp_yaml1 = Path(tmp1) / "allowed_combinations.yaml"
        shutil.copy2(str(good_allowed_path), str(tmp_yaml1))
        with TemporaryDirectory(ignore_cleanup_errors=True) as tmp2:
            tmp_yaml2 = Path(tmp2) / "allowed_combinations.yaml"
            shutil.copy2(str(good_allowed_path), str(tmp_yaml2))
            v1 = _get_validator(tmp_yaml1)
            v2 = _get_validator(tmp_yaml2)
            assert v1 is not v2


def test_resolve_with_explicit_allowed_path(
    allowed_pairs: list[tuple[str, str]],
    good_allowed_path: Path,
) -> None:
    """resolve() with an explicit allowed_path uses the injected test catalog."""
    tier_1, tier_2 = allowed_pairs[0]
    result = resolve(
        tier_1,
        tier_2,
        occurs_during="always",
        engine_state="running",
        load_state="steady_cruise",
        allowed_path=good_allowed_path,
    )
    assert result.tier_1_primary_symptom == tier_1
    assert result.tier_2_subfield_filter == tier_2
