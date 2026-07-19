"""T-W-ARCH-6: assert explicit ``use_v2_registry`` selects the intended engine.

Verifies that the new constructor argument controls the v1/v2 path gate
independently of the ``USE_V2_REGISTRY`` environment variable.
"""

from __future__ import annotations

import os
from unittest.mock import patch

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter


def _router_deps() -> tuple[FaultAtlasKG, PowerLossAnalytics]:
    """Return real constructor dependencies; registry loading is patched out."""
    return FaultAtlasKG(), PowerLossAnalytics()



def test_use_v2_registry_true_selects_v2_path() -> None:
    """Explicit use_v2_registry=True sets the v2 flag."""
    kg, analytics = _router_deps()
    with patch.object(FaultAtlasRouter, "_load_registry", return_value=None):
        router = FaultAtlasRouter(
            "/fake/path.json", kg, analytics, use_v2_registry=True,
        )
        assert router._use_v2_registry is True


def test_use_v2_registry_false_selects_v1_path() -> None:
    """Explicit use_v2_registry=False sets the v1 (legacy) flag."""
    kg, analytics = _router_deps()
    with patch.object(FaultAtlasRouter, "_load_registry", return_value=None):
        router = FaultAtlasRouter(
            "/fake/path.json", kg, analytics, use_v2_registry=False,
        )
        assert router._use_v2_registry is False


def test_default_is_v2() -> None:
    """Without an explicit arg the router defaults to REG-V2."""
    kg, analytics = _router_deps()
    with patch.object(FaultAtlasRouter, "_load_registry", return_value=None):
        router = FaultAtlasRouter("/fake/path.json", kg, analytics)
        assert router._use_v2_registry is True


def test_env_var_does_not_override_explicit() -> None:
    """Explicit arg wins over any USE_V2_REGISTRY env value."""
    os.environ["USE_V2_REGISTRY"] = "0"
    try:
        kg, analytics = _router_deps()
        with patch.object(FaultAtlasRouter, "_load_registry", return_value=None):
            router = FaultAtlasRouter(
                "/fake/path.json", kg, analytics, use_v2_registry=True,
            )
            assert router._use_v2_registry is True  # explicit wins over env
    finally:
        del os.environ["USE_V2_REGISTRY"]
