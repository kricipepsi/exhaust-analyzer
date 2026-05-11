"""M0 — Vehicle DNA profile from vref.db + engine-state FSM.

R6: era-aware KG — M0 is the only module that reads vref.db.
R4 / L04: consumes ValidatedInput, never raw DiagnosticInput.
L15: engine-state FSM is M0's primary output, not a late filter.
L10: vref.db must be populated before M0 tests run.

Source: v2-era-masking §2–§6.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from engine.v2.input_model import ValidatedInput, ValidationWarning

# ── era bucket constants ────────────────────────────────────────────────────
# source: v2-era-masking §2 era buckets

ERA_PRE_OBDII = "ERA_PRE_OBDII"
ERA_OBDII_EARLY = "ERA_OBDII_EARLY"
ERA_CAN = "ERA_CAN"
ERA_MODERN = "ERA_MODERN"

# source: v2-era-masking §2 era bucket reference
_MY_ERA_TABLE: tuple[tuple[int, int, str], ...] = (
    (1990, 1995, ERA_PRE_OBDII),
    (1996, 2005, ERA_OBDII_EARLY),
    (2006, 2015, ERA_CAN),
    (2016, 2020, ERA_MODERN),
)

# ── tech mask flag inventory ────────────────────────────────────────────────
# source: v2-era-masking §3 technology mask flags
_TECH_FLAG_NAMES = (
    "has_vvt",
    "has_gdi",
    "has_turbo",
    "is_v_engine",
    "has_egr",
    "has_secondary_air",
)

# ── fallback defaults (vref.db miss) ────────────────────────────────────────
# source: v2-era-masking §6 fallback rules
_DEFAULT_TARGET_RPM = 2500
_DEFAULT_TARGET_LAMBDA = 1.000

# ── engine-state FSM thresholds ─────────────────────────────────────────────
# source: v2-era-masking §4 engine-state FSM
# source: v2-validation-layer §3 category 9 (ECT < 75 = cold)
_COLD_ECT_THRESHOLD = 75.0

# source: v2-era-masking §6 rule 3 — confidence ceiling when vref.db misses
_VREF_MISS_CEILING = 0.60

# ── output dataclass ────────────────────────────────────────────────────────


@dataclass(slots=True)
class DNAOutput:
    """M0 output — vehicle DNA profile consumed by all downstream modules.

    Closes L10 (vref.db populated before M0 tests) and L15 (engine-state
    FSM is M0's primary output, not a late filter).

    R6: era_bucket masks era-inappropriate fault nodes in M4.
    """
    engine_state: str
    era_bucket: str
    tech_mask: dict[str, bool]
    o2_type: str
    target_rpm_u2: int
    target_lambda_v112: float
    vref_missing: bool
    confidence_ceiling: float
    warnings: list[ValidationWarning] = field(default_factory=list)


# ── public entry point ──────────────────────────────────────────────────────


def load_dna(
    validated_input: ValidatedInput,
    db_path: Path | str | None = None,
) -> DNAOutput:
    """Load vehicle DNA profile from vref.db and compute engine state.

    M0 is the only module allowed to do I/O (vref.db lookup). All other
    modules receive DNAOutput and never query the database directly.

    When a valid VIN is present (VL cat 12 passed), M0 resolves it via
    engine.v2.vin.resolve() to auto-fill engine_code, displacement_cc,
    and induction before vref.db lookup. Manual fields act as fallback.

    Args:
        validated_input: Post-VL input (R4/L04 — never raw DiagnosticInput).
        db_path: Path to vref.db. Defaults to engine/v2/vref.db next to
                 this module.

    Returns:
        DNAOutput with engine_state (FSM), era_bucket, tech_mask flags,
        target_rpm_u2, target_lambda_v112, and any vref-miss warnings.
    """
    ctx = validated_input.raw.vehicle_context
    engine_code = ctx.engine_code
    displacement_cc = ctx.displacement_cc
    my = ctx.my

    db_path = (
        Path(__file__).resolve().parent / "vref.db"
        if db_path is None
        else Path(db_path)
    )

    # ── VIN resolution (before vref.db lookup) ───────────────────────────
    vin = ctx.vin
    vin_dna = None
    # Only block VIN usage on format failures (checksum failures are advisory
    # — many European VINs don't enforce the ISO 3779 check digit).
    vin_blocked = (
        vin is not None
        and any(
            w.category == 12 and "format" in w.message.lower()
            for w in validated_input.warnings
            if w.channel == "vehicle_context"
        )
    )
    if vin and not vin_blocked:
        from engine.v2.vin import resolve as resolve_vin
        vin_dna = resolve_vin(vin)

    warnings: list[ValidationWarning] = []

    if vin_dna is not None and vin_dna.confidence == "high":
        engine_code = vin_dna.engine_code or engine_code
        if vin_dna.displacement_l is not None:
            displacement_cc = int(round(vin_dna.displacement_l * 1000))
    elif vin_dna is not None and vin_dna.confidence == "partial":
        engine_code = vin_dna.engine_code or engine_code

    # ── vref.db lookup ──────────────────────────────────────────────────
    row = _query_vref(db_path, engine_code)

    if row is None:
        era_bucket = _my_to_era(my)
        tech_mask = {flag: False for flag in _TECH_FLAG_NAMES}
        o2_type = "NB"
        target_rpm_u2 = _DEFAULT_TARGET_RPM
        target_lambda_v112 = _DEFAULT_TARGET_LAMBDA
        confidence_ceiling = _VREF_MISS_CEILING
        vref_missing = True
        warnings.append(
            ValidationWarning(
                category=0,
                message=(
                    f"vref.db miss for engine_code={engine_code!r} "
                    f"— era/my defaults applied"
                ),
                channel="vehicle_context",
            )
        )
    else:
        era_bucket = row["era_bucket"]
        tech_mask = {flag: bool(row[flag]) for flag in _TECH_FLAG_NAMES}
        o2_type = row["o2_type"]
        target_rpm_u2 = row["target_rpm_u2"]
        target_lambda_v112 = row["target_lambda_v112"]
        confidence_ceiling = 1.00
        vref_missing = False

    # ── engine-state FSM ─────────────────────────────────────────────────
    engine_state = _compute_engine_state(validated_input)

    return DNAOutput(
        engine_state=engine_state,
        era_bucket=era_bucket,
        tech_mask=tech_mask,
        o2_type=o2_type,
        target_rpm_u2=target_rpm_u2,
        target_lambda_v112=target_lambda_v112,
        vref_missing=vref_missing,
        confidence_ceiling=confidence_ceiling,
        warnings=warnings,
    )


# ── vref.db helpers ─────────────────────────────────────────────────────────


def _query_vref(db_path: Path, engine_code: str) -> dict | None:
    """Look up engine_code in vref.db. Returns row dict or None on miss."""
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM engine_ref WHERE engine_code = ?", (engine_code,)
        )
        row = cursor.fetchone()
        return dict(row) if row is not None else None


def _my_to_era(my: int) -> str:
    """Derive era bucket from model year alone (vref.db miss fallback).

    source: v2-era-masking §2 era buckets
    """
    for start, end, era in _MY_ERA_TABLE:
        if start <= my <= end:
            return era
    return ERA_MODERN


# ── engine-state FSM ────────────────────────────────────────────────────────


def _compute_engine_state(vi: ValidatedInput) -> str:
    """Deterministic lookup of engine_state from ECT, RPM, and fuel_status.

    source: v2-era-masking §4 engine-state FSM table

    States:
      cold_open_loop    — ECT < 75 °C
      warm_cranking     — ECT >= 75 °C, RPM = 0
      warm_closed_loop  — ECT >= 75 °C, RPM > 0, fuel_status CL/CL_FAULT
      warm_open_loop    — ECT >= 75 °C, RPM > 0, fuel_status OL_DRIVE/OL_FAULT
      warm_dfco         — ECT >= 75 °C, RPM > 0, fuel_status OL (decel fuel cut)
    """
    ect = _extract_ect(vi)
    rpm = _extract_rpm(vi)
    fuel_status = _extract_fuel_status(vi)

    # cold open loop — thermal gate applies regardless of other signals
    if ect is not None and ect < _COLD_ECT_THRESHOLD:
        return "cold_open_loop"

    # warm states
    if rpm is not None and rpm == 0:
        return "warm_cranking"

    if fuel_status is not None:
        fuel_upper = fuel_status.upper()
        if fuel_upper in ("OL_DRIVE", "OL_FAULT"):
            return "warm_open_loop"
        if fuel_upper == "OL":
            return "warm_dfco"

    # default: closed loop (or unknown fuel_status with RPM > 0)
    return "warm_closed_loop"


# ── signal extraction helpers ───────────────────────────────────────────────


def _extract_ect(vi: ValidatedInput) -> float | None:
    """Extract ECT from OBD (priority) or freeze frame (fallback)."""
    raw = vi.raw
    if raw.obd is not None and raw.obd.ect_c is not None:
        return raw.obd.ect_c
    if raw.freeze_frame is not None and raw.freeze_frame.ect_c is not None:
        return raw.freeze_frame.ect_c
    return None


def _extract_rpm(vi: ValidatedInput) -> int | None:
    """Extract RPM from OBD (priority) or freeze frame (fallback)."""
    raw = vi.raw
    if raw.obd is not None and raw.obd.rpm is not None:
        return raw.obd.rpm
    if raw.freeze_frame is not None and raw.freeze_frame.rpm is not None:
        return raw.freeze_frame.rpm
    return None


def _extract_fuel_status(vi: ValidatedInput) -> str | None:
    """Extract fuel_status from OBD (priority) or freeze frame (fallback)."""
    raw = vi.raw
    if raw.obd is not None and raw.obd.fuel_status is not None:
        return raw.obd.fuel_status
    if raw.freeze_frame is not None and raw.freeze_frame.fuel_status is not None:
        return raw.freeze_frame.fuel_status
    return None
