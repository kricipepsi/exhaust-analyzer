"""T-VINA-14: a vref.db row keeps a map BOXER's second bank (R1) and a TecDoc-stated induction (R2).
T-VINA-16 R3: a vref.db row's positive cylinder_count replaces the map's count; NULL or 0 keeps it.

The fixture tests decode real VINs against a tmp_path copy of the shipped vref.db with one engine_ref row set by the
test. The real-VIN tests at the end decode against the shipped vref.db itself.
"""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest

from vinlab.decoder import RobustVINDecoder
from vinlab.models import InductionType, PrimaryLoadCalculation

# EJ25, map BOXER_4, model year 2002; the shipped EJ25 row has is_v_engine 0 (TecDoc writes BOXER as 0).
BOXER_VIN = "JF1BH9LJB2G051603"
# XFX, map V6, model year 2008 (row window 2000-2020).
V6_VIN = "VF38CXFXA81270589"
# B5254S, map I5, model year 1997 (row window 1991-2006).
I5_VIN = "YV1LW5502V2373912"
# AZQ, map row with no displacement and no cylinder count, model year 2003. At TecDoc's 1198 cc the Skoda brand rule
# reads a 1.2 TSI (I3 TURBOCHARGED); TecDoc states AZQ NATURALLY_ASPIRATED.
AZQ_VIN = "TMBCY46Y733811341"
# AEB, map V6/6 (2.4 L), model year 2000 (row window 1995-2006); TecDoc states 4 cylinders (1781 cc).
AEB_VIN = "WAUZZZ4BZYN125879"

AZQ_ROW = (
    "INSERT OR REPLACE INTO engine_ref (engine_code, brand, displacement_cc, my_start, my_end, era_bucket, "
    "has_turbo, is_v_engine, o2_type, induction_type, fuel_delivery_type) "
    "VALUES ('AZQ', 'SKODA', 1198, 2001, 2009, 'ERA_OBDII_EARLY', 0, 0, '', ?, 'PORT_INJECTION')"
)


@pytest.fixture()
def vref_copy(data_dir, tmp_path):
    """Return a decoder on a tmp_path copy of vref.db after running the given SQL on the copy."""

    def make(sql: str, params: tuple = ()) -> RobustVINDecoder:
        path: Path = tmp_path / "vref.db"
        shutil.copyfile(data_dir / "vref.db", path)
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


def test_vref_zero_with_map_boxer_gives_two_banks(vref_copy):
    decoder = vref_copy("UPDATE engine_ref SET is_v_engine = 0 WHERE engine_code = 'EJ25'")
    assert decoder.decode_vin_payload(BOXER_VIN).number_of_banks == 2


def test_vref_zero_with_map_v6_gives_one_bank(vref_copy):
    # PIN: the survey found the map V/W wrong where TecDoc says not V (R1); the row's 0 wins.
    decoder = vref_copy("UPDATE engine_ref SET is_v_engine = 0 WHERE engine_code = 'XFX'")
    assert decoder.decode_vin_payload(V6_VIN).number_of_banks == 1


def test_vref_one_gives_two_banks(vref_copy):
    # PIN
    decoder = vref_copy("UPDATE engine_ref SET is_v_engine = 1 WHERE engine_code = 'B5254S'")
    assert decoder.decode_vin_payload(I5_VIN).number_of_banks == 2


def test_stated_na_is_not_replaced_by_turbo_hint(vref_copy):
    dna = vref_copy(AZQ_ROW, ("NATURALLY_ASPIRATED",)).decode_vin_payload(AZQ_VIN)
    assert dna.cylinder_count == 3
    assert dna.induction_type == InductionType.NATURALLY_ASPIRATED


def test_null_induction_takes_the_hint(vref_copy):
    # PIN
    dna = vref_copy(AZQ_ROW, (None,)).decode_vin_payload(AZQ_VIN)
    assert dna.cylinder_count == 3
    assert dna.induction_type == InductionType.TURBOCHARGED


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_induction_takes_the_hint(vref_copy, blank):
    # Review correction 02 (c): a blank induction_type states nothing, like NULL.
    dna = vref_copy(AZQ_ROW, (blank,)).decode_vin_payload(AZQ_VIN)
    assert dna.cylinder_count == 3
    assert dna.induction_type == InductionType.TURBOCHARGED


def test_real_boxer_vin_has_two_banks(decoder):
    assert decoder.decode_vin_payload(BOXER_VIN).number_of_banks == 2


def test_real_azq_vin_after_merge_is_na_and_maf_only(decoder):
    dna = decoder.decode_vin_payload(AZQ_VIN)
    assert dna.engine_displacement_liters == 1.198  # the merged AZQ row is applied
    assert dna.induction_type == InductionType.NATURALLY_ASPIRATED
    assert dna.air_metering_architecture.primary_load_calculation == PrimaryLoadCalculation.MAF_ONLY


def test_vref_count_replaces_map_count(vref_copy):
    decoder = vref_copy("UPDATE engine_ref SET cylinder_count = 4 WHERE engine_code = 'XFX'")
    assert decoder.decode_vin_payload(V6_VIN).cylinder_count == 4


@pytest.mark.parametrize("count", [None, 0])
def test_null_or_zero_vref_count_keeps_map_count(vref_copy, count):
    # PIN: a NULL or 0 count states nothing (R3); the map's 6 stays and the fallback does not run (it would say 4).
    decoder = vref_copy("UPDATE engine_ref SET cylinder_count = ? WHERE engine_code = 'AEB'", (count,))
    assert decoder.decode_vin_payload(AEB_VIN).cylinder_count == 6


@pytest.mark.parametrize("displacement_cc", [1198, 3000])
def test_vref_count_with_blank_map_count_skips_the_heuristic(vref_copy, displacement_cc):
    # The map states no count; the heuristic would say I3 TURBOCHARGED at 1198 cc and V6 (two banks) at 3000 cc.
    decoder = vref_copy(
        "UPDATE engine_ref SET cylinder_count = 6, induction_type = NULL, displacement_cc = ? WHERE engine_code = 'AZQ'",
        (displacement_cc,),
    )
    dna = decoder.decode_vin_payload(AZQ_VIN)
    assert dna.cylinder_count == 6
    assert dna.induction_type == InductionType.NATURALLY_ASPIRATED
    assert dna.number_of_banks == 1


@pytest.mark.parametrize(
    ("vin", "cylinders", "banks"),
    [
        (AEB_VIN, 4, 1),  # AEB: TecDoc 4, map V6/6
        ("WAUZZZ8GZNA003486", 5, 1),  # NG: TecDoc 5, map V6/6
        ("JSAFTD62V00115689", 6, 2),  # H25A: row inserted by T-VINA-16, TecDoc 6 and is_v_engine 1, map blank
    ],
)
def test_real_vin_takes_the_tecdoc_count(decoder, vin, cylinders, banks):
    dna = decoder.decode_vin_payload(vin)
    assert dna.cylinder_count == cylinders
    assert dna.number_of_banks == banks
