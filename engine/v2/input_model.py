"""Input model dataclasses for the 4D Petrol Diagnostic Engine V2.

Defines the unified input contract (DiagnosticInput) and the post-validation
wrapper (ValidatedInput) that all downstream modules consume.  Closes V1
lessons L17 (UI fields derived from DiagnosticInput) and L04 (no module reads
raw DiagnosticInput).

Source: v2-validation-layer §2 data contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# ── vehicle context ────────────────────────────────────────────────────────

@dataclass(slots=True)
class VehicleContext:
    """Vehicle identification for M0 tech-mask / era-mask lookup in vref.db.

    my (model year) must be in [1990, 2020]; values outside this range are
    rejected by VL category 1 (range check).
    vin: 17-character VIN string (optional). Validated by VL category 12
    (format + ISO 3779 checksum). When present and valid, M0 resolves it
    via engine.v2.vin.resolve() to auto-fill engine_code, displacement_cc,
    and induction before vref.db lookup.
    """
    brand: str
    model: str
    engine_code: str
    displacement_cc: int
    my: int
    vin: str | None = None


# ── gas records ────────────────────────────────────────────────────────────

@dataclass(slots=True)
class GasRecord:
    """Single exhaust-gas sample from a 4-gas or 5-gas analyser.

    All percentages are volumetric (%, v/v).  nox_ppm and lambda_analyser may
    be None on 4-gas analysers (nox_suppressed path, VL category 11).
    """
    co_pct: float
    hc_ppm: float
    co2_pct: float
    o2_pct: float
    nox_ppm: float | None = None
    lambda_analyser: float | None = None


# ── OBD live data ──────────────────────────────────────────────────────────

@dataclass(slots=True)
class OBDRecord:
    """OBD-II Mode 1 live-data PIDs captured at diagnosis time.

    All fields are optional — a vehicle may report only a subset of PIDs.
    stft/ltft values are percentages (negative = fuel removal).
    """
    stft_b1: float | None = None
    stft_b2: float | None = None
    ltft_b1: float | None = None
    ltft_b2: float | None = None
    map_kpa: float | None = None
    maf_gs: float | None = None
    rpm: int | None = None
    ect_c: float | None = None
    iat_c: float | None = None
    fuel_status: str | None = None
    o2_voltage_b1: float | None = None
    o2_voltage_b2: float | None = None
    obd_lambda: float | None = None
    vvt_angle: float | None = None
    fuel_pressure_kpa: float | None = None
    baro_kpa: float | None = None
    evap_purge_pct: float | None = None
    load_pct: float | None = None
    tps_pct: float | None = None


# ── freeze frame ───────────────────────────────────────────────────────────

@dataclass(slots=True)
class FreezeFrameRecord:
    """Freeze frame data captured at the moment a DTC was set (SAE J1979).

    19 fields matching the V2 freeze frame master guide specification.
    """
    dtc_trigger: str = ""
    ect_c: float | None = None
    rpm: int | None = None
    load_pct: float | None = None
    map_kpa: float | None = None
    maf_gs: float | None = None
    stft_b1: float | None = None
    stft_b2: float | None = None
    ltft_b1: float | None = None
    ltft_b2: float | None = None
    speed_kph: int | None = None
    iat_c: float | None = None
    fuel_status: str | None = None
    o2_voltage_b1: float | None = None
    o2_voltage_b2: float | None = None
    baro_kpa: float | None = None
    tps_pct: float | None = None
    evap_purge_pct: float | None = None
    runtime_s: int | None = None


# ── validation ─────────────────────────────────────────────────────────────

@dataclass(slots=True)
class ValidationWarning:
    """A non-rejection flag raised by VL soft-mode categories (6, 8b).

    category: VL category number (int).
    message:  human-readable description of the concern.
    channel:  the input channel the warning applies to (e.g. "obd", "gas_idle").
    """
    category: int
    message: str
    channel: str


# ── top-level input contracts ──────────────────────────────────────────────

@dataclass
class DiagnosticInput:
    """Unified input container — the single entry point for all 4 pathways.

    Closes L17: every UI field must derive from this dataclass; no
    independently-defined fields.  Downstream modules never consume this
    directly — VL transforms it into ValidatedInput first (R4/L04).
    """
    vehicle_context: VehicleContext
    dtcs: list[str]
    analyser_type: Literal["4-gas", "5-gas"]
    gas_idle: GasRecord | None = None
    gas_high: GasRecord | None = None
    obd: OBDRecord | None = None
    freeze_frame: FreezeFrameRecord | None = None


@dataclass
class ValidatedInput:
    """Post-VL wrapper — the only input form that modules M0–M5 may read.

    R4 / L04: no module downstream of VL reads raw DiagnosticInput.
    Pipeline routers (restricted_cold_start, open_loop_suppression,
    nox_suppressed) drive path selection in M0/M1/M2.
    """
    raw: DiagnosticInput
    valid_channels: set[str] = field(default_factory=set)
    invalid_channels: dict[str, str] = field(default_factory=dict)
    warnings: list[ValidationWarning] = field(default_factory=list)
    restricted_cold_start: bool = False
    open_loop_suppression: bool = False
    nox_suppressed: bool = False


# ── signal extraction helpers ────────────────────────────────────────────────


def extract_ect(obd: OBDRecord | None, ff: FreezeFrameRecord | None) -> float | None:
    """Extract ECT from OBD (priority) or freeze frame (fallback).

    OBD live data takes priority over freeze frame when both are available,
    as live data reflects current engine state while freeze frame is a
    snapshot captured at DTC-set time.
    """
    if obd is not None and obd.ect_c is not None:
        return obd.ect_c
    if ff is not None and ff.ect_c is not None:
        return ff.ect_c
    return None


def extract_rpm(obd: OBDRecord | None, ff: FreezeFrameRecord | None) -> int | None:
    """Extract RPM from OBD (priority) or freeze frame (fallback)."""
    if obd is not None and obd.rpm is not None:
        return obd.rpm
    if ff is not None and ff.rpm is not None:
        return ff.rpm
    return None


def extract_fuel_status(
    obd: OBDRecord | None, ff: FreezeFrameRecord | None
) -> str | None:
    """Extract fuel_status from OBD (priority) or freeze frame (fallback)."""
    if obd is not None and obd.fuel_status is not None:
        return obd.fuel_status
    if ff is not None and ff.fuel_status is not None:
        return ff.fuel_status
    return None
