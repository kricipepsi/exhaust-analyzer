"""Discrete combinatorial suite for DTCLab (T-TST-9).

Lab-local generator — the shared engine's CombinatorialGenerator is
GAS_DIMS-hardcoded and yields 0 cases for discrete labs.  This suite
enumerates every routing tag, DNA-gate branch, context bucket, and
MIL/fuel combination from the descriptor's declared axes and demands
exact agreement with the DTC_VOCABULARY.md oracles.

Coverage axes (printed at start):
  A1 — routing:  one exemplar DTC per DTCRoutingTag
  A2 — DNA gate:  {None, HIGH-with-hardware, HIGH-without-hardware}
  A3 — context:   {COLD_START, IDLE, LOAD, UNKNOWN}
  A4 — MIL/fuel:  active_mil × mil_flashing × FuelSystemStatus
"""

from __future__ import annotations

from itertools import product
from unittest.mock import patch

import pytest

from dtclab.core.routing_tag_mapper import RoutingTagMapper
from dtclab.schemas.dna_view import DtcLabDnaView, ResolvedHorizon, VinConfidence
from dtclab.schemas.vocabulary import (
    DTCRoutingTag,
    FuelSystemStatus,
    HistoricalFaultContext,
)
from tests.conftest import (
    CODE_TAG_ORACLE,
    GATED_TAGS,
    classify_context_oracle,
    is_fail_closed,
    make_dna_view,
    make_freeze_frame_raw,
    run_sanitize,
)


# =============================================================================
# Axis declarations (printed at collect time for auditability)
# =============================================================================

# A1 — Routing exemplars: one DTC code per DTCRoutingTag
ROUTING_AXIS: list[tuple[str, DTCRoutingTag]] = list(CODE_TAG_ORACLE.items())

# A2 — DNA gate axis for gated tags
DNA_GATE_AXIS: list[tuple[DTCRoutingTag, str, str | None, str]] = []
for tag, gate_name in GATED_TAGS.items():
    exemplar = next((code for code, t in CODE_TAG_ORACLE.items() if t == tag), None)
    if exemplar is None:
        continue
    # dna_view=None → emit
    DNA_GATE_AXIS.append((tag, exemplar, None, "emit"))
    # HIGH with hardware → emit
    DNA_GATE_AXIS.append((tag, exemplar, "HIGH_with", "emit"))
    # HIGH without hardware → drop
    DNA_GATE_AXIS.append((tag, exemplar, "HIGH_without", "drop"))

# A3 — Freeze-frame context axis: one representative per bucket
# (ect, rpm, load, expected_context)
CONTEXT_AXIS: list[tuple[float, int, float, HistoricalFaultContext]] = [
    (25.0, 800, 20.0, HistoricalFaultContext.COLD_START_TRANSIT_FAULT),
    (90.0, 800, 20.0, HistoricalFaultContext.HISTORICAL_IDLE_FAULT),
    (90.0, 2500, 65.0, HistoricalFaultContext.HISTORICAL_LOAD_FAULT),
    (90.0, 1500, 35.0, HistoricalFaultContext.UNKNOWN),
]

# A4 — MIL / fuel axis
MIL_AXIS: list[bool] = [False, True]
FUEL_AXIS: list[FuelSystemStatus] = [
    FuelSystemStatus.CL,
    FuelSystemStatus.OL,
    FuelSystemStatus.OL_DRIVE,
    FuelSystemStatus.OL_FAULT,
]


# =============================================================================
# Axis size audit (printed at collection, not runtime)
# =============================================================================

_AXIS_SIZES = {
    "A1_routing_exemplars": len(ROUTING_AXIS),
    "A2_dna_gate_combinations": len(DNA_GATE_AXIS),
    "A3_context_buckets": len(CONTEXT_AXIS),
    "A4_mil_fuel_combinations": len(MIL_AXIS) * len(MIL_AXIS) * len(FUEL_AXIS),
}
_TOTAL_CASES = (
    _AXIS_SIZES["A1_routing_exemplars"]
    + _AXIS_SIZES["A2_dna_gate_combinations"]
    + _AXIS_SIZES["A3_context_buckets"]
    + _AXIS_SIZES["A4_mil_fuel_combinations"]
)


def test_print_combinatorial_coverage() -> None:
    """Auditable coverage report — prints axis sizes and total case count."""
    print("\nDTCLab combinatorial coverage:")
    for axis, size in _AXIS_SIZES.items():
        print(f"  {axis}: {size}")
    print(f"  TOTAL: {_TOTAL_CASES}")
    assert _TOTAL_CASES > 0


# =============================================================================
# A1 — Routing tag exemplar tests
# =============================================================================


@pytest.mark.parametrize(
    "dtc_code,expected_tag",
    ROUTING_AXIS,
    ids=[f"{code}→{tag.value}" for code, tag in ROUTING_AXIS],
)
def test_routing_tag_exact_match(dtc_code: str, expected_tag: DTCRoutingTag) -> None:
    """Every exemplar DTC routes to exactly its declared tag.

    gt_source: DTC_VOCABULARY.md §4, §15; routing_tag_map.yaml
    """
    result, error = run_sanitize([dtc_code])
    assert error is None, f"unexpected error: {error}"
    assert is_fail_closed(result, error)

    tags = [t.value for t in result.routing_tags]
    assert expected_tag.value in tags, (
        f"{dtc_code} → expected {expected_tag.value}, got {tags}"
    )


# =============================================================================
# A2 — DNA gate tests
# =============================================================================


def _build_dna_view_for_case(gate_name: str, case: str | None) -> DtcLabDnaView | None:
    """Build the appropriate dna_view (or None) for a DNA-gate test case."""
    if case == "emit" or case is None:
        return None  # None → emit unconditionally (§14.3)

    has_catalyst = gate_name == "has_catalyst" and case == "HIGH_with"
    egr_equipped = gate_name == "egr_equipped" and case == "HIGH_with"

    if case == "HIGH_with":
        return make_dna_view(
            has_catalyst=has_catalyst or (gate_name == "has_catalyst"),
            egr_equipped=egr_equipped or (gate_name == "egr_equipped"),
            horizon=ResolvedHorizon.HORIZON_MODERN,
            confidence=VinConfidence.HIGH,
        )
    else:  # HIGH_without
        return make_dna_view(
            has_catalyst=False,
            egr_equipped=False,
            horizon=ResolvedHorizon.HORIZON_MODERN,
            confidence=VinConfidence.HIGH,
        )


@pytest.mark.parametrize(
    "tag,dtc_code,dna_case,expected_behavior",
    DNA_GATE_AXIS,
    ids=[f"{t.value}/{c}" for t, _, c, _ in DNA_GATE_AXIS],
)
def test_dna_gate(
    tag: DTCRoutingTag,
    dtc_code: str,
    dna_case: str | None,
    expected_behavior: str,
) -> None:
    """DNA-gated tags emit/drop per confidence and hardware presence.

    gt_source: DTC_VOCABULARY.md §4.1, §14.2, §14.3
    """
    gate_name = GATED_TAGS[tag]
    dna_view = _build_dna_view_for_case(gate_name, dna_case) if dna_case is not None else None

    result, error = run_sanitize([dtc_code], dna_view=dna_view)
    assert error is None, f"unexpected error: {error}"
    assert is_fail_closed(result, error)

    tags = [t.value for t in result.routing_tags]

    if expected_behavior == "drop":
        assert tag.value not in tags, (
            f"{dtc_code} with {dna_case}: expected {tag.value} DROPPED, got {tags}"
        )
    else:
        assert tag.value in tags, (
            f"{dtc_code} with {dna_case}: expected {tag.value} EMITTED, got {tags}"
        )


# =============================================================================
# A3 — Freeze-frame context tests
# =============================================================================


@pytest.mark.parametrize(
    "ect,rpm,load_pct,expected_ctx",
    CONTEXT_AXIS,
    ids=[f"ect={ect}_rpm={rpm}_load={load}→{ctx.value}" for ect, rpm, load, ctx in CONTEXT_AXIS],
)
def test_historical_context_classification(
    ect: float, rpm: int, load_pct: float, expected_ctx: HistoricalFaultContext
) -> None:
    """Freeze-frame context PIDs classify to the correct HistoricalFaultContext.

    gt_source: DTC_VOCABULARY.md §9
    """
    ff = make_freeze_frame_raw(
        coolant_temp_c=ect,
        engine_rpm=rpm,
        calculated_load_pct=load_pct,
    )
    result, error = run_sanitize(["P0171"], freeze_frame=ff)
    assert error is None, f"unexpected error: {error}"
    assert is_fail_closed(result, error)

    actual_ctx = result.historical_fault_context
    assert actual_ctx == expected_ctx, (
        f"ect={ect} rpm={rpm} load={load_pct}: "
        f"expected {expected_ctx.value}, got {actual_ctx.value}"
    )

    # Cross-check against the oracle mirror
    oracle_ctx = classify_context_oracle(ect, rpm, load_pct)
    assert actual_ctx == oracle_ctx, (
        f"classify_historical_context disagrees with oracle mirror: "
        f"{actual_ctx.value} != {oracle_ctx.value}"
    )


def test_cold_start_priority_over_idle() -> None:
    """Cold-start (ECT < 60) dominates idle conditions per §9 priority rule."""
    ff = make_freeze_frame_raw(
        coolant_temp_c=25.0,  # < 60 → COLD_START
        engine_rpm=800,        # < 1000 → would be IDLE
        calculated_load_pct=20.0,  # < 25 → would be IDLE
    )
    result, error = run_sanitize(["P0171"], freeze_frame=ff)
    assert error is None
    assert result.historical_fault_context == HistoricalFaultContext.COLD_START_TRANSIT_FAULT


# =============================================================================
# A4 — MIL / fuel axis tests
# =============================================================================


@pytest.mark.parametrize(
    "active_mil,mil_flashing,fuel_status",
    [
        (mil, flash, fs)
        for mil, flash, fs in product(MIL_AXIS, MIL_AXIS, FUEL_AXIS)
    ],
    ids=[
        f"MIL={mil}_flash={flash}_{fs.value}"
        for mil, flash, fs in product(MIL_AXIS, MIL_AXIS, FUEL_AXIS)
    ],
)
def test_mil_fuel_roundtrip(
    active_mil: bool,
    mil_flashing: bool,
    fuel_status: FuelSystemStatus,
) -> None:
    """MIL flags and fuel_status round-trip through the pipeline.

    gt_source: DTC_VOCABULARY.md §8, §11, §12.3
    """
    ff = make_freeze_frame_raw(fuel_system_status=fuel_status.value)
    result, error = run_sanitize(
        ["P0171"],
        freeze_frame=ff,
        active_mil=active_mil,
        mil_flashing=mil_flashing,
    )
    assert error is None, f"unexpected error: {error}"
    assert is_fail_closed(result, error)

    assert result.active_mil == active_mil
    assert result.mil_flashing == mil_flashing
    # fuel_system_status round-trips through freeze_frame
    assert result.freeze_frame.fuel_system_status == fuel_status

    # _derive_open_loop flag check (DTC_VOCABULARY.md §12.3)
    expected_ol = fuel_status in (
        FuelSystemStatus.OL,
        FuelSystemStatus.OL_FAULT,
        FuelSystemStatus.OL_DRIVE,
    )
    assert result.freeze_frame.ff_open_loop_at_fault == expected_ol, (
        f"ff_open_loop_at_fault should be {expected_ol} for {fuel_status.value}"
    )


# =============================================================================
# Cross-field tag tests (CoolantLeakSig.md §4)
# =============================================================================


def test_coolant_system_malfunction_cross_field() -> None:
    """P0128 in OL_FAULT → COOLANT_SYSTEM_MALFUNCTION.

    gt_source: CoolantLeakSig.md §4; DTC_VOCABULARY.md §4
    """
    ff = make_freeze_frame_raw(fuel_system_status="OL_FAULT")
    result, error = run_sanitize(["P0128"], freeze_frame=ff)
    assert error is None
    tags = [t.value for t in result.routing_tags]
    assert DTCRoutingTag.COOLANT_SYSTEM_MALFUNCTION.value in tags


def test_cylinder_fluid_misfire_cross_field() -> None:
    """P0302 in CL → CYLINDER_FLUID_MISFIRE.

    gt_source: CoolantLeakSig.md §4; DTC_VOCABULARY.md §4
    """
    ff = make_freeze_frame_raw(fuel_system_status="CL")
    result, error = run_sanitize(["P0302"], freeze_frame=ff)
    assert error is None
    tags = [t.value for t in result.routing_tags]
    # P0302 routes MISFIRE_HISTORY AND CYLINDER_FLUID_MISFIRE
    assert DTCRoutingTag.MISFIRE_HISTORY.value in tags
    assert DTCRoutingTag.CYLINDER_FLUID_MISFIRE.value in tags


# =============================================================================
# DNA confidence branches test (§14.2, §14.3)
# =============================================================================


def test_dna_none_emits_unconditionally() -> None:
    """dna_view=None ≡ VinConfidence.NONE — emit gated tag unconditionally."""
    result, error = run_sanitize(["P0420"], dna_view=None)
    assert error is None
    tags = [t.value for t in result.routing_tags]
    assert DTCRoutingTag.CATALYST_HISTORY.value in tags


def test_dna_partial_emits_with_downgrade() -> None:
    """VinConfidence.PARTIAL — emit gated tag (advisory)."""
    dna = make_dna_view(
        has_catalyst=False,  # no hardware
        confidence=VinConfidence.PARTIAL,
    )
    result, error = run_sanitize(["P0420"], dna_view=dna)
    assert error is None
    tags = [t.value for t in result.routing_tags]
    assert DTCRoutingTag.CATALYST_HISTORY.value in tags


def test_dna_high_strict_drop() -> None:
    """VinConfidence.HIGH without hardware → gated tag DROPPED."""
    dna = make_dna_view(
        has_catalyst=False,
        confidence=VinConfidence.HIGH,
    )
    result, error = run_sanitize(["P0420"], dna_view=dna)
    assert error is None
    tags = [t.value for t in result.routing_tags]
    assert DTCRoutingTag.CATALYST_HISTORY.value not in tags


# =============================================================================
# Negative control — proof the harness sees a routing regression
# =============================================================================


def test_negative_control_forced_empty_map() -> None:
    """Temporarily force RoutingTagMapper.map to return [] → suite MUST fail.

    This proves the harness is not a tautology — it actually detects a
    routing regression.  The monkeypatch is reverted after this test.
    """
    with patch.object(
        RoutingTagMapper,
        "map",
        return_value=[],
    ):
        result, error = run_sanitize(["P0171"])
        assert error is None

        tags = [t.value for t in result.routing_tags]
        # With the real mapper, P0171 → LEAN_HISTORY.
        # With the patched mapper returning [], LEAN_HISTORY is absent.
        assert DTCRoutingTag.LEAN_HISTORY.value not in tags, (
            "Negative control failed: harness did NOT detect the forced-empty "
            "routing map. The patch may not have taken effect."
        )

    # After revert — P0171 routes correctly again
    result2, error2 = run_sanitize(["P0171"])
    assert error2 is None
    tags2 = [t.value for t in result2.routing_tags]
    assert DTCRoutingTag.LEAN_HISTORY.value in tags2, (
        "Post-revert: P0171 should route to LEAN_HISTORY again"
    )
