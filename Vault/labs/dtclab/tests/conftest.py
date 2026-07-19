"""Pytest configuration and shared fixtures for dtclab tests.

Shared oracle helpers live here (single source of truth) so both
combinatorial and fuzz suites import the same code→tag map, context
classifier mirror, and fail-closed predicate.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Any

import pytest

# Add the shared harness engine to sys.path so per-lab descriptors can
# import from harness.descriptor (PROJECTION_CONTRACT §2).
_HARNESS_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "harness"
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

from dtclab.core.data_fusion_sanitizer import DataFusionSanitizer  # noqa: E402
from dtclab.schemas.dna_view import (  # noqa: E402
    AirMeteringStrategy,
    DtcEmissionsView,
    DtcLabDnaView,
    EuroEmissionCategory,
    ResolvedHorizon,
    VinConfidence,
)
from dtclab.schemas.vocabulary import (  # noqa: E402
    DTC_REGEX,
    DTCRoutingTag,
    FuelSystemStatus,
    HistoricalFaultContext,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
_CSV_PATH = _FIXTURES_DIR / "dtclab_cases.csv"

_COMPILED_DTC_REGEX = re.compile(DTC_REGEX)


# ---------------------------------------------------------------------------
# DTC parsing (T-TST-7 split-on-comma rule; also handles pipe from master)
# ---------------------------------------------------------------------------

def parse_dtc_cell(raw: str) -> list[str]:
    """Split a DTC cell on comma or pipe, strip whitespace, drop empties."""
    if not raw or not raw.strip():
        return []
    tokens = re.split(r"[,\|]", raw)
    return [t.strip() for t in tokens if t.strip()]


# ---------------------------------------------------------------------------
# fuel_status mapping (master CSV display names → enum values)
# ---------------------------------------------------------------------------

_FUEL_STATUS_MAP: dict[str, FuelSystemStatus] = {
    "Closed_Loop": FuelSystemStatus.CL,
    "Open_Loop": FuelSystemStatus.OL,
    "Open_Loop_Drive": FuelSystemStatus.OL_DRIVE,
    "Open_Loop_Fault": FuelSystemStatus.OL_FAULT,
    "CL": FuelSystemStatus.CL,
    "OL": FuelSystemStatus.OL,
    "OL_DRIVE": FuelSystemStatus.OL_DRIVE,
    "OL_FAULT": FuelSystemStatus.OL_FAULT,
}


def map_fuel_status(raw: str) -> FuelSystemStatus | None:
    """Map a CSV fuel_status value to the enum; None if empty/unrecognised."""
    if not raw or not raw.strip():
        return None
    return _FUEL_STATUS_MAP.get(raw.strip())


# ---------------------------------------------------------------------------
# Code → Routing-Tag Oracle Map (DTC_VOCABULARY.md §4, §15)
#
# One exemplar DTC per DTCRoutingTag. Each entry cites its wiki section.
# The combinatorial suite asserts exact agreement against this map.
# ---------------------------------------------------------------------------

CODE_TAG_ORACLE: dict[str, DTCRoutingTag] = {
    # wiki: DTC_VOCABULARY.md §4, §15
    "P0171": DTCRoutingTag.LEAN_HISTORY,
    "P0174": DTCRoutingTag.LEAN_HISTORY,
    "P0172": DTCRoutingTag.RICH_HISTORY,
    "P0175": DTCRoutingTag.RICH_HISTORY,
    "P0300": DTCRoutingTag.MISFIRE_HISTORY,
    "P0301": DTCRoutingTag.MISFIRE_HISTORY,
    "P0302": DTCRoutingTag.MISFIRE_HISTORY,
    "P0420": DTCRoutingTag.CATALYST_HISTORY,  # DNA-gated: has_catalyst
    "P0430": DTCRoutingTag.CATALYST_HISTORY,  # DNA-gated: has_catalyst
    "P0401": DTCRoutingTag.EGR_HISTORY,       # DNA-gated: egr_equipped
    "P0131": DTCRoutingTag.O2_HISTORY,
    "P0151": DTCRoutingTag.O2_HISTORY,
    "P0201": DTCRoutingTag.INJECTOR_HISTORY,
    "P0011": DTCRoutingTag.VVT_HISTORY,
    "P0441": DTCRoutingTag.EVAP_HISTORY,
    "P0116": DTCRoutingTag.THERMAL_HISTORY,
    "P0606": DTCRoutingTag.ECU_INTERNAL_HISTORY,
    "P0507": DTCRoutingTag.IDLE_CONTROL_HISTORY,
    "P0234": DTCRoutingTag.BOOST_HISTORY,
    "P0299": DTCRoutingTag.BOOST_HISTORY,
    "P0325": DTCRoutingTag.KNOCK_HISTORY,
    # Cross-field tags (DTC_VOCABULARY.md §4, CoolantLeakSig.md §4) —
    # these require specific fuel_status context and are tested separately.
    # P0128/P0117 route THERMAL_HISTORY from the base table;
    # COOLANT_SYSTEM_MALFUNCTION is added by evaluate_coolant_dtc_context
    # only when fuel_status == OL_FAULT.
    # P030x routes MISFIRE_HISTORY; CYLINDER_FLUID_MISFIRE is added
    # by evaluate_coolant_dtc_context only when fuel_status == CL.
}

# DNA-gated tags and their gate names (DTC_VOCABULARY.md §4.1)
GATED_TAGS: dict[DTCRoutingTag, str] = {
    DTCRoutingTag.CATALYST_HISTORY: "has_catalyst",
    DTCRoutingTag.EGR_HISTORY: "egr_equipped",
}


# ---------------------------------------------------------------------------
# Context classifier mirror (DTC_VOCABULARY.md §9)
#
# Exact replica of classify_historical_context for oracle assertions.
# ---------------------------------------------------------------------------

def classify_context_oracle(
    coolant_temp_c: float,
    engine_rpm: int,
    calculated_load_pct: float,
) -> HistoricalFaultContext:
    """Mirror of classify_historical_context per DTC_VOCABULARY.md §9."""
    if coolant_temp_c < 60:  # wiki: §9 — cold-start priority first
        return HistoricalFaultContext.COLD_START_TRANSIT_FAULT
    if engine_rpm < 1000 and calculated_load_pct < 25:  # wiki: §9
        return HistoricalFaultContext.HISTORICAL_IDLE_FAULT
    if engine_rpm > 2000 and calculated_load_pct > 45:  # wiki: §9
        return HistoricalFaultContext.HISTORICAL_LOAD_FAULT
    return HistoricalFaultContext.UNKNOWN


# ---------------------------------------------------------------------------
# Fail-closed predicate (T-TST-9 spec §2 error taxonomy)
# ---------------------------------------------------------------------------

VALID_ERROR_TYPES = (
    type(None),  # no error (valid payload)
)

# Import error types lazily to avoid circular imports at collect time.

def is_fail_closed(result: Any, error: BaseException | None) -> bool:
    """True if the outcome is fail-closed: typed error or schema-valid payload.

    Fail-closed = one of the typed errors from the taxonomy (§2) OR a clean
    validated DTCLabPayload — never an uncaught crash and never a silently
    mis-routed tag.
    """
    from dtclab.core.dtc_ingestion_gate import DTCFormatError
    from dtclab.core.freeze_frame_extractor import FreezeFrameIncompleteError
    from dtclab.schemas.payload import DTCLabPayload

    if error is not None:
        return isinstance(error, (DTCFormatError, FreezeFrameIncompleteError, ValueError))
    return isinstance(result, DTCLabPayload)


# ---------------------------------------------------------------------------
# DNA view builders (for combinatorial DNA-gate axis)
# ---------------------------------------------------------------------------

def make_dna_view(
    *,
    has_catalyst: bool = False,
    egr_equipped: bool = False,
    horizon: ResolvedHorizon = ResolvedHorizon.HORIZON_MODERN,
    confidence: VinConfidence = VinConfidence.HIGH,
) -> DtcLabDnaView:
    """Build a DtcLabDnaView with the given hardware flags."""
    return DtcLabDnaView(
        make="TEST",
        model="TEST",
        model_year=2020,
        euro_emission_category=EuroEmissionCategory.EURO_6,
        air_metering_strategy=AirMeteringStrategy.MAF,
        resolved_horizon=horizon,
        emissions=DtcEmissionsView(
            has_catalyst=has_catalyst,
            egr_equipped=egr_equipped,
        ),
        confidence=confidence,
    )


# ---------------------------------------------------------------------------
# Freeze-frame builder (for combinatorial/fuzz suites)
# ---------------------------------------------------------------------------

def make_freeze_frame_raw(
    *,
    coolant_temp_c: float = 90.0,
    engine_rpm: int = 800,
    calculated_load_pct: float = 20.0,
    manifold_pressure_kpa: float = 100.0,
    short_term_ft1: float = 0.0,
    long_term_ft1: float = 0.0,
    fuel_system_status: str = "CL",
    vehicle_speed_kmh: int = 0,
    ignition_advance_deg: float = 5.0,
    intake_air_temp_c: float = 25.0,
    maf_gps: float = 3.0,
    throttle_pos_pct: float = 15.0,
) -> dict[str, Any]:
    """Build a complete freeze-frame raw dict with all 12 mandatory PIDs."""
    return {
        "coolant_temp_c": coolant_temp_c,
        "engine_rpm": engine_rpm,
        "calculated_load_pct": calculated_load_pct,
        "manifold_pressure_kpa": manifold_pressure_kpa,
        "short_term_ft1": short_term_ft1,
        "long_term_ft1": long_term_ft1,
        "fuel_system_status": fuel_system_status,
        "vehicle_speed_kmh": vehicle_speed_kmh,
        "ignition_advance_deg": ignition_advance_deg,
        "intake_air_temp_c": intake_air_temp_c,
        "maf_gps": maf_gps,
        "throttle_pos_pct": throttle_pos_pct,
    }


# ---------------------------------------------------------------------------
# Sanitize helper (one call, used by combinatorial + fuzz)
# ---------------------------------------------------------------------------

def run_sanitize(
    dtc_codes: list[str],
    freeze_frame: dict[str, Any] | None = None,
    mode06: dict[str, float] | None = None,
    *,
    dna_view: DtcLabDnaView | None = None,
    codes_cleared: bool = False,
    active_mil: bool = False,
    mil_flashing: bool = False,
) -> tuple[Any, BaseException | None]:
    """Run the DTCLab pipeline and return (result, error)."""
    sanitizer = DataFusionSanitizer(dna_view=dna_view)
    raw_dtcs = {"$03": dtc_codes, "$07": [], "$0A": []}
    raw_ff = freeze_frame if freeze_frame is not None else make_freeze_frame_raw()
    raw_m06 = mode06 if mode06 is not None else {}
    try:
        result = sanitizer.sanitize(
            raw_dtcs, raw_ff, raw_m06,
            codes_cleared=codes_cleared,
            active_mil=active_mil,
            mil_flashing=mil_flashing,
        )
        return result, None
    except Exception as exc:
        return None, exc


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def dtclab_csv_path() -> Path:
    """Path to the dtclab_cases.csv fixture (T-TST-7 output)."""
    if not _CSV_PATH.exists():
        pytest.fail(f"dtclab_cases.csv not found at {_CSV_PATH}")
    return _CSV_PATH


@pytest.fixture(scope="session")
def dtclab_csv_rows(dtclab_csv_path: Path) -> list[dict[str, str]]:
    """All 194 rows from dtclab_cases.csv as a list of dicts."""
    rows: list[dict[str, str]] = []
    with dtclab_csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
    return rows
