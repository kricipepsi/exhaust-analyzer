"""Standalone verification — vinlab imports without MySQL or requests."""

from __future__ import annotations

import sys
from unittest import mock


def test_import_without_mysql():
    """vinlab imports cleanly when mysql.connector is absent."""
    with mock.patch.dict(sys.modules, {"mysql.connector": None}):
        # Force reimport of vinlab modules to catch import-time errors
        modules_to_reload = [
            k for k in list(sys.modules.keys())
            if k.startswith("vinlab")
        ]
        for m in modules_to_reload:
            del sys.modules[m]

        import vinlab  # noqa: F811
        assert vinlab.decode is not None


def test_import_without_requests():
    """vinlab imports cleanly when requests is absent."""
    with mock.patch.dict(sys.modules, {"requests": None}):
        modules_to_reload = [
            k for k in list(sys.modules.keys())
            if k.startswith("vinlab")
        ]
        for m in modules_to_reload:
            del sys.modules[m]

        import vinlab
        assert vinlab.decode is not None


def test_import_without_both():
    """vinlab imports cleanly with both mysql.connector and requests absent."""
    with mock.patch.dict(sys.modules, {"mysql.connector": None, "requests": None}):
        modules_to_reload = [
            k for k in list(sys.modules.keys())
            if k.startswith("vinlab")
        ]
        for m in modules_to_reload:
            del sys.modules[m]

        import vinlab
        assert vinlab.decode is not None


def test_decode_without_network_dependencies():
    """decode() works with mysql and requests mocked absent."""
    with mock.patch.dict(sys.modules, {"mysql.connector": None, "requests": None}):
        modules_to_reload = [
            k for k in list(sys.modules.keys())
            if k.startswith("vinlab")
        ]
        for m in modules_to_reload:
            del sys.modules[m]

        from vinlab import VinDNA, decode
        dna = decode("VF1CB05CF25935016")
        assert isinstance(dna, VinDNA)
        assert dna.confidence in ("HIGH", "PARTIAL")
