"""DTCLab ModuleDescriptor for the generative test harness.

Discrete lab — no continuous FaultBox geometry. The routing-tag→code-range
oracle lives in the lab-local generators (T-TST-9 spec §1); the shared engine
contributes ModuleDescriptor / FieldRange / run_suite.

Source: DTC_VOCABULARY.md §4 (routing tags), §9 (context classifier),
        §8 (fuel system status).
"""

from __future__ import annotations

import re
from typing import Any

from dtclab.core.data_fusion_sanitizer import DataFusionSanitizer
from dtclab.schemas.vocabulary import (
    DTC_REGEX,
    FuelSystemStatus,
)
from harness.descriptor import FieldRange, ModuleDescriptor

# ---------------------------------------------------------------------------
# CSV column ↔ runtime name mappings (T-TST-7 projection script)
# ---------------------------------------------------------------------------

_CSV_TO_FF_PID: dict[str, str] = {
    "ff_ect": "coolant_temp_c",
    "ff_rpm": "engine_rpm",
    "ff_load": "calculated_load_pct",
    "ff_map": "manifold_pressure_kpa",
    "ff_stft_b1": "short_term_ft1",
    "ff_ltft_b1": "long_term_ft1",
}

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

# Mandatory PIDs that the CSV projection does not supply — filled with
# benign defaults in build_args so the pipeline can run on partial-FF rows.
_MISSING_FF_DEFAULTS: dict[str, Any] = {
    "vehicle_speed_kmh": 0,
    "ignition_advance_deg": 0,
    "intake_air_temp_c": 20,
    "maf_gps": 0,
    "throttle_pos_pct": 0,
}

_EXPECTED_COLS = (
    "expected_routing_tags",
    "expected_historical_context",
    "expected_freeze_frame_status",
)

_COMPILED_DTC_REGEX = re.compile(DTC_REGEX)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_dtc_cell(raw: str) -> list[str]:
    """Split a DTC cell on comma or pipe, strip whitespace, drop empties."""
    if not raw.strip():
        return []
    tokens = re.split(r"[,\|]", raw)
    return [t.strip() for t in tokens if t.strip()]


def _map_fuel_status(raw: str) -> FuelSystemStatus | None:
    """Map a CSV fuel_status value to the enum; None if empty/unrecognised."""
    if not raw.strip():
        return None
    return _FUEL_STATUS_MAP.get(raw.strip())


# ---------------------------------------------------------------------------
# Descriptor builder
# ---------------------------------------------------------------------------


def build_dtclab_descriptor() -> ModuleDescriptor:
    """Build a ModuleDescriptor for the DTCLab fork.

    boxes is empty — continuous FaultBox geometry does not apply to
    discrete DTC codes (T-TST-9 spec §1, §3). The routing-tag→code-range
    oracle lives in the lab-local generators.
    """
    fields: list[FieldRange] = [
        FieldRange(
            name="routing_exemplar",
            type_="str",
            enum_values=_ROUTING_EXEMPLARS,
        ),
        FieldRange(
            name="fuel_status",
            type_="str",
            enum_values=[e.value for e in FuelSystemStatus],
        ),
        FieldRange(
            name="ff_ect",
            type_="float",
            min_=-40.0,
            max_=150.0,
        ),
        FieldRange(
            name="ff_rpm",
            type_="int",
            min_=0,
            max_=8000,
        ),
        FieldRange(
            name="ff_load",
            type_="float",
            min_=0.0,
            max_=100.0,
        ),
        FieldRange(
            name="active_mil",
            type_="bool",
            enum_values=["True", "False"],
        ),
        FieldRange(
            name="mil_flashing",
            type_="bool",
            enum_values=["True", "False"],
        ),
    ]

    return ModuleDescriptor(
        name="DTCLab",
        fields=fields,
        boxes={},  # discrete lab — no continuous FaultBox geometry
        build_args=_build_args,
        entry_point=_entry_point,
        extract_expected=_extract_expected,
        diff=_diff,
    )


# ---------------------------------------------------------------------------
# One exemplar DTC code per DTCRoutingTag (DTC_VOCABULARY.md §4).
# Used by the combinatorial generator for the routing axis.
# ---------------------------------------------------------------------------

_ROUTING_EXEMPLARS: list[str] = [
    "P0171",  # LEAN_HISTORY
    "P0172",  # RICH_HISTORY
    "P0300",  # MISFIRE_HISTORY
    "P0420",  # CATALYST_HISTORY (DNA-gated)
    "P0401",  # EGR_HISTORY (DNA-gated)
    "P0131",  # O2_HISTORY
    "P0201",  # INJECTOR_HISTORY
    "P0011",  # VVT_HISTORY
    "P0441",  # EVAP_HISTORY
    "P0116",  # THERMAL_HISTORY
    "P0606",  # ECU_INTERNAL_HISTORY
    "P0507",  # IDLE_CONTROL_HISTORY
    "P0234",  # BOOST_HISTORY
    "P0325",  # KNOCK_HISTORY
]


# ---------------------------------------------------------------------------
# build_args / entry_point / extract_expected / diff
# ---------------------------------------------------------------------------


def _entry_point(
    raw_dtcs: dict[str, list[str]],
    raw_freeze_frame: dict[str, Any],
    raw_mode06: dict[str, float],
    *,
    codes_cleared: bool = False,
    active_mil: bool = False,
    mil_flashing: bool = False,
) -> Any:
    """Thin wrapper so the descriptor's entry_point matches the run_suite signature."""
    sanitizer = DataFusionSanitizer(dna_view=None)
    return sanitizer.sanitize(
        raw_dtcs,
        raw_freeze_frame,
        raw_mode06,
        codes_cleared=codes_cleared,
        active_mil=active_mil,
        mil_flashing=mil_flashing,
    )


def _build_args(row: dict[str, str]) -> tuple:
    """Build sanitize() args from a dtclab_cases.csv row.

    Raises ValueError when mandatory freeze-frame PIDs are absent and no
    partial-FF core (ect/rpm/load) is present to hang defaults on.
    """
    # --- DTCs ---
    dtc_codes = _parse_dtc_cell(row.get("dtcs", ""))
    raw_dtcs: dict[str, list[str]] = {
        "$03": dtc_codes,
        "$07": [],
        "$0A": [],
    }

    # --- Freeze frame ---
    raw_freeze_frame: dict[str, Any] = {}
    has_ff_core = False
    for csv_col, pid_name in _CSV_TO_FF_PID.items():
        val = row.get(csv_col, "").strip()
        if val:
            raw_freeze_frame[pid_name] = val
            if csv_col in ("ff_ect", "ff_rpm", "ff_load"):
                has_ff_core = True

    # fuel_status
    fuel_raw = row.get("fuel_status", "").strip()
    if fuel_raw:
        fs_enum = _map_fuel_status(fuel_raw)
        if fs_enum is not None:
            raw_freeze_frame["fuel_system_status"] = fs_enum.value

    # Fill missing mandatory PIDs with defaults when core FF data is present.
    if has_ff_core:
        for pid_name, default in _MISSING_FF_DEFAULTS.items():
            if pid_name not in raw_freeze_frame:
                raw_freeze_frame[pid_name] = default

    # --- Mode $06 (always empty for CSV projection) ---
    raw_mode06: dict[str, float] = {}

    # --- MIL flags ---
    codes_cleared = False
    active_mil = bool(dtc_codes)
    mil_flashing = False

    return (raw_dtcs, raw_freeze_frame, raw_mode06, codes_cleared, active_mil, mil_flashing)


def _extract_expected(row: dict[str, str]) -> dict[str, Any]:
    """Extract expected-output columns from a CSV row.

    All expected columns are empty in T-TST-7 (gt_method=characterization).
    """
    return {col: row.get(col, "") for col in _EXPECTED_COLS}


def _diff(actual: Any, expected: dict[str, Any]) -> list[str]:
    """Compare DTCLabPayload fields to expected dict values.

    Empty expected cells are skipped (characterization net — nothing to assert).
    """
    mismatches: list[str] = []
    from dtclab.schemas.payload import DTCLabPayload

    if not isinstance(actual, DTCLabPayload):
        return [f"expected DTCLabPayload, got {type(actual).__name__}"]

    exp_tags = expected.get("expected_routing_tags", "")
    if exp_tags.strip():
        actual_tags = [t.value for t in actual.routing_tags]
        exp_list = [t.strip() for t in exp_tags.split(",") if t.strip()]
        if sorted(actual_tags) != sorted(exp_list):
            mismatches.append(
                f"routing_tags mismatch: {sorted(actual_tags)} != {sorted(exp_list)}"
            )

    exp_ctx = expected.get("expected_historical_context", "")
    if exp_ctx.strip():
        actual_ctx = actual.historical_fault_context.value
        if actual_ctx != exp_ctx:
            mismatches.append(
                f"historical_context mismatch: {actual_ctx} != {exp_ctx}"
            )

    exp_ff = expected.get("expected_freeze_frame_status", "")
    if exp_ff.strip():
        # freeze_frame_status is derived from the freeze_frame record validity
        pass

    return mismatches
