"""T-VINA-3 (F-C6-4): a vref.db row is applied only inside its model-year window."""

import sqlite3

import pytest

from vinlab.models import EuroEmissionCategory, VinConfidence

OUT_OF_WINDOW = [
    "JF1BG5LJ4SG009089",  # Subaru, decoded 1995, EJ20 row 1998-2010
    "JF1GF8LJ4TG036967",  # Subaru, decoded 1996, EJ20 row 1998-2010
]


@pytest.mark.parametrize("vin", OUT_OF_WINDOW)
def test_row_outside_its_window_is_not_applied(decoder, vin):
    dna = decoder.decode_vin_payload(vin)
    assert dna.euro_emission_category != EuroEmissionCategory.EURO_4
    assert dna.confidence != VinConfidence.HIGH


def test_every_vref_row_has_a_window(data_dir):
    con = sqlite3.connect(data_dir / "vref.db")
    bad = con.execute("select count(*) from engine_ref where my_start is null or my_end is null or my_start > my_end").fetchone()[0]
    assert bad == 0
