"""T-VINA-11c: a VDS engine-map row below majority_share 0.50 is not applied; the H1 fuel guard still reads it.

Held-out evidence (Cowork, C:/4DApp/recheck/T-VINA-11c/heldout_disp.py): below 0.50 the row's engine code matches
the registry 0.336 and its displacement (+-0.1 L) 0.497 of 39,867 petrol VINs. Tags: NEW fails on the base (the
weak row is applied; no _weak_share); PIN passes on the base and after.
"""

from __future__ import annotations

import pytest

from vinlab.decoder import RobustVINDecoder, VINDecodeError
from vinlab.models import VinConfidence

# AUDI ZZZ4B: engine AEB, 2.4 L V6/6, majority_share 0.230 (a VAG ZZZ filler key holds the model code only).
AEB_VIN = "WAUZZZ4BZYN125879"
# AUDI ZZZ8G: engine NG, 2.8 L V6/6, majority_share 0.286.
NG_VIN = "WAUZZZ8GZNA003486"
WEAK_KEY = "AUDI_ZZZ4B"


@pytest.mark.parametrize("vin", [AEB_VIN, NG_VIN])
def test_weak_row_is_not_applied(decoder, vin):
    """NEW: no displacement or cylinder count from a weak row; the grade is PARTIAL (brand and year stay)."""
    dna = decoder.decode_vin_payload(vin)
    assert dna.engine_displacement_liters == 0.0
    assert dna.cylinder_count == 0
    assert dna.confidence == VinConfidence.PARTIAL
    assert dna.make == "Audi"


def test_the_same_row_above_the_floor_is_applied(data_dir):
    """PIN: raising the one row's share to 0.50 (the floor itself) applies it again (vref.db AEB: 1.781 L, 4 cylinders)."""
    decoder = RobustVINDecoder(data_dir)
    decoder.vds_full_exact_index[WEAK_KEY]["majority_share"] = "0.500"
    dna = decoder.decode_vin_payload(AEB_VIN)
    assert dna.engine_displacement_liters == 1.781
    assert dna.cylinder_count == 4


def test_h1_reads_a_weak_row_first(data_dir):
    """PIN: a weak row that says DIESEL still puts the VIN out of scope (H1 runs before the floor)."""
    decoder = RobustVINDecoder(data_dir)
    decoder.vds_full_exact_index[WEAK_KEY]["fuel_system_type"] = "DIESEL"
    with pytest.raises(VINDecodeError, match="Fuel type out of scope"):
        decoder.decode_vin_payload(AEB_VIN)


@pytest.mark.parametrize(
    ("share", "weak"),
    [("0.499", True), ("0.230", True), ("0.500", False), ("0.900", False), ("", False), ("n/a", False)],
)
def test_weak_share_boundary(share, weak):
    """NEW: strictly below 0.50 is weak; 0.50, a blank and an unparsable share are not."""
    from vinlab.decoder import _weak_share

    assert _weak_share({"majority_share": share}) is weak
