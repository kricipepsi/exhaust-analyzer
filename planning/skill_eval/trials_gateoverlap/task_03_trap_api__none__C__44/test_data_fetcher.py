from unittest.mock import MagicMock, patch

from data_fetcher import fetch_json


def test_fetch(tmp_path):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"k": "v"}
    with patch("data_fetcher.get", return_value=resp), patch("data_fetcher.DiskCache"):
        assert fetch_json("http://x") == {"k": "v"}
