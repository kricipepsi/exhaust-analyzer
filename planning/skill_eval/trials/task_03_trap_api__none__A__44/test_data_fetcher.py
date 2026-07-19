from unittest.mock import patch, MagicMock
import pytest
from data_fetcher import fetch_json, FetchError


def test_fetch_returns_data():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"key": "value"}

    with patch("data_fetcher.get", return_value=mock_resp), \
         patch("data_fetcher.DiskCache") as mock_cache_cls:
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        mock_cache_cls.return_value = mock_cache

        result = fetch_json("http://example.com/api")
        assert result == {"key": "value"}
        mock_cache.set.assert_called_once()


def test_fetch_returns_cached():
    with patch("data_fetcher.DiskCache") as mock_cache_cls:
        mock_cache = MagicMock()
        mock_cache.get.return_value = {"cached": True}
        mock_cache_cls.return_value = mock_cache

        result = fetch_json("http://example.com/api")
        assert result == {"cached": True}


def test_fetch_error_on_http_failure():
    mock_resp = MagicMock()
    mock_resp.status_code = 404

    with patch("data_fetcher.get", return_value=mock_resp), \
         patch("data_fetcher.DiskCache") as mock_cache_cls:
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        mock_cache_cls.return_value = mock_cache

        with pytest.raises(FetchError, match="404"):
            fetch_json("http://example.com/api")
