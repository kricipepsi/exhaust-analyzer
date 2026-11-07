"""T-VINA-7a: lookup_engine_ref closes every connection it opens (F-C6-14); a blank-brand WMI grades NONE (F-C6-9).

Tags: NEW fails on the base (ResourceWarning on each lookup; a blank-brand WMI grades PARTIAL).
"""

from __future__ import annotations

import gc
import warnings

import pytest

from vinlab.db.tecdoc_query import lookup_engine_ref
from vinlab.models import VinConfidence


@pytest.mark.parametrize(
    ("code", "found"),
    [("AEB", "AEB"), ("aeb", "AEB"), ("NO-SUCH-ENGINE-9", None)],  # exact, normalised, miss
)
def test_lookup_leaves_no_connection_open(data_dir, code, found):
    """NEW: no ResourceWarning 'unclosed database' after an exact, a normalised and a missed lookup."""
    gc.collect()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ResourceWarning)
        row = lookup_engine_ref(data_dir / "vref.db", code)
        del row
        gc.collect()
    unclosed = [str(w.message) for w in caught if "unclosed database" in str(w.message)]
    assert unclosed == []
    result = lookup_engine_ref(data_dir / "vref.db", code)
    assert (result or {}).get("engine_code") == found


def test_blank_brand_wmi_grades_none(decoder):
    """NEW: WMI 002 has a blank brand: no engine, every engine field at its default, grade NONE."""
    dna = decoder.decode_vin_payload("002ZZZZZ0Y1234567")
    assert dna.make == ""
    assert dna.engine_displacement_liters == 0.0
    assert dna.cylinder_count == 0
    assert dna.confidence == VinConfidence.NONE
