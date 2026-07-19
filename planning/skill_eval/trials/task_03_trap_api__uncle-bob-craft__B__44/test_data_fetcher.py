from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from data_fetcher import FetchError, fetch_json


class TestFetchJson:
    def test_fetches_and_returns_json(self) -> None:
        payload = json.dumps({"ok": True}).encode()
        with patch("data_fetcher.urlopen") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = payload
            result = fetch_json("http://example.com/x")
        assert result == {"ok": True}

    def test_raises_on_connection_error(self) -> None:
        from urllib.error import URLError
        with patch("data_fetcher.urlopen", side_effect=URLError("timeout")):
            with pytest.raises(FetchError, match="timeout"):
                fetch_json("http://dead.example.com")

    def test_cache_hit(self) -> None:
        cache_dir = Path("/tmp/t03_ub_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        key_file = cache_dir / "http___x_com.json"
        key_file.write_text('{"cached":1}')
        try:
            assert fetch_json("http://x.com", str(cache_dir)) == {"cached": 1}
        finally:
            key_file.unlink(missing_ok=True)
