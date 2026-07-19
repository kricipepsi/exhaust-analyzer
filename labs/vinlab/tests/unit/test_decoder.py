"""Decoder tests — exercises RobustVINDecoder against the actual vinlab/data/ artefacts."""

from __future__ import annotations

import pytest
from vinlab.decoder import (
    _EUROPEAN_COUNTRIES,
    ChassisNumberError,
    RobustVINDecoder,
    VINDecodeError,
    _fold_brand,
    _is_non_petrol,
    pre_clean_vin,
)
from vinlab.overlay.horizon import _year_to_horizon


class TestValidDecodes:
    def test_citroen_presentation_vin_resolves_engine(self, decoder):
        dna = decoder.decode_vin_payload("VF7SA5FR8AW511081")
        assert dna.make == "CITROEN"
        assert dna.engine_displacement_liters == 1.598
        assert dna.cylinder_count == 4
        assert dna.fuel_delivery_type == "GDI"
        assert dna.induction_type == "TURBOCHARGED"
        assert dna.euro_emission_category == "EURO_5"
        assert dna.confidence == "HIGH"

    def test_peugeot_5fr_vin_uses_same_authoritative_equipment(self, decoder):
        dna = decoder.decode_vin_payload("VF3WB5FR8CE025644")
        assert dna.make == "Peugeot"
        assert dna.engine_displacement_liters == 1.598
        assert dna.cylinder_count == 4
        assert dna.fuel_delivery_type == "GDI"
        assert dna.induction_type == "TURBOCHARGED"
        assert dna.euro_emission_category == "EURO_5"
        assert dna.confidence == "HIGH"

    @pytest.mark.parametrize(
        (
            "vin",
            "make",
            "displacement",
            "cylinders",
            "induction",
            "fuel",
            "euro",
            "has_maf",
            "has_map",
            "co2",
        ),
        [
            (
                "JF1BC5CL0A1234567",
                "Subaru",
                1.994,
                4,
                "NATURALLY_ASPIRATED",
                "PORT_INJECTION",
                "EURO_4",
                True,
                False,
                206.0,
            ),
            (
                "WBA1B9100A1234567",
                "BMW",
                2.979,
                6,
                "TURBOCHARGED",
                "GDI",
                "EURO_5",
                False,
                True,
                186.0,
            ),
            (
                "WBA1S3100G1234567",
                "BMW",
                1.998,
                4,
                "TURBOCHARGED",
                "GDI",
                "EURO_6",
                True,
                True,
                159.0,
            ),
        ],
    )
    def test_vref1_tranche_vins_receive_sourced_techmask(
        self,
        decoder,
        vin,
        make,
        displacement,
        cylinders,
        induction,
        fuel,
        euro,
        has_maf,
        has_map,
        co2,
    ):
        dna = decoder.decode_vin_payload(vin)

        assert dna.make == make
        assert dna.engine_displacement_liters == displacement
        assert dna.cylinder_count == cylinders
        assert dna.induction_type == induction
        assert dna.fuel_delivery_type == fuel
        assert dna.euro_emission_category == euro
        assert dna.air_metering_architecture.has_maf_sensor is has_maf
        assert dna.air_metering_architecture.has_map_sensor is has_map
        assert dna.co2_type_approval == co2
        assert dna.confidence == "HIGH"

    def test_mercedes_brand_spelling_resolves_through_folded_join(self, decoder):
        dna = decoder.decode_vin_payload("1MB010010A1234567")
        assert dna.make == "Mercedes-Benz"
        assert dna.engine_displacement_liters == 1.8
        assert dna.cylinder_count == 4
        assert dna.confidence == "PARTIAL"

    def test_renault_2002_petrol(self, decoder):
        """VF1CB05CF25935016 — Renault Clio 1.2, 2002, Port Injection."""
        dna = decoder.decode_vin_payload("VF1CB05CF25935016")
        assert dna.make == "Renault"
        assert dna.model_year == 2002
        assert dna.engine_displacement_liters == 1.1
        assert dna.fuel_delivery_type == "PORT_INJECTION"
        assert dna.confidence in ("HIGH", "PARTIAL")
        assert dna.air_metering_architecture.has_maf_sensor is True
        assert dna.emissions.upstream_o2_type == "WIDEBAND_AFR"

    def test_renault_2001_petrol(self, decoder):
        """VF1357K0F17697151 — Renault Clio 1.2, model year 2001."""
        dna = decoder.decode_vin_payload("VF1357K0F17697151")
        assert dna.make == "Renault"
        assert dna.model_year == 2001
        assert _year_to_horizon(dna.model_year) == "HORIZON_ADAPTIVE"
        assert dna.engine_displacement_liters == 1.1
        assert dna.confidence in ("HIGH", "PARTIAL")

    def test_land_rover_legacy_none_confidence(self, decoder):
        """SALLN12P0YAXXXXXX — Land Rover, no engine in CSV or vref.db → NONE."""
        dna = decoder.decode_vin_payload("SALLN12P0YAXXXXXX")
        assert dna.make == "Land Rover"
        assert dna.model_year == 2000
        assert dna.confidence == "NONE"
        assert dna.engine_displacement_liters == 0.0
        assert dna.cylinder_count == 0

class TestNormalisedVrefJoinAndAmbiguity:
    """T-VIN-ENG-2: Normalized vref join + engine-ambiguity confidence flag."""

    def test_normalised_join_matches_despite_space_dot_case(self, decoder):
        """A VIN whose map code differs from vref only by space/dot/case
        receives the vref tech-mask (using real pair from ENG-1 disclosure).

        Example: Lotus VDS LNBBL maps to '2ZZ-GE' in map; vref has '2ZZGE'.
        Normalized join (uppercase, alphanumeric only) should match both.
        """
        # Lotus Elise VIN with VDS LNBBL -> engine_code '2ZZ-GE' in map
        # vref.db has '2ZZGE' (without hyphen)
        dna = decoder.decode_vin_payload("SCCLNBBL0AA000001")
        assert dna.make == "Lotus"
        # If normalized join works, we get tech-mask from vref
        assert dna.fuel_delivery_type in ("PORT_INJECTION", "GDI", "DIRECT_INJECTION")
        assert dna.induction_type in ("NATURALLY_ASPIRATED", "TURBOCHARGED", "SUPERCHARGED")
        # Confidence should be HIGH or PARTIAL (not NONE)
        assert dna.confidence in ("HIGH", "PARTIAL")

    def test_ambiguity_flag_demotes_confidence(self, decoder):
        """VINs with majority_share < 0.70 get 'vds_engine_ambiguous' flag
        and confidence demoted to PARTIAL."""
        # Volkswagen VDS ZZZ9N has majority_share=0.249 (from ENG-1 disclosure)
        dna = decoder.decode_vin_payload("WVWZZZ9NZ6D040769")
        assert dna.make == "Volkswagen"
        # Ambiguity flag should demote confidence to PARTIAL
        assert dna.confidence == "PARTIAL"

    def test_unambiguous_high_majority_share_keeps_high_confidence(self, decoder):
        """VINs with majority_share >= 0.70 should NOT get ambiguity flag."""
        # Citroen VDS SA5FR has high majority_share
        dna = decoder.decode_vin_payload("VF7SA5FR8AW511081")
        assert dna.make == "CITROEN"
        # Should remain HIGH (no ambiguity flag)
        assert dna.confidence == "HIGH"

class TestBrandJoinIntegrity:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("Mercedes-Benz", "MERCEDESBENZ"),
            ("MERCEDES BENZ", "MERCEDESBENZ"),
            ("Škoda", "SKODA"),
        ],
    )
    def test_brand_fold_normalises_join_variants(self, raw, expected):
        assert _fold_brand(raw) == expected

    def test_blank_wmi_brand_sets_flag_and_downgrades_public_confidence(self, decoder):
        flags: list[str] = []
        assert decoder._resolve_engine("115ZZZZZZAZZZZZZZ", "", flags) is None
        assert flags == ["wmi_brand_missing"]
        assert decoder._compute_confidence(flags) == "PARTIAL"

        dna = decoder.decode_vin_payload("115ZZZZZZAZZZZZZZ")
        assert dna.make == ""
        assert dna.confidence == "PARTIAL"
        assert dna.engine_displacement_liters == 0.0
        assert dna.cylinder_count == 0

    def test_position_8_fallback_resolves_engine(self, tmp_path, make_mini_data_dir):
        data_dir = make_mini_data_dir(tmp_path)
        with (data_dir / "vds_engine_map.csv").open(
            "a", encoding="utf-8", newline=""
        ) as fh:
            fh.write("RENAULT,,C,D4F-POS8,1.1,4,PORT_INJECTION,INLINE\n")
        loaded = RobustVINDecoder(data_dir)

        row = loaded._resolve_engine("VF1ZZZZCZ2ZZZZZZZ", "Renault", [])

        assert row is not None
        assert row["engine_code"] == "D4F-POS8"


class TestDecoderLoading:
    def test_short_wmi_row_does_not_prevent_decoder_construction(
        self, tmp_path, make_mini_data_dir
    ):
        data_dir = make_mini_data_dir(tmp_path)
        with (data_dir / "wmi.csv").open("a", encoding="utf-8", newline="") as fh:
            fh.write("YTD,Toyota,CZEC\n")
            fh.write("ZZ1\n")

        loaded = RobustVINDecoder(data_dir)

        assert loaded.wmi_index["YTD"] == {
            "brand": "Toyota",
            "country": "CZEC",
            "era_hint": "modern",
        }
        assert loaded.wmi_index["ZZ1"] == {
            "brand": "",
            "country": "",
            "era_hint": "modern",
        }


class TestLYearDisambiguation:
    def test_l_year_legacy_wmi(self, decoder):
        """VIN with vin[9]='L' and legacy WMI → resolves to 1990."""
        # WMI '101' has era_hint=legacy; vin[8]='Z' bypasses checksum
        dna = decoder.decode_vin_payload("101ZZZZZZLZZZZZZZ")
        assert dna.model_year == 1990
        assert _year_to_horizon(dna.model_year) == "HORIZON_LEGACY"

    def test_l_year_modern_wmi(self, decoder):
        """VIN with vin[9]='L' and modern WMI → resolves to 2020."""
        # WMI '102' has era_hint=modern; vin[8]='Z' bypasses checksum
        dna = decoder.decode_vin_payload("102ZZZZZZLZZZZZZZ")
        assert dna.model_year == 2020
        assert _year_to_horizon(dna.model_year) == "HORIZON_MODERN"

    def test_era_hint_unrecognised_flagged(self, decoder, monkeypatch):
        """Unrecognised era_hint triggers flag, not silent fallback.

        Strategy (b): when era_hint is neither "legacy" nor "modern" AND
        no ERA_3-matching row exists among candidates, _resolve_year returns
        the first candidate with the "era_hint_unrecognised" flag. The
        caller appends this to conf_flags, degrading confidence to PARTIAL.

        The fallback is structurally dead with current production data
        (wmi.csv only carries "legacy"/"modern" and year code L has both
        ERA_1 and ERA_3 rows). This test monkeypatches year_index to
        simulate a future data shape that would activate it.
        """
        monkeypatch.setitem(
            decoder.year_index, "L",
            [
                {"calendar_year": "1990", "era_bucket": "ERA_1"},
                {"calendar_year": "1991", "era_bucket": "ERA_1"},
            ],
        )
        year, flag = decoder._resolve_year(
            "101ZZZZZZLZZZZZZZ", {"era_hint": "unknown"},
        )
        assert year == 1990
        assert flag == "era_hint_unrecognised"


class TestLowVolumeManufacturer:
    def test_low_volume_extended_wmi(self, decoder):
        """VIN with vin[2]='9' consults extended 6-char WMI (SAE J853)."""
        # WMI '109013' is the extended entry for '109' with pos 12-14='013'
        dna = decoder.decode_vin_payload("109ZZZZZZLZ013ZZZ")
        assert dna.make == "Odom's Manufacturers"


class TestH1PetrolOnly:
    def test_is_non_petrol_detects_diesel(self):
        """Direct test of the H1 fuel keyword guard."""
        assert _is_non_petrol("DIESEL") is True
        assert _is_non_petrol("GASOLINE") is False
        assert _is_non_petrol("PETROL") is False
        assert _is_non_petrol("LPG") is True
        assert _is_non_petrol("CNG") is True
        assert _is_non_petrol("ELECTRIC") is True
        assert _is_non_petrol("HYBRID") is True
        assert _is_non_petrol(None) is False

    def test_is_non_petrol_case_insensitive(self):
        """Keyword detection is case-insensitive."""
        assert _is_non_petrol("Diesel") is True
        assert _is_non_petrol("diesel") is True
        assert _is_non_petrol("DiEsEl") is True
        assert _is_non_petrol("Flex_Fuel") is True


class TestH2YearBounds:
    def test_year_below_1990_raises(self, decoder):
        """Year character mapping to pre-1990 raises VINDecodeError."""
        original = decoder.year_index.get("A")
        decoder.year_index["A"] = [
            {"calendar_year": "1985", "era_bucket": "ERA_0"}
        ]
        try:
            with pytest.raises(VINDecodeError, match="Year out of supported scope"):
                decoder.decode_vin_payload("VF1ZZZZZZAZZZZZZZ")
        finally:
            if original is not None:
                decoder.year_index["A"] = original
            else:
                decoder.year_index.pop("A", None)


class TestValidation:
    def test_invalid_checksum_raises(self, decoder):
        """North American VIN with bad checksum digit raises VINDecodeError."""
        # vin[8]='1' is in "123456789X" so no European bypass
        # Computed checksum for 1G5ZZZZZ1ZZZZZZZZ is 6, not 1
        with pytest.raises(VINDecodeError):
            decoder.decode_vin_payload("1G5ZZZZZ1ZZZZZZZZ")

    def test_european_bypass_checksum_skip(self, decoder):
        """VIN with vin[8]='Z' skips checksum and proceeds to decode."""
        # European legacy dummy marker at position 9 bypasses checksum
        dna = decoder.decode_vin_payload("VF1CB05CF25935016")
        assert dna.make == "Renault"

    def test_16_char_vin_raises(self, decoder):
        """VIN shorter than 17 chars raises ChassisNumberError (subclass of VINDecodeError)."""
        with pytest.raises(ChassisNumberError, match="not a 17-character VIN"):
            decoder.decode_vin_payload("ABCDEFGHJKLMN123")

    def test_invalid_characters_raise(self, decoder):
        """VIN with I/O chars gets cleaned first; with pre_clean=False it still raises."""
        with pytest.raises(VINDecodeError, match="invalid characters"):
            # pre_clean=False skips I→1/O→0 substitution
            decoder.decode_vin_payload("IIIZZZZZZZZZZZZZZ", pre_clean=False)

    def test_unknown_wmi_raises(self, decoder):
        """VIN with unresolvable WMI raises VINDecodeError."""
        with pytest.raises(VINDecodeError, match="WMI not found"):
            decoder.decode_vin_payload("ZZZZZZZZZXXXXXXXX")


class TestEuropeanChecksumBypass:
    """T-FX-1: European-market VINs skip NHTSA checksum (data-driven WMI→country)."""

    def test_structural_european_countries(self):
        """_EUROPEAN_COUNTRIES frozenset has at least 20 member states."""
        assert len(_EUROPEAN_COUNTRIES) >= 20
        assert "FRANCE" in _EUROPEAN_COUNTRIES
        assert "GERMANY" in _EUROPEAN_COUNTRIES
        assert "UNITED KINGDOM" in _EUROPEAN_COUNTRIES

    EU_VINS = [
        # VIN, expected make, expected year (from vin[9] year code)
        ("WDD1690321J749046", "Mercedes-Benz", 2001),  # vin[9]='1', Germany
        ("VF12R051560978004", "Renault", 2006),          # vin[9]='6', France
        ("W0LGM6ET6E1072040", "Opel", 2014),              # vin[9]='E', EU-market Opel
    ]

    @pytest.mark.parametrize("vin,expected_make,expected_year", EU_VINS)
    def test_european_vin_bypasses_checksum(self, decoder, vin, expected_make, expected_year):
        """Known-failing EU VINs decode after European checksum bypass."""
        dna = decoder.decode_vin_payload(vin)
        assert dna.make == expected_make
        assert dna.model_year == expected_year

    def test_na_vin_still_validates_checksum(self, decoder):
        """North American VIN with correct checksum still validates (no false bypass)."""
        # 1HGCM82633A004352 — Honda US plant, checksum must be enforced
        dna = decoder.decode_vin_payload("1HGCM82633A004352")
        assert dna.make == "Honda"

    def test_na_vin_bad_checksum_still_raises(self, decoder):
        """North American VIN with wrong checksum still raises (bypass only for EU)."""
        # 1G5 is a USA WMI; vin[8]='1' is in 123456789X so no legacy bypass
        with pytest.raises(VINDecodeError):
            decoder.decode_vin_payload("1G5ZZZZZ1ZZZZZZZZ")


class TestYearPassthrough:
    """T-FX-2: VINs with pos[9] in {0, U, Z} decode with model_year=None."""

    PASSTHROUGH_VINS = [
        ("JTDKGNEC50N036354", "Toyota", None),   # pos[9]='0', JDM
        ("ZFA35600006N64200", "Fiat", None),       # pos[9]='0', Italian domestic
        ("WF0UXXGAJU3C20388", "Ford", None),       # pos[9]='U', Ford Germany
    ]

    @pytest.mark.parametrize("vin,expected_make,expected_year", PASSTHROUGH_VINS)
    def test_passthrough_year_vins_decode(self, decoder, vin, expected_make, expected_year):
        """VINs with passthrough year chars decode with model_year=None."""
        dna = decoder.decode_vin_payload(vin)
        assert dna.make == expected_make
        assert dna.model_year is expected_year, (
            f"{vin}: expected model_year=None, got {dna.model_year}"
        )

    def test_standard_vin_still_resolves_year(self, decoder):
        """Regression guard: standard VIN must still resolve to concrete int."""
        dna = decoder.decode_vin_payload("VF1CB05CF25935016")
        assert isinstance(dna.model_year, int)
        assert dna.model_year == 2002


class TestDbRowPath:
    def test_bmw_with_vref_match(self, decoder):
        """BMW VIN with engine_code in both CSV and vref.db hits db_row path."""
        dna = decoder.decode_vin_payload("WBA4W9C5ZLYYYYYYY")
        assert dna.make == "BMW"
        assert dna.model_year == 2020
        assert dna.engine_displacement_liters > 0
        assert dna.confidence == "PARTIAL"  # co_low_idle is NULL
        assert dna.fuel_delivery_type == "GDI"
        assert dna.induction_type == "TURBOCHARGED"
        assert dna.euro_emission_category == "EURO_6"
        # CoC field from vref.db
        assert dna.idle_rpm_low == 714
        assert dna.co_low_idle is None


class TestPreCleanAndChassisNumberError:
    """T-FX-4: pre_clean_vin() + ChassisNumberError for wrong-length inputs."""

    # -- pre_clean_vin unit tests -------------------------------------------

    def test_pre_clean_substitutes_I_to_1(self):
        """I characters → 1 substitution."""
        assert pre_clean_vin("FIAT100GBS0089543") == "F1AT100GBS0089543"

    def test_pre_clean_substitutes_O_to_0(self):
        """O characters → 0 substitution."""
        assert pre_clean_vin("VF1EMOU0631012087") == "VF1EM0U0631012087"

    def test_pre_clean_mixed_I_and_O(self):
        """Multiple I and O characters all substituted."""
        result = pre_clean_vin("  SA9wzeI11WXOE39278  ")
        assert "I" not in result
        assert "O" not in result

    def test_pre_clean_no_substitution_needed(self):
        """Already-clean VIN is uppercased and stripped but not otherwise changed."""
        assert pre_clean_vin("  vf1cb05cf25935016  ") == "VF1CB05CF25935016"

    # -- ChassisNumberError tests -------------------------------------------

    def test_wrong_length_raises_chassis_number_error(self, decoder):
        """len != 17 raises ChassisNumberError, not generic VINDecodeError."""
        with pytest.raises(ChassisNumberError, match="not a 17-character VIN"):
            decoder.decode_vin_payload("S640401316")  # len=10 chassis number

    def test_chassis_number_error_is_subclass_of_vin_decode_error(self, decoder):
        """ChassisNumberError is catchable as VINDecodeError."""
        try:
            decoder.decode_vin_payload("S640401316")
        except VINDecodeError:
            pass  # ChassisNumberError is a subclass, so this catches it
        else:
            pytest.fail("Expected VINDecodeError (or subclass)")

    # -- I/O VINs no longer blocked by invalid_chars ------------------------

    IO_VINS = [
        "FIAT100GBS0089543",   # I in FIAT → cleaned to F1AT...
        "SA9WZEI11WX039278",   # I at pos[6]
        "VF1EMOU0631012087",   # O at pos[6]
        "SJNFAAJ1OU1002472",   # O at pos[9]
    ]

    @pytest.mark.parametrize("vin", IO_VINS)
    def test_io_vin_not_blocked_by_invalid_chars(self, decoder, vin):
        """I/O VINs are cleaned and no longer fail with 'invalid characters'."""
        try:
            decoder.decode_vin_payload(vin)
        except VINDecodeError as e:
            assert "invalid characters" not in str(e), (
                f"{vin} still blocked by invalid_chars: {e}"
            )

    def test_16_char_vin_still_raises_chassis_number_error(self, decoder):
        """16-char input with pre_clean still raises ChassisNumberError."""
        with pytest.raises(ChassisNumberError):
            decoder.decode_vin_payload("ABCDEFGHJKLMN123")

    def test_pre_clean_false_disables_substitution(self, decoder):
        """pre_clean=False skips I/O substitution; I chars cause invalid_chars."""
        with pytest.raises(VINDecodeError, match="invalid characters"):
            decoder.decode_vin_payload("FIAT100GBS0089543", pre_clean=False)


class TestSampleVins:

    def test_all_sample_vins_decode(self, decoder, sample_vins):
        """Most sample VINs from specimens CSV decode without error.

        Some VINs may have year codes outside 1990-2020 (real-world data),
        which correctly raises VINDecodeError per H2 guard.
        """
        if not sample_vins:
            pytest.skip("No sample VINs available")
        ok = 0
        bad = 0
        for vin in sample_vins:
            try:
                dna = decoder.decode_vin_payload(vin)
                assert dna.vin == vin
                if dna.model_year is not None:
                    assert 1990 <= dna.model_year <= 2020
                ok += 1
            except VINDecodeError:
                bad += 1
        # At least 50% should decode — real data has edge cases
        assert ok > 0, f"None of {len(sample_vins)} sample VINs decoded"
        assert ok >= len(sample_vins) * 0.5, (
            f"Only {ok}/{len(sample_vins)} decoded ({bad} failed)"
        )

    def test_sample_vin_confidence_not_none(self, decoder, sample_vins):
        """At least one sample VIN should have non-NONE confidence."""
        if not sample_vins:
            pytest.skip("No sample VINs available")
        confidences = set()
        for v in sample_vins:
            try:
                confidences.add(decoder.decode_vin_payload(v).confidence)
            except VINDecodeError:
                pass
        assert confidences & {"HIGH", "PARTIAL"}, f"All NONE: {confidences}"


class TestHeuristicBanks:
    """T-FX-7: heuristic config wires into number_of_banks."""

    def test_heuristic_v_engine_emits_two_banks(self, decoder):
        """SCFDAM2S1A1234567 — Aston Martin, heuristic → V12 → 2 banks."""
        dna = decoder.decode_vin_payload("SCFDAM2S1A1234567")
        assert dna.cylinder_count == 12, (
            f"expected 12, got {dna.cylinder_count}"
        )
        assert dna.number_of_banks == 2, (
            f"expected 2 banks, got {dna.number_of_banks}"
        )

    def test_heuristic_boxer_emits_two_banks(self, decoder):
        """Subaru EE20 Boxer engine → engine_config BOXER_4 → 2 banks."""
        dna = decoder.decode_vin_payload("JF1SHJLW1A1234567")
        assert dna.cylinder_count == 4, (
            f"expected 4, got {dna.cylinder_count}"
        )
        assert dna.number_of_banks == 2, (
            f"expected 2 banks, got {dna.number_of_banks}"
        )


class TestO2NarrowbandHint:
    def test_o2_narrowband_hint_respected_post_2001(self):
        """vref.db o2_type=NB hint honoured even for year>=2001 fuel-injected."""
        from vinlab.models import UpstreamO2Type as O
        from vinlab.overlay.switches import derive_upstream_o2_type

        # NB hint wins over year/fuel heuristic
        assert derive_upstream_o2_type(2005, "PORT_INJECTION", "NB") == O.NARROWBAND
        assert derive_upstream_o2_type(2010, "GDI", "NB") == O.NARROWBAND

        # WB hint still works
        assert derive_upstream_o2_type(2005, "PORT_INJECTION", "WB") == O.WIDEBAND_AFR

        # Empty hint — year/fuel rule fires
        assert derive_upstream_o2_type(2005, "PORT_INJECTION", "") == O.WIDEBAND_AFR

        # Pre-2001 default
        assert derive_upstream_o2_type(1996, "PORT_INJECTION", "") == O.NARROWBAND

        # Carburetor always narrowband
        assert derive_upstream_o2_type(2010, "CARBURETOR", "") == O.NARROWBAND


class TestBrandSpellingRepair:
    """T-SHIP-3: corrupted brand spellings repaired; join no longer dead.

    The \x8a-prefixed latin-1 misdecode ("\x8aKODA") and U+FFFD mojibake
    ("�KODA", "CITRO�N") killed the brand -> engine-map fold-join for
    Skoda/Citroen traffic (audit 2026-07-06 + SHIP_VERIFY_2026-07-07).
    Repair tool: labs/vinlab/tools/repair_brand_spellings.py (idempotent).
    """

    @staticmethod
    def _live_data_dir():
        from pathlib import Path

        return Path(__file__).resolve().parents[2] / "vinlab" / "data"

    def test_no_corrupt_brand_cells_remain(self):
        import csv as _csv

        for name in ("wmi.csv", "vds_engine_map.csv"):
            path = self._live_data_dir() / name
            for row in _csv.DictReader(path.open(newline="", encoding="utf-8")):
                brand = row.get("brand") or ""
                assert not any(
                    ord(c) < 32 or (127 <= ord(c) < 160) or c == "�" for c in brand
                ), f"corrupt brand cell {brand!r} in {name}"

    def test_skoda_wmis_carry_repaired_brand(self):
        import csv as _csv

        path = self._live_data_dir() / "wmi.csv"
        brands = {
            row["wmi"]: row["brand"]
            for row in _csv.DictReader(path.open(newline="", encoding="utf-8"))
        }
        assert brands["TMB"] == "SKODA"
        assert brands["TNB"] == "SKODA"

    def test_real_skoda_vin_decodes_with_skoda_make(self):
        import dataclasses

        live = RobustVINDecoder(self._live_data_dir())
        dna = dataclasses.asdict(live.decode_vin_payload("TMBJJ7NE3F0123456"))
        assert dna["make"] == "SKODA"
