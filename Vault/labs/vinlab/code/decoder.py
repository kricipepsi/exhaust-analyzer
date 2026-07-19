"""RobustVINDecoder — per VINlookup.md (patched) with overlay rules.

Adaptive VIN decoder implementing:
  - NHTSA modulo-11 checksum validation with European legacy bypass
  - Low-volume manufacturer rule (SAE J853, vin[2] == '9')
  - L-year disambiguation (1990 vs 2020) via WMI era_hint
  - Two-path engine resolution (vds_full / pos_8_only fallback)
  - vref.db tech-mask + CoC overlay
  - H1 petrol-only guard, H2 1990-2020 year bound
"""

from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path
from typing import Any

from vinlab.db.tecdoc_query import lookup_engine_ref
from vinlab.models import (
    AirMeteringArchitecture,
    AirMeteringStrategy,
    Emissions,
    EuroEmissionCategory,
    FuelDeliveryType,
    InductionType,
    VinConfidence,
    VinDNA,
)
from vinlab.overlay.air_metering import classify_air_metering
from vinlab.overlay.cylinder_heuristic import infer_cylinder as _infer_cylinder
from vinlab.overlay.horizon import euro_to_horizon
from vinlab.overlay.stress_rpm import stress_idle_rpm
from vinlab.overlay.switches import derive_upstream_o2_type

__all__ = ["ChassisNumberError", "RobustVINDecoder", "VINDecodeError", "pre_clean_vin"]


class VINDecodeError(ValueError):
    """Raised when a VIN cannot be decoded within VINLab's supported scope."""


class ChassisNumberError(VINDecodeError):
    """Raised when input length != 17 — likely a pre-VIN chassis/frame number.

    Callers can catch ``ChassisNumberError`` to route these to a separate
    legacy-identifier pipeline rather than treating them as decode failures.
    Catching ``VINDecodeError`` still catches this subclass.
    """


# source: SAE J853 §4.1.2 — I, O, Q are excluded from VIN character set.
# I→1 and O→0 substitution is the VIN-standard recovery for OCR/keyboard errors.
_CHAR_SUBSTITUTIONS: dict[str, str] = {"I": "1", "O": "0"}

# source: NHTSA 49 CFR Part 565 — VIN checksum transliteration table
_TRANSLITERATION: dict[str, int] = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
}
# source: NHTSA 49 CFR Part 565 — position weights (pos 9 check digit = 0)
_WEIGHTS: tuple[int, ...] = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)

# source: VINlookup.md §1 — valid VIN characters (excludes I, O, Q)
_VIN_PATTERN = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")

# source: H1 petrol-only — keywords that signal out-of-scope fuel types
_NON_PETROL_KEYWORDS: tuple[str, ...] = (
    "DIESEL", "LPG", "CNG", "E85", "HYBRID", "ELECTRIC", "EV",
    "FLEX_FUEL", "FLEXFUEL", "METHANOL", "ETHANOL", "BIOFUEL",
)

# source: Wikipedia "List of sovereign states and dependent territories in Europe"
# + European Commission member/EEA states — used to skip NHTSA checksum
# for European-market VINs where the check-digit was never mandatory.
_EUROPEAN_COUNTRIES: frozenset[str] = frozenset({
    "FRANCE", "GERMANY", "UNITED KINGDOM", "ITALY", "SWEDEN", "SPAIN",
    "NETHERLANDS", "BELGIUM", "AUSTRIA", "FINLAND", "DENMARK", "NORWAY",
    "PORTUGAL", "POLAND", "CZECH REPUBLIC", "SLOVAKIA", "HUNGARY",
    "ROMANIA", "BULGARIA", "CROATIA", "SLOVENIA", "ESTONIA", "LATVIA",
    "LITHUANIA", "IRELAND", "GREECE", "LUXEMBOURG", "SWITZERLAND",
})

# source: ISO 3780 — NHTSA checksum (49 CFR Part 565) is mandatory only
# for vehicles manufactured for sale in the USA/Canada/Mexico market.
# Manufacturers in these countries do not encode a NHTSA check digit.
_NON_NHTSA_COUNTRIES: frozenset[str] = frozenset({
    "JAPAN",
    "SOUTH KOREA",
    "INDIA",
})

# source: T-FX-5 full-run analysis — 1,866 Mexican Mazda VINs in OPSI have
# invalid check digits. Mazda Mexico (NAFTA) should follow NHTSA checksum but
# the Slovenian DMV registration data has corrupt pos-9 digits for these WMIs.
_OPSI_CHECKSUM_CORRUPT_PREFIXES: frozenset[str] = frozenset({
    "3MZ", "3MD", "3MV",
})

# source: SEMANTIC_CONTRACT.md §6.4 — euro_norm string normalisation
_EURO_MAP: dict[str, str] = {
    "euro1": "EURO_1", "euro 1": "EURO_1",
    "euro2": "EURO_2", "euro 2": "EURO_2",
    "euro3": "EURO_3", "euro 3": "EURO_3",
    "euro4": "EURO_4", "euro 4": "EURO_4",
    "euro5": "EURO_5", "euro 5": "EURO_5",
    "euro6": "EURO_6", "euro 6": "EURO_6",
    "euro7": "EURO_7", "euro 7": "EURO_7",
}


# SAE J853 excludes I, O, Q, U, Z from the year-code alphabet.
# '0' is also unused. Manufacturers assign these as placeholders
# for non-year-coded market variants; treat them as year=None.
_YEAR_PASSTHROUGH: frozenset[str] = frozenset({"0", "U", "Z"})


def _normalise_euro(raw: str | None) -> str:
    """Normalise a raw euro_norm string to the contract enum form."""
    if raw is None:
        return "EURO_1"
    key = raw.strip().lower()
    return _EURO_MAP.get(key, "EURO_1")


def _fold_brand(raw: str) -> str:
    """Fold a display brand into a stable join key.

    Brand display values remain untouched. Join keys ignore case, diacritics,
    spaces, hyphens, and other punctuation so equivalent source spellings
    resolve through the same fallback index.
    """
    decomposed = unicodedata.normalize("NFKD", raw)
    without_diacritics = "".join(
        char for char in decomposed if not unicodedata.combining(char)
    )
    return re.sub(r"[^A-Z0-9]+", "", without_diacritics.upper())


def _is_non_petrol(*values: str | None) -> bool:
    """Check any value for non-petrol fuel keywords (H1 guard)."""
    for v in values:
        if v is None:
            continue
        upper = v.upper()
        for kw in _NON_PETROL_KEYWORDS:
            if kw in upper:
                return True
    return False


def pre_clean_vin(raw: str) -> str:
    """Substitute visually ambiguous characters before VIN validation.

    Replaces ``I`` → ``1`` and ``O`` → ``0`` per SAE J853 exclusion rule.
    Strips whitespace and uppercases. Does not validate length or charset.

    Args:
        raw: The raw VIN string as received from the data source.

    Returns:
        Cleaned VIN string ready for structural validation.
    """
    cleaned = raw.strip().upper()
    for bad, good in _CHAR_SUBSTITUTIONS.items():
        cleaned = cleaned.replace(bad, good)
    return cleaned


class RobustVINDecoder:
    """Adaptive VIN decoder with position-8 fallback and L-year disambiguation.

    Loads wmi.csv, years.csv, vds_engine_map.csv into in-memory dicts
    on init and opens vref.db read-only. All network-free and MySQL-free
    per VINLab hard constraints.
    """

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

        # --- load wmi.csv ---------------------------------------------------
        self.wmi_index: dict[str, dict[str, str]] = {}
        with (data_dir / "wmi.csv").open("r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                key = row["wmi"].strip().upper()
                if key:
                    self.wmi_index[key] = {
                        "brand": (row.get("brand") or "").strip(),
                        "country": (row.get("country") or "").strip(),
                        "era_hint": (row.get("era_hint") or "modern").strip(),
                    }

        # --- load years.csv -------------------------------------------------
        # year_code can repeat (L appears twice). Store lists keyed by code.
        self.year_index: dict[str, list[dict[str, str]]] = {}
        with (data_dir / "years.csv").open("r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                code = row["year_code"].strip().upper()
                if code:
                    self.year_index.setdefault(code, []).append({
                        "calendar_year": row["calendar_year"].strip(),
                        "era_bucket": row["era_bucket"].strip(),
                    })

        # --- load vds_engine_map.csv ----------------------------------------
        self.vds_full_exact_index: dict[str, dict[str, str]] = {}
        self.vds_pos8_exact_index: dict[str, dict[str, str]] = {}
        self.vds_full_index: dict[str, dict[str, str]] = {}
        self.vds_pos8_index: dict[str, dict[str, str]] = {}
        with (data_dir / "vds_engine_map.csv").open(
            "r", encoding="utf-8", newline=""
        ) as fh:
            for row in csv.DictReader(fh):
                raw_brand = row["brand"].strip()
                exact_brand = raw_brand.upper()
                folded_brand = _fold_brand(raw_brand)
                if row.get("vds_full", "").strip():
                    vds_full = row["vds_full"].strip().upper()
                    exact_key = f"{exact_brand}_{vds_full}"
                    folded_key = f"{folded_brand}_{vds_full}"
                    self.vds_full_exact_index[exact_key] = row
                    self.vds_full_index.setdefault(folded_key, row)
                elif row.get("pos_8_only", "").strip():
                    pos_8_only = row["pos_8_only"].strip().upper()
                    exact_key = f"{exact_brand}_{pos_8_only}"
                    folded_key = f"{folded_brand}_{pos_8_only}"
                    self.vds_pos8_exact_index[exact_key] = row
                    self.vds_pos8_index.setdefault(folded_key, row)

        # --- vref.db path for H8-compliant lookups ---------------------------
        self.db_path = data_dir / "vref.db"

    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------

    def _is_non_nhtsa_wmi(self, vin: str) -> bool:
        """Return True if checksum validation should be skipped for this VIN.

        Checks both European countries (ISO 3166) and non-NHTSA markets
        (Japan, South Korea, India) where the NHTSA check digit was never
        mandatory per ISO 3780.
        """
        wmi_record = self.wmi_index.get(vin[:3], {})
        country = wmi_record.get("country", "")
        return country in _EUROPEAN_COUNTRIES or country in _NON_NHTSA_COUNTRIES

    def _engine_attrs_from_csv(
        self, engine_row: dict[str, str] | None
    ) -> tuple[float, int, int]:
        """Extract displacement, cylinders, and bank count from CSV engine_row."""
        displacement = 0.0
        cylinder_count = 0
        number_of_banks = 1

        if engine_row is not None:
            csv_disp = engine_row.get("engine_displacement", "").strip()
            if csv_disp:
                try:
                    displacement = float(csv_disp)
                except ValueError:
                    pass
            csv_cyl = engine_row.get("cylinder_count", "").strip()
            if csv_cyl:
                try:
                    cylinder_count = int(csv_cyl)
                except ValueError:
                    pass
            csv_config = (engine_row.get("engine_configuration") or "").strip().upper()
            if csv_config:
                if csv_config[:1] in ("V", "W") or csv_config.startswith("BOXER"):
                    number_of_banks = 2

        return displacement, cylinder_count, number_of_banks

    def _apply_vref_techmask(
        self,
        db_row: dict[str, Any] | None,
        engine_row: dict[str, str] | None,
        model_year: int | None,
        engine_displacement_liters: float,
        induction_type: InductionType,
        fuel_delivery_type: FuelDeliveryType,
        number_of_banks: int,
        euro_emission_category: EuroEmissionCategory,
        conf_flags: list[str],
    ) -> tuple[
        dict[str, Any],
        float,
        InductionType,
        FuelDeliveryType,
        int,
        EuroEmissionCategory,
        Emissions,
        int | None,
        float | None,
        int | None,
        int | None,
        float | None,
        float | None,
        float | None,
        float | None,
        float | None,
        float | None,
        float | None,
        float | None,
        int | None,
        float | None,
    ]:
        """Apply the tech-mask and CoC measurements from vref.db or fall back to CSV-only defaults."""
        db_dict = {}
        displacement = engine_displacement_liters
        induction = induction_type
        fuel_delivery = fuel_delivery_type
        banks = number_of_banks
        euro = euro_emission_category
        emissions = Emissions()

        rated_rpm = None
        target_lambda_v112 = None
        target_rpm_u2 = None
        idle_rpm_low = None
        co_low_idle = None
        co_high_idle = None
        co_type_approval = None
        hc_type_approval = None
        nox_type_approval = None
        hc_nox_type_approval = None
        co2_type_approval = None
        noise_stationary_dba = None
        noise_rpm = None
        noise_driving_dba = None

        if db_row is not None:
            db_dict = db_row
            # displacement — vref.db is authoritative (displacement_cc)
            disp_cc = db_dict.get("displacement_cc")
            if disp_cc is not None and disp_cc > 0:
                displacement = disp_cc / 1000.0

            # induction type
            raw_ind = db_dict.get("induction_type", "")
            if raw_ind and raw_ind.strip():
                induction = InductionType(raw_ind.strip().upper())

            # fuel delivery type
            raw_fuel = db_dict.get("fuel_delivery_type", "")
            if raw_fuel and raw_fuel.strip():
                fuel_delivery = FuelDeliveryType(raw_fuel.strip().upper())
            elif engine_row is not None:
                csv_fuel = engine_row.get("fuel_system_type", "").strip().upper()
                if csv_fuel:
                    fuel_delivery = FuelDeliveryType(csv_fuel)

            # number of banks — is_v_engine flag
            banks = 2 if db_dict.get("is_v_engine") else 1

            # euro emission category
            euro = EuroEmissionCategory(
                _normalise_euro(db_dict.get("euro_norm"))
            )

            # emissions equipment
            emissions = Emissions(
                upstream_o2_type=derive_upstream_o2_type(
                    model_year if model_year is not None else 2000,
                    fuel_delivery,
                    (db_dict.get("o2_type") or "").strip(),
                ),
                downstream_o2_present=(model_year is not None and model_year >= 1996),
                egr_equipped=bool(db_dict.get("has_egr")),
            )

            # --- CoC measurements --------------------------------------------
            rated_rpm = db_dict.get("rated_rpm")
            target_lambda_v112 = db_dict.get("target_lambda_v112")
            target_rpm_u2 = db_dict.get("target_rpm_u2")
            idle_rpm_low = db_dict.get("idle_rpm_low")
            co_low_idle = db_dict.get("co_low_idle")
            co_high_idle = db_dict.get("co_high_idle")
            co_type_approval = db_dict.get("co_type_approval")
            hc_type_approval = db_dict.get("hc_type_approval")
            nox_type_approval = db_dict.get("nox_type_approval")
            hc_nox_type_approval = db_dict.get("hc_nox_type_approval")
            co2_type_approval = db_dict.get("co2_type_approval")
            noise_stationary_dba = db_dict.get("noise_stationary_dba")
            noise_rpm = db_dict.get("noise_rpm")
            noise_driving_dba = db_dict.get("noise_driving_dba")

            # check for NULL CoC fields — any NULL downgrades confidence
            coc_fields = (
                "target_lambda_v112", "target_rpm_u2", "idle_rpm_low",
                "co_low_idle", "co_high_idle", "co_type_approval",
                "hc_type_approval", "nox_type_approval", "co2_type_approval",
            )
            for fld in coc_fields:
                if db_dict.get(fld) is None:
                    conf_flags.append(f"coc_null_{fld}")
                    break
        else:
            # No vref.db row — use CSV-only values with defaults
            if engine_row is not None:
                csv_fuel = engine_row.get("fuel_system_type", "").strip().upper()
                if csv_fuel:
                    fuel_delivery = FuelDeliveryType(csv_fuel)
            emissions = Emissions(
                upstream_o2_type=derive_upstream_o2_type(
                    model_year if model_year is not None else 2000,
                    fuel_delivery, "",
                ),
                downstream_o2_present=(model_year is not None and model_year >= 1996),
            )

        return (
            db_dict,
            displacement,
            induction,
            fuel_delivery,
            banks,
            euro,
            emissions,
            rated_rpm,
            target_lambda_v112,
            target_rpm_u2,
            idle_rpm_low,
            co_low_idle,
            co_high_idle,
            co_type_approval,
            hc_type_approval,
            nox_type_approval,
            hc_nox_type_approval,
            co2_type_approval,
            noise_stationary_dba,
            noise_rpm,
            noise_driving_dba,
        )

    def _cylinder_fallback(
        self,
        cylinder_count: int,
        engine_row: dict[str, str] | None,
        displacement_liters: float,
        brand: str,
        induction_type: InductionType,
        number_of_banks: int,
    ) -> tuple[int, InductionType, int]:
        """Apply last-resort cylinder heuristic fallback (T-VL-7).

        Fires only as last-resort when CSV + vref.db both failed to provide
        a non-zero cylinder_count. Never overwrites real data.
        """
        if cylinder_count == 0:
            engine_code = (
                engine_row.get("engine_code", "").strip()
                if engine_row is not None
                else ""
            )
            hint = _infer_cylinder(engine_code, displacement_liters, brand)
            if hint.count > 0:
                cylinder_count = hint.count
                if induction_type == InductionType.NATURALLY_ASPIRATED:
                    induction_type = InductionType(hint.induction)
                # wiki: SEMANTIC_CONTRACT.md §4.1 — V/W/Boxer engines emit
                # number_of_banks=2.  W16/W12 are 4-bank in metal; contract
                # caps at 2 for OBDLab routing.
                if number_of_banks == 1 and (
                    hint.config[:1] in ("V", "W") or hint.config.startswith("BOXER")
                ):
                    number_of_banks = 2
        return cylinder_count, induction_type, number_of_banks

    def _derive_air_metering(
        self,
        db_dict: dict[str, Any],
        fuel_delivery_type: FuelDeliveryType,
        induction_type: InductionType,
        emissions: Emissions,
    ) -> tuple[AirMeteringArchitecture, AirMeteringStrategy]:
        """Derive air metering strategy and architecture from DB dict, fuel system, and induction."""
        db_maf = db_dict.get("has_maf")
        db_map = db_dict.get("has_map")
        has_maf = (
            bool(db_maf) if db_maf is not None
            else fuel_delivery_type != FuelDeliveryType.CARBURETOR
        )
        has_map = (
            bool(db_map) if db_map is not None
            else (
                induction_type in (InductionType.TURBOCHARGED, InductionType.SUPERCHARGED)
                or fuel_delivery_type == FuelDeliveryType.CARBURETOR
                or fuel_delivery_type == FuelDeliveryType.GDI
                or emissions.egr_equipped
            )
        )

        classification = classify_air_metering(has_maf, has_map)
        air_metering_architecture = AirMeteringArchitecture(
            has_maf_sensor=has_maf,
            has_map_sensor=has_map,
            primary_load_calculation=classification.primary_load_calculation,
        )
        air_metering_strategy = classification.strategy_label
        return air_metering_architecture, air_metering_strategy

    def _compute_confidence(self, conf_flags: list[str]) -> VinConfidence:
        """Compute VIN decode confidence based on collection of confidence flags."""
        if "engine_not_in_csv" in conf_flags:
            return VinConfidence.NONE
        elif conf_flags:
            return VinConfidence.PARTIAL
        else:
            return VinConfidence.HIGH

    # -------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------

    def decode_vin_payload(self, raw_vin: str, *, pre_clean: bool = True) -> VinDNA:
        """Decode a 17-char VIN into a VinDNA dataclass.

        Zero network, zero MySQL. Raises ChassisNumberError for inputs
        that are not 17 characters, VINDecodeError for out-of-scope
        vehicles (H1: non-petrol, H2: year outside 1990-2020).

        Args:
            raw_vin: The VIN string (may contain I/O if pre_clean is True).
            pre_clean: If True (default), apply pre_clean_vin() before
                validation. Set to False if the caller has already cleaned
                the string.
        """
        vin = pre_clean_vin(raw_vin) if pre_clean else raw_vin.strip().upper()
        if len(vin) != 17:
            raise ChassisNumberError(
                f"Input is not a 17-character VIN (len={len(vin)}): {vin!r}. "
                "This may be a pre-standardisation chassis or frame number."
            )
        if not _VIN_PATTERN.match(vin):
            raise VINDecodeError(f"VIN contains invalid characters: {vin!r}")

        # 1. structural validation
        if not self.validate_vin_checksum(vin):
            raise VINDecodeError(f"VIN checksum validation failed: {vin!r}")

        # 2. resolve WMI
        wmi_record = self._resolve_wmi(vin)
        brand = wmi_record.get("brand", "")

        # 3. resolve model year
        model_year, year_flag = self._resolve_year(vin, wmi_record)

        # H2: year within supported scope — only enforced for known years
        if model_year is not None and (model_year < 1990 or model_year > 2020):
            raise VINDecodeError("Year out of supported scope 1990-2020")

        conf_flags: list[str] = []  # track confidence downgrades
        if year_flag:
            conf_flags.append(year_flag)

        # 4. resolve engine from VDS (may be None)
        engine_row = self._resolve_engine(vin, brand, conf_flags)

        # H1: petrol-only guard — check fuel_system_type from CSV
        if engine_row is not None:
            csv_fuel = engine_row.get("fuel_system_type", "")
            if _is_non_petrol(csv_fuel):
                raise VINDecodeError("Fuel type out of scope")

        # 5. vref.db lookup for tech-mask + CoC
        db_row = None
        if engine_row is not None:
            engine_code = engine_row.get("engine_code", "").strip()
            if engine_code:
                db_row = lookup_engine_ref(self.db_path, engine_code)
                if db_row is None:
                    conf_flags.append("engine_not_in_vref")
            else:
                conf_flags.append("no_engine_code")
        else:
            if "wmi_brand_missing" not in conf_flags:
                conf_flags.append("engine_not_in_csv")

        # H1: secondary petrol-only check against vref.db fuel_delivery_type
        if db_row is not None:
            db_fuel = db_row["fuel_delivery_type"] or ""
            if _is_non_petrol(db_fuel):
                raise VINDecodeError("Fuel type out of scope")

        # 6. assemble VinDNA — gather all values, then one constructor call
        _engine_displacement_liters, _cylinder_count, _number_of_banks = (
            self._engine_attrs_from_csv(engine_row)
        )

        (
            db_dict,
            _engine_displacement_liters,
            _induction_type,
            _fuel_delivery_type,
            _number_of_banks,
            _euro_emission_category,
            _emissions,
            _rated_rpm,
            _target_lambda_v112,
            _target_rpm_u2,
            _idle_rpm_low,
            _co_low_idle,
            _co_high_idle,
            _co_type_approval,
            _hc_type_approval,
            _nox_type_approval,
            _hc_nox_type_approval,
            _co2_type_approval,
            _noise_stationary_dba,
            _noise_rpm,
            _noise_driving_dba,
        ) = self._apply_vref_techmask(
            db_row,
            engine_row,
            model_year,
            _engine_displacement_liters,
            InductionType.NATURALLY_ASPIRATED,
            FuelDeliveryType.PORT_INJECTION,
            _number_of_banks,
            EuroEmissionCategory.EURO_1,
            conf_flags,
        )

        _cylinder_count, _induction_type, _number_of_banks = self._cylinder_fallback(
            _cylinder_count,
            engine_row,
            _engine_displacement_liters,
            brand,
            _induction_type,
            _number_of_banks,
        )

        _air_metering_architecture, _air_metering_strategy = self._derive_air_metering(
            db_dict,
            _fuel_delivery_type,
            _induction_type,
            _emissions,
        )

        # --- stress RPM ------------------------------------------------------
        horizon = euro_to_horizon(_euro_emission_category)
        _stress_idle_rpm_target = stress_idle_rpm(
            euro=_euro_emission_category,
            induction=_induction_type,
            fuel_delivery=_fuel_delivery_type,
            displacement=_engine_displacement_liters,
            horizon=horizon,
        )

        _confidence = self._compute_confidence(conf_flags)

        return VinDNA(
            vin=vin,
            make=brand,
            model_year=model_year,
            engine_displacement_liters=_engine_displacement_liters,
            cylinder_count=_cylinder_count,
            number_of_banks=_number_of_banks,
            induction_type=_induction_type,
            fuel_delivery_type=_fuel_delivery_type,
            air_metering_architecture=_air_metering_architecture,
            emissions=_emissions,
            euro_emission_category=_euro_emission_category,
            resolved_horizon=horizon,
            stress_idle_rpm_target=_stress_idle_rpm_target,
            confidence=_confidence,
            air_metering_strategy=_air_metering_strategy,
            rated_rpm=_rated_rpm,
            target_lambda_v112=_target_lambda_v112,
            target_rpm_u2=_target_rpm_u2,
            idle_rpm_low=_idle_rpm_low,
            co_low_idle=_co_low_idle,
            co_high_idle=_co_high_idle,
            co_type_approval=_co_type_approval,
            hc_type_approval=_hc_type_approval,
            nox_type_approval=_nox_type_approval,
            hc_nox_type_approval=_hc_nox_type_approval,
            co2_type_approval=_co2_type_approval,
            noise_stationary_dba=_noise_stationary_dba,
            noise_rpm=_noise_rpm,
            noise_driving_dba=_noise_driving_dba,
        )

    # -------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------

    def validate_vin_checksum(self, vin: str) -> bool:
        """NHTSA modulo-11 checksum with bypass paths.

        Per VINlookup.md §1: the NHTSA 49 CFR Part 565 checksum is mandatory
        only for North American market vehicles. Bypass paths:
        1. Non-NHTSA WMI — European, Japanese, Korean, Indian manufacturers
           do not compute the check digit (ISO 3780, data-driven via wmi.csv).
        2. OPSI corrupt prefixes — Mazda Mexico (3MZ/3MD/3MV) VINs in the
           Slovenian DMV registration data have corrupt pos-9 digits.
        3. Legacy dummy marker — position 9 carries a non-standard character
           (European vehicles from the 1990s often used Z or 0 as a dummy).
        """
        if self._is_non_nhtsa_wmi(vin):
            return True

        if vin[:3] in _OPSI_CHECKSUM_CORRUPT_PREFIXES:
            return True

        # source: NHTSA 49 CFR Part 565 — valid check digits are 0-9, X.
        # European legacy vehicles used Z, 0, or other letters as dummy
        # markers at position 9. Skip validation when the character is
        # not a standard check digit (1-9, X) (where '0' is treated as
        # a dummy/bypass marker per VINlookup.md §1).
        if vin[8] not in "123456789X":
            return True

        total = 0
        for i, char in enumerate(vin):
            if char.isdigit():
                val = int(char)
            else:
                val = _TRANSLITERATION.get(char, 0)
            total += val * _WEIGHTS[i]

        remainder = total % 11
        expected = "X" if remainder == 10 else str(remainder)
        return expected == vin[8]

    # -------------------------------------------------------------------
    # Resolvers
    # -------------------------------------------------------------------

    def _resolve_engine(
        self, vin: str, brand: str, conf_flags: list[str]
    ) -> dict[str, str] | None:
        """Two-path engine resolution with brand-folded fallback (D1/D2/D4).

        Path A: 5-char VDS (vin[3:8]); Path B: legacy pos-8 (vin[7]). Each path
        tries an exact brand key first, then a folded brand key
        (case/diacritic/space/hyphen-insensitive) so equivalent source
        spellings (e.g. "Mercedes-Benz" vs "MERCEDES BENZ") still join. An empty
        brand cannot form a key — flag it loudly so the miss is visible.
        """
        if not brand.strip():
            if "wmi_brand_missing" not in conf_flags:
                conf_flags.append("wmi_brand_missing")
            return None

        vds_slice = vin[3:8]
        pos_8_char = vin[7]
        exact_brand = brand.strip().upper()
        folded_brand = _fold_brand(brand)

        # Path A — modern 5-character VDS match (exact brand, then folded)
        row = self.vds_full_exact_index.get(f"{exact_brand}_{vds_slice}")
        if row is None:
            row = self.vds_full_index.get(f"{folded_brand}_{vds_slice}")
        if row is not None:
            return dict(row)

        # Path B — legacy single-character position-8 fallback
        if pos_8_char:
            row = self.vds_pos8_exact_index.get(f"{exact_brand}_{pos_8_char}")
            if row is None:
                row = self.vds_pos8_index.get(f"{folded_brand}_{pos_8_char}")
            if row is not None:
                return dict(row)

        return None

    def _resolve_wmi(self, vin: str) -> dict[str, str]:
        """Resolve WMI with low-volume manufacturer rule (SAE J853).

        When vin[2] == '9' the manufacturer produces <500 units/year.
        The SAE standard places the manufacturer code at positions 12-13,
        so we try vin[0:3] + vin[11:14] first, then fall back to vin[0:3].
        """
        # Low-volume rule: try 6-char extended WMI first
        if vin[2] == "9":
            extended = vin[0:3] + vin[11:14]
            if extended in self.wmi_index:
                return self.wmi_index[extended]

        # Standard WMI (positions 1-3)
        wmi_key = vin[0:3]
        if wmi_key in self.wmi_index:
            return self.wmi_index[wmi_key]

        raise VINDecodeError(f"WMI not found in registry: {wmi_key!r}")

    def _resolve_year(
        self, vin: str, wmi_record: dict[str, str]
    ) -> tuple[int | None, str | None]:
        """Resolve model year from vin[9]; return None for passthrough chars.

        SAE J853 excludes I, O, Q, U, Z from the year-code alphabet.
        '0' is also unused. Manufacturers assign these as placeholders
        for non-year-coded market variants (e.g., JDM, Italian domestic).
        These return None — year unknown, not an error.

        The only colliding code in 1990-2020 is 'L' (1990 vs 2020).
        Disambiguation uses the WMI era_hint column:
          "legacy" -> ERA_1 -> 1990
          "modern" -> ERA_3 -> 2020
        """
        year_char = vin[9]
        if year_char in _YEAR_PASSTHROUGH:
            return None, None
        candidates = self.year_index.get(year_char)
        if not candidates:
            raise VINDecodeError(f"Year character not found: {year_char!r}")

        if len(candidates) == 1:
            return int(candidates[0]["calendar_year"]), None

        # L-year disambiguation
        era_hint = wmi_record.get("era_hint", "modern")
        for row in candidates:
            if era_hint == "legacy" and row["era_bucket"] == "ERA_1":
                return int(row["calendar_year"]), None
            if era_hint != "legacy" and row["era_bucket"] == "ERA_3":
                return int(row["calendar_year"]), None

        # Fallback: return first candidate with unrecognised-era flag
        return int(candidates[0]["calendar_year"]), "era_hint_unrecognised"
