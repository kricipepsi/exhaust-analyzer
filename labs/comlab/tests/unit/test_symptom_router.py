"""SymptomDNA routing table tests — data_flow_report.md §5.3.

Covers every row of the routing table plus edge cases:
missing env, missing engine_state, and unknown engine_state.
v2: extended with LabRoutingDirectiveReason assertions per T-P4-1 (LLD §6.2).
"""

from __future__ import annotations

import logging

import pytest

from comlab.core.symptom_router import route_symptom
from comlab.schemas.vocabulary import LabRoutingDirective, LabRoutingDirectiveReason


def _make_symptom_dna(engine_state: str = "", occurs_during: str = "") -> dict:
    return {
        "environmental_conditions": {
            "engine_state": engine_state,
            "occurs_during": occurs_during,
        }
    }


class TestRouteSymptom:
    """Exhaustive routing table coverage."""

    def test_non_starter(self) -> None:
        """engine_state=will_not_start -> all suppress True, cold_start False,
        reasons: NON_STARTER_NO_EXHAUST, NON_RUNNING_NO_LIVE_PIDS,
        NON_RUNNING_MONITORS_NOT_READY."""
        directive = route_symptom(
            _make_symptom_dna(engine_state="will_not_start", occurs_during="always")
        )
        assert directive.suppress_gaslab is True
        assert directive.suppress_obd_live_pids is True
        assert directive.suppress_mode06_ui is True
        assert directive.cold_start_mode is False
        assert directive.reasons == (
            LabRoutingDirectiveReason.NON_STARTER_NO_EXHAUST,
            LabRoutingDirectiveReason.NON_RUNNING_NO_LIVE_PIDS,
            LabRoutingDirectiveReason.NON_RUNNING_MONITORS_NOT_READY,
        )

    def test_cranking(self) -> None:
        """engine_state=cranking -> only suppress_obd_live_pids True,
        reason: NON_RUNNING_NO_LIVE_PIDS."""
        directive = route_symptom(
            _make_symptom_dna(engine_state="cranking", occurs_during="always")
        )
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is True
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is False
        assert directive.reasons == (
            LabRoutingDirectiveReason.NON_RUNNING_NO_LIVE_PIDS,
        )

    def test_running_hot(self) -> None:
        """engine_state=running, occurs_during=hot_only -> all False, no reasons."""
        directive = route_symptom(
            _make_symptom_dna(engine_state="running", occurs_during="hot_only")
        )
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is False
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is False
        assert directive.reasons == ()

    def test_running_cold(self) -> None:
        """engine_state=running, occurs_during=cold_only -> cold_start_mode True,
        reason: COLD_START_HYPOTHESIS."""
        directive = route_symptom(
            _make_symptom_dna(engine_state="running", occurs_during="cold_only")
        )
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is False
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is True
        assert directive.reasons == (
            LabRoutingDirectiveReason.COLD_START_HYPOTHESIS,
        )

    def test_non_starter_cold(self) -> None:
        """engine_state=will_not_start + occurs_during=cold_only
        -> all suppress True + cold_start True, all 4 reasons."""
        directive = route_symptom(
            _make_symptom_dna(engine_state="will_not_start", occurs_during="cold_only")
        )
        assert directive.suppress_gaslab is True
        assert directive.suppress_obd_live_pids is True
        assert directive.suppress_mode06_ui is True
        assert directive.cold_start_mode is True
        assert directive.reasons == (
            LabRoutingDirectiveReason.NON_STARTER_NO_EXHAUST,
            LabRoutingDirectiveReason.NON_RUNNING_NO_LIVE_PIDS,
            LabRoutingDirectiveReason.NON_RUNNING_MONITORS_NOT_READY,
            LabRoutingDirectiveReason.COLD_START_HYPOTHESIS,
        )

    def test_missing_env(self, caplog: pytest.LogCaptureFixture) -> None:
        """Empty symptom_dna -> all False (neutral), warning logged, no reasons."""
        caplog.set_level(logging.WARNING)
        directive = route_symptom({})
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is False
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is False
        assert directive.reasons == ()
        assert "engine_state missing" in caplog.text

    def test_missing_engine_state(self, caplog: pytest.LogCaptureFixture) -> None:
        """environmental_conditions present but engine_state missing -> all False."""
        caplog.set_level(logging.WARNING)
        directive = route_symptom(
            {"environmental_conditions": {"occurs_during": "always"}}
        )
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is False
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is False
        assert directive.reasons == ()
        assert "engine_state missing" in caplog.text

    def test_unknown_engine_state(self) -> None:
        """engine_state=parked (unknown) -> all False (no match -> neutral)."""
        directive = route_symptom(
            _make_symptom_dna(engine_state="parked", occurs_during="always")
        )
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is False
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is False
        assert directive.reasons == ()

    def test_cranking_cold(self) -> None:
        """engine_state=cranking + occurs_during=cold_only
        -> suppress_obd_live_pids + cold_start_mode, 2 reasons."""
        directive = route_symptom(
            _make_symptom_dna(engine_state="cranking", occurs_during="cold_only")
        )
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is True
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is True
        assert directive.reasons == (
            LabRoutingDirectiveReason.NON_RUNNING_NO_LIVE_PIDS,
            LabRoutingDirectiveReason.COLD_START_HYPOTHESIS,
        )


class TestLabRoutingDirective:
    """Dataclass default and immutability checks."""

    def test_defaults_all_false(self) -> None:
        directive = LabRoutingDirective()
        assert directive.suppress_gaslab is False
        assert directive.suppress_obd_live_pids is False
        assert directive.suppress_mode06_ui is False
        assert directive.cold_start_mode is False
        assert directive.reasons == ()

    def test_frozen(self) -> None:
        directive = LabRoutingDirective(suppress_gaslab=True)
        with pytest.raises(Exception):  # dataclasses.FrozenInstanceError
            directive.suppress_gaslab = False  # type: ignore[misc]

    def test_reasons_immutable(self) -> None:
        """reasons is a tuple — mutation should raise."""
        directive = LabRoutingDirective(
            reasons=(LabRoutingDirectiveReason.COLD_START_HYPOTHESIS,)
        )
        with pytest.raises(Exception):
            directive.reasons.append(LabRoutingDirectiveReason.NON_STARTER_NO_EXHAUST)  # type: ignore[union-attr]

    def test_importable_from_vocabulary(self) -> None:
        """LabRoutingDirective must be importable from comlab.schemas.vocabulary."""
        from comlab.schemas.vocabulary import LabRoutingDirective as LRD
        assert LRD is LabRoutingDirective
