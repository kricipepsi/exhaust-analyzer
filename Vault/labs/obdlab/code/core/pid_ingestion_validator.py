"""PID ingestion validator per OBDLab_KG_Wiki.md §3.

Source: OBDLab_KG_Wiki.md §3.1 (sensor bounds), §3.2 (unit normalisation).
DNA-relative RPM check per NewArchProposal §3.3 (three-branch confidence).
Bank-2 null contract per OBDLab_KG_Wiki.md §3.1.
"""

import json
import logging
from pathlib import Path

from obdlab.core.exceptions import PIDValidationError
from obdlab.schemas.dna_view import ObdLabDnaView, VinConfidence
from obdlab.schemas.vocabulary import FuelSystemStatus

logger = logging.getLogger(__name__)

# wiki: §3.2 — {alternate_suffix: (canonical_suffix, conversion_fn)}
_UNIT_CONVERSIONS = {
    "_f":     ("_c",   lambda v: (v - 32.0) * 5.0 / 9.0),  # wiki: §3.2 — °F → °C
    "_psi":   ("_kpa", lambda v: v * 6.895),                 # wiki: §3.2 — psi → kPa
    "_inhg":  ("_kpa", lambda v: v * 3.386),                 # wiki: §3.2 — in Hg → kPa
    "_lbmin": ("_gps", lambda v: v * 7.559),                 # wiki: §3.2 — lb/min → g/s
}

_DNA_RPM_HEADROOM = 1.05  # wiki: §3 — 5% headroom for redline overshoot


class PIDIngestionValidator:
    """Validates manually-entered OBD-II PIDs against physical sensor bounds.

    Source: OBDLab_KG_Wiki.md §3.1, §3.2.
    DNA-relative RPM check per NewArchProposal §3.3.
    """

    def __init__(self, config_path: Path) -> None:
        with open(config_path, encoding="utf-8") as fh:
            config = json.load(fh)
        self._bounds: dict = config["bounds"]

    def validate_and_convert(
        self,
        raw_user_inputs: dict,
        dna_view: ObdLabDnaView | None = None,
    ) -> dict:
        """Apply §3.2 unit conversions, validate against §3.1 bounds, return sanitised dict.

        Raises PIDValidationError on bounds violation, DNA-RPM exceedance, or
        bank-2 null contract breach.
        """
        sanitized = self._apply_unit_conversions(raw_user_inputs)
        self._validate_bounds(sanitized)
        self._check_dna_rpm(sanitized, dna_view)
        self._enforce_bank2_contract(sanitized)
        self._validate_and_map_fuel_system_status(raw_user_inputs, sanitized)
        self._validate_per_cylinder_misfire_counts(raw_user_inputs, sanitized)
        self._validate_ltft_cell_vector(raw_user_inputs, sanitized)
        return sanitized

    def _validate_ltft_cell_vector(self, raw_user_inputs: dict, sanitized: dict) -> None:
        """Validate and ferry ltft_cell_vector.

        Must be a dict[int, float] or None.
        Cell indices must be non-negative integers (>= 0).
        LTFT % values must be floats or ints between -127 and 127.
        Raises PIDValidationError on violation.
        """
        vector = raw_user_inputs.get("ltft_cell_vector")
        if vector is None:
            sanitized["ltft_cell_vector"] = None
            return

        if not isinstance(vector, dict):
            raise PIDValidationError(
                f"ltft_cell_vector: expected dict, got {type(vector).__name__}"
            )

        sanitized_vector = {}
        for cell, ltft in vector.items():
            try:
                cell_idx = int(cell)
            except (ValueError, TypeError) as exc:
                raise PIDValidationError(
                    f"ltft_cell_vector: cell key must be integer, got {cell}"
                ) from exc

            try:
                ltft_val = float(ltft)
            except (ValueError, TypeError) as exc:
                raise PIDValidationError(
                    f"ltft_cell_vector: LTFT for cell {cell} must be numeric, got {ltft}"
                ) from exc

            if cell_idx < 0:  # wiki: research/chunks/fuel-trim/13
                raise PIDValidationError(
                    f"ltft_cell_vector: cell index must be >= 0, got {cell_idx}"
                )

            if ltft_val < -127 or ltft_val > 127:  # wiki: research/chunks/fuel-trim/13
                raise PIDValidationError(
                    f"ltft_cell_vector: LTFT for cell {cell_idx} must be between -127 and 127, got {ltft_val}"
                )

            sanitized_vector[cell_idx] = ltft_val

        sanitized["ltft_cell_vector"] = sanitized_vector

    def _validate_per_cylinder_misfire_counts(self, raw_user_inputs: dict, sanitized: dict) -> None:
        """Validate and ferry per_cylinder_misfire_counts.

        Must be a dict[int, int] or None.
        Cylinder indices must be >= 1 (1-indexed).
        Misfire counts must be >= 0.
        Raises PIDValidationError on violation.
        """
        counts = raw_user_inputs.get("per_cylinder_misfire_counts")
        if counts is None:
            sanitized["per_cylinder_misfire_counts"] = None
            return

        if not isinstance(counts, dict):
            raise PIDValidationError(
                f"per_cylinder_misfire_counts: expected dict, got {type(counts).__name__}"
            )

        sanitized_counts = {}
        for cyl, count in counts.items():
            try:
                cyl_idx = int(cyl)
            except (ValueError, TypeError) as exc:
                raise PIDValidationError(
                    f"per_cylinder_misfire_counts: cylinder key must be integer, got {cyl}"
                ) from exc

            try:
                cnt_val = int(count)
            except (ValueError, TypeError) as exc:
                raise PIDValidationError(
                    f"per_cylinder_misfire_counts: misfire count for cylinder {cyl} must be integer, got {count}"
                ) from exc

            if cyl_idx < 1:  # wiki: research/chunks/fuel-trim/17
                raise PIDValidationError(
                    f"per_cylinder_misfire_counts: cylinder index must be >= 1, got {cyl_idx}"
                )

            if cnt_val < 0:  # wiki: research/chunks/fuel-trim/17
                raise PIDValidationError(
                    f"per_cylinder_misfire_counts: misfire count for cylinder {cyl_idx} must be non-negative, got {cnt_val}"
                )

            sanitized_counts[cyl_idx] = cnt_val

        sanitized["per_cylinder_misfire_counts"] = sanitized_counts

    def _validate_and_map_fuel_system_status(self, raw_user_inputs: dict, sanitized: dict) -> None:
        """Validate and map fuel_system_status/fuel_sys_status manual input to FuelSystemStatus enum."""
        fuel_status_val = raw_user_inputs.get("fuel_system_status")
        if fuel_status_val is None:
            fuel_status_val = raw_user_inputs.get("fuel_sys_status")

        if fuel_status_val is not None:
            sanitized_fuel_status = FuelSystemStatus.from_wire(fuel_status_val)
            if sanitized_fuel_status is None:
                if isinstance(fuel_status_val, str):
                    raise PIDValidationError(f"Invalid fuel_system_status value: {fuel_status_val}")
                else:
                    raise PIDValidationError(
                        f"fuel_system_status: expected string or FuelSystemStatus, got {type(fuel_status_val).__name__}"
                    )
            sanitized["fuel_system_status"] = sanitized_fuel_status
            sanitized["fuel_sys_status"] = sanitized_fuel_status
        else:
            sanitized["fuel_system_status"] = FuelSystemStatus.CL
            sanitized["fuel_sys_status"] = FuelSystemStatus.CL

    # ------------------------------------------------------------------
    # §3.2 — unit normalisation
    # ------------------------------------------------------------------

    def _apply_unit_conversions(self, inputs: dict) -> dict:
        """Convert alternate-unit fields to canonical form per §3.2.

        When both an alternate and canonical field are present for the same
        quantity, the canonical value is kept and the alternate is dropped.
        """
        result: dict = {}
        for key, value in inputs.items():
            if not isinstance(key, str):
                result[key] = value
                continue

            matched = False
            for alt_suffix, (canon_suffix, convert_fn) in _UNIT_CONVERSIONS.items():
                if key.endswith(alt_suffix):
                    canon_key = key[: -len(alt_suffix)] + canon_suffix
                    # Only convert if the canonical field is not already present
                    if canon_key not in inputs:
                        result[canon_key] = convert_fn(value)
                    # Drop the alternate — canonical form is the output
                    matched = True
                    break

            if not matched:
                result[key] = value

        return result

    # ------------------------------------------------------------------
    # §3.1 — boundary validation
    # ------------------------------------------------------------------

    def _validate_bounds(self, inputs: dict) -> None:
        """Validate each field against §3.1 bounds. Raise PIDValidationError on violation.

        Bank-2 fields (shrtft2, longft2) are only validated when
        number_of_banks == 2.  Fields not in the bounds table pass through.
        """
        number_of_banks = inputs.get("number_of_banks", 1)

        for field, bound in self._bounds.items():
            value = inputs.get(field)
            if value is None:
                continue

            # Bank-2 fields only validated when number_of_banks == 2
            if field in ("shrtft2", "longft2") and number_of_banks != 2:
                continue

            if not isinstance(value, (int, float)):
                raise PIDValidationError(
                    f"{field}: expected numeric, got {type(value).__name__}"
                )

            if value < bound["min"] or value > bound["max"]:
                raise PIDValidationError(
                    f"{field}={value} outside bounds "
                    f"[{bound['min']}, {bound['max']}] {bound['unit']}"
                )

    # ------------------------------------------------------------------
    # DNA-relative RPM check — three-branch confidence pattern
    # ------------------------------------------------------------------

    def _check_dna_rpm(
        self, inputs: dict, dna_view: ObdLabDnaView | None,
    ) -> None:
        """DNA-relative RPM boundary per NewArchProposal §3.3.

        HIGH:     strict — engine_rpm > rated_rpm * 1.05 raises PIDValidationError.
        PARTIAL:  log-and-fallback to static 0..8000.
        NONE/None: static 0..8000 (already enforced by §3.1 bounds).
        """
        engine_rpm = inputs.get("engine_rpm")
        if engine_rpm is None:
            return

        if dna_view is None or dna_view.confidence == VinConfidence.NONE:
            return

        if dna_view.confidence == VinConfidence.PARTIAL:
            logger.info(
                "dna_check_downgraded: check=rpm_vs_rated reason=PARTIAL_DNA"
            )
            return

        # HIGH confidence
        rated_rpm = dna_view.rated_rpm
        if rated_rpm is None:
            return

        limit = rated_rpm * _DNA_RPM_HEADROOM
        if engine_rpm > limit:
            raise PIDValidationError(
                f"engine_rpm {engine_rpm} exceeds DNA rated_rpm "
                f"{rated_rpm} * {_DNA_RPM_HEADROOM} = {limit:.1f}"
            )

    # ------------------------------------------------------------------
    # Bank-2 null contract per §3.1
    # ------------------------------------------------------------------

    def _enforce_bank2_contract(self, inputs: dict) -> None:
        """Enforce bank-2 null contract per OBDLab_KG_Wiki.md §3.1.

        shrtft2 and longft2 must be null (None) when number_of_banks == 1.
        Emitting 0.0 for absent bank fields is a SEMANTIC_CONTRACT violation.
        """
        if inputs.get("number_of_banks", 1) != 1:
            return

        for field in ("shrtft2", "longft2"):
            value = inputs.get(field)
            if value is not None:
                raise PIDValidationError(
                    f"{field} must be null when number_of_banks == 1, "
                    f"got {value} — SEMANTIC_CONTRACT §4.4 violation"
                )
