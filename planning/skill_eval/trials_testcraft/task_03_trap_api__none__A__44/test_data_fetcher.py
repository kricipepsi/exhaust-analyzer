from unittest.mock import MagicMock, patch

from data_fetcher import fetch_json


def test_fetch_returns_data(tmp_path):
    payload = b'{"key": "value"}'
    response = MagicMock()
    response.read.return_value = payload
    response.__enter__.return_value = response
    with patch("data_fetcher.urlopen", return_value=response):
        result = fetch_json("http://example.com/api", cache_dir=str(tmp_path))
    assert result == {"key": "value"}
