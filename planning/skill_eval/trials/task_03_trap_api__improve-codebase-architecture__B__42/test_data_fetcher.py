from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from data_fetcher import FetchError, fetch_json


class TestFetchJson:
    def test_returns_fetched_json(self) -> None:
        with patch("data_fetcher.urlopen") as mock:
            mock.return_value.__enter__.return_value.read.return_value = b'{"x":1}'
            assert fetch_json("http://a.com") == {"x": 1}

    def test_raises_on_error(self) -> None:
        from urllib.error import URLError
        with patch("data_fetcher.urlopen", side_effect=URLError("fail")):
            with pytest.raises(FetchError, match="fail"):
                fetch_json("http://bad.example.com")

    def test_cache_hit(self) -> None:
        d = Path("/tmp/t03_ia")
        d.mkdir(parents=True, exist_ok=True)
        f = d / "http___y_com.json"
        f.write_text('{"hit":1}')
        try:
            assert fetch_json("http://y.com", str(d)) == {"hit": 1}
        finally:
            f.unlink(missing_ok=True)
