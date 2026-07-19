from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest
from data_fetcher import FetchError, fetch_json


def _mock_response(payload: bytes) -> MagicMock:
    response = MagicMock()
    response.read.return_value = payload
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


def test_url_error_raises_fetch_error_regression(tmp_path: Path) -> None:
    """GUARD: unreachable URL raises FetchError, not a bare URLError (error path)."""
    with patch("data_fetcher.urlopen", side_effect=URLError("unreachable")):
        with pytest.raises(FetchError):
            fetch_json("http://x/api", cache_dir=str(tmp_path))


def test_fetch_error_message_carries_url_regression(tmp_path: Path) -> None:
    """GUARD: FetchError message includes the offending URL (diagnosability)."""
    with patch("data_fetcher.urlopen", side_effect=URLError("nope")):
        with pytest.raises(FetchError, match="http://x/api"):
            fetch_json("http://x/api", cache_dir=str(tmp_path))


def test_invalid_json_raises_fetch_error_regression(tmp_path: Path) -> None:
    """GUARD: a 200 body that is not JSON raises FetchError, not JSONDecodeError."""
    response = _mock_response(b"not json at all")
    with patch("data_fetcher.urlopen", return_value=response):
        with pytest.raises(FetchError):
            fetch_json("http://x/api", cache_dir=str(tmp_path))


def test_cache_hit_does_not_call_network_regression(tmp_path: Path) -> None:
    """GUARD: second call hits cache; urlopen must not be called twice (cache path)."""
    response = _mock_response(b'{"v": 1}')
    with patch("data_fetcher.urlopen", return_value=response) as opener:
        fetch_json("http://x/api", cache_dir=str(tmp_path))
        fetch_json("http://x/api", cache_dir=str(tmp_path))
    assert opener.call_count == 1


def test_cache_roundtrip_returns_same_value_regression(tmp_path: Path) -> None:
    """GUARD: cached read returns the same payload the miss path wrote (parity)."""
    response = _mock_response(b'{"v": 7}')
    with patch("data_fetcher.urlopen", return_value=response):
        first = fetch_json("http://x/api", cache_dir=str(tmp_path))
    # Second call: no network patched in -> must come from cache or it would error.
    second = fetch_json("http://x/api", cache_dir=str(tmp_path))
    assert first == second == {"v": 7}
