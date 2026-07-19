from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from data_fetcher import FetchError, fetch_json


class DescribeFetchJson:
    def test_returns_parsed_json(self) -> None:
        payload = json.dumps({"key": "value"}).encode()
        with patch("data_fetcher.urlopen") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = payload
            result = fetch_json("http://example.com/api", cache_dir="/tmp/cache")
        assert result == {"key": "value"}

    def test_raises_fetch_error_on_urlerror(self) -> None:
        from urllib.error import URLError
        with patch("data_fetcher.urlopen", side_effect=URLError("refused")):
            with pytest.raises(FetchError, match="refused"):
                fetch_json("http://down.example.com")

    def test_raises_fetch_error_on_bad_json(self) -> None:
        with patch("data_fetcher.urlopen") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b"not json"
            with pytest.raises(FetchError, match="not valid JSON"):
                fetch_json("http://example.com/bad")

    def test_cache_hit_avoids_request(self) -> None:
        cache_dir = Path("/tmp/test_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        key = "http___example_com_data.json"
        (cache_dir / key).write_text('{"from_cache":true}')
        try:
            result = fetch_json("http://example.com/data", cache_dir=str(cache_dir))
            assert result == {"from_cache": True}
        finally:
            (cache_dir / key).unlink(missing_ok=True)
