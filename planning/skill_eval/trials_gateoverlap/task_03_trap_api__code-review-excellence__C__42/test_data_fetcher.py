from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from data_fetcher import FetchError, fetch_json


def test_returns_json(tmp_path) -> None:
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"k": "v"}
    with patch("data_fetcher.get", return_value=resp), patch("data_fetcher.DiskCache"):
        assert fetch_json("http://x") == {"k": "v"}


def test_raises_on_error(tmp_path) -> None:
    resp = MagicMock()
    resp.status_code = 500
    with patch("data_fetcher.get", return_value=resp), patch("data_fetcher.DiskCache"):
        with pytest.raises(FetchError):
            fetch_json("http://x")
