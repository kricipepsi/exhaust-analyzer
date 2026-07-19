from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from data_fetcher import FetchError, fetch_json


def _mock_response(payload: bytes) -> MagicMock:
    response = MagicMock()
    response.read.return_value = payload
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class TestFetchJson:
    def test_returns_parsed_json_on_miss(self, tmp_path: Path) -> None:
        response = _mock_response(b'{"key": "value"}')
        with patch("data_fetcher.urlopen", return_value=response):
            result = fetch_json("http://example.com/api", cache_dir=str(tmp_path))
        assert result == {"key": "value"}

    def test_writes_cache_on_miss(self, tmp_path: Path) -> None:
        response = _mock_response(b'{"n": 1}')
        with patch("data_fetcher.urlopen", return_value=response):
            fetch_json("http://example.com/api", cache_dir=str(tmp_path))
        cached = list(tmp_path.glob("*.json"))
        assert len(cached) == 1
        assert json.loads(cached[0].read_text(encoding="utf-8")) == {"n": 1}

    def test_cache_hit_skips_network(self, tmp_path: Path) -> None:
        response = _mock_response(b'{"first": true}')
        with patch("data_fetcher.urlopen", return_value=response) as opener:
            fetch_json("http://example.com/api", cache_dir=str(tmp_path))
            fetch_json("http://example.com/api", cache_dir=str(tmp_path))
        assert opener.call_count == 1

    def test_url_error_raises_fetch_error(self, tmp_path: Path) -> None:
        from urllib.error import URLError

        with patch("data_fetcher.urlopen", side_effect=URLError("down")):
            with pytest.raises(FetchError):
                fetch_json("http://example.com/api", cache_dir=str(tmp_path))
