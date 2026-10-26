"""P4 probe for apps/ui survivors. Run from apps/ui with labs/comlab on sys.path:
  cd apps/ui && PYTHONPATH=../../labs/comlab python -m pytest -q -p no:cacheprovider ../../audit/scratch/P4/probes/test_p4_ui_probes.py
"""
import pytest
from ui_payload import build_diagnose_payload


@pytest.mark.parametrize("status,expected", [("Normal", False), ("Recently cleared (<50 mi)", True)])
def test_dtc_memory_status_maps_to_codes_cleared(status, expected):
    """Kills ui_payload.py:1054 `==` -> `!=` (mutant ui.build_diagnose_payload#0051). 4DLab_UI_FieldMap.md:232:
    'DTC Memory Status | Normal · Recently cleared (<50 mi) | DTCLab freeze_frame.ff_codes_cleared_invalidated'."""
    p = build_diagnose_payload({"vin": "", "dna_module": False, "gas_module": False, "obd_module": False,
                                "dtc_module": True, "dtc_memory_status": status})
    assert p["dtc"]["codes_cleared"] is expected
