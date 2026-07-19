"""Tests for dtclab.ranking — per-family confidence from §16 weights + §14.2 DNA gating.

Covers: §16 weight sourcing, max-over-contributors, DNA gate degradation,
MatchType derivation, monotonicity, POA_HISTORY exclusion.
"""

from __future__ import annotations


from dtclab.ranking import CandidateScore, MatchType, rank_candidates
from dtclab.schemas.dna_view import (
    DtcEmissionsView,
    DtcLabDnaView,
    EuroEmissionCategory,
    AirMeteringStrategy,
    ResolvedHorizon,
    VinConfidence,
)
from dtclab.schemas.mode06_result import Mode06MonitorResult
from dtclab.schemas.payload import DTCLabPayload, FreezeFrameRecord
from dtclab.schemas.vocabulary import (
    DTC_CONFIDENCE_WEIGHTS,
    DTCRoutingTag,
    FuelSystemStatus,
    HistoricalFaultContext,
    Mode06MonitorState,
)


# ---------------------------------------------------------------------------
# Minimal payload builder
# ---------------------------------------------------------------------------

def _payload(
    *,
    confirmed: list[str] | None = None,
    pending: list[str] | None = None,
    permanent: list[str] | None = None,
    routing_tags: list[DTCRoutingTag] | None = None,
    monitors: dict[str, Mode06MonitorResult] | None = None,
) -> DTCLabPayload:
    """Build a minimal DTCLabPayload for testing."""
    return DTCLabPayload(
        active_mil=False,
        mil_flashing=False,
        confirmed_dtcs=confirmed or [],
        pending_dtcs=pending or [],
        permanent_dtcs=permanent or [],
        routing_tags=routing_tags or [],
        mode_06_monitors=monitors or {},
        historical_fault_context=HistoricalFaultContext.UNKNOWN,
        freeze_frame=FreezeFrameRecord(
            coolant_temp_c=85.0,
            calculated_load_pct=30.0,
            engine_rpm=800,
            vehicle_speed_kmh=0,
            short_term_ft1=0.0,
            long_term_ft1=0.0,
            manifold_pressure_kpa=100.0,
            maf_gps=5.0,
            ignition_advance_deg=10.0,
            throttle_pos_pct=15.0,
            intake_air_temp_c=25.0,
            fuel_system_status=FuelSystemStatus.CL,
        ),
    )


def _monitor(state: Mode06MonitorState) -> Mode06MonitorResult:
    """Build a minimal Mode06MonitorResult with the given state."""
    return Mode06MonitorResult(
        monitor_id="MID_A1_TID_01",
        state=state,
        margin_pct=10.0,
        target_component="Test Component",
    )


def _dna_view(*, confidence: VinConfidence = VinConfidence.HIGH) -> DtcLabDnaView:
    """Build a DtcLabDnaView with catalyst-equipped defaults."""
    return DtcLabDnaView(
        make="BMW",
        model="330i",
        model_year=2006,
        euro_emission_category=EuroEmissionCategory.EURO_4,
        air_metering_strategy=AirMeteringStrategy.MAF,
        resolved_horizon=ResolvedHorizon.HORIZON_CLASSIC,
        emissions=DtcEmissionsView(
            has_catalyst=True,
            egr_equipped=False,
        ),
        confidence=confidence,
    )


# ===========================================================================
# test_state_weight_sourced_from_s16
# ===========================================================================


def test_state_weight_sourced_from_s16_confirmed() -> None:
    """A single CONFIRMED DTC contributes weight 1.0 from §16."""
    # P0171 → LEAN_HISTORY → lean_condition
    payload = _payload(
        confirmed=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    assert candidates[0].family == "lean_condition"
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["confirmed"]
    assert candidates[0].match_type == MatchType.DEFINITIVE


def test_state_weight_sourced_from_s16_permanent() -> None:
    """A PERMANENT DTC contributes weight 1.0 from §16."""
    payload = _payload(
        permanent=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["permanent"]


def test_state_weight_sourced_from_s16_pending() -> None:
    """A PENDING DTC contributes weight 0.5 from §16."""
    payload = _payload(
        pending=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["pending"]
    assert candidates[0].match_type == MatchType.INDICATIVE


def test_state_weight_sourced_from_s16_mode06_critical_fail() -> None:
    """A Mode $06 CRITICAL_FAIL contributes weight 0.7 from §16 on an active family."""
    payload = _payload(
        confirmed=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
        monitors={"MID_A1_TID_01": _monitor(Mode06MonitorState.CRITICAL_FAIL)},
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    # Monitor weight 0.7 > DTC weight 1.0? No — max is 1.0 from confirmed DTC
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["confirmed"]


def test_state_weight_sourced_from_s16_mode06_marginal() -> None:
    """A Mode $06 PENDING_FAIL_MARGINAL contributes weight 0.4 from §16."""
    payload = _payload(
        pending=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
        monitors={"MID_A1_TID_01": _monitor(Mode06MonitorState.PENDING_FAIL_MARGINAL)},
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["pending"]  # 0.5 > 0.4


def test_state_weight_sourced_from_s16_mode06_passed() -> None:
    """A Mode $06 PASSED contributes weight 0.0 from §16."""
    payload = _payload(
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
        monitors={"MID_A1_TID_01": _monitor(Mode06MonitorState.PASSED)},
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["mode06_passed"]
    assert candidates[0].match_type == MatchType.MONITOR_PASS


def test_state_weight_matches_dtc_confidence_weights() -> None:
    """Every weight used by the scorer is a key in DTC_CONFIDENCE_WEIGHTS."""
    # All weights come from the canonical dict — no new numerics.
    for key in ("confirmed", "permanent", "pending", "mode06_critical_fail",
                "mode06_marginal", "mode06_passed"):
        assert key in DTC_CONFIDENCE_WEIGHTS, f"missing key {key!r}"
        assert isinstance(DTC_CONFIDENCE_WEIGHTS[key], float), (
            f"{key!r} is not a float"
        )


# ===========================================================================
# test_family_confidence_is_max_over_contributors
# ===========================================================================


def test_family_confidence_is_max_over_contributors() -> None:
    """When multiple DTCs feed one family, the max weight wins."""
    # P0171 → LEAN → lean_condition, P0174 → LEAN → lean_condition
    # One confirmed (1.0) + one pending (0.5) → max = 1.0
    payload = _payload(
        confirmed=["P0171"],
        pending=["P0174"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    assert candidates[0].family == "lean_condition"
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["confirmed"]


def test_family_confidence_monitor_exceeds_dtc() -> None:
    """Mode $06 CRITICAL_FAIL (0.7) wins over PENDING (0.5) for same family."""
    # P0300 → MISFIRE → misfire (pending = 0.5), monitor CRITICAL_FAIL = 0.7
    payload = _payload(
        pending=["P0300"],
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
        monitors={"MID_A1_TID_01": _monitor(Mode06MonitorState.CRITICAL_FAIL)},
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 1
    assert candidates[0].family == "misfire"
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["mode06_critical_fail"]
    assert candidates[0].match_type == MatchType.MONITOR_WEAK


# ===========================================================================
# test_dna_gate_degrades_not_inflates
# ===========================================================================


def test_dna_gate_high_full_confidence() -> None:
    """HIGH DNA confidence on catalyst → full weight (no degradation)."""
    payload = _payload(
        confirmed=["P0420"],  # → CATALYST_HISTORY → catalyst_failure
        routing_tags=[DTCRoutingTag.CATALYST_HISTORY],
    )
    dna = _dna_view(confidence=VinConfidence.HIGH)
    candidates = rank_candidates(payload, dna_view=dna)
    assert len(candidates) == 1
    assert candidates[0].family == "catalyst_failure"
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["confirmed"]  # 1.0 × 1.0


def test_dna_gate_partial_degraded() -> None:
    """PARTIAL DNA confidence on catalyst → degraded confidence (never higher)."""
    payload = _payload(
        confirmed=["P0420"],
        routing_tags=[DTCRoutingTag.CATALYST_HISTORY],
    )
    dna = _dna_view(confidence=VinConfidence.PARTIAL)
    candidates = rank_candidates(payload, dna_view=dna)
    assert len(candidates) == 1
    assert candidates[0].family == "catalyst_failure"
    # degraded: 1.0 × 0.7 = 0.7
    assert candidates[0].raw_confidence < DTC_CONFIDENCE_WEIGHTS["confirmed"]
    assert candidates[0].raw_confidence > 0.0


def test_dna_gate_none_degraded() -> None:
    """NONE DNA confidence on catalyst → further degraded (never higher)."""
    payload = _payload(
        confirmed=["P0420"],
        routing_tags=[DTCRoutingTag.CATALYST_HISTORY],
    )
    dna = _dna_view(confidence=VinConfidence.NONE)
    candidates = rank_candidates(payload, dna_view=dna)
    assert len(candidates) == 1
    # degraded: 1.0 × 0.5 = 0.5
    assert candidates[0].raw_confidence < DTC_CONFIDENCE_WEIGHTS["confirmed"]


def test_dna_gate_none_vs_partial_ordering() -> None:
    """NONE degrades more than PARTIAL (ordered degradation)."""
    payload = _payload(
        confirmed=["P0420"],
        routing_tags=[DTCRoutingTag.CATALYST_HISTORY],
    )
    dna_partial = _dna_view(confidence=VinConfidence.PARTIAL)
    dna_none = _dna_view(confidence=VinConfidence.NONE)
    c_partial = rank_candidates(payload, dna_view=dna_partial)[0]
    c_none = rank_candidates(payload, dna_view=dna_none)[0]
    assert c_none.raw_confidence < c_partial.raw_confidence, (
        f"NONE ({c_none.raw_confidence}) should be < PARTIAL ({c_partial.raw_confidence})"
    )


def test_dna_gate_never_inflates() -> None:
    """DNA gate never increases confidence above the ungated baseline."""
    # Ungated family should have the same confidence regardless of dna_view
    payload = _payload(
        confirmed=["P0171"],  # LEAN → lean_condition (no DNA gate)
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    no_dna = rank_candidates(payload, dna_view=None)[0]
    high_dna = rank_candidates(payload, dna_view=_dna_view(confidence=VinConfidence.HIGH))[0]
    partial_dna = rank_candidates(payload, dna_view=_dna_view(confidence=VinConfidence.PARTIAL))[0]
    # Ungated family — all should be same
    assert no_dna.raw_confidence == high_dna.raw_confidence == partial_dna.raw_confidence


def test_dna_none_view_pure_dtc_pattern() -> None:
    """None dna_view is equivalent to NONE confidence for a DNA-gated family."""
    payload = _payload(
        confirmed=["P0420"],
        routing_tags=[DTCRoutingTag.CATALYST_HISTORY],
    )
    no_view = rank_candidates(payload, dna_view=None)[0]
    none_view = rank_candidates(payload, dna_view=_dna_view(confidence=VinConfidence.NONE))[0]
    assert no_view.raw_confidence == none_view.raw_confidence


# ===========================================================================
# test_match_type_is_dtc_state
# ===========================================================================


def test_match_type_definitive_from_confirmed() -> None:
    """CONFIRMED DTC → DEFINITIVE MatchType."""
    payload = _payload(
        confirmed=["P0300"],
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert candidates[0].match_type == MatchType.DEFINITIVE


def test_match_type_definitive_from_permanent() -> None:
    """PERMANENT DTC → DEFINITIVE MatchType."""
    payload = _payload(
        permanent=["P0300"],
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert candidates[0].match_type == MatchType.DEFINITIVE


def test_match_type_indicative_from_pending() -> None:
    """PENDING DTC → INDICATIVE MatchType."""
    payload = _payload(
        pending=["P0300"],
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert candidates[0].match_type == MatchType.INDICATIVE


def test_match_type_monitor_weak_from_critical_fail() -> None:
    """Mode $06 CRITICAL_FAIL → MONITOR_WEAK when no DTC evidence."""
    payload = _payload(
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
        monitors={"MID_A1_TID_01": _monitor(Mode06MonitorState.CRITICAL_FAIL)},
    )
    candidates = rank_candidates(payload)
    assert candidates[0].match_type == MatchType.MONITOR_WEAK


def test_match_type_monitor_pass() -> None:
    """Mode $06 PASSED → MONITOR_PASS when no other evidence."""
    payload = _payload(
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
        monitors={"MID_A1_TID_01": _monitor(Mode06MonitorState.PASSED)},
    )
    candidates = rank_candidates(payload)
    assert candidates[0].match_type == MatchType.MONITOR_PASS


# ===========================================================================
# test_monotone
# ===========================================================================


def test_monotone_stronger_state_never_lowers() -> None:
    """Adding a CONFIRMED DTC to a family with only PENDING never lowers confidence."""
    # Baseline: only pending
    payload_pending = _payload(
        pending=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    baseline = rank_candidates(payload_pending)[0].raw_confidence

    # Now add confirmed DTC for same family
    payload_both = _payload(
        confirmed=["P0174"],  # also LEAN → lean_condition
        pending=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    combined = rank_candidates(payload_both)[0].raw_confidence
    assert combined >= baseline, (
        f"Confirmed+Pending ({combined}) should be >= Pending alone ({baseline})"
    )
    assert combined == DTC_CONFIDENCE_WEIGHTS["confirmed"]


def test_monotone_add_monitor_never_lowers() -> None:
    """Adding a CRITICAL_FAIL monitor never lowers a PENDING-only family."""
    payload_pending = _payload(
        pending=["P0300"],
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
    )
    baseline = rank_candidates(payload_pending)[0].raw_confidence

    payload_with_monitor = _payload(
        pending=["P0300"],
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY],
        monitors={"MID_A1_TID_01": _monitor(Mode06MonitorState.CRITICAL_FAIL)},
    )
    combined = rank_candidates(payload_with_monitor)[0].raw_confidence
    assert combined >= baseline, (
        f"Pending+Monitor ({combined}) should be >= Pending alone ({baseline})"
    )


# ===========================================================================
# test_no_poa_candidate
# ===========================================================================


def test_no_poa_candidate() -> None:
    """POA_HISTORY in routing_tags produces no candidate."""
    payload = _payload(
        confirmed=["P0420"],
        routing_tags=[DTCRoutingTag.POA_HISTORY, DTCRoutingTag.CATALYST_HISTORY],
    )
    candidates = rank_candidates(payload)
    families = {c.family for c in candidates}
    # POA_HISTORY maps to None in family_map → never produces a candidate
    assert "catalyst_failure" in families
    # POA should never appear
    for c in candidates:
        assert c.family != "poa_signature", "POA must not produce a candidate"


def test_no_poa_candidate_no_other_tags() -> None:
    """Only POA_HISTORY → empty result."""
    payload = _payload(
        routing_tags=[DTCRoutingTag.POA_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert candidates == []


# ===========================================================================
# test_multiple_families_sorting
# ===========================================================================


def test_multiple_families_sorted_by_confidence() -> None:
    """Candidates are sorted descending by raw_confidence, then family name."""
    payload = _payload(
        confirmed=["P0171"],   # LEAN → lean_condition (1.0)
        pending=["P0300"],     # MISFIRE → misfire (0.5)
        routing_tags=[DTCRoutingTag.LEAN_HISTORY, DTCRoutingTag.MISFIRE_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert len(candidates) == 2
    assert candidates[0].family == "lean_condition"
    assert candidates[0].raw_confidence == DTC_CONFIDENCE_WEIGHTS["confirmed"]
    assert candidates[1].family == "misfire"
    assert candidates[1].raw_confidence == DTC_CONFIDENCE_WEIGHTS["pending"]


def test_empty_payload() -> None:
    """No routing tags → empty list."""
    payload = _payload()
    candidates = rank_candidates(payload)
    assert candidates == []


# ===========================================================================
# test_rank_candidates_returns_candidatescore
# ===========================================================================


def test_rank_candidates_returns_candidatescore_instances() -> None:
    """Every returned element is a CandidateScore with expected fields."""
    payload = _payload(
        confirmed=["P0171"],
        routing_tags=[DTCRoutingTag.LEAN_HISTORY],
    )
    candidates = rank_candidates(payload)
    for c in candidates:
        assert isinstance(c, CandidateScore)
        assert isinstance(c.family, str)
        assert isinstance(c.raw_confidence, float)
        assert isinstance(c.match_type, MatchType)
        assert 0.0 <= c.raw_confidence <= 1.0


def test_context_only_tags_excluded() -> None:
    """Context-only tags (EGR, EVAP, THERMAL, etc.) produce no candidates."""
    payload = _payload(
        confirmed=["P0400"],  # → EGR_HISTORY → None (context-only)
        routing_tags=[DTCRoutingTag.EGR_HISTORY],
    )
    candidates = rank_candidates(payload)
    assert candidates == []
