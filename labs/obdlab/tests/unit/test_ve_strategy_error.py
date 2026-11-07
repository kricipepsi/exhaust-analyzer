"""T-AUD-17: an unknown air-metering strategy raises an ObdLabError subclass, not a bare ValueError (ADR-0005).

Tags: NEW fails on the base (ValueError); PIN passes there and after.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from obdlab.core.exceptions import ObdLabError
from obdlab.core.ve_engine import VEEngine
from obdlab.schemas.vocabulary import RpmStateBucket

BOGUS = SimpleNamespace(air_metering_strategy="BOGUS_STRATEGY", engine_displacement_liters=2.0)


def test_new_unknown_strategy_is_obdlab_error():
    from obdlab.core.exceptions import AirMeteringStrategyError
    with pytest.raises(AirMeteringStrategyError, match="Unknown air_metering_strategy") as caught:
        VEEngine().compute_ve({}, RpmStateBucket.STABILIZED_IDLE, BOGUS)
    assert isinstance(caught.value, ObdLabError) and type(caught.value) is AirMeteringStrategyError


def test_new_error_has_its_own_class():
    from obdlab.core.exceptions import AirMeteringStrategyError
    assert issubclass(AirMeteringStrategyError, ObdLabError)


def test_pin_no_dna_view_still_computes():
    ve, *_ = VEEngine().compute_ve({}, RpmStateBucket.STABILIZED_IDLE, None)
    assert ve is None
