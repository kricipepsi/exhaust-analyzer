"""T-VINA-10 (F-C6-1, F-D1-13): with the euro norm unknown, the era follows the model year (wiki §10.8).

The euro is known only when the applied (in-window) vref.db row states a recognised euro_norm. Every test decodes real
VINs against a tmp_path copy of the shipped vref.db, with one engine_ref row set by the test where it says so.
"""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest

import vinlab.decoder
from vinlab.decoder import RobustVINDecoder
from vinlab.models import EuroEmissionCategory, Horizon, VinConfidence, VinDNA
from vinlab.overlay.horizon import _year_to_horizon

# F20C2 not in vref.db, model year 2005, NATURALLY_ASPIRATED 2.0 L.
NO_ROW_2005_VIN = "JHMAP11305S202318"
# G15SF not in vref.db, model year 1995.
NO_ROW_1995_VIN = "KLATF19T1SB604957"
# Z5 not in vref.db, no model year (position 10 is "0").
NO_YEAR_VIN = "JMZBA145201537959"
# EJ20 row 1998-2010 euro4, model year 2003, HIGH with no flag on the shipped db.
EURO4_VIN = "JF1GG9LK43G020691"
# euro5 row, model year 2010, HIGH on the shipped db.
EURO5_VIN = "VF7SA5FR8AW511081"
# 1KR-FE row 2005-2020 euro4, no model year: the row is applied (no year to compare).
NO_YEAR_ROW_VIN = "JTDJG18C40N041061"
# F16D3 row 2003-2020, model year 2008.
F16D3_VIN = "KL1NF356J8K002340"
# 14K4F row 1991-2006, model year 2010: the row is outside its window.
OUT_OF_WINDOW_VIN = "SARRFMNHMAD141869"
# RFK row 2003-2020, model year 2008.
RFK_VIN = "VF33BRFKC83559254"


@pytest.fixture()
def vref_copy(data_dir, tmp_path):
    """Return a decoder on a tmp_path copy of vref.db after running the given SQL (if any) on the copy."""

    def make(sql: str | None = None, params: tuple = ()) -> RobustVINDecoder:
        path: Path = tmp_path / "vref.db"
        shutil.copyfile(data_dir / "vref.db", path)
        if sql is not None:
            conn = sqlite3.connect(path)
            try:
                conn.execute(sql, params)
                conn.commit()
            finally:
                conn.close()
        decoder = RobustVINDecoder(data_dir)
        decoder.db_path = path
        return decoder

    return make


def _decode(decoder: RobustVINDecoder, vin: str, monkeypatch) -> tuple[VinDNA, list[str]]:
    """Decode and return the confidence flags too (they are not serialised; VIN_VOCABULARY.md §4)."""
    seen: list[str] = []
    compute = decoder._compute_confidence

    def spy(conf_flags: list[str]) -> VinConfidence:
        seen.extend(conf_flags)
        return compute(conf_flags)

    monkeypatch.setattr(decoder, "_compute_confidence", spy)
    return decoder.decode_vin_payload(vin), seen


def test_no_row_2005_takes_adaptive_from_year(vref_copy, monkeypatch):
    dna, flags = _decode(vref_copy(), NO_ROW_2005_VIN, monkeypatch)
    assert dna.model_year == 2005
    assert dna.resolved_horizon == Horizon.ADAPTIVE
    assert dna.stress_idle_rpm_target == 3500  # ADAPTIVE fallback, not the EURO_1 NA 3000
    assert dna.euro_emission_category == EuroEmissionCategory.EURO_1
    assert "euro_unknown" in flags


def test_no_row_1995_stays_legacy(vref_copy, monkeypatch):
    # PIN
    dna, _ = _decode(vref_copy(), NO_ROW_1995_VIN, monkeypatch)
    assert dna.resolved_horizon == Horizon.LEGACY
    assert dna.stress_idle_rpm_target == 3000


def test_no_year_no_row_stays_legacy_with_flag(vref_copy, monkeypatch):
    dna, flags = _decode(vref_copy(), NO_YEAR_VIN, monkeypatch)
    assert dna.model_year is None
    assert dna.resolved_horizon == Horizon.LEGACY
    assert dna.stress_idle_rpm_target == 3000
    assert "euro_unknown" in flags


def test_euro4_row_gives_adaptive_without_flag(vref_copy, monkeypatch):
    # PIN
    dna, flags = _decode(vref_copy(), EURO4_VIN, monkeypatch)
    assert dna.euro_emission_category == EuroEmissionCategory.EURO_4
    assert dna.resolved_horizon == Horizon.ADAPTIVE
    assert dna.confidence == VinConfidence.HIGH
    assert "euro_unknown" not in flags


def test_euro5_row_stays_modern(vref_copy, monkeypatch):
    # PIN: a recognised euro5 decides, not the 2010 model year (ADAPTIVE)
    dna, flags = _decode(vref_copy(), EURO5_VIN, monkeypatch)
    assert dna.model_year == 2010
    assert dna.euro_emission_category == EuroEmissionCategory.EURO_5
    assert dna.resolved_horizon == Horizon.MODERN
    assert "euro_unknown" not in flags


def test_euro4_row_keeps_euro_stress_rule(vref_copy):
    # PIN: EURO_4 NA >= 2.0 L is 4000 by the euro rule; the ADAPTIVE fallback would give 3500
    decoder = vref_copy("UPDATE engine_ref SET displacement_cc = 2000 WHERE engine_code = 'EJ20'")
    dna = decoder.decode_vin_payload(EURO4_VIN)
    assert dna.engine_displacement_liters == 2.0
    assert dna.stress_idle_rpm_target == 4000


@pytest.mark.parametrize(
    ("euro_norm", "euro", "horizon", "stress", "flagged"),
    [
        # recognised after strip() and lower(): the euro rule decides (EURO_4 NA >= 2.0 L)
        (" EuRo 4 ", EuroEmissionCategory.EURO_4, Horizon.ADAPTIVE, 4000, False),
        # blank: unknown, the 2003 model year decides and the stress RPM takes the ADAPTIVE fallback
        ("", EuroEmissionCategory.EURO_1, Horizon.ADAPTIVE, 3500, True),
        ("  ", EuroEmissionCategory.EURO_1, Horizon.ADAPTIVE, 3500, True),
    ],
    ids=["mixed_case_spaces", "empty", "whitespace"],
)
def test_euro_norm_is_matched_after_strip_and_lower(vref_copy, monkeypatch, euro_norm, euro, horizon, stress, flagged):
    decoder = vref_copy(
        "UPDATE engine_ref SET euro_norm = ?, displacement_cc = 2000 WHERE engine_code = 'EJ20'", (euro_norm,)
    )
    dna, flags = _decode(decoder, EURO4_VIN, monkeypatch)
    assert dna.euro_emission_category == euro
    assert dna.resolved_horizon == horizon
    assert dna.stress_idle_rpm_target == stress
    assert ("euro_unknown" in flags) is flagged


def test_no_year_euro5_row_gives_modern(vref_copy, monkeypatch):
    # no model year, but the applied row states euro5: the euro decides, not the no-year LEGACY default
    decoder = vref_copy("UPDATE engine_ref SET euro_norm = 'euro5' WHERE engine_code = '1KR-FE'")
    dna, flags = _decode(decoder, NO_YEAR_ROW_VIN, monkeypatch)
    assert dna.model_year is None
    assert dna.euro_emission_category == EuroEmissionCategory.EURO_5
    assert dna.resolved_horizon == Horizon.MODERN
    assert "euro_unknown" not in flags


def test_null_euro_row_takes_year(vref_copy, monkeypatch):
    decoder = vref_copy("UPDATE engine_ref SET euro_norm = NULL WHERE engine_code = 'F16D3'")
    dna, flags = _decode(decoder, F16D3_VIN, monkeypatch)
    assert dna.model_year == 2008
    assert dna.resolved_horizon == Horizon.ADAPTIVE
    assert dna.stress_idle_rpm_target == 3500
    assert dna.euro_emission_category == EuroEmissionCategory.EURO_1
    assert "euro_unknown" in flags


def test_out_of_window_row_year_decides(vref_copy, monkeypatch):
    # the row's euro5 would give MODERN; the row is not applied, so the 2010 year gives ADAPTIVE
    decoder = vref_copy("UPDATE engine_ref SET euro_norm = 'euro5' WHERE engine_code = '14K4F'")
    dna, flags = _decode(decoder, OUT_OF_WINDOW_VIN, monkeypatch)
    assert dna.model_year == 2010
    assert "vref_year_out_of_window" in flags
    assert dna.resolved_horizon == Horizon.ADAPTIVE
    assert "euro_unknown" in flags


def test_unrecognised_euro_string_is_unknown(vref_copy, monkeypatch):
    decoder = vref_copy("UPDATE engine_ref SET euro_norm = 'Euro IV' WHERE engine_code = 'RFK'")
    dna, flags = _decode(decoder, RFK_VIN, monkeypatch)
    assert dna.model_year == 2008
    assert dna.resolved_horizon == Horizon.ADAPTIVE
    assert dna.euro_emission_category == EuroEmissionCategory.EURO_1
    assert dna.stress_idle_rpm_target == 3500
    assert "euro_unknown" in flags


def test_flag_alone_demotes_high_to_partial(vref_copy):
    decoder = vref_copy("UPDATE engine_ref SET euro_norm = NULL WHERE engine_code = 'EJ20'")
    dna = decoder.decode_vin_payload(EURO4_VIN)
    assert dna.confidence == VinConfidence.PARTIAL
    assert dna.resolved_horizon == Horizon.ADAPTIVE  # from the 2003 model year


def test_year_bands_follow_wiki_10_8():
    # PIN: labs/vinlab/wiki/10_decode_scope_rules.md §10.8
    assert _year_to_horizon(1990) == Horizon.LEGACY
    assert _year_to_horizon(2000) == Horizon.LEGACY
    assert _year_to_horizon(2001) == Horizon.ADAPTIVE
    assert _year_to_horizon(2010) == Horizon.ADAPTIVE
    assert _year_to_horizon(2011) == Horizon.MODERN


def test_decoder_calls_the_cited_year_helper(vref_copy, monkeypatch):
    monkeypatch.setattr(vinlab.decoder, "_year_to_horizon", lambda year: Horizon.MODERN)
    dna = vref_copy().decode_vin_payload(NO_ROW_2005_VIN)
    assert dna.resolved_horizon == Horizon.MODERN
